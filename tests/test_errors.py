import json
import ssl

import httpx
import pytest
import requests

from reco_box.errors import (
    AccessRestricted,
    DiskFull,
    FFmpegFailed,
    ManualStop,
    NetworkInterrupted,
    NetworkTimeout,
    ParseFailure,
    RateLimited,
    RecordingFailureKind,
    ResolverError,
    ResolverErrorKind,
    RetryDirective,
    Stalled,
    StreamExpired,
    TLSFailure,
    UnknownResolverFailure,
    classify_recording_error,
    classify_resolver_error,
    recording_failure_for_exit,
    safe_error_text,
)
from reco_box.resolver import AnonymousAccessUnavailableError, UnsupportedPlatformError
from reco_box.youtube import YouTubeRateLimitedError


def test_resolver_taxonomy_exposes_recovery_hints_without_applying_them() -> None:
    assert isinstance(AccessRestricted("denied"), ResolverError)
    assert RateLimited("busy").kind is ResolverErrorKind.RATE_LIMITED
    assert RateLimited("busy").retry_directive is RetryDirective.LONG_BACKOFF
    assert NetworkTimeout("slow").retry_directive is RetryDirective.SHORT_BACKOFF
    assert TLSFailure("certificate").retry_directive is RetryDirective.NO_RETRY
    assert ParseFailure("bad payload").retry_directive is RetryDirective.NO_RETRY
    assert UnknownResolverFailure("unknown").retry_directive is RetryDirective.SHORT_BACKOFF


def test_existing_resolver_errors_are_classified_compatibly() -> None:
    assert (
        classify_resolver_error(UnsupportedPlatformError("unsupported")).kind
        is ResolverErrorKind.UNSUPPORTED_PLATFORM
    )
    assert (
        classify_resolver_error(AnonymousAccessUnavailableError("restricted")).kind
        is ResolverErrorKind.ACCESS_RESTRICTED
    )
    assert isinstance(UnsupportedPlatformError("unsupported"), ValueError)
    assert classify_resolver_error(YouTubeRateLimitedError("busy")).retry_directive is RetryDirective.LONG_BACKOFF


def test_http_status_and_transport_errors_are_classified() -> None:
    request = httpx.Request("GET", "https://example.test/room")
    response = httpx.Response(429, request=request)
    status_error = httpx.HTTPStatusError("too many requests", request=request, response=response)

    assert classify_resolver_error(status_error).kind is ResolverErrorKind.RATE_LIMITED
    assert (
        classify_resolver_error(httpx.ReadTimeout("read timed out")).kind
        is ResolverErrorKind.NETWORK_TIMEOUT
    )
    assert (
        classify_resolver_error(ssl.SSLError("certificate verify failed")).kind
        is ResolverErrorKind.TLS_FAILURE
    )
    assert (
        classify_resolver_error(json.JSONDecodeError("invalid", "{}", 0)).kind
        is ResolverErrorKind.PARSE_FAILURE
    )


@pytest.mark.parametrize("status_code", [401, 403, 407, 451])
def test_access_statuses_are_classified_as_restricted(status_code: int) -> None:
    request = httpx.Request("GET", "https://example.test/room")
    response = httpx.Response(status_code, request=request)
    error = httpx.HTTPStatusError("access denied", request=request, response=response)

    assert classify_resolver_error(error).kind is ResolverErrorKind.ACCESS_RESTRICTED


def test_requests_timeout_and_wrapped_tls_errors_are_classified() -> None:
    assert classify_resolver_error(requests.ReadTimeout("read timed out")).kind is ResolverErrorKind.NETWORK_TIMEOUT
    try:
        try:
            raise ssl.SSLError("certificate verify failed")
        except ssl.SSLError as cause:
            raise RuntimeError("transport failed") from cause
    except RuntimeError as error:
        assert classify_resolver_error(error).kind is ResolverErrorKind.TLS_FAILURE


def test_unrecognized_programming_exception_is_not_called_parse_failure() -> None:
    assert classify_resolver_error(TypeError("unexpected bug")).kind is ResolverErrorKind.UNKNOWN_RESOLVER_FAILURE
    assert classify_resolver_error(ValueError("unexpected bug")).kind is ResolverErrorKind.UNKNOWN_RESOLVER_FAILURE


def test_error_text_redacts_credentials_and_query_strings() -> None:
    text = safe_error_text(
        "request failed at https://user:password@example.test/live.m3u8?token=secret#part"
    )

    assert text == "request failed at https://example.test/…"
    assert "password" not in text
    assert "secret" not in text

    metadata = safe_error_text(
        "Cookie: session=secret; Authorization: Bearer access-secret; token=another-secret; "
        "proxy_password=proxy-secret"
    )
    assert "secret" not in metadata
    assert "access-secret" not in metadata
    assert "proxy-secret" not in metadata
    assert metadata == "Cookie: [redacted]"

    relative = safe_error_text(
        "failed /live.m3u8?sig=signature-secret Authorization Bearer bearer-secret"
    )
    assert relative == "failed /live.m3u8?… Authorization: [redacted]"
    assert "signature-secret" not in relative
    assert "bearer-secret" not in relative


def test_empty_error_text_stays_empty() -> None:
    assert safe_error_text("") == ""


def test_recording_failures_preserve_explicit_no_retry_boundaries() -> None:
    assert (
        classify_recording_error(ConnectionError("connection lost")).kind
        is RecordingFailureKind.NETWORK_INTERRUPTED
    )
    assert isinstance(recording_failure_for_exit(1), FFmpegFailed)
    assert isinstance(recording_failure_for_exit(1, protective_error="disk low"), DiskFull)
    assert isinstance(recording_failure_for_exit(1, intentional_stop=True), ManualStop)
    assert recording_failure_for_exit(0) is None


@pytest.mark.parametrize(
    ("failure_type", "kind", "directive"),
    [
        (NetworkInterrupted, RecordingFailureKind.NETWORK_INTERRUPTED, RetryDirective.SHORT_BACKOFF),
        (StreamExpired, RecordingFailureKind.STREAM_EXPIRED, RetryDirective.RE_RESOLVE),
        (DiskFull, RecordingFailureKind.DISK_FULL, RetryDirective.NO_RETRY),
        (FFmpegFailed, RecordingFailureKind.FFMPEG_FAILED, RetryDirective.SHORT_BACKOFF),
        (Stalled, RecordingFailureKind.STALLED, RetryDirective.RE_RESOLVE),
        (ManualStop, RecordingFailureKind.MANUAL_STOP, RetryDirective.NO_RETRY),
    ],
)
def test_recording_taxonomy_covers_each_planned_failure(
    failure_type, kind: RecordingFailureKind, directive: RetryDirective
) -> None:
    failure = failure_type("failure")

    assert failure.kind is kind
    assert failure.retry_directive is directive
