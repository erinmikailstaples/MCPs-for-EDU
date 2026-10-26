import asyncio
import json
import shutil
import subprocess
import sys
from pathlib import Path

import pytest
from mcp import Client

from context_loader import DEFAULT_CONTEXT, LoadedContext
from server import create_server


@pytest.fixture
def context_dir(tmp_path):
    directory = tmp_path / "context"
    shutil.copytree(DEFAULT_CONTEXT, directory)
    return directory


def edit(directory, mutate):
    path = directory / "guide.json"
    raw = json.loads(path.read_text())
    mutate(raw)
    path.write_text(json.dumps(raw))


def test_invalid_default_and_missing_questions_report_context(context_dir):
    edit(context_dir, lambda raw: raw["tasks"][0].update(default_choice="not-an-option"))
    with pytest.raises(ValueError, match="guide.json.*|default_choice") as error:
        LoadedContext(context_dir)
    assert "default_choice" in str(error.value)
    edit(
        context_dir, lambda raw: raw["tasks"][0].update(default_choice="preview", fact_questions={})
    )
    with pytest.raises(ValueError, match="missing fact questions"):
        LoadedContext(context_dir)


def test_references_cannot_escape_context_directory(context_dir):
    (context_dir.parent / "outside.md").write_text("outside")
    edit(context_dir, lambda raw: raw["tasks"][0].update(references=["../outside.md"]))
    with pytest.raises(ValueError, match="Markdown file in context"):
        LoadedContext(context_dir)


def test_default_cannot_depend_on_unconfirmed_facts(context_dir):
    edit(context_dir, lambda raw: raw["tasks"][0].update(default_choice="production"))
    with pytest.raises(ValueError, match="default_choice must not require"):
        LoadedContext(context_dir)


def test_duplicate_task_ids_fail(context_dir):
    edit(context_dir, lambda raw: raw["tasks"].append(raw["tasks"][0]))
    with pytest.raises(ValueError, match="duplicate task IDs"):
        LoadedContext(context_dir)


def test_context_edit_changes_docs_and_trace(context_dir):
    original = LoadedContext(context_dir)
    edit(context_dir, lambda raw: raw["tasks"][0].update(default_choice="staging"))
    updated = LoadedContext(context_dir)
    assert updated.revision != original.revision
    assert "Default choice: **staging**" in updated.render()
    assert "product.md" in updated.render()


def test_protocol_handles_unknown_choices_false_facts_and_user_overrides(context_dir):
    async def check():
        async with Client(create_server(context_dir)) as client:
            override = await client.call_tool(
                "recommend_next_step", {"task_id": "deploy", "choice": "staging"}
            )
            assert override.structured_content["decision_basis"] == "explicit_choice"
            assert override.structured_content["recommended_choice"] == "staging"
            false = await client.call_tool(
                "recommend_next_step",
                {
                    "task_id": "deploy",
                    "choice": "production",
                    "facts": {"verified_nonproduction": False},
                },
            )
            result = false.structured_content
            assert result["recommended_choice"] == "preview"
            assert result["unmet_requirements"][0]["supplied_value"] is False
            for arguments in [
                {"task_id": "unknown"},
                {"task_id": "deploy", "choice": "unknown"},
                {"task_id": "deploy", "facts": {"unknown_fact": True}},
                {"task_id": "deploy", "facts": {"verified_nonproduction": "yes"}},
            ]:
                error = await client.call_tool("recommend_next_step", arguments)
                assert error.is_error

    asyncio.run(check())


def test_human_docs_match_context():
    assert (Path(__file__).resolve().parents[1] / "CONTEXT_GUIDE.md").read_text() == (
        LoadedContext(DEFAULT_CONTEXT).render()
    )


def test_copy_helper_excludes_env_and_preserves_existing_files(tmp_path):
    source = tmp_path / "source"
    source.mkdir()
    helper = source / "copy_template.py"
    shutil.copy2(Path(__file__).resolve().parents[1] / "copy_template.py", helper)
    (source / ".venv").mkdir()
    (source / ".venv/generated").write_text("do not copy")
    (source / "server.py").write_text("user source")
    destination = tmp_path / "copied"
    command = [sys.executable, str(helper), str(destination)]
    subprocess.run(command, check=True, capture_output=True)
    assert (destination / "server.py").read_text() == "user source"
    assert not (destination / ".venv").exists()
    (destination / "server.py").write_text("preserve my edits")
    assert subprocess.run(command, capture_output=True).returncode != 0
    assert (destination / "server.py").read_text() == "preserve my edits"
    nested = subprocess.run(
        [sys.executable, str(helper), str(source / "nested")], capture_output=True
    )
    assert nested.returncode != 0 and not (source / "nested").exists()
