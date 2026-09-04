from __future__ import annotations

import re
import shlex
from pathlib import Path

import pytest
import yaml

ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"
RELEASE_WORKFLOW = ROOT / ".github" / "workflows" / "release.yml"

EXPECTED_ACTION_REFS = {
    "actions/checkout": "3d3c42e5aac5ba805825da76410c181273ba90b1",
    "actions/setup-python": "5fda3b95a4ea91299a34e894583c3862153e4b97",
    "astral-sh/setup-uv": "20cfd1bf945f4377ade1205e4dbc17946fc9a30d",
    "actions/upload-artifact": "b7c566a772e6b6bfb58ed0dc250532a479d7789f",
    "actions/download-artifact": "70fc10c6e5e1ce46ad2ea6f2b72d43f7d47b13c3",
    "actions/attest": "1e69f48acb82d1966a394da916b4c1698aa569d6",
}


def _windows_ci_job(source: str) -> str:
    lines = source.splitlines()
    start = next(
        index
        for index, line in enumerate(lines)
        if line == "  test-build-self-check:"
    )
    end = next(
        (
            index
            for index in range(start + 1, len(lines))
            if lines[index].startswith("  ")
            and not lines[index].startswith("    ")
            and lines[index].strip()
        ),
        len(lines),
    )
    return "\n".join(lines[start:end])


def _windows_ci_steps(source: str) -> dict[str, dict[str, object]]:
    workflow = yaml.safe_load(source)
    if not isinstance(workflow, dict):
        raise TypeError("CI workflow must be a YAML mapping")

    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        raise TypeError("CI workflow must define a jobs mapping")

    job = jobs.get("test-build-self-check")
    if not isinstance(job, dict):
        raise TypeError("CI workflow must define the Windows CI job")

    raw_steps = job.get("steps")
    if not isinstance(raw_steps, list):
        raise TypeError("Windows CI job must define a steps list")

    steps: dict[str, dict[str, object]] = {}
    for position, raw_step in enumerate(raw_steps, start=1):
        if not isinstance(raw_step, dict):
            raise TypeError(f"CI step {position} must be a mapping")

        name = raw_step.get("name", f"<unnamed step {position}>")
        if not isinstance(name, str):
            raise TypeError(f"CI step {position} name must be a string")
        if name in steps:
            raise AssertionError(f"Duplicate CI step name: {name}")
        steps[name] = dict(raw_step)
    return steps


def _run_text(step: dict[str, object]) -> str:
    value = step.get("run", "")
    if not isinstance(value, str):
        raise TypeError("CI run field must be a string")
    return value


def _workflow_triggers(source: str) -> dict[str, object]:
    workflow = yaml.safe_load(source)
    if not isinstance(workflow, dict):
        raise TypeError("Workflow must be a YAML mapping")

    triggers = workflow.get("on")
    if triggers is None:
        triggers = workflow.get(True)
    if not isinstance(triggers, dict):
        raise TypeError("Workflow triggers must be a YAML mapping")
    return triggers


def _external_action_refs(source: str) -> dict[str, str]:
    refs: dict[str, str] = {}
    for line in source.splitlines():
        match = re.match(r"\s*uses:\s*([^\s#]+)(?:\s+#\s*(v[^\s]+))?\s*$", line)
        if not match:
            continue
        reference = match.group(1)
        if reference.startswith("./"):
            continue
        action, sha = reference.rsplit("@", maxsplit=1)
        assert re.fullmatch(r"[0-9a-f]{40}", sha), (
            f"Action must use a full commit SHA: {reference}"
        )
        assert match.group(2), f"Pinned action needs a version comment: {reference}"
        refs[action] = sha
    return refs


def _assert_all_uv_runs_are_locked(steps: dict[str, dict[str, object]]) -> None:
    for step_name, step in steps.items():
        script = _run_text(step)
        for match in re.finditer(r"\buv\s+run\b", script):
            lexer = shlex.shlex(
                script[match.start() :],
                posix=True,
                punctuation_chars=";&|",
            )
            lexer.whitespace_split = True
            tokens = iter(lexer)
            command = [next(tokens, None), next(tokens, None)]
            assert command == ["uv", "run"], (
                f"Could not parse uv run invocation in CI step: {step_name}"
            )
            options: list[str] = []
            for token in tokens:
                if token in {";", "|", "&", "&&", "||"}:
                    break
                if not token.startswith("-"):
                    break
                options.append(token)
            assert "--locked" in options, (
                f"Unlocked uv run invocation in CI step: {step_name}"
            )


@pytest.mark.parametrize(
    ("header", "content_indent"),
    [
        ("|-", 10),
        ("|+", 10),
        (">-", 10),
        (">+", 10),
        ("|1", 9),
        ("|+2", 10),
        (">2-", 10),
        ("| # comment", 10),
    ],
)
def test_windows_ci_parses_yaml_block_scalar_variants(
    header: str, content_indent: int
) -> None:
    source = (
        "jobs:\n"
        "  test-build-self-check:\n"
        "    steps:\n"
        "      - name: script\n"
        f"        run: {header}\n"
        f"{' ' * content_indent}uv run --locked python -V\n"
    )

    steps = _windows_ci_steps(source)

    assert _run_text(steps["script"]).strip() == "uv run --locked python -V"
    _assert_all_uv_runs_are_locked(steps)


