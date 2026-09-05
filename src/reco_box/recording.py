from __future__ import annotations

import os
import shutil
import subprocess
import time
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from PySide6.QtCore import QObject, QProcess, QRunnable, QThreadPool, QTimer, Signal, Slot

from .domain import RecordingSession, RecordingSessionState, RoomStatus
from .errors import (
    DiskFull,
    FFmpegFailed,
    RecordingFailure,
    Stalled,
    classify_recording_error,
    recording_failure_for_exit,
    safe_error_text,
)
from .ffmpeg import FFmpegPlanner, StreamInput, hidden_startup_info
from .localization import tr
from .media_probe import ProbeResult, find_ffprobe, media_files, probe_media_files
from .output_paths import next_session_output_number
from .resolver import ResolvedStream
from .resources import application_resource
from .room_model import RoomListModel
from .storage import Database

DEFAULT_STALL_TIMEOUT_SECONDS = 120.0
STALL_STARTUP_GRACE_SECONDS = 30.0


def recording_retry_delay(attempt: int) -> int:
    return min(5 * (2 ** max(0, attempt - 1)), 120)


def has_minimum_free_space(path: Path, minimum_gb: float) -> bool:
    required_bytes = max(0, int(minimum_gb * 1024**3))
    return shutil.disk_usage(path).free >= required_bytes


def recording_succeeded(
    exit_code: int, intentional_stop: bool, protective_error: str = ""
) -> bool:
    return (exit_code == 0 or intentional_stop) and not protective_error


def should_mark_stalled(
    *,
    process_running: bool,
    file_bytes: int,
    last_file_bytes: int,
    started_at: float,
    last_growth_at: float,
    now: float,
    stall_timeout_seconds: float = DEFAULT_STALL_TIMEOUT_SECONDS,
    startup_grace_seconds: float = STALL_STARTUP_GRACE_SECONDS,
) -> bool:
    """Return whether a running recording has exceeded the no-growth window."""

    if not process_running:
        return False
    if now - started_at < max(0.0, float(startup_grace_seconds)):
        return False
    if file_bytes > last_file_bytes:
        return False
    return now - last_growth_at >= max(0.0, float(stall_timeout_seconds))


def find_ffmpeg() -> Path | None:
    override = os.environ.get("RECO_BOX_FFMPEG", "").strip()
    discovered = shutil.which("ffmpeg")
    candidates = [
        Path(override) if override else None,
        application_resource("runtime", "ffmpeg", "ffmpeg.exe"),
        Path(discovered) if discovered else None,
    ]
    return next((path for path in candidates if path and path.is_file()), None)


@dataclass(slots=True, frozen=True)
class ConversionResult:
    success: bool
    total_bytes: int
    error: str = ""
    failure: RecordingFailure | None = None


def convert_ts_segments(ffmpeg_path: Path, session_dir: Path) -> ConversionResult:
    sources = [path for path in media_files(session_dir) if path.suffix.lower() == ".ts"]
    if not sources:
        total = sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file())
        return ConversionResult(True, total)

    converted: list[Path] = []
    creation_flags = getattr(subprocess, "CREATE_NO_WINDOW", 0)
    for source in sources:
        destination = source.with_suffix(".mp4")
        command = [
            str(ffmpeg_path),
            "-hide_banner",
            "-loglevel",
            "error",
            "-y",
            "-i",
            str(source),
            "-map",
            "0",
            "-c",
            "copy",
            "-movflags",
            "+faststart",
            str(destination),
        ]
        try:
            completed = subprocess.run(
                command,
                capture_output=True,
                text=True,
                encoding="utf-8",
                errors="replace",
                check=False,
                timeout=600,
                creationflags=creation_flags,
                startupinfo=hidden_startup_info(),
            )
        except (OSError, subprocess.TimeoutExpired) as error:
            destination.unlink(missing_ok=True)
            failure = classify_recording_error(error)
            return ConversionResult(
                False,
                sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file()),
                f"{source.name} 转换失败：{failure}",
                failure,
            )
        if completed.returncode != 0:
            destination.unlink(missing_ok=True)
            message = completed.stderr.replace("\r", " ").replace("\n", " ").strip()
            failure = FFmpegFailed(
                f"{source.name} 转换失败：{message[:300] or completed.returncode}"
            )
            return ConversionResult(
                False,
                sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file()),
                str(failure),
                failure,
            )
        converted.append(destination)

    for source in sources:
        source.unlink()
    total = sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file())
    return ConversionResult(True, total)


