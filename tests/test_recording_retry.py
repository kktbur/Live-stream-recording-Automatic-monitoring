from collections import namedtuple
from pathlib import Path
from subprocess import CompletedProcess

from reco_box.recording import (
    RecordingManager,
    convert_ts_segments,
    has_minimum_free_space,
    recording_retry_delay,
    recording_succeeded,
)


def test_recording_line_selects_requested_url_and_falls_back_to_last() -> None:
    urls = ("line-1", "line-2")
    assert RecordingManager._selected_stream_url("线路1", urls) == "line-1"
    assert RecordingManager._selected_stream_url("线路2", urls) == "line-2"
    assert RecordingManager._selected_stream_url("线路5", urls) == "line-2"


def test_recording_retry_uses_bounded_exponential_backoff() -> None:
    assert [recording_retry_delay(attempt) for attempt in range(1, 7)] == [
        5,
        10,
        20,
        40,
        80,
        120,
    ]


def test_disk_space_threshold(monkeypatch, tmp_path) -> None:
    usage = namedtuple("usage", "total used free")
    monkeypatch.setattr(
        "reco_box.recording.shutil.disk_usage",
        lambda _path: usage(10 * 1024**3, 7 * 1024**3, 3 * 1024**3),
    )

    assert has_minimum_free_space(tmp_path, 2) is True
    assert has_minimum_free_space(tmp_path, 5) is False


def test_manual_stop_is_success_even_when_qprocess_reports_crash_code() -> None:
    assert recording_succeeded(62097, True) is True
    assert recording_succeeded(62097, False) is False
    assert recording_succeeded(0, True, "磁盘空间不足") is False


def test_convert_numbered_ts_segments_to_mp4_then_remove_sources(
    monkeypatch, tmp_path
) -> None:
    for number in (1, 2):
        (tmp_path / f"{number}.ts").write_bytes(b"transport-stream")

    commands: list[list[str]] = []

    def fake_run(command, **_kwargs):
        commands.append(command)
        Path(command[-1]).write_bytes(b"mp4")
        return CompletedProcess(command, 0, "", "")

    monkeypatch.setattr("reco_box.recording.subprocess.run", fake_run)
    result = convert_ts_segments(Path("ffmpeg.exe"), tmp_path)

    assert result.success is True
    assert [path.name for path in sorted(tmp_path.glob("*.mp4"))] == ["1.mp4", "2.mp4"]
    assert list(tmp_path.glob("*.ts")) == []
    assert [Path(command[-1]).name for command in commands] == ["1.mp4", "2.mp4"]


def test_failed_conversion_keeps_original_ts(monkeypatch, tmp_path) -> None:
    source = tmp_path / "1.ts"
    source.write_bytes(b"transport-stream")

    monkeypatch.setattr(
        "reco_box.recording.subprocess.run",
        lambda command, **_kwargs: CompletedProcess(command, 1, "", "mux error"),
    )
    result = convert_ts_segments(Path("ffmpeg.exe"), tmp_path)

    assert result.success is False
    assert source.is_file()
    assert not (tmp_path / "1.mp4").exists()
