from __future__ import annotations

import json
import sqlite3
import uuid
from contextlib import contextmanager
from datetime import UTC, datetime
from pathlib import Path
from typing import Any, Iterator


def utc_now() -> str:
    return datetime.now(UTC).isoformat()


class Database:
    def __init__(self, path: Path) -> None:
        self.path = path

    @contextmanager
    def connect(self) -> Iterator[sqlite3.Connection]:
        connection = sqlite3.connect(self.path)
        connection.row_factory = sqlite3.Row
        connection.execute("PRAGMA foreign_keys = ON")
        connection.execute("PRAGMA journal_mode = WAL")
        try:
            yield connection
            connection.commit()
        finally:
            connection.close()

    def initialize(self, owner_name: str) -> None:
        with self.connect() as db:
            db.executescript(
                """
                CREATE TABLE IF NOT EXISTS profiles (
                    profile_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    consented INTEGER NOT NULL DEFAULT 0,
                    preferences_json TEXT NOT NULL DEFAULT '{}',
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    profile_id TEXT NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
                    role TEXT NOT NULL CHECK(role IN ('user', 'assistant', 'system')),
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_conversations_profile_created
                    ON conversations(profile_id, created_at DESC);
                CREATE TABLE IF NOT EXISTS memories (
                    memory_id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
                    category TEXT NOT NULL,
                    content TEXT NOT NULL,
                    importance INTEGER NOT NULL DEFAULT 2,
                    created_at TEXT NOT NULL,
                    last_accessed_at TEXT NOT NULL
                );
                CREATE INDEX IF NOT EXISTS idx_memories_profile_importance
                    ON memories(profile_id, importance DESC, created_at DESC);
                CREATE TABLE IF NOT EXISTS action_rules (
                    rule_id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
                    action_type TEXT NOT NULL,
                    display_name TEXT NOT NULL,
                    allowed_targets_json TEXT NOT NULL,
                    expires_at TEXT,
                    enabled INTEGER NOT NULL DEFAULT 1,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS actions (
                    action_id TEXT PRIMARY KEY,
                    profile_id TEXT NOT NULL REFERENCES profiles(profile_id) ON DELETE CASCADE,
                    action_type TEXT NOT NULL,
                    summary TEXT NOT NULL,
                    payload_json TEXT NOT NULL,
                    status TEXT NOT NULL,
                    requires_confirmation INTEGER NOT NULL,
                    reason TEXT NOT NULL,
                    rule_id TEXT,
                    created_at TEXT NOT NULL,
                    expires_at TEXT
                );
                CREATE INDEX IF NOT EXISTS idx_actions_profile_created
                    ON actions(profile_id, created_at DESC);
                CREATE TABLE IF NOT EXISTS audit_events (
                    event_id TEXT PRIMARY KEY,
                    profile_id TEXT,
                    event_type TEXT NOT NULL,
                    details_json TEXT NOT NULL,
                    created_at TEXT NOT NULL
                );
                CREATE TABLE IF NOT EXISTS skills (
                    skill_id TEXT PRIMARY KEY,
                    display_name TEXT NOT NULL,
                    description TEXT NOT NULL,
                    category TEXT NOT NULL,
                    enabled INTEGER NOT NULL DEFAULT 0,
                    requires_configuration INTEGER NOT NULL DEFAULT 0,
                    updated_at TEXT NOT NULL
                );
                """
            )
            db.execute(
                """
                INSERT INTO profiles(profile_id, display_name, consented, preferences_json, created_at)
                VALUES ('owner', ?, 1, '{}', ?)
                ON CONFLICT(profile_id) DO NOTHING
                """,
                (owner_name, utc_now()),
            )

    def create_profile(
        self, profile_id: str, display_name: str, consented: bool, preferences: dict[str, Any]
    ) -> dict[str, Any]:
        created_at = utc_now()
        with self.connect() as db:
            db.execute(
                """
                INSERT INTO profiles(profile_id, display_name, consented, preferences_json, created_at)
                VALUES (?, ?, ?, ?, ?)
                """,
                (profile_id, display_name, int(consented), json.dumps(preferences), created_at),
            )
        return self.get_profile(profile_id) or {}

    def get_profile(self, profile_id: str) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute("SELECT * FROM profiles WHERE profile_id = ?", (profile_id,)).fetchone()
        return self._profile_dict(row) if row else None

    def list_profiles(self) -> list[dict[str, Any]]:
        with self.connect() as db:
            rows = db.execute("SELECT * FROM profiles ORDER BY created_at ASC").fetchall()
        return [self._profile_dict(row) for row in rows]

    def save_turn(self, profile_id: str, role: str, content: str) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO conversations(profile_id, role, content, created_at) VALUES (?, ?, ?, ?)",
                (profile_id, role, content, utc_now()),
            )

    def recent_turns(self, profile_id: str, limit: int = 12) -> list[dict[str, str]]:
        with self.connect() as db:
            rows = db.execute(
                """
                SELECT role, content, created_at FROM conversations
                WHERE profile_id = ? ORDER BY id DESC LIMIT ?
                """,
                (profile_id, limit),
            ).fetchall()
        return [dict(row) for row in reversed(rows)]

    def create_memory(self, profile_id: str, content: str, category: str, importance: int) -> dict[str, Any]:
        memory_id = uuid.uuid4().hex
        now = utc_now()
        with self.connect() as db:
            db.execute(
                """
                INSERT INTO memories(memory_id, profile_id, category, content, importance, created_at, last_accessed_at)
                VALUES (?, ?, ?, ?, ?, ?, ?)
                """,
                (memory_id, profile_id, category, content, importance, now, now),
            )
        return {"memory_id": memory_id, "profile_id": profile_id, "category": category, "content": content, "importance": importance, "created_at": now}

    def recall_memories(self, profile_id: str, query: str, limit: int = 6) -> list[dict[str, Any]]:
        terms = [term.strip() for term in query.lower().split() if len(term.strip()) > 2][:8]
        where = " OR ".join("lower(content) LIKE ?" for _ in terms)
        parameters: list[Any] = [profile_id]
        sql = "SELECT * FROM memories WHERE profile_id = ?"
        if where:
            sql += f" AND ({where})"
            parameters.extend(f"%{term}%" for term in terms)
        sql += " ORDER BY importance DESC, last_accessed_at DESC LIMIT ?"
        parameters.append(limit)
        with self.connect() as db:
            rows = db.execute(sql, parameters).fetchall()
            if rows:
                now = utc_now()
                db.executemany(
                    "UPDATE memories SET last_accessed_at = ? WHERE memory_id = ?",
                    [(now, row["memory_id"]) for row in rows],
                )
        return [dict(row) for row in rows]

    def create_action_rule(
        self,
        rule_id: str,
        profile_id: str,
        action_type: str,
        display_name: str,
        allowed_targets: list[str],
        expires_at: str | None,
        enabled: bool,
    ) -> dict[str, Any]:
        created_at = utc_now()
        with self.connect() as db:
            db.execute(
                """
                INSERT INTO action_rules(rule_id, profile_id, action_type, display_name, allowed_targets_json, expires_at, enabled, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                ON CONFLICT(rule_id) DO UPDATE SET
                    display_name = excluded.display_name,
                    allowed_targets_json = excluded.allowed_targets_json,
                    expires_at = excluded.expires_at,
                    enabled = excluded.enabled
                """,
                (rule_id, profile_id, action_type, display_name, json.dumps(allowed_targets), expires_at, int(enabled), created_at),
            )
        return self.get_action_rule(rule_id) or {}

    def get_action_rule(self, rule_id: str) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute("SELECT * FROM action_rules WHERE rule_id = ?", (rule_id,)).fetchone()
        if not row:
            return None
        record = dict(row)
        record["allowed_targets"] = json.loads(record.pop("allowed_targets_json"))
        record["enabled"] = bool(record["enabled"])
        return record

    def create_action(
        self,
        profile_id: str,
        action_type: str,
        summary: str,
        payload: dict[str, Any],
        status: str,
        requires_confirmation: bool,
        reason: str,
        rule_id: str | None = None,
        expires_at: str | None = None,
    ) -> dict[str, Any]:
        action_id = uuid.uuid4().hex
        created_at = utc_now()
        with self.connect() as db:
            db.execute(
                """
                INSERT INTO actions(action_id, profile_id, action_type, summary, payload_json, status,
                    requires_confirmation, reason, rule_id, created_at, expires_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """,
                (action_id, profile_id, action_type, summary, json.dumps(payload), status, int(requires_confirmation), reason, rule_id, created_at, expires_at),
            )
        return self.get_action(action_id) or {}

    def get_action(self, action_id: str) -> dict[str, Any] | None:
        with self.connect() as db:
            row = db.execute("SELECT * FROM actions WHERE action_id = ?", (action_id,)).fetchone()
        return self._action_dict(row) if row else None

    def set_action_status(self, action_id: str, status: str) -> dict[str, Any] | None:
        with self.connect() as db:
            db.execute("UPDATE actions SET status = ? WHERE action_id = ?", (status, action_id))
        return self.get_action(action_id)

    def audit(self, event_type: str, details: dict[str, Any], profile_id: str | None = None) -> None:
        with self.connect() as db:
            db.execute(
                "INSERT INTO audit_events(event_id, profile_id, event_type, details_json, created_at) VALUES (?, ?, ?, ?, ?)",
                (uuid.uuid4().hex, profile_id, event_type, json.dumps(details), utc_now()),
            )

    def seed_skills(self, skills: list[dict[str, Any]]) -> None:
        now = utc_now()
        with self.connect() as db:
            db.executemany(
                """
                INSERT INTO skills(skill_id, display_name, description, category, enabled, requires_configuration, updated_at)
                VALUES (:skill_id, :display_name, :description, :category, :enabled, :requires_configuration, :updated_at)
                ON CONFLICT(skill_id) DO UPDATE SET
                    display_name = excluded.display_name,
                    description = excluded.description,
                    category = excluded.category,
                    requires_configuration = excluded.requires_configuration
                """,
                [
                    {
                        **skill,
                        "enabled": int(skill.get("enabled", False)),
                        "requires_configuration": int(skill.get("requires_configuration", False)),
                        "updated_at": now,
                    }
                    for skill in skills
                ],
            )

    def list_skills(self) -> list[dict[str, Any]]:
        with self.connect() as db:
            rows = db.execute("SELECT * FROM skills ORDER BY category, display_name").fetchall()
        records = [dict(row) for row in rows]
        for record in records:
            record["enabled"] = bool(record["enabled"])
            record["requires_configuration"] = bool(record["requires_configuration"])
        return records

    def set_skill_enabled(self, skill_id: str, enabled: bool) -> dict[str, Any] | None:
        with self.connect() as db:
            db.execute("UPDATE skills SET enabled = ?, updated_at = ? WHERE skill_id = ?", (int(enabled), utc_now(), skill_id))
            row = db.execute("SELECT * FROM skills WHERE skill_id = ?", (skill_id,)).fetchone()
        if not row:
            return None
        record = dict(row)
        record["enabled"] = bool(record["enabled"])
        record["requires_configuration"] = bool(record["requires_configuration"])
        return record

    @staticmethod
    def _profile_dict(row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        record["consented"] = bool(record["consented"])
        record["preferences"] = json.loads(record.pop("preferences_json"))
        return record

    @staticmethod
    def _action_dict(row: sqlite3.Row) -> dict[str, Any]:
        record = dict(row)
        record["payload"] = json.loads(record.pop("payload_json"))
        record["requires_confirmation"] = bool(record["requires_confirmation"])
        return record
