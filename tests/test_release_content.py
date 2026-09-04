from __future__ import annotations

import ast
import re
import tomllib
import xml.etree.ElementTree as ET
from pathlib import Path

from reco_box.localization import LANGUAGES

ROOT = Path(__file__).resolve().parents[1]
with (ROOT / "pyproject.toml").open("rb") as handle:
    PROJECT_VERSION = tomllib.load(handle)["project"]["version"]
NAVIGATION = (
    "[简体中文](README.md) | [繁體中文](README.zh-TW.md) | "
    "[English](README.en.md) | [Español](README.es.md) | "
    "[Français](README.fr.md) | [Deutsch](README.de.md) | "
    "[Português](README.pt.md) | [Русский](README.ru.md) | "
    "[日本語](README.ja.md) | [한국어](README.ko.md)"
)
READMES = (
    "README.md",
    "README.zh-TW.md",
    "README.en.md",
    "README.es.md",
    "README.fr.md",
    "README.de.md",
    "README.pt.md",
    "README.ru.md",
    "README.ja.md",
    "README.ko.md",
)


def test_readmes_share_navigation_version_and_scope() -> None:
    for name in READMES:
        text = (ROOT / name).read_text(encoding="utf-8")
        assert NAVIGATION in text
        assert PROJECT_VERSION in text
        assert "Twitch" in text
        assert "Shopee Live" in text
        assert "Roadmap" in text
        assert "CONTRIBUTING.md" in text
        assert "SECURITY.md" in text


def test_translation_catalogs_are_complete_and_aligned() -> None:
    qml = (ROOT / "src" / "reco_box" / "ui" / "Main.qml").read_text(encoding="utf-8")
    source_texts = {
        value.replace(r"\n", "\n").replace(r'\"', '"').replace(r"\\", "\\")
        for value in re.findall(r'qsTr\("((?:[^"\\]|\\.)*)"\)', qml)
    }
    for path in (ROOT / "src" / "reco_box").glob("*.py"):
        tree = ast.parse(path.read_text(encoding="utf-8"))
        source_texts.update(
            node.args[0].value
            for node in ast.walk(tree)
            if isinstance(node, ast.Call)
            and isinstance(node.func, ast.Name)
            and node.func.id == "tr"
            and node.args
            and isinstance(node.args[0], ast.Constant)
            and isinstance(node.args[0].value, str)
        )
    expected_sources: set[str] | None = None
    for code, _name in LANGUAGES:
        if code == "zh-CN":
            continue
        ts_path = ROOT / "src" / "reco_box" / "translations" / f"reco_box_{code}.ts"
        qm_path = ts_path.with_suffix(".qm")
        assert ts_path.is_file()
        assert qm_path.is_file()
        tree = ET.parse(ts_path)
        messages = tree.findall(".//message")
        sources = {message.findtext("source", "") for message in messages}
        assert sources
        assert all(
            (translation := message.find("translation")) is not None
            and translation.get("type") != "unfinished"
            and bool("".join(translation.itertext()).strip())
            for message in messages
        )
        expected_sources = sources if expected_sources is None else expected_sources
        assert sources == expected_sources
    assert expected_sources == source_texts
