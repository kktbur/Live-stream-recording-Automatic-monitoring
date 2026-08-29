from __future__ import annotations

from dataclasses import asdict, dataclass, field
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
    CONVERTING = "converting"
    RETRYING = "retrying"
    ERROR = "error"


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


@dataclass(slots=True, frozen=True)
class RecordingPlan:
    room_id: str
    stream_url: str
    ffmpeg_path: Path
    session_dir: Path
    command: tuple[str, ...]
    output_pattern: Path
