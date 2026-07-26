from __future__ import annotations

import json
from collections.abc import AsyncIterator
from typing import Any

import httpx

from app.config import Settings


class OllamaClient:
    def __init__(self, settings: Settings) -> None:
        self.base_url = settings.ollama_base_url
        self.model = settings.ollama_model
        self.timeout = settings.request_timeout_seconds

    async def health(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=min(self.timeout, 8.0)) as client:
                response = await client.get(f"{self.base_url}/api/tags")
                response.raise_for_status()
                models = [item.get("name", "") for item in response.json().get("models", [])]
            return {"reachable": True, "configured_model": self.model, "model_available": self.model in models, "models": models}
        except httpx.HTTPError as error:
            return {"reachable": False, "configured_model": self.model, "model_available": False, "error": str(error)}

    async def complete(self, messages: list[dict[str, str]], temperature: float = 0.2) -> str:
        text = ""
        async for token in self.stream(messages, temperature=temperature):
            text += token
        return text.strip()

    async def stream(self, messages: list[dict[str, str]], temperature: float = 0.2) -> AsyncIterator[str]:
        payload = {
            "model": self.model,
            "messages": messages,
            "stream": True,
            "options": {"temperature": temperature},
        }
        timeout = httpx.Timeout(self.timeout, connect=min(self.timeout, 10.0))
        async with httpx.AsyncClient(timeout=timeout) as client:
            async with client.stream("POST", f"{self.base_url}/api/chat", json=payload) as response:
                response.raise_for_status()
                async for line in response.aiter_lines():
                    if not line:
                        continue
                    chunk = json.loads(line)
                    if chunk.get("error"):
                        raise RuntimeError(str(chunk["error"]))
                    content = chunk.get("message", {}).get("content", "")
                    if content:
                        yield content
                    if chunk.get("done"):
                        return
