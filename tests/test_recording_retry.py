from collections import namedtuple
from datetime import datetime
from pathlib import Path
from subprocess import CompletedProcess

from PySide6.QtCore import QCoreApplication

from reco_box.domain import Platform, Room
from reco_box.recording import (
    ConversionResult,
    RecordingManager,
    convert_ts_segments,
    has_minimum_free_space,
    recording_retry_delay,
    recording_succeeded,
)
from reco_box.room_model import RoomListModel
from reco_box.storage import Database


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
    assert result.failure is not None
    assert result.failure.kind.value == "ffmpeg_failed"
    assert source.is_file()
    assert not (tmp_path / "1.mp4").exists()


def test_recording_manager_sanitizes_and_persists_compat_conversion_failure(tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/6",
        platform=Platform.BILIBILI,
        convert_to_mp4=True,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    session_dir = tmp_path / "session"
    session_dir.mkdir()
    recording_id = database.start_recording(
        room.id, datetime.now().astimezone(), session_dir
    )

    manager._conversion_finished(
        room.id,
        recording_id,
        session_dir,
        False,
        ConversionResult(
            False,
            12,
            "conversion failed /live.m3u8?sig=signature-secret Cookie: first=one; second=two",
        ),
    )

    with database.connection() as connection:
        record = connection.execute(
            "SELECT status, error_message FROM recordings WHERE id = ?",
            (recording_id,),
        ).fetchone()

    assert record is not None
    assert record["status"] == "failed"
    assert "signature-secret" not in record["error_message"]
    assert "first=one" not in record["error_message"]
    assert "second=two" not in record["error_message"]
    assert manager.last_recording_failures[room.id].kind.value == "ffmpeg_failed"
    assert "signature-secret" not in rooms.get_room(room.id).last_error
