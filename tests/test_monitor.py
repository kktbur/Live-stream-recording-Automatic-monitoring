from reco_box.domain import Room
from reco_box.monitor import MonitoringCoordinator
from reco_box.room_model import RoomListModel
from reco_box.storage import Database


def test_check_all_now_clears_wait_for_every_enabled_room(monkeypatch, tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    first = Room(url="https://live.bilibili.com/1")
    second = Room(url="https://live.bilibili.com/2")
    database.upsert_room(first)
    database.upsert_room(second)
    rooms = RoomListModel(database)
    coordinator = MonitoringCoordinator(rooms, object())
    coordinator.next_check = {first.id: 1000, second.id: 2000}
    ticks: list[bool] = []
    monkeypatch.setattr(coordinator, "_tick", lambda: ticks.append(True))

    coordinator.checkAllNow()

    assert coordinator.next_check == {first.id: 0, second.id: 0}
    assert ticks == [True]
