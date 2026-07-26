from __future__ import annotations

from pathlib import Path
from typing import Any

from app.config import Settings
from app.db import Database
from app.services.vault import ProfileVault


class GoogleDriveMirror:
    """Imports explicitly selected text documents from a read-only mounted Drive mirror.

    OAuth and rclone run outside this service. The container only receives a limited,
    read-only directory mount, which avoids storing a cloud credential in the agent.
    """

    allowed_extensions = {".txt", ".md", ".csv", ".json", ".log"}
    max_file_bytes = 2_000_000
    max_import_chars = 120_000

    def __init__(self, settings: Settings, database: Database, vault: ProfileVault) -> None:
        self.root = settings.google_drive_sync_dir
        self.database = database
        self.vault = vault

    def status(self) -> dict[str, Any]:
        if not self.root:
            return {
                "configured": False,
                "ready": False,
                "message": "No Google Drive mirror directory is configured.",
                "file_count": 0,
            }
        ready = self.root.is_dir()
        return {
            "configured": True,
            "ready": ready,
            "message": "Google Drive mirror is ready." if ready else "Configured Drive mirror directory is unavailable.",
            "file_count": len(self.list_files(limit=250)) if ready else 0,
        }

    def list_files(self, limit: int = 100) -> list[dict[str, Any]]:
        if not self.root or not self.root.is_dir():
            return []
        root = self.root.resolve()
        records: list[dict[str, Any]] = []
        for path in sorted(root.rglob("*"), key=lambda item: str(item).lower()):
            if not path.is_file() or path.suffix.lower() not in self.allowed_extensions:
                continue
            try:
                resolved = path.resolve()
                if not resolved.is_relative_to(root):
                    continue
                size = resolved.stat().st_size
            except OSError:
                continue
            if size > self.max_file_bytes:
                continue
            records.append(
                {
                    "relative_path": str(resolved.relative_to(root)),
                    "size_bytes": size,
                    "extension": resolved.suffix.lower(),
                }
            )
            if len(records) >= limit:
                break
        return records

    def import_file(self, profile_id: str, relative_path: str, remember_excerpt: bool) -> dict[str, Any]:
        if not self.database.get_profile(profile_id):
            raise ValueError("Unknown profile")
        source = self._resolve_allowed_file(relative_path)
        try:
            text = source.read_text(encoding="utf-8", errors="replace")
        except OSError as error:
            raise ValueError(f"Could not read Drive mirror file: {error}") from error
        text = text[: self.max_import_chars]
        imported = self.vault.save_text(
            profile_id=profile_id,
            title=f"Drive import — {source.name}",
            content=text,
            category="google-drive-imports",
        )
        memory = None
        if remember_excerpt:
            excerpt = " ".join(text.split())[:1200]
            if excerpt:
                memory = self.database.create_memory(
                    profile_id=profile_id,
                    content=f"User explicitly imported Drive document '{source.name}': {excerpt}",
                    category="google-drive-import",
                    importance=2,
                )
        self.database.audit(
            "google_drive_file_imported",
            {
                "relative_path": str(source.relative_to(self.root.resolve() if self.root else source.parent)),
                "remember_excerpt": remember_excerpt,
                "vault_relative_path": imported["relative_path"],
            },
            profile_id,
        )
        return {"imported": imported, "memory": memory, "source_file": source.name}

    def _resolve_allowed_file(self, relative_path: str) -> Path:
        if not self.root or not self.root.is_dir():
            raise ValueError("Google Drive mirror is not configured or unavailable")
        root = self.root.resolve()
        candidate = (root / relative_path).resolve()
        if not candidate.is_relative_to(root):
            raise ValueError("Requested file is outside the configured Drive mirror")
        if not candidate.is_file() or candidate.suffix.lower() not in self.allowed_extensions:
            raise ValueError("Only supported text documents in the configured Drive mirror can be imported")
        try:
            if candidate.stat().st_size > self.max_file_bytes:
                raise ValueError("Drive mirror file exceeds the import size limit")
        except OSError as error:
            raise ValueError(f"Could not inspect Drive mirror file: {error}") from error
        return candidate
