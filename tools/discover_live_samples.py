from __future__ import annotations

import argparse
import json
import re
import urllib.request


def fetch_text(url: str) -> str:
    request = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0"})
    with urllib.request.urlopen(request, timeout=20) as response:
        return response.read().decode("utf-8", "ignore")


def discover_bigo() -> list[str]:
    html = fetch_text("https://www.bigo.tv/")
    paths = re.findall(r'href=["\']?(/(?:id|en|cn|th|vn|jp)/[A-Za-z0-9_.-]+)', html)
    return [f"https://www.bigo.tv{path}" for path in dict.fromkeys(paths)]


def discover_showroom() -> list[str]:
    payload = json.loads(fetch_text("https://www.showroom-live.com/api/live/onlives"))
    rooms: list[str] = []
    for section in payload.get("onlives", []):
        for live in section.get("lives", []):
            key = live.get("room_url_key")
            if key:
                rooms.append(f"https://www.showroom-live.com/r/{key}")
    return list(dict.fromkeys(rooms))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("platform", choices=("bigo", "showroom"))
    parser.add_argument("--limit", type=int, default=20)
    args = parser.parse_args()
    discover = {"bigo": discover_bigo, "showroom": discover_showroom}[args.platform]
    print(*discover()[: max(1, args.limit)], sep="\n")


if __name__ == "__main__":
    main()
