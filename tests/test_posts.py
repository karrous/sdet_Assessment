"""/posts deep dive: schema, filtering, nested routes, CRUD and negative cases.

JSONPlaceholder does not persist writes and does not validate input, so write
tests assert only against the response of the call that made the change.
"""
import pytest
from jsonschema import validate

from schemas import COMMENT_SCHEMA, POST_SCHEMA

NEW_POST = {"userId": 1, "title": "foo", "body": "bar"}


@pytest.mark.schema
def test_list_posts_items_match_schema(api_client):
    for post in api_client.get("/posts").json():
        validate(post, POST_SCHEMA)


@pytest.mark.schema
def test_get_post_by_id_matches_schema(api_client):
    validate(api_client.get("/posts/1").json(), POST_SCHEMA)


def test_get_posts_filtered_by_user_id_returns_only_that_users_posts(api_client):
    resp = api_client.get("/posts", params={"userId": 1})
    assert resp.status_code == 200
    posts = resp.json()
    assert len(posts) == 10
    assert all(p["userId"] == 1 for p in posts)


def test_get_posts_filter_with_no_match_returns_empty_list(api_client):
    resp = api_client.get("/posts", params={"userId": 999})
    assert resp.status_code == 200
    assert resp.json() == []


def test_get_post_comments_returns_comments_for_that_post(api_client):
    resp = api_client.get("/posts/1/comments")
    assert resp.status_code == 200
    comments = resp.json()
    assert len(comments) == 5
    for comment in comments:
        validate(comment, COMMENT_SCHEMA)
        assert comment["postId"] == 1


def test_create_post_returns_201_and_echoes_fields_with_generated_id(api_client):
    resp = api_client.post("/posts", json=NEW_POST)
    assert resp.status_code == 201
    assert resp.json() == {**NEW_POST, "id": 101}


def test_created_post_is_not_persisted(api_client):
    """JSONPlaceholder fakes writes: the new id is not retrievable afterwards."""
    created = api_client.post("/posts", json=NEW_POST).json()
    assert api_client.get(f"/posts/{created['id']}").status_code == 404


@pytest.mark.negative
def test_create_post_with_empty_body_is_accepted_and_only_returns_id(api_client):
    # Surprising but observed: no validation, so an empty payload still yields 201.
    resp = api_client.post("/posts", json={})
    assert resp.status_code == 201
    assert resp.json() == {"id": 101}


def test_put_post_replaces_resource_and_echoes_new_body(api_client):
    payload = {"id": 1, "userId": 1, "title": "updated", "body": "new body"}
    resp = api_client.put("/posts/1", json=payload)
    assert resp.status_code == 200
    assert resp.json() == payload


def test_patch_post_changes_only_the_patched_field(api_client):
    original = api_client.get("/posts/1").json()
    resp = api_client.patch("/posts/1", json={"title": "patched"})
    assert resp.status_code == 200
    assert resp.json() == {**original, "title": "patched"}


def test_delete_post_returns_200_and_empty_object(api_client):
    resp = api_client.delete("/posts/1")
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.negative
@pytest.mark.parametrize("post_id", ["-1", "0", "abc", "999999"])
def test_get_post_with_invalid_or_unknown_id_returns_404(api_client, post_id):
    # A strict API would return 400 for a malformed id; JSONPlaceholder returns 404.
    assert api_client.get(f"/posts/{post_id}").status_code == 404


@pytest.mark.negative
def test_update_nonexistent_post_returns_error(api_client):
    # Observed quirk: PUT on an unknown id returns 500 rather than a 404.
    resp = api_client.put("/posts/999999", json={"title": "x"})
    assert resp.status_code == 500
