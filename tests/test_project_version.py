from __future__ import annotations

import re
import subprocess
import sys
import tomllib
from pathlib import Path

import reco_box

ROOT = Path(__file__).resolve().parents[1]
VERSION_SCRIPT = ROOT / "tools" / "project_version.py"


def project_version_from_pyproject() -> str:
    with (ROOT / "pyproject.toml").open("rb") as handle:
        return tomllib.load(handle)["project"]["version"]


def test_project_version_cli_reads_pyproject_version() -> None:
    result = subprocess.run(
        [sys.executable, str(VERSION_SCRIPT)],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    )

    assert result.stdout.strip() == project_version_from_pyproject()
    assert result.stderr == ""


def test_installed_package_version_matches_project_version() -> None:
    assert reco_box.__version__ == project_version_from_pyproject()


def test_uv_lock_root_package_version_matches_project_version() -> None:
    with (ROOT / "uv.lock").open("rb") as handle:
        lock_data = tomllib.load(handle)

    root_packages = [
        package
        for package in lock_data["package"]
        if package.get("name") == "reco-box" and package.get("source") == {"editable": "."}
    ]

    assert len(root_packages) == 1
    assert root_packages[0]["version"] == project_version_from_pyproject()


def test_runtime_version_is_not_a_second_literal_source() -> None:
    source = (ROOT / "src" / "reco_box" / "__init__.py").read_text(encoding="utf-8")

    assert "importlib.metadata" in source
    assert not re.search(r"__version__\s*=\s*['\"]\d+\.\d+\.\d+", source)


def test_release_build_surfaces_do_not_embed_a_release_version() -> None:
    paths = (
        ROOT / "packaging" / "installer.iss",
        ROOT / "packaging" / "build.ps1",
        ROOT / "packaging" / "build_installer.ps1",
        ROOT / "tools" / "test_installer.ps1",
        ROOT / ".github" / "workflows" / "ci.yml",
    )
    release_literals = (
        r"MyAppVersion\s+['\"]\d+\.\d+\.\d+",
        r"RecoBox-Setup-\d+\.\d+\.\d+",
        r"install-test-\d+\.\d+\.\d+",
    )

    for path in paths:
        source = path.read_text(encoding="utf-8")
        assert all(not re.search(pattern, source) for pattern in release_literals), path


def test_release_build_surfaces_call_the_version_reader() -> None:
    installer_script = (ROOT / "packaging" / "build_installer.ps1").read_text(
        encoding="utf-8"
    )
    test_script = (ROOT / "tools" / "test_installer.ps1").read_text(encoding="utf-8")
    ci_workflow = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")

    assert "project_version.py" in installer_script
    assert "project_version.py" in test_script
    assert "project_version.py" in ci_workflow
    assert "check_version_consistency.ps1" in ci_workflow
    assert "check_version_consistency.ps1" in test_script
    assert "/DMyAppVersion=" in installer_script


def test_pyinstaller_build_declares_version_resource_and_package_metadata() -> None:
    spec = (ROOT / "packaging" / "reco_box.spec").read_text(encoding="utf-8")
    template = (ROOT / "packaging" / "version_info.txt.in").read_text(encoding="utf-8")

    assert "copy_metadata(\"reco-box\")" in spec
    assert "RECO_BOX_VERSION_FILE" in spec
    assert "version=version_file" in spec
    assert "@VERSION_PARTS@" in template
    assert template.count("@VERSION@") == 2
