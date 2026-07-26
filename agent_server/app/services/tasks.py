from __future__ import annotations

import re
from typing import Any

from app.adapters.ollama import OllamaClient
from app.db import Database
from app.services.actions import ActionPolicyService


class TaskPlanner:
    """Turn a natural-language goal into an explainable, non-executing task plan."""

    def __init__(self, database: Database, ollama: OllamaClient, actions: ActionPolicyService) -> None:
        self.database = database
        self.ollama = ollama
        self.actions = actions

    async def plan(self, profile_id: str, request: str) -> dict[str, Any]:
        profile = self.database.get_profile(profile_id)
        if not profile:
            raise ValueError("The selected profile does not exist.")
        action_type = self._classify_action(request)
        plan = self._deterministic_steps(request, action_type)
        proposal: dict[str, Any] | None = None
        if action_type:
            payload = self._build_payload(request, action_type)
            proposal = self.actions.propose(
                profile_id=profile_id,
                action_type=action_type,
                summary=request.strip()[:240],
                payload=payload,
                rule_id=None,
            )
        refinement = await self._optional_refinement(request, action_type)
        if refinement:
            plan[0] = refinement
        self.database.audit(
            "task_planned",
            {"action_type": action_type, "has_proposal": bool(proposal), "request_preview": request.strip()[:160]},
            profile_id,
        )
        return {
            "profile_id": profile_id,
            "request": request.strip(),
            "steps": plan,
            "action_type": action_type,
            "proposal": proposal,
            "note": self._note_for(proposal),
        }

    async def _optional_refinement(self, request: str, action_type: str | None) -> str:
        prompt = [
            {"role": "system", "content": "Write one concise first step for a personal assistant task plan. Do not claim an action has happened. Return one sentence only."},
            {"role": "user", "content": f"Task: {request}\nAction type: {action_type or 'research'}"},
        ]
        try:
            result = await self.ollama.complete(prompt, temperature=0.1)
            result = re.sub(r"\s+", " ", result).strip()
            return result[:240] if result else "Clarify the relevant details and gather the information needed to proceed."
        except Exception:
            return "Clarify the relevant details and gather the information needed to proceed."

    @staticmethod
    def _classify_action(request: str) -> str | None:
        lowered = request.lower()
        if any(token in lowered for token in ("book ", "booking", "reservation", "reserve a", "reserve table")):
            return "booking"
        if any(token in lowered for token in ("send ", "message ", "text ", "email ")):
            return "message"
        if any(token in lowered for token in ("transfer", "copy file", "send file", "upload file")):
            return "file_transfer"
        if any(token in lowered for token in ("share location", "send my location", "location share")):
            return "location_share"
        if any(token in lowered for token in ("turn on", "turn off", "switch on", "switch off", "control device")):
            return "device_control"
        return None

    @staticmethod
    def _build_payload(request: str, action_type: str) -> dict[str, Any]:
        target = ""
        target_match = re.search(r"\b(?:to|with|for|on)\s+([A-Za-z0-9 _.'-]{2,80})", request, flags=re.IGNORECASE)
        if target_match:
            target = target_match.group(1).strip(" .")
        if action_type == "device_control":
            device_match = re.search(r"(?:turn|switch)\s+(?:on|off)\s+(.+)$", request, flags=re.IGNORECASE)
            target = device_match.group(1).strip(" .") if device_match else target
            return {"device": target, "request": request.strip()}
        if action_type == "file_transfer":
            return {"destination": target, "request": request.strip()}
        if action_type == "location_share":
            return {"target": target, "request": request.strip()}
        return {"target": target, "request": request.strip()}

    @staticmethod
    def _deterministic_steps(request: str, action_type: str | None) -> list[str]:
        base = [
            "Clarify the relevant details and gather the information needed to proceed.",
            "Present a concise result, draft, or availability summary on the kiosk.",
        ]
        if action_type in {"message", "booking"}:
            base.append("Ask for a spoken or on-screen confirmation immediately before the external action is sent.")
        elif action_type in {"file_transfer", "location_share", "device_control"}:
            base.append("Check for a matching active owner-managed rule and named target before any connector delivery.")
        else:
            base.append("Save only information the active profile explicitly asks to retain.")
        return base

    @staticmethod
    def _note_for(proposal: dict[str, Any] | None) -> str:
        if not proposal:
            return "This is a research or planning task; no external action has been proposed."
        if proposal["status"] == "awaiting_confirmation":
            return "A proposal was created, but it will not be delivered until you confirm it."
        if proposal["status"] == "authorized":
            return "A bounded owner-managed rule authorizes this named action; connector delivery remains separate."
        return proposal["reason"]
