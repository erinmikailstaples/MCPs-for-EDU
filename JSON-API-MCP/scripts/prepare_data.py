#!/usr/bin/env python3
"""Validate upstream combined.json and create a deterministic workshop sample."""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import tempfile
from collections import defaultdict
from pathlib import Path
from typing import Any

from pydantic import ValidationError

from jeopardy_template.adapter import DatasetError
from jeopardy_template.models import Clue, Round


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--source", type=Path, required=True)
    parser.add_argument("--output", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--source-revision", required=True)
    parser.add_argument("--limit", type=int, default=300)
    return parser.parse_args()


def validate_records(raw: Any) -> list[Clue]:
    if not isinstance(raw, list):
        raise DatasetError("source must contain a JSON array")
    clues: list[Clue] = []
    ids: set[int] = set()
    for index, record in enumerate(raw):
        try:
            clue = Clue.model_validate(record)
        except ValidationError as exc:
            raise DatasetError(f"invalid source record at index {index}: {exc}") from exc
        if clue.id in ids:
            raise DatasetError(f"duplicate source clue id {clue.id} at index {index}")
        ids.add(clue.id)
        clues.append(clue)
    return clues


def balanced_sample(clues: list[Clue], limit: int) -> list[Clue]:
    if limit < 3:
        raise DatasetError("limit must be at least 3 so every round can be represented")
    buckets: dict[Round, list[Clue]] = defaultdict(list)
    for clue in sorted(clues, key=lambda item: item.id):
        buckets[clue.round].append(clue)
    missing = [round_.value for round_ in Round if not buckets[round_]]
    if missing:
        raise DatasetError(f"source has no records for rounds: {', '.join(missing)}")

    selected: list[Clue] = []
    positions = {round_: 0 for round_ in Round}
    while len(selected) < min(limit, len(clues)):
        added = False
        for round_ in Round:
            position = positions[round_]
            if position < len(buckets[round_]) and len(selected) < limit:
                selected.append(buckets[round_][position])
                positions[round_] += 1
                added = True
        if not added:
            break
    return sorted(selected, key=lambda item: item.id)


def atomic_json_write(path: Path, value: Any) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    payload = json.dumps(value, indent=2, ensure_ascii=False) + "\n"
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_name, path)
    except BaseException:
        Path(temporary_name).unlink(missing_ok=True)
        raise


def main() -> None:
    args = parse_args()
    source_bytes = args.source.read_bytes()
    try:
        raw = json.loads(source_bytes)
    except json.JSONDecodeError as exc:
        raise DatasetError(
            f"malformed JSON: line {exc.lineno}, column {exc.colno}"
        ) from exc
    clues = validate_records(raw)
    selected = balanced_sample(clues, args.limit)
    records = [clue.model_dump(mode="json", by_alias=True) for clue in selected]
    checksum = hashlib.sha256(source_bytes).hexdigest()
    version = f"chancehl-{args.source_revision[:12]}-{checksum[:12]}"
    manifest = {
        "dataset_version": version,
        "source_kind": "chancehl/JeopardyQuestions combined.json",
        "source_repository": "https://github.com/chancehl/JeopardyQuestions",
        "source_revision": args.source_revision,
        "source_sha256": checksum,
        "source_record_count": len(clues),
        "output_record_count": len(selected),
        "selection_rule": "Ascending source ID, round-robin across all three rounds",
        "redistribution_note": "Confirm upstream rights before committing this generated output",
    }
    atomic_json_write(args.output, records)
    atomic_json_write(args.manifest, manifest)
    print(f"prepared {len(selected)} clues as dataset {version}")


if __name__ == "__main__":
    main()
