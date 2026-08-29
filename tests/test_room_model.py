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
    )
    model = RoomListModel(database)

    added = model.addRoom("https://live.bilibili.com/6", "主播", "")
    room = database.list_rooms()[0]

    assert error == ""
    assert added is True
    assert database.get_setting("default_segment_enabled") == "1"
    assert room.segment_enabled is True
    assert room.segment_minutes == 5


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
