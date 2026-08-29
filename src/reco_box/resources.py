from __future__ import annotations

import os
import sys
from pathlib import Path


def is_frozen() -> bool:
    return bool(getattr(sys, "frozen", False)) and hasattr(sys, "_MEIPASS")


def application_resource(*parts: str) -> Path:
    if is_frozen():
        base = Path(sys._MEIPASS)  # type: ignore[attr-defined]
    else:
        base = Path(__file__).resolve().parents[2]
    return base.joinpath(*parts)


def package_resource(*parts: str) -> Path:
    if is_frozen():
        return application_resource("reco_box", *parts)
    return Path(__file__).resolve().parent.joinpath(*parts)


def upstream_resource() -> Path:
    override = os.environ.get("RECO_BOX_UPSTREAM_DIR", "").strip()
    if override:
        return Path(override)
    if is_frozen():
        return application_resource("vendor", "DouyinLiveRecorder")
    return application_resource("vendor", "DouyinLiveRecorder")


def configure_bundled_runtime() -> None:
    runtime_node = application_resource("runtime", "node")
    if not (runtime_node / "node.exe").is_file():
        return
    current = os.environ.get("PATH", "")
    entries = current.split(os.pathsep) if current else []
    node_text = str(runtime_node)
    if node_text.casefold() not in {entry.casefold() for entry in entries}:
        os.environ["PATH"] = os.pathsep.join([node_text, *entries])
