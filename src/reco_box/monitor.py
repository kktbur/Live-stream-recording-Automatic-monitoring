from __future__ import annotations

import asyncio
import time

from PySide6.QtCore import QObject, QRunnable, QThreadPool, QTimer, Signal, Slot

from .domain import RoomStatus
from .rate_limit import ResolverRateLimitConfig, ResolverRateLimiter
from .resolver import DouyinLiveRecorderResolver, ResolvedStream
from .room_model import RoomListModel
from .scheduler import MonitoringScheduler


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

    def __init__(
        self,
        rooms: RoomListModel,
        resolver: DouyinLiveRecorderResolver,
        scheduler: MonitoringScheduler | None = None,
        rate_limit_config: ResolverRateLimitConfig | None = None,
        resolver_pool: QThreadPool | None = None,
    ):
        super().__init__()
        self.rooms = rooms
        self.resolver = resolver
        self.scheduler = scheduler or MonitoringScheduler()
        self.rate_limiter = ResolverRateLimiter(rate_limit_config)
        self.resolver_pool = (
            resolver_pool if resolver_pool is not None else QThreadPool(self)
        )
        self.resolver_pool.setMaxThreadCount(
            self.rate_limiter.config.max_resolver_concurrency
        )
        self.pool = self.resolver_pool
        self.running: set[str] = set()
        self.next_check: dict[str, float] = {}
        self.resolver_retry_attempts: dict[str, int] = {}
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
        self.scheduler.schedule_immediate(self.next_check, room_id)
        self._tick()

    @Slot(str)
    def checkNow(self, room_id: str) -> None:
        self.check_now(room_id)

    @Slot()
    def checkAllNow(self) -> None:
        for room in self.rooms.rooms:
            if room.enabled:
                self.scheduler.schedule_immediate(self.next_check, room.id)
        self._tick()

    def stream_for_room(self, room_id: str) -> ResolvedStream | None:
        return self.last_streams.get(room_id)

    def update_rate_limit_config(self, config: ResolverRateLimitConfig) -> None:
        self.rate_limiter.reconfigure(config)
        self.resolver_pool.setMaxThreadCount(config.max_resolver_concurrency)

    @Slot(str, int)
    def schedule_retry(self, room_id: str, delay_seconds: int) -> None:
        self.scheduler.schedule_delay(self.next_check, room_id, delay_seconds)

    @Slot()
    def _tick(self) -> None:
        now = time.monotonic()
        for room in tuple(self.rooms.rooms):
            if not room.enabled or room.id in self.running:
                continue
            if room.status in (RoomStatus.RECORDING, RoomStatus.CONVERTING, RoomStatus.PREPARING):
                continue
            if not self.scheduler.is_due(self.next_check, room.id, now):
                continue
            if not self.rate_limiter.try_acquire(room.id, room.platform, now=now):
                continue
            self.running.add(room.id)
            self.rooms.update_room_state(room.id, RoomStatus.CHECKING)
            worker = ResolverWorker(room.id, room.url, room.proxy, room.quality, self.resolver)
            worker.signals.completed.connect(self._resolved)
            worker.signals.failed.connect(self._failed)
            self.resolver_pool.start(worker)

    def _release_room(self, room_id: str) -> None:
        self.running.discard(room_id)
        self.rate_limiter.release(room_id)

    @Slot(str, object)
    def _resolved(self, room_id: str, result: ResolvedStream) -> None:
        self._release_room(room_id)
        self.resolver_retry_attempts.pop(room_id, None)
        room = self.rooms.get_room(room_id)
        if room is None:
            return
        self.scheduler.schedule_success(
            self.next_check, room_id, room.check_interval_seconds
        )
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
        self._release_room(room_id)
        attempt = self.resolver_retry_attempts.get(room_id, 0) + 1
        self.resolver_retry_attempts[room_id] = attempt
        self.last_streams.pop(room_id, None)
        room = self.rooms.get_room(room_id)
        if room is None:
            return
        self.scheduler.schedule_retry(
            self.next_check, room_id, room.check_interval_seconds, attempt=attempt
        )
        self.rooms.update_room_state(room_id, RoomStatus.RETRYING, error=message)


def _safe_error(error: Exception) -> str:
    text = str(error).replace("\r", " ").replace("\n", " ").strip()
    return (text or error.__class__.__name__)[:300]
