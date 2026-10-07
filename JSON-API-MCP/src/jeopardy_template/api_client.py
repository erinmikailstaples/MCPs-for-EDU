"""Validated asynchronous client used by the MCP tools."""

from __future__ import annotations

import os
from typing import Any

import httpx
from pydantic import ValidationError

from .models import CategoryPage, CluePage, ClueResult, Round


class APIClientError(RuntimeError):
    """A controlled API failure safe to translate into an MCP tool error."""


class JeopardyAPIClient:
    def __init__(self, base_url: str, timeout_seconds: float = 5.0) -> None:
        self.base_url = base_url.rstrip("/")
        self.timeout_seconds = timeout_seconds

    @classmethod
    def from_env(cls) -> JeopardyAPIClient:
        return cls(os.environ.get("JEOPARDY_API_BASE_URL", "http://127.0.0.1:8000"))

    async def _get(self, path: str, params: dict[str, Any] | None = None) -> Any:
        try:
            async with httpx.AsyncClient(
                base_url=self.base_url,
                timeout=self.timeout_seconds,
            ) as client:
                response = await client.get(path, params=params)
        except (httpx.ConnectError, httpx.TimeoutException) as exc:
            raise APIClientError(
                "Jeopardy API is unavailable; start FastAPI and try again"
            ) from exc

        if response.status_code == 404:
            raise APIClientError("the requested clue does not exist")
        if response.status_code == 422:
            raise APIClientError("the API rejected the tool arguments")
        try:
            response.raise_for_status()
        except httpx.HTTPStatusError as exc:
            raise APIClientError(f"Jeopardy API returned HTTP {response.status_code}") from exc
        try:
            return response.json()
        except ValueError as exc:
            raise APIClientError("Jeopardy API returned invalid JSON") from exc

    async def search_clues(
        self,
        *,
        query: str | None,
        category: str | None,
        round_: Round | None,
        limit: int,
        offset: int,
    ) -> CluePage:
        optional_params = {
            "query": query,
            "category": category,
            "round": round_.value if round_ else None,
        }
        params = {
            **{key: value for key, value in optional_params.items() if value is not None},
            "limit": limit,
            "offset": offset,
        }
        try:
            return CluePage.model_validate(await self._get("/clues", params=params))
        except ValidationError as exc:
            raise APIClientError(
                "Jeopardy API returned an unexpected clue-search response"
            ) from exc

    async def get_clue(self, clue_id: int) -> ClueResult:
        try:
            return ClueResult.model_validate(await self._get(f"/clues/{clue_id}"))
        except ValidationError as exc:
            raise APIClientError("Jeopardy API returned an unexpected clue response") from exc

    async def list_categories(
        self, *, query: str | None, limit: int, offset: int
    ) -> CategoryPage:
        params = {"limit": limit, "offset": offset}
        if query is not None:
            params["query"] = query
        try:
            return CategoryPage.model_validate(await self._get("/categories", params=params))
        except ValidationError as exc:
            raise APIClientError("Jeopardy API returned an unexpected category response") from exc
