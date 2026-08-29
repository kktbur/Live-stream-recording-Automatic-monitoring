from __future__ import annotations

import configparser
import json
import re
from dataclasses import dataclass
from datetime import datetime
from pathlib import Path
from typing import Any

from .domain import Platform, Room, RoomStatus
from .platforms import detect_platform
from .storage import Database

QUALITY_VALUES = {"原画", "蓝光", "超清", "高清", "标清", "流畅"}
SENSITIVE_SECTIONS = {"Cookie", "Authorization", "账号密码", "推送配置"}


@dataclass(slots=True)
class LegacyCandidate:
    url: str
    quality: str
    streamer_name: str
    enabled: bool
    platform: Platform


@dataclass(slots=True)
class LegacyInspection:
    source_directory: str
    url_file: str
    config_file: str
    supported: int
    disabled: int
    unsupported: int
    duplicates_in_file: int
    sensitive_fields_detected: int
    settings: dict[str, Any]
    candidates: list[LegacyCandidate]

    def summary(self) -> str:
        segment = "关闭"
        if self.settings.get("segment_enabled"):
            segment = f"每 {self.settings.get('segment_minutes', 0)} 分钟"
        return (
            f"可导入直播间：{self.supported} 个\n"
            f"其中暂停监控：{self.disabled} 个\n"
            f"不属于首批八个平台：{self.unsupported} 个\n"
            f"文件内重复：{self.duplicates_in_file} 个\n"
            f"检测到但不会导入的敏感字段：{self.sensitive_fields_detected} 个\n\n"
            f"旧版默认格式：{self.settings.get('output_format', 'ts').upper()}\n"
            f"旧版默认画质：{self.settings.get('quality', '原画')}\n"
            f"旧版轮询间隔：{self.settings.get('check_interval_seconds', 300)} 秒\n"
            f"旧版分段设置：{segment}"
        )


@dataclass(slots=True)
class LegacyImportResult:
    imported: int
    skipped_existing: int
    skipped_unsupported: int
    disabled_imported: int
    sensitive_fields_skipped: int
    report_path: str

    def summary(self) -> str:
        return (
            f"导入完成：{self.imported} 个\n"
            f"其中暂停监控：{self.disabled_imported} 个\n"
            f"已存在并跳过：{self.skipped_existing} 个\n"
            f"不支持并跳过：{self.skipped_unsupported} 个\n"
            f"敏感字段跳过：{self.sensitive_fields_skipped} 个\n\n"
            f"报告：{self.report_path}"
        )


def inspect_legacy_folder(folder: Path) -> LegacyInspection:
    config_dir = _config_directory(Path(folder))
    url_file = config_dir / "URL_config.ini"
    config_file = config_dir / "config.ini"
    if not url_file.is_file():
        raise ValueError("所选目录中没有找到 config\\URL_config.ini 或 URL_config.ini")

    parser = _read_config(config_file)
    settings = _safe_settings(parser)
    candidates, unsupported, duplicates = _read_candidates(
        url_file, str(settings.get("quality", "原画"))
    )
    sensitive_count = _sensitive_value_count(parser)
    return LegacyInspection(
        source_directory=str(config_dir.parent if config_dir.name.lower() == "config" else config_dir),
        url_file=str(url_file),
        config_file=str(config_file) if config_file.is_file() else "",
        supported=len(candidates),
        disabled=sum(not candidate.enabled for candidate in candidates),
        unsupported=unsupported,
        duplicates_in_file=duplicates,
        sensitive_fields_detected=sensitive_count,
        settings=settings,
        candidates=candidates,
    )


def import_legacy_folder(folder: Path, database: Database) -> LegacyImportResult:
    inspection = inspect_legacy_folder(folder)
    existing_urls = {room.url for room in database.list_rooms()}
    imported = 0
    skipped_existing = 0
    disabled_imported = 0
    settings = inspection.settings
    save_root = str(settings.get("save_root") or database.get_setting("default_save_root"))
    if not save_root:
        save_root = str(Path.home() / "Videos" / "Reco Box")

    for candidate in inspection.candidates:
        if candidate.url in existing_urls:
            skipped_existing += 1
            continue
        room = Room(
            url=candidate.url,
            platform=candidate.platform,
            streamer_name=candidate.streamer_name or "待识别主播",
            enabled=candidate.enabled,
            quality=candidate.quality,
            save_root=save_root,
            output_format=str(settings.get("output_format", "ts")),
            segment_enabled=bool(settings.get("segment_enabled", False)),
            segment_minutes=settings.get("segment_minutes"),
            convert_to_mp4=bool(settings.get("convert_to_mp4", False)),
            audio_only=str(settings.get("output_format", "ts")) in {"mp3", "m4a"},
            check_interval_seconds=int(settings.get("check_interval_seconds", 300)),
        )
        if not candidate.enabled:
            room.status = RoomStatus.DISABLED
            disabled_imported += 1
        existing = database.room_url_state(candidate.url)
        if existing:
            database.restore_room(room, existing[0])
        else:
            database.upsert_room(room)
        existing_urls.add(candidate.url)
        imported += 1

    _store_imported_defaults(database, settings)
    report_dir = database.path.parent / "import-reports"
    report_dir.mkdir(parents=True, exist_ok=True)
    created_at = datetime.now().astimezone()
    report_path = report_dir / f"legacy-import-{created_at:%Y%m%d-%H%M%S}.json"
    report_data = {
        "created_at": created_at.isoformat(),
        "source_directory": inspection.source_directory,
        "imported": imported,
        "disabled_imported": disabled_imported,
        "skipped_existing": skipped_existing,
        "skipped_unsupported": inspection.unsupported,
        "sensitive_fields_skipped": inspection.sensitive_fields_detected,
        "settings_imported": settings,
        "source_files_modified": False,
    }
    report_path.write_text(
        json.dumps(report_data, ensure_ascii=False, indent=2), encoding="utf-8"
    )
    return LegacyImportResult(
        imported=imported,
        skipped_existing=skipped_existing,
        skipped_unsupported=inspection.unsupported,
        disabled_imported=disabled_imported,
        sensitive_fields_skipped=inspection.sensitive_fields_detected,
        report_path=str(report_path),
    )


