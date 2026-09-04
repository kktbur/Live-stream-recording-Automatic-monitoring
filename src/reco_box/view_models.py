from __future__ import annotations

import configparser
from pathlib import Path

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QModelIndex,
    QObject,
    Qt,
    QUrl,
    Signal,
    Slot,
)
from PySide6.QtGui import QDesktopServices
from PySide6.QtWidgets import QFileDialog

from .legacy_import import import_legacy_folder, inspect_legacy_folder
from .localization import tr
from .network import normalize_proxy
from .room_model import RoomListModel
from .storage import Database


class DictionaryListModel(QAbstractListModel):
    def __init__(self, database: Database, roles: tuple[str, ...]):
        super().__init__()
        self.database = database
        self._roles = roles
        self.items: list[dict[str, object]] = []

    def roleNames(self) -> dict[int, bytes]:
        return {Qt.UserRole + index + 1: name.encode() for index, name in enumerate(self._roles)}

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        return 0 if parent is not None and parent.isValid() else len(self.items)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self.items):
            return None
        role_index = role - Qt.UserRole - 1
        if not 0 <= role_index < len(self._roles):
            return None
        return self.items[index.row()].get(self._roles[role_index], "")


class RecordingHistoryModel(DictionaryListModel):
    def __init__(self, database: Database):
        super().__init__(
            database,
            (
                "id",
                "room_id",
                "platform",
                "streamer_name",
                "title",
                "started_at",
                "ended_at",
                "status",
                "session_dir",
                "session_dirs",
                "total_bytes",
                "error_message",
                "recovery_parts",
                "probe_status",
                "duration_seconds",
                "codec_summary",
                "probe_error",
            ),
        )
        self.refresh()

    @Slot()
    def refresh(self) -> None:
        self.beginResetModel()
        self.items = self.database.list_recordings()
        self.endResetModel()


class EventLogModel(DictionaryListModel):
    def __init__(self, database: Database):
        super().__init__(
            database,
            ("id", "room_id", "streamer_name", "level", "message", "created_at"),
        )
        self.refresh()

    @Slot()
    def refresh(self) -> None:
        self.beginResetModel()
        self.items = self.database.list_events()
        self.endResetModel()


