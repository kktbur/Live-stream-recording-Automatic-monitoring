import pytest

from reco_box.domain import Platform
from reco_box.rate_limit import ResolverRateLimitConfig, ResolverRateLimiter
from reco_box.scheduler import MonitoringScheduler


def test_scheduler_jitter_is_bounded_and_injectable() -> None:
    scheduler = MonitoringScheduler(
        jitter_ratio=0.1,
        random_source=lambda low, high: high,
    )
    next_check = {}

    scheduler.schedule_success(next_check, "room", 300, now=1000)

    assert next_check["room"] == 1330


def test_scheduler_jitter_includes_the_lower_bound() -> None:
    scheduler = MonitoringScheduler(
        jitter_ratio=0.1,
        random_source=lambda low, high: low,
    )
    next_check = {}

    scheduler.schedule_success(next_check, "room", 300, now=1000)

    assert next_check["room"] == 1270


def test_scheduler_generates_independent_deadlines_per_room() -> None:
    values = iter((270.0, 330.0))
    scheduler = MonitoringScheduler(random_source=lambda low, high: next(values))
    next_check = {}

    scheduler.schedule_success(next_check, "first", 300, now=1000)
    scheduler.schedule_success(next_check, "second", 300, now=1000)

    assert next_check == {"first": 1270, "second": 1330}


def test_scheduler_retry_keeps_the_existing_sixty_second_cap() -> None:
    scheduler = MonitoringScheduler(random_source=lambda low, high: low)
    next_check = {}

    scheduler.schedule_retry(next_check, "room", 300, attempt=5, now=1000)

    assert next_check["room"] == 1054


def test_scheduler_retry_uses_exponential_backoff_before_the_cap() -> None:
    scheduler = MonitoringScheduler(random_source=lambda low, high: low)
    next_check = {}

    scheduler.schedule_retry(next_check, "room", 300, attempt=2, now=1000)

    assert next_check["room"] == 1009


def test_scheduler_retry_jitter_never_exceeds_the_cap() -> None:
    scheduler = MonitoringScheduler(random_source=lambda low, high: high)
    next_check = {}

    scheduler.schedule_retry(next_check, "room", 300, attempt=5, now=1000)

    assert next_check["room"] == 1060


def test_scheduler_retry_keeps_the_backoff_curve_when_poll_interval_is_short() -> None:
    scheduler = MonitoringScheduler(random_source=lambda low, high: low)
    next_check = {}

    scheduler.schedule_retry(next_check, "room", 30, attempt=4, now=1000)

    assert next_check["room"] == 1036


def test_scheduler_retry_reaches_the_cap_when_poll_interval_is_short() -> None:
    scheduler = MonitoringScheduler(random_source=lambda low, high: low)
    next_check = {}

    scheduler.schedule_retry(next_check, "room", 30, attempt=5, now=1000)

    assert next_check["room"] == 1054


def test_scheduler_immediate_deadline_and_due_check() -> None:
    scheduler = MonitoringScheduler()
    next_check = {"room": 100}

    scheduler.schedule_immediate(next_check, "room")

    assert scheduler.is_due(next_check, "room", now=0)
    assert scheduler.is_due(next_check, "other", now=0)


def test_scheduler_preserves_a_caller_selected_delay() -> None:
    scheduler = MonitoringScheduler()
    next_check = {}

    scheduler.schedule_delay(next_check, "room", 5, now=100)

    assert next_check["room"] == 105


def test_rate_limiter_enforces_global_and_platform_limits() -> None:
    limiter = ResolverRateLimiter(
        ResolverRateLimitConfig(
            max_resolver_concurrency=2,
            default_platform_concurrency=1,
        )
    )

    assert limiter.try_acquire("douyin-1", Platform.DOUYIN)
    assert not limiter.try_acquire("douyin-2", Platform.DOUYIN)
    assert limiter.try_acquire("twitch-1", Platform.TWITCH)
    assert not limiter.try_acquire("bilibili-1", Platform.BILIBILI)

    limiter.release("douyin-1")

    assert limiter.try_acquire("bilibili-1", Platform.BILIBILI)
    assert limiter.running_by_platform == {
        Platform.TWITCH: 1,
        Platform.BILIBILI: 1,
    }


def test_rate_limiter_accepts_a_platform_override() -> None:
    limiter = ResolverRateLimiter(
        ResolverRateLimitConfig(
            max_resolver_concurrency=3,
            default_platform_concurrency=1,
            default_platform_interval_seconds=0,
            platform_concurrency={Platform.DOUYIN: 2},
        )
    )

    assert limiter.try_acquire("one", Platform.DOUYIN)
    assert limiter.try_acquire("two", Platform.DOUYIN)
    assert not limiter.try_acquire("three", Platform.DOUYIN)


def test_rate_limiter_enforces_platform_cooldown_after_release() -> None:
    limiter = ResolverRateLimiter(
        ResolverRateLimitConfig(
            max_resolver_concurrency=2,
            default_platform_concurrency=1,
            default_platform_interval_seconds=10,
        )
    )

    assert limiter.try_acquire("first", Platform.DOUYIN, now=100)
    limiter.release("first")

    assert not limiter.try_acquire("second", Platform.DOUYIN, now=109)
    assert limiter.try_acquire("second", Platform.DOUYIN, now=110)
    assert limiter.last_request_by_platform[Platform.DOUYIN] == 110
    assert limiter.next_allowed_request[Platform.DOUYIN] == 120


def test_rate_limiter_reconfigures_an_existing_platform_cooldown() -> None:
    limiter = ResolverRateLimiter(
        ResolverRateLimitConfig(default_platform_interval_seconds=10)
    )

    assert limiter.try_acquire("first", Platform.DOUYIN, now=100)
    limiter.release("first")

    limiter.reconfigure(ResolverRateLimitConfig(default_platform_interval_seconds=0))
    assert limiter.try_acquire("second", Platform.DOUYIN, now=101)
    limiter.release("second")

    limiter.reconfigure(ResolverRateLimitConfig(default_platform_interval_seconds=10))
    assert not limiter.try_acquire("third", Platform.DOUYIN, now=102)
    assert limiter.next_allowed_request[Platform.DOUYIN] == 111


@pytest.mark.parametrize(
    ("field", "value"),
    [
        ("max_resolver_concurrency", 0),
        ("default_platform_concurrency", 0),
        ("default_platform_interval_seconds", -1),
    ],
)
def test_rate_limit_config_rejects_non_positive_limits(field: str, value: int) -> None:
    with pytest.raises(ValueError):
        ResolverRateLimitConfig(**{field: value})
