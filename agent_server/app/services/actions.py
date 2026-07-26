from __future__ import annotations

from datetime import UTC, datetime, timedelta
from typing import Any

from app.db import Database


class ActionPolicyService:
    CONFIRMED_ACTIONS = {"message", "booking"}
    PREAUTHORIZED_ACTIONS = {"file_transfer", "location_share", "device_control"}

    def __init__(self, database: Database) -> None:
        self.database = database

    def create_rule(
        self,
        rule_id: str,
        profile_id: str,
        action_type: str,
        display_name: str,
        allowed_targets: list[str],
        expires_at: datetime | None,
        enabled: bool,
    ) -> dict[str, Any]:
        if action_type not in self.PREAUTHORIZED_ACTIONS:
            raise ValueError("Only file transfers, location shares, and device controls may use pre-authorized rules.")
        targets = sorted({target.strip() for target in allowed_targets if target.strip()})
        if not targets:
            raise ValueError("At least one named target is required.")
        rule = self.database.create_action_rule(
            rule_id=rule_id,
            profile_id=profile_id,
            action_type=action_type,
            display_name=display_name,
            allowed_targets=targets,
            expires_at=expires_at.astimezone(UTC).isoformat() if expires_at else None,
            enabled=enabled,
        )
        self.database.audit("action_rule_saved", {"rule_id": rule_id, "action_type": action_type, "targets": targets}, profile_id)
        return rule

    def propose(
        self,
        profile_id: str,
        action_type: str,
        summary: str,
        payload: dict[str, Any],
        rule_id: str | None,
    ) -> dict[str, Any]:
        if not self.database.get_profile(profile_id):
            raise ValueError("The selected profile does not exist.")
        if action_type in self.CONFIRMED_ACTIONS:
            expires_at = (datetime.now(UTC) + timedelta(minutes=10)).isoformat()
            action = self.database.create_action(
                profile_id, action_type, summary, payload, "awaiting_confirmation", True,
                "This action always requires the owner to speak or tap confirmation.", expires_at=expires_at,
            )
        elif action_type in self.PREAUTHORIZED_ACTIONS:
            action = self._apply_rule(profile_id, action_type, summary, payload, rule_id)
        else:
            raise ValueError("Unsupported action type.")
        self.database.audit("action_proposed", {"action_id": action["action_id"], "type": action_type, "status": action["status"]}, profile_id)
        return action

    def confirm(self, action_id: str, confirmation_phrase: str) -> dict[str, Any]:
        action = self.database.get_action(action_id)
        if not action:
            raise ValueError("The action does not exist.")
        if action["status"] != "awaiting_confirmation" or not action["requires_confirmation"]:
            raise ValueError("This action cannot be confirmed in its current state.")
        if not self._contains_confirmation(confirmation_phrase):
            raise ValueError("Confirmation phrase was not recognized. Say or type 'confirm'.")
        expires_at = action.get("expires_at")
        if expires_at and datetime.fromisoformat(expires_at) <= datetime.now(UTC):
            self.database.set_action_status(action_id, "expired")
            raise ValueError("The confirmation window expired; create a new proposal.")
        updated = self.database.set_action_status(action_id, "confirmed")
        if updated:
            self.database.audit("action_confirmed", {"action_id": action_id, "type": updated["action_type"]}, updated["profile_id"])
        return updated or action

    def _apply_rule(
        self,
        profile_id: str,
        action_type: str,
        summary: str,
        payload: dict[str, Any],
        rule_id: str | None,
    ) -> dict[str, Any]:
        if not rule_id:
            return self.database.create_action(
                profile_id, action_type, summary, payload, "blocked", False,
                "A named owner-managed rule is required for this action type.",
            )
        rule = self.database.get_action_rule(rule_id)
        target = str(payload.get("target") or payload.get("destination") or payload.get("device") or "").strip()
        if not rule or rule["profile_id"] != profile_id or rule["action_type"] != action_type:
            return self.database.create_action(profile_id, action_type, summary, payload, "blocked", False, "The requested rule does not match this profile and action.", rule_id)
        if not rule["enabled"]:
            return self.database.create_action(profile_id, action_type, summary, payload, "blocked", False, "The owner-managed rule is disabled.", rule_id)
        if rule["expires_at"] and datetime.fromisoformat(rule["expires_at"]) <= datetime.now(UTC):
            return self.database.create_action(profile_id, action_type, summary, payload, "blocked", False, "The owner-managed rule has expired.", rule_id)
        if not target or target not in rule["allowed_targets"]:
            return self.database.create_action(profile_id, action_type, summary, payload, "blocked", False, "The named destination or device is not in this rule's allowlist.", rule_id)
        return self.database.create_action(
            profile_id, action_type, summary, payload, "authorized", False,
            f"Authorized by the active owner-managed rule '{rule['display_name']}'.", rule_id,
            expires_at=rule["expires_at"],
        )

    @staticmethod
    def _contains_confirmation(value: str) -> bool:
        words = {word.strip(".,!? ").lower() for word in value.split()}
        return bool(words & {"confirm", "confirmed", "yes"})
