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

from .domain import RoomStatus
from .ffmpeg import FFmpegPlanner, StreamInput, hidden_startup_info
from .localization import tr
from .media_probe import ProbeResult, find_ffprobe, media_files, probe_media_files
from .resolver import ResolvedStream
from .resources import application_resource
from .room_model import RoomListModel
from .storage import Database


def recording_retry_delay(attempt: int) -> int:
    return min(5 * (2 ** max(0, attempt - 1)), 120)


def has_minimum_free_space(path: Path, minimum_gb: float) -> bool:
    required_bytes = max(0, int(minimum_gb * 1024**3))
    return shutil.disk_usage(path).free >= required_bytes


def recording_succeeded(
    exit_code: int, intentional_stop: bool, protective_error: str = ""
) -> bool:
    return (exit_code == 0 or intentional_stop) and not protective_error


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
            return ConversionResult(
                False,
                sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file()),
                f"{source.name} 转换失败：{str(error)[:300]}",
            )
        if completed.returncode != 0:
            destination.unlink(missing_ok=True)
            message = completed.stderr.replace("\r", " ").replace("\n", " ").strip()
            return ConversionResult(
                False,
                sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file()),
                f"{source.name} 转换失败：{message[:300] or completed.returncode}",
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
    completed = Signal(str, str, object, bool, object)


class ConversionWorker(QRunnable):
    def __init__(
        self,
        room_id: str,
        recording_id: str,
        ffmpeg_path: Path,
        session_dir: Path,
        pause_monitoring: bool,
    ):
        super().__init__()
        self.room_id = room_id
        self.recording_id = recording_id
        self.ffmpeg_path = ffmpeg_path
        self.session_dir = session_dir
        self.pause_monitoring = pause_monitoring
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
        )


