from __future__ import annotations

import base64
import binascii
import re
from datetime import UTC, datetime
from pathlib import Path

from app.config import Settings


class ProfileVault:
    def __init__(self, settings: Settings) -> None:
        self.root = settings.data_dir / "profiles"
        self.root.mkdir(parents=True, exist_ok=True)

    def save_text(self, profile_id: str, title: str, content: str, category: str) -> dict[str, str]:
        profile_dir = self.root / self._safe_name(profile_id)
        category_dir = profile_dir / self._safe_name(category)
        category_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        file_name = f"{timestamp}-{self._safe_name(title)[:64]}.md"
        path = category_dir / file_name
        path.write_text(
            "# " + title.strip() + "\n\n"
            + f"Saved at: {datetime.now(UTC).isoformat()}\n"
            + f"Profile: {profile_id}\n"
            + f"Category: {category}\n\n"
            + content.strip()
            + "\n",
            encoding="utf-8",
        )
        return {
            "profile_id": profile_id,
            "category": category,
            "title": title.strip(),
            "file_name": file_name,
            "relative_path": str(path.relative_to(self.root)),
        }

    def save_enrollment_image(self, profile_id: str, image_data_url: str, label: str) -> dict[str, str]:
        """Persist one explicit profile-enrollment image locally without recognition processing."""
        match = re.fullmatch(r"data:image/(jpeg|png|webp);base64,([A-Za-z0-9+/=\s]+)", image_data_url)
        if not match:
            raise ValueError("Enrollment image must be a JPEG, PNG, or WebP data URL.")
        try:
            image_bytes = base64.b64decode(match.group(2), validate=True)
        except (binascii.Error, ValueError) as exc:
            raise ValueError("Enrollment image could not be decoded.") from exc
        if not image_bytes or len(image_bytes) > 2 * 1024 * 1024:
            raise ValueError("Enrollment image must be between 1 byte and 2 MB.")
        extension = {"jpeg": "jpg", "png": "png", "webp": "webp"}[match.group(1)]
        profile_dir = self.root / self._safe_name(profile_id) / "enrollment"
        profile_dir.mkdir(parents=True, exist_ok=True)
        timestamp = datetime.now(UTC).strftime("%Y%m%dT%H%M%SZ")
        file_name = f"{timestamp}-profile-image.{extension}"
        path = profile_dir / file_name
        path.write_bytes(image_bytes)
        return {
            "profile_id": profile_id,
            "label": label.strip() or "Galaxy Book explicit profile enrollment",
            "file_name": file_name,
            "relative_path": str(path.relative_to(self.root)),
        }

    def list_files(self, profile_id: str, limit: int = 60) -> list[dict[str, str]]:
        profile_dir = self.root / self._safe_name(profile_id)
        if not profile_dir.exists():
            return []
        files = sorted(profile_dir.rglob("*.md"), key=lambda item: item.stat().st_mtime, reverse=True)[:limit]
        return [
            {
                "relative_path": str(path.relative_to(self.root)),
                "category": path.parent.name,
                "file_name": path.name,
                "updated_at": datetime.fromtimestamp(path.stat().st_mtime, UTC).isoformat(),
            }
            for path in files
        ]

    @staticmethod
    def _safe_name(value: str) -> str:
        name = re.sub(r"[^a-zA-Z0-9_-]+", "-", value.strip()).strip("-").lower()
        return name or "untitled"
