from __future__ import annotations

import argparse
import asyncio

from reco_box.resolver import DouyinLiveRecorderResolver


async def run(url: str) -> None:
    result = await DouyinLiveRecorderResolver().resolve(url)
    print(
        {
            "platform": result.platform.value,
            "is_live": result.is_live,
            "stream_count": len(result.stream_urls),
            "streamer_name": result.streamer_name,
            "title": result.title,
        }
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    asyncio.run(run(args.url))


if __name__ == "__main__":
    main()
