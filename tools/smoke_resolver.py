from __future__ import annotations

import argparse
import asyncio
import json
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from reco_box.resolver import DouyinLiveRecorderResolver
from reco_box.resources import configure_bundled_runtime


async def run(url: str) -> None:
    configure_bundled_runtime()
    result = await DouyinLiveRecorderResolver().resolve(url)
    print(
        json.dumps(
            {
                "platform": result.platform.value,
                "is_live": result.is_live,
                "stream_count": len(result.stream_urls),
                "streamer_name": result.streamer_name,
                "title": result.title,
            },
            ensure_ascii=True,
        )
    )


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    args = parser.parse_args()
    asyncio.run(run(args.url))


if __name__ == "__main__":
    main()
