from __future__ import annotations

import re
from datetime import datetime
from pathlib import Path

from .localization import tr

INVALID_WINDOWS_CHARS = re.compile(r'[<>:"/\\|?*\x00-\x1f]')
RESERVED_WINDOWS_NAMES = {
    "CON",
    "PRN",
    "AUX",
    "NUL",
    *(f"COM{number}" for number in range(1, 10)),
    *(f"LPT{number}" for number in range(1, 10)),
}


def sanitize_component(value: str, fallback: str = "未知主播") -> str:
    cleaned = INVALID_WINDOWS_CHARS.sub("_", value).strip().rstrip(". ")
    if not cleaned:
        cleaned = fallback
    if cleaned.upper() in RESERVED_WINDOWS_NAMES:
        cleaned = f"_{cleaned}"
    return cleaned[:120]


def create_session_directory(root: Path, streamer_name: str, started_at: datetime) -> Path:
    streamer = sanitize_component(streamer_name)
    date_dir = started_at.strftime("%Y-%m-%d")
    time_dir = started_at.strftime("%H-%M-%S")
    parent = Path(root) / streamer / date_dir
    candidate = parent / time_dir
    suffix = 2
    while candidate.exists():
        candidate = parent / f"{time_dir}_{suffix}"
        suffix += 1
    candidate.mkdir(parents=True, exist_ok=False)
    return candidate


def segment_output_pattern(session_dir: Path, extension: str) -> Path:
    normalized = extension.lower().lstrip(".")
    if not normalized or not normalized.isalnum():
        raise ValueError(tr("输出格式必须是简单扩展名"))
    return Path(session_dir) / f"%d.{normalized}"


def single_output_path(session_dir: Path, extension: str, file_name: str = "") -> Path:
    return numbered_single_output_path(session_dir, extension, file_name)


def numbered_single_output_path(
    session_dir: Path,
    extension: str,
    file_name: str = "",
    sequence_number: int = 1,
) -> Path:
    normalized = extension.lower().lstrip(".")
    if not normalized or not normalized.isalnum():
        raise ValueError(tr("输出格式必须是简单扩展名"))
    if sequence_number < 1:
        raise ValueError("sequence_number must be positive")
    if file_name.strip():
        base_name = sanitize_component(file_name, "1")
        if sequence_number > 1:
            base_name = f"{base_name}_{sequence_number}"
    else:
        base_name = str(sequence_number)
    return Path(session_dir) / f"{base_name}.{normalized}"


def next_session_output_number(
    session_dir: Path, extension: str, file_name: str = ""
) -> int:
    """Return the next monotonic output number for a session folder."""

    normalized = extension.lower().lstrip(".")
    if not normalized or not normalized.isalnum():
        raise ValueError(tr("输出格式必须是简单扩展名"))
    directory = Path(session_dir)
    paths = tuple(directory.iterdir()) if directory.exists() else ()
    if file_name.strip():
        base_name = sanitize_component(file_name, "1")
        sequence_number = 1
        while any(
            path.is_file()
            and path.stem == (
                base_name
                if sequence_number == 1
                else f"{base_name}_{sequence_number}"
            )
            for path in paths
        ):
            sequence_number += 1
        return sequence_number

    numbers = [
        int(path.stem)
        for path in paths
        if path.is_file() and path.stem.isdecimal()
    ]
    return max(numbers, default=0) + 1
