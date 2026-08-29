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
    }
    for url, expected in cases.items():
        assert detect_platform(url) is expected


def test_reject_host_suffix_impersonation() -> None:
    assert detect_platform("https://youtube.com.example.org/live") is Platform.UNKNOWN