def _config_directory(folder: Path) -> Path:
    direct = folder / "URL_config.ini"
    nested = folder / "config" / "URL_config.ini"
    if direct.is_file():
        return folder
    if nested.is_file():
        return folder / "config"
    return folder


def _read_config(path: Path) -> configparser.ConfigParser:
    parser = configparser.ConfigParser(interpolation=None)
    if path.is_file():
        parser.read(path, encoding="utf-8-sig")
    return parser


def _read_candidates(path: Path, default_quality: str) -> tuple[list[LegacyCandidate], int, int]:
    candidates: list[LegacyCandidate] = []
    seen: set[str] = set()
    unsupported = 0
    duplicates = 0
    for original in path.read_text(encoding="utf-8-sig", errors="replace").splitlines():
        line = original.strip()
        if not line or len(line) < 8:
            continue
        enabled = not line.startswith("#")
        line = line.lstrip("#").strip()
        parts = [part.strip() for part in re.split("[,，]", line, maxsplit=2)]
        quality = default_quality if default_quality in QUALITY_VALUES else "原画"
        name = ""
        if len(parts) == 1:
            url = parts[0]
        elif parts[0].startswith(("http://", "https://")):
            url = parts[0]
            name = parts[1] if len(parts) > 1 else ""
        else:
            quality = parts[0] if parts[0] in QUALITY_VALUES else "原画"
            url = parts[1] if len(parts) > 1 else ""
            name = parts[2] if len(parts) > 2 else ""
        if url and "://" not in url:
            url = "https://" + url
        name = re.sub(r"^主播:\s*", "", name).strip()
        platform = detect_platform(url)
        if platform is Platform.UNKNOWN:
            unsupported += 1
            continue
        if url in seen:
            duplicates += 1
            continue
        seen.add(url)
        candidates.append(LegacyCandidate(url, quality, name, enabled, platform))
    return candidates, unsupported, duplicates


def _safe_settings(parser: configparser.ConfigParser) -> dict[str, Any]:
    section = parser["录制设置"] if parser.has_section("录制设置") else {}
    raw_format = str(section.get("视频保存格式TS|MKV|FLV|MP4|MP3音频|M4A音频", "TS"))
    output_format = next(
        (value for value in ("m4a", "mp3", "mp4", "mkv", "flv", "ts") if value in raw_format.lower()),
        "ts",
    )
    quality = str(section.get("原画|超清|高清|标清|流畅", "原画")).strip()
    if quality not in QUALITY_VALUES:
        quality = "原画"
    interval = _positive_int(section.get("循环时间(秒)", "300"), 300)
    segment_enabled = _is_yes(section.get("分段录制是否开启", "否"))
    segment_seconds = _positive_int(section.get("视频分段时间(秒)", "1800"), 1800)
    return {
        "save_root": str(section.get("直播保存路径(不填则默认)", "")).strip(),
        "output_format": output_format,
        "quality": quality,
        "check_interval_seconds": interval,
        "segment_enabled": segment_enabled,
        "segment_minutes": max(1, (segment_seconds + 59) // 60) if segment_enabled else None,
        "convert_to_mp4": _is_yes(section.get("录制完成后自动转为MP4格式", "否")),
        "minimum_free_gb": _positive_int(section.get("录制空间剩余阈值(GB)", "5"), 5),
    }


def _store_imported_defaults(database: Database, settings: dict[str, Any]) -> None:
    mapping = {
        "default_output_format": settings.get("output_format", "ts"),
        "default_quality": settings.get("quality", "原画"),
        "default_check_interval_seconds": settings.get("check_interval_seconds", 300),
        "default_segment_enabled": int(bool(settings.get("segment_enabled", False))),
        "default_segment_minutes": settings.get("segment_minutes") or 5,
        "minimum_free_gb": settings.get("minimum_free_gb", 5),
    }
    if settings.get("save_root"):
        mapping["default_save_root"] = settings["save_root"]
    for key, value in mapping.items():
        database.set_setting(key, str(value))


def _sensitive_value_count(parser: configparser.ConfigParser) -> int:
    count = 0
    for section_name in SENSITIVE_SECTIONS:
        if not parser.has_section(section_name):
            continue
        count += sum(bool(value.strip()) for value in parser[section_name].values())
    return count


def _positive_int(value: object, default: int) -> int:
    try:
        parsed = int(str(value).strip())
    except ValueError:
        return default
    return parsed if parsed > 0 else default


def _is_yes(value: object) -> bool:
    return str(value).strip().lower() in {"是", "yes", "true", "1", "on"}
