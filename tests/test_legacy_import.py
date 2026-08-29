import json
from pathlib import Path

from reco_box.legacy_import import import_legacy_folder, inspect_legacy_folder
from reco_box.storage import Database


def _legacy_fixture(tmp_path):
    root = tmp_path / "legacy"
    config = root / "config"
    config.mkdir(parents=True)
    (config / "config.ini").write_text(
        """
[录制设置]
直播保存路径(不填则默认)=D:\\旧录制
视频保存格式TS|MKV|FLV|MP4|MP3音频|M4A音频=MP4
原画|超清|高清|标清|流畅=高清
循环时间(秒)=120
分段录制是否开启=是
视频分段时间(秒)=301
录制完成后自动转为MP4格式=否

[Cookie]
抖音Cookie=secret-cookie-must-not-leak
""".strip(),
        encoding="utf-8-sig",
    )
    (config / "URL_config.ini").write_text(
        """
高清,https://live.bilibili.com/6,主播: 测试主播
#https://live.douyin.com/123456
https://www.huya.com/not-in-v1
高清,https://live.bilibili.com/6,重复
""".strip(),
        encoding="utf-8-sig",
    )
    return root


def test_inspect_legacy_folder_redacts_sensitive_values(tmp_path) -> None:
    root = _legacy_fixture(tmp_path)

    inspection = inspect_legacy_folder(root)

    assert inspection.supported == 2
    assert inspection.disabled == 1
    assert inspection.unsupported == 1
    assert inspection.duplicates_in_file == 1
    assert inspection.sensitive_fields_detected == 1
    assert inspection.settings["segment_minutes"] == 6
    assert "secret-cookie" not in inspection.summary()


def test_import_legacy_folder_preserves_source_and_writes_safe_report(tmp_path) -> None:
    root = _legacy_fixture(tmp_path)
    source_before = (root / "config" / "config.ini").read_bytes()
    database = Database(tmp_path / "app-data" / "reco_box.db")

    result = import_legacy_folder(root, database)

    rooms = database.list_rooms()
    assert result.imported == 2
    assert len(rooms) == 2
    assert sum(not room.enabled for room in rooms) == 1
    assert rooms[0].segment_enabled is True
    assert rooms[0].segment_minutes == 6
    assert database.get_setting("default_output_format") == "mp4"
    assert (root / "config" / "config.ini").read_bytes() == source_before
    report = json.loads(Path(result.report_path).read_text(encoding="utf-8"))
    assert report["source_files_modified"] is False
    assert "secret-cookie-must-not-leak" not in json.dumps(report, ensure_ascii=False)
