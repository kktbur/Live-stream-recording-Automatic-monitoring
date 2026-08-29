import asyncio
from types import SimpleNamespace

import pytest

from reco_box.domain import Platform
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
