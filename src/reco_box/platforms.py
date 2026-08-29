from __future__ import annotations

from urllib.parse import urlparse

from .domain import Platform

HOST_RULES: tuple[tuple[tuple[str, ...], Platform], ...] = (
    (("live.douyin.com", "v.douyin.com"), Platform.DOUYIN),
    (("live.kuaishou.com", "v.kuaishou.com"), Platform.KUAISHOU),
    (("live.bilibili.com", "b23.tv"), Platform.BILIBILI),
    (("xiaohongshu.com", "xhslink.com"), Platform.XIAOHONGSHU),
    (("tiktok.com",), Platform.TIKTOK),
    (("youtube.com", "youtu.be"), Platform.YOUTUBE),
    (("taobao.com", "m.tb.cn", "tb.cn"), Platform.TAOBAO),
    (("jd.com", "3.cn"), Platform.JD),
    (("twitch.tv",), Platform.TWITCH),
    (("sooplive.com",), Platform.SOOP),
    (("chzzk.naver.com",), Platform.CHZZK),
    (("twitcasting.tv",), Platform.TWITCASTING),
    (("showroom-live.com",), Platform.SHOWROOM),
    (("bigo.tv",), Platform.BIGO),
    (("17.live",), Platform.LIVE17),
    (("liveme.com",), Platform.LIVEME),
    (("picarto.tv",), Platform.PICARTO),
    (("shp.ee",), Platform.SHOPEE),
    (
        (
            "live.shopee.sg",
            "live.shopee.com.my",
            "live.shopee.co.th",
            "live.shopee.ph",
            "live.shopee.vn",
            "live.shopee.co.id",
            "live.shopee.com.br",
            "live.shopee.com.mx",
            "live.shopee.tw",
        ),
        Platform.SHOPEE,
    ),
)


def detect_platform(url: str) -> Platform:
    candidate = url.strip()
    if not candidate:
        return Platform.UNKNOWN
    if "://" not in candidate:
        candidate = f"https://{candidate}"
    hostname = (urlparse(candidate).hostname or "").lower().rstrip(".")
    for domains, platform in HOST_RULES:
        if any(hostname == domain or hostname.endswith(f".{domain}") for domain in domains):
            return platform
    return Platform.UNKNOWN
