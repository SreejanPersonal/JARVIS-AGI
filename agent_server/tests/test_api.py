from __future__ import annotations

import os
import tempfile
import unittest
from pathlib import Path

# Settings are read when app.main is imported.
TEMP_DATA_DIR = tempfile.TemporaryDirectory()
os.environ["DATA_DIR"] = str(Path(TEMP_DATA_DIR.name) / "data")
os.environ["DATABASE_FILE"] = "test-agent.db"

from fastapi.testclient import TestClient  # noqa: E402
from app.main import app  # noqa: E402


class AgentApiTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.client_context = TestClient(app)
        cls.client = cls.client_context.__enter__()

    @classmethod
    def tearDownClass(cls) -> None:
        cls.client_context.__exit__(None, None, None)
        TEMP_DATA_DIR.cleanup()

    def test_profile_and_skill_routes(self) -> None:
        profiles = self.client.get("/api/profiles")
        self.assertEqual(profiles.status_code, 200)
        self.assertEqual(profiles.json()[0]["profile_id"], "owner")

        skills = self.client.get("/api/skills")
        self.assertEqual(skills.status_code, 200)
        self.assertTrue(any(skill["skill_id"] == "web_search" for skill in skills.json()["skills"]))

    def test_enrollment_image_requires_explicit_profile_consent(self) -> None:
        image = "data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAYAAAAfFcSJAAAADUlEQVQIHWP4z8DwHwAFgAI/ScL1jwAAAABJRU5ErkJggg=="
        self.client.post(
            "/api/profiles",
            json={"profile_id": "unenrolled", "display_name": "Unenrolled", "consented": False, "preferences": {}},
        )
        denied = self.client.post(
            "/api/profiles/unenrolled/enrollment-image",
            json={"image_data_url": image, "consented": True},
        )
        self.assertEqual(denied.status_code, 400)
        self.client.post(
            "/api/profiles",
            json={"profile_id": "riley", "display_name": "Riley", "consented": True, "preferences": {}},
        )
        saved = self.client.post(
            "/api/profiles/riley/enrollment-image",
            json={"image_data_url": image, "consented": True},
        )
        self.assertEqual(saved.status_code, 201)
        self.assertIn("riley/enrollment/", saved.json()["relative_path"])

    def test_vault_route_writes_only_to_active_profile(self) -> None:
        create = self.client.post(
            "/api/profiles",
            json={"profile_id": "alex", "display_name": "Alex", "consented": True, "preferences": {}},
        )
        self.assertEqual(create.status_code, 201)
        saved = self.client.post(
            "/api/vault",
            json={"profile_id": "alex", "title": "Test note", "content": "Keep this private.", "category": "notes"},
        )
        self.assertEqual(saved.status_code, 201)
        self.assertEqual(saved.json()["profile_id"], "alex")
        self.assertEqual(self.client.get("/api/vault/owner").json()["files"], [])
        self.assertEqual(len(self.client.get("/api/vault/alex").json()["files"]), 1)


if __name__ == "__main__":
    unittest.main()
