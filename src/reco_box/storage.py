from __future__ import annotations

import sqlite3
from collections.abc import Iterator
from contextlib import contextmanager
from datetime import datetime
from pathlib import Path
from uuid import uuid4

from .domain import RecordingSession, RecordingSessionState, Room
from .errors import safe_error_text

SCHEMA_VERSION = 7


class Database:
    def __init__(self, path: Path):
        self.path = Path(path)
        self.path.parent.mkdir(parents=True, exist_ok=True)
        self._initialize()

    @contextmanager
    def connection(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def _initialize(self) -> None:
        with self.connection() as connection:
            connection.executescript(
                """
                CREATE TABLE IF NOT EXISTS rooms (
                    id TEXT PRIMARY KEY,
                    url TEXT NOT NULL UNIQUE,
                    platform TEXT NOT NULL,
                    streamer_name TEXT NOT NULL,
                    title TEXT NOT NULL DEFAULT '',
                    enabled INTEGER NOT NULL DEFAULT 1,
                    status TEXT NOT NULL DEFAULT 'offline',
                    quality TEXT NOT NULL DEFAULT '原画',
                    line TEXT NOT NULL DEFAULT '线路1',
                    file_name TEXT NOT NULL DEFAULT '',
                    save_root TEXT NOT NULL DEFAULT '',
                    output_format TEXT NOT NULL DEFAULT 'ts',
                    segment_enabled INTEGER NOT NULL DEFAULT 0,
                    segment_minutes INTEGER,
                    convert_to_mp4 INTEGER NOT NULL DEFAULT 0,
                    audio_only INTEGER NOT NULL DEFAULT 0,
                    record_danmaku INTEGER NOT NULL DEFAULT 0,
                    proxy TEXT NOT NULL DEFAULT '',
                    check_interval_seconds INTEGER NOT NULL DEFAULT 300,
                    last_error TEXT NOT NULL DEFAULT '',
                    archived INTEGER NOT NULL DEFAULT 0,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS recordings (
                    id TEXT PRIMARY KEY,
                    room_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    ended_at TEXT,
                    status TEXT NOT NULL,
                    session_dir TEXT NOT NULL,
                    total_bytes INTEGER NOT NULL DEFAULT 0,
                    error_message TEXT NOT NULL DEFAULT '',
                    group_id TEXT NOT NULL DEFAULT '',
                    recovery_index INTEGER NOT NULL DEFAULT 0,
                    probe_status TEXT NOT NULL DEFAULT 'unchecked',
                    duration_seconds REAL NOT NULL DEFAULT 0,
                    codec_summary TEXT NOT NULL DEFAULT '',
                    probe_error TEXT NOT NULL DEFAULT '',
                    FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE RESTRICT
                );

                CREATE TABLE IF NOT EXISTS recording_sessions (
                    id TEXT PRIMARY KEY,
                    room_id TEXT NOT NULL,
                    started_at TEXT NOT NULL,
                    session_dir TEXT NOT NULL,
                    attempt INTEGER NOT NULL DEFAULT 0 CHECK (attempt >= 0),
                    state TEXT NOT NULL DEFAULT 'active',
                    recovery_reason TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE RESTRICT
                );

                CREATE TABLE IF NOT EXISTS app_settings (
                    key TEXT PRIMARY KEY,
                    value TEXT NOT NULL,
                    updated_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );

                CREATE TABLE IF NOT EXISTS room_events (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    room_id TEXT NOT NULL,
                    level TEXT NOT NULL,
                    message TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY(room_id) REFERENCES rooms(id) ON DELETE CASCADE
                );

                CREATE TABLE IF NOT EXISTS schema_migrations (
                    version INTEGER PRIMARY KEY,
                    applied_at TEXT NOT NULL DEFAULT CURRENT_TIMESTAMP
                );
                """
            )
            room_columns = {
                str(row["name"]) for row in connection.execute("PRAGMA table_info(rooms)")
            }
            if "archived" not in room_columns:
                connection.execute(
                    "ALTER TABLE rooms ADD COLUMN archived INTEGER NOT NULL DEFAULT 0"
                )
            if "file_name" not in room_columns:
                connection.execute(
                    "ALTER TABLE rooms ADD COLUMN file_name TEXT NOT NULL DEFAULT ''"
                )
            if "proxy" not in room_columns:
                connection.execute(
                    "ALTER TABLE rooms ADD COLUMN proxy TEXT NOT NULL DEFAULT ''"
                )
            recording_columns = {
                str(row["name"]) for row in connection.execute("PRAGMA table_info(recordings)")
            }
            if "group_id" not in recording_columns:
                connection.execute(
                    "ALTER TABLE recordings ADD COLUMN group_id TEXT NOT NULL DEFAULT ''"
                )
            if "recovery_index" not in recording_columns:
                connection.execute(
                    "ALTER TABLE recordings ADD COLUMN recovery_index INTEGER NOT NULL DEFAULT 0"
                )
            if "probe_status" not in recording_columns:
                connection.execute(
                    "ALTER TABLE recordings ADD COLUMN probe_status TEXT NOT NULL DEFAULT 'unchecked'"
                )
            if "duration_seconds" not in recording_columns:
                connection.execute(
                    "ALTER TABLE recordings ADD COLUMN duration_seconds REAL NOT NULL DEFAULT 0"
                )
            if "codec_summary" not in recording_columns:
                connection.execute(
                    "ALTER TABLE recordings ADD COLUMN codec_summary TEXT NOT NULL DEFAULT ''"
                )
            if "probe_error" not in recording_columns:
                connection.execute(
                    "ALTER TABLE recordings ADD COLUMN probe_error TEXT NOT NULL DEFAULT ''"
                )
            applied_versions = {
                int(row["version"])
                for row in connection.execute("SELECT version FROM schema_migrations")
            }
            if 5 not in applied_versions:
                # 0.1.0 exposed no working conversion control even though users
                # expected durable MP4 output. Upgrade existing video/TS rooms to
                # the safe record-as-TS, then remux-to-MP4 workflow.
                connection.execute(
                    "UPDATE rooms SET convert_to_mp4 = 1 "
                    "WHERE output_format = 'ts' AND audio_only = 0"
                )
                connection.execute(
                    "INSERT INTO schema_migrations(version) VALUES (?)",
                    (5,),
                )
            if 6 not in applied_versions:
                connection.execute(
                    "UPDATE rooms SET line = '线路1' WHERE line = '自动' OR line = ''"
                )
                connection.execute(
                    "INSERT INTO schema_migrations(version) VALUES (?)",
                    (6,),
                )
            if SCHEMA_VERSION not in applied_versions:
                # The idempotent schema bootstrap creates this table for both
                # new and existing databases; version 7 records that durable
                # RecordingSession storage is available.
                connection.execute(
                    "INSERT INTO schema_migrations(version) VALUES (?)",
                    (SCHEMA_VERSION,),
                )

    def list_rooms(self) -> list[Room]:
        with self.connection() as connection:
            rows = connection.execute(
                """
                SELECT id, url, platform, streamer_name, title, enabled, status,
                       quality, line, file_name, save_root, output_format, segment_enabled,
                       segment_minutes, convert_to_mp4, audio_only, record_danmaku,
                       proxy, check_interval_seconds, last_error
                FROM rooms
                WHERE archived = 0
                ORDER BY created_at ASC
                """
            ).fetchall()
        return [Room.from_record(dict(row)) for row in rows]

    def upsert_room(self, room: Room) -> None:
        record = room.to_record()
        columns = tuple(record)
        placeholders = ", ".join("?" for _ in columns)
        updates = ", ".join(f"{name}=excluded.{name}" for name in columns if name != "id")
        with self.connection() as connection:
            connection.execute(
                f"""
                INSERT INTO rooms ({', '.join(columns)}) VALUES ({placeholders})
                ON CONFLICT(id) DO UPDATE SET {updates}, updated_at=CURRENT_TIMESTAMP
                """,
                tuple(record[name] for name in columns),
            )

    def room_url_state(self, url: str) -> tuple[str, bool] | None:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT id, archived FROM rooms WHERE url = ?", (url,)
            ).fetchone()
        return (str(row["id"]), bool(row["archived"])) if row else None

    def restore_room(self, room: Room, existing_id: str) -> None:
        room.id = existing_id
        self.upsert_room(room)
        with self.connection() as connection:
            connection.execute(
                "UPDATE rooms SET archived = 0, updated_at = CURRENT_TIMESTAMP WHERE id = ?",
                (existing_id,),
            )

    def delete_room(self, room_id: str) -> None:
        with self.connection() as connection:
            connection.execute(
                "UPDATE rooms SET archived = 1, enabled = 0, updated_at = CURRENT_TIMESTAMP "
                "WHERE id = ?",
                (room_id,),
            )

    def upsert_recording_session(self, session: RecordingSession) -> None:
        record = session.to_record()
        with self.connection() as connection:
            connection.execute(
                """
                INSERT INTO recording_sessions(
                    id, room_id, started_at, session_dir, attempt, state, recovery_reason
                )
                VALUES (?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(id) DO UPDATE SET
                    room_id = excluded.room_id,
                    started_at = excluded.started_at,
                    session_dir = excluded.session_dir,
                    attempt = excluded.attempt,
                    state = excluded.state,
                    recovery_reason = excluded.recovery_reason,
                    updated_at = CURRENT_TIMESTAMP
                """,
                (
                    record["session_id"],
                    record["room_id"],
                    record["started_at"],
                    record["session_dir"],
                    record["attempt"],
                    record["state"],
                    safe_error_text(record["recovery_reason"])
                    if record["recovery_reason"]
                    else "",
                ),
            )

    def create_recording_session(
        self,
        room_id: str,
        started_at: datetime,
        session_dir: Path,
        *,
        attempt: int = 0,
        state: RecordingSessionState = RecordingSessionState.ACTIVE,
        recovery_reason: str = "",
    ) -> RecordingSession:
        session = RecordingSession(
            session_id=str(uuid4()),
            room_id=room_id,
            started_at=started_at,
            session_dir=session_dir,
            attempt=attempt,
            state=state,
            recovery_reason=recovery_reason,
        )
        self.upsert_recording_session(session)
        return session

    def get_recording_session(self, session_id: str) -> RecordingSession | None:
        with self.connection() as connection:
            row = connection.execute(
                """
                SELECT id AS session_id, room_id, started_at, session_dir,
                       attempt, state, recovery_reason
                FROM recording_sessions
                WHERE id = ?
                """,
                (session_id,),
            ).fetchone()
        return RecordingSession.from_record(dict(row)) if row else None

    def list_recording_sessions(
        self, room_id: str | None = None
    ) -> list[RecordingSession]:
        query = """
            SELECT id AS session_id, room_id, started_at, session_dir,
                   attempt, state, recovery_reason
            FROM recording_sessions
        """
        parameters: tuple[str, ...] = ()
        if room_id is not None:
            query += " WHERE room_id = ?"
            parameters = (room_id,)
        query += " ORDER BY started_at ASC, id ASC"
        with self.connection() as connection:
            rows = connection.execute(query, parameters).fetchall()
        return [RecordingSession.from_record(dict(row)) for row in rows]

    def start_recording(
        self,
        room_id: str,
        started_at: datetime,
        session_dir: Path,
        group_id: str = "",
        recovery_index: int = 0,
    ) -> str:
        recording_id = str(uuid4())
        with self.connection() as connection:
            connection.execute(
                """
                INSERT INTO recordings(
                    id, room_id, started_at, status, session_dir, group_id, recovery_index
                )
                VALUES (?, ?, ?, 'recording', ?, ?, ?)
                """,
                (
                    recording_id,
                    room_id,
                    started_at.isoformat(),
                    str(session_dir),
                    group_id,
                    recovery_index,
                ),
            )
        return recording_id

    def finish_recording(
        self,
        recording_id: str,
        ended_at: datetime,
        status: str,
        total_bytes: int,
        error_message: str = "",
    ) -> None:
        safe_error = safe_error_text(error_message) if error_message else ""
        with self.connection() as connection:
            connection.execute(
                """
                UPDATE recordings
                SET ended_at = ?, status = ?, total_bytes = ?, error_message = ?,
                    probe_status = CASE WHEN ? = 'completed' THEN 'pending' ELSE 'unchecked' END
                WHERE id = ?
                """,
                (
                    ended_at.isoformat(),
                    status,
                    total_bytes,
                    safe_error,
                    status,
                    recording_id,
                ),
            )

    def mark_recording_converting(
        self, recording_id: str, ended_at: datetime, total_bytes: int
    ) -> None:
        with self.connection() as connection:
            connection.execute(
                """
                UPDATE recordings
                SET ended_at = ?, status = 'converting', total_bytes = ?,
                    error_message = '', probe_status = 'pending'
                WHERE id = ?
                """,
                (ended_at.isoformat(), total_bytes, recording_id),
            )

    def update_recording_probe(
        self,
        recording_id: str,
        status: str,
        duration_seconds: float,
        codec_summary: str,
        error: str = "",
    ) -> None:
        safe_error = safe_error_text(error) if error else ""
        with self.connection() as connection:
            connection.execute(
                """
                UPDATE recordings
                SET probe_status = ?, duration_seconds = ?, codec_summary = ?, probe_error = ?
                WHERE id = ?
                """,
                (status, duration_seconds, codec_summary[:200], safe_error, recording_id),
            )

    def list_recordings(self, limit: int = 200) -> list[dict[str, object]]:
        with self.connection() as connection:
            rows = connection.execute(
                """
                WITH normalized AS (
                    SELECT recordings.*,
                           CASE WHEN group_id = '' THEN id ELSE group_id END AS group_key
                    FROM recordings
                )
                SELECT normalized.group_key AS id,
                       normalized.room_id,
                       rooms.platform,
                       rooms.streamer_name,
                       rooms.title,
                       MIN(normalized.started_at) AS started_at,
                       CASE WHEN SUM(normalized.status = 'recording') > 0
                            THEN NULL ELSE MAX(normalized.ended_at) END AS ended_at,
                       CASE
                           WHEN SUM(normalized.status = 'recording') > 0 THEN 'recording'
                           WHEN SUM(normalized.status = 'converting') > 0 THEN 'converting'
                           WHEN SUM(normalized.status = 'completed') > 0 THEN 'completed'
                           ELSE 'failed'
                       END AS status,
                       MIN(normalized.session_dir) AS session_dir,
                       GROUP_CONCAT(normalized.session_dir, '|') AS session_dirs,
                       SUM(normalized.total_bytes) AS total_bytes,
                       CASE
                           WHEN SUM(normalized.status = 'recording') > 0
                                OR SUM(normalized.status = 'completed') > 0
                           THEN '' ELSE MAX(normalized.error_message)
                       END AS error_message,
                       COUNT(*) AS recovery_parts,
                       CASE
                           WHEN SUM(normalized.status = 'recording') > 0 THEN 'pending'
                           WHEN SUM(normalized.probe_status = 'pending') > 0 THEN 'pending'
                           WHEN SUM(normalized.probe_status = 'valid') > 0 THEN 'valid'
                           WHEN SUM(normalized.probe_status = 'invalid') > 0 THEN 'invalid'
                           ELSE 'unchecked'
                       END AS probe_status,
                       SUM(normalized.duration_seconds) AS duration_seconds,
                       GROUP_CONCAT(DISTINCT normalized.codec_summary) AS codec_summary,
                       MAX(normalized.probe_error) AS probe_error
                FROM normalized
                JOIN rooms ON rooms.id = normalized.room_id
                GROUP BY normalized.group_key, normalized.room_id
                ORDER BY MIN(normalized.started_at) DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def add_event(self, room_id: str, level: str, message: str) -> None:
        safe_message = safe_error_text(message) if message else ""
        with self.connection() as connection:
            connection.execute(
                "INSERT INTO room_events(room_id, level, message) VALUES (?, ?, ?)",
                (room_id, level, safe_message[:500]),
            )

    def list_events(self, limit: int = 300) -> list[dict[str, object]]:
        with self.connection() as connection:
            rows = connection.execute(
                """
                SELECT room_events.id, room_events.room_id, rooms.streamer_name,
                       room_events.level, room_events.message, room_events.created_at
                FROM room_events
                JOIN rooms ON rooms.id = room_events.room_id
                ORDER BY room_events.id DESC
                LIMIT ?
                """,
                (limit,),
            ).fetchall()
        return [dict(row) for row in rows]

    def get_setting(self, key: str, default: str = "") -> str:
        with self.connection() as connection:
            row = connection.execute(
                "SELECT value FROM app_settings WHERE key = ?", (key,)
            ).fetchone()
        return str(row["value"]) if row else default

    def set_setting(self, key: str, value: str) -> None:
        with self.connection() as connection:
            connection.execute(
                """
                INSERT INTO app_settings(key, value) VALUES (?, ?)
                ON CONFLICT(key) DO UPDATE SET value=excluded.value,
                                               updated_at=CURRENT_TIMESTAMP
                """,
                (key, value),
            )

