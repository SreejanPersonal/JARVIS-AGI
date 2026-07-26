from __future__ import annotations

from typing import Any

from app.db import Database


class MemoryService:
    def __init__(self, database: Database, max_context_chars: int) -> None:
        self.database = database
        self.max_context_chars = max_context_chars

    def context(self, profile_id: str, query: str) -> tuple[list[dict[str, str]], list[dict[str, Any]]]:
        memories = self.database.recall_memories(profile_id, query)
        turns = self.database.recent_turns(profile_id)
        compact_turns: list[dict[str, str]] = []
        remaining = self.max_context_chars
        for turn in reversed(turns):
            cost = len(turn["content"]) + 32
            if cost > remaining:
                continue
            compact_turns.append({"role": turn["role"], "content": turn["content"]})
            remaining -= cost
        compact_turns.reverse()
        return compact_turns, memories

    def remember(self, profile_id: str, content: str, category: str = "note", importance: int = 2) -> dict[str, Any]:
        return self.database.create_memory(profile_id, content, category, importance)
