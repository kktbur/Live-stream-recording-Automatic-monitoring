from __future__ import annotations

import json
import re
from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import urljoin, urlsplit

import httpx

from .domain import Platform
from .errors import (
    ParseFailure,
    ResolverError,
    ResolverErrorKind,
    RetryDirective,
    classify_resolver_error,
)
from .network import normalize_proxy
from .network_policy import DEFAULT_NETWORK_POLICY, NetworkPolicy

YOUTUBE_PAGE_HOSTS = ("youtube.com", "youtu.be")
REDIRECT_STATUSES = {301, 302, 303, 307, 308}
MAX_REDIRECTS = 5
PLAYER_RESPONSE_PATTERN = re.compile(
    r"var\s+ytInitialPlayerResponse\s*=\s*(\{.*?\});\s*var\s+meta\s*=",
    re.DOTALL,
)
BANDWIDTH_PATTERN = re.compile(r"(?:^|,)BANDWIDTH=(\d+)(?:,|$)")
QUALITY_INDEX = {"OD": 0, "BD": 0, "UHD": 1, "HD": 2, "SD": 3, "LD": 4}

ClientFactory = Callable[..., httpx.AsyncClient]
FailureSink = Callable[[ResolverError], None]


class YouTubeResolverError(ParseFailure):
    """Base error for an invalid or unavailable YouTube public response."""


class YouTubeAnonymousAccessUnavailableError(YouTubeResolverError):
    """The public YouTube page or manifest rejected an anonymous request."""

    kind = ResolverErrorKind.ACCESS_RESTRICTED
    retry_directive = RetryDirective.NO_RETRY


class YouTubeRateLimitedError(YouTubeResolverError):
    """The public YouTube endpoint asked the anonymous client to slow down."""

    kind = ResolverErrorKind.RATE_LIMITED
    retry_directive = RetryDirective.LONG_BACKOFF


class YouTubeResolver:
    """Resolve public YouTube live pages through a first-party verified client."""

    def __init__(
        self,
        network_policy: NetworkPolicy | None = None,
        client_factory: ClientFactory | None = None,
    ) -> None:
        self.network_policy = network_policy or DEFAULT_NETWORK_POLICY
        self._client_factory = client_factory or httpx.AsyncClient

    async def resolve(
        self,
        url: str,
        proxy_addr: str | None = None,
        quality_code: str = "OD",
        failure_sink: FailureSink | None = None,
    ) -> dict[str, Any]:
        try:
            safe_proxy = normalize_proxy(proxy_addr) if proxy_addr else None
            return await self._resolve(url, safe_proxy, quality_code)
        except (
            YouTubeResolverError,
            httpx.HTTPError,
            TypeError,
            ValueError,
            KeyError,
            IndexError,
        ) as error:
            if failure_sink is not None:
                failure_sink(classify_resolver_error(error))
            # Keep the pinned resolver's anonymous public contract: an
            # unavailable or malformed response is treated as offline.
            return {"anchor_name": "", "live_status": False, "room_url": url}

    async def _resolve(
        self,
        url: str,
        proxy_addr: str | None,
        quality_code: str,
    ) -> dict[str, Any]:
        page_url = _normalise_page_url(url)
        transport = _YouTubeTransport(
            network_policy=self.network_policy,
            client_factory=self._client_factory,
            proxy_addr=proxy_addr,
        )
        html, _resolved_page_url = await transport.get_text(
            page_url, validate_page_host=True
        )
        player = _player_response(html)
        video_details = _optional_mapping(player.get("videoDetails"))
        anchor_name = _text(video_details.get("author"))
        live_status = _as_bool(video_details.get("isLive"))
        result: dict[str, Any] = {
            "anchor_name": anchor_name,
            "live_status": live_status,
            "room_url": url,
        }
        if not live_status:
            return result

        title = _text(video_details.get("title"))
        streaming_data = _required_mapping(player, "streamingData")
        manifest_url = _text(streaming_data.get("hlsManifestUrl"))
        if not manifest_url:
            raise TypeError("YouTube live response is missing hlsManifestUrl")
        manifest, resolved_manifest_url = await transport.get_text(manifest_url)
        play_urls = _hls_variant_urls(manifest, resolved_manifest_url)
        if not play_urls:
            raise YouTubeResolverError("YouTube HLS manifest has no playable variants")
        selected_index = QUALITY_INDEX.get(str(quality_code).upper(), 0)
        selected_url = play_urls[min(selected_index, len(play_urls) - 1)]
        result.update(
            {
                "title": title,
                "m3u8_url": manifest_url,
                "play_url_list": play_urls,
                "record_url": selected_url,
            }
        )
        return result


