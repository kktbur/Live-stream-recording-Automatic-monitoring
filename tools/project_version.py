"""Read and print the canonical project version from pyproject.toml."""

from __future__ import annotations

import tomllib
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
PYPROJECT_PATH = PROJECT_ROOT / "pyproject.toml"


def read_project_version(pyproject_path: Path = PYPROJECT_PATH) -> str:
    """Return the non-empty version declared in the project metadata."""
    with pyproject_path.open("rb") as handle:
        metadata = tomllib.load(handle)

    try:
        version = metadata["project"]["version"]
    except (KeyError, TypeError) as error:
        raise ValueError(f"Missing [project].version in {pyproject_path}") from error

    if (
        not isinstance(version, str)
        or not version
        or version != version.strip()
        or any(character.isspace() for character in version)
    ):
        raise ValueError(f"Invalid [project].version in {pyproject_path}")
    return version


def main() -> int:
    print(read_project_version())
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
