from __future__ import annotations

import asyncio
import tempfile
import unittest
from pathlib import Path

from app.db import Database
from app.services.actions import ActionPolicyService
from app.services.tasks import TaskPlanner


class FakePlannerOllama:
    async def complete(self, messages, temperature=0.0):
        return "Gather the details needed to prepare this task."


class TaskPlannerTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "agent.db")
        self.database.initialize("Owner")
        self.planner = TaskPlanner(self.database, FakePlannerOllama(), ActionPolicyService(self.database))

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_message_task_creates_a_confirmation_proposal(self) -> None:
        plan = asyncio.run(self.planner.plan("owner", "Send a message to Ava about dinner at 7."))
        self.assertEqual(plan["action_type"], "message")
        self.assertEqual(plan["proposal"]["status"], "awaiting_confirmation")
        self.assertIn("Gather the details", plan["steps"][0])
        self.assertIn("confirm", plan["note"].lower())

    def test_unmatched_device_task_is_blocked_without_execution(self) -> None:
        plan = asyncio.run(self.planner.plan("owner", "Turn off the lounge lamp."))
        self.assertEqual(plan["action_type"], "device_control")
        self.assertEqual(plan["proposal"]["status"], "blocked")
        self.assertIn("rule", plan["note"].lower())

    def test_research_task_has_no_external_action(self) -> None:
        plan = asyncio.run(self.planner.plan("owner", "Research quiet dinner options nearby."))
        self.assertIsNone(plan["action_type"])
        self.assertIsNone(plan["proposal"])
        self.assertIn("no external action", plan["note"].lower())


if __name__ == "__main__":
    unittest.main()
