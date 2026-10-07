def test_health_confirms_data_is_loaded(api_client):
    response = api_client.get("/health")
    assert response.status_code == 200
    assert response.json() == {
        "status": "ready",
        "dataset_version": "synthetic-workshop-v1",
        "clue_count": 6,
    }


def test_search_and_exact_category_filter(api_client):
    response = api_client.get(
        "/clues",
        params={"query": "protocol", "category": "developer tools"},
    )
    assert response.status_code == 200
    body = response.json()
    assert [item["id"] for item in body["items"]] == [0, 3]
    assert body["items"][0]["value"] == 200


def test_get_preserves_null_value(api_client):
    response = api_client.get("/clues/4")
    assert response.status_code == 200
    assert response.json()["item"]["value"] is None
    assert response.json()["dataset_version"] == "synthetic-workshop-v1"


def test_missing_and_invalid_inputs_have_stable_status_codes(api_client):
    assert api_client.get("/clues/999").status_code == 404
    assert api_client.get("/clues", params={"limit": 0}).status_code == 422
    assert api_client.get("/clues", params={"round": "SemiFinal"}).status_code == 422


def test_categories_are_sorted_and_paginated(api_client):
    response = api_client.get("/categories", params={"limit": 2, "offset": 1})
    assert response.status_code == 200
    body = response.json()
    assert body["items"] == ["DEVELOPER TOOLS", "PYTHON"]
    assert body["has_more"] is True
