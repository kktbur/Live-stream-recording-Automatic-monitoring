"""Write a PNG without ancillary metadata chunks."""

from __future__ import annotations

import argparse
from pathlib import Path

from PIL import Image


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("source", type=Path)
    parser.add_argument("destination", type=Path)
    args = parser.parse_args()

    with Image.open(args.source) as image:
        clean = Image.new(image.mode, image.size)
        clean.putdata(list(image.getdata()))
        clean.save(args.destination, format="PNG", optimize=True)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
