from __future__ import annotations

import os
import sys
from pathlib import Path

from platformdirs import user_data_path
from PySide6.QtCore import QUrl
from PySide6.QtGui import QIcon
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtWidgets import QApplication

from . import __version__
from .localization import LocalizationController
from .monitor import MonitoringCoordinator
from .preview import PreviewController
from .rate_limit import ResolverRateLimitConfig
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
    app.setApplicationVersion(__version__)
    app.setQuitOnLastWindowClosed(False)

    icon = project_asset("reco-box-icon-final.png")
    if icon.exists():
        app.setWindowIcon(QIcon(str(icon)))

    database_path = data_directory() / "reco_box.db"
    existing_database = database_path.exists()
    database = Database(database_path)
    localization = LocalizationController(app, database, existing_database)
    rooms = RoomListModel(database)
    room_proxy = RoomFilterProxyModel(rooms)
    history = RecordingHistoryModel(database)
    event_log = EventLogModel(database)
    settings = SettingsController(database)
    desktop_actions = DesktopActions()
    legacy_import = LegacyImportController(database, rooms, settings)
    recorder = RecordingManager(rooms, database)
    monitor = MonitoringCoordinator(
        rooms,
        DouyinLiveRecorderResolver(),
        rate_limit_config=_resolver_rate_limit_config(settings),
    )
    _connect_resolver_rate_limit_settings(settings, monitor)
    preview = PreviewController(monitor)
    monitor.liveDetected.connect(recorder.start_for_room)
    monitor.streamOffline.connect(recorder.handle_stream_offline)
    recorder.retryRequested.connect(monitor.schedule_retry)
    recorder.recordingCompleted.connect(history.refresh)
    recorder.recordingCompleted.connect(event_log.refresh)

    engine = QQmlApplicationEngine()
    engine.rootContext().setContextProperty("roomModel", rooms)
    engine.rootContext().setContextProperty("applicationVersion", __version__)
    engine.rootContext().setContextProperty("roomProxyModel", room_proxy)
    engine.rootContext().setContextProperty("recordingManager", recorder)
    engine.rootContext().setContextProperty("historyModel", history)
    engine.rootContext().setContextProperty("eventLogModel", event_log)
    engine.rootContext().setContextProperty("settingsController", settings)
    engine.rootContext().setContextProperty("desktopActions", desktop_actions)
    engine.rootContext().setContextProperty("legacyImport", legacy_import)
    engine.rootContext().setContextProperty("monitorCoordinator", monitor)
    engine.rootContext().setContextProperty("previewController", preview)
    engine.rootContext().setContextProperty("localizationController", localization)
    qml_path = package_resource("ui", "Main.qml")
    engine.load(QUrl.fromLocalFile(str(qml_path)))
    if not engine.rootObjects():
        return 1
    localization.set_engine(engine)
    default_recording_dir = Path.home() / "Videos" / "Reco Box"
    tray = TrayController(
        app,
        engine.rootObjects()[0],
        rooms,
        recorder,
        icon,
        default_recording_dir,
        localization,
    )
    app.setProperty("trayController", tray)
    app.setProperty("monitorCoordinator", monitor)
    app.setProperty("recordingManager", recorder)
    monitor.start()
    return app.exec()


def _resolver_rate_limit_config(settings: SettingsController) -> ResolverRateLimitConfig:
    return ResolverRateLimitConfig(
        max_resolver_concurrency=settings.resolverMaxConcurrency,
        default_platform_concurrency=settings.resolverPlatformConcurrency,
        default_platform_interval_seconds=settings.resolverPlatformIntervalSeconds,
    )


def _connect_resolver_rate_limit_settings(
    settings: SettingsController, monitor: MonitoringCoordinator
) -> None:
    settings.defaultsChanged.connect(
        lambda: monitor.update_rate_limit_config(_resolver_rate_limit_config(settings))
    )


if __name__ == "__main__":
    raise SystemExit(main())
