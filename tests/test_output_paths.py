from datetime import UTC, datetime

from reco_box.output_paths import create_session_directory, sanitize_component


def test_output_tree_and_collision(tmp_path) -> None:
    started = datetime(2026, 8, 14, 21, 5, 12, tzinfo=UTC)
    first = create_session_directory(tmp_path, "主播:A", started)
    second = create_session_directory(tmp_path, "主播:A", started)

    assert first.relative_to(tmp_path).as_posix() == "主播_A/2026-08-14/21-05-12"
    assert second.relative_to(tmp_path).as_posix() == "主播_A/2026-08-14/21-05-12_2"


def test_reserved_windows_name_is_safe() -> None:
    assert sanitize_component("CON") == "_CON"
