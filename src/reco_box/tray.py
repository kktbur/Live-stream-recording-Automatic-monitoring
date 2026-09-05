from __future__ import annotations

from pathlib import Path

from PySide6.QtCore import QCoreApplication, QObject, QTimer, QUrl
from PySide6.QtGui import QDesktopServices, QIcon
from PySide6.QtWidgets import QApplication, QMenu, QSystemTrayIcon

from .localization import LocalizationController
from .recording import RecordingManager
from .room_model import RoomListModel


class TrayController(QObject):
    def __init__(
        self,
        app: QApplication,
        window: QObject,
        rooms: RoomListModel,
        recorder: RecordingManager,
        icon_path: Path,
        default_recording_dir: Path,
        localization: LocalizationController,
    ) -> None:
        super().__init__()
        self.app = app
        self.window = window
        self.rooms = rooms
        self.recorder = recorder
        self.default_recording_dir = Path(default_recording_dir)
        self.tray = QSystemTrayIcon(QIcon(str(icon_path)), app)
        self.tray.setToolTip("Reco Box")

        self.localization = localization
        self._rebuild_menu()
        self.localization.languageChanged.connect(self._rebuild_menu)
        self.tray.activated.connect(self._activated)
        self.tray.show()

    def _text(self, source: str) -> str:
        return QCoreApplication.translate("TrayController", source)

    def _rebuild_menu(self) -> None:
        menu = QMenu()
        menu.addAction(self._text("显示 Reco Box"), self.show_window)
        menu.addSeparator()
        menu.addAction(self._text("继续全部监控"), lambda: self.rooms.setAllEnabled(True))
        menu.addAction(self._text("暂停全部监控"), self.recorder.stopAllAndPause)
        menu.addAction(self._text("打开录制目录"), self.open_recording_dir)
        menu.addSeparator()
        menu.addAction(self._text("退出"), self.exit_application)
        self.tray.setContextMenu(menu)

    def show_window(self) -> None:
        self.window.show()
        self.window.raise_()
        self.window.requestActivate()

    def open_recording_dir(self) -> None:
        self.default_recording_dir.mkdir(parents=True, exist_ok=True)
        QDesktopServices.openUrl(QUrl.fromLocalFile(str(self.default_recording_dir)))

    def _activated(self, reason: QSystemTrayIcon.ActivationReason) -> None:
        if reason in (
            QSystemTrayIcon.ActivationReason.Trigger,
            QSystemTrayIcon.ActivationReason.DoubleClick,
        ):
            self.show_window()

    def exit_application(self) -> None:
        if not self.recorder.processes:
            self.app.quit()
            return
        self.tray.setToolTip(self._text("Reco Box · 正在安全停止录制"))
        self.recorder.stop_all()
        self._wait_for_recorders()

    def _wait_for_recorders(self) -> None:
        if not self.recorder.processes and not self.recorder.converting_rooms:
            self.app.quit()
            return
        QTimer.singleShot(250, self._wait_for_recorders)

