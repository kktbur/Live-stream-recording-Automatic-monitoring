from datetime import UTC, datetime
from pathlib import Path

import pytest

from reco_box.domain import Room
from reco_box.ffmpeg import FFmpegPlanner, StreamInput


def test_unsegmented_is_default_and_named_one(tmp_path) -> None:
    room = Room(url="https://example.com/live", streamer_name="主播", save_root=str(tmp_path))
    plan = FFmpegPlanner(Path("ffmpeg.exe")).build(
        room,
        StreamInput("https://cdn.example.com/live.flv"),
        datetime(2026, 8, 14, 9, 8, 7, tzinfo=UTC),
    )
    assert plan.output_pattern.name == "1.ts"
    assert "-segment_time" not in plan.command


def test_segment_minutes_and_numbered_pattern(tmp_path) -> None:
    room = Room(
        url="https://example.com/live",
        streamer_name="主播",
        save_root=str(tmp_path),
        segment_enabled=True,
        segment_minutes=5,
    )
    plan = FFmpegPlanner(Path("ffmpeg.exe")).build(
        room,
        StreamInput("https://cdn.example.com/live.flv"),
        datetime(2026, 8, 14, 9, 8, 7, tzinfo=UTC),
    )
    assert plan.output_pattern.name == "%d.ts"
    assert plan.command[plan.command.index("-segment_time") + 1] == "300"
    assert plan.command[plan.command.index("-segment_start_number") + 1] == "1"


def test_unsegmented_custom_file_name_is_sanitized(tmp_path) -> None:
    room = Room(
        url="https://example.com/live",
        streamer_name="主播",
        save_root=str(tmp_path),
        file_name="新品:直播",
    )
    plan = FFmpegPlanner(Path("ffmpeg.exe")).build(
        room,
        StreamInput("https://cdn.example.com/live.flv"),
        datetime(2026, 8, 14, 9, 8, 7, tzinfo=UTC),
    )
    assert plan.output_pattern.name == "新品_直播.ts"


def test_build_for_session_reuses_a_caller_owned_directory(tmp_path) -> None:
    room = Room(
        url="https://example.com/live",
        streamer_name="主播",
        save_root=str(tmp_path),
    )
    session_dir = tmp_path / "stable-session"

    plan = FFmpegPlanner(Path("ffmpeg.exe")).build_for_session(
        room,
        StreamInput("https://cdn.example.com/live.flv"),
        session_dir,
    )

    assert plan.session_dir == session_dir
    assert plan.output_pattern == session_dir / "1.ts"
    assert not session_dir.exists()


def test_invalid_segment_minutes_are_rejected(tmp_path) -> None:
    room = Room(
        url="https://example.com/live",
        save_root=str(tmp_path),
        segment_enabled=True,
        segment_minutes=0,
    )
    with pytest.raises(ValueError, match="正整数"):
        FFmpegPlanner(Path("ffmpeg.exe")).build(
            room, StreamInput("https://cdn.example.com/live.flv"), datetime.now(UTC)
        )
    assert not (tmp_path / "待识别主播").exists()


def test_http_reconnect_options_are_enabled(tmp_path) -> None:
    room = Room(url="https://example.com/live", save_root=str(tmp_path))
    plan = FFmpegPlanner(Path("ffmpeg.exe")).build(
        room,
        StreamInput("https://cdn.example.com/live.flv"),
        datetime.now(UTC),
    )
    assert plan.command[plan.command.index("-reconnect") + 1] == "1"
    assert plan.command[plan.command.index("-reconnect_delay_max") + 1] == "10"


@pytest.mark.parametrize(
    ("output_format", "codec"),
    [("mp3", "libmp3lame"), ("m4a", "aac")],
)
def test_audio_formats_use_compatible_audio_codec(tmp_path, output_format, codec) -> None:
    room = Room(
        url="https://example.com/live",
        save_root=str(tmp_path),
        output_format=output_format,
        audio_only=True,
    )
    plan = FFmpegPlanner(Path("ffmpeg.exe")).build(
        room,
        StreamInput("https://cdn.example.com/live.flv"),
        datetime.now(UTC),
    )
    assert "-vn" in plan.command
    assert plan.command[plan.command.index("-c:a") + 1] == codec

