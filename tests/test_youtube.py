import asyncio
import json
from dataclasses import dataclass, field
from types import SimpleNamespace

import httpx
import pytest

from reco_box.domain import Platform
from reco_box.network_policy import NetworkPolicy, TLSEndpointOverride
from reco_box.resolver import DouyinLiveRecorderResolver
from reco_box.youtube import YouTubeResolver


@dataclass
class FakeResponse:
    body: str
    status_code: int = 200
    url: str = "https://www.youtube.com/watch?v=demo"
    headers: dict[str, str] = field(default_factory=dict)

    @property
    def text(self) -> str:
        return self.body

    def raise_for_status(self) -> None:
        if self.status_code >= 400:
            request = httpx.Request("GET", self.url)
            raise httpx.HTTPError(
                f"fake HTTP {self.status_code}", request=request
            )


class FakeAsyncClient:
    def __init__(self, responses, calls, options, **kwargs):
        self._responses = responses
        self._calls = calls
        options.append(kwargs)

    async def __aenter__(self):
        return self

    async def __aexit__(self, exc_type, exc, traceback):
        return None

    async def get(self, url, params=None):
        self._calls.append((url, params))
        return self._responses.pop(0)


def fake_client_factory(responses, calls, options):
    def factory(**kwargs):
        return FakeAsyncClient(responses, calls, options, **kwargs)

    return factory


def live_html(manifest_url: str) -> str:
    payload = {
        "videoDetails": {
            "author": "主播",
            "title": "直播标题",
            "isLive": True,
        },
        "streamingData": {"hlsManifestUrl": manifest_url},
    }
    encoded = json.dumps(payload, ensure_ascii=False)
    return (
        '<script>var ytInitialPlayerResponse = '
        f'{encoded};var meta = document.createElement("meta")</script>'
    )


def run_resolver(resolver: YouTubeResolver, url: str):
    return asyncio.run(resolver.resolve(url, proxy_addr="http://127.0.0.1:7890"))


def test_youtube_uses_verified_anonymous_httpx_and_hls_variants() -> None:
    page_url = "https://www.youtube.com/watch?v=demo"
    manifest_url = "https://manifest.example/master.m3u8"
    responses = [
        FakeResponse(live_html(manifest_url), url=page_url),
        FakeResponse(
            "#EXTM3U\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=100\n/high.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=10\n/low.m3u8\n",
            url=manifest_url,
        ),
    ]
    calls = []
    options = []
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, calls, options)
    )

    result = run_resolver(resolver, page_url)

    assert result["anchor_name"] == "主播"
    assert result["live_status"] is True
    assert result["title"] == "直播标题"
    assert result["record_url"] == "https://manifest.example/high.m3u8"
    assert result["play_url_list"] == [
        "https://manifest.example/high.m3u8",
        "https://manifest.example/low.m3u8",
    ]
    assert [url for url, _params in calls] == [page_url, manifest_url]
    assert all(option["verify"] is True for option in options)
    assert all(option["proxy"] == "http://127.0.0.1:7890" for option in options)
    assert all(option["http2"] is True for option in options)
    assert all(option["follow_redirects"] is False for option in options)
    assert all("Cookie" not in option["headers"] for option in options)


def test_youtube_rechecks_tls_policy_after_an_allowed_redirect() -> None:
    short_url = "https://youtu.be/demo"
    page_url = "https://www.youtube.com/watch?v=demo"
    manifest_url = "https://manifest.example/master.m3u8"
    responses = [
        FakeResponse(
            "",
            status_code=302,
            url=short_url,
            headers={"location": page_url},
        ),
        FakeResponse(live_html(manifest_url), url=page_url),
        FakeResponse("#EXTM3U\nhttps://manifest.example/live.m3u8\n", url=manifest_url),
    ]
    calls = []
    options = []
    policy = NetworkPolicy(
        tls_overrides=(
            TLSEndpointOverride(
                Platform.YOUTUBE,
                "youtu.be",
                "test-only exact-host compatibility override",
            ),
        )
    )
    resolver = YouTubeResolver(
        network_policy=policy,
        client_factory=fake_client_factory(responses, calls, options),
    )

    result = run_resolver(resolver, short_url)

    assert result["record_url"] == "https://manifest.example/live.m3u8"
    assert [option["verify"] for option in options] == [False, True, True]
    assert [url for url, _params in calls] == [short_url, page_url, manifest_url]


