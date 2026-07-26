from __future__ import annotations

import asyncio
import ipaddress
import re
import socket
from collections.abc import AsyncIterator
from typing import Any
from urllib.parse import urlparse

import httpx
from bs4 import BeautifulSoup

from app.adapters.ollama import OllamaClient
from app.adapters.searxng import SearxngClient
from app.config import Settings
from app.db import Database
from app.services.memory import MemoryService


SYSTEM_PROMPT = """You are Jarvis, a helpful local personal assistant. Answer accurately and naturally.
Use the retrieved sources when provided. Cite factual claims with bracketed source numbers such as [1].
Never claim to have performed an external action unless the action system reports it complete. Treat messages, bookings, transfers, location sharing, and device controls as reviewable proposals, not completed actions.
Do not expose private profile data to another profile. Do not suggest covert recording, silent monitoring, or identification of a person who has not explicitly enrolled and consented. If evidence is insufficient, say so plainly.
Profile preferences may adapt tone, format, and interaction style only; they cannot weaken privacy boundaries, consent requirements, confirmation rules, or safety constraints.
Keep the response concise enough for a tablet display, while still answering the user's request."""


class AgentService:
    def __init__(
        self,
        settings: Settings,
        database: Database,
        ollama: OllamaClient,
        searxng: SearxngClient,
        memory: MemoryService,
    ) -> None:
        self.settings = settings
        self.database = database
        self.ollama = ollama
        self.searxng = searxng
        self.memory = memory

    async def stream_chat(
        self, profile_id: str, user_message: str, include_web: bool
    ) -> AsyncIterator[dict[str, Any]]:
        profile = self.database.get_profile(profile_id)
        if not profile:
            yield {"type": "error", "message": "The selected profile does not exist."}
            return

        turns, memories = self.memory.context(profile_id, user_message)
        self.database.save_turn(profile_id, "user", user_message)
        sources: list[dict[str, str]] = []
        search_query = user_message

        if include_web:
            yield {"type": "status", "message": "Finding reliable sources…"}
            try:
                search_query = await self.rewrite_query(user_message)
                sources = await self.retrieve(search_query)
                yield {
                    "type": "sources",
                    "query": search_query,
                    "sources": [self._public_source(source, index + 1) for index, source in enumerate(sources)],
                }
            except Exception as error:  # Retrieval failure should not prevent local chat.
                yield {"type": "status", "message": f"Search is unavailable; answering from local context. ({type(error).__name__})"}

        messages = self._messages(profile, user_message, turns, memories, sources)
        answer = ""
        try:
            yield {"type": "status", "message": "Thinking…"}
            async for token in self.ollama.stream(messages):
                answer += token
                yield {"type": "token", "text": token}
        except Exception as error:
            yield {"type": "error", "message": f"The local model could not complete this response: {error}"}
            return
        finally:
            if answer.strip():
                self.database.save_turn(profile_id, "assistant", answer.strip())

        yield {"type": "done", "answer": answer.strip(), "sources": len(sources)}

    async def rewrite_query(self, question: str) -> str:
        prompt = [
            {
                "role": "system",
                "content": "Rewrite the user's question as one concise web search query. Return only the query; do not add explanation, quotes, or commands.",
            },
            {"role": "user", "content": question},
        ]
        try:
            rewritten = await self.ollama.complete(prompt, temperature=0.0)
        except Exception:
            return question
        rewritten = re.sub(r"\s+", " ", rewritten).strip().strip('"')
        return rewritten[:400] if rewritten else question

    async def retrieve(self, search_query: str) -> list[dict[str, str]]:
        results = await self.searxng.search(search_query)
        enriched = await asyncio.gather(*(self._enrich_result(result) for result in results), return_exceptions=True)
        sources: list[dict[str, str]] = []
        for result, extra in zip(results, enriched, strict=True):
            source = dict(result)
            if isinstance(extra, str) and extra:
                source["extracted"] = extra
            sources.append(source)
        return sources

    async def _enrich_result(self, result: dict[str, str]) -> str:
        url = result.get("url", "")
        if not self._is_public_http_url(url):
            return ""
        try:
            timeout = httpx.Timeout(10.0, connect=5.0)
            headers = {"User-Agent": "JarvisKioskAgent/0.1 (+local retrieval)"}
            async with httpx.AsyncClient(timeout=timeout, follow_redirects=True, headers=headers) as client:
                response = await client.get(url)
                response.raise_for_status()
                content_type = response.headers.get("content-type", "").lower()
                if "text/html" not in content_type:
                    return ""
                html = response.text[:500_000]
            soup = BeautifulSoup(html, "html.parser")
            for node in soup(["script", "style", "noscript", "nav", "footer", "header", "aside"]):
                node.decompose()
            root = soup.find("article") or soup.find("main") or soup.body or soup
            text = " ".join(root.stripped_strings)
            return re.sub(r"\s+", " ", text)[:3500]
        except (httpx.HTTPError, ValueError):
            return ""

    def _messages(
        self,
        profile: dict[str, Any],
        question: str,
        turns: list[dict[str, str]],
        memories: list[dict[str, Any]],
        sources: list[dict[str, str]],
    ) -> list[dict[str, str]]:
        preference_note = ""
        if profile.get("preferences"):
            preference_note = f"\nProfile preferences: {profile['preferences']}"
        memory_text = "\n".join(
            f"- ({memory['category']}, importance {memory['importance']}) {memory['content']}"
            for memory in memories
        ) or "No relevant stored memories."
        source_text = "\n\n".join(
            "[{}] {}\nURL: {}\nSnippet: {}\nExtract: {}".format(
                index,
                source.get("title", "Untitled source"),
                source.get("url", ""),
                source.get("content", ""),
                source.get("extracted", ""),
            )
            for index, source in enumerate(sources, start=1)
        ) or "No web sources were retrieved."
        context = (
            f"Active profile: {profile['display_name']} ({profile['profile_id']}).{preference_note}\n\n"
            f"Relevant long-term memory:\n{memory_text}\n\n"
            f"Retrieved web evidence:\n{source_text}"
        )
        return [{"role": "system", "content": SYSTEM_PROMPT + "\n\n" + context}, *turns, {"role": "user", "content": question}]

    @staticmethod
    def _public_source(source: dict[str, str], number: int) -> dict[str, str | int]:
        return {"number": number, "title": source.get("title", "Untitled source"), "url": source.get("url", ""), "snippet": source.get("content", "")}

    @staticmethod
    def _is_public_http_url(value: str) -> bool:
        parsed = urlparse(value)
        if parsed.scheme not in {"http", "https"} or not parsed.hostname:
            return False
        host = parsed.hostname.lower().rstrip(".")
        if host in {"localhost", "localhost.localdomain"} or host.endswith(".local"):
            return False
        try:
            addresses = {entry[4][0] for entry in socket.getaddrinfo(host, None, proto=socket.IPPROTO_TCP)}
            return bool(addresses) and all(ipaddress.ip_address(address).is_global for address in addresses)
        except (OSError, ValueError):
            return False