class SettingsController(QObject):
    defaultsChanged = Signal()

    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        fallback = str(Path.home() / "Videos" / "Reco Box")
        self._default_save_root = database.get_setting("default_save_root", fallback)
        self._default_output_format = database.get_setting("default_output_format", "ts")
        self._default_quality = database.get_setting("default_quality", "原画")
        self._default_check_interval = int(
            database.get_setting("default_check_interval_seconds", "300")
        )
        self._default_segment_enabled = (
            database.get_setting("default_segment_enabled", "0") == "1"
        )
        self._default_segment_minutes = int(
            database.get_setting("default_segment_minutes", "5")
        )
        self._minimum_free_gb = int(database.get_setting("minimum_free_gb", "5"))
        self._default_proxy = database.get_setting("default_proxy", "")
        self._resolver_max_concurrency = int(
            database.get_setting("resolver_max_concurrency", "4")
        )
        self._resolver_platform_concurrency = int(
            database.get_setting("resolver_platform_concurrency", "1")
        )
        self._resolver_platform_interval_seconds = int(
            database.get_setting("resolver_platform_interval_seconds", "1")
        )

    @Property(str, notify=defaultsChanged)
    def defaultSaveRoot(self) -> str:
        return self._default_save_root

    @Property(str, notify=defaultsChanged)
    def defaultOutputFormat(self) -> str:
        return self._default_output_format

    @Property(str, notify=defaultsChanged)
    def defaultQuality(self) -> str:
        return self._default_quality

    @Property(int, notify=defaultsChanged)
    def defaultCheckInterval(self) -> int:
        return self._default_check_interval

    @Property(bool, notify=defaultsChanged)
    def defaultSegmentEnabled(self) -> bool:
        return self._default_segment_enabled

    @Property(int, notify=defaultsChanged)
    def defaultSegmentMinutes(self) -> int:
        return self._default_segment_minutes

    @Property(int, notify=defaultsChanged)
    def minimumFreeGb(self) -> int:
        return self._minimum_free_gb

    @Property(str, notify=defaultsChanged)
    def defaultProxy(self) -> str:
        return self._default_proxy

    @Property(int, notify=defaultsChanged)
    def resolverMaxConcurrency(self) -> int:
        return self._resolver_max_concurrency

    @Property(int, notify=defaultsChanged)
    def resolverPlatformConcurrency(self) -> int:
        return self._resolver_platform_concurrency

    @Property(int, notify=defaultsChanged)
    def resolverPlatformIntervalSeconds(self) -> int:
        return self._resolver_platform_interval_seconds

    @Slot(str, str, str, str, bool, str, str, str, str, str, str, result=str)
    def saveDefaults(
        self,
        save_root: str,
        output_format: str,
        quality: str,
        check_interval: str,
        segment_enabled: bool,
        segment_minutes: str,
        minimum_free_gb: str,
        default_proxy: str,
        resolver_max_concurrency: str = "4",
        resolver_platform_concurrency: str = "1",
        resolver_platform_interval_seconds: str = "1",
    ) -> str:
        if not save_root.strip():
            return tr("默认录制目录不能为空")
        try:
            interval = int(check_interval)
            minutes = int(segment_minutes)
            free_gb = int(minimum_free_gb)
            max_concurrency = int(resolver_max_concurrency)
            platform_concurrency = int(resolver_platform_concurrency)
            platform_interval = int(resolver_platform_interval_seconds)
        except ValueError:
            return tr("轮询、分段和解析限制参数必须是整数")
        if interval < 30:
            return tr("轮询间隔不能低于 30 秒")
        if minutes <= 0:
            return tr("分段分钟数必须是正整数")
        if not 1 <= free_gb <= 1024:
            return tr("磁盘保护阈值必须是 1 至 1024 GB")
        if not 1 <= max_concurrency <= 32:
            return tr("Resolver 最大并发必须是 1 至 32")
        if not 1 <= platform_concurrency <= 16:
            return tr("单平台并发必须是 1 至 16")
        if not 0 <= platform_interval <= 3600:
            return tr("平台冷却必须是 0 至 3600 秒")
        try:
            normalized_proxy = normalize_proxy(default_proxy)
        except ValueError as error:
            return str(error)
        self.database.set_setting("default_save_root", save_root.strip())
        self.database.set_setting("default_output_format", output_format.lower())
        self.database.set_setting("default_quality", quality)
        self.database.set_setting("default_check_interval_seconds", str(interval))
        self.database.set_setting("default_segment_enabled", "1" if segment_enabled else "0")
        self.database.set_setting("default_segment_minutes", str(minutes))
        self.database.set_setting("minimum_free_gb", str(free_gb))
        self.database.set_setting("default_proxy", normalized_proxy)
        self.database.set_setting("resolver_max_concurrency", str(max_concurrency))
        self.database.set_setting(
            "resolver_platform_concurrency", str(platform_concurrency)
        )
        self.database.set_setting(
            "resolver_platform_interval_seconds", str(platform_interval)
        )
        self.reload()
        expected = {
            "default_save_root": save_root.strip(),
            "default_output_format": output_format.lower(),
            "default_quality": quality,
            "default_check_interval_seconds": str(interval),
            "default_segment_enabled": "1" if segment_enabled else "0",
            "default_segment_minutes": str(minutes),
            "minimum_free_gb": str(free_gb),
            "default_proxy": normalized_proxy,
            "resolver_max_concurrency": str(max_concurrency),
            "resolver_platform_concurrency": str(platform_concurrency),
            "resolver_platform_interval_seconds": str(platform_interval),
        }
        if any(self.database.get_setting(key) != value for key, value in expected.items()):
            return tr("设置保存后校验失败，请重试")
        return ""

    @Slot()
    def reload(self) -> None:
        fallback = str(Path.home() / "Videos" / "Reco Box")
        self._default_save_root = self.database.get_setting("default_save_root", fallback)
        self._default_output_format = self.database.get_setting("default_output_format", "ts")
        self._default_quality = self.database.get_setting("default_quality", "原画")
        self._default_check_interval = int(
            self.database.get_setting("default_check_interval_seconds", "300")
        )
        self._default_segment_enabled = (
            self.database.get_setting("default_segment_enabled", "0") == "1"
        )
        self._default_segment_minutes = int(
            self.database.get_setting("default_segment_minutes", "5")
        )
        self._minimum_free_gb = int(self.database.get_setting("minimum_free_gb", "5"))
        self._default_proxy = self.database.get_setting("default_proxy", "")
        self._resolver_max_concurrency = int(
            self.database.get_setting("resolver_max_concurrency", "4")
        )
        self._resolver_platform_concurrency = int(
            self.database.get_setting("resolver_platform_concurrency", "1")
        )
        self._resolver_platform_interval_seconds = int(
            self.database.get_setting("resolver_platform_interval_seconds", "1")
        )
        self.defaultsChanged.emit()


