from reco_box.domain import Platform
from reco_box.platforms import detect_platform


def test_detect_supported_platforms() -> None:
    cases = {
        "https://live.douyin.com/123": Platform.DOUYIN,
        "https://live.kuaishou.com/u/demo": Platform.KUAISHOU,
        "https://live.bilibili.com/6": Platform.BILIBILI,
        "https://xhslink.com/a": Platform.XIAOHONGSHU,
        "https://www.tiktok.com/@demo/live": Platform.TIKTOK,
        "https://youtu.be/demo": Platform.YOUTUBE,
        "https://m.tb.cn/demo": Platform.TAOBAO,
        "https://3.cn/demo": Platform.JD,
        "https://www.twitch.tv/demo": Platform.TWITCH,
        "https://www.sooplive.com/demo": Platform.SOOP,
        "https://chzzk.naver.com/live/demo": Platform.CHZZK,
        "https://twitcasting.tv/demo": Platform.TWITCASTING,
        "https://www.showroom-live.com/room/profile?room_id=1": Platform.SHOWROOM,
        "https://www.bigo.tv/cn/demo": Platform.BIGO,
        "https://17.live/en/live/1": Platform.LIVE17,
        "https://www.liveme.com/en/v/1/index.html": Platform.LIVEME,
        "https://www.picarto.tv/demo": Platform.PICARTO,
        "https://sg.shp.ee/demo": Platform.SHOPEE,
        "https://live.shopee.sg/share?session=1": Platform.SHOPEE,
    }
    for url, expected in cases.items():
        assert detect_platform(url) is expected


def test_reject_host_suffix_impersonation() -> None:
    assert detect_platform("https://youtube.com.example.org/live") is Platform.UNKNOWN
    assert detect_platform("https://twitch.tv.example.org/live") is Platform.UNKNOWN
    assert detect_platform("https://live.shopee.example.org/live") is Platform.UNKNOWN
    assert detect_platform("https://play.sooplive.co.kr/demo") is Platform.UNKNOWN