def test_youtube_selects_the_requested_quality_from_sorted_variants() -> None:
    page_url = "https://www.youtube.com/watch?v=quality"
    manifest_url = "https://manifest.example/master.m3u8"
    responses = [
        FakeResponse(live_html(manifest_url), url=page_url),
        FakeResponse(
            "#EXTM3U\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=300\n/high.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=200\n/mid.m3u8\n"
            "#EXT-X-STREAM-INF:BANDWIDTH=100\n/low.m3u8\n",
            url=manifest_url,
        ),
    ]
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, [], [])
    )

    result = asyncio.run(
        resolver.resolve(page_url, proxy_addr=None, quality_code="HD")
    )

    assert result["play_url_list"] == [
        "https://manifest.example/high.m3u8",
        "https://manifest.example/mid.m3u8",
        "https://manifest.example/low.m3u8",
    ]
    assert result["record_url"] == "https://manifest.example/low.m3u8"


def test_youtube_rejects_redirects_that_leave_the_page_host() -> None:
    page_url = "https://www.youtube.com/watch?v=demo"
    responses = [
        FakeResponse(
            "",
            status_code=302,
            url=page_url,
            headers={"location": "https://evil.example/watch?v=demo"},
        )
    ]
    calls = []
    options = []
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, calls, options)
    )

    result = run_resolver(resolver, page_url)

    assert result == {
        "anchor_name": "",
        "live_status": False,
        "room_url": page_url,
    }
    assert calls == [(page_url, {})]


@pytest.mark.parametrize("status_code", [403, 500])
def test_youtube_maps_anonymous_http_failures_to_offline(status_code: int) -> None:
    page_url = "https://www.youtube.com/watch?v=blocked"
    responses = [FakeResponse("", status_code=status_code, url=page_url)]
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, [], [])
    )

    result = run_resolver(resolver, page_url)

    assert result["live_status"] is False
    assert result["room_url"] == page_url


@pytest.mark.parametrize(
    "body",
    [
        "<html>no player response</html>",
        'var ytInitialPlayerResponse = {"videoDetails": };var meta = document.createElement',
    ],
)
def test_youtube_maps_malformed_page_payload_to_offline(body: str) -> None:
    page_url = "https://www.youtube.com/watch?v=malformed"
    responses = [FakeResponse(body, url=page_url)]
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, [], [])
    )

    result = run_resolver(resolver, page_url)

    assert result["live_status"] is False
    assert result["room_url"] == page_url


def test_youtube_maps_empty_manifest_to_offline() -> None:
    page_url = "https://www.youtube.com/watch?v=empty"
    manifest_url = "https://manifest.example/empty.m3u8"
    responses = [
        FakeResponse(live_html(manifest_url), url=page_url),
        FakeResponse("#EXTM3U\n# no variants\n", url=manifest_url),
    ]
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, [], [])
    )

    result = run_resolver(resolver, page_url)

    assert result["live_status"] is False
    assert result["room_url"] == page_url


def test_youtube_rejects_non_http_manifest_urls() -> None:
    page_url = "https://www.youtube.com/watch?v=scheme"
    responses = [FakeResponse(live_html("file:///tmp/live.m3u8"), url=page_url)]
    calls = []
    resolver = YouTubeResolver(
        client_factory=fake_client_factory(responses, calls, [])
    )

    result = run_resolver(resolver, page_url)

    assert result["live_status"] is False
    assert calls == [(page_url, {})]


def test_resolver_routes_youtube_to_first_party_adapter() -> None:
    captured = {}

    async def resolve_youtube(url, proxy_addr=None, quality_code=""):
        captured.update(url=url, proxy=proxy_addr, quality=quality_code)
        return {
            "anchor_name": "主播",
            "is_live": True,
            "record_url": "https://cdn.example/live.m3u8",
        }

    resolver = DouyinLiveRecorderResolver(
        youtube_resolver=SimpleNamespace(resolve=resolve_youtube),
    )
    result = asyncio.run(
        resolver.resolve("https://www.youtube.com/watch?v=demo", quality="高清")
    )

    assert result.platform is Platform.YOUTUBE
    assert result.stream_urls == ("https://cdn.example/live.m3u8",)
    assert captured == {
        "url": "https://www.youtube.com/watch?v=demo",
        "proxy": None,
        "quality": "HD",
    }
