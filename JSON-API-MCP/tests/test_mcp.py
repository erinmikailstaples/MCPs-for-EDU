import pytest
from mcp import Client

from jeopardy_template.mcp_server import mcp

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


async def test_mcp_discovers_exactly_three_tools():
    async with Client(mcp) as client:
        tools = await client.list_tools()
        assert {tool.name for tool in tools.tools} == {
            "search_clues",
            "get_clue",
            "list_categories",
        }
