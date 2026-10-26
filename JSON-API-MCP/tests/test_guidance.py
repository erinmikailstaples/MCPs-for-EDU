import json
import shutil

import pytest

from jeopardy_template.guidance import (
    CONTENT_DIR,
    PROJECT_ROOT,
    GuidanceError,
    load_guidance,
    render_documentation,
)


@pytest.fixture
def content_dir(tmp_path):
    directory = tmp_path / "content"
    shutil.copytree(CONTENT_DIR, directory)
    return directory


def edit_rule(directory, task, rule_id, **changes):
    path = directory / f"{task}.json"
    raw = json.loads(path.read_text())
    next(rule for rule in raw["rules"] if rule["id"] == rule_id).update(changes)
    path.write_text(json.dumps(raw))


@pytest.mark.parametrize("value", [True, 0, 11, "3"])
def test_invalid_default_reports_file_and_rule(content_dir, value):
    edit_rule(content_dir, "practice", "practice.default_count", value=value)
    with pytest.raises(GuidanceError, match=r"practice.json.*|practice.default_count") as error:
        load_guidance("practice", content_dir)
    assert "practice.json" in str(error.value)
    assert "practice.default_count" in str(error.value) or "rules.0.value" in str(error.value)


def test_constraint_content_cannot_claim_unimplemented_behavior(content_dir):
    edit_rule(content_dir, "practice", "practice.answer_visibility", value="always_visible")
    with pytest.raises(GuidanceError, match="practice.answer_visibility"):
        load_guidance("practice", content_dir)


def test_missing_rationale_and_duplicate_rules_fail_with_location(content_dir):
    path = content_dir / "practice.json"
    original = json.loads(path.read_text())
    raw = json.loads(path.read_text())
    del raw["rules"][0]["rationale"]
    path.write_text(json.dumps(raw))
    with pytest.raises(GuidanceError, match="rationale"):
        load_guidance("practice", content_dir)
    original["rules"].append(original["rules"][0])
    path.write_text(json.dumps(original))
    with pytest.raises(GuidanceError, match="duplicate rule IDs"):
        load_guidance("practice", content_dir)


def test_content_edit_changes_description_docs_and_revision(content_dir):
    before = load_guidance("practice", content_dir)
    original = before.rules["practice.default_count"].value
    changed = 3 if original != 3 else 2
    edit_rule(content_dir, "practice", "practice.default_count", value=changed)
    after = load_guidance("practice", content_dir)
    assert after.revision != before.revision
    assert f"Start with {changed} clues" in after.description()
    assert f"Start with {changed} clues" in render_documentation(content_dir)
    assert "{value}" not in after.description()


def test_generated_docs_match_loaded_content():
    assert (PROJECT_ROOT / "PRODUCT_GUIDANCE.md").read_text() == render_documentation()
