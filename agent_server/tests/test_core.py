from __future__ import annotations

import asyncio
import tempfile
import unittest
from types import SimpleNamespace
from datetime import UTC, datetime, timedelta
from pathlib import Path

from app.db import Database
from app.services.actions import ActionPolicyService
from app.services.executor import ActionExecutor
from app.services.memory import MemoryService
from app.services.skills import SkillRegistry
from app.services.vault import ProfileVault


class AgentCoreTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.database = Database(Path(self.temp_dir.name) / "agent.db")
        self.database.initialize("Owner")
        self.actions = ActionPolicyService(self.database)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_memory_is_profile_scoped(self) -> None:
        self.database.create_profile("alex", "Alex", True, {})
        memory = MemoryService(self.database, 8000)
        memory.remember("alex", "Alex prefers quiet restaurants.", "preference", 4)
        self.assertEqual(memory.context("owner", "quiet restaurants")[1], [])
        recalled = memory.context("alex", "quiet restaurants")[1]
        self.assertEqual(len(recalled), 1)
        self.assertIn("quiet restaurants", recalled[0]["content"])

    def test_message_needs_confirmation(self) -> None:
        action = self.actions.propose("owner", "message", "Send a dinner message", {"target": "Ava"}, None)
        self.assertEqual(action["status"], "awaiting_confirmation")
        self.assertTrue(action["requires_confirmation"])
        confirmed = self.actions.confirm(action["action_id"], "Yes, confirm")
        self.assertEqual(confirmed["status"], "confirmed")

    def test_unruled_device_action_is_blocked(self) -> None:
        action = self.actions.propose("owner", "device_control", "Turn off lounge lamp", {"device": "Lounge lamp"}, None)
        self.assertEqual(action["status"], "blocked")
        self.assertFalse(action["requires_confirmation"])

    def test_allowlisted_device_action_is_authorized(self) -> None:
        self.actions.create_rule(
            "lounge-lamp",
            "owner",
            "device_control",
            "Lounge lamp controls",
            ["Lounge lamp"],
            datetime.now(UTC) + timedelta(hours=1),
            True,
        )
        action = self.actions.propose(
            "owner", "device_control", "Turn off lounge lamp", {"device": "Lounge lamp"}, "lounge-lamp"
        )
        self.assertEqual(action["status"], "authorized")
        other = self.actions.propose(
            "owner", "device_control", "Turn off bedroom lamp", {"device": "Bedroom lamp"}, "lounge-lamp"
        )
        self.assertEqual(other["status"], "blocked")

    def test_approved_action_is_not_sent_without_a_configured_connector(self) -> None:
        action = self.actions.propose("owner", "message", "Send a dinner message", {"target": "Ava"}, None)
        confirmed = self.actions.confirm(action["action_id"], "confirm")
        executor = ActionExecutor(SimpleNamespace(action_webhook_url="", action_webhook_token="", request_timeout_seconds=5.0), self.database)
        outcome = asyncio.run(executor.execute(confirmed["action_id"]))
        self.assertEqual(outcome["delivery"]["status"], "connector_unavailable")
        self.assertEqual(outcome["action"]["status"], "connector_unavailable")

    def test_skill_registry_seeds_catalog(self) -> None:
        registry = SkillRegistry(self.database)
        registry.initialize()
        skills = {skill["skill_id"]: skill for skill in registry.list()}
        self.assertTrue(skills["web_search"]["enabled"])
        self.assertFalse(skills["google_drive"]["enabled"])
        self.assertTrue(skills["google_drive"]["requires_configuration"])

    def test_enrollment_image_stays_in_consented_profile_folder(self) -> None:
        self.database.create_profile("alex", "Alex", True, {})
        vault = ProfileVault(SimpleNamespace(data_dir=Path(self.temp_dir.name) / "data"))
        image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL1jwAAAABJRU5ErkJggg=="
        saved = vault.save_enrollment_image("alex", image, "Alex consented profile image")
        image_path = Path(self.temp_dir.name) / "data" / "profiles" / saved["relative_path"]
        self.assertTrue(image_path.exists())
        self.assertIn("alex/enrollment/", saved["relative_path"])
        self.assertFalse((Path(self.temp_dir.name) / "data" / "profiles" / "owner" / "enrollment").exists())

    def test_vault_saves_to_the_active_profile_folder(self) -> None:
        self.database.create_profile("alex", "Alex", True, {})
        vault = ProfileVault(SimpleNamespace(data_dir=Path(self.temp_dir.name) / "data"))
        saved = vault.save_text("alex", "Dinner options", "Try the quiet Italian restaurant.", "plans")
        self.assertTrue((Path(self.temp_dir.name) / "data" / "profiles" / saved["relative_path"]).exists())
        self.assertEqual(vault.list_files("owner"), [])
        self.assertEqual(len(vault.list_files("alex")), 1)


if __name__ == "__main__":
    unittest.main()
