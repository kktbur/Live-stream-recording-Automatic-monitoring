from __future__ import annotations

import sqlite3
from pathlib import Path

from PySide6.QtCore import (
    Property,
    QAbstractListModel,
    QModelIndex,
    QSortFilterProxyModel,
    Qt,
    Signal,
    Slot,
)

from .domain import Room, RoomStatus
from .errors import safe_error_text
from .localization import tr
from .network import normalize_proxy
from .platforms import detect_platform
from .storage import Database


class RoomListModel(QAbstractListModel):
    countChanged = Signal()
    roomAdded = Signal(str)

    IdRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    PlatformRole = Qt.UserRole + 3
    UrlRole = Qt.UserRole + 4
    StatusRole = Qt.UserRole + 5
    EnabledRole = Qt.UserRole + 6
    QualityRole = Qt.UserRole + 7
    ErrorRole = Qt.UserRole + 8
    TitleRole = Qt.UserRole + 9
    SaveRootRole = Qt.UserRole + 10
    FormatRole = Qt.UserRole + 11
    SegmentEnabledRole = Qt.UserRole + 12
    SegmentMinutesRole = Qt.UserRole + 13
    AudioOnlyRole = Qt.UserRole + 14
    DanmakuRole = Qt.UserRole + 15
    DurationRole = Qt.UserRole + 16
    FileBytesRole = Qt.UserRole + 17
    ConvertToMp4Role = Qt.UserRole + 18
    LineRole = Qt.UserRole + 19
    CheckIntervalRole = Qt.UserRole + 20
    FileNameRole = Qt.UserRole + 21
    ProxyRole = Qt.UserRole + 22

    def __init__(self, database: Database):
        super().__init__()
        self.database = database
        self.rooms = database.list_rooms()
        self._normalize_stalled_rooms()
        self.runtime: dict[str, dict[str, int]] = {}

    def _normalize_stalled_rooms(self) -> None:
        """Clear persisted transient stall markers after an application restart."""

        for room in self.rooms:
            if room.status != RoomStatus.STALLED:
                continue
            room.status = RoomStatus.OFFLINE
            self.database.upsert_room(room)

    def roleNames(self) -> dict[int, bytes]:
        return {
            self.IdRole: b"roomId",
            self.NameRole: b"streamerName",
            self.PlatformRole: b"platformName",
            self.UrlRole: b"roomUrl",
            self.StatusRole: b"roomStatus",
            self.EnabledRole: b"roomEnabled",
            self.QualityRole: b"qualityName",
            self.ErrorRole: b"lastError",
            self.TitleRole: b"roomTitle",
            self.SaveRootRole: b"saveRoot",
            self.FormatRole: b"outputFormat",
            self.SegmentEnabledRole: b"segmentEnabled",
            self.SegmentMinutesRole: b"segmentMinutes",
            self.AudioOnlyRole: b"audioOnly",
            self.DanmakuRole: b"recordDanmaku",
            self.DurationRole: b"durationSeconds",
            self.FileBytesRole: b"fileBytes",
            self.ConvertToMp4Role: b"convertToMp4",
            self.LineRole: b"recordingLine",
            self.CheckIntervalRole: b"checkIntervalSeconds",
            self.FileNameRole: b"fileName",
            self.ProxyRole: b"roomProxy",
        }

    def rowCount(self, parent: QModelIndex | None = None) -> int:
        return 0 if parent is not None and parent.isValid() else len(self.rooms)

    @Property(int, notify=countChanged)
    def count(self) -> int:
        return len(self.rooms)

    def data(self, index: QModelIndex, role: int = Qt.DisplayRole):
        if not index.isValid() or not 0 <= index.row() < len(self.rooms):
            return None
        room = self.rooms[index.row()]
        runtime = self.runtime.get(room.id, {})
        values = {
            self.IdRole: room.id,
            self.NameRole: room.streamer_name,
            self.PlatformRole: room.platform.value,
            self.UrlRole: room.url,
            self.StatusRole: room.status.value,
            self.EnabledRole: room.enabled,
            self.QualityRole: room.quality,
            self.ErrorRole: room.last_error,
            self.TitleRole: room.title,
            self.SaveRootRole: room.save_root,
            self.FormatRole: room.output_format,
            self.SegmentEnabledRole: room.segment_enabled,
            self.SegmentMinutesRole: room.segment_minutes or 0,
            self.AudioOnlyRole: room.audio_only,
            self.DanmakuRole: room.record_danmaku,
            self.DurationRole: runtime.get("duration", 0),
            self.FileBytesRole: runtime.get("bytes", 0),
            self.ConvertToMp4Role: room.convert_to_mp4,
            self.LineRole: room.line,
            self.CheckIntervalRole: room.check_interval_seconds,
            self.FileNameRole: room.file_name,
            self.ProxyRole: room.proxy,
        }
        return values.get(role)

    @Slot(str, str, str, result=bool)
    def addRoom(self, url: str, streamer_name: str, save_root: str) -> bool:
        url = url.strip()
        if not url:
            return False
        room = Room(
            url=url,
            platform=detect_platform(url),
            streamer_name=streamer_name.strip() or "待识别主播",
            save_root=save_root.strip()
            or self.database.get_setting(
                "default_save_root", str(Path.home() / "Videos" / "Reco Box")
            ),
            output_format=self.database.get_setting("default_output_format", "ts"),
            quality=self.database.get_setting("default_quality", "原画"),
            segment_enabled=self.database.get_setting("default_segment_enabled", "0") == "1",
            segment_minutes=int(self.database.get_setting("default_segment_minutes", "5")),
            check_interval_seconds=int(
                self.database.get_setting("default_check_interval_seconds", "300")
            ),
            proxy=self.database.get_setting("default_proxy", ""),
        )
        if not room.segment_enabled:
            room.segment_minutes = None
        room.audio_only = room.output_format in {"mp3", "m4a"}
        existing = self.database.room_url_state(url)
        if existing and not existing[1]:
            return False
        try:
            if existing:
                self.database.restore_room(room, existing[0])
            else:
                self.database.upsert_room(room)
        except sqlite3.IntegrityError:
            return False
        row = len(self.rooms)
        self.beginInsertRows(QModelIndex(), row, row)
        self.rooms.append(room)
        self.endInsertRows()
        self.countChanged.emit()
        self.roomAdded.emit(room.id)
        return True

    @Slot(str)
    def toggleRoom(self, room_id: str) -> None:
        room = self.get_room(room_id)
        if room is not None:
            self.set_room_enabled(room_id, not room.enabled)

    def set_room_enabled(self, room_id: str, enabled: bool) -> None:
        for row, room in enumerate(self.rooms):
            if room.id != room_id:
                continue
            room.enabled = enabled
            room.status = RoomStatus.OFFLINE if room.enabled else RoomStatus.DISABLED
            self.database.upsert_room(room)
            index = self.index(row, 0)
            self.dataChanged.emit(index, index, [self.EnabledRole, self.StatusRole])
            return

    @Slot(str)
    def removeRoom(self, room_id: str) -> None:
        for row, room in enumerate(self.rooms):
            if room.id != room_id:
                continue
            self.beginRemoveRows(QModelIndex(), row, row)
            self.database.delete_room(room_id)
            self.rooms.pop(row)
            self.endRemoveRows()
            self.countChanged.emit()
            return

    @Slot(result=str)
    def removeAllRooms(self) -> str:
        busy = {
            RoomStatus.PREPARING,
            RoomStatus.RECORDING,
            RoomStatus.STALLED,
            RoomStatus.CONVERTING,
        }
        if any(room.status in busy for room in self.rooms):
            return tr("仍有直播间正在录制或转换，请先全部暂停并等待收尾完成")
        self.beginResetModel()
        try:
            for room in self.rooms:
                self.database.delete_room(room.id)
            self.rooms.clear()
            self.runtime.clear()
        finally:
            self.endResetModel()
        self.countChanged.emit()
        return ""

    @Slot(bool)
    def setAllEnabled(self, enabled: bool) -> None:
        self.beginResetModel()
        try:
            for room in self.rooms:
                room.enabled = enabled
                if room.status not in {
                    RoomStatus.PREPARING,
                    RoomStatus.RECORDING,
                    RoomStatus.STALLED,
                    RoomStatus.CONVERTING,
                }:
                    room.status = RoomStatus.OFFLINE if enabled else RoomStatus.DISABLED
                self.database.upsert_room(room)
        finally:
            self.endResetModel()

    @Slot()
    def reload(self) -> None:
        self.beginResetModel()
        self.rooms = self.database.list_rooms()
        self.endResetModel()
        self.countChanged.emit()

    @Slot(
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        str,
        bool,
        str,
        bool,
        bool,
        bool,
        result=str,
    )
    def updateRoom(
        self,
        room_id: str,
        streamer_name: str,
        title: str,
        url: str,
        file_name: str,
        check_interval: str,
        save_root: str,
        proxy: str,
        output_format: str,
        quality: str,
        line: str,
        segment_enabled: bool,
        segment_minutes: str,
        convert_to_mp4: bool,
        audio_only: bool,
        record_danmaku: bool,
    ) -> str:
        room = self.get_room(room_id)
        if room is None:
            return tr("找不到直播间")
        normalized_url = url.strip()
        if not normalized_url:
            return tr("直播间地址不能为空")
        existing = self.database.room_url_state(normalized_url)
        if existing and existing[0] != room_id:
            return tr("该直播间地址已经存在")
        root = save_root.strip()
        if not root:
            return tr("保存目录不能为空")
        try:
            normalized_proxy = normalize_proxy(proxy)
        except ValueError as error:
            return str(error)
        try:
            interval = int(check_interval)
        except ValueError:
            return tr("检测间隔必须是正整数")
        if interval < 30:
            return tr("检测间隔不能低于 30 秒")
        minutes: int | None = None
        if segment_enabled:
            try:
                minutes = int(segment_minutes)
            except ValueError:
                return tr("分段分钟数必须是正整数")
            if minutes <= 0:
                return tr("分段分钟数必须是正整数")
        allowed_formats = {"ts", "mp4", "mkv", "flv", "mp3", "m4a"}
        normalized_format = output_format.lower().strip()
        if normalized_format not in allowed_formats:
            return tr("不支持该输出格式")
        room.streamer_name = streamer_name.strip() or "待识别主播"
        room.title = title.strip()
        room.url = normalized_url
        room.platform = detect_platform(normalized_url)
        room.file_name = file_name.strip()
        room.check_interval_seconds = interval
        room.save_root = root
        room.proxy = normalized_proxy
        room.output_format = normalized_format
        room.quality = quality.strip() or "原画"
        room.line = line.strip() or "线路1"
        room.segment_enabled = segment_enabled
        room.segment_minutes = minutes
        room.audio_only = audio_only or normalized_format in {"mp3", "m4a"}
        room.convert_to_mp4 = (
            convert_to_mp4 and normalized_format == "ts" and not room.audio_only
        )
        room.record_danmaku = record_danmaku
        self.database.upsert_room(room)
        row = self.rooms.index(room)
        index = self.index(row, 0)
        self.dataChanged.emit(index, index)
        return ""

    def get_room(self, room_id: str) -> Room | None:
        return next((room for room in self.rooms if room.id == room_id), None)

    def update_room_state(
        self,
        room_id: str,
        status: RoomStatus,
        *,
        streamer_name: str | None = None,
        title: str | None = None,
        error: str = "",
    ) -> None:
        for row, room in enumerate(self.rooms):
            if room.id != room_id:
                continue
            previous_status = room.status
            room.status = status
            safe_error = safe_error_text(error) if error else ""
            room.last_error = safe_error
            if streamer_name and streamer_name != "待识别主播":
                room.streamer_name = streamer_name
            if title:
                room.title = title
            self.database.upsert_room(room)
            if status != previous_status:
                level = (
                    "error"
                    if status in (RoomStatus.ERROR, RoomStatus.RETRYING, RoomStatus.STALLED)
                    else "info"
                )
                message = safe_error or f"状态变更：{previous_status.value} → {status.value}"
                self.database.add_event(room.id, level, message)
            index = self.index(row, 0)
            self.dataChanged.emit(
                index,
                index,
                [self.StatusRole, self.NameRole, self.TitleRole, self.ErrorRole],
            )
            return

    def update_recording_progress(self, room_id: str, duration: int, file_bytes: int) -> None:
        for row, room in enumerate(self.rooms):
            if room.id != room_id:
                continue
            self.runtime[room_id] = {
                "duration": max(0, int(duration)),
                "bytes": max(0, int(file_bytes)),
            }
            index = self.index(row, 0)
            self.dataChanged.emit(index, index, [self.DurationRole, self.FileBytesRole])
            return