class DesktopActions(QObject):
    VIDEO_EXTENSIONS = frozenset({".ts", ".mp4", ".mkv", ".flv", ".mp3", ".m4a"})

    @Slot(str, result=bool)
    def openDirectory(self, value: str) -> bool:
        path = Path(value)
        if not path.is_dir():
            return False
        return QDesktopServices.openUrl(QUrl.fromLocalFile(str(path)))

    @Slot(str, result=str)
    def chooseDirectory(self, initial: str) -> str:
        start = initial if initial.strip() and Path(initial).is_dir() else str(Path.home())
        return QFileDialog.getExistingDirectory(None, tr("选择文件夹"), start)

    @Slot(str, result=bool)
    def openRecordingDirectories(self, joined_paths: str) -> bool:
        directories = self._recording_directories(joined_paths)
        if not directories:
            return False
        target = directories[0] if len(directories) == 1 else directories[0].parent
        return QDesktopServices.openUrl(QUrl.fromLocalFile(str(target)))

    @Slot(str, result=bool)
    def playRecording(self, joined_paths: str) -> bool:
        for directory in self._recording_directories(joined_paths):
            files = sorted(
                (
                    path
                    for path in directory.iterdir()
                    if path.is_file() and path.suffix.lower() in self.VIDEO_EXTENSIONS
                ),
                key=lambda path: (path.stat().st_mtime, path.name),
            )
            if files:
                return QDesktopServices.openUrl(QUrl.fromLocalFile(str(files[0])))
        return False

    @staticmethod
    def _recording_directories(joined_paths: str) -> list[Path]:
        return [
            path
            for value in joined_paths.split("|")
            if value.strip() and (path := Path(value)).is_dir()
        ]


class LegacyImportController(QObject):
    changed = Signal()

    def __init__(
        self,
        database: Database,
        rooms: RoomListModel,
        settings: SettingsController,
    ) -> None:
        super().__init__()
        self.database = database
        self.rooms = rooms
        self.settings = settings
        self._preview_text = ""
        self._result_text = ""
        self._report_path = ""

    @Property(str, notify=changed)
    def previewText(self) -> str:
        return self._preview_text

    @Property(str, notify=changed)
    def resultText(self) -> str:
        return self._result_text

    @Property(str, notify=changed)
    def reportPath(self) -> str:
        return self._report_path

    @Slot(str, result=bool)
    def preview(self, folder: str) -> bool:
        try:
            inspection = inspect_legacy_folder(Path(folder))
        except (OSError, ValueError, configparser.Error) as error:
            self._preview_text = tr("预检失败：{error}").format(error=error)
            self._result_text = ""
            self._report_path = ""
            self.changed.emit()
            return False
        self._preview_text = inspection.summary()
        self._result_text = ""
        self._report_path = ""
        self.changed.emit()
        return True

    @Slot(str, result=bool)
    def runImport(self, folder: str) -> bool:
        try:
            result = import_legacy_folder(Path(folder), self.database)
        except (OSError, ValueError, configparser.Error) as error:
            self._result_text = tr("导入失败：{error}").format(error=error)
            self.changed.emit()
            return False
        self.rooms.reload()
        self.settings.reload()
        self._result_text = result.summary()
        self._report_path = result.report_path
        self.changed.emit()
        return True
