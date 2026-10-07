#!/usr/bin/env python3
"""Protocol-level smoke test against a running FastAPI process."""

from __future__ import annotations

import asyncio
import os
import sys
from pathlib import Path

import httpx
from mcp import Client, StdioServerParameters


async def main() -> None:
    base_url = os.environ.get("JEOPARDY_API_BASE_URL", "http://127.0.0.1:8000")
    async with httpx.AsyncClient(base_url=base_url, timeout=5) as http:
        health = await http.get("/health")
        health.raise_for_status()

    root = Path(__file__).resolve().parents[1]
    parameters = StdioServerParameters(
        command=sys.executable,
        args=["-m", "jeopardy_template.mcp_server"],
        cwd=root,
        env={"JEOPARDY_API_BASE_URL": base_url},
    )
    async with Client(parameters) as client:
        tools = await client.list_tools()
        names = {tool.name for tool in tools.tools}
        assert names == {"search_clues", "get_clue", "list_categories"}, names

        numeric = await client.call_tool("get_clue", {"clue_id": 0})
        final = await client.call_tool("get_clue", {"clue_id": 4})
        search = await client.call_tool("search_clues", {"limit": 2})
        categories = await client.call_tool("list_categories", {"limit": 2})
        assert not numeric.is_error and numeric.structured_content is not None
        assert not final.is_error and final.structured_content is not None
        assert not search.is_error and search.structured_content is not None
        assert not categories.is_error and categories.structured_content is not None
        assert numeric.structured_content["item"]["value"] == 200
        assert final.structured_content["item"]["value"] is None
        assert len(search.structured_content["items"]) == 2
        assert len(categories.structured_content["items"]) == 2

    print(
        f"smoke test passed: REST ready, {len(names)} MCP tools, "
        "numeric and null values preserved"
    )


if __name__ == "__main__":
    asyncio.run(main())
