from datetime import datetime

from PySide6.QtCore import QCoreApplication

from reco_box.domain import Platform, RecordingSessionState, Room, RoomStatus
from reco_box.errors import AccessRestricted
from reco_box.monitor import MonitoringCoordinator, ResolvedStream
from reco_box.recording import ConversionResult, ConversionWorker, RecordingManager
from reco_box.room_model import RoomListModel
from reco_box.storage import Database


class FakeSignal:
    def connect(self, _callback) -> None:
        return None


class FakeProcess:
    class ProcessChannelMode:
        MergedChannels = object()

    def __init__(self, _parent=None) -> None:
        self.started = FakeSignal()
        self.errorOccurred = FakeSignal()
        self.finished = FakeSignal()
        self.arguments: list[str] = []
        self.properties: dict[str, object] = {}

    def setProcessChannelMode(self, _mode) -> None:
        return None

    def setProgram(self, program: str) -> None:
        self.program = program

    def setArguments(self, arguments: list[str]) -> None:
        self.arguments = arguments

    def setProperty(self, name: str, value: object) -> None:
        self.properties[name] = value

    def property(self, name: str) -> object:
        return self.properties.get(name)

    def start(self) -> None:
        return None

    def deleteLater(self) -> None:
        return None


def test_failed_attempt_reuses_session_directory_and_next_file_number(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

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
    resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/first",),
    )

    manager.start_for_room(room.id, resolved)

    first_process = manager.processes[room.id]
    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/duplicate",),
        ),
    )
    assert manager.processes[room.id] is first_process
    first_session = manager.recording_sessions[room.id]
    first_dir = first_session.session_dir
    (first_dir / "1.ts").write_bytes(b"first attempt")
    manager._finished(room.id, 1)

    assert room.id not in manager.processes
    assert manager.recording_sessions[room.id].session_id == first_session.session_id
    assert manager.recording_sessions[room.id].state.value == "active"

    second_resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/second",),
    )
    manager.start_for_room(room.id, second_resolved)

    second_process = manager.processes[room.id]
    second_session = manager.recording_sessions[room.id]
    assert second_process is not first_process
    assert second_session.session_id == first_session.session_id
    assert second_session.session_dir == first_dir
    assert second_session.attempt == 1
    assert "https://cdn.example.test/second" in second_process.arguments
    assert second_process.arguments[-1] == str(first_dir / "2.ts")

    persisted = database.get_recording_session(first_session.session_id)
    assert persisted is not None
    assert persisted.session_dir == first_dir
    assert persisted.attempt == 1
    assert persisted.last_stream_url == ""

    with database.connection() as connection:
        attempts = connection.execute(
            """
            SELECT group_id, recovery_index, session_dir
            FROM recordings
            WHERE room_id = ?
            ORDER BY recovery_index
            """,
            (room.id,),
        ).fetchall()
    assert [(row["group_id"], row["recovery_index"], row["session_dir"]) for row in attempts] == [
        (first_session.session_id, 0, str(first_dir)),
        (first_session.session_id, 1, str(first_dir)),
    ]

    manager._finished(room.id, 0)

    completed = database.get_recording_session(first_session.session_id)
    assert completed is not None
    assert completed.state is RecordingSessionState.COMPLETED
    assert room.id not in manager.recording_sessions


def test_manual_stop_abandons_the_session_and_cannot_be_retried(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

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

    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/manual-stop",),
        ),
    )
    session_id = manager.recording_sessions[room.id].session_id
    manager.manual_stops.add(room.id)

    manager._finished(room.id, 0)

    abandoned = database.get_recording_session(session_id)
    assert abandoned is not None
    assert abandoned.state is RecordingSessionState.ABANDONED


def test_segmented_recovery_uses_numeric_segments_even_with_custom_file_name(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/9",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        segment_enabled=True,
        segment_minutes=5,
        file_name="custom-name",
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/segmented",),
    )

    manager.start_for_room(room.id, resolved)
    session_dir = manager.recording_sessions[room.id].session_dir
    (session_dir / "1.ts").write_bytes(b"first segment")
    manager._finished(room.id, 1)
    manager.start_for_room(room.id, resolved)

    process = manager.processes[room.id]
    assert process.arguments[process.arguments.index("-segment_start_number") + 1] == "2"
    assert process.arguments[-1] == str(session_dir / "%d.ts")


def test_exhausted_retries_mark_the_session_failed(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/10",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/retry",),
    )

    session_id = ""
    for attempt in range(6):
        manager.start_for_room(room.id, resolved)
        session_id = manager.recording_sessions[room.id].session_id
        manager._finished(room.id, 1)
        if attempt < 5:
            assert room.id in manager.recording_sessions

    failed = database.get_recording_session(session_id)
    assert failed is not None
    assert failed.state is RecordingSessionState.FAILED
    assert room.id not in manager.recording_sessions


