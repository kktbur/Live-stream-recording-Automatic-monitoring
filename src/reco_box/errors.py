from __future__ import annotations

import asyncio
import json
import re
import ssl
from enum import StrEnum
from typing import ClassVar
from urllib.parse import urlsplit

import httpx
import requests


class RetryDirective(StrEnum):
    """A future recovery hint; this PR does not apply the hint automatically."""

    NO_RETRY = "no_retry"
    SHORT_BACKOFF = "short_backoff"
    LONG_BACKOFF = "long_backoff"
    RE_RESOLVE = "re_resolve"


class ResolverErrorKind(StrEnum):
    UNSUPPORTED_PLATFORM = "unsupported_platform"
    ACCESS_RESTRICTED = "access_restricted"
    RATE_LIMITED = "rate_limited"
    NETWORK_TIMEOUT = "network_timeout"
    TLS_FAILURE = "tls_failure"
    PARSE_FAILURE = "parse_failure"
    UNKNOWN_RESOLVER_FAILURE = "unknown_resolver_failure"


class RecordingFailureKind(StrEnum):
    NETWORK_INTERRUPTED = "network_interrupted"
    STREAM_EXPIRED = "stream_expired"
    DISK_FULL = "disk_full"
    FFMPEG_FAILED = "ffmpeg_failed"
    STALLED = "stalled"
    MANUAL_STOP = "manual_stop"


_URL_PATTERN = re.compile(r"https?://[^\s<>()]+", re.IGNORECASE)
_TRAILING_URL_CHARS = ".,;:!?]}\"'"
_SENSITIVE_FIELD_PATTERN = re.compile(
    r"(?i)(?P<label>\b(?:cookie|authorization|proxy[-_ ]?authorization|"
    r"access[-_ ]?token|refresh[-_ ]?token|token|password|secret|"
    r"proxy[-_ ]?(?:user|password|credential))\b)\s*"
    r"(?:(?:[:=]\s*)|(?:\s+bearer\s+))[^\r\n]*"
)
_QUERY_PATTERN = re.compile(r"(?i)(?P<prefix>[?&])[^\s<>()]+")


def safe_error_text(error: BaseException | str) -> str:
    """Return a bounded UI/log message without query strings or credentials."""

    try:
        text = str(error)
    except Exception:  # noqa: BLE001 - error rendering must never mask the failure
        text = type(error).__name__
    text = _URL_PATTERN.sub(_redact_url, text)
    text = _QUERY_PATTERN.sub(_redact_query, text)
    text = _SENSITIVE_FIELD_PATTERN.sub(_redact_sensitive_field, text)
    text = text.replace("\r", " ").replace("\n", " ").strip()
    if not text:
        return "" if isinstance(error, str) else type(error).__name__
    return text[:300]


def _redact_sensitive_field(match: re.Match[str]) -> str:
    return f"{match.group('label')}: [redacted]"


def _redact_query(match: re.Match[str]) -> str:
    value = match.group(0)
    trailing = ""
    while value and value[-1] in _TRAILING_URL_CHARS:
        trailing = value[-1] + trailing
        value = value[:-1]
    return f"{match.group('prefix')}…" + trailing


def _redact_url(match: re.Match[str]) -> str:
    value = match.group(0)
    trailing = ""
    while value and value[-1] in _TRAILING_URL_CHARS:
        trailing = value[-1] + trailing
        value = value[:-1]
    try:
        parsed = urlsplit(value)
    except ValueError:
        return "[url]" + trailing
    hostname = parsed.hostname
    if not hostname:
        return "[url]" + trailing
    return f"{parsed.scheme}://{hostname}/…" + trailing


class ResolverError(RuntimeError):
    kind: ClassVar[ResolverErrorKind] = ResolverErrorKind.UNKNOWN_RESOLVER_FAILURE
    retry_directive: ClassVar[RetryDirective] = RetryDirective.SHORT_BACKOFF

    def __init__(self, message: str = "", *, cause: BaseException | None = None) -> None:
        self.cause_type = type(cause).__name__ if cause is not None else ""
        super().__init__(_safe_failure_message(message, type(self).__name__))


class UnsupportedPlatform(ResolverError):
    kind = ResolverErrorKind.UNSUPPORTED_PLATFORM
    retry_directive = RetryDirective.NO_RETRY


class AccessRestricted(ResolverError):
    kind = ResolverErrorKind.ACCESS_RESTRICTED
    retry_directive = RetryDirective.NO_RETRY


class RateLimited(ResolverError):
    kind = ResolverErrorKind.RATE_LIMITED
    retry_directive = RetryDirective.LONG_BACKOFF


class NetworkTimeout(ResolverError):
    kind = ResolverErrorKind.NETWORK_TIMEOUT
    retry_directive = RetryDirective.SHORT_BACKOFF


class TLSFailure(ResolverError):
    kind = ResolverErrorKind.TLS_FAILURE
    retry_directive = RetryDirective.NO_RETRY


