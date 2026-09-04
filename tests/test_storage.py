from datetime import datetime

from reco_box.domain import Platform, Room
from reco_box.storage import Database


def test_room_round_trip(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/6",
        platform=Platform.BILIBILI,
        streamer_name="测试主播",
        save_root=str(tmp_path / "records"),
    )
    database.upsert_room(room)
    rooms = database.list_rooms()

    assert len(rooms) == 1
    assert rooms[0].id == room.id
    assert rooms[0].platform is Platform.BILIBILI
    assert rooms[0].segment_enabled is False


def test_recording_history_round_trip(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    database.upsert_room(room)

    started_at = datetime.now().astimezone()
    recording_id = database.start_recording(room.id, started_at, tmp_path / "session")
    database.finish_recording(recording_id, started_at, "completed", 1234)

    with database.connection() as connection:
        record = connection.execute(
            "SELECT status, total_bytes, error_message FROM recordings WHERE id = ?",
            (recording_id,),
        ).fetchone()

    assert record is not None
    assert record["status"] == "completed"
    assert record["total_bytes"] == 1234
    assert record["error_message"] == ""

    history = database.list_recordings()
    assert history[0]["streamer_name"] == "待识别主播"
    assert history[0]["session_dir"] == str(tmp_path / "session")


def test_settings_and_safe_event_log(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    database.upsert_room(room)

    database.set_setting("default_save_root", str(tmp_path / "records"))
    database.add_event(room.id, "info", "状态变更：offline → checking")

    assert database.get_setting("default_save_root") == str(tmp_path / "records")
    assert database.list_events()[0]["message"] == "状态变更：offline → checking"


def test_event_storage_sanitizes_direct_error_messages(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    database.upsert_room(room)

    database.add_event(
        room.id,
        "error",
        "failed /live.m3u8?sig=signature-secret Cookie: first=one; second=two",
    )

    message = database.list_events()[0]["message"]
    assert "signature-secret" not in message
    assert "first=one" not in message
    assert "second=two" not in message


def test_delete_room_keeps_recording_history(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    database.upsert_room(room)
    started_at = datetime.now().astimezone()
    recording_id = database.start_recording(room.id, started_at, tmp_path / "session")
    database.finish_recording(recording_id, started_at, "completed", 99)

    database.delete_room(room.id)

    assert database.list_rooms() == []
    assert database.list_recordings()[0]["id"] == recording_id


def test_recovery_attempts_are_grouped_as_one_history_item(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    database.upsert_room(room)
    started_at = datetime.now().astimezone()
    group_id = "same-live-session"
    first = database.start_recording(
        room.id, started_at, tmp_path / "part-1", group_id=group_id, recovery_index=0
    )
    database.finish_recording(first, started_at, "failed", 100, "network")
    second = database.start_recording(
        room.id, started_at, tmp_path / "part-2", group_id=group_id, recovery_index=1
    )
    database.finish_recording(second, started_at, "completed", 200)
    database.update_recording_probe(second, "valid", 12.5, "video:h264, audio:aac")

    history = database.list_recordings()

    assert len(history) == 1
    assert history[0]["id"] == group_id
    assert history[0]["status"] == "completed"
    assert history[0]["recovery_parts"] == 2
    assert history[0]["total_bytes"] == 300
    assert history[0]["probe_status"] == "valid"
    assert history[0]["duration_seconds"] == 12.5
    assert "video:h264" in history[0]["codec_summary"]
    assert str(tmp_path / "part-1") in history[0]["session_dirs"]
    assert str(tmp_path / "part-2") in history[0]["session_dirs"]


def test_v5_upgrade_enables_mp4_conversion_for_existing_video_ts_rooms(tmp_path) -> None:
    path = tmp_path / "reco_box.db"
    database = Database(path)
    room = Room(url="https://live.bilibili.com/6", convert_to_mp4=False)
    database.upsert_room(room)
    with database.connection() as connection:
        connection.execute("DELETE FROM schema_migrations WHERE version = 5")
        connection.execute("INSERT OR IGNORE INTO schema_migrations(version) VALUES (4)")

    upgraded = Database(path)

    assert upgraded.list_rooms()[0].convert_to_mp4 is True
