import json

import pytest
from mcp import Client

from jeopardy_template.api_client import JeopardyAPIClient
from jeopardy_template.guide_server import create_guide

pytestmark = pytest.mark.anyio


@pytest.fixture
def anyio_backend():
    return "asyncio"


@pytest.fixture
def guide(api_client, monkeypatch):
    client = JeopardyAPIClient("http://testserver")

    async def get(path, params=None):
        response = api_client.get(path, params=params)
        response.raise_for_status()
        return response.json()

    monkeypatch.setattr(client, "_get", get)
    return create_guide(api_client=client)


async def invoke(client, tool, arguments):
    result = await client.call_tool(tool, arguments)
    assert not result.is_error, result.content
    assert result.structured_content is not None
    return result.structured_content


async def test_practice_uses_source_hides_answers_and_allows_explicit_reveal(guide):
    async with Client(guide) as client:
        guidance = await invoke(client, "get_guidance", {"task": "practice"})
        result = await invoke(client, "build_practice_set", {"category": "Developer Tools"})
        count = guidance["rules"][0]["configured_value"]
        assert result["requested_count"] == count
        assert result["returned_count"] == min(count, 3)
        assert [c["value"] for c in result["items"]] == [200, 800, 1200][:count]
        assert all("answer" not in item for item in result["items"])
        assert result["guidance"][0]["content_revision"] == guidance["content_revision"]
        answer = await invoke(client, "reveal_answer", {"clue_id": 0})
        assert answer["answer"] == "What is MCP?"


async def test_explicit_choice_shortage_and_no_matches_are_disclosed(guide):
    async with Client(guide) as client:
        result = await invoke(
            client,
            "build_practice_set",
            {"category": "Developer Tools", "clue_count": 1, "difficulty": "advanced"},
        )
        assert result["items"][0]["value"] == 1200
        assert result["guidance"][0]["decision_basis"] == "explicit_user_choice"
        assert "not a measure of conceptual difficulty" in result["selection_note"]
        shortage = await invoke(
            client, "build_practice_set", {"category": "Developer Tools", "clue_count": 10}
        )
        assert shortage["returned_count"] == 3 and shortage["shortage"]
        assert "filters were preserved" in shortage["selection_note"]
        empty = await invoke(client, "build_practice_set", {"category": "NO SUCH CATEGORY"})
        assert empty["items"] == [] and empty["shortage"]
        assert "Choose another category" in empty["next_action"]


async def test_null_board_value_is_preserved_and_labeled(guide):
    async with Client(guide) as client:
        result = await invoke(client, "build_practice_set", {"category": "DATA MODELING"})
        assert result["items"][0]["value"] is None
        assert "no fixed board value" in result["selection_note"]


async def test_deployment_requires_confirmation_and_reports_explicit_choices():
    async with Client(create_guide(tasks=("deployment",))) as client:
        guidance = await invoke(client, "get_guidance", {"task": "deployment"})
        default = guidance["rules"][0]["configured_value"]
        unknown = await invoke(client, "recommend_deployment", {"target": "production"})
        assert unknown["recommended_target"] == default
        assert unknown["question"] and not unknown["executes_deployment"]
        denied = await invoke(
            client,
            "recommend_deployment",
            {"target": "production", "verified_nonproduction": False},
        )
        assert denied["recommended_target"] == default
        confirmed = await invoke(
            client, "recommend_deployment", {"target": "production", "verified_nonproduction": True}
        )
        assert confirmed["recommended_target"] == "production" and not confirmed["question"]
        assert confirmed["guidance"][0]["rule_id"] == "deployment.production_readiness"
        staging = await invoke(client, "recommend_deployment", {"target": "staging"})
        assert staging["recommended_target"] == "staging"
        assert staging["guidance"][0]["decision_basis"] == "explicit_user_choice"
        unavailable = await client.call_tool("get_guidance", {"task": "practice"})
        assert unavailable.is_error


async def test_standalone_adaptation_changes_default_without_api(tmp_path):
    from jeopardy_template.guidance import CONTENT_DIR

    path = tmp_path / "deployment.json"
    raw = json.loads((CONTENT_DIR / "deployment.json").read_text())
    rule = next(r for r in raw["rules"] if r["id"] == "deployment.default_environment")
    rule["value"] = "preview"
    path.write_text(json.dumps(raw))
    before = create_guide(tmp_path, tasks=("deployment",))
    async with Client(before) as client:
        original = await invoke(client, "recommend_deployment", {})
    rule["value"] = "staging"
    path.write_text(json.dumps(raw))
    async with Client(create_guide(tmp_path, tasks=("deployment",))) as client:
        updated = await invoke(client, "recommend_deployment", {})
        assert original["recommended_target"] == "preview"
        assert updated["recommended_target"] == "staging"
        assert (
            original["guidance"][0]["content_revision"]
            != updated["guidance"][0]["content_revision"]
        )
