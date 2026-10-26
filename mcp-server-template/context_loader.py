"""Validate task context and preserve references to the exact loaded files."""

from __future__ import annotations

import hashlib
from pathlib import Path
from typing import Annotated

from pydantic import BaseModel, ConfigDict, Field, StringConstraints, model_validator

Text = Annotated[str, StringConstraints(strip_whitespace=True, min_length=1)]
Identifier = Annotated[str, StringConstraints(pattern=r"^[a-z][a-z0-9_-]{0,63}$")]
DEFAULT_CONTEXT = Path(__file__).resolve().parent / "context"


class ContentModel(BaseModel):
    model_config = ConfigDict(extra="forbid")


class Choice(ContentModel):
    id: Identifier
    recommendation: Text
    rationale: Text
    requires: list[Identifier] = Field(default_factory=list)


class Task(ContentModel):
    id: Identifier
    title: Text
    when_to_use: Text
    default_choice: Identifier
    avoid: Text
    example_request: Text
    example_behavior: Text
    choices: list[Choice] = Field(min_length=1)
    fact_questions: dict[Identifier, Text] = Field(default_factory=dict)
    references: list[Text] = Field(default_factory=list)

    @model_validator(mode="after")
    def check_choices(self) -> Task:
        choices = {choice.id: choice for choice in self.choices}
        if len(choices) != len(self.choices):
            raise ValueError(f"{self.id}: duplicate choice IDs")
        if self.default_choice not in choices:
            raise ValueError(f"{self.id}: default_choice must name an existing choice")
        if choices[self.default_choice].requires:
            raise ValueError(f"{self.id}: default_choice must not require unconfirmed facts")
        for choice in self.choices:
            unknown = set(choice.requires) - self.fact_questions.keys()
            if unknown:
                raise ValueError(
                    f"{self.id}/{choice.id}: missing fact questions for {sorted(unknown)}"
                )
        return self


class ProductContext(ContentModel):
    product_name: Text
    tasks: list[Task] = Field(min_length=1)

    @model_validator(mode="after")
    def check_ids(self) -> ProductContext:
        if len({task.id for task in self.tasks}) != len(self.tasks):
            raise ValueError("duplicate task IDs")
        return self


class Source(BaseModel):
    file: str
    pointer: str
    revision: str


class ReferenceDocument(BaseModel):
    source: Source
    content: str


class LoadedContext:
    def __init__(self, directory: Path):
        self.directory = directory.resolve()
        manifest = self.directory / "guide.json"
        try:
            raw = manifest.read_bytes()
            self.product = ProductContext.model_validate_json(raw)
            self.revision = hashlib.sha256(raw).hexdigest()
            self.tasks = {task.id: task for task in self.product.tasks}
            self.references: dict[str, list[ReferenceDocument]] = {}
            for task in self.product.tasks:
                docs = []
                for reference in task.references:
                    path = (self.directory / reference).resolve()
                    if not path.is_relative_to(self.directory) or path.suffix != ".md":
                        raise ValueError(f"{task.id}: reference must be a Markdown file in context")
                    data = path.read_bytes()
                    docs.append(
                        ReferenceDocument(
                            source=Source(
                                file=f"context/{path.relative_to(self.directory).as_posix()}",
                                pointer="",
                                revision=hashlib.sha256(data).hexdigest(),
                            ),
                            content=data.decode("utf-8"),
                        )
                    )
                self.references[task.id] = docs
        except (OSError, ValueError) as exc:
            raise ValueError(f"Invalid context in {manifest}: {exc}") from exc

    def source(self, task: Task, field: str = "") -> Source:
        index = self.product.tasks.index(task)
        return Source(
            file="context/guide.json", pointer=f"/tasks/{index}{field}", revision=self.revision
        )

    def choice_source(self, task: Task, choice: Choice) -> Source:
        return self.source(task, f"/choices/{task.choices.index(choice)}")

    def render(self) -> str:
        lines = [
            f"# {self.product.product_name} guidance",
            "",
            "Generated from `context/guide.json` and its Markdown references. "
            "Run `uv run --locked python render_context.py` after editing context.",
            "",
        ]
        for task in self.product.tasks:
            lines += [
                f"## {task.title}",
                "",
                f"Task ID: `{task.id}`",
                "",
                task.when_to_use,
                "",
                f"Default choice: **{task.default_choice}**",
                "",
                f"Avoid: {task.avoid}",
                "",
                f"Example request: {task.example_request}",
                "",
                f"Example behavior: {task.example_behavior}",
                "",
            ]
            for choice in task.choices:
                lines += [f"### {choice.id}", "", choice.recommendation, "", choice.rationale, ""]
                for key in choice.requires:
                    lines += [f"Required confirmation: {task.fact_questions[key]}", ""]
            for reference in self.references[task.id]:
                lines += [f"Reference: `{reference.source.file}`", "", reference.content, ""]
        return "\n".join(lines)
