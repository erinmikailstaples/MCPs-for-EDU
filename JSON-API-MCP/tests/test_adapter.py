import json

import pytest

from jeopardy_template.adapter import DatasetError, load_clues


def test_rejects_boolean_as_integer(tmp_path):
    path = tmp_path / "bad.json"
    path.write_text(
        json.dumps(
            [
                {
                    "id": True,
                    "prompt": "Prompt",
                    "answer": "Answer",
                    "category": "Category",
                    "round": "Jeopardy",
                    "value": 200,
                    "gameId": 1,
                }
            ]
        )
    )
    with pytest.raises(DatasetError, match="array index 0"):
        load_clues(path)


def test_rejects_duplicate_ids(tmp_path):
    record = {
        "id": 0,
        "prompt": "Prompt",
        "answer": "Answer",
        "category": "Category",
        "round": "Jeopardy",
        "value": 200,
        "gameId": 1,
    }
    path = tmp_path / "duplicate.json"
    path.write_text(json.dumps([record, record]))
    with pytest.raises(DatasetError, match="duplicate clue id 0"):
        load_clues(path)
