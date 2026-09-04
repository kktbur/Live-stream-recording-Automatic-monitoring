from __future__ import annotations

from collections.abc import Callable, Mapping
from typing import Any
from urllib.parse import urljoin, urlsplit

import httpx

from .domain import Platform
from .network_policy import DEFAULT_NETWORK_POLICY, NetworkPolicy

BILIBILI_API_ORIGIN = "https://api.live.bilibili.com"
ROOM_INIT_URL = f"{BILIBILI_API_ORIGIN}/room/v1/Room/room_init"
MASTER_INFO_URL = f"{BILIBILI_API_ORIGIN}/live_user/v1/Master/info"
H5_ROOM_INFO_URL = f"{BILIBILI_API_ORIGIN}/xlive/web-room/v1/index/getH5InfoByRoom"
LEGACY_PLAY_URL = f"{BILIBILI_API_ORIGIN}/room/v1/Room/playUrl"
ROOM_PLAY_INFO_URL = f"{BILIBILI_API_ORIGIN}/xlive/web-room/v2/index/getRoomPlayInfo"
REDIRECT_STATUSES = {301, 302, 303, 307, 308}
MAX_REDIRECTS = 5

QUALITY_CODES = {
    "OD": "10000",
    "BD": "400",
    "UHD": "250",
    "HD": "150",
    "SD": "80",
    "LD": "80",
}

ClientFactory = Callable[..., httpx.AsyncClient]


class BilibiliResolverError(RuntimeError):
    """Base error for an invalid or unavailable Bilibili public response."""


class BilibiliAnonymousAccessUnavailableError(BilibiliResolverError):
    """The public Bilibili endpoint rejected an anonymous request."""


class BilibiliResolver:
    """Resolve public Bilibili rooms through a first-party verified client."""

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
    ) -> dict[str, Any]:
        transport = _BilibiliTransport(
            network_policy=self.network_policy,
            client_factory=self._client_factory,
            proxy_addr=proxy_addr,
        )
        _resolved_url, room_id = await transport.resolve_room(url)

        room_payload = await transport.get_json(
            ROOM_INIT_URL, {"id": room_id}, require_success=True
        )
        room_data = _required_mapping(room_payload, "data")
        uid = _positive_int(room_data.get("uid"), "Bilibili room owner")
        live_status = _as_int(room_data.get("live_status")) == 1

        master_payload = await transport.get_json(
            MASTER_INFO_URL, {"uid": uid}, require_success=True
        )
        master_data = _required_mapping(master_payload, "data")
        anchor_info = _required_mapping(master_data, "info")
        anchor_name = _text(anchor_info.get("uname"))

        h5_payload = await transport.get_json(
            H5_ROOM_INFO_URL, {"room_id": room_id}, require_success=True
        )
        h5_data = _optional_mapping(h5_payload.get("data"))
        room_info = _optional_mapping(h5_data.get("room_info"))
        title = _text(room_info.get("title"))

        result: dict[str, Any] = {
            "anchor_name": anchor_name,
            "live_status": live_status,
            "room_url": url,
            "title": title,
        }
        if not live_status:
            return result

        record_url = await self._play_url(transport, room_id, quality_code)
        if record_url:
            result["record_url"] = record_url
        return result

    async def _play_url(
        self,
        transport: _BilibiliTransport,
        room_id: str,
        quality_code: str,
    ) -> str:
        qn = QUALITY_CODES.get(quality_code, QUALITY_CODES["OD"])
        legacy_payload = await transport.get_json(
            LEGACY_PLAY_URL,
            {"cid": room_id, "qn": qn, "platform": "web"},
        )
        if _as_int(legacy_payload.get("code")) == 0:
            legacy_url = _legacy_url(legacy_payload)
            if legacy_url:
                return legacy_url

        modern_payload = await transport.get_json(
            ROOM_PLAY_INFO_URL,
            {
                "room_id": room_id,
                "protocol": "0,1",
                "format": "0,1,2",
                "codec": "0,1,2",
                "qn": qn,
                "platform": "web",
                "ptype": "8",
                "dolby": "5",
                "panorama": "1",
                "hdr_type": "0,1",
            },
            require_success=True,
        )
        return _modern_url(modern_payload, quality_code)


