from __future__ import annotations

import importlib
import os
import sys
from dataclasses import dataclass
from pathlib import Path
from types import ModuleType
from typing import Any

from platformdirs import user_data_path

from .bilibili import BilibiliResolver
from .domain import Platform
from .localization import tr
from .network import normalize_proxy
from .network_policy import DEFAULT_NETWORK_POLICY, NetworkPolicy
from .platforms import detect_platform
from .resources import upstream_resource


class UnsupportedPlatformError(ValueError):
    pass


class AnonymousAccessUnavailableError(RuntimeError):
    pass


QUALITY_CODES = {
    "原画": "OD",
    "蓝光": "BD",
    "超清": "UHD",
    "高清": "HD",
    "标清": "SD",
    "流畅": "LD",
}


@dataclass(slots=True, frozen=True)
class ResolvedStream:
    platform: Platform
    is_live: bool
    streamer_name: str
    title: str
    stream_urls: tuple[str, ...]
    headers: str = ""


def default_upstream_path() -> Path:
    return upstream_resource()


def default_upstream_runtime_path() -> Path:
    override = os.environ.get("RECO_BOX_UPSTREAM_RUNTIME_DIR", "").strip()
    if override:
        return Path(override)
    data_override = os.environ.get("RECO_BOX_DATA_DIR", "").strip()
    if data_override:
        return Path(data_override) / "upstream-runtime"
    return Path(user_data_path("Reco Box", "Reco Box")) / "upstream-runtime"