class ParseFailure(ResolverError):
    kind = ResolverErrorKind.PARSE_FAILURE
    retry_directive = RetryDirective.NO_RETRY


class UnknownResolverFailure(ResolverError):
    kind = ResolverErrorKind.UNKNOWN_RESOLVER_FAILURE
    retry_directive = RetryDirective.SHORT_BACKOFF


class RecordingFailure(RuntimeError):
    kind: ClassVar[RecordingFailureKind] = RecordingFailureKind.FFMPEG_FAILED
    retry_directive: ClassVar[RetryDirective] = RetryDirective.SHORT_BACKOFF

    def __init__(self, message: str = "", *, cause: BaseException | None = None) -> None:
        self.cause_type = type(cause).__name__ if cause is not None else ""
        super().__init__(_safe_failure_message(message, type(self).__name__))


def _safe_failure_message(message: str, fallback: str) -> str:
    return safe_error_text(message) if message else fallback


class NetworkInterrupted(RecordingFailure):
    kind = RecordingFailureKind.NETWORK_INTERRUPTED
    retry_directive = RetryDirective.SHORT_BACKOFF


class StreamExpired(RecordingFailure):
    kind = RecordingFailureKind.STREAM_EXPIRED
    retry_directive = RetryDirective.RE_RESOLVE


class DiskFull(RecordingFailure):
    kind = RecordingFailureKind.DISK_FULL
    retry_directive = RetryDirective.NO_RETRY


class FFmpegFailed(RecordingFailure):
    kind = RecordingFailureKind.FFMPEG_FAILED
    retry_directive = RetryDirective.SHORT_BACKOFF


class Stalled(RecordingFailure):
    kind = RecordingFailureKind.STALLED
    retry_directive = RetryDirective.RE_RESOLVE


class ManualStop(RecordingFailure):
    kind = RecordingFailureKind.MANUAL_STOP
    retry_directive = RetryDirective.NO_RETRY


def classify_resolver_error(error: BaseException) -> ResolverError:
    """Normalize transport, access, parsing, and unknown errors for monitoring."""

    if isinstance(error, ResolverError):
        return error
    status_code = _status_code(error)
    if status_code == 429:
        return RateLimited(safe_error_text(error), cause=error)
    if status_code in {401, 403, 407, 451}:
        return AccessRestricted(safe_error_text(error), cause=error)
    if _is_timeout(error):
        return NetworkTimeout(safe_error_text(error), cause=error)
    if _is_tls_failure(error):
        return TLSFailure(safe_error_text(error), cause=error)
    if _is_parse_failure(error):
        return ParseFailure(safe_error_text(error), cause=error)
    return UnknownResolverFailure(safe_error_text(error), cause=error)


def classify_recording_error(error: BaseException | str) -> RecordingFailure:
    """Normalize a low-level recording exception without deciding recovery yet."""

    if isinstance(error, RecordingFailure):
        return error
    if isinstance(error, (ConnectionError, requests.exceptions.ConnectionError)):
        return NetworkInterrupted(
            safe_error_text(error),
            cause=error if isinstance(error, BaseException) else None,
        )
    return FFmpegFailed(
        safe_error_text(error),
        cause=error if isinstance(error, BaseException) else None,
    )


def recording_failure_for_exit(
    exit_code: int,
    *,
    intentional_stop: bool = False,
    protective_error: str = "",
    message: str = "",
    recovery_failure: RecordingFailure | None = None,
) -> RecordingFailure | None:
    """Classify an FFmpeg completion without changing the existing retry policy."""

    if protective_error:
        return DiskFull(protective_error)
    if intentional_stop:
        return ManualStop(message or "手动停止录制")
    if recovery_failure is not None:
        return recovery_failure
    if exit_code == 0:
        return None
    return FFmpegFailed(message or f"FFmpeg 退出码 {exit_code}")


def _status_code(error: BaseException) -> int | None:
    for candidate in (getattr(error, "response", None), error):
        value = getattr(candidate, "status_code", None)
        if isinstance(value, int):
            return value
    return None


def _is_timeout(error: BaseException) -> bool:
    return isinstance(
        error,
        (
            httpx.TimeoutException,
            requests.exceptions.Timeout,
            TimeoutError,
            asyncio.TimeoutError,
        ),
    )


def _is_tls_failure(error: BaseException) -> bool:
    current: BaseException | None = error
    seen: set[int] = set()
    while current is not None and id(current) not in seen:
        seen.add(id(current))
        if isinstance(current, (ssl.SSLError, requests.exceptions.SSLError)):
            return True
        current = current.__cause__ or current.__context__
    return False


def _is_parse_failure(error: BaseException) -> bool:
    return isinstance(
        error,
        (
            json.JSONDecodeError,
            httpx.DecodingError,
            httpx.InvalidURL,
            httpx.UnsupportedProtocol,
            requests.exceptions.InvalidURL,
        ),
    )
