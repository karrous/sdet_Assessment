"""Route discovery: nested routes, unknown routes and unsupported methods."""
import pytest

NESTED_ROUTES = [
    ("/posts/1/comments", "postId"),
    ("/albums/1/photos", "albumId"),
    ("/users/1/albums", "userId"),
    ("/users/1/todos", "userId"),
    ("/users/1/posts", "userId"),
]


@pytest.mark.parametrize("path, owner_field", NESTED_ROUTES)
def test_nested_route_returns_only_items_of_parent(api_client, path, owner_field):
    resp = api_client.get(path)
    assert resp.status_code == 200
    items = resp.json()
    assert items
    assert all(item[owner_field] == 1 for item in items)


@pytest.mark.negative
@pytest.mark.parametrize("path", ["/unknown", "/posts/1/unknown"])
def test_unknown_route_returns_404(api_client, path):
    assert api_client.get(path).status_code == 404


@pytest.mark.negative
@pytest.mark.parametrize("path", ["/posts/1/comments", "/users/1/todos"])
def test_nested_route_for_nonexistent_parent_returns_empty_list(api_client, path):
    resp = api_client.get(path.replace("/1/", "/999999/"))
    assert resp.status_code == 200
    assert resp.json() == []
