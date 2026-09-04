from __future__ import annotations

import random
import time
from collections.abc import Callable, MutableMapping

RandomSource = Callable[[float, float], float]


class MonitoringScheduler:
    """Calculate independent resolver deadlines with bounded jitter."""

    def __init__(
        self,
        jitter_ratio: float = 0.1,
        random_source: RandomSource | None = None,
        retry_base_seconds: int = 5,
        retry_cap_seconds: int = 60,
    ) -> None:
        if not 0 <= jitter_ratio < 1:
            raise ValueError("jitter_ratio must be between 0 and 1")
        if isinstance(retry_base_seconds, bool) or retry_base_seconds < 1:
            raise ValueError("retry_base_seconds must be positive")
        if isinstance(retry_cap_seconds, bool) or retry_cap_seconds < 1:
            raise ValueError("retry_cap_seconds must be positive")
        if retry_base_seconds > retry_cap_seconds:
            raise ValueError("retry_base_seconds must not exceed retry_cap_seconds")
        self.jitter_ratio = jitter_ratio
        self.retry_base_seconds = retry_base_seconds
        self.retry_cap_seconds = retry_cap_seconds
        self._random_source = random_source or random.uniform

    def schedule_success(
        self,
        next_check: MutableMapping[str, float],
        room_id: str,
        interval_seconds: int,
        now: float | None = None,
    ) -> None:
        next_check[room_id] = self._deadline(interval_seconds, now)

    def schedule_retry(
        self,
        next_check: MutableMapping[str, float],
        room_id: str,
        interval_seconds: int,
        attempt: int = 1,
        now: float | None = None,
    ) -> None:
        if isinstance(attempt, bool) or attempt < 1:
            raise ValueError("attempt must be positive")
        retry_seconds = min(
            self.retry_cap_seconds,
            self.retry_base_seconds * 2 ** (attempt - 1),
        )
        next_check[room_id] = self._deadline(
            retry_seconds, now, maximum_delay=self.retry_cap_seconds
        )

    def schedule_delay(
        self,
        next_check: MutableMapping[str, float],
        room_id: str,
        delay_seconds: int,
        now: float | None = None,
    ) -> None:
        """Schedule a caller-selected delay without applying retry jitter or a cap."""
        base = max(1.0, float(delay_seconds))
        next_check[room_id] = (time.monotonic() if now is None else now) + base

    @staticmethod
    def schedule_immediate(next_check: MutableMapping[str, float], room_id: str) -> None:
        next_check[room_id] = 0

    @staticmethod
    def is_due(
        next_check: MutableMapping[str, float], room_id: str, now: float
    ) -> bool:
        return now >= next_check.get(room_id, 0)

    def _deadline(
        self,
        interval_seconds: int,
        now: float | None,
        maximum_delay: float | None = None,
    ) -> float:
        base = max(1.0, float(interval_seconds))
        delay = self._jittered_delay(base)
        if maximum_delay is not None:
            delay = min(maximum_delay, delay)
        return (time.monotonic() if now is None else now) + delay

    def _jittered_delay(self, interval_seconds: float) -> float:
        low = interval_seconds * (1 - self.jitter_ratio)
        high = interval_seconds * (1 + self.jitter_ratio)
        value = float(self._random_source(low, high))
        return min(high, max(low, value))