def test_windows_ci_parses_folded_multiline_run() -> None:
    source = (
        "jobs:\n"
        "  test-build-self-check:\n"
        "    steps:\n"
        "      - name: script\n"
        "        run: >-\n"
        "          uv run --locked\n"
        "          python -V\n"
    )

    steps = _windows_ci_steps(source)

    assert _run_text(steps["script"]).strip() == "uv run --locked python -V"
    _assert_all_uv_runs_are_locked(steps)


def test_windows_ci_rejects_duplicate_step_names() -> None:
    source = (
        "jobs:\n"
        "  test-build-self-check:\n"
        "    steps:\n"
        "      - name: duplicate\n"
        "        run: first\n"
        "      - name: \"duplicate\"\n"
        "        run: second\n"
    )

    with pytest.raises(AssertionError, match="Duplicate CI step name"):
        _windows_ci_steps(source)


def test_windows_ci_checks_unnamed_steps() -> None:
    source = (
        "jobs:\n"
        "  test-build-self-check:\n"
        "    steps:\n"
        "      - run: uv run python -V\n"
    )

    steps = _windows_ci_steps(source)

    with pytest.raises(AssertionError, match="Unlocked uv run invocation"):
        _assert_all_uv_runs_are_locked(steps)


def test_windows_ci_does_not_treat_post_command_text_as_a_lock() -> None:
    source = (
        "jobs:\n"
        "  test-build-self-check:\n"
        "    steps:\n"
        "      - name: script\n"
        "        run: uv run python -c \"'--locked'\"\n"
    )

    steps = _windows_ci_steps(source)

    with pytest.raises(AssertionError, match="Unlocked uv run invocation"):
        _assert_all_uv_runs_are_locked(steps)


def test_windows_ci_checks_each_same_line_uv_invocation() -> None:
    source = (
        "jobs:\n"
        "  test-build-self-check:\n"
        "    steps:\n"
        "      - name: script\n"
        "        run: uv run --locked python -V; uv run python -V\n"
    )

    steps = _windows_ci_steps(source)

    with pytest.raises(AssertionError, match="Unlocked uv run invocation"):
        _assert_all_uv_runs_are_locked(steps)


def test_windows_ci_installs_and_runs_from_locked_uv_environment() -> None:
    source = CI_WORKFLOW.read_text(encoding="utf-8")
    job = _windows_ci_job(source)
    steps = _windows_ci_steps(source)

    assert steps["Install uv"]["uses"] == (
        "astral-sh/setup-uv@20cfd1bf945f4377ade1205e4dbc17946fc9a30d"
    )
    setup_with = steps["Install uv"].get("with")
    assert isinstance(setup_with, dict)
    assert setup_with["enable-cache"] is True
    assert _run_text(steps["Check uv lockfile"]).strip() == "uv lock --check"
    assert _run_text(steps["Install project and development dependencies"]).strip() == (
        "uv sync --locked --extra dev"
    )
    assert "uv run --locked python tools/project_version.py" in _run_text(
        steps["Read project version"]
    )
    assert (
        'uv run --locked python -c "import reco_box; print(reco_box.__version__)"'
        in _run_text(steps["Read project version"])
    )
    assert _run_text(steps["Check first-party source"]).strip() == (
        "uv run --locked ruff check src tests tools"
    )
    assert _run_text(steps["Run tests"]).strip() == (
        "uv run --locked pytest tests -q -p no:cacheprovider"
    )
    assert "Get-FileHash" in _run_text(steps["Prepare pinned previous release installer"])
    assert "PREVIOUS_INSTALLER_PATH" in _run_text(
        steps["Prepare pinned previous release installer"]
    )
    assert _run_text(steps["Run installer install, upgrade, and uninstall smoke"]).strip() == (
        "pwsh -NoProfile -File tools/test_installer.ps1 "
        "-PreviousInstallerPath $env:PREVIOUS_INSTALLER_PATH"
    )
    _assert_all_uv_runs_are_locked(steps)

    order = [
        "Install uv",
        "Check uv lockfile",
        "Install project and development dependencies",
        "Read project version",
        "Prepare verified FFmpeg runtime",
        "Prepare verified Node.js runtime",
        "Prepare pinned previous release installer",
        "Check first-party source",
        "Run tests",
        "Build Windows application",
        "Run packaged self-test",
        "Install Inno Setup",
        "Prepare pinned Inno Setup language files",
        "Build ten-language installer and checksum",
        "Run installer install, upgrade, and uninstall smoke",
    ]
    positions = [list(steps).index(name) for name in order]
    assert positions == sorted(positions)

    assert "python -m venv .venv" not in job
    assert "pip install" not in job
    assert "cache: pip" not in job