class _BilibiliTransport:
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
            "Accept": "application/json, text/plain, */*",
            "Accept-Language": "zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3",
            "Origin": "https://live.bilibili.com",
            "Referer": "https://live.bilibili.com/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/127.0",
        }

    async def resolve_room(self, url: str) -> tuple[str, str]:
        room_id = _room_id_or_none(url)
        if room_id:
            return url, room_id

        hostname = (urlsplit(url).hostname or "").rstrip(".").casefold()
        if hostname != "b23.tv" and not hostname.endswith(".b23.tv"):
            raise ValueError("Bilibili room URL does not contain a numeric room id")

        response = await self._get_response(url, {})
        resolved_url = str(response.url)
        resolved_host = (urlsplit(resolved_url).hostname or "").rstrip(".").casefold()
        if resolved_host != "live.bilibili.com" and not resolved_host.endswith(
            ".live.bilibili.com"
        ):
            raise ValueError("Bilibili short URL did not resolve to a Bilibili live room")
        resolved_room_id = _room_id(resolved_url)
        return resolved_url, resolved_room_id

    async def get_json(
        self,
        url: str,
        params: Mapping[str, Any],
        *,
        require_success: bool = False,
    ) -> dict[str, Any]:
        response = await self._get_response(url, params)
        if response.status_code in {401, 403, 412}:
            raise BilibiliAnonymousAccessUnavailableError(
                f"Bilibili anonymous access unavailable at {url} (HTTP {response.status_code})"
            )
        response.raise_for_status()
        payload = response.json()
        if not isinstance(payload, dict):
            raise TypeError("Bilibili API returned a non-object JSON response")
        if require_success and "code" in payload and _as_int(payload.get("code")) != 0:
            code = _as_int(payload.get("code"))
            raise BilibiliAnonymousAccessUnavailableError(
                f"Bilibili anonymous access unavailable at {url} (code {code})"
            )
        return payload

    async def _get_response(
        self, url: str, params: Mapping[str, Any]
    ) -> httpx.Response:
        next_url = url
        next_params = dict(params)
        for _ in range(MAX_REDIRECTS + 1):
            verify = self._network_policy.verify_for(Platform.BILIBILI, next_url)
            async with self._client_factory(
                headers=self._headers,
                http2=True,
                follow_redirects=False,
                proxy=self._proxy_addr,
                timeout=20,
                verify=verify,
            ) as client:
                response = await client.get(next_url, params=next_params)
            if response.status_code not in REDIRECT_STATUSES:
                return response
            location = _text(response.headers.get("location"))
            if not location:
                raise BilibiliResolverError(
                    f"Bilibili endpoint returned HTTP {response.status_code} without a redirect target"
                )
            next_url = urljoin(next_url, location)
            next_params = {}
        raise BilibiliResolverError("Bilibili endpoint exceeded the redirect limit")


def _room_id(url: str) -> str:
    room_id = _room_id_or_none(url)
    if not room_id:
        raise ValueError("Bilibili room URL does not contain a numeric room id")
    return room_id


def _room_id_or_none(url: str) -> str | None:
    room_id = urlsplit(url).path.rstrip("/").rsplit("/", 1)[-1]
    return room_id if room_id.isdigit() else None


def _required_mapping(payload: Mapping[str, Any], key: str) -> Mapping[str, Any]:
    value = payload.get(key)
    if not isinstance(value, Mapping):
        raise TypeError(f"Bilibili API response is missing {key}")
    return value


def _optional_mapping(value: Any) -> Mapping[str, Any]:
    return value if isinstance(value, Mapping) else {}


def _positive_int(value: Any, label: str) -> int:
    number = _as_int(value)
    if number <= 0:
        raise ValueError(f"Bilibili API returned an invalid {label}")
    return number


def _as_int(value: Any) -> int:
    try:
        return int(value)
    except (TypeError, ValueError):
        return 0


def _text(value: Any) -> str:
    return value.strip() if isinstance(value, str) else ""


def _legacy_url(payload: Mapping[str, Any]) -> str:
    data = _optional_mapping(payload.get("data"))
    durls = data.get("durl")
    if not isinstance(durls, list):
        return ""
    urls = [
        _text(item.get("url"))
        for item in durls
        if isinstance(item, Mapping) and _text(item.get("url"))
    ]
    preferred = next((url for url in urls if "d1--cn-gotcha" in url), "")
    return preferred or (urls[-1] if urls else "")


def _modern_url(payload: Mapping[str, Any], quality_code: str) -> str:
    data = _optional_mapping(payload.get("data"))
    if _as_int(data.get("live_status")) == 0:
        return ""
    playurl_info = _optional_mapping(data.get("playurl_info"))
    playurl = _optional_mapping(playurl_info.get("playurl"))
    streams = playurl.get("stream")
    first_stream = streams[0] if isinstance(streams, list) and streams else {}
    formats = _optional_mapping(first_stream).get("format")
    first_format = formats[0] if isinstance(formats, list) and formats else {}
    codecs = _optional_mapping(first_format).get("codec")
    if not isinstance(codecs, list) or not codecs:
        return ""

    sorted_codecs = sorted(codecs, key=lambda item: _as_int(item.get("current_qn")), reverse=True)
    quality_index = {"OD": 0, "BD": 1, "UHD": 2, "HD": 3, "SD": 4, "LD": 4}.get(
        quality_code, 0
    )
    selected = _optional_mapping(sorted_codecs[min(quality_index, len(sorted_codecs) - 1)])
    url_info = selected.get("url_info")
    first_url = url_info[0] if isinstance(url_info, list) and url_info else {}
    first_url = _optional_mapping(first_url)
    host = _text(first_url.get("host"))
    base_url = _text(selected.get("base_url"))
    extra = _text(first_url.get("extra"))
    return f"{host}{base_url}{extra}" if host and base_url else ""
