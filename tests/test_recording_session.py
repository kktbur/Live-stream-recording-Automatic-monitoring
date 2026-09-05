from datetime import UTC, datetime

import pytest

from reco_box.domain import (
    Platform,
    RecordingSession,
    RecordingSessionState,
    Room,
)
from reco_box.storage import Database


def test_recording_session_requires_a_nonnegative_attempt(tmp_path) -> None:
    with pytest.raises(ValueError, match="attempt"):
        RecordingSession(
            session_id="session-1",
            room_id="room-1",
            started_at=datetime(2026, 9, 5, tzinfo=UTC),
            session_dir=tmp_path,
            attempt=-1,
        )


def test_recording_session_round_trip_keeps_transient_stream_url_in_memory(
    tmp_path,
) -> None:
    database = Database(tmp_path / "reco_box.db")
    room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    database.upsert_room(room)
    session = RecordingSession(
        session_id="session-1",
        room_id=room.id,
        started_at=datetime(2026, 9, 5, 9, 8, 7, tzinfo=UTC),
        session_dir=tmp_path / "主播" / "2026-09-05" / "09-08-07",
        attempt=2,
        last_stream_url="memory-only-stream-url",
        state=RecordingSessionState.ACTIVE,
        recovery_reason="stalled",
    )

    database.upsert_recording_session(session)

    loaded = database.get_recording_session("session-1")
    assert loaded is not None
    assert loaded.session_id == session.session_id
    assert loaded.room_id == room.id
    assert loaded.started_at == session.started_at
    assert loaded.session_dir == session.session_dir
    assert loaded.attempt == 2
    assert loaded.state is RecordingSessionState.ACTIVE
    assert loaded.recovery_reason == "stalled"
    assert loaded.last_stream_url == ""
    assert "last_stream_url" not in session.to_record()

    with database.connection() as connection:
        columns = {
            str(row["name"])
            for row in connection.execute("PRAGMA table_info(recording_sessions)")
        }
        row = connection.execute(
            "SELECT recovery_reason FROM recording_sessions WHERE id = ?",
            (session.session_id,),
        ).fetchone()
    assert "last_stream_url" not in columns
    assert row is not None
    assert row["recovery_reason"] == "stalled"


def test_recording_session_updates_and_filters_by_room(tmp_path) -> None:
    database = Database(tmp_path / "reco_box.db")
    first_room = Room(url="https://live.bilibili.com/6", platform=Platform.BILIBILI)
    second_room = Room(url="https://live.bilibili.com/7", platform=Platform.BILIBILI)
    database.upsert_room(first_room)
    database.upsert_room(second_room)

    first = database.create_recording_session(
        first_room.id,
        datetime(2026, 9, 5, 9, 0, tzinfo=UTC),
        tmp_path / "first",
    )
    second = database.create_recording_session(
        second_room.id,
        datetime(2026, 9, 5, 9, 1, tzinfo=UTC),
        tmp_path / "second",
        attempt=1,
    )
    first.state = RecordingSessionState.COMPLETED
    first.recovery_reason = ""
    database.upsert_recording_session(first)

    assert database.get_recording_session(first.session_id).state is RecordingSessionState.COMPLETED
    assert [item.session_id for item in database.list_recording_sessions(first_room.id)] == [
        first.session_id
    ]
    assert [item.session_id for item in database.list_recording_sessions()] == [
        first.session_id,
        second.session_id,
    ]


def test_schema_v7_recreates_recording_session_table(tmp_path) -> None:
    path = tmp_path / "reco_box.db"
    Database(path)
    with Database(path).connection() as connection:
        connection.execute("DROP TABLE recording_sessions")
        connection.execute("DELETE FROM schema_migrations WHERE version = 7")

    upgraded = Database(path)

    with upgraded.connection() as connection:
        table = connection.execute(
            "SELECT name FROM sqlite_master WHERE type = 'table' AND name = 'recording_sessions'"
        ).fetchone()
        migration = connection.execute(
            "SELECT version FROM schema_migrations WHERE version = 7"
        ).fetchone()
        versions = {
            int(row["version"])
            for row in connection.execute(
                "SELECT version FROM schema_migrations ORDER BY version"
            )
        }
    assert table is not None
    assert migration is not None
    assert {5, 6, 7}.issubset(versions)

