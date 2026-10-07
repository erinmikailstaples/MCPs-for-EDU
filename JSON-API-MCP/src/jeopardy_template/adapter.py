"""Dataset-specific JSON loading and validation."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from .models import Clue


class DatasetError(ValueError):
    """Raised when a source dataset cannot be safely loaded."""


def load_clues(path: Path) -> list[Clue]:
    try:
        raw: Any = json.loads(path.read_text(encoding="utf-8"))
    except FileNotFoundError as exc:
        raise DatasetError(f"dataset not found: {path}") from exc
    except json.JSONDecodeError as exc:
        raise DatasetError(
            f"malformed JSON in {path}: line {exc.lineno}, column {exc.colno}"
        ) from exc

    if not isinstance(raw, list):
        raise DatasetError(f"expected a JSON array in {path}")

    clues: list[Clue] = []
    seen_ids: set[int] = set()
    for index, record in enumerate(raw):
        try:
            clue = Clue.model_validate(record)
        except ValidationError as exc:
            raise DatasetError(f"invalid clue at array index {index}: {exc}") from exc
        if clue.id in seen_ids:
            raise DatasetError(f"duplicate clue id {clue.id} at array index {index}")
        seen_ids.add(clue.id)
        clues.append(clue)

    if not clues:
        raise DatasetError(f"dataset is empty: {path}")
    return clues


def load_manifest_version(path: Path) -> str:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
        version = raw["dataset_version"]
    except (FileNotFoundError, json.JSONDecodeError, KeyError, TypeError) as exc:
        raise DatasetError(f"invalid dataset manifest: {path}") from exc
    if not isinstance(version, str) or not version.strip():
        raise DatasetError(f"manifest dataset_version must be a nonempty string: {path}")
    return version