class DouyinLiveRecorderResolver:
    """Thin anonymous-only adapter around the pinned v4.0.7 resolver functions."""

    def __init__(
        self,
        spider_module: ModuleType | None = None,
        stream_module: ModuleType | None = None,
        upstream_path: Path | None = None,
        runtime_path: Path | None = None,
        network_policy: NetworkPolicy | None = None,
        bilibili_resolver: BilibiliResolver | None = None,
    ):
        self._spider = spider_module
        self._stream = stream_module
        self.upstream_path = Path(upstream_path or default_upstream_path())
        self.runtime_path = Path(runtime_path or default_upstream_runtime_path())
        self.network_policy = network_policy or DEFAULT_NETWORK_POLICY
        self._bilibili_resolver = bilibili_resolver or BilibiliResolver(
            network_policy=self.network_policy
        )

    def _load_spider(self) -> ModuleType:
        if self._spider is not None:
            return self._spider
        if not (self.upstream_path / "src" / "spider.py").exists():
            raise RuntimeError(tr("找不到已锁定的解析源码：{path}").format(path=self.upstream_path))
        upstream = str(self.upstream_path)
        if upstream not in sys.path:
            sys.path.insert(0, upstream)
        self.runtime_path.mkdir(parents=True, exist_ok=True)
        original_argv0 = sys.argv[0]
        original_stderr = sys.stderr
        null_stderr = None
        try:
            # v4.0.7 derives its log directory from argv[0]. Redirect that legacy
            # behavior away from Program Files and into Reco Box application data.
            sys.argv[0] = str(self.runtime_path / "reco-box-runtime.exe")
            # A PyInstaller windowed executable has no console and therefore no
            # sys.stderr. The upstream logger requires a writable sink while it
            # is imported; Reco Box removes every upstream sink immediately after.
            if sys.stderr is None:
                null_stderr = open(os.devnull, "w", encoding="utf-8")  # noqa: SIM115
                sys.stderr = null_stderr
            self._spider = importlib.import_module("src.spider")
            upstream_logger = importlib.import_module("src.logger").logger
            # The upstream INFO sink writes full transient play URLs. Reco Box
            # disables those sinks so sensitive stream URLs never enter logs.
            upstream_logger.remove()
        finally:
            sys.argv[0] = original_argv0
            sys.stderr = original_stderr
            if null_stderr is not None:
                null_stderr.close()
        return self._spider

    def _load_stream(self) -> ModuleType:
        self._load_spider()
        if self._stream is None:
            self._stream = importlib.import_module("src.stream")
        return self._stream

    async def resolve(self, url: str, proxy: str = "", quality: str = "原画") -> ResolvedStream:
        platform = detect_platform(url)
        if platform is Platform.UNKNOWN:
            raise UnsupportedPlatformError(tr("暂不支持该直播间链接"))
        proxy_addr = normalize_proxy(proxy) or None
        quality_code = QUALITY_CODES.get(quality, "OD")

        if platform is Platform.BILIBILI:
            payload = await self._bilibili_resolver.resolve(
                url, proxy_addr=proxy_addr, quality_code=quality_code
            )
            return normalize_payload(platform, payload)

        spider = self._load_spider()
        if platform is Platform.DOUYIN:
            raw = await spider.get_douyin_stream_data(url, proxy_addr=proxy_addr, cookies=None)
            payload = await self._load_stream().get_douyin_stream_url(
                raw, quality_code, proxy_addr
            )
        elif platform is Platform.KUAISHOU:
            raw = await spider.get_kuaishou_stream_data(url, proxy_addr=proxy_addr, cookies=None)
            payload = await self._load_stream().get_kuaishou_stream_url(raw, quality_code)
        elif platform is Platform.TIKTOK:
            raw = await spider.get_tiktok_stream_data(url, proxy_addr=proxy_addr, cookies=None)
            payload = await self._load_stream().get_tiktok_stream_url(
                raw, quality_code, proxy_addr
            )
        elif platform is Platform.YOUTUBE:
            raw = await spider.get_youtube_stream_url(url, proxy_addr=proxy_addr, cookies=None)
            payload = await self._load_stream().get_stream_url(raw, quality_code, spec=True)
        elif platform is Platform.TAOBAO:
            raise AnonymousAccessUnavailableError(
                tr(
                    "当前锁定版淘宝解析器要求登录会话，Reco Box 不导入账号或 Cookie，"
                    "因此暂不尝试绕过；后续需要实现匿名公开接口后才能启用。"
                )
            )
        elif platform is Platform.TWITCASTING:
            payload = await self._resolve_twitcasting_anonymous(spider, url, proxy_addr)
        else:
            function_names = {
                Platform.XIAOHONGSHU: "get_xhs_stream_url",
                Platform.JD: "get_jd_stream_url",
                Platform.TWITCH: "get_twitchtv_stream_data",
                Platform.SOOP: "get_sooplive_stream_data",
                Platform.CHZZK: "get_chzzk_stream_data",
                Platform.SHOWROOM: "get_showroom_stream_data",
                Platform.BIGO: "get_bigo_stream_url",
                Platform.LIVE17: "get_17live_stream_url",
                Platform.LIVEME: "get_liveme_stream_url",
                Platform.PICARTO: "get_picarto_stream_url",
                Platform.SHOPEE: "get_shopee_stream_url",
            }
            function = getattr(spider, function_names[platform])
            if platform is Platform.SOOP:
                payload = await function(
                    url,
                    proxy_addr=proxy_addr,
                    cookies=None,
                    username=None,
                    password=None,
                )
            else:
                payload = await function(url, proxy_addr=proxy_addr, cookies=None)
        return normalize_payload(platform, payload)

    async def _resolve_twitcasting_anonymous(
        self, spider: ModuleType, url: str, proxy_addr: str | None
    ) -> dict[str, Any]:
        """Resolve public TwitCasting rooms without invoking upstream login helpers."""
        import json
        import re

        headers = {
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.8",
            "Referer": "https://twitcasting.tv/",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) Firefox/124.0",
        }
        if "login=true" in url.lower():
            raise AnonymousAccessUnavailableError(tr("该 TwitCasting 直播间要求登录，匿名模式不可用"))
        html = await self._anonymous_request(spider, url, proxy_addr, headers)
        anchor = re.search(r"<title>(.*?) \(@(.*?)\).*?Twit", str(html), re.DOTALL)
        status = re.search(r'data-is-onlive="(.*?)"', str(html))
        movie_id = re.search(r'data-movie-id="(.*?)"', str(html))
        if not anchor or not status or not movie_id:
            raise AnonymousAccessUnavailableError(
                tr("该 TwitCasting 页面无法匿名读取，可能需要登录或已受访问限制")
            )
        result: dict[str, Any] = {
            "anchor_name": f"{anchor.group(1).strip()}-{anchor.group(2)}-{movie_id.group(1)}",
            "is_live": status.group(1) == "true",
            "headers": _ffmpeg_headers(headers),
        }
        if not result["is_live"]:
            return result
        anchor_id = url.split("?")[0].rstrip("/").rsplit("/", 1)[-1]
        endpoint = (
            "https://twitcasting.tv/streamserver.php?"
            f"target={anchor_id}&mode=client&player=pc_web"
        )
        stream_text = await self._anonymous_request(spider, endpoint, proxy_addr, headers)
        streams = json.loads(str(stream_text)).get("tc-hls", {}).get("streams", {})
        quality_order = {"high": 0, "medium": 1, "low": 2}
        play_urls = [
            value
            for key, value in sorted(
                streams.items(), key=lambda item: quality_order.get(item[0], 99)
            )
        ]
        if not play_urls:
            raise RuntimeError(tr("TwitCasting 未返回可录制的公开播放地址"))
        result["play_url_list"] = play_urls
        return result

    async def _anonymous_request(
        self,
        spider: ModuleType,
        url: str,
        proxy_addr: str | None,
        headers: dict[str, str],
    ) -> Any:
        return await spider.async_req(
            url,
            proxy_addr=proxy_addr,
            headers=headers,
            verify=self.network_policy.verify_for(Platform.TWITCASTING, url),
        )


