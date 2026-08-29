from __future__ import annotations

from PySide6.QtCore import Property, QObject, QUrl, Signal, Slot

from .localization import tr
from .monitor import MonitoringCoordinator


class PreviewController(QObject):
    changed = Signal()

    def __init__(self, monitor: MonitoringCoordinator):
        super().__init__()
        self.monitor = monitor
        self._source = QUrl()
        self._title = tr("直播预览")
        self._error = ""

    @Property(QUrl, notify=changed)
    def source(self) -> QUrl:
        return self._source

    @Property(str, notify=changed)
    def title(self) -> str:
        return self._title

    @Property(str, notify=changed)
    def error(self) -> str:
        return self._error

    @Slot(str, result=bool)
    def play(self, room_id: str) -> bool:
        resolved = self.monitor.stream_for_room(room_id)
        if resolved is None or not resolved.stream_urls:
            self._source = QUrl()
            self._title = tr("直播预览")
            self._error = tr("尚未取得直播流，请先点击“立即检查并录制”")
            self.changed.emit()
            return False
        self._source = QUrl(resolved.stream_urls[0])
        self._title = resolved.title or resolved.streamer_name or tr("直播预览")
        self._error = ""
        self.changed.emit()
        return True

    @Slot(str)
    def setPlayerError(self, message: str) -> None:
        self._error = message[:300]
        self.changed.emit()

    @Slot()
    def clear(self) -> None:
        self._source = QUrl()
        self._error = ""
        self.changed.emit()