class _YouTubeTransport:
    def __init__(
        self,
        network_policy: NetworkPolicy,
        client_factory: ClientFactory,
        proxy_addr: str | None,
    ) -> None:
        self._network_policy = network_policy
        self._client_factory = client_factory
        self._proxy_addr = proxy_addr
        self._headers = {
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/127.0",
        }

    async def get_text(
        self,
        url: str,
        *,
        validate_page_host: bool = False,
    ) -> tuple[str, str]:
        next_url = url
        for _ in range(MAX_REDIRECTS + 1):
            parsed_url = urlsplit(next_url)
            if parsed_url.scheme not in {"http", "https"} or not parsed_url.netloc:
                raise ValueError("YouTube request URL must use HTTP or HTTPS")
            if validate_page_host and not _is_youtube_page_host(next_url):
                raise YouTubeResolverError("YouTube page redirect left the YouTube host")
            verify = self._network_policy.verify_for(Platform.YOUTUBE, next_url)
            async with self._client_factory(
                headers=self._headers,
                http2=True,
                follow_redirects=False,
                proxy=self._proxy_addr,
                timeout=20,
                verify=verify,
            ) as client:
                response = await client.get(next_url, params={})
            if response.status_code not in REDIRECT_STATUSES:
                if response.status_code == 429:
                    raise YouTubeRateLimitedError(
                        f"YouTube anonymous request rate limited at {next_url}"
                    )
                if response.status_code in {401, 403}:
                    raise YouTubeAnonymousAccessUnavailableError(
                        f"YouTube anonymous access unavailable at {next_url} "
                        f"(HTTP {response.status_code})"
                    )
                response.raise_for_status()
                return response.text, str(response.url)
            location = _text(response.headers.get("location"))
            if not location:
                raise YouTubeResolverError(
                    f"YouTube endpoint returned HTTP {response.status_code} without a redirect target"
                )
            next_url = urljoin(next_url, location)
        raise YouTubeResolverError("YouTube endpoint exceeded the redirect limit")


def _normalise_page_url(url: str) -> str:
    candidate = url.strip()
    if "://" not in candidate:
        candidate = f"https://{candidate}"
    parsed = urlsplit(candidate)
    if parsed.scheme not in {"http", "https"} or not _is_youtube_page_host(candidate):
        raise ValueError("YouTube URL does not use an allowed page host")
    return candidate


def _is_youtube_page_host(url: str) -> bool:
    hostname = (urlsplit(url).hostname or "").rstrip(".").casefold()
    return any(
        hostname == domain or hostname.endswith(f".{domain}")
        for domain in YOUTUBE_PAGE_HOSTS
    )


def _player_response(html: str) -> dict[str, Any]:
    match = PLAYER_RESPONSE_PATTERN.search(html)
    if not match:
        return {}
    payload = json.loads(match.group(1))
    if not isinstance(payload, dict):
        raise TypeError("YouTube player response must be an object")
    return payload


def _hls_variant_urls(manifest: str, manifest_url: str) -> list[str]:
    variants: list[tuple[int, str]] = []
    pending_bandwidth: int | None = None
    for raw_line in manifest.splitlines():
        line = raw_line.strip()
        if line.startswith("#EXT-X-STREAM-INF:"):
            match = BANDWIDTH_PATTERN.search(line.removeprefix("#EXT-X-STREAM-INF:"))
            pending_bandwidth = int(match.group(1)) if match else 0
            continue
        if not line or line.startswith("#"):
            continue
        if pending_bandwidth is not None:
            variants.append(
                (pending_bandwidth, _require_http_url(urljoin(manifest_url, line)))
            )
            pending_bandwidth = None
    if variants:
        return [url for _bandwidth, url in sorted(variants, reverse=True)]
    fallback_urls = []
    for raw_line in manifest.splitlines():
        line = raw_line.strip()
        if line.endswith(".m3u8"):
            fallback_urls.append(_require_http_url(urljoin(manifest_url, line)))
    return fallback_urls


def _require_http_url(url: str) -> str:
    parsed = urlsplit(url)
    if parsed.scheme not in {"http", "https"} or not parsed.netloc:
        raise YouTubeResolverError("YouTube HLS variant must use an HTTP(S) URL")
    return url


def _required_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise TypeError(f"YouTube response is missing {key}")
    return value


def _optional_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _as_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().casefold() in {"1", "true", "yes"}
    return bool(value)


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""
