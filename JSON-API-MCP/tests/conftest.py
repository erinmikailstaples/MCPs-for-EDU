from pathlib import Path

import pytest
from fastapi.testclient import TestClient

from jeopardy_template.api import create_app


@pytest.fixture
def api_client() -> TestClient:
    root = Path(__file__).resolve().parents[1]
    app = create_app(root / "data/clues.json", root / "data/manifest.json")
    with TestClient(app) as client:
        yield client
