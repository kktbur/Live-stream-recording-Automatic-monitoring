from __future__ import annotations

import subprocess
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path

from .domain import RecordingPlan, Room
from .localization import tr
from .output_paths import (
    create_session_directory,
    numbered_single_output_path,
    segment_output_pattern,
)


@dataclass(slots=True, frozen=True)
class StreamInput:
    url: str
    headers: str = ""
    proxy: str = ""


class SessionPathPlanner:
    """Choose and create the stable output directory for one live session."""

    def build(self, room: Room, started_at: datetime) -> Path:
        if not room.save_root:
            raise ValueError(tr("必须先设置录制保存目录"))
        return create_session_directory(
            Path(room.save_root), room.streamer_name, started_at
        )


class FFmpegPlanner:
    def __init__(self, ffmpeg_path: Path):
        self.ffmpeg_path = Path(ffmpeg_path)
        self.session_path_planner = SessionPathPlanner()

    def build(self, room: Room, stream: StreamInput, started_at: datetime) -> RecordingPlan:
        self._validate_room(room)
        session_dir = self.session_path_planner.build(room, started_at)
        return self.build_for_session(room, stream, session_dir)

    def build_for_session(
        self,
        room: Room,
        stream: StreamInput,
        session_dir: Path,
        *,
        start_number: int = 1,
    ) -> RecordingPlan:
        """Build one FFmpeg attempt under a caller-owned session directory."""

        self._validate_room(room)
        if start_number < 1:
            raise ValueError("start_number must be positive")

        session_dir = Path(session_dir)
        output = (
            segment_output_pattern(session_dir, room.output_format)
            if room.segment_enabled
            else numbered_single_output_path(
                session_dir, room.output_format, room.file_name, start_number
            )
        )

        command = [
            str(self.ffmpeg_path),
            "-hide_banner",
            "-y",
            "-reconnect",
            "1",
            "-reconnect_streamed",
            "1",
            "-reconnect_delay_max",
            "10",
            "-rw_timeout",
            "15000000",
        ]
        if stream.proxy:
            command.extend(["-http_proxy", stream.proxy])
        if stream.headers:
            command.extend(["-headers", stream.headers])
        command.extend(["-i", stream.url])

        if room.audio_only:
            command.extend(["-map", "0:a:0", "-vn"])
            if room.output_format == "mp3":
                command.extend(["-c:a", "libmp3lame", "-b:a", "320k"])
            elif room.output_format == "m4a":
                command.extend(["-c:a", "aac", "-b:a", "256k"])
            else:
                command.extend(["-c:a", "copy"])
        else:
            command.extend(["-map", "0:v:0?", "-map", "0:a:0?", "-c", "copy"])

        if room.segment_enabled:
            command.extend(
                [
                    "-f",
                    "segment",
                    "-segment_time",
                    str(room.segment_minutes * 60),
                    "-segment_start_number",
                    str(start_number),
                    "-reset_timestamps",
                    "1",
                ]
            )
        command.append(str(output))
        return RecordingPlan(
            room_id=room.id,
            stream_url=stream.url,
            ffmpeg_path=self.ffmpeg_path,
            session_dir=session_dir,
            command=tuple(command),
            output_pattern=output,
        )

    @staticmethod
    def _validate_room(room: Room) -> None:
        if room.segment_enabled and (room.segment_minutes is None or room.segment_minutes <= 0):
            raise ValueError(tr("分段分钟数必须是正整数"))


def hidden_startup_info() -> subprocess.STARTUPINFO | None:
    if not hasattr(subprocess, "STARTUPINFO"):
        return None
    startup = subprocess.STARTUPINFO()
    startup.dwFlags |= subprocess.STARTF_USESHOWWINDOW
    startup.wShowWindow = subprocess.SW_HIDE
    return startup
