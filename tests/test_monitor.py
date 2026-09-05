from PySide6.QtCore import QThreadPool

import reco_box.monitor as monitor_module
import reco_box.scheduler as scheduler_module
from reco_box.domain import Platform, Room, RoomStatus
from reco_box.errors import AccessRestricted, ResolverErrorKind, RetryDirective
from reco_box.monitor import MonitoringCoordinator, ResolverWorker
from reco_box.rate_limit import ResolverRateLimitConfig
from reco_box.resolver import ResolvedStream
from reco_box.room_model import RoomListModel
from reco_box.scheduler import MonitoringScheduler
from reco_box.storage import Database


class FakeResolverPool:
    def __init__(self) -> None:
        self.workers = []
        self._max_thread_count = 0

    def setMaxThreadCount(self, count: int) -> None:
        self._max_thread_count = count

    def maxThreadCount(self) -> int:
        return self._max_thread_count

    def start(self, worker) -> None:
        self.workers.append(worker)


def test_resolver_worker_emits_classified_timeout() -> None:
    class FailingResolver:
        async def resolve(self, *_args):
            raise TimeoutError("resolver timed out")

    failures = []
    worker = ResolverWorker(
        "room", "https://example.test/live", "", "原画", FailingResolver()
    )
    worker.signals.failed.connect(lambda room_id, failure: failures.append((room_id, failure)))

    worker.run()

    assert failures[0][0] == "room"
    assert failures[0][1].kind is ResolverErrorKind.NETWORK_TIMEOUT
    assert failures[0][1].retry_directive is RetryDirective.SHORT_BACKOFF


