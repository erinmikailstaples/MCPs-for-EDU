"""One validated source for human documentation, tool descriptions, and defaults."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Literal

from pydantic import BaseModel, ConfigDict, Field, StrictInt, StrictStr, ValidationError

PROJECT_ROOT = Path(__file__).resolve().parents[2]
CONTENT_DIR = PROJECT_ROOT / "content"
Task = Literal["practice", "deployment"]


class GuidanceError(ValueError):
    """Content is invalid; report the file and rule instead of ignoring it."""


class ContentModel(BaseModel):
    model_config = ConfigDict(extra="forbid", str_strip_whitespace=True)


class Rule(ContentModel):
    id: str = Field(min_length=1)
    mechanism: Literal["default", "constraint", "advisory"]
    value: StrictInt | StrictStr
    recommendation: str = Field(min_length=1)
    rationale: str = Field(min_length=1)
    applies_when: str = Field(min_length=1)
    exceptions: list[str] = Field(min_length=1)
    avoid: str = Field(min_length=1)
    example_request: str = Field(min_length=1)
    example_behavior: str = Field(min_length=1)

    def render(self, text: str) -> str:
        return text.replace("{value}", str(self.value))


class GuidanceDocument(ContentModel):
    task: Task
    title: str = Field(min_length=1)
    use_when: str = Field(min_length=1)
    rules: list[Rule] = Field(min_length=1)


class RuleApplication(BaseModel):
    rule_id: str
    source: str
    source_field: str
    content_revision: str
    mechanism: str
    decision_basis: str
    configured_value: int | str
    applied_value: int | str
    recommendation: str
    rationale: str
    applies_when: str
    exceptions: list[str]


class LoadedGuidance:
    def __init__(self, path: Path, document: GuidanceDocument, revision: str):
        self.path = path
        self.document = document
        self.revision = revision
        self.rules = {rule.id: rule for rule in document.rules}

    def application(
        self,
        rule_id: str,
        applied_value: int | str | None = None,
        *,
        decision_basis: str | None = None,
    ) -> RuleApplication:
        rule = self.rules[rule_id]
        index = self.document.rules.index(rule)
        return RuleApplication(
            rule_id=rule.id,
            source=f"content/{self.path.name}",
            source_field=f"/rules/{index}/value",
            content_revision=self.revision,
            mechanism=rule.mechanism,
            decision_basis=decision_basis or rule.mechanism,
            configured_value=rule.value,
            applied_value=rule.value if applied_value is None else applied_value,
            recommendation=rule.render(rule.recommendation),
            rationale=rule.rationale,
            applies_when=rule.applies_when,
            exceptions=rule.exceptions,
        )

    def description(self) -> str:
        sections = [self.document.title, self.document.use_when]
        for rule in self.document.rules:
            sections.append(
                f"{rule.id}: {rule.render(rule.recommendation)} "
                f"Why: {rule.rationale} When: {rule.applies_when} "
                f"Exceptions: {' '.join(rule.exceptions)} Avoid: {rule.avoid} "
                f"Example: {rule.example_request} -> {rule.render(rule.example_behavior)}"
            )
        return "\n\n".join(sections)


def load_guidance(task: Task, content_dir: Path = CONTENT_DIR) -> LoadedGuidance:
    path = content_dir / f"{task}.json"
    try:
        raw = path.read_bytes()
        document = GuidanceDocument.model_validate_json(raw)
        if document.task != task:
            raise ValueError(f"task must be {task}")
        rules = {rule.id: rule for rule in document.rules}
        if len(rules) != len(document.rules):
            raise ValueError("duplicate rule IDs")
        expected = {
            "practice": {
                "practice.default_count": ("default", None),
                "practice.answer_visibility": ("constraint", "on_request"),
                "practice.difficulty": ("advisory", "board_value_proxy"),
            },
            "deployment": {
                "deployment.default_environment": ("default", None),
                "deployment.production_readiness": (
                    "constraint",
                    "confirm_nonproduction_verification",
                ),
            },
        }[task]
        if set(rules) != set(expected):
            raise ValueError(f"expected rule IDs: {', '.join(expected)}")
        for rule_id, (mechanism, value) in expected.items():
            rule = rules[rule_id]
            if rule.mechanism != mechanism or (value is not None and rule.value != value):
                raise ValueError(f"{rule_id}: handler requires {mechanism} value {value!r}")
            if any(not item.strip() for item in rule.exceptions):
                raise ValueError(f"{rule_id}: exceptions must contain text")
        if task == "practice":
            count = rules["practice.default_count"].value
            if type(count) is not int or not 1 <= count <= 10:
                raise ValueError("practice.default_count: value must be an integer from 1 to 10")
        elif rules["deployment.default_environment"].value not in {"preview", "staging"}:
            raise ValueError("deployment.default_environment: choose preview or staging")
    except (OSError, ValidationError, ValueError) as exc:
        raise GuidanceError(f"{path}: {exc}") from exc
    return LoadedGuidance(path, document, hashlib.sha256(raw).hexdigest())


def render_documentation(content_dir: Path = CONTENT_DIR) -> str:
    lines = [
        "# Product guidance",
        "",
        "Generated from `content/*.json`. Edit the source, then run "
        "`uv run --locked python scripts/render_guidance.py`.",
        "",
        "Defaults fill omitted choices. Valid user choices override defaults. "
        "Handler constraints still apply. Advisory guidance informs the agent; "
        "it does not enforce arbitrary prose as code.",
        "",
    ]
    for task in ("practice", "deployment"):
        loaded = load_guidance(task, content_dir)
        doc = loaded.document
        lines += [f"## {doc.title}", "", doc.use_when, ""]
        for rule in doc.rules:
            lines += [
                f"### {rule.id}",
                "",
                f"Source: `content/{task}.json` · Mechanism: `{rule.mechanism}`",
                "",
                rule.render(rule.recommendation),
                "",
                f"**Why:** {rule.rationale}",
                "",
                f"**When:** {rule.applies_when}",
                "",
                f"**Exceptions:** {' '.join(rule.exceptions)}",
                "",
                f"**Avoid:** {rule.avoid}",
                "",
                f"**Example request:** {rule.example_request}",
                "",
                f"**Example behavior:** {rule.render(rule.example_behavior)}",
                "",
            ]
    return "\n".join(lines)
