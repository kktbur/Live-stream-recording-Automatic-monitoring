import os
from pathlib import Path

os.environ.setdefault("QT_QPA_PLATFORM", "offscreen")
os.environ.setdefault("QT_QUICK_CONTROLS_STYLE", "Basic")
os.environ.setdefault("QT_MEDIA_BACKEND", "ffmpeg")

from PySide6.QtCore import QMetaObject, QObject, QUrl
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtQuick import QQuickItem
from PySide6.QtTest import QTest

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


def _find_visual_item(item: QQuickItem, object_name: str) -> QQuickItem | None:
    if item.objectName() == object_name:
        return item
    for child in item.childItems():
        found = _find_visual_item(child, object_name)
        if found is not None:
            return found
    return None


def test_main_qml_loads(tmp_path) -> None:
    app = QGuiApplication.instance() or QGuiApplication([])
    database = Database(tmp_path / "qml-smoke.db")
    model = RoomListModel(database)
    assert model.addRoom("https://live.bilibili.com/6", "大文件测试", str(tmp_path))
    room_id = model.rooms[0].id
    model.update_recording_progress(room_id, 60, 3 * 1024 * 1024 * 1024)
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
    preview = PreviewController(monitor)
    engine.rootContext().setContextProperty("previewController", preview)
    qml_path = Path(__file__).parents[1] / "src" / "reco_box" / "ui" / "Main.qml"
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    QTest.qWait(150)
    app.processEvents()

    roots = engine.rootObjects()
    assert roots, "Main.qml failed to create its root window"
    root = roots[0]
    size_label = _find_visual_item(root.contentItem(), "roomFileSize")
    assert size_label is not None
    assert size_label.property("text") == "3.00 GB"

    preview_button = _find_visual_item(root.contentItem(), "previewButton")
    assert preview_button is not None
    assert QMetaObject.invokeMethod(preview_button, "clicked")
    app.processEvents()
    assert "尚未取得直播流" in preview.error

    root.setProperty("visible", False)
    engine.deleteLater()
    app.processEvents()
    app.quit()


def test_room_card_uses_large_file_safe_number_and_preview_play_action() -> None:
    qml_path = Path(__file__).parents[1] / "src" / "reco_box" / "ui" / "Main.qml"
    source = qml_path.read_text(encoding="utf-8")

    assert "required property double fileBytes" in source
    assert "previewController.play(roomId)" in source
    assert "previewController.prepare(roomId)" not in source
