from __future__ import annotations

import json
import os
import shutil
import subprocess
from dataclasses import dataclass
from pathlib import Path
from typing import Any

from .localization import tr
from .resources import application_resource

MEDIA_EXTENSIONS = frozenset({".ts", ".mp4", ".mkv", ".flv", ".mp3", ".m4a"})


@dataclass(slots=True, frozen=True)
class ProbeResult:
    valid: bool
    duration_seconds: float
    codec_summary: str
    error: str = ""


def find_ffprobe() -> Path | None:
    override = os.environ.get("RECO_BOX_FFPROBE", "").strip()
    discovered = shutil.which("ffprobe")
    candidates = [
        Path(override) if override else None,
        application_resource("runtime", "ffmpeg", "ffprobe.exe"),
        Path(discovered) if discovered else None,
    ]
    return next((path for path in candidates if path and path.is_file()), None)


def first_media_file(session_dir: Path) -> Path | None:
    files = media_files(session_dir)
    return files[0] if files else None


def media_files(session_dir: Path) -> list[Path]:
    if not session_dir.is_dir():
        return []
    return sorted(
        (
            path
            for path in session_dir.iterdir()
            if path.is_file() and path.suffix.lower() in MEDIA_EXTENSIONS
        ),
        key=_media_sort_key,
    )


def _media_sort_key(path: Path) -> tuple[int, int | str]:
    return (0, int(path.stem)) if path.stem.isdigit() else (1, path.name.casefold())


def probe_media_file(ffprobe_path: Path, media_path: Path) -> ProbeResult:
    command = [
        str(ffprobe_path),
        "-v",
        "error",
        "-show_entries",
        "format=duration:stream=codec_type,codec_name",
        "-of",
        "json",
        str(media_path),
    ]
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    try:
        completed = subprocess.run(
            command,
            capture_output=True,
            text=True,
            encoding="utf-8",
            errors="replace",
            timeout=20,
            check=False,
            creationflags=creation_flags,
        )
    except (OSError, subprocess.TimeoutExpired) as error:
        return ProbeResult(False, 0, "", str(error)[:300])
    if completed.returncode != 0:
        message = completed.stderr.replace("\r", " ").replace("\n", " ").strip()
        return ProbeResult(False, 0, "", message[:300] or tr("ffprobe 验证失败"))
    try:
        payload = json.loads(completed.stdout)
    except json.JSONDecodeError:
        return ProbeResult(False, 0, "", tr("ffprobe 返回了无效 JSON"))
    return parse_probe_payload(payload)


def probe_media_files(ffprobe_path: Path, paths: list[Path]) -> ProbeResult:
    if not paths:
        return ProbeResult(False, 0, "", tr("录制目录中没有媒体文件"))
    duration = 0.0
    codecs: list[str] = []
    for path in paths:
        result = probe_media_file(ffprobe_path, path)
        if not result.valid:
            return ProbeResult(False, duration, ", ".join(codecs), f"{path.name}: {result.error}")
        duration += result.duration_seconds
        for codec in result.codec_summary.split(", "):
            if codec and codec not in codecs:
                codecs.append(codec)
    return ProbeResult(True, duration, ", ".join(codecs))


def parse_probe_payload(payload: dict[str, Any]) -> ProbeResult:
    streams = payload.get("streams")
    if not isinstance(streams, list) or not streams:
        return ProbeResult(False, 0, "", tr("文件中没有可识别的音视频流"))
    codecs = []
    for stream in streams:
        if not isinstance(stream, dict):
            continue
        codec_type = str(stream.get("codec_type", "unknown"))
        codec_name = str(stream.get("codec_name", "unknown"))
        codecs.append(f"{codec_type}:{codec_name}")
    try:
        duration = float(payload.get("format", {}).get("duration", 0) or 0)
    except (TypeError, ValueError):
        duration = 0
    return ProbeResult(bool(codecs), max(0, duration), ", ".join(codecs))
