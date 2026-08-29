from reco_box.domain import Room, RoomStatus
from reco_box.room_model import RoomFilterProxyModel, RoomListModel
from reco_box.storage import Database


def _names(proxy: RoomFilterProxyModel) -> list[str]:
    role = RoomListModel.NameRole
    return [str(proxy.data(proxy.index(row, 0), role)) for row in range(proxy.rowCount())]


def test_filter_search_and_sort_rooms(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    database.upsert_room(Room(url="https://live.bilibili.com/1", streamer_name="Beta", title="眼镜专场", status=RoomStatus.RECORDING))
    database.upsert_room(Room(url="https://live.bilibili.com/2", streamer_name="Alpha", enabled=False, status=RoomStatus.DISABLED))
    source = RoomListModel(database)
    proxy = RoomFilterProxyModel(source)

    proxy.setStatusFilter("录制中")
    assert _names(proxy) == ["Beta"]
    proxy.setStatusFilter("全部状态")
    proxy.setSearchText("眼镜")
    assert _names(proxy) == ["Beta"]
    proxy.setSearchText("")
    proxy.setSortMode("名称正序")
    assert _names(proxy) == ["Alpha", "Beta"]


def test_remove_all_rejects_busy_room_then_archives_idle_rooms(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    busy = Room(url="https://live.bilibili.com/1", status=RoomStatus.RECORDING)
    idle = Room(url="https://live.bilibili.com/2")
    database.upsert_room(busy)
    database.upsert_room(idle)
    model = RoomListModel(database)

    assert "正在录制" in model.removeAllRooms()
    model.update_room_state(busy.id, RoomStatus.DISABLED)
    assert model.removeAllRooms() == ""
    assert model.count == 0
    assert database.list_rooms() == []
