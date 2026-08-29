from __future__ import annotations

import asyncio
import time

from PySide6.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal, Slot

from .domain import RoomStatus
from .resolver import DouyinLiveRecorderResolver, ResolvedStream
from .room_model import RoomListModel


class ResolverSignals(QObject):
    completed = Signal(str, object)
    failed = Signal(str, str)


class ResolverWorker(QRunnable):
    def __init__(
        self,
        room_id: str,
        url: str,
        proxy: str,
        quality: str,
        resolver: DouyinLiveRecorderResolver,
    ):
        super().__init__()
        self.room_id = room_id
        self.url = url
        self.proxy = proxy
        self.quality = quality
        self.resolver = resolver
        self.signals = ResolverSignals()

    @Slot()
    def run(self) -> None:
        try:
            result = asyncio.run(self.resolver.resolve(self.url, self.proxy, self.quality))
        except Exception as error:  # noqa: BLE001 - worker converts errors to user state
            self.signals.failed.emit(self.room_id, _safe_error(error))
        else:
            self.signals.completed.emit(self.room_id, result)


class MonitoringCoordinator(QObject):
    liveDetected = Signal(str, object)

    def __init__(self, rooms: RoomListModel, resolver: DouyinLiveRecorderResolver):
        super().__init__()
        self.rooms = rooms
        self.resolver = resolver
        self.pool = QThreadPool.globalInstance()
        self.running: set[str] = set()
        self.next_check: dict[str, float] = {}
        self.last_streams: dict[str, ResolvedStream] = {}
        self.timer = QTimer(self)
        self.timer.setInterval(1_000)
        self.timer.timeout.connect(self._tick)
        self.rooms.roomAdded.connect(self.check_now)

    def start(self) -> None:
        self.timer.start()
        QTimer.singleShot(300, self._tick)

    @Slot(str)
    def check_now(self, room_id: str) -> None:
        self.next_check[room_id] = 0
        self._tick()

    @Slot(str)
    def checkNow(self, room_id: str) -> None:
        self.check_now(room_id)

    @Slot()
    def checkAllNow(self) -> None:
        for room in self.rooms.rooms:
            if room.enabled:
                self.next_check[room.id] = 0
        self._tick()

    def stream_for_room(self, room_id: str) -> ResolvedStream | None:
        return self.last_streams.get(room_id)

    @Slot(str, int)
    def schedule_retry(self, room_id: str, delay_seconds: int) -> None:
        self.next_check[room_id] = time.monotonic() + max(1, delay_seconds)

    @Slot()
    def _tick(self) -> None:
        now = time.monotonic()
        for room in tuple(self.rooms.rooms):
            if not room.enabled or room.id in self.running:
                continue
            if room.status in (RoomStatus.RECORDING, RoomStatus.CONVERTING, RoomStatus.PREPARING):
                continue
            if now < self.next_check.get(room.id, 0):
                continue
            self.running.add(room.id)
            self.rooms.update_room_state(room.id, RoomStatus.CHECKING)
            worker = ResolverWorker(room.id, room.url, room.proxy, room.quality, self.resolver)
            worker.signals.completed.connect(self._resolved)
            worker.signals.failed.connect(self._failed)
            self.pool.start(worker)

    @Slot(str, object)
    def _resolved(self, room_id: str, result: ResolvedStream) -> None:
        self.running.discard(room_id)
        room = self.rooms.get_room(room_id)
        if room is None:
            return
        self.next_check[room_id] = time.monotonic() + room.check_interval_seconds
        if result.is_live and result.stream_urls:
            self.last_streams[room_id] = result
            self.rooms.update_room_state(
                room_id,
                RoomStatus.PREPARING,
                streamer_name=result.streamer_name,
                title=result.title,
            )
            self.liveDetected.emit(room_id, result)
        else:
            self.last_streams.pop(room_id, None)
            self.rooms.update_room_state(
                room_id,
                RoomStatus.OFFLINE,
                streamer_name=result.streamer_name,
                title=result.title,
            )

    @Slot(str, str)
    def _failed(self, room_id: str, message: str) -> None:
        self.running.discard(room_id)
        self.last_streams.pop(room_id, None)
        room = self.rooms.get_room(room_id)
        if room is None:
            return
        self.next_check[room_id] = time.monotonic() + min(room.check_interval_seconds, 60)
        self.rooms.update_room_state(room_id, RoomStatus.RETRYING, error=message)


def _safe_error(error: Exception) -> str:
    text = str(error).replace("\r", " ").replace("\n", " ").strip()
    return (text or error.__class__.__name__)[:300]