def test_all_workflow_actions_are_pinned_to_reviewed_commit_shas() -> None:
    observed: dict[str, str] = {}
    for workflow_path in (CI_WORKFLOW, RELEASE_WORKFLOW):
        observed.update(_external_action_refs(workflow_path.read_text(encoding="utf-8")))

    assert observed == EXPECTED_ACTION_REFS


def test_ci_is_read_only_and_only_uploads_when_called_for_a_release_candidate() -> None:
    source = CI_WORKFLOW.read_text(encoding="utf-8")
    triggers = _workflow_triggers(source)
    steps = _windows_ci_steps(source)

    assert set(triggers) == {"push", "pull_request", "workflow_call"}
    assert triggers["push"] == {"branches": ["main"]}
    assert "contents: read" in source
    assert "contents: write" not in source
    assert "PREVIOUS_INSTALLER_SHA256" in source
    assert "RecoBox-Setup-0.2.0.exe" in source
    assert "Run installer install, upgrade, and uninstall smoke" in source
    assert steps["Upload installer test artifact"]["if"] == "${{ inputs.upload_artifact }}"


def test_release_workflow_builds_attests_and_publishes_only_tag_or_manual() -> None:
    source = RELEASE_WORKFLOW.read_text(encoding="utf-8")
    workflow = yaml.safe_load(source)
    if not isinstance(workflow, dict):
        raise TypeError("Release workflow must be a YAML mapping")
    triggers = _workflow_triggers(source)
    jobs = workflow.get("jobs")
    if not isinstance(jobs, dict):
        raise TypeError("Release workflow must define jobs")

    assert set(triggers) == {"push", "workflow_dispatch"}
    assert triggers["push"] == {"tags": ["v*"]}
    assert set(triggers["workflow_dispatch"]["inputs"]) == {"release_tag"}
    assert "publish" in triggers["workflow_dispatch"]["inputs"]["release_tag"]["description"]

    build = jobs["build-release"]
    assert build["uses"] == "./.github/workflows/ci.yml"
    assert build["with"] == {
        "upload_artifact": True,
        "checkout_ref": (
            "${{ github.event_name == 'workflow_dispatch' && "
            "format('refs/tags/{0}', inputs.release_tag) || github.ref }}"
        ),
    }
    assert build["permissions"] == {"contents": "read"}

    attest = jobs["attest-release"]
    assert attest["needs"] == "build-release"
    assert attest["runs-on"] == "ubuntu-latest"
    assert attest["permissions"] == {
        "contents": "read",
        "id-token": "write",
        "attestations": "write",
    }
    attest_steps = {step["name"]: step for step in attest["steps"]}
    assert attest_steps["Download release asset"]["uses"] == (
        "actions/download-artifact@70fc10c6e5e1ce46ad2ea6f2b72d43f7d47b13c3"
    )
    assert "sha256sum" in attest_steps["Verify release asset checksum"]["run"]
    assert attest_steps["Generate binary provenance attestation"]["uses"] == (
        "actions/attest@1e69f48acb82d1966a394da916b4c1698aa569d6"
    )
    assert "RecoBox-Setup-*.exe" in attest_steps["Generate binary provenance attestation"][
        "with"
    ]["subject-path"]

    publish = jobs["publish-release"]
    assert publish["needs"] == "attest-release"
    assert publish["runs-on"] == "ubuntu-latest"
    assert publish["permissions"] == {"contents": "write"}
    publish_steps = {step["name"]: step for step in publish["steps"]}
    assert publish_steps["Download release asset"]["uses"] == (
        "actions/download-artifact@70fc10c6e5e1ce46ad2ea6f2b72d43f7d47b13c3"
    )
    publish_script = publish_steps["Create and publish release"]["run"]
    assert "gh release create" in publish_script
    assert "gh release edit" in publish_script
    assert "--verify-tag" in publish_script
    assert "--draft" in publish_script
    assert "Refusing to replace an existing GitHub Release" in publish_script

    assert set(jobs) == {"build-release", "attest-release", "publish-release"}
    assert source.count("contents: write") == 1
    assert "actions/attest@v4" not in source
    assert "pull_request" not in triggers


def test_installer_smoke_covers_upgrade_uninstall_and_user_data_preservation() -> None:
    source = (ROOT / "tools" / "test_installer.ps1").read_text(encoding="utf-8")

    assert "PreviousInstallerPath" in source
    assert "[Parameter(Mandatory = $true)]" in source
    assert "/VERYSILENT /SUPPRESSMSGBOXES /NORESTART" in source
    assert "RECO_BOX_DATA_DIR" in source
    assert "reco_box.db" in source
    assert "from reco_box.storage import Database" in source
    assert "upgrade_sentinel_config" in source
    assert "start_recording" in source
    assert "list_recordings" in source
    assert "status\"] == \"completed\"" in source
    assert "Get-ChildItem -LiteralPath $Target -Filter \"unins*.exe\"" in source
    assert "Start-Sleep -Milliseconds 250" in source
    assert "Assert-PreservedUserData" in source
    assert "self-check.json" in source
