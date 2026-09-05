from __future__ import annotations

from dataclasses import asdict, dataclass, field
from datetime import datetime
from enum import StrEnum
from pathlib import Path
from typing import Any
from uuid import uuid4


class RoomStatus(StrEnum):
    DISABLED = "disabled"
    CHECKING = "checking"
    OFFLINE = "offline"
    PREPARING = "preparing"
    RECORDING = "recording"
    STALLED = "stalled"
    CONVERTING = "converting"
    RETRYING = "retrying"
    ERROR = "error"


class RecordingSessionState(StrEnum):
    """Lifecycle states for one logical live broadcast."""

    ACTIVE = "active"
    COMPLETED = "completed"
    FAILED = "failed"
    ABANDONED = "abandoned"


class Platform(StrEnum):
    DOUYIN = "douyin"
    KUAISHOU = "kuaishou"
    BILIBILI = "bilibili"
    XIAOHONGSHU = "xiaohongshu"
    TIKTOK = "tiktok"
    YOUTUBE = "youtube"
    TAOBAO = "taobao"
    JD = "jd"
    TWITCH = "twitch"
    SOOP = "soop"
    CHZZK = "chzzk"
    TWITCASTING = "twitcasting"
    SHOWROOM = "showroom"
    BIGO = "bigo"
    LIVE17 = "17live"
    LIVEME = "liveme"
    PICARTO = "picarto"
    SHOPEE = "shopee"
    UNKNOWN = "unknown"


@dataclass(slots=True)
class Room:
    url: str
    platform: Platform = Platform.UNKNOWN
    streamer_name: str = "待识别主播"
    title: str = ""
    id: str = field(default_factory=lambda: str(uuid4()))
    enabled: bool = True
    status: RoomStatus = RoomStatus.OFFLINE
    quality: str = "原画"
    line: str = "线路1"
    file_name: str = ""
    save_root: str = ""
    output_format: str = "ts"
    segment_enabled: bool = False
    segment_minutes: int | None = None
    convert_to_mp4: bool = True
    audio_only: bool = False
    record_danmaku: bool = False
    proxy: str = ""
    check_interval_seconds: int = 300
    last_error: str = ""

    def to_record(self) -> dict[str, Any]:
        data = asdict(self)
        data["platform"] = self.platform.value
        data["status"] = self.status.value
        data["enabled"] = int(self.enabled)
        data["segment_enabled"] = int(self.segment_enabled)
        data["convert_to_mp4"] = int(self.convert_to_mp4)
        data["audio_only"] = int(self.audio_only)
        data["record_danmaku"] = int(self.record_danmaku)
        return data

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> Room:
        values = dict(record)
        values["platform"] = Platform(values.get("platform", Platform.UNKNOWN.value))
        values["status"] = RoomStatus(values.get("status", RoomStatus.OFFLINE.value))
        for key in (
            "enabled",
            "segment_enabled",
            "convert_to_mp4",
            "audio_only",
            "record_danmaku",
        ):
            values[key] = bool(values.get(key))
        return cls(**values)


@dataclass(slots=True)
class RecordingSession:
    """The logical broadcast that may contain several FFmpeg attempts."""

    session_id: str
    room_id: str
    started_at: datetime
    session_dir: Path
    attempt: int = 0
    last_stream_url: str = field(default="", repr=False, compare=False)
    state: RecordingSessionState = RecordingSessionState.ACTIVE
    recovery_reason: str = ""

    def __post_init__(self) -> None:
        if not self.session_id:
            raise ValueError("session_id must not be empty")
        if not self.room_id:
            raise ValueError("room_id must not be empty")
        if self.attempt < 0:
            raise ValueError("attempt must not be negative")
        self.state = RecordingSessionState(self.state)
        self.session_dir = Path(self.session_dir)

    def to_record(self) -> dict[str, Any]:
        """Return only durable fields; transient stream URLs stay in memory."""

        return {
            "session_id": self.session_id,
            "room_id": self.room_id,
            "started_at": self.started_at.isoformat(),
            "session_dir": str(self.session_dir),
            "attempt": self.attempt,
            "state": self.state.value,
            "recovery_reason": self.recovery_reason,
        }

    @classmethod
    def from_record(cls, record: dict[str, Any]) -> RecordingSession:
        values = dict(record)
        if "session_id" not in values and "id" in values:
            values["session_id"] = values.pop("id")
        started_at = values.get("started_at")
        if isinstance(started_at, str):
            values["started_at"] = datetime.fromisoformat(started_at)
        values["session_dir"] = Path(values.get("session_dir", ""))
        values["state"] = RecordingSessionState(
            values.get("state", RecordingSessionState.ACTIVE.value)
        )
        values["attempt"] = int(values.get("attempt", 0))
        return cls(**values)


@dataclass(slots=True, frozen=True)
class RecordingPlan:
    room_id: str
    stream_url: str
    ffmpeg_path: Path
    session_dir: Path
    command: tuple[str, ...]
    output_pattern: Path

