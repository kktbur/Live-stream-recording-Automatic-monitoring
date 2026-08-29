from __future__ import annotations

import os
import sys
from pathlib import Path

from platformdirs import user_data_path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from .monitor import MonitoringCoordinator
from .preview import PreviewController
from .recording import RecordingManager
from .resolver import DouyinLiveRecorderResolver
from .resources import application_resource, configure_bundled_runtime, package_resource
from .room_model import RoomFilterProxyModel, RoomListModel
from .self_check import run_self_check
from .storage import Database
from .tray import TrayController
from .view_models import (
    DesktopActions,
    EventLogModel,
    LegacyImportController,
    RecordingHistoryModel,
    SettingsController,
)


def data_directory() -> Path:
    override = os.environ.get("RECO_BOX_DATA_DIR", "").strip()
    return Path(override) if override else Path(user_data_path("Reco Box", "Reco Box"))


def project_asset(name: str) -> Path:
    return application_resource("assets", name)


def main() -> int:
    os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
    # The FFmpeg Qt backend supports the FLV/HLS formats commonly returned by
    # livestream platforms. Windows Media Foundation often opens them without
    # an explicit error but never produces a video frame.
    os.environ.setdefault("QT_MEDIA_BACKEND", "ffmpeg")
    configure_bundled_runtime()
    if "--self-test" in sys.argv:
        return run_self_check(data_directory())
    app = QApplication(sys.argv)
    app.setApplicationName("Reco Box")
    app.setOrganizationName("Reco Box")
    app.setQuitOnLastWindowClosed(False)

    icon = project_asset("reco-box-icon-final.png")
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))

    database = Database(data_directory() / "reco_box.db")
    rooms = RoomListModel(database)
    room_proxy = RoomFilterProxyModel(rooms)
    history = RecordingHistoryModel(database)
    event_log = EventLogModel(database)
    settings = SettingsController(database)
    desktop_actions = DesktopActions()
    legacy_import = LegacyImportController(database, rooms, settings)
    recorder = RecordingManager(rooms, database)
    monitor = MonitoringCoordinator(rooms, DouyinLiveRecorderResolver())
    preview = PreviewController(monitor)
    monitor.liveDetected.connect(recorder.start_for_room)
    recorder.retryRequested.connect(monitor.schedule_retry)
    recorder.recordingCompleted.connect(history.refresh)
    recorder.recordingCompleted.connect(event_log.refresh)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("roomModel", rooms)
    engine.rootContext().setContextProperty("roomProxyModel", room_proxy)
    engine.rootContext().setContextProperty("recordingManager", recorder)
    engine.rootContext().setContextProperty("historyModel", history)
    engine.rootContext().setContextProperty("eventLogModel", event_log)
    engine.rootContext().setContextProperty("settingsController", settings)
    engine.rootContext().setContextProperty("desktopActions", desktop_actions)
    engine.rootContext().setContextProperty("legacyImport", legacy_import)
    engine.rootContext().setContextProperty("monitorCoordinator", monitor)
    engine.rootContext().setContextProperty("previewController", preview)
    qml_path = package_resource("ui", "Main.qml")
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        return 1
    default_recording_dir = Path.home() / "Videos" / "Reco Box"
    tray = TrayController(
        app,
        engine.rootObjects()[0],
        rooms,
        recorder,
        icon,
        default_recording_dir,
    )
    app.setProperty("trayController", tray)
    app.setProperty("monitorCoordinator", monitor)
    app.setProperty("recordingManager", recorder)
    monitor.start()
    return app.exec()


if __name__ == "__main__":
    raise SystemExit(main())