def _ffmpeg_headers(headers: dict[str, str]) -> str:
    return "".join(f"{key}: {value}\r\n" for key, value in headers.items())


def normalize_payload(platform: Platform, payload: Any) -> ResolvedStream:
    if isinstance(payload, str):
        urls = (payload,) if payload.startswith(("http://", "https://")) else ()
        return ResolvedStream(platform, bool(urls), "待识别主播", "", urls)
    if not isinstance(payload, dict):
        return ResolvedStream(platform, False, "待识别主播", "", ())

    urls = tuple(dict.fromkeys(_preferred_stream_urls(payload)))
    live_flags = (
        payload.get("is_live"),
        payload.get("live_status"),
        payload.get("status"),
    )
    explicit = next((flag for flag in live_flags if isinstance(flag, bool)), None)
    is_live = explicit if explicit is not None else bool(urls)
    name = _first_text(payload, "anchor_name", "user_name", "nickname", "name")
    title = _first_text(payload, "title", "room_title", "live_title")
    header_value = payload.get("headers")
    headers = header_value if isinstance(header_value, str) else ""
    return ResolvedStream(platform, is_live, name or "待识别主播", title, urls, headers)


def _first_text(payload: dict[str, Any], *keys: str) -> str:
    for key in keys:
        value = payload.get(key)
        if isinstance(value, str) and value.strip():
            return value.strip()
    return ""


def _collect_stream_urls(value: Any, key_hint: str = "") -> list[str]:
    found: list[str] = []
    if isinstance(value, dict):
        for key, child in value.items():
            found.extend(_collect_stream_urls(child, str(key).lower()))
    elif isinstance(value, (list, tuple)):
        for child in value:
            found.extend(_collect_stream_urls(child, key_hint))
    elif isinstance(value, str) and value.startswith(("http://", "https://")):
        stream_hint = any(token in key_hint for token in ("flv", "m3u8", "play", "stream", "url"))
        media_hint = any(token in value.lower() for token in (".flv", ".m3u8", "live"))
        if stream_hint and media_hint:
            found.append(value)
    return found


def _preferred_stream_urls(payload: dict[str, Any]) -> list[str]:
    found: list[str] = []
    for key in ("record_url", "flv_url", "m3u8_url"):
        found.extend(_collect_stream_urls(payload.get(key), key))
    if found:
        return found
    for key in ("play_url_list", "streams", "stream_urls"):
        found.extend(_collect_stream_urls(payload.get(key), key))
    return found
