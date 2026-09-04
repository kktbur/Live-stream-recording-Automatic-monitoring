import asyncio
from typing import Any, Self

import httpx
import pytest

from reco_box.bilibili import (
    H5_ROOM_INFO_URL,
    LEGACY_PLAY_URL,
    MASTER_INFO_URL,
    ROOM_INIT_URL,
    ROOM_PLAY_INFO_URL,
    BilibiliResolver,
)
from reco_box.domain import Platform
from reco_box.network_policy import NetworkPolicy, TLSEndpointOverride


class FakeResponse:
    def __init__(
        self,
        payload: Any,
        *,
        url: str,
        status_code: int = 200,
        headers: dict[str, str] | None = None,
    ) -> None:
        self._payload = payload
        self.url = url
        self.status_code = status_code
        self.headers = headers or {}

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("GET", self.url)
            response = httpx.Response(self.status_code, request=request)
            raise httpx.HTTPStatusError("fake HTTP error", request=request, response=response)

    def json(self) -> Any:
        return self._payload


class FakeAsyncClient:
    def __init__(self, response: Any, call_log: list[tuple[str, dict[str, Any]]]) -> None:
        self._response = response
        self._call_log = call_log
        self.calls: list[tuple[str, dict[str, Any]]] = []

    async def __aenter__(self) -> Self:
        return self

    async def __aexit__(self, *_args: object) -> None:
        return None

    async def get(self, url: str, params: dict[str, Any]) -> FakeResponse:
        call = (url, params)
        self.calls.append(call)
        self._call_log.append(call)
        if isinstance(self._response, FakeResponse):
            return self._response
        return FakeResponse(self._response, url=url)


def _factory_for(
    responses: list[Any], captured: dict[str, Any]
):
    response_index = 0

    def factory(**kwargs: Any) -> FakeAsyncClient:
        nonlocal response_index
        captured.setdefault("client_kwargs", []).append(kwargs)
        captured.update(kwargs)
        response = responses[response_index]
        response_index += 1
        client = FakeAsyncClient(response, captured.setdefault("calls", []))
        captured.setdefault("clients", []).append(client)
        return client

    return factory


def _base_live_responses() -> list[dict[str, Any]]:
    return [
        {"code": 0, "data": {"uid": 42, "live_status": 1}},
        {"code": 0, "data": {"info": {"uname": "主播"}}},
        {"code": 0, "data": {"room_info": {"title": "直播标题"}}},
    ]


def test_bilibili_resolver_uses_verified_anonymous_httpx_client() -> None:
    captured: dict[str, Any] = {}
    responses = _base_live_responses()
    responses.append(
        {
            "code": 0,
            "data": {"durl": [{"url": "https://cdn.example/live.flv"}]},
        }
    )

    resolver = BilibiliResolver(
        client_factory=_factory_for(responses, captured),
    )
    result = asyncio.run(
        resolver.resolve(
            "https://live.bilibili.com/6",
            proxy_addr="http://127.0.0.1:7890",
            quality_code="UHD",
        )
    )

    assert result == {
        "anchor_name": "主播",
        "live_status": True,
        "room_url": "https://live.bilibili.com/6",
        "title": "直播标题",
        "record_url": "https://cdn.example/live.flv",
    }
    assert captured["client_kwargs"][0]["verify"] is True
    assert captured["proxy"] == "http://127.0.0.1:7890"
    assert captured["follow_redirects"] is False
    assert captured["http2"] is True
    assert "Cookie" not in captured["headers"]
    assert all("cookies" not in kwargs for kwargs in captured["client_kwargs"])

    calls = captured["calls"]
    assert [url for url, _params in calls] == [
        ROOM_INIT_URL,
        MASTER_INFO_URL,
        H5_ROOM_INFO_URL,
        LEGACY_PLAY_URL,
    ]
    assert calls[0][1] == {"id": "6"}
    assert calls[3][1]["qn"] == "250"


