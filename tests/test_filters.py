"""Query-parameter filtering (single and multiple parameters)."""
import pytest


@pytest.mark.parametrize(
    "path, params, field, value",
    [
        ("/comments", {"postId": 1}, "postId", 1),
        ("/albums", {"userId": 1}, "userId", 1),
        ("/photos", {"albumId": 1}, "albumId", 1),
        ("/todos", {"userId": 1}, "userId", 1),
    ],
)
def test_single_param_filter_returns_only_matching_items(api_client, path, params, field, value):
    resp = api_client.get(path, params=params)
    assert resp.status_code == 200
    items = resp.json()
    assert items
    assert all(item[field] == value for item in items)


def test_todos_multi_param_filter_applies_both_conditions(api_client):
    resp = api_client.get("/todos", params={"userId": 1, "completed": "true"})
    assert resp.status_code == 200
    todos = resp.json()
    assert todos
    assert all(t["userId"] == 1 and t["completed"] is True for t in todos)

