from __future__ import annotations

import asyncio
import os
from typing import Any, Dict, Optional

import httpx


DEFAULT_TIMEOUT = float(os.getenv("HTTP_TIMEOUT_SECONDS", "15"))
DEFAULT_RETRIES = int(os.getenv("HTTP_MAX_RETRIES", "3"))
DEFAULT_BACKOFF_BASE = float(os.getenv("HTTP_BACKOFF_BASE", "0.5"))


class HttpClient:
    """Lightweight async HTTP client with retry + exponential backoff.

    Designed to keep dependencies minimal and stay framework-agnostic.
    """

    def __init__(self, timeout: float = DEFAULT_TIMEOUT):
        self._client = httpx.AsyncClient(timeout=timeout, follow_redirects=True)

    async def aclose(self) -> None:
        await self._client.aclose()

    async def get_json(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retries: int = DEFAULT_RETRIES,
        backoff_base: float = DEFAULT_BACKOFF_BASE,
    ) -> Dict[str, Any]:
        attempt = 0
        while True:
            try:
                resp = await self._client.get(url, params=params, headers=headers)
                resp.raise_for_status()
                return resp.json()
            except httpx.HTTPError:
                if attempt >= retries:
                    raise
                await asyncio.sleep(backoff_base * (2 ** attempt))
                attempt += 1

    async def get_text(
        self,
        url: str,
        params: Optional[Dict[str, Any]] = None,
        headers: Optional[Dict[str, str]] = None,
        retries: int = DEFAULT_RETRIES,
        backoff_base: float = DEFAULT_BACKOFF_BASE,
    ) -> str:
        attempt = 0
        while True:
            try:
                resp = await self._client.get(url, params=params, headers=headers)
                resp.raise_for_status()
                return resp.text
            except httpx.HTTPError:
                if attempt >= retries:
                    raise
                await asyncio.sleep(backoff_base * (2 ** attempt))
                attempt += 1


async def with_client(coro_func, *args, **kwargs):
    """Helper to use HttpClient without manual lifecycle management."""

    client = HttpClient()
    try:
        return await coro_func(client, *args, **kwargs)
    finally:
        await client.aclose()