class ProbeSignals(QObject):
    completed = Signal(str, object)


class ProbeWorker(QRunnable):
    def __init__(self, recording_id: str, ffprobe_path: Path, session_dir: Path):
        super().__init__()
        self.recording_id = recording_id
        self.ffprobe_path = ffprobe_path
        self.session_dir = session_dir
        self.signals = ProbeSignals()

    @Slot()
    def run(self) -> None:
        result = probe_media_files(self.ffprobe_path, media_files(self.session_dir))
        self.signals.completed.emit(self.recording_id, result)


class ConversionSignals(QObject):
    completed = Signal(str, str, object, bool, object, bool)


class ConversionWorker(QRunnable):
    def __init__(
        self,
        room_id: str,
        recording_id: str,
        ffmpeg_path: Path,
        session_dir: Path,
        pause_monitoring: bool,
        intentional_stop: bool = False,
    ):
        super().__init__()
        self.room_id = room_id
        self.recording_id = recording_id
        self.ffmpeg_path = ffmpeg_path
        self.session_dir = session_dir
        self.pause_monitoring = pause_monitoring
        self.intentional_stop = intentional_stop
        self.signals = ConversionSignals()

    @Slot()
    def run(self) -> None:
        result = convert_ts_segments(self.ffmpeg_path, self.session_dir)
        self.signals.completed.emit(
            self.room_id,
            self.recording_id,
            self.session_dir,
            self.pause_monitoring,
            result,
            self.intentional_stop,
        )


