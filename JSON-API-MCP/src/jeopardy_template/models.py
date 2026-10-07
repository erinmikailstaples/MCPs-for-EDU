"""Validated domain and API response models."""

from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field, StrictInt, field_validator


class Round(StrEnum):
    JEOPARDY = "Jeopardy"
    DOUBLE_JEOPARDY = "DoubleJeopardy"
    FINAL_JEOPARDY = "FinalJeopardy"


class Clue(BaseModel):
    model_config = ConfigDict(populate_by_name=True)

    id: StrictInt = Field(ge=0)
    prompt: str = Field(min_length=1)
    answer: str = Field(min_length=1)
    category: str = Field(min_length=1)
    round: Round
    value: StrictInt | None = Field(default=None, ge=0)
    game_id: StrictInt = Field(alias="gameId", gt=0)

    @field_validator("prompt", "answer", "category")
    @classmethod
    def reject_blank_text(cls, value: str) -> str:
        if not value.strip():
            raise ValueError("must contain non-whitespace text")
        return value


class CluePage(BaseModel):
    items: list[Clue]
    limit: int
    offset: int
    has_more: bool
    dataset_version: str


class ClueResult(BaseModel):
    item: Clue
    dataset_version: str


class CategoryPage(BaseModel):
    items: list[str]
    limit: int
    offset: int
    has_more: bool
    dataset_version: str


class HealthResponse(BaseModel):
    status: str
    dataset_version: str
    clue_count: int
