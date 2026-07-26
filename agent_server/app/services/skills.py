from __future__ import annotations

from typing import Any

from app.db import Database


SKILL_CATALOG: list[dict[str, Any]] = [
    {
        "skill_id": "web_search",
        "display_name": "Perplexity-style web search",
        "description": "Rewrites a question, searches SearXNG, retrieves public sources, and streams cited answers.",
        "category": "Knowledge",
        "enabled": True,
        "requires_configuration": False,
    },
    {
        "skill_id": "profile_memory",
        "display_name": "Profile memory",
        "description": "Keeps separate conversation recall and saved notes for each enrolled profile.",
        "category": "Memory",
        "enabled": True,
        "requires_configuration": False,
    },
    {
        "skill_id": "google_drive",
        "display_name": "Google Drive archive and search",
        "description": "Imports selected folders and backs up approved per-person exports after OAuth configuration.",
        "category": "Cloud storage",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "google_photos",
        "display_name": "Google Photos library",
        "description": "Searches or saves explicitly approved photos after a user-owned OAuth connection is configured.",
        "category": "Cloud storage",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "contacts",
        "display_name": "Contacts lookup",
        "description": "Looks up contacts only through a configured address-book provider.",
        "category": "Communication",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "messaging",
        "display_name": "Message drafting and send approval",
        "description": "Drafts messages and pauses for spoken or on-screen confirmation before sending.",
        "category": "Communication",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "bookings",
        "display_name": "Reservation helper",
        "description": "Researches availability and creates a booking proposal that needs confirmation before submission.",
        "category": "Tasks",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "file_transfer",
        "display_name": "Trusted file transfer",
        "description": "Transfers files only through named destination allowlists and owner-managed rules.",
        "category": "Devices",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "location_share",
        "display_name": "Trusted location sharing",
        "description": "Shares location only through named destinations and bounded owner-managed rules.",
        "category": "Devices",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "smart_devices",
        "display_name": "Smart-device control",
        "description": "Controls configured devices only through named device allowlists and owner-managed rules.",
        "category": "Devices",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "webcam_capture",
        "display_name": "Galaxy Book webcam capture",
        "description": "Uses browser permission to capture an explicitly initiated image or video frame.",
        "category": "Media",
        "enabled": False,
        "requires_configuration": False,
    },
    {
        "skill_id": "person_enrollment",
        "display_name": "Consenting-person enrollment",
        "description": "Stores a consent record and optional profile image for enrolled household members.",
        "category": "Media",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "security_cameras",
        "display_name": "Named security-camera sources",
        "description": "Connects configured camera streams with visible state and restricted owner access.",
        "category": "Media",
        "enabled": False,
        "requires_configuration": True,
    },
    {
        "skill_id": "wake_word",
        "display_name": "Wake-word listener",
        "description": "Provides an optional, visibly active wake-word pathway on a capable kiosk client.",
        "category": "Voice",
        "enabled": False,
        "requires_configuration": True,
    },
]


class SkillRegistry:
    def __init__(self, database: Database) -> None:
        self.database = database

    def initialize(self) -> None:
        self.database.seed_skills(SKILL_CATALOG)

    def list(self) -> list[dict[str, Any]]:
        return self.database.list_skills()

    def set_enabled(self, skill_id: str, enabled: bool) -> dict[str, Any] | None:
        record = self.database.set_skill_enabled(skill_id, enabled)
        if record:
            self.database.audit("skill_state_changed", {"skill_id": skill_id, "enabled": enabled})
        return record
