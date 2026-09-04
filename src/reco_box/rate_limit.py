from __future__ import annotations

import math
import time
from collections.abc import Mapping
from dataclasses import dataclass, field
from types import MappingProxyType

from .domain import Platform

DEFAULT_MAX_RESOLVER_CONCURRENCY = 4
DEFAULT_PLATFORM_CONCURRENCY = 1
DEFAULT_PLATFORM_INTERVAL_SECONDS = 1.0


@dataclass(frozen=True, slots=True)
class ResolverRateLimitConfig:
    """Independent resolver concurrency limits.

    The global default is intentionally conservative. Platform limits remain
    configuration data so pressure testing can tune them without changing the
    scheduler or the recording thread pool.
    """

    max_resolver_concurrency: int = DEFAULT_MAX_RESOLVER_CONCURRENCY
    default_platform_concurrency: int = DEFAULT_PLATFORM_CONCURRENCY
    platform_concurrency: Mapping[Platform, int] = field(default_factory=dict)
    default_platform_interval_seconds: float = DEFAULT_PLATFORM_INTERVAL_SECONDS
    platform_interval_seconds: Mapping[Platform, float] = field(default_factory=dict)

    def __post_init__(self) -> None:
        _require_positive(self.max_resolver_concurrency, "max_resolver_concurrency")
        _require_positive(
            self.default_platform_concurrency, "default_platform_concurrency"
        )
        limits = dict(self.platform_concurrency)
        for platform, limit in limits.items():
            if not isinstance(platform, Platform):
                raise TypeError("platform_concurrency keys must be Platform values")
            _require_positive(limit, f"platform_concurrency[{platform.value}]")
        object.__setattr__(self, "platform_concurrency", MappingProxyType(limits))

        _require_nonnegative_seconds(
            self.default_platform_interval_seconds,
            "default_platform_interval_seconds",
        )
        intervals = dict(self.platform_interval_seconds)
        for platform, interval in intervals.items():
            if not isinstance(platform, Platform):
                raise TypeError("platform_interval_seconds keys must be Platform values")
            _require_nonnegative_seconds(
                interval,
                f"platform_interval_seconds[{platform.value}]",
            )
        object.__setattr__(self, "platform_interval_seconds", MappingProxyType(intervals))

    def limit_for(self, platform: Platform) -> int:
        return self.platform_concurrency.get(platform, self.default_platform_concurrency)

    def interval_for(self, platform: Platform) -> float:
        return self.platform_interval_seconds.get(
            platform, self.default_platform_interval_seconds
        )


class ResolverRateLimiter:
    """Track resolver permits without touching QThreadPool.globalInstance()."""

    def __init__(self, config: ResolverRateLimitConfig | None = None) -> None:
        self.config = config or ResolverRateLimitConfig()
        self.running_by_room: dict[str, Platform] = {}
        self.running_by_platform: dict[Platform, int] = {}
        self.last_request_by_platform: dict[Platform, float] = {}
        self.next_allowed_request: dict[Platform, float] = {}

    def reconfigure(self, config: ResolverRateLimitConfig) -> None:
        """Apply new limits while allowing already acquired permits to finish."""
        self.config = config
        for platform, last_request in self.last_request_by_platform.items():
            self.next_allowed_request[platform] = last_request + config.interval_for(
                platform
            )

    @property
    def active_count(self) -> int:
        return len(self.running_by_room)

    def is_running(self, room_id: str) -> bool:
        return room_id in self.running_by_room

    def try_acquire(
        self, room_id: str, platform: Platform, now: float | None = None
    ) -> bool:
        if room_id in self.running_by_room:
            return False
        if self.active_count >= self.config.max_resolver_concurrency:
            return False
        if self.running_by_platform.get(platform, 0) >= self.config.limit_for(platform):
            return False
        current = time.monotonic() if now is None else now
        if current < self.next_allowed_request.get(platform, 0):
            return False
        self.running_by_room[room_id] = platform
        self.running_by_platform[platform] = self.running_by_platform.get(platform, 0) + 1
        self.last_request_by_platform[platform] = current
        self.next_allowed_request[platform] = current + self.config.interval_for(platform)
        return True

    def release(self, room_id: str) -> None:
        platform = self.running_by_room.pop(room_id, None)
        if platform is None:
            return
        remaining = self.running_by_platform.get(platform, 1) - 1
        if remaining > 0:
            self.running_by_platform[platform] = remaining
        else:
            self.running_by_platform.pop(platform, None)


def _require_positive(value: int, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, int) or value < 1:
        raise ValueError(f"{name} must be a positive integer")


def _require_nonnegative_seconds(value: float, name: str) -> None:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        raise TypeError(f"{name} must be a non-negative number")
    if not math.isfinite(value) or value < 0:
        raise ValueError(f"{name} must be a non-negative number")
