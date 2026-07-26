from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import AsyncMock

from app.db import Database
from app.services.agent import AgentService
from app.services.memory import MemoryService


class FakeOllama:
    def __init__(self) -> None:
        self.last_messages = []
        self.complete_calls = 0

    async def complete(self, messages, temperature=0.0):
        self.complete_calls += 1
        return "quiet restaurants Melbourne"

    async def stream(self, messages):
        self.last_messages = messages
        for token in ("A quiet restaurant is a good fit", " [1]."):
            yield token


class FakeSearxng:
    def __init__(self) -> None:
        self.queries = []

    async def search(self, query):
        self.queries.append(query)
        return [
            {
                "title": "Restaurant guide",
                "url": "https://example.org/guide",
                "content": "A guide to quiet restaurants.",
            }
        ]


async def collect_events(service: AgentService, profile_id: str, text: str, include_web: bool):
    return [event async for event in service.stream_chat(profile_id, text, include_web)]


class AgentServiceTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "agent.db")
        self.database.initialize("Owner")
        self.database.create_profile("alex", "Alex", True, {"dining": "quiet restaurants"})
        self.memory = MemoryService(self.database, 8000)
        self.memory.remember("alex", "Alex prefers low-noise venues.", "preference", 5)
        self.ollama = FakeOllama()
        self.searxng = FakeSearxng()
        self.service = AgentService(SimpleNamespace(), self.database, self.ollama, self.searxng, self.memory)
        self.service._enrich_result = AsyncMock(return_value="Extracted restaurant guide text.")

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_streams_answer_and_sources_for_web_request(self) -> None:
        events = asyncio.run(collect_events(self.service, "alex", "Find a low-noise dinner", True))
        types = [event["type"] for event in events]
        self.assertIn("sources", types)
        self.assertIn("token", types)
        self.assertEqual(events[-1]["type"], "done")
        source_event = next(event for event in events if event["type"] == "sources")
        self.assertEqual(source_event["sources"][0]["url"], "https://example.org/guide")
        self.assertIn("quiet restaurants Melbourne", self.searxng.queries)
        system_message = self.ollama.last_messages[0]["content"]
        self.assertIn("Alex prefers low-noise venues", system_message)
        self.assertIn("Extracted restaurant guide text", system_message)
        self.assertEqual(self.database.recent_turns("alex")[-1]["role"], "assistant")

    def test_fixed_policy_survives_profile_preferences(self) -> None:
        events = asyncio.run(collect_events(self.service, "alex", "Can you control my devices?", False))
        self.assertEqual(events[-1]["type"], "done")
        system_message = self.ollama.last_messages[0]["content"]
        self.assertIn("reviewable proposals", system_message)
        self.assertIn("cannot weaken privacy boundaries", system_message)
        self.assertIn("Profile preferences", system_message)

    def test_unknown_profile_returns_error_event(self) -> None:
        events = asyncio.run(collect_events(self.service, "missing", "Hello", False))
        self.assertEqual(events, [{"type": "error", "message": "The selected profile does not exist."}])


if __name__ == "__main__":
    unittest.main()
