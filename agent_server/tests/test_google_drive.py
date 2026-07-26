from __future__ import annotations

import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace

from app.db import Database
from app.services.google_drive import GoogleDriveMirror
from app.services.vault import ProfileVault


class GoogleDriveMirrorTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temp_dir = tempfile.TemporaryDirectory()
        self.root = Path(self.temp_dir.name)
        self.drive_root = self.root / "drive-mirror"
        self.drive_root.mkdir()
        (self.drive_root / "household-notes.md").write_text("Ava prefers quiet restaurants near home.", encoding="utf-8")
        self.database = Database(self.root / "agent.db")
        self.database.initialize("Owner")
        self.settings = SimpleNamespace(data_dir=self.root / "data", google_drive_sync_dir=self.drive_root)
        self.vault = ProfileVault(self.settings)
        self.mirror = GoogleDriveMirror(self.settings, self.database, self.vault)

    def tearDown(self) -> None:
        self.temp_dir.cleanup()

    def test_lists_and_imports_only_supported_text_documents(self) -> None:
        files = self.mirror.list_files()
        self.assertEqual(files[0]["relative_path"], "household-notes.md")
        result = self.mirror.import_file("owner", "household-notes.md", remember_excerpt=True)
        self.assertEqual(result["source_file"], "household-notes.md")
        self.assertEqual(result["imported"]["profile_id"], "owner")
        self.assertEqual(len(self.vault.list_files("owner")), 1)
        recalled = self.database.recall_memories("owner", "quiet restaurants")
        self.assertEqual(len(recalled), 1)

    def test_rejects_paths_outside_the_configured_mirror(self) -> None:
        with self.assertRaises(ValueError):
            self.mirror.import_file("owner", "../agent.db", remember_excerpt=False)

    def test_unconfigured_mirror_stays_unavailable(self) -> None:
        settings = SimpleNamespace(data_dir=self.root / "other-data", google_drive_sync_dir=None)
        mirror = GoogleDriveMirror(settings, self.database, ProfileVault(settings))
        self.assertFalse(mirror.status()["ready"])
        self.assertEqual(mirror.list_files(), [])


if __name__ == "__main__":
    unittest.main()
