from datetime import datetime

from PySide6.QtCore import QCoreApplication, QProcess

from reco_box.domain import Platform, Room, RoomStatus
from reco_box.errors import Stalled, recording_failure_for_exit
from reco_box.recording import RecordingManager, should_mark_stalled
from reco_box.room_model import RoomListModel
from reco_box.storage import Database


class RunningProcess:
    def __init__(self) -> None:
        self.writes: list[bytes] = []
        self.properties: dict[str, object] = {}
        self.terminate_calls = 0
        self.kill_calls = 0

    def state(self):
        return QProcess.ProcessState.Running

    def setProperty(self, name: str, value: object) -> None:
        self.properties[name] = value

    def property(self, name: str) -> object:
        return self.properties.get(name)

    def write(self, data: bytes) -> int:
        self.writes.append(data)
        return len(data)

    def terminate(self) -> None:
        self.terminate_calls += 1

    def kill(self) -> None:
        self.kill_calls += 1


class FinishedProcess:
    def __init__(self, *, intentional_stop: bool = False) -> None:
        self.intentional_stop = intentional_stop

    def property(self, name: str) -> object:
        return self.intentional_stop if name == "intentionalStop" else None

    def deleteLater(self) -> None:
        return None


def test_stall_predicate_respects_process_state_grace_and_growth() -> None:
    assert should_mark_stalled(
        process_running=True,
        file_bytes=0,
        last_file_bytes=0,
        started_at=0,
        last_growth_at=0,
        now=29,
    ) is False
    assert should_mark_stalled(
        process_running=True,
        file_bytes=0,
        last_file_bytes=0,
        started_at=0,
        last_growth_at=0,
        now=119,
    ) is False
    assert should_mark_stalled(
        process_running=True,
        file_bytes=0,
        last_file_bytes=0,
        started_at=0,
        last_growth_at=0,
        now=120,
    ) is True
    assert should_mark_stalled(
        process_running=False,
        file_bytes=0,
        last_file_bytes=0,
        started_at=0,
        last_growth_at=0,
        now=120,
    ) is False
    assert should_mark_stalled(
        process_running=True,
        file_bytes=11,
        last_file_bytes=10,
        started_at=0,
        last_growth_at=0,
        now=120,
    ) is False


def test_progress_does_not_start_stall_clock_before_process_started(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/9",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(
        rooms,
        database,
        ffmpeg_path=tmp_path / "ffmpeg.exe",
        stall_timeout_seconds=120,
        stall_grace_seconds=30,
    )
    manager.progress_timer.stop()
    process = RunningProcess()
    session_dir = tmp_path / "session"
    session_dir.mkdir()
    now = 1_000.0
    monkeypatch.setattr("reco_box.recording.time.monotonic", lambda: now)
    manager.processes[room.id] = process
    manager.session_dirs[room.id] = session_dir
    manager.last_file_bytes[room.id] = 0
    manager.last_growth_at[room.id] = now - 120

    manager._update_progress()

    assert rooms.get_room(room.id).status == RoomStatus.OFFLINE
    assert room.id not in manager.started_monotonic
    assert room.id not in manager.recovery_reasons


def test_recording_manager_marks_stall_and_requests_graceful_quit(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/6",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(
        rooms,
        database,
        ffmpeg_path=tmp_path / "ffmpeg.exe",
        stall_timeout_seconds=120,
        stall_grace_seconds=30,
    )
    manager.progress_timer.stop()
    process = RunningProcess()
    session_dir = tmp_path / "session"
    session_dir.mkdir()
    now = 1_000.0
    monkeypatch.setattr("reco_box.recording.time.monotonic", lambda: now)
    manager.processes[room.id] = process
    manager.session_dirs[room.id] = session_dir
    manager.started_monotonic[room.id] = now - 120
    manager.last_file_bytes[room.id] = 0
    manager.last_growth_at[room.id] = now - 120
    manager.last_disk_checks[room.id] = now

    manager._update_progress()

    assert rooms.get_room(room.id).status == RoomStatus.STALLED
    assert manager.last_recording_failures[room.id].kind.value == "stalled"
    assert manager.recovery_reasons[room.id].kind.value == "stalled"
    assert process.writes == [b"q\n"]
    assert process.properties["recoveryReason"] == "stalled"

    manager._process_error(room.id, QProcess.ProcessError.Crashed, "process crashed")
    assert rooms.get_room(room.id).status == RoomStatus.STALLED
    assert manager.last_recording_failures[room.id].kind.value == "stalled"


def test_finalization_fallback_does_not_touch_a_newer_retry_process(tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/10", platform=Platform.BILIBILI)
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    old_process = RunningProcess()
    new_process = RunningProcess()
    manager.processes[room.id] = new_process

    manager._terminate_if_running(room.id, old_process)
    manager._kill_if_running(room.id, old_process)

    assert new_process.terminate_calls == 0
    assert new_process.kill_calls == 0

    manager._terminate_if_running(room.id, new_process)
    manager._kill_if_running(room.id, new_process)
    assert new_process.terminate_calls == 1
    assert new_process.kill_calls == 1


def test_stall_failure_overrides_clean_ffmpeg_exit() -> None:
    failure = recording_failure_for_exit(0, recovery_failure=Stalled("no growth"))
    assert failure is not None
    assert failure.kind.value == "stalled"


def test_finished_persists_stall_as_failed_even_with_clean_ffmpeg_exit(tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/6",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
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
    manager.processes[room.id] = FinishedProcess()
    manager.session_dirs[room.id] = session_dir
    manager.recording_ids[room.id] = recording_id
    manager.recovery_reasons[room.id] = Stalled("no growth")

    manager._finished(room.id, 0)

    with database.connection() as connection:
        record = connection.execute(
            "SELECT status, error_message FROM recordings WHERE id = ?",
            (recording_id,),
        ).fetchone()
    assert record is not None
    assert record["status"] == "failed"
    assert "no growth" in record["error_message"]
    assert rooms.get_room(room.id).status.value == "retrying"


def test_manual_stop_overrides_stall_reason_during_finalization(tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/7",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
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
    manager.processes[room.id] = FinishedProcess(intentional_stop=True)
    manager.session_dirs[room.id] = session_dir
    manager.recording_ids[room.id] = recording_id
    manager.manual_stops.add(room.id)
    manager.recovery_reasons[room.id] = Stalled("no growth")

    manager._finished(room.id, 0)

    with database.connection() as connection:
        record = connection.execute(
            "SELECT status FROM recordings WHERE id = ?",
            (recording_id,),
        ).fetchone()
    assert record is not None
    assert record["status"] == "completed"
    assert rooms.get_room(room.id).status.value == "offline"


def test_persisted_stall_is_reset_after_restart(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/8",
        platform=Platform.BILIBILI,
        enabled=True,
        status=RoomStatus.STALLED,
    )
    database.upsert_room(room)

    rooms = RoomListModel(database)

    assert rooms.get_room(room.id).status == RoomStatus.OFFLINE
    assert database.list_rooms()[0].status == RoomStatus.OFFLINE
