from datetime import datetime

import pytest
from PySide6.QtCore import QCoreApplication, QProcess

from reco_box.domain import Platform, RecordingSessionState, Room, RoomStatus
from reco_box.monitor import MonitoringCoordinator
from reco_box.recording import ConversionResult, RecordingManager
from reco_box.recovery import RecoveryEvent, RecoveryState, RecoveryStateStore
from reco_box.resolver import ResolvedStream
from reco_box.room_model import RoomListModel
from reco_box.scheduler import MonitoringScheduler
from reco_box.storage import Database


class FakeSignal:
    def connect(self, _callback) -> None:
        return None


class FakeResolverPool:
    def __init__(self) -> None:
        self.workers = []

    def setMaxThreadCount(self, _count: int) -> None:
        return None

    def start(self, worker) -> None:
        self.workers.append(worker)


class FakeProcess:
    class ProcessChannelMode:
        MergedChannels = object()

    class ProcessState:
        Running = object()
        NotRunning = object()

    class ProcessError:
        FailedToStart = object()

    def __init__(self, _parent=None) -> None:
        self.started = FakeSignal()
        self.errorOccurred = FakeSignal()
        self.finished = FakeSignal()
        self.arguments: list[str] = []
        self.properties: dict[str, object] = {}
        self.writes: list[bytes] = []
        self._state = self.ProcessState.Running

    def setProcessChannelMode(self, _mode) -> None:
        return None

    def setProgram(self, _program: str) -> None:
        return None

    def setArguments(self, arguments: list[str]) -> None:
        self.arguments = arguments

    def setProperty(self, name: str, value: object) -> None:
        self.properties[name] = value

    def property(self, name: str) -> object:
        return self.properties.get(name)

    def start(self) -> None:
        return None

    def state(self):
        return self._state

    def write(self, data: bytes) -> int:
        self.writes.append(data)
        return len(data)

    def terminate(self) -> None:
        self._state = self.ProcessState.NotRunning

    def kill(self) -> None:
        self._state = self.ProcessState.NotRunning

    def deleteLater(self) -> None:
        return None


def test_monitor_state_store_tracks_check_live_and_offline_boundaries(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/21", platform=Platform.BILIBILI)
    database.upsert_room(room)
    rooms = RoomListModel(database)
    states = RecoveryStateStore()
    pool = FakeResolverPool()
    coordinator = MonitoringCoordinator(
        rooms,
        object(),
        scheduler=MonitoringScheduler(random_source=lambda low, high: low),
        resolver_pool=pool,
        recovery_states=states,
    )
    coordinator.next_check = {room.id: 0}

    coordinator._tick()
    assert states.state_for(room.id) is RecoveryState.CHECKING

    coordinator._resolved(
        room.id,
        ResolvedStream(Platform.BILIBILI, True, "主播", "直播", ("https://cdn.example/live",)),
    )
    assert states.state_for(room.id) is RecoveryState.PREPARING

    coordinator._resolved(
        room.id,
        ResolvedStream(Platform.BILIBILI, False, "主播", "", ()),
    )
    assert states.state_for(room.id) is RecoveryState.OFFLINE


def test_recording_manager_requires_offline_confirmation_after_clean_exit(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/22",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    states = RecoveryStateStore()
    manager = RecordingManager(
        rooms,
        database,
        ffmpeg_path=tmp_path / "ffmpeg.exe",
        recovery_states=states,
    )
    manager.progress_timer.stop()
    resolved = ResolvedStream(
        Platform.BILIBILI,
        True,
        "主播",
        "直播",
        ("https://cdn.example.test/clean",),
    )

    manager.start_for_room(room.id, resolved)
    assert states.state_for(room.id) is RecoveryState.PREPARING
    manager._process_started(room.id)
    assert states.state_for(room.id) is RecoveryState.RECORDING

    manager._finished(room.id, 0)

    assert states.state_for(room.id) is RecoveryState.CONFIRMING_OFFLINE
    first_session = manager.recording_sessions[room.id]
    assert first_session.state is RecordingSessionState.ACTIVE
    assert first_session.recovery_reason == "confirming_offline"
    assert rooms.get_room(room.id).status.value == "offline"

    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播继续",
            ("https://cdn.example.test/continued",),
        ),
    )
    second_session = manager.recording_sessions[room.id]
    assert second_session.session_id == first_session.session_id
    assert second_session.session_dir == first_session.session_dir
    assert second_session.attempt == 1
    assert "https://cdn.example.test/continued" in manager.processes[room.id].arguments
    manager._process_started(room.id)
    manager._finished(room.id, 0)

    manager.handle_stream_offline(room.id)
    assert states.state_for(room.id) is RecoveryState.OFFLINE
    persisted = database.get_recording_session(first_session.session_id)
    assert persisted is not None
    assert persisted.state is RecordingSessionState.COMPLETED
    assert room.id not in manager.recording_sessions


