"""FastAPI application for the active Jeopardy-shaped dataset."""

from __future__ import annotations

import os
from collections.abc import AsyncIterator
from contextlib import asynccontextmanager
from pathlib import Path
from typing import Annotated

from fastapi import FastAPI, HTTPException, Query, Request

from .adapter import load_clues, load_manifest_version
from .models import CategoryPage, CluePage, ClueResult, HealthResponse, Round
from .repository import ClueRepository


def _path_from_env(name: str, default: str) -> Path:
    return Path(os.environ.get(name, default)).expanduser().resolve()


def create_app(
    data_path: Path | None = None,
    manifest_path: Path | None = None,
) -> FastAPI:
    @asynccontextmanager
    async def lifespan(app: FastAPI) -> AsyncIterator[None]:
        active_data = data_path or _path_from_env("JEOPARDY_DATA_PATH", "data/clues.json")
        active_manifest = manifest_path or _path_from_env(
            "JEOPARDY_MANIFEST_PATH", "data/manifest.json"
        )
        clues = load_clues(active_data)
        app.state.repository = ClueRepository(
            clues=tuple(clues),
            dataset_version=load_manifest_version(active_manifest),
        )
        yield

    app = FastAPI(
        title="Jeopardy JSON Reference API",
        version="0.1.0",
        lifespan=lifespan,
    )

    def repository(request: Request) -> ClueRepository:
        return request.app.state.repository

    @app.get("/health", response_model=HealthResponse)
    async def health(request: Request) -> HealthResponse:
        repo = repository(request)
        return HealthResponse(
            status="ready",
            dataset_version=repo.dataset_version,
            clue_count=len(repo.clues),
        )

    @app.get("/clues", response_model=CluePage)
    async def search_clues(
        request: Request,
        query: Annotated[str | None, Query(min_length=1)] = None,
        category: Annotated[str | None, Query(min_length=1)] = None,
        round_: Annotated[Round | None, Query(alias="round")] = None,
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> CluePage:
        return repository(request).search(
            query=query,
            category=category,
            round_=round_,
            limit=limit,
            offset=offset,
        )

    @app.get("/clues/{clue_id}", response_model=ClueResult)
    async def get_clue(clue_id: int, request: Request) -> ClueResult:
        repo = repository(request)
        clue = repo.get(clue_id)
        if clue is None:
            raise HTTPException(status_code=404, detail=f"clue {clue_id} was not found")
        return ClueResult(item=clue, dataset_version=repo.dataset_version)

    @app.get("/categories", response_model=CategoryPage)
    async def list_categories(
        request: Request,
        query: Annotated[str | None, Query(min_length=1)] = None,
        limit: Annotated[int, Query(ge=1, le=50)] = 10,
        offset: Annotated[int, Query(ge=0)] = 0,
    ) -> CategoryPage:
        return repository(request).categories(query=query, limit=limit, offset=offset)

    return app


app = create_app()