class RecordingManager(QObject):
    recordingCompleted = Signal()
    retryRequested = Signal(str, int)

    def __init__(self, rooms: RoomListModel, database: Database, ffmpeg_path: Path | None = None):
        super().__init__()
        self.rooms = rooms
        self.database = database
        self.ffmpeg_path = Path(ffmpeg_path) if ffmpeg_path else find_ffmpeg()
        self.ffprobe_path = find_ffprobe()
        self.worker_pool = QThreadPool.globalInstance()
        self.processes: dict[str, QProcess] = {}
        self.converting_rooms: set[str] = set()
        self.recording_ids: dict[str, str] = {}
        self.session_dirs: dict[str, Path] = {}
        self.started_monotonic: dict[str, float] = {}
        self.manual_stops: set[str] = set()
        self.pause_after_stops: set[str] = set()
        self.retry_counts: dict[str, int] = {}
        self.session_groups: dict[str, str] = {}
        self.recovery_indices: dict[str, int] = {}
        self.last_disk_checks: dict[str, float] = {}
        self.protective_stop_errors: dict[str, str] = {}
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
            self.rooms.update_room_state(
                room_id,
                RoomStatus.ERROR,
                error=tr("未找到 FFmpeg；开发版需要设置 RECO_BOX_FFMPEG"),
            )
            return
        if not resolved.stream_urls:
            self.rooms.update_room_state(room_id, RoomStatus.OFFLINE)
            return

        started_at = datetime.now().astimezone()
        try:
            plan = FFmpegPlanner(self.ffmpeg_path).build(
                room,
                StreamInput(
                    self._selected_stream_url(room.line, resolved.stream_urls),
                    headers=resolved.headers,
                    proxy=room.proxy,
                ),
                started_at,
            )
        except ValueError as error:
            self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=str(error))
            return

        try:
            minimum_free_gb = float(self.database.get_setting("minimum_free_gb", "5"))
        except ValueError:
            minimum_free_gb = 5.0
        if not has_minimum_free_space(plan.session_dir, minimum_free_gb):
            self.rooms.update_room_state(
                room_id,
                RoomStatus.ERROR,
                error=tr("磁盘剩余空间低于 {minimum_free_gb:g} GB，已阻止开始录制").format(
                    minimum_free_gb=minimum_free_gb
                ),
            )
            return

        process = QProcess(self)
        process.setProcessChannelMode(QProcess.ProcessChannelMode.MergedChannels)
        process.setProgram(plan.command[0])
        process.setArguments(list(plan.command[1:]))
        process.started.connect(lambda: self.rooms.update_room_state(room_id, RoomStatus.RECORDING))
        process.errorOccurred.connect(
            lambda error: self._process_error(room_id, error, process.errorString())
        )
        process.finished.connect(lambda exit_code, _status: self._finished(room_id, int(exit_code)))
        self.processes[room_id] = process
        self.session_dirs[room_id] = plan.session_dir
        self.started_monotonic[room_id] = time.monotonic()
        self.last_disk_checks[room_id] = 0
        group_id = self.session_groups.setdefault(room_id, str(uuid4()))
        recovery_index = self.recovery_indices.get(room_id, 0)
        self.recording_ids[room_id] = self.database.start_recording(
            room_id,
            started_at,
            plan.session_dir,
            group_id=group_id,
            recovery_index=recovery_index,
        )
        process.start()

    @Slot()
    def _update_progress(self) -> None:
        for room_id, session_dir in tuple(self.session_dirs.items()):
            started = self.started_monotonic.get(room_id, time.monotonic())
            duration = max(0, int(time.monotonic() - started))
            file_bytes = (
                sum(path.stat().st_size for path in session_dir.glob("*") if path.is_file())
                if session_dir.exists()
                else 0
            )
            self.rooms.update_recording_progress(room_id, duration, file_bytes)
            now = time.monotonic()
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
                    self.protective_stop_errors[room_id] = message
                    process = self.processes.get(room_id)
                    if process:
                        process.write(b"q\n")
                        QTimer.singleShot(
                            8_000, lambda room=room_id: self._terminate_if_running(room)
                        )

    @Slot(str)
    def stop_room(self, room_id: str) -> None:
        self._request_stop(room_id, pause_monitoring=True)

    def _request_stop(self, room_id: str, pause_monitoring: bool) -> None:
        process = self.processes.get(room_id)
        if process is None:
            return
        self.manual_stops.add(room_id)
        if pause_monitoring:
            self.pause_after_stops.add(room_id)
        process.setProperty("intentionalStop", True)
        process.write(b"q\n")
        QTimer.singleShot(8_000, lambda: self._terminate_if_running(room_id))

    @Slot()
    def stop_all(self) -> None:
        for room_id in tuple(self.processes):
            self._request_stop(room_id, pause_monitoring=False)

    @Slot()
    def stopAllAndPause(self) -> None:
        self.rooms.setAllEnabled(False)
        for room_id in tuple(self.processes):
            self._request_stop(room_id, pause_monitoring=True)

    @staticmethod
    def _selected_stream_url(line: str, stream_urls: tuple[str, ...]) -> str:
        if not stream_urls:
            raise ValueError(tr("未找到可用直播线路"))
        digits = "".join(character for character in line if character.isdigit())
        index = max(0, int(digits or "1") - 1)
        return stream_urls[min(index, len(stream_urls) - 1)]

    def _terminate_if_running(self, room_id: str) -> None:
        process = self.processes.get(room_id)
        if process and process.state() != QProcess.ProcessState.NotRunning:
            process.terminate()
            QTimer.singleShot(3_000, lambda: self._kill_if_running(room_id))

    def _kill_if_running(self, room_id: str) -> None:
        process = self.processes.get(room_id)
        if process and process.state() != QProcess.ProcessState.NotRunning:
            process.kill()

    def _process_error(
        self, room_id: str, error: QProcess.ProcessError, message: str
    ) -> None:
        process = self.processes.get(room_id)
        intentional = bool(process and process.property("intentionalStop"))
        if intentional or room_id in self.manual_stops:
            return
        self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=message[:300])
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
        success = recording_succeeded(exit_code, manual_stop, protective_error)
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
                "" if success else protective_error or f"FFmpeg 退出码 {exit_code}",
            )
            if success:
                self._start_probe(recording_id, session_dir)
        if protective_error:
            self.retry_counts.pop(room_id, None)
            self.session_groups.pop(room_id, None)
            self.recovery_indices.pop(room_id, None)
            room = self.rooms.get_room(room_id)
            delay = room.check_interval_seconds if room else 300
            self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=protective_error)
            self.retryRequested.emit(room_id, delay)
        elif success:
            self.retry_counts.pop(room_id, None)
            self.session_groups.pop(room_id, None)
            self.recovery_indices.pop(room_id, None)
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
                self.recovery_indices[room_id] = attempt
                self.rooms.update_room_state(
                    room_id,
                    RoomStatus.RETRYING,
                    error=f"FFmpeg 退出码 {exit_code}；{delay} 秒后进行第 {attempt} 次重试",
                )
            else:
                delay = room.check_interval_seconds if room else 300
                self.retry_counts.pop(room_id, None)
                self.session_groups.pop(room_id, None)
                self.recovery_indices.pop(room_id, None)
                self.rooms.update_room_state(
                    room_id,
                    RoomStatus.ERROR,
                    error=f"FFmpeg 连续重试 5 次仍失败；{delay} 秒后恢复常规监控",
                )
            self.retryRequested.emit(room_id, delay)
        self.rooms.update_recording_progress(room_id, 0, total_bytes)
        self.recordingCompleted.emit()

    @Slot(str, str, object, bool, object)
    def _conversion_finished(
        self,
        room_id: str,
        recording_id: str,
        session_dir: Path,
        pause_monitoring: bool,
        result: ConversionResult,
    ) -> None:
        self.converting_rooms.discard(room_id)
        self.database.finish_recording(
            recording_id,
            datetime.now().astimezone(),
            "completed",
            result.total_bytes,
            result.error,
        )
        self._start_probe(recording_id, session_dir)
        self.retry_counts.pop(room_id, None)
        self.session_groups.pop(room_id, None)
        self.recovery_indices.pop(room_id, None)
        if pause_monitoring:
            self.rooms.set_room_enabled(room_id, False)
            if result.error:
                self.rooms.update_room_state(
                    room_id, RoomStatus.DISABLED, error=result.error
                )
        elif result.success:
            self.rooms.update_room_state(room_id, RoomStatus.OFFLINE)
        else:
            self.rooms.update_room_state(room_id, RoomStatus.ERROR, error=result.error)
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
