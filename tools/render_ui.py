from __future__ import annotations

import os
import tempfile
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
os.environ.setdefault("QT_QUICK_BACKEND", "software")
os.environ.setdefault("QSG_RHI_BACKEND", "software")

from PySide6.QtCore import QBuffer, QByteArray, QIODevice, QMetaObject, QObject, QTimer, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickWindow

from reco_box.domain import Platform, Room, RoomStatus
from reco_box.monitor import MonitoringCoordinator
from reco_box.preview import PreviewController
from reco_box.resolver import DouyinLiveRecorderResolver
from reco_box.room_model import RoomFilterProxyModel, RoomListModel
from reco_box.storage import Database
from reco_box.view_models import (
    DesktopActions,
    EventLogModel,
    LegacyImportController,
    RecordingHistoryModel,
    SettingsController,
)

PROJECT_ROOT = Path(__file__).resolve().parents[1]
OUTPUT = PROJECT_ROOT / "artifacts" / (
    "reco-box-edit-preview-ui-refresh.png"
    if os.environ.get("RECO_BOX_RENDER_EDIT") == "1"
    else "reco-box-ui-preview-ui-refresh.png"
)


def main() -> None:
    app = QGuiApplication([])
    with tempfile.TemporaryDirectory(prefix="reco-box-preview-") as temp_dir:
        database = Database(Path(temp_dir) / "preview.db")
        database.upsert_room(
            Room(
                url="https://live.douyin.com/123456",
                platform=Platform.DOUYIN,
                streamer_name="示例主播",
                status=RoomStatus.RECORDING,
                save_root=str(Path(temp_dir) / "records"),
            )
        )
        database.upsert_room(
            Room(
                url="https://live.bilibili.com/6",
                platform=Platform.BILIBILI,
                streamer_name="等待开播",
                status=RoomStatus.OFFLINE,
                save_root=str(Path(temp_dir) / "records"),
            )
        )
        model = RoomListModel(database)
        model.update_recording_progress(
            model.rooms[0].id,
            duration=5_600,
            file_bytes=3 * 1024 * 1024 * 1024,
        )
        engine = QQmlApplicationEngine()
        engine.rootContext().setContextProperty("roomModel", model)
        room_proxy = RoomFilterProxyModel(model)
        engine.rootContext().setContextProperty("roomProxyModel", room_proxy)
        engine.rootContext().setContextProperty("historyModel", RecordingHistoryModel(database))
        engine.rootContext().setContextProperty("eventLogModel", EventLogModel(database))
        settings = SettingsController(database)
        engine.rootContext().setContextProperty("settingsController", settings)
        engine.rootContext().setContextProperty("desktopActions", DesktopActions())
        engine.rootContext().setContextProperty("recordingManager", QObject())
        engine.rootContext().setContextProperty(
            "legacyImport", LegacyImportController(database, model, settings)
        )
        monitor = MonitoringCoordinator(model, DouyinLiveRecorderResolver())
        engine.rootContext().setContextProperty("monitorCoordinator", monitor)
        engine.rootContext().setContextProperty("previewController", PreviewController(monitor))
        qml_path = PROJECT_ROOT / "src" / "reco_box" / "ui" / "Main.qml"
        engine.load(QUrl.fromLocalFile(str(qml_path)))
        if not engine.rootObjects():
            raise RuntimeError("Main.qml failed to load")
        window = engine.rootObjects()[0]
        if os.environ.get("RECO_BOX_RENDER_EDIT") == "1":
            edit_dialog = window.findChild(QObject, "editDialog")
            if edit_dialog is not None:
                QMetaObject.invokeMethod(edit_dialog, "open")

        def capture() -> None:
            try:
                OUTPUT.parent.mkdir(parents=True, exist_ok=True)
                screenshot = QQuickWindow.grabWindow(window)
                if screenshot.isNull():
                    raise RuntimeError("UI preview is empty on the selected Qt platform")
                encoded = QByteArray()
                buffer = QBuffer(encoded)
                buffer.open(QIODevice.WriteOnly)
                if not screenshot.save(buffer, "PNG"):
                    raise RuntimeError("Failed to save UI preview")
                OUTPUT.write_bytes(bytes(encoded))
            finally:
                app.quit()

        QTimer.singleShot(800, capture)
        QTimer.singleShot(5_000, app.quit)
        app.exec()
    print(OUTPUT)


if __name__ == "__main__":
    main()
