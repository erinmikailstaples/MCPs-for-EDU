"""Task guidance with attributable recommendations; data still comes from the API."""

from __future__ import annotations

import os
from pathlib import Path
from typing import Annotated, Literal

from mcp.server import MCPServer
from mcp.server.mcpserver.exceptions import ToolError
from mcp.types import ToolAnnotations
from pydantic import BaseModel, Field

from .api_client import APIClientError, JeopardyAPIClient
from .guidance import CONTENT_DIR, RuleApplication, Task, load_guidance

READ_ONLY = ToolAnnotations(read_only_hint=True, open_world_hint=False)


class PracticeClue(BaseModel):
    id: int
    prompt: str
    category: str
    value: int | None


class GuidanceView(BaseModel):
    task: Task
    source: str
    content_revision: str
    content: str
    rules: list[RuleApplication]


class AnswerReveal(BaseModel):
    clue_id: int
    answer: str
    dataset_version: str
    guidance: RuleApplication


class PracticeSet(BaseModel):
    items: list[PracticeClue]
    requested_count: int
    returned_count: int
    recommendation: str
    selection_note: str
    shortage: bool
    dataset_version: str
    guidance: list[RuleApplication]
    next_action: str


class DeploymentAdvice(BaseModel):
    requested_target: str | None
    recommended_target: str
    recommendation: str
    question: str | None
    guidance: list[RuleApplication]
    next_action: str
    executes_deployment: bool = False


def create_guide(
    content_dir: Path | None = None,
    *,
    tasks: tuple[Task, ...] = ("practice", "deployment"),
    api_client: JeopardyAPIClient | None = None,
) -> MCPServer:
    directory = content_dir or Path(os.environ.get("GUIDANCE_CONTENT_DIR", str(CONTENT_DIR)))
    documents = {task: load_guidance(task, directory) for task in tasks}
    server = MCPServer(
        "Product Education Guide",
        instructions=(
            "Use get_guidance for the applicable task before recommending a path. "
            "Explain recommendations using returned rationale and cite the content source and "
            "rule ID. Distinguish configured defaults from explicit user choices. "
            "Do not invent evidence, user confirmations, or universal difficulty ratings. "
            "Offer a way to verify the result and explain when the advice would change. "
            "Call reveal_answer only when the learner explicitly asks for that answer."
        ),
    )

    @server.tool(
        annotations=READ_ONLY,
        description="Retrieve task guidance before choosing a recommendation. Available tasks: "
        + ", ".join(documents),
    )
    def get_guidance(task: Task) -> GuidanceView:
        if task not in documents:
            raise ToolError(f"This server provides: {', '.join(documents)}")
        loaded = documents[task]
        return GuidanceView(
            task=task,
            source=f"content/{loaded.path.name}",
            content_revision=loaded.revision,
            content=loaded.description(),
            rules=[loaded.application(rule.id) for rule in loaded.document.rules],
        )

    if "practice" in documents:
        practice = documents["practice"]

        @server.tool(annotations=READ_ONLY, description=practice.description())
        async def build_practice_set(
            category: Annotated[str | None, Field(min_length=1)] = None,
            clue_count: Annotated[int | None, Field(ge=1, le=10)] = None,
            difficulty: Literal["beginner", "advanced"] = "beginner",
        ) -> PracticeSet:
            client = api_client or JeopardyAPIClient.from_env()
            count_rule = practice.rules["practice.default_count"]
            count = clue_count if clue_count is not None else int(count_rule.value)
            # Bound retrieval and disclose the search scope instead of claiming global difficulty.
            candidates = []
            offset = 0
            try:
                while True:
                    page = await client.search_clues(
                        query=None, category=category, round_=None, limit=50, offset=offset
                    )
                    candidates.extend(page.items)
                    if not page.has_more or len(candidates) >= 500:
                        break
                    if not page.items:
                        raise ToolError("API pagination did not advance")
                    offset += len(page.items)
            except APIClientError as exc:
                raise ToolError(str(exc)) from exc
            candidates.sort(
                key=lambda clue: (
                    clue.value is None,
                    (clue.value or 0) * (-1 if difficulty == "advanced" else 1),
                    clue.id,
                )
            )
            items = [
                PracticeClue(id=c.id, prompt=c.prompt, category=c.category, value=c.value)
                for c in candidates[:count]
            ]
            shortage = len(items) < count
            choice = "your explicit count" if clue_count is not None else "the documented default"
            note = (
                f"Ordered by {'lower' if difficulty == 'beginner' else 'higher'} board value "
                "as a rough difficulty proxy, not a measure of conceptual difficulty. "
                "Clues with no fixed board value are placed last."
            )
            if page.has_more:
                note += " Selection covers only the first 500 matching API records."
            if shortage:
                note += f" Only {len(items)} matching clues are available; filters were preserved."
            return PracticeSet(
                items=items,
                requested_count=count,
                returned_count=len(items),
                recommendation=(
                    f"Start with {len(items)} clues using {choice}; keep answers hidden."
                ),
                selection_note=note,
                shortage=shortage,
                dataset_version=page.dataset_version,
                guidance=[
                    practice.application(
                        "practice.default_count",
                        count,
                        decision_basis=(
                            "explicit_user_choice" if clue_count is not None else "default"
                        ),
                    ),
                    practice.application("practice.answer_visibility"),
                    practice.application("practice.difficulty", difficulty),
                ],
                next_action=(
                    "Try a clue, then explicitly ask to reveal its answer using its ID."
                    if items
                    else "Choose another category or relax a filter explicitly."
                ),
            )

        @server.tool(
            annotations=READ_ONLY,
            description="Reveal one clue's answer only after an explicit learner request.\n"
            + practice.rules["practice.answer_visibility"].rationale,
        )
        async def reveal_answer(clue_id: Annotated[int, Field(ge=0)]) -> AnswerReveal:
            try:
                result = await (api_client or JeopardyAPIClient.from_env()).get_clue(clue_id)
            except APIClientError as exc:
                raise ToolError(str(exc)) from exc
            return AnswerReveal(
                clue_id=result.item.id,
                answer=result.item.answer,
                dataset_version=result.dataset_version,
                guidance=practice.application("practice.answer_visibility"),
            )

    if "deployment" in documents:
        deployment = documents["deployment"]

        @server.tool(annotations=READ_ONLY, description=deployment.description())
        def recommend_deployment(
            target: Literal["preview", "staging", "production"] | None = None,
            verified_nonproduction: bool | None = None,
        ) -> DeploymentAdvice:
            default = str(deployment.rules["deployment.default_environment"].value)
            requested = target or default
            question = None
            recommended = requested
            applied = [deployment.application("deployment.default_environment", recommended)]
            if requested == "production":
                applied = []  # An explicit production choice does not apply the default.
                if verified_nonproduction is not True:
                    recommended = default
                    question = "Has this change been verified in a nonproduction environment?"
                    applied.append(
                        deployment.application("deployment.default_environment", recommended)
                    )
                applied.append(deployment.application("deployment.production_readiness"))
            elif target is not None:
                applied = [
                    deployment.application(
                        "deployment.default_environment",
                        recommended,
                        decision_basis="explicit_user_choice",
                    )
                ]
            return DeploymentAdvice(
                requested_target=target,
                recommended_target=recommended,
                recommendation=f"Use {recommended} as the next deployment step.",
                question=question,
                guidance=applied,
                next_action=(
                    "Confirm nonproduction verification before considering production."
                    if question
                    else "Verify behavior here and follow your team's release checks."
                ),
            )

    return server


if __name__ == "__main__":
    create_guide().run()
