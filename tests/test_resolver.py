import asyncio
from types import SimpleNamespace

import pytest

from reco_box.domain import Platform
from reco_box.network_policy import NetworkPolicy, TLSEndpointOverride
from reco_box.resolver import (
    AnonymousAccessUnavailableError,
    DouyinLiveRecorderResolver,
    normalize_payload,
)


def test_normalize_nested_stream_urls() -> None:
    result = normalize_payload(
        Platform.DOUYIN,
        {
            "is_live": True,
            "anchor_name": "主播",
            "title": "直播标题",
            "streams": {"flv_url": "https://cdn.example/live.flv"},
        },
    )
    assert result.is_live is True
    assert result.streamer_name == "主播"
    assert result.stream_urls == ("https://cdn.example/live.flv",)


def test_resolver_never_passes_account_credentials() -> None:
    captured = {}

    async def get_douyin_stream_data(url, proxy_addr=None, cookies=None):
        captured.update(url=url, proxy_addr=proxy_addr, cookies=cookies)
        return {"is_live": False}

    async def get_douyin_stream_url(payload, quality, proxy):
        captured.update(quality=quality, stream_proxy=proxy)
        return payload

    spider = SimpleNamespace(get_douyin_stream_data=get_douyin_stream_data)
    stream = SimpleNamespace(get_douyin_stream_url=get_douyin_stream_url)
    resolver = DouyinLiveRecorderResolver(spider_module=spider, stream_module=stream)
    result = asyncio.run(resolver.resolve("https://live.douyin.com/123", quality="高清"))

    assert result.is_live is False
    assert captured["cookies"] is None
    assert captured["quality"] == "HD"


def test_bilibili_uses_room_info_and_selected_quality() -> None:
    captured = {}

    async def get_bilibili_room_info(url, proxy_addr=None, cookies=None):
        captured.update(url=url, proxy_addr=proxy_addr, cookies=cookies)
        return {"anchor_name": "主播", "live_status": True, "room_url": url}

    async def get_bilibili_stream_url(payload, quality, proxy_addr, cookies):
        captured.update(quality=quality, stream_cookies=cookies)
        return {
            "anchor_name": payload["anchor_name"],
            "is_live": True,
            "record_url": "https://cdn.example.com/live.flv",
        }

    resolver = DouyinLiveRecorderResolver(
        spider_module=SimpleNamespace(get_bilibili_room_info=get_bilibili_room_info),
        stream_module=SimpleNamespace(get_bilibili_stream_url=get_bilibili_stream_url),
    )
    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6", quality="超清"))

    assert result.streamer_name == "主播"
    assert result.stream_urls == ("https://cdn.example.com/live.flv",)
    assert captured["quality"] == "UHD"
    assert captured["cookies"] is None
    assert captured["stream_cookies"] is None


def test_page_url_is_never_treated_as_media_stream() -> None:
    result = normalize_payload(
        Platform.BILIBILI,
        {
            "is_live": True,
            "room_url": "https://live.bilibili.com/6",
            "record_url": "https://cdn.example.com/live.flv",
        },
    )
    assert result.stream_urls == ("https://cdn.example.com/live.flv",)


def test_taobao_reports_anonymous_access_limit_without_calling_upstream() -> None:
    resolver = DouyinLiveRecorderResolver(spider_module=SimpleNamespace())
    with pytest.raises(AnonymousAccessUnavailableError, match="不导入账号或 Cookie"):
        asyncio.run(resolver.resolve("https://m.tb.cn/example"))


def test_twitcasting_forwards_anonymous_viewer_headers_to_ffmpeg() -> None:
    captured = {"verify": []}

    async def async_req(url, proxy_addr=None, headers=None, verify=None):
        captured["verify"].append(verify)
        if "streamserver.php" in url:
            return '{"tc-hls":{"streams":{"high":"https://cdn.example/live.m3u8"}}}'
        return (
            '<title>Demo (@demo) TwitCasting</title>'
            '<div data-is-onlive="true" data-movie-id="123"></div>'
        )

    resolver = DouyinLiveRecorderResolver(
        spider_module=SimpleNamespace(async_req=async_req)
    )
    result = asyncio.run(resolver.resolve("https://twitcasting.tv/demo"))

    assert result.stream_urls == ("https://cdn.example/live.m3u8",)
    assert "Referer: https://twitcasting.tv/\r\n" in result.headers
    assert result.headers.endswith("\r\n")
    assert captured["verify"] == [True, True]


def test_twitcasting_applies_exact_host_override_through_resolver() -> None:
    captured = {"verify": []}

    async def async_req(url, proxy_addr=None, headers=None, verify=None):
        captured["verify"].append(verify)
        if "streamserver.php" in url:
            return '{"tc-hls":{"streams":{"high":"https://cdn.example/live.m3u8"}}}'
        return (
            '<title>Demo (@demo) TwitCasting</title>'
            '<div data-is-onlive="true" data-movie-id="123"></div>'
        )

    policy = NetworkPolicy(
        tls_overrides=(
            TLSEndpointOverride(
                Platform.TWITCASTING,
                "twitcasting.tv",
                "test-only exact-host compatibility override",
            ),
        )
    )
    resolver = DouyinLiveRecorderResolver(
        spider_module=SimpleNamespace(async_req=async_req),
        network_policy=policy,
    )

    result = asyncio.run(resolver.resolve("https://twitcasting.tv/demo"))

    assert result.stream_urls == ("https://cdn.example/live.m3u8",)
    assert captured["verify"] == [False, False]


@pytest.mark.parametrize(
    ("url", "platform", "function_name"),
    [
        ("https://www.twitch.tv/demo", Platform.TWITCH, "get_twitchtv_stream_data"),
        ("https://www.sooplive.com/demo", Platform.SOOP, "get_sooplive_stream_data"),
        ("https://chzzk.naver.com/live/demo", Platform.CHZZK, "get_chzzk_stream_data"),
        ("https://www.showroom-live.com/room/profile?room_id=1", Platform.SHOWROOM, "get_showroom_stream_data"),
        ("https://www.bigo.tv/cn/demo", Platform.BIGO, "get_bigo_stream_url"),
        ("https://17.live/en/live/1", Platform.LIVE17, "get_17live_stream_url"),
        ("https://www.liveme.com/en/v/1/index.html", Platform.LIVEME, "get_liveme_stream_url"),
        ("https://www.picarto.tv/demo", Platform.PICARTO, "get_picarto_stream_url"),
        ("https://live.shopee.sg/share?session=1", Platform.SHOPEE, "get_shopee_stream_url"),
    ],
)
def test_overseas_resolvers_use_anonymous_upstream_functions(
    url, platform, function_name
) -> None:
    captured = {}

    async def resolve_upstream(value, proxy_addr=None, cookies=None, **kwargs):
        captured.update(url=value, proxy=proxy_addr, cookies=cookies, kwargs=kwargs)
        return {
            "anchor_name": "demo",
            "is_live": True,
            "record_url": "https://cdn.example/live.m3u8",
        }

    resolver = DouyinLiveRecorderResolver(
        spider_module=SimpleNamespace(**{function_name: resolve_upstream})
    )
    result = asyncio.run(resolver.resolve(url, proxy="127.0.0.1:7890"))

    assert result.platform is platform
    assert result.stream_urls == ("https://cdn.example/live.m3u8",)
    assert captured["cookies"] is None
    assert captured["proxy"] == "http://127.0.0.1:7890"
