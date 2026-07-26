from __future__ import annotations

import os
from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path


@dataclass(frozen=True)
class Settings:
    app_name: str
    data_dir: Path
    database_path: Path
    ollama_base_url: str
    ollama_model: str
    ollama_vision_model: str
    searxng_base_url: str
    search_result_limit: int
    request_timeout_seconds: float
    agent_step_limit: int
    max_context_chars: int
    public_origin: str
    owner_profile_name: str
    action_webhook_url: str
    action_webhook_token: str
    google_drive_sync_dir: Path | None


@lru_cache
def get_settings() -> Settings:
    data_dir = Path(os.getenv("DATA_DIR", "/data"))
    data_dir.mkdir(parents=True, exist_ok=True)
    return Settings(
        app_name=os.getenv("APP_NAME", "Jarvis Kiosk Agent"),
        data_dir=data_dir,
        database_path=data_dir / os.getenv("DATABASE_FILE", "agent.db"),
        ollama_base_url=os.getenv("OLLAMA_BASE_URL", "http://host.docker.internal:11434").rstrip("/"),
        ollama_model=os.getenv("OLLAMA_MODEL", "llama3.2:3b"),
        ollama_vision_model=os.getenv("OLLAMA_VISION_MODEL", ""),
        searxng_base_url=os.getenv("SEARXNG_BASE_URL", "http://searxng:8080").rstrip("/"),
        search_result_limit=max(1, min(int(os.getenv("SEARCH_RESULT_LIMIT", "6")), 12)),
        request_timeout_seconds=max(5.0, float(os.getenv("REQUEST_TIMEOUT_SECONDS", "45"))),
        agent_step_limit=max(1, min(int(os.getenv("AGENT_STEP_LIMIT", "4")), 8)),
        max_context_chars=max(2000, min(int(os.getenv("MAX_CONTEXT_CHARS", "12000")), 40000)),
        public_origin=os.getenv("PUBLIC_ORIGIN", ""),
        owner_profile_name=os.getenv("OWNER_PROFILE_NAME", "Owner"),
        action_webhook_url=os.getenv("ACTION_WEBHOOK_URL", "").rstrip("/"),
        action_webhook_token=os.getenv("ACTION_WEBHOOK_TOKEN", ""),
        google_drive_sync_dir=Path(os.environ["GOOGLE_DRIVE_SYNC_DIR"]) if os.getenv("GOOGLE_DRIVE_SYNC_DIR") else None,
    )