class RoomFilterProxyModel(QSortFilterProxyModel):
    countChanged = Signal()

    def __init__(self, source: RoomListModel):
        super().__init__()
        self._status_filter = "all"
        self._search_text = ""
        self._sort_mode = "default"
        self.setSourceModel(source)
        self.setDynamicSortFilter(True)
        source.countChanged.connect(self._refresh)
        source.dataChanged.connect(lambda *_: self._refresh())
        source.modelReset.connect(self._refresh)
        source.rowsInserted.connect(lambda *_: self._refresh())
        source.rowsRemoved.connect(lambda *_: self._refresh())

    @Property(int, notify=countChanged)
    def count(self) -> int:
        return self.rowCount()

    @Slot(str)
    def setStatusFilter(self, value: str) -> None:
        if value == self._status_filter:
            return
        self._status_filter = value
        self._refresh()

    @Slot(str)
    def setSearchText(self, value: str) -> None:
        normalized = value.strip().casefold()
        if normalized == self._search_text:
            return
        self._search_text = normalized
        self._refresh()

    @Slot(str)
    def setSortMode(self, value: str) -> None:
        self._sort_mode = value
        if value == "name_asc":
            self.setSortRole(RoomListModel.NameRole)
            self.sort(0, Qt.SortOrder.AscendingOrder)
        elif value == "name_desc":
            self.setSortRole(RoomListModel.NameRole)
            self.sort(0, Qt.SortOrder.DescendingOrder)
        else:
            self.sort(-1)
        self._refresh()

    def filterAcceptsRow(self, source_row: int, source_parent: QModelIndex) -> bool:
        source = self.sourceModel()
        if source is None:
            return False
        index = source.index(source_row, 0, source_parent)
        status = str(source.data(index, RoomListModel.StatusRole) or "")
        enabled = bool(source.data(index, RoomListModel.EnabledRole))
        if self._status_filter == "recording" and status not in {"recording", "stalled", "converting"}:
            return False
        if self._status_filter == "monitoring" and (
            not enabled or status in {"recording", "stalled", "converting", "disabled"}
        ):
            return False
        if self._status_filter == "not_started" and enabled:
            return False
        if not self._search_text:
            return True
        values = (
            source.data(index, RoomListModel.NameRole),
            source.data(index, RoomListModel.TitleRole),
            source.data(index, RoomListModel.UrlRole),
        )
        return any(self._search_text in str(value or "").casefold() for value in values)

    def lessThan(self, left: QModelIndex, right: QModelIndex) -> bool:
        left_value = str(left.data(self.sortRole()) or "").casefold()
        right_value = str(right.data(self.sortRole()) or "").casefold()
        return left_value < right_value

    def _refresh(self) -> None:
        self.invalidateFilter()
        self.countChanged.emit()