def test_monitor_retains_platform_failure_on_compatible_offline_result(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/1", platform=Platform.BILIBILI)
    database.upsert_room(room)
    rooms = RoomListModel(database)
    coordinator = MonitoringCoordinator(rooms, object())
    failure = AccessRestricted("anonymous access denied")
    offline_rooms: list[str] = []
    coordinator.streamOffline.connect(offline_rooms.append)

    coordinator._resolved(
        room.id,
        ResolvedStream(Platform.BILIBILI, False, "", "", (), failure=failure),
    )

    assert coordinator.last_resolver_failures[room.id] is failure
    assert rooms.get_room(room.id).status is RoomStatus.OFFLINE
    assert offline_rooms == []

    coordinator._resolved(
        room.id,
        ResolvedStream(Platform.BILIBILI, False, "", "", ()),
    )

    assert room.id not in coordinator.last_resolver_failures
    assert offline_rooms == [room.id]


def test_check_all_now_clears_wait_for_every_enabled_room(monkeypatch, tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    first = Room(url="https://live.bilibili.com/1")
    second = Room(url="https://live.bilibili.com/2")
    database.upsert_room(first)
    database.upsert_room(second)
    rooms = RoomListModel(database)
    coordinator = MonitoringCoordinator(rooms, object())
    coordinator.next_check = {first.id: 1000, second.id: 2000}
    ticks: list[bool] = []
    monkeypatch.setattr(coordinator, "_tick", lambda: ticks.append(True))

    coordinator.checkAllNow()

    assert coordinator.next_check == {first.id: 0, second.id: 0}
    assert ticks == [True]


def test_monitor_uses_an_independent_resolver_pool(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    rooms = RoomListModel(database)
    coordinator = MonitoringCoordinator(rooms, object())

    assert coordinator.resolver_pool is not QThreadPool.globalInstance()
    assert coordinator.resolver_pool.maxThreadCount() == 4

    coordinator.update_rate_limit_config(ResolverRateLimitConfig(max_resolver_concurrency=2))

    assert coordinator.resolver_pool.maxThreadCount() == 2
    assert coordinator.rate_limiter.config.max_resolver_concurrency == 2


def test_monitor_limits_resolver_workers_and_releases_permit(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    first = Room(url="https://example.test/one", platform=Platform.DOUYIN)
    second = Room(url="https://example.test/two", platform=Platform.TWITCH)
    database.upsert_room(first)
    database.upsert_room(second)
    rooms = RoomListModel(database)
    pool = FakeResolverPool()
    coordinator = MonitoringCoordinator(
        rooms,
        object(),
        scheduler=MonitoringScheduler(random_source=lambda low, high: low),
        rate_limit_config=ResolverRateLimitConfig(
            max_resolver_concurrency=1,
            default_platform_interval_seconds=0,
        ),
        resolver_pool=pool,
    )
    coordinator.next_check = {first.id: 0, second.id: 0}

    coordinator._tick()

    assert len(pool.workers) == 1
    assert coordinator.running == {first.id}
    assert coordinator.rate_limiter.active_count == 1
    assert rooms.get_room(second.id).status is RoomStatus.OFFLINE

    coordinator._resolved(
        first.id,
        ResolvedStream(Platform.DOUYIN, False, "", "", ()),
    )
    coordinator._tick()

    assert len(pool.workers) == 2
    assert coordinator.running == {second.id}
    assert coordinator.rate_limiter.active_count == 1


def test_monitor_releases_resolver_permit_after_failure(monkeypatch, tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    first = Room(url="https://example.test/one", platform=Platform.DOUYIN)
    second = Room(url="https://example.test/two", platform=Platform.TWITCH)
    database.upsert_room(first)
    database.upsert_room(second)
    rooms = RoomListModel(database)
    pool = FakeResolverPool()
    coordinator = MonitoringCoordinator(
        rooms,
        object(),
        scheduler=MonitoringScheduler(random_source=lambda low, high: low),
        rate_limit_config=ResolverRateLimitConfig(
            max_resolver_concurrency=1,
            default_platform_interval_seconds=0,
        ),
        resolver_pool=pool,
    )
    now = [1000.0]
    monkeypatch.setattr(monitor_module.time, "monotonic", lambda: now[0])
    monkeypatch.setattr(scheduler_module.time, "monotonic", lambda: now[0])
    coordinator.next_check = {first.id: 0, second.id: 0}

    coordinator._tick()

    assert len(pool.workers) == 1
    assert coordinator.running == {first.id}
    assert coordinator.rate_limiter.active_count == 1

    coordinator._failed(first.id, "first failure")

    assert coordinator.next_check[first.id] == 1004.5
    assert coordinator.running == set()
    assert coordinator.rate_limiter.active_count == 0

    coordinator._tick()

    assert len(pool.workers) == 2
    assert coordinator.running == {second.id}
    assert coordinator.rate_limiter.active_count == 1

    coordinator._resolved(
        second.id,
        ResolvedStream(Platform.TWITCH, False, "", "", ()),
    )
    now[0] = 1005.0
    coordinator._tick()
    assert coordinator.running == {first.id}
    assert coordinator.rate_limiter.active_count == 1

    coordinator._failed(first.id, "second failure")
    assert coordinator.next_check[first.id] == 1014
    assert coordinator.resolver_retry_attempts[first.id] == 2
    assert coordinator.running == set()
    assert coordinator.rate_limiter.active_count == 0

    now[0] = 1015.0
    coordinator._tick()
    assert coordinator.running == {first.id}
    assert coordinator.rate_limiter.active_count == 1

    coordinator._resolved(
        first.id,
        ResolvedStream(Platform.DOUYIN, False, "", "", ()),
    )
    assert first.id not in coordinator.resolver_retry_attempts
    assert coordinator.running == set()
    assert coordinator.rate_limiter.active_count == 0


def test_monitor_applies_platform_cooldown_between_rooms(monkeypatch, tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    first = Room(url="https://example.test/one", platform=Platform.DOUYIN)
    second = Room(url="https://example.test/two", platform=Platform.DOUYIN)
    database.upsert_room(first)
    database.upsert_room(second)
    rooms = RoomListModel(database)
    pool = FakeResolverPool()
    coordinator = MonitoringCoordinator(
        rooms,
        object(),
        scheduler=MonitoringScheduler(random_source=lambda low, high: low),
        rate_limit_config=ResolverRateLimitConfig(
            max_resolver_concurrency=2,
            default_platform_concurrency=2,
            default_platform_interval_seconds=10,
        ),
        resolver_pool=pool,
    )
    coordinator.next_check = {first.id: 0, second.id: 0}
    monkeypatch.setattr(monitor_module.time, "monotonic", lambda: 1000.0)

    coordinator._tick()
    coordinator._resolved(
        first.id,
        ResolvedStream(Platform.DOUYIN, False, "", "", ()),
    )
    coordinator._tick()

    assert len(pool.workers) == 1
    assert coordinator.rate_limiter.next_allowed_request[Platform.DOUYIN] == 1010

    monkeypatch.setattr(monitor_module.time, "monotonic", lambda: 1010.0)
    coordinator._tick()

    assert len(pool.workers) == 2
    assert coordinator.running == {second.id}
