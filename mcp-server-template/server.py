"""A standalone MCP guide. Replace context to teach your own product decisions."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, StrictBool

from context_loader import DEFAULT_CONTEXT, LoadedContext, ReferenceDocument, Source, Task

READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)


class TaskSummary(BaseModel):
    id: str
    title: str
    when_to_use: str
    default_choice: str
    choices: list[str]


class TaskCatalog(BaseModel):
    product_name: str
    tasks: list[TaskSummary]
    source: Source


class TaskGuidance(BaseModel):
    product_name: str
    task: Task
    source: Source
    references: list[ReferenceDocument]


class RequiredConfirmation(BaseModel):
    fact: str
    question: str
    supplied_value: bool | None


class Recommendation(BaseModel):
    task_id: str
    requested_choice: str | None
    recommended_choice: str
    recommendation: str
    rationale: str
    decision_basis: Literal["default", "explicit_choice", "clarification_required"]
    unmet_requirements: list[RequiredConfirmation]
    guidance_sources: list[Source]
    reference_sources: list[Source]
    advisory_only: bool = True


def create_server(context_dir: Path = DEFAULT_CONTEXT) -> MCPServer:
    loaded = LoadedContext(context_dir)
    overview = "\n".join(
        f"{task.id}: {task.title}. Use when: {task.when_to_use} "
        f"Default: {task.default_choice}. Avoid: {task.avoid}"
        for task in loaded.product.tasks
    )
    server = MCPServer(
        f"{loaded.product.product_name} Guide",
        instructions=(
            "Discover tasks with list_tasks. Read get_guidance for the matching task before "
            "making a recommendation. Use recommend_next_step, explain the returned rationale, "
            "and cite the source file and pointer. Omit choice unless the user selected one. "
            "Pass facts only when explicitly provided; never invent confirmation. Ask the "
            "returned questions when required facts are unknown or false. "
            "This server provides advice and does not execute product operations."
        ),
    )

    def find(task_id: str) -> Task:
        if task_id not in loaded.tasks:
            raise ToolError(f"Unknown task {task_id!r}. Available IDs: {', '.join(loaded.tasks)}")
        return loaded.tasks[task_id]

    @server.tool(annotations=READ_ONLY, description="Discover product tasks.\n" + overview)
    def list_tasks() -> TaskCatalog:
        return TaskCatalog(
            product_name=loaded.product.product_name,
            tasks=[
                TaskSummary(
                    id=t.id,
                    title=t.title,
                    when_to_use=t.when_to_use,
                    default_choice=t.default_choice,
                    choices=[c.id for c in t.choices],
                )
                for t in loaded.product.tasks
            ],
            source=Source(file="context/guide.json", pointer="/tasks", revision=loaded.revision),
        )

    @server.tool(
        annotations=READ_ONLY,
        description="Read a task's choices, rationale, exceptions, questions and reference docs.\n"
        + overview,
    )
    def get_guidance(task_id: str) -> TaskGuidance:
        task = find(task_id)
        return TaskGuidance(
            product_name=loaded.product.product_name,
            task=task,
            source=loaded.source(task),
            references=loaded.references[task_id],
        )

    @server.tool(
        annotations=READ_ONLY,
        description="Recommend a next step from documented context. Valid explicit choices "
        "override the default. Unconfirmed requirements return the default and questions. "
        "Omit choice to apply the documented default. Facts must reflect user-provided evidence.\n"
        + overview,
    )
    def recommend_next_step(
        task_id: str,
        choice: str | None = None,
        facts: dict[str, StrictBool] | None = None,
    ) -> Recommendation:
        task = find(task_id)
        choices = {item.id: item for item in task.choices}
        requested = choice if choice is not None else task.default_choice
        if requested not in choices:
            raise ToolError(f"Unknown choice {requested!r}. Choose: {', '.join(choices)}")
        supplied = facts or {}
        unknown = supplied.keys() - task.fact_questions.keys()
        if unknown:
            raise ToolError(f"Unknown fact IDs: {', '.join(sorted(unknown))}")
        selected = choices[requested]
        unmet = [
            RequiredConfirmation(
                fact=key,
                question=task.fact_questions[key],
                supplied_value=supplied.get(key),
            )
            for key in selected.requires
            if supplied.get(key) is not True
        ]
        sources = [loaded.choice_source(task, selected)]
        basis = "explicit_choice" if choice is not None else "default"
        if unmet:
            selected = choices[task.default_choice]
            basis = "clarification_required"
            sources += [
                loaded.source(task, "/fact_questions"),
                loaded.choice_source(task, selected),
            ]
        if choice is None or unmet:
            sources.insert(0, loaded.source(task, "/default_choice"))
        return Recommendation(
            task_id=task_id,
            requested_choice=choice,
            recommended_choice=selected.id,
            recommendation=selected.recommendation,
            rationale=selected.rationale,
            decision_basis=basis,
            unmet_requirements=unmet,
            guidance_sources=sources,
            reference_sources=[doc.source for doc in loaded.references[task_id]],
        )

    return server


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--context", type=Path, default=DEFAULT_CONTEXT)
    parser.add_argument(
        "--check", action="store_true", help="Validate context without starting MCP"
    )
    args = parser.parse_args()
    if args.check:
        loaded = LoadedContext(args.context)
        print(f"Context ready: {loaded.product.product_name}, {len(loaded.tasks)} task(s)")
    else:
        create_server(args.context).run()


if __name__ == "__main__":
    main()
