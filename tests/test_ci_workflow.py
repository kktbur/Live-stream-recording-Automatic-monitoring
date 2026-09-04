from __future__ import annotations

import re
import shlex
from pathlib import Path

import pytest
import yaml

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

    assert steps["Install uv"]["uses"] == "astral-sh/setup-uv@v10.0.1"
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
    _assert_all_uv_runs_are_locked(steps)

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
