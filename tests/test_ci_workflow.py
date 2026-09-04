from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CI_WORKFLOW = ROOT / ".github" / "workflows" / "ci.yml"


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


def _windows_ci_steps(source: str) -> dict[str, dict[str, str]]:
    job = _windows_ci_job(source)
    lines = job.splitlines()
    starts = [
        index
        for index, line in enumerate(lines)
        if line.startswith("      - name: ")
    ]
    steps: dict[str, dict[str, str]] = {}
    for position, start in enumerate(starts):
        end = starts[position + 1] if position + 1 < len(starts) else len(lines)
        name = lines[start].removeprefix("      - name: ")
        raw = "\n".join(lines[start:end])
        fields: dict[str, str] = {"raw": raw}
        for index in range(start + 1, end):
            match = re.match(r"^        (uses|run):(?:\s*(.*))?$", lines[index])
            if not match:
                continue
            field, value = match.groups()
            value = value or ""
            if value in {"|", ">"}:
                body: list[str] = []
                body_index = index + 1
                while body_index < end and (
                    not lines[body_index].strip()
                    or lines[body_index].startswith("          ")
                ):
                    body.append(lines[body_index][10:])
                    body_index += 1
                value = "\n".join(body)
            fields[field] = value
        if name in steps:
            raise AssertionError(f"Duplicate CI step name: {name}")
        steps[name] = fields
    return steps


def test_windows_ci_installs_and_runs_from_locked_uv_environment() -> None:
    source = CI_WORKFLOW.read_text(encoding="utf-8")
    job = _windows_ci_job(source)
    steps = _windows_ci_steps(source)

    assert steps["Install uv"]["uses"] == "astral-sh/setup-uv@v9"
    assert "enable-cache: true" in steps["Install uv"]["raw"]
    assert steps["Check uv lockfile"]["run"].strip() == "uv lock --check"
    assert steps["Install project and development dependencies"]["run"].strip() == (
        "uv sync --locked --extra dev"
    )
    assert "uv run --locked python tools/project_version.py" in steps[
        "Read project version"
    ]["run"]
    assert (
        'uv run --locked python -c "import reco_box; print(reco_box.__version__)"'
        in steps["Read project version"]["run"]
    )
    assert steps["Check first-party source"]["run"].strip() == (
        "uv run --locked ruff check src tests tools"
    )
    assert steps["Run tests"]["run"].strip() == (
        "uv run --locked pytest tests -q -p no:cacheprovider"
    )
    for step_name, step in steps.items():
        for invocation in re.findall(r"uv run[^\r\n]*", step.get("run", "")):
            assert "--locked" in invocation, (
                f"Unlocked uv run invocation in CI step: {step_name}"
            )

    order = [
        "Install uv",
        "Check uv lockfile",
        "Install project and development dependencies",
        "Read project version",
        "Check first-party source",
        "Run tests",
    ]
    positions = [list(steps).index(name) for name in order]
    assert positions == sorted(positions)

    assert "python -m venv .venv" not in job
    assert "pip install" not in job
    assert "cache: pip" not in job
