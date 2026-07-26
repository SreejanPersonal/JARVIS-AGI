from __future__ import annotations

from datetime import UTC, datetime
from typing import Any

import httpx

from app.config import Settings
from app.db import Database


class ActionExecutor:
    """Deliver approved actions to one explicit, user-owned connector endpoint.

    The connector is deliberately fixed in environment configuration rather than
    accepted from a chat message or action payload. This prevents the model from
    choosing arbitrary network destinations.
    """

    RETRYABLE_STATUSES = {"confirmed", "authorized", "connector_unavailable", "execution_failed"}

    def __init__(self, settings: Settings, database: Database) -> None:
        self.settings = settings
        self.database = database

    async def execute(self, action_id: str) -> dict[str, Any]:
        action = self.database.get_action(action_id)
        if not action:
            raise ValueError("The action does not exist.")
        if action["status"] not in self.RETRYABLE_STATUSES:
            raise ValueError("This action is not approved for execution in its current state.")
        if self._is_expired(action.get("expires_at")):
            updated = self.database.set_action_status(action_id, "expired")
            raise ValueError("The action authorization has expired. Create a new proposal.")
        if not self.settings.action_webhook_url:
            updated = self.database.set_action_status(action_id, "connector_unavailable")
            self.database.audit("action_connector_unavailable", {"action_id": action_id, "type": action["action_type"]}, action["profile_id"])
            return {
                "action": updated or action,
                "delivery": {
                    "status": "connector_unavailable",
                    "message": "No action connector is configured. The approved action was not sent anywhere.",
                },
            }

        outbound = {
            "action_id": action["action_id"],
            "profile_id": action["profile_id"],
            "action_type": action["action_type"],
            "summary": action["summary"],
            "payload": action["payload"],
            "authorized_at": datetime.now(UTC).isoformat(),
        }
        headers = {"Content-Type": "application/json", "X-Jarvis-Action-ID": action["action_id"]}
        if self.settings.action_webhook_token:
            headers["Authorization"] = f"Bearer {self.settings.action_webhook_token}"

        try:
            timeout = httpx.Timeout(self.settings.request_timeout_seconds, connect=min(10.0, self.settings.request_timeout_seconds))
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=False) as client:
                response = await client.post(self.settings.action_webhook_url, json=outbound, headers=headers)
            response_preview = response.text[:500]
            if 200 <= response.status_code < 300:
                updated = self.database.set_action_status(action_id, "executed")
                self.database.audit("action_executed", {"action_id": action_id, "status_code": response.status_code}, action["profile_id"])
                return {
                    "action": updated or action,
                    "delivery": {"status": "executed", "http_status": response.status_code, "response_preview": response_preview},
                }
            updated = self.database.set_action_status(action_id, "execution_failed")
            self.database.audit("action_execution_failed", {"action_id": action_id, "status_code": response.status_code}, action["profile_id"])
            return {
                "action": updated or action,
                "delivery": {"status": "execution_failed", "http_status": response.status_code, "response_preview": response_preview},
            }
        except httpx.HTTPError as error:
            updated = self.database.set_action_status(action_id, "execution_failed")
            self.database.audit("action_execution_failed", {"action_id": action_id, "error": type(error).__name__}, action["profile_id"])
            return {
                "action": updated or action,
                "delivery": {"status": "execution_failed", "message": f"Connector request failed: {type(error).__name__}"},
            }

    @staticmethod
    def _is_expired(value: str | None) -> bool:
        return bool(value and datetime.fromisoformat(value) <= datetime.now(UTC))
