from __future__ import annotations

from typing import Any

import httpx

from app.config import Settings


class SearxngClient:
    def __init__(self, settings: Settings) -> None:
        self.base_url = settings.searxng_base_url
        self.limit = settings.search_result_limit
        self.timeout = settings.request_timeout_seconds

    async def health(self) -> dict[str, Any]:
        try:
            async with httpx.AsyncClient(timeout=min(self.timeout, 8.0)) as client:
                response = await client.get(f"{self.base_url}/healthz")
                if response.status_code not in {200, 204}:
                    response = await client.get(f"{self.base_url}/")
                response.raise_for_status()
            return {"reachable": True}
        except httpx.HTTPError as error:
            return {"reachable": False, "error": str(error)}

    async def search(self, query: str) -> list[dict[str, str]]:
        params = {"q": query, "format": "json", "language": "en", "safesearch": 1}
        async with httpx.AsyncClient(timeout=self.timeout, follow_redirects=True) as client:
            response = await client.get(f"{self.base_url}/search", params=params)
            response.raise_for_status()
            payload = response.json()
        results: list[dict[str, str]] = []
        seen_urls: set[str] = set()
        for raw in payload.get("results", []):
            url = str(raw.get("url", "")).strip()
            title = str(raw.get("title", "")).strip()
            content = str(raw.get("content", "")).strip()
            if not url or url in seen_urls:
                continue
            seen_urls.add(url)
            results.append({"title": title[:300], "url": url[:2048], "content": content[:1500]})
            if len(results) >= self.limit:
                break
        return results
