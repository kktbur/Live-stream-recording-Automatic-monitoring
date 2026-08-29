from __future__ import annotations

import json
import shutil
import sys
from datetime import UTC, datetime
from pathlib import Path

import PySide6

from .localization import LANGUAGES
from .resolver import DouyinLiveRecorderResolver
from .resources import application_resource, is_frozen, package_resource, upstream_resource


def run_self_check(data_dir: Path) -> int:
    checks: dict[str, dict[str, object]] = {}

    def write_progress(stage: str) -> None:
        data_dir.mkdir(parents=True, exist_ok=True)
        (data_dir / "self-check-progress.json").write_text(
            json.dumps({"stage": stage, "checks": checks}, ensure_ascii=False, indent=2),
            encoding="utf-8",
        )

    def check_file(name: str, path: Path) -> None:
        checks[name] = {"ok": path.is_file(), "path": str(path)}

    check_file("qml", package_resource("ui", "Main.qml"))
    check_file("icon", application_resource("assets", "reco-box-icon-final.png"))
    check_file("ffmpeg", application_resource("runtime", "ffmpeg", "ffmpeg.exe"))
    check_file("ffprobe", application_resource("runtime", "ffmpeg", "ffprobe.exe"))
    media_backend = (
        application_resource(
            "PySide6", "plugins", "multimedia", "ffmpegmediaplugin.dll"
        )
        if getattr(sys, "frozen", False)
        else Path(PySide6.__file__).resolve().parent
        / "plugins"
        / "multimedia"
        / "ffmpegmediaplugin.dll"
    )
    check_file("qt_ffmpeg_media_backend", media_backend)
    check_file("resolver_source", upstream_resource() / "src" / "spider.py")

    for code, _ in LANGUAGES:
        if code != "zh-CN":
            check_file(
                f"translation_{code}",
                package_resource("translations", f"reco_box_{code}.qm"),
            )

    node = shutil.which("node")
    checks["node"] = {
        "ok": bool(node),
        "required": is_frozen(),
        "required_for": ["liveme"],
        "path": node or "",
    }
    write_progress("resolver_import_started")

    try:
        DouyinLiveRecorderResolver()._load_spider()
        checks["resolver_import"] = {"ok": True, "error": ""}
    except Exception as error:  # noqa: BLE001 - diagnostic must report any startup failure
        checks["resolver_import"] = {"ok": False, "error": str(error)[:500]}

    write_progress("resolver_import_finished")

    passed = all(
        bool(item["ok"])
        for item in checks.values()
        if item.get("required", True)
    )
    payload = {
        "checked_at": datetime.now(UTC).isoformat(),
        "passed": passed,
        "checks": checks,
    }
    data_dir.mkdir(parents=True, exist_ok=True)
    (data_dir / "self-check.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    (data_dir / "self-check-progress.json").unlink(missing_ok=True)
    return 0 if passed else 2