def test_protective_stop_marks_the_session_failed(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/11",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()

    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/disk",),
        ),
    )
    session_id = manager.recording_sessions[room.id].session_id
    manager.protective_stop_errors[room.id] = "磁盘空间不足"

    manager._finished(room.id, 0)

    failed = database.get_recording_session(session_id)
    assert failed is not None
    assert failed.state is RecordingSessionState.FAILED
    assert room.id not in manager.recording_sessions


def test_offline_result_closes_recoverable_session(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/12",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/offline-boundary",),
    )

    manager.start_for_room(room.id, resolved)
    session_id = manager.recording_sessions[room.id].session_id
    manager._finished(room.id, 1)
    manager.handle_stream_offline(room.id)

    completed = database.get_recording_session(session_id)
    assert completed is not None
    assert completed.state is RecordingSessionState.COMPLETED
    assert completed.recovery_reason == "offline"
    assert room.id not in manager.recording_sessions


def test_resolver_failure_does_not_close_pending_recovery(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/15",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/resolver-failure",),
        ),
    )
    session_id = manager.recording_sessions[room.id].session_id
    manager._finished(room.id, 1)

    coordinator = MonitoringCoordinator(rooms, object())
    coordinator.streamOffline.connect(manager.handle_stream_offline)
    coordinator._resolved(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            False,
            "",
            "",
            (),
            failure=AccessRestricted("anonymous access denied"),
        ),
    )

    pending = database.get_recording_session(session_id)
    assert pending is not None
    assert pending.state is RecordingSessionState.ACTIVE
    assert room.id in manager.recording_sessions


def test_manual_pause_abandons_pending_recovery(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/13",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()

    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/manual-pause",),
        ),
    )
    session_id = manager.recording_sessions[room.id].session_id
    manager._finished(room.id, 1)

    manager.stop_room(room.id)

    abandoned = database.get_recording_session(session_id)
    assert abandoned is not None
    assert abandoned.state is RecordingSessionState.ABANDONED
    assert abandoned.recovery_reason == "manual_stop"
    assert room.id not in manager.recording_sessions
    assert room.id not in manager.retry_counts
    assert rooms.get_room(room.id).enabled is False
    assert rooms.get_room(room.id).status is RoomStatus.DISABLED


def test_recovery_disk_guard_marks_session_failed(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    free_space = [True]
    monkeypatch.setattr(
        "reco_box.recording.has_minimum_free_space",
        lambda *_args: free_space[0],
    )

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/14",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/disk-preflight",),
    )

    manager.start_for_room(room.id, resolved)
    session_id = manager.recording_sessions[room.id].session_id
    manager._finished(room.id, 1)
    free_space[0] = False

    manager.start_for_room(room.id, resolved)

    failed = database.get_recording_session(session_id)
    assert failed is not None
    assert failed.state is RecordingSessionState.FAILED
    assert failed.recovery_reason == "disk_full"
    assert room.id not in manager.recording_sessions
    assert room.id not in manager.retry_counts
    assert room.id not in manager.processes


def test_manual_stop_during_conversion_abandons_the_session(monkeypatch, tmp_path) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/8",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    manager = RecordingManager(rooms, database, ffmpeg_path=tmp_path / "ffmpeg.exe")
    manager.progress_timer.stop()
    manager.ffprobe_path = None
    session_dir = tmp_path / "session"
    session_dir.mkdir()
    session = database.create_recording_session(
        room.id, datetime.now().astimezone(), session_dir
    )
    manager.recording_sessions[room.id] = session
    recording_id = database.start_recording(room.id, session.started_at, session_dir)

    manager._conversion_finished(
        room.id,
        recording_id,
        session_dir,
        True,
        ConversionResult(True, 12),
        True,
    )

    abandoned = database.get_recording_session(session.session_id)
    assert abandoned is not None
    assert abandoned.state is RecordingSessionState.ABANDONED


def test_conversion_worker_forwards_intentional_stop(monkeypatch, tmp_path) -> None:
    result = ConversionResult(True, 12)
    monkeypatch.setattr("reco_box.recording.convert_ts_segments", lambda *_args: result)
    worker = ConversionWorker(
        "room",
        "recording",
        tmp_path / "ffmpeg.exe",
        tmp_path,
        False,
        True,
    )
    emitted: list[tuple[object, ...]] = []
    worker.signals.completed.connect(lambda *args: emitted.append(args))

    worker.run()

    assert len(emitted) == 1
    assert emitted[0][:5] == ("room", "recording", tmp_path, False, result)
    assert emitted[0][5] is True