def test_bilibili_resolver_falls_back_to_modern_play_url() -> None:
    captured: dict[str, Any] = {}
    responses = _base_live_responses()
    responses.extend(
        [
            {"code": -400, "data": {}},
            {
                "code": 0,
                "data": {
                    "live_status": 1,
                    "playurl_info": {
                        "playurl": {
                            "stream": [
                                {
                                    "format": [
                                        {
                                            "codec": [
                                                {
                                                    "current_qn": 10000,
                                                    "base_url": "/live/od.flv",
                                                    "url_info": [
                                                        {
                                                            "host": "https://cdn.example",
                                                            "extra": "?quality=od",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "current_qn": 400,
                                                    "base_url": "/live/bd.flv",
                                                    "url_info": [
                                                        {
                                                            "host": "https://cdn.example",
                                                            "extra": "?quality=bd",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "current_qn": 250,
                                                    "base_url": "/live/uhd.flv",
                                                    "url_info": [
                                                        {
                                                            "host": "https://cdn.example",
                                                            "extra": "?quality=uhd",
                                                        }
                                                    ],
                                                },
                                                {
                                                    "current_qn": 150,
                                                    "base_url": "/live/hd.flv",
                                                    "url_info": [
                                                        {
                                                            "host": "https://cdn.example",
                                                            "extra": "?quality=hd",
                                                        }
                                                    ],
                                                },
                                            ]
                                        }
                                    ]
                                }
                            ]
                        }
                    },
                },
            },
        ]
    )

    resolver = BilibiliResolver(
        client_factory=_factory_for(responses, captured),
    )
    result = asyncio.run(
        resolver.resolve("https://live.bilibili.com/6", quality_code="HD")
    )

    assert result["record_url"] == "https://cdn.example/live/hd.flv?quality=hd"
    calls = captured["calls"]
    assert [url for url, _params in calls][-2:] == [LEGACY_PLAY_URL, ROOM_PLAY_INFO_URL]
    assert calls[-2][1]["qn"] == "150"
    assert calls[-1][1]["qn"] == "150"


def test_bilibili_tls_override_is_exact_host_and_platform_scoped() -> None:
    captured: dict[str, Any] = {}
    policy = NetworkPolicy(
        tls_overrides=(
            TLSEndpointOverride(
                Platform.BILIBILI,
                "api.live.bilibili.com",
                "test-only compatibility placeholder",
            ),
        )
    )
    responses = [
        {"code": 0, "data": {"uid": 42, "live_status": 0}},
        {"code": 0, "data": {"info": {"uname": "主播"}}},
        {"code": 0, "data": {"room_info": {"title": "离线房间"}}},
    ]

    resolver = BilibiliResolver(
        network_policy=policy,
        client_factory=_factory_for(responses, captured),
    )
    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6"))

    assert result["live_status"] is False
    assert captured["client_kwargs"][0]["verify"] is False
    assert policy.verify_for(Platform.BILIBILI, ROOM_INIT_URL) is False
    assert policy.verify_for(
        Platform.BILIBILI, "https://api.live.bilibili.com.evil.example/room"
    ) is True
    assert policy.verify_for(Platform.TWITCH, ROOM_INIT_URL) is True


def test_bilibili_redirect_rechecks_tls_policy_for_new_host() -> None:
    captured: dict[str, Any] = {}
    policy = NetworkPolicy(
        tls_overrides=(
            TLSEndpointOverride(
                Platform.BILIBILI,
                "api.live.bilibili.com",
                "test-only exact-host compatibility placeholder",
            ),
        )
    )
    responses = [
        FakeResponse(
            {},
            url=ROOM_INIT_URL,
            status_code=302,
            headers={"location": "https://redirect.example/room_init"},
        ),
        {"code": 0, "data": {"uid": 42, "live_status": 0}},
        {"code": 0, "data": {"info": {"uname": "主播"}}},
        {"code": 0, "data": {"room_info": {"title": "重定向房间"}}},
    ]

    resolver = BilibiliResolver(
        network_policy=policy,
        client_factory=_factory_for(responses, captured),
    )
    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6"))

    assert result["live_status"] is False
    assert [kwargs["verify"] for kwargs in captured["client_kwargs"][:2]] == [False, True]
    assert captured["calls"][1][0] == "https://redirect.example/room_init"


def test_bilibili_resolver_supports_b23_short_link_redirect() -> None:
    captured: dict[str, Any] = {}
    responses: list[Any] = [
        FakeResponse(
            {},
            url="https://live.bilibili.com/6",
            status_code=302,
            headers={"location": "https://live.bilibili.com/6"},
        ),
        FakeResponse({}, url="https://live.bilibili.com/6"),
        *_base_live_responses(),
        {"code": 0, "data": {"durl": [{"url": "https://cdn.example/live.flv"}]}},
    ]

    resolver = BilibiliResolver(
        client_factory=_factory_for(responses, captured),
    )
    result = asyncio.run(resolver.resolve("https://b23.tv/short-room"))

    assert result["room_url"] == "https://b23.tv/short-room"
    assert result["live_status"] is True
    assert captured["calls"][0] == ("https://b23.tv/short-room", {})
    assert captured["calls"][2][0] == ROOM_INIT_URL


def test_bilibili_resolver_treats_anonymous_access_denied_as_offline() -> None:
    captured: dict[str, Any] = {}
    resolver = BilibiliResolver(
        client_factory=_factory_for([{"code": -101, "data": {}}], captured),
    )

    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6"))

    assert result == {
        "anchor_name": "",
        "live_status": False,
        "room_url": "https://live.bilibili.com/6",
    }


@pytest.mark.parametrize("status_code", [403, 500])
def test_bilibili_resolver_treats_http_errors_as_offline(status_code: int) -> None:
    captured: dict[str, Any] = {}
    resolver = BilibiliResolver(
        client_factory=_factory_for(
            [FakeResponse({}, url=ROOM_INIT_URL, status_code=status_code)], captured
        ),
    )

    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6"))

    assert result["live_status"] is False
    assert result["room_url"] == "https://live.bilibili.com/6"


def test_bilibili_resolver_reports_malformed_api_response() -> None:
    captured: dict[str, Any] = {}
    resolver = BilibiliResolver(
        client_factory=_factory_for([[]], captured),
    )

    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6"))

    assert result["live_status"] is False


def test_bilibili_resolver_treats_malformed_nested_codec_as_offline() -> None:
    captured: dict[str, Any] = {}
    responses = _base_live_responses()
    responses.extend(
        [
            {"code": -400, "data": {}},
            {
                "code": 0,
                "data": {
                    "live_status": 1,
                    "playurl_info": {
                        "playurl": {
                            "stream": [{"format": [{"codec": ["not-an-object"]}]}]
                        }
                    },
                },
            },
        ]
    )
    resolver = BilibiliResolver(client_factory=_factory_for(responses, captured))

    result = asyncio.run(resolver.resolve("https://live.bilibili.com/6"))

    assert result == {
        "anchor_name": "",
        "live_status": False,
        "room_url": "https://live.bilibili.com/6",
    }


def test_bilibili_resolver_rejects_room_urls_without_numeric_id() -> None:
    captured: dict[str, Any] = {}
    resolver = BilibiliResolver(client_factory=_factory_for([], captured))

    result = asyncio.run(resolver.resolve("https://live.bilibili.com/room/demo"))

    assert result["live_status"] is False
    assert "client" not in captured