def test_manual_stop_is_idempotent_and_stall_watchdog_does_not_race(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/23",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    states = RecoveryStateStore()
    manager = RecordingManager(
        rooms,
        database,
        ffmpeg_path=tmp_path / "ffmpeg.exe",
        stall_timeout_seconds=1,
        stall_grace_seconds=0,
        recovery_states=states,
    )
    manager.progress_timer.stop()

    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/manual",),
        ),
    )
    manager._process_started(room.id)
    process = manager.processes[room.id]

    manager.stop_room(room.id)
    manager.stop_room(room.id)

    assert states.state_for(room.id) is RecoveryState.STOPPING
    assert process.writes == [b"q\n"]
    now = 1_000.0
    monkeypatch.setattr("reco_box.recording.time.monotonic", lambda: now)
    manager.started_monotonic[room.id] = now - 10
    manager.last_growth_at[room.id] = now - 10
    manager.last_file_bytes[room.id] = 0
    manager._update_progress()

    assert room.id not in manager.recovery_reasons
    assert process.writes == [b"q\n"]


@pytest.mark.parametrize(
    "result",
    [ConversionResult(True, 12), ConversionResult(False, 12, "conversion failed")],
)
def test_pause_during_conversion_wins_over_late_conversion_callback(
    monkeypatch, tmp_path, result
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/24",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=True,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    states = RecoveryStateStore()
    manager = RecordingManager(
        rooms,
        database,
        ffmpeg_path=tmp_path / "ffmpeg.exe",
        recovery_states=states,
    )
    manager.progress_timer.stop()
    manager.ffprobe_path = None
    session_dir = tmp_path / "session"
    session_dir.mkdir()
    session = database.create_recording_session(
        room.id, datetime.now().astimezone(), session_dir
    )
    manager.recording_sessions[room.id] = session
    recording_id = database.start_recording(room.id, session.started_at, session_dir)
    manager.converting_rooms.add(room.id)
    states.transition(room.id, RecoveryEvent.LIVE_DETECTED)
    states.transition(room.id, RecoveryEvent.RECORDING_STARTED)
    states.transition(room.id, RecoveryEvent.CONVERSION_STARTED)

    manager.stop_room(room.id)
    assert states.state_for(room.id) is RecoveryState.DISABLED
    assert room.id not in manager.recording_sessions
    assert rooms.get_room(room.id).enabled is False

    manager._conversion_finished(
        room.id,
        recording_id,
        session_dir,
        False,
        result,
        False,
    )

    assert states.state_for(room.id) is RecoveryState.DISABLED
    assert rooms.get_room(room.id).status is RoomStatus.DISABLED
    assert rooms.get_room(room.id).enabled is False


def test_qprocess_error_enters_recovery_and_monitor_waits_for_finalization(
    monkeypatch, tmp_path
) -> None:
    QCoreApplication.instance() or QCoreApplication([])
    monkeypatch.setattr("reco_box.recording.QProcess", FakeProcess)
    monkeypatch.setattr("reco_box.recording.has_minimum_free_space", lambda *_args: True)

    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/25",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path),
        convert_to_mp4=False,
    )
    database.upsert_room(room)
    rooms = RoomListModel(database)
    states = RecoveryStateStore()
    manager = RecordingManager(
        rooms,
        database,
        ffmpeg_path=tmp_path / "ffmpeg.exe",
        recovery_states=states,
    )
    manager.progress_timer.stop()
    manager.start_for_room(
        room.id,
        ResolvedStream(
            Platform.BILIBILI,
            True,
            "主播",
            "直播",
            ("https://cdn.example.test/crash",),
        ),
    )
    manager._process_started(room.id)

    manager._process_error(room.id, QProcess.ProcessError.Crashed, "process crashed")

    assert states.state_for(room.id) is RecoveryState.RECOVERING
    assert manager.recovery_reasons[room.id].kind.value == "ffmpeg_failed"
    assert rooms.get_room(room.id).status is RoomStatus.ERROR

    pool = FakeResolverPool()
    coordinator = MonitoringCoordinator(
        rooms,
        object(),
        scheduler=MonitoringScheduler(random_source=lambda low, high: low),
        resolver_pool=pool,
        recovery_states=states,
    )
    coordinator.next_check[room.id] = 0
    coordinator._tick()
    assert pool.workers == []

    manager._finished(room.id, 1)
    assert states.state_for(room.id) is RecoveryState.RECOVERING
    assert rooms.get_room(room.id).status is RoomStatus.RETRYING


def test_recovery_event_enum_is_the_only_input_to_a_state_machine() -> None:
    states = RecoveryStateStore()

    assert states.transition("room", RecoveryEvent.CHECK_REQUESTED) is RecoveryState.CHECKING
    assert states.state_for("room") is RecoveryState.CHECKING

