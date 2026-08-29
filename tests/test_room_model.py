from reco_box.domain import Platform, Room
from reco_box.room_model import RoomListModel
from reco_box.storage import Database
from reco_box.view_models import SettingsController


def test_edit_room_segment_settings(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(
        url="https://live.bilibili.com/6",
        platform=Platform.BILIBILI,
        save_root=str(tmp_path / "old"),
    )
    database.upsert_room(room)
    model = RoomListModel(database)

    error = model.updateRoom(
        room.id,
        "新主播",
        "新标题",
        room.url,
        "我的录像",
        "60",
        str(tmp_path / "new"),
        "127.0.0.1:7890",
        "mkv",
        "高清",
        "线路2",
        True,
        "5",
        False,
        False,
        True,
    )

    updated = database.list_rooms()[0]
    assert error == ""
    assert updated.streamer_name == "新主播"
    assert updated.title == "新标题"
    assert updated.file_name == "我的录像"
    assert updated.check_interval_seconds == 60
    assert updated.proxy == "http://127.0.0.1:7890"
    assert updated.line == "线路2"
    assert updated.segment_enabled is True
    assert updated.segment_minutes == 5
    assert updated.output_format == "mkv"
    assert updated.record_danmaku is True


def test_edit_room_rejects_invalid_segment_minutes(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", save_root=str(tmp_path))
    database.upsert_room(room)
    model = RoomListModel(database)

    error = model.updateRoom(
        room.id,
        "主播",
        "",
        room.url,
        "",
        "300",
        str(tmp_path),
        "",
        "ts",
        "原画",
        "线路1",
        True,
        "0",
        False,
        False,
        False,
    )

    assert error == "分段分钟数必须是正整数"
    assert database.list_rooms()[0].segment_enabled is False


def test_new_room_inherits_confirmed_default_segment_settings(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    settings = SettingsController(database)
    error = settings.saveDefaults(
        str(tmp_path / "records"),
        "ts",
        "原画",
        "300",
        True,
        "5",
        "1",
        "127.0.0.1:7890",
    )
    model = RoomListModel(database)

    added = model.addRoom("https://live.bilibili.com/6", "主播", "")
    room = database.list_rooms()[0]

    assert error == ""
    assert added is True
    assert database.get_setting("default_segment_enabled") == "1"
    assert database.get_setting("default_proxy") == "http://127.0.0.1:7890"
    assert room.segment_enabled is True
    assert room.segment_minutes == 5
    assert room.proxy == "http://127.0.0.1:7890"


def test_proxy_rejects_credentials(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    settings = SettingsController(database)
    error = settings.saveDefaults(
        str(tmp_path / "records"), "ts", "原画", "300", False, "5", "1",
        "http://user:secret@127.0.0.1:7890",
    )
    assert "账号密码" in error


def test_existing_database_without_proxy_column_is_upgraded(tmp_path) -> None:
    import sqlite3

    path = tmp_path / "legacy.db"
    connection = sqlite3.connect(path)
    connection.execute(
        "CREATE TABLE rooms (id TEXT PRIMARY KEY, url TEXT NOT NULL UNIQUE, "
        "platform TEXT NOT NULL, streamer_name TEXT NOT NULL, title TEXT NOT NULL DEFAULT '', "
        "enabled INTEGER NOT NULL DEFAULT 1, status TEXT NOT NULL DEFAULT 'offline', "
        "quality TEXT NOT NULL DEFAULT '原画', line TEXT NOT NULL DEFAULT '线路1', "
        "file_name TEXT NOT NULL DEFAULT '', save_root TEXT NOT NULL DEFAULT '', "
        "output_format TEXT NOT NULL DEFAULT 'ts', segment_enabled INTEGER NOT NULL DEFAULT 0, "
        "segment_minutes INTEGER, convert_to_mp4 INTEGER NOT NULL DEFAULT 0, "
        "audio_only INTEGER NOT NULL DEFAULT 0, record_danmaku INTEGER NOT NULL DEFAULT 0, "
        "check_interval_seconds INTEGER NOT NULL DEFAULT 300, last_error TEXT NOT NULL DEFAULT '', "
        "archived INTEGER NOT NULL DEFAULT 0, created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP, "
        "updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP)"
    )
    connection.commit()
    connection.close()

    database = Database(path)

    with database.connection() as upgraded:
        columns = {row[1] for row in upgraded.execute("PRAGMA table_info(rooms)")}
    assert "proxy" in columns


def test_recording_progress_keeps_large_byte_counts_and_clamps_negative_values(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", save_root=str(tmp_path))
    database.upsert_room(room)
    model = RoomListModel(database)

    large_recording = 3 * 1024 * 1024 * 1024
    model.update_recording_progress(room.id, 60, large_recording)
    assert model.runtime[room.id] == {"duration": 60, "bytes": large_recording}

    model.update_recording_progress(room.id, -1, -1)
    assert model.runtime[room.id] == {"duration": 0, "bytes": 0}