class RecordingManager(QObject):
    recordingCompleted = Signal()
    retryRequested = Signal(str, int)

    def __init__(
        self,
        rooms: RoomListModel,
        database: Database,
        ffmpeg_path: Path | None = None,
        *,
        stall_timeout_seconds: float = DEFAULT_STALL_TIMEOUT_SECONDS,
        stall_grace_seconds: float = STALL_STARTUP_GRACE_SECONDS,
    ):
        super().__init__()
        self.rooms = rooms
        self.database = database
        self.ffmpeg_path = Path(ffmpeg_path) if ffmpeg_path else find_ffmpeg()
        self.ffprobe_path = find_ffprobe()
        self.stall_timeout_seconds = max(0.0, float(stall_timeout_seconds))
        self.stall_grace_seconds = max(0.0, float(stall_grace_seconds))
        self.worker_pool = QThreadPool.globalInstance()
        self.processes: dict[str, QProcess] = {}
        self.converting_rooms: set[str] = set()
        self.recording_ids: dict[str, str] = {}
        self.session_dirs: dict[str, Path] = {}
        self.recording_sessions: dict[str, RecordingSession] = {}
        self.started_monotonic: dict[str, float] = {}
        self.manual_stops: set[str] = set()
        self.pause_after_stops: set[str] = set()
        self.retry_counts: dict[str, int] = {}
        self.session_groups: dict[str, str] = {}
        self.recovery_indices: dict[str, int] = {}
        self.last_file_bytes: dict[str, int] = {}
        self.last_growth_at: dict[str, float] = {}
        self.recovery_reasons: dict[str, RecordingFailure] = {}
        self.last_disk_checks: dict[str, float] = {}
        self.protective_stop_errors: dict[str, str] = {}
        self.last_recording_failures: dict[str, RecordingFailure] = {}
        self.progress_timer = QTimer(self)
        self.progress_timer.setInterval(1_000)
        self.progress_timer.timeout.connect(self._update_progress)
        self.progress_timer.start()

    @Slot(str, object)
    def start_for_room(self, room_id: str, resolved: ResolvedStream) -> None:
        room = self.rooms.get_room(room_id)
        if room is None or room_id in self.processes or room_id in self.converting_rooms:
            return
        if self.ffmpeg_path is None:
            failure = FFmpegFailed(tr("未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG"))
            self.last_recording_failures[room_id] = failure
            self.rooms.update_room_state(
                room_id,
                RoomStatus.ERROR,
                error=str(failure),
            )
            return
        if not resolved.stream_urls:
            self.last_recording_failures.pop(room_id, None)
            self.rooms.update_room_state(room_id, RoomStatus.OFFLINE)
            return

        started_at = datetime.now().astimezone()
        stream = StreamInput(
            self._selected_stream_url(room.line, resolved.stream_urls),
            headers=resolved.headers,
            proxy=room.proxy,
        )
        planner = FFmpegPlanner(self.ffmpeg_path)
        current_session = self.recording_sessions.get(room_id)
        try:
            if current_session is None or current_session.state is not RecordingSessionState.ACTIVE:
                plan = planner.build(room, stream, started_at)
                session = RecordingSession(
                    session_id=str(uuid4()),
                    room_id=room_id,
                    started_at=started_at,
                    session_dir=plan.session_dir,
                    last_stream_url=stream.url,
                )
            else:
                start_number = next_session_output_number(
                    current_session.session_dir,
                    room.output_format,
                    "" if room.segment_enabled else room.file_name,
                )
                plan = planner.build_for_session(
                    room,
                    stream,
                    current_session.session_dir,
                    start_number=start_number,
                )
                session = RecordingSession(
                    session_id=current_session.session_id,
                    room_id=room_id,
                    started_at=current_session.started_at,
                    session_dir=current_session.session_dir,
                    attempt=current_session.attempt + 1,
                    last_stream_url=stream.url,
                )
        except ValueError as error:
            failure = classify_recording_error(error)
            self.last_recording_failures[room_id] = failure
            self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=str(failure))
            return

        try:
            minimum_free_gb = float(self.database.get_setting("minimum_free_gb", "5"))
        except ValueError:
            minimum_free_gb = 5.0
        if not has_minimum_free_space(plan.session_dir, minimum_free_gb):
            failure = DiskFull(
                tr("磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制").format(
                    minimum_free_gb=minimum_free_gb
                )
            )
            if (
                current_session is not None
                and current_session.state is RecordingSessionState.ACTIVE
            ):
                self.retry_counts.pop(room_id, None)
                self._finish_session(
                    room_id, RecordingSessionState.FAILED, failure.kind.value
                )
            self.last_recording_failures[room_id] = failure
            self.rooms.update_room_state(
                room_id,
                RoomStatus.ERROR,
                error=str(failure),
            )
            return

        self.recording_sessions[room_id] = session
        self.database.upsert_recording_session(session)
        self.last_recording_failures.pop(room_id, None)
        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.setProgram(plan.command[0])
        process.setArguments(list(plan.command[1:]))
        process.started.connect(lambda: self._process_started(room_id))
        process.errorOccurred.connect(
            lambda error: self._process_error(room_id, error, process.errorString())
        )
        process.finished.connect(lambda exit_code, _status: self._finished(room_id, int(exit_code)))
        self.processes[room_id] = process
        self.session_dirs[room_id] = plan.session_dir
        self.last_file_bytes[room_id] = 0
        self.started_monotonic.pop(room_id, None)
        self.last_growth_at.pop(room_id, None)
        self.last_disk_checks[room_id] = 0
        self.session_groups[room_id] = session.session_id
        self.recovery_indices[room_id] = session.attempt
        self.recording_ids[room_id] = self.database.start_recording(
            room_id,
            started_at,
            plan.session_dir,
            group_id=session.session_id,
            recovery_index=session.attempt,
        )
        process.start()

    def _retain_session_for_recovery(
        self, room_id: str, failure: RecordingFailure | None
    ) -> None:
        session = self.recording_sessions.get(room_id)
        if session is None:
            return
        session.state = RecordingSessionState.ACTIVE
        session.recovery_reason = failure.kind.value if failure else "ffmpeg_failed"
        self.database.upsert_recording_session(session)
        self.session_groups[room_id] = session.session_id
        self.recovery_indices[room_id] = session.attempt + 1

    def _finish_session(
        self,
        room_id: str,
        state: RecordingSessionState,
        recovery_reason: str = "",
    ) -> None:
        session = self.recording_sessions.pop(room_id, None)
        if session is not None:
            session.state = state
            session.recovery_reason = recovery_reason
            self.database.upsert_recording_session(session)
        self.session_groups.pop(room_id, None)
        self.recovery_indices.pop(room_id, None)

    @Slot(str)
    def handle_stream_offline(self, room_id: str) -> None:
        """Close a recoverable session after the resolver reports it offline."""

        if room_id in self.processes or room_id in self.converting_rooms:
            return
        self.retry_counts.pop(room_id, None)
        self._finish_session(room_id, RecordingSessionState.COMPLETED, "offline")

    def _process_started(self, room_id: str) -> None:
        if room_id not in self.processes:
            return
        started = time.monotonic()
        self.started_monotonic[room_id] = started
        self.last_growth_at[room_id] = started
        self.rooms.update_room_state(room_id, RoomStatus.RECORDING)

    @Slot()
    def _update_progress(self) -> None:
        for room_id, session_dir in tuple(self.session_dirs.items()):
            file_bytes = (
                sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file())
                if session_dir.exists()
                else 0
            )
            started = self.started_monotonic.get(room_id)
            if started is None:
                self.last_file_bytes[room_id] = file_bytes
                self.rooms.update_recording_progress(room_id, 0, file_bytes)
                continue
            duration = max(0, int(time.monotonic() - started))
            self.rooms.update_recording_progress(room_id, duration, file_bytes)
            now = time.monotonic()
            previous_file_bytes = self.last_file_bytes.get(room_id, file_bytes)
            if file_bytes > previous_file_bytes:
                self.last_growth_at[room_id] = now
            self.last_file_bytes[room_id] = file_bytes
            if (
                room_id not in self.protective_stop_errors
                and now - self.last_disk_checks.get(room_id, 0) >= 30
            ):
                self.last_disk_checks[room_id] = now
                try:
                    minimum_free_gb = float(
                        self.database.get_setting("minimum_free_gb", "5")
                    )
                except ValueError:
                    minimum_free_gb = 5.0
                if not has_minimum_free_space(session_dir, minimum_free_gb):
                    message = (
                        f"磁盘剩余空间低于 {minimum_free_gb:g} GB，已安全停止录制"
                    )
                    self.last_recording_failures[room_id] = DiskFull(message)
                    self.protective_stop_errors[room_id] = message
                    process = self.processes.get(room_id)
                    if process:
                        process.write(b"q\n")
                        QTimer.singleShot(
                            8_000,
                            lambda room=room_id, expected=process: self._terminate_if_running(
                                room, expected
                            ),
                        )
            process = self.processes.get(room_id)
            if (
                process is not None
                and room_id not in self.protective_stop_errors
                and room_id not in self.recovery_reasons
                and should_mark_stalled(
                    process_running=process.state() == QProcess.ProcessState.Running,
                    file_bytes=file_bytes,
                    last_file_bytes=previous_file_bytes,
                    started_at=started,
                    last_growth_at=self.last_growth_at.get(room_id, started),
                    now=now,
                    stall_timeout_seconds=self.stall_timeout_seconds,
                    startup_grace_seconds=self.stall_grace_seconds,
                )
            ):
                self._request_recovery_stop(
                    room_id,
                    Stalled(
                        f"录制文件已超过 {self.stall_timeout_seconds:g} 秒未增长，已安全停止录制"
                    ),
                )

    @Slot(str)
    def stop_room(self, room_id: str) -> None:
        self._request_stop(room_id, pause_monitoring=True)

    def _abandon_pending_session(self, room_id: str) -> None:
        if room_id not in self.recording_sessions:
            return
        self.retry_counts.pop(room_id, None)
        self._finish_session(room_id, RecordingSessionState.ABANDONED, "manual_stop")
        self.rooms.update_recording_progress(room_id, 0, 0)
        self.recordingCompleted.emit()

    def _request_stop(self, room_id: str, pause_monitoring: bool) -> None:
        process = self.processes.get(room_id)
        if process is None:
            if pause_monitoring:
                self._abandon_pending_session(room_id)
                self.rooms.set_room_enabled(room_id, False)
            return
        self.manual_stops.add(room_id)
        if pause_monitoring:
            self.pause_after_stops.add(room_id)
        process.setProperty("intentionalStop", True)
        process.write(b"q\n")
        QTimer.singleShot(
            8_000,
            lambda room=room_id, expected=process: self._terminate_if_running(room, expected),
        )

    def _request_recovery_stop(self, room_id: str, failure: RecordingFailure) -> None:
        process = self.processes.get(room_id)
        if process is None or process.state() != QProcess.ProcessState.Running:
            return
        self.recovery_reasons[room_id] = failure
        process.setProperty("recoveryReason", failure.kind.value)
        self.last_recording_failures[room_id] = failure
        self.rooms.update_room_state(room_id, RoomStatus.STALLED, error=str(failure))
        process.write(b"q\n")
        QTimer.singleShot(
            8_000,
            lambda room=room_id, expected=process: self._terminate_if_running(room, expected),
        )

    @Slot()
    def stop_all(self) -> None:
        for room_id in tuple(self.processes):
            self._request_stop(room_id, pause_monitoring=False)

    @Slot()
    def stopAllAndPause(self) -> None:
        self.rooms.setAllEnabled(False)
        for room_id in tuple(self.recording_sessions):
            if room_id not in self.processes and room_id not in self.converting_rooms:
                self._abandon_pending_session(room_id)
        for room_id in tuple(self.processes):
            self._request_stop(room_id, pause_monitoring=True)

    @staticmethod
    def _selected_stream_url(line: str, stream_urls: tuple[str, ...]) -> str:
        if not stream_urls:
            raise ValueError(tr("未找到可用直播线路"))
        digits = "".join(character for character in line if character.isdigit())
        index = max(0, int(digits or "1") - 1)
        return stream_urls[min(index, len(stream_urls) - 1)]

    def _terminate_if_running(
        self, room_id: str, expected_process: QProcess | None = None
    ) -> None:
        process = self.processes.get(room_id)
        if (
            process
            and (expected_process is None or process is expected_process)
            and process.state() != QProcess.ProcessState.NotRunning
        ):
            process.terminate()
            QTimer.singleShot(
                3_000,
                lambda room=room_id, expected=process: self._kill_if_running(room, expected),
            )

    def _kill_if_running(self, room_id: str, expected_process: QProcess | None = None) -> None:
        process = self.processes.get(room_id)
        if (
            process
            and (expected_process is None or process is expected_process)
            and process.state() != QProcess.ProcessState.NotRunning
        ):
            process.kill()

    def _process_error(
        self, room_id: str, error: QProcess.ProcessError, message: str
    ) -> None:
        process = self.processes.get(room_id)
        intentional = bool(process and process.property("intentionalStop"))
        if intentional or room_id in self.manual_stops or room_id in self.recovery_reasons:
            return
        failure = FFmpegFailed(message or f"FFmpeg 进程错误：{error}")
        self.last_recording_failures[room_id] = failure
        self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=str(failure))
        if error == QProcess.ProcessError.FailedToStart:
            QTimer.singleShot(0, lambda: self._finished(room_id, -1))

    def _finished(self, room_id: str, exit_code: int) -> None:
        if room_id not in self.processes:
            return
        process = self.processes.pop(room_id, None)
        intentional_stop = bool(process and process.property("intentionalStop"))
        if process:
            process.deleteLater()
        session_dir = self.session_dirs.pop(room_id, Path())
        self.started_monotonic.pop(room_id, None)
        self.last_file_bytes.pop(room_id, None)
        self.last_growth_at.pop(room_id, None)
        recovery_failure = self.recovery_reasons.pop(room_id, None)
        self.last_disk_checks.pop(room_id, None)
        total_bytes = (
            sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file())
            if session_dir.exists()
            else 0
        )
        recording_id = self.recording_ids.pop(room_id, "")
        manual_stop = room_id in self.manual_stops or intentional_stop
        self.manual_stops.discard(room_id)
        pause_monitoring = room_id in self.pause_after_stops
        self.pause_after_stops.discard(room_id)
        protective_error = self.protective_stop_errors.pop(room_id, "")
        recovery_failed = recovery_failure is not None and not manual_stop and not protective_error
        success = recording_succeeded(exit_code, manual_stop, protective_error) and (
            not recovery_failed
        )
        failure = recording_failure_for_exit(
            exit_code,
            intentional_stop=manual_stop,
            protective_error=protective_error,
            message=f"FFmpeg 退出码 {exit_code}",
            recovery_failure=recovery_failure,
        )
        if failure is not None:
            self.last_recording_failures[room_id] = failure
        elif success:
            self.last_recording_failures.pop(room_id, None)
        room = self.rooms.get_room(room_id)
        if success and recording_id and room and room.convert_to_mp4:
            self.database.mark_recording_converting(
                recording_id, datetime.now().astimezone(), total_bytes
            )
            self.converting_rooms.add(room_id)
            self.rooms.update_room_state(room_id, RoomStatus.CONVERTING)
            worker = ConversionWorker(
                room_id,
                recording_id,
                self.ffmpeg_path,
                session_dir,
                pause_monitoring,
                manual_stop,
            )
            worker.signals.completed.connect(self._conversion_finished)
            self.worker_pool.start(worker)
            self.rooms.update_recording_progress(room_id, 0, total_bytes)
            self.recordingCompleted.emit()
            return
        if recording_id:
            self.database.finish_recording(
                recording_id,
                datetime.now().astimezone(),
                "completed" if success else "failed",
                total_bytes,
                "" if success else str(failure or FFmpegFailed(f"FFmpeg 退出码 {exit_code}")),
            )
            if success:
                self._start_probe(recording_id, session_dir)
        if protective_error:
            self.retry_counts.pop(room_id, None)
            self._finish_session(
                room_id,
                RecordingSessionState.FAILED,
                failure.kind.value if failure else "disk_full",
            )
            room = self.rooms.get_room(room_id)
            delay = room.check_interval_seconds if room else 300
            self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=str(failure))
            self.retryRequested.emit(room_id, delay)
        elif success:
            self.retry_counts.pop(room_id, None)
            self._finish_session(
                room_id,
                RecordingSessionState.ABANDONED
                if manual_stop
                else RecordingSessionState.COMPLETED,
                "manual_stop" if manual_stop else "",
            )
            if pause_monitoring:
                self.rooms.set_room_enabled(room_id, False)
            else:
                self.rooms.update_room_state(room_id, RoomStatus.OFFLINE)
        else:
            attempt = self.retry_counts.get(room_id, 0) + 1
            self.retry_counts[room_id] = attempt
            room = self.rooms.get_room(room_id)
            if attempt <= 5:
                delay = recording_retry_delay(attempt)
                if room_id not in self.recording_sessions:
                    self.recovery_indices[room_id] = attempt
                self._retain_session_for_recovery(room_id, failure)
                self.rooms.update_room_state(
                    room_id,
                    RoomStatus.RETRYING,
                    error=f"{failure or FFmpegFailed(f'FFmpeg 退出码 {exit_code}')}；{delay} 秒后进行第 {attempt} 次重试",
                )
            else:
                delay = room.check_interval_seconds if room else 300
                self.retry_counts.pop(room_id, None)
                self._finish_session(
                    room_id,
                    RecordingSessionState.FAILED,
                    failure.kind.value if failure else "ffmpeg_failed",
                )
                self.rooms.update_room_state(
                    room_id,
                    RoomStatus.ERROR,
                    error=f"FFmpeg 连续重试 5 次仍失败；{delay} 秒后恢复常规监控",
                )
            self.retryRequested.emit(room_id, delay)
        self.rooms.update_recording_progress(room_id, 0, total_bytes)
        self.recordingCompleted.emit()

    @Slot(str, str, object, bool, object, bool)
    def _conversion_finished(
        self,
        room_id: str,
        recording_id: str,
        session_dir: Path,
        pause_monitoring: bool,
        result: ConversionResult,
        intentional_stop: bool = False,
    ) -> None:
        self.converting_rooms.discard(room_id)
        failure = result.failure
        if failure is None and not result.success:
            failure = classify_recording_error(result.error or "录制转换失败")
        if failure is not None:
            self.last_recording_failures[room_id] = failure
        elif result.success:
            self.last_recording_failures.pop(room_id, None)
        error_message = safe_error_text(result.error) if result.error else ""
        if failure is not None and not error_message:
            error_message = str(failure)
        status = "completed" if result.success else "failed"
        self.database.finish_recording(
            recording_id,
            datetime.now().astimezone(),
            status,
            result.total_bytes,
            error_message,
        )
        if result.success:
            self._start_probe(recording_id, session_dir)
        self.retry_counts.pop(room_id, None)
        self._finish_session(
            room_id,
            RecordingSessionState.ABANDONED
            if intentional_stop
            else (
                RecordingSessionState.COMPLETED
                if result.success
                else RecordingSessionState.FAILED
            ),
            "manual_stop"
            if intentional_stop
            else ("" if result.success else (failure.kind.value if failure else "ffmpeg_failed")),
        )
        if pause_monitoring:
            self.rooms.set_room_enabled(room_id, False)
            if error_message:
                self.rooms.update_room_state(
                    room_id, RoomStatus.DISABLED, error=error_message
                )
        elif result.success:
            self.rooms.update_room_state(room_id, RoomStatus.OFFLINE)
        else:
            self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=error_message)
        self.rooms.update_recording_progress(room_id, 0, result.total_bytes)
        self.recordingCompleted.emit()

    def _start_probe(self, recording_id: str, session_dir: Path) -> None:
        if self.ffprobe_path is None:
            self.database.update_recording_probe(
                recording_id, "invalid", 0, "", tr("未找到 ffprobe")
            )
            return
        if not media_files(session_dir):
            self.database.update_recording_probe(
                recording_id, "invalid", 0, "", tr("录制目录中没有媒体文件")
            )
            return
        worker = ProbeWorker(recording_id, self.ffprobe_path, session_dir)
        worker.signals.completed.connect(self._probe_finished)
        self.worker_pool.start(worker)

    @Slot(str, object)
    def _probe_finished(self, recording_id: str, result: ProbeResult) -> None:
        self.database.update_recording_probe(
            recording_id,
            "valid" if result.valid else "invalid",
            result.duration_seconds,
            result.codec_summary,
            result.error,
        )
        self.recordingCompleted.emit()
