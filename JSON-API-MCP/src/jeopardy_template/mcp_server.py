"""Thin MCP wrapper around the FastAPI service."""

from typing import Annotated

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import Field

from .api_client import APIClientError, JeopardyAPIClient
from .models import CategoryPage, CluePage, ClueResult, Round

mcp = MCPServer(
    "Jeopardy Basics",
    instructions=(
        "Use these read-only tools to search and retrieve Jeopardy-shaped clues. "
        "Results include answers and board values; value may be null for Final Jeopardy."
    ),
)

READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)


def _client() -> JeopardyAPIClient:
    return JeopardyAPIClient.from_env()


@mcp.tool(title="Search clues", annotations=READ_ONLY)
async def search_clues(
    query: Annotated[str | None, Field(min_length=1)] = None,
    category: Annotated[str | None, Field(min_length=1)] = None,
    round: Round | None = None,
    limit: Annotated[int, Field(ge=1, le=50)] = 10,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> CluePage:
    """Search clue prompts and filter by exact category or round.

    Returned clues include their answers and board value. Final Jeopardy values may be null.
    """
    try:
        return await _client().search_clues(
            query=query,
            category=category,
            round_=round,
            limit=limit,
            offset=offset,
        )
    except APIClientError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool(title="Get a clue", annotations=READ_ONLY)
async def get_clue(
    clue_id: Annotated[int, Field(ge=0)],
) -> ClueResult:
    """Retrieve one clue by its dataset-scoped ID, including answer and board value."""
    try:
        return await _client().get_clue(clue_id)
    except APIClientError as exc:
        raise ToolError(str(exc)) from exc


@mcp.tool(title="List categories", annotations=READ_ONLY)
async def list_categories(
    query: Annotated[str | None, Field(min_length=1)] = None,
    limit: Annotated[int, Field(ge=1, le=50)] = 10,
    offset: Annotated[int, Field(ge=0)] = 0,
) -> CategoryPage:
    """List category names, optionally filtered by a case-insensitive substring."""
    try:
        return await _client().list_categories(query=query, limit=limit, offset=offset)
    except APIClientError as exc:
        raise ToolError(str(exc)) from exc


if __name__ == "__main__":
    mcp.run()
