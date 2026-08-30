from __future__ import annotations

import argparse
import asyncio
import json
import re
import subprocess
import sys
from datetime import UTC, datetime
from pathlib import Path
from urllib.parse import urlsplit

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SOURCE_ROOT = PROJECT_ROOT / "src"
if str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from reco_box.resolver import DouyinLiveRecorderResolver
from reco_box.resources import application_resource, configure_bundled_runtime


def _run(command: list[str], timeout: int) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        check=False,
        capture_output=True,
        text=True,
        encoding="utf-8",
        errors="replace",
        timeout=timeout,
    )


def _safe_error_tail(value: str) -> str:
    redacted = re.sub(r"https?://\S+", "[stream-url-redacted]", value)
    return "\n".join(redacted.splitlines()[-8:])[-2000:]


async def validate(url: str, seconds: int, proxy: str = "") -> dict[str, object]:
    configure_bundled_runtime()
    resolved = await DouyinLiveRecorderResolver().resolve(url, proxy=proxy)
    report: dict[str, object] = {
        "tested_at": datetime.now(UTC).isoformat(timespec="seconds"),
        "public_url": url,
        "platform": resolved.platform.value,
        "anonymous_resolve": True,
        "is_live": resolved.is_live,
        "stream_count": len(resolved.stream_urls),
        "stream_origins": [
            f"{parts.scheme}://{parts.netloc}"
            for parts in (urlsplit(item) for item in resolved.stream_urls)
        ],
        "streamer_name": resolved.streamer_name,
        "title": resolved.title,
        "ts_recorded": False,
        "mp4_remuxed": False,
    }
    if not resolved.is_live or not resolved.stream_urls:
        return report

    ffmpeg = application_resource("runtime", "ffmpeg", "ffmpeg.exe")
    ffprobe = application_resource("runtime", "ffmpeg", "ffprobe.exe")
    if not ffmpeg.is_file() or not ffprobe.is_file():
        raise FileNotFoundError("Pinned FFmpeg runtime is missing")

    output_dir = PROJECT_ROOT / "artifacts" / "live-validation" / resolved.platform.value
    output_dir.mkdir(parents=True, exist_ok=True)
    ts_path = output_dir / "sample.ts"
    mp4_path = output_dir / "sample.mp4"
    report_path = output_dir / "report.json"

    command = [
        str(ffmpeg),
        "-hide_banner",
        "-loglevel",
        "warning",
        "-y",
        "-reconnect",
        "1",
        "-reconnect_streamed",
        "1",
        "-reconnect_delay_max",
        "10",
        "-rw_timeout",
        "15000000",
    ]
    if resolved.headers:
        command.extend(["-headers", resolved.headers])
    if proxy:
        command.extend(["-http_proxy", proxy])
    command.extend(
        [
            "-i",
            resolved.stream_urls[0],
            "-t",
            str(seconds),
            "-map",
            "0:v:0?",
            "-map",
            "0:a:0?",
            "-c",
            "copy",
            str(ts_path),
        ]
    )
    try:
        recorded = _run(command, timeout=seconds + 45)
    except subprocess.TimeoutExpired as error:
        report["record_exit_code"] = "timeout"
        report["record_error"] = "FFmpeg timed out while stopping the public stream"
        report["record_error_detail"] = _safe_error_tail(str(error.stderr or ""))
        report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")
        return report
    report["record_exit_code"] = recorded.returncode
    report["ts_recorded"] = recorded.returncode == 0 and ts_path.stat().st_size > 0
    report["ts_bytes"] = ts_path.stat().st_size if ts_path.exists() else 0
    if not report["ts_recorded"]:
        report["record_error"] = "FFmpeg could not record the public stream"
        report["record_error_detail"] = _safe_error_tail(recorded.stderr)
        report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")
        return report

    remuxed = _run(
        [
            str(ffmpeg),
            "-hide_banner",
            "-loglevel",
            "warning",
            "-y",
            "-i",
            str(ts_path),
            "-map",
            "0:v:0?",
            "-map",
            "0:a:0?",
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(mp4_path),
        ],
        timeout=45,
    )
    report["remux_exit_code"] = remuxed.returncode
    report["mp4_remuxed"] = remuxed.returncode == 0 and mp4_path.stat().st_size > 0
    report["mp4_bytes"] = mp4_path.stat().st_size if mp4_path.exists() else 0
    if report["mp4_remuxed"]:
        probed = _run(
            [
                str(ffprobe),
                "-v",
                "error",
                "-show_entries",
                "format=duration",
                "-of",
                "default=noprint_wrappers=1:nokey=1",
                str(mp4_path),
            ],
            timeout=30,
        )
        report["duration_seconds"] = probed.stdout.strip()
    report_path.write_text(json.dumps(report, ensure_ascii=True, indent=2), encoding="utf-8")
    return report


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("url")
    parser.add_argument("--seconds", type=int, default=8)
    parser.add_argument("--proxy", default="")
    args = parser.parse_args()
    report = asyncio.run(validate(args.url, max(3, min(args.seconds, 30)), args.proxy))
    print(json.dumps(report, ensure_ascii=True))
    if not report["mp4_remuxed"]:
        raise SystemExit(1)


if __name__ == "__main__":
    main()
