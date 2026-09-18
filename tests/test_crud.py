"""Write operations (POST/PUT/PATCH/DELETE) across all six resources.

JSONPlaceholder accepts writes but never persists them, so each test asserts
only on the response of the call itself.
"""
import pytest

from conftest import RESOURCES

# resource -> (payload, field to patch, expected id of a newly created item)
WRITE_DATA = {
    "posts": ({"userId": 1, "title": "t", "body": "b"}, "title", 101),
    "comments": ({"postId": 1, "name": "n", "email": "a@b.com", "body": "b"}, "name", 501),
    "albums": ({"userId": 1, "title": "t"}, "title", 101),
    "photos": ({"albumId": 1, "title": "t", "url": "http://x/y.png", "thumbnailUrl": "http://x/t.png"}, "title", 5001),
    "todos": ({"userId": 1, "title": "t", "completed": False}, "title", 201),
    "users": ({"name": "n", "username": "u", "email": "a@b.com"}, "name", 11),
}


@pytest.mark.parametrize("resource", RESOURCES)
def test_post_creates_resource_with_echoed_fields_and_next_id(api_client, resource):
    payload, _, expected_id = WRITE_DATA[resource]
    resp = api_client.post(f"/{resource}", json=payload)
    assert resp.status_code == 201
    assert resp.json() == {**payload, "id": expected_id}


@pytest.mark.parametrize("resource", RESOURCES)
def test_put_replaces_resource_and_echoes_body(api_client, resource):
    payload, _, _ = WRITE_DATA[resource]
    resp = api_client.put(f"/{resource}/1", json=payload)
    assert resp.status_code == 200
    assert resp.json() == {**payload, "id": 1}


@pytest.mark.parametrize("resource", RESOURCES)
def test_patch_changes_only_the_patched_field(api_client, resource):
    _, field, _ = WRITE_DATA[resource]
    original = api_client.get(f"/{resource}/1").json()
    resp = api_client.patch(f"/{resource}/1", json={field: "patched"})
    assert resp.status_code == 200
    assert resp.json() == {**original, field: "patched"}


@pytest.mark.parametrize("resource", RESOURCES)
def test_delete_returns_200_and_empty_object(api_client, resource):
    resp = api_client.delete(f"/{resource}/1")
    assert resp.status_code == 200
    assert resp.json() == {}


@pytest.mark.negative
@pytest.mark.parametrize("resource", RESOURCES)
def test_writes_are_not_persisted(api_client, resource):
    payload, _, expected_id = WRITE_DATA[resource]
    api_client.post(f"/{resource}", json=payload)
    assert api_client.get(f"/{resource}/{expected_id}").status_code == 404


@pytest.mark.negative
@pytest.mark.parametrize("resource", RESOURCES)
def test_post_with_empty_body_is_accepted_and_only_returns_id(api_client, resource):
    # Surprising but observed: no input validation on any resource.
    _, _, expected_id = WRITE_DATA[resource]
    resp = api_client.post(f"/{resource}", json={})
    assert resp.status_code == 201
    assert resp.json() == {"id": expected_id}


@pytest.mark.negative
@pytest.mark.parametrize("resource", RESOURCES)
def test_put_on_nonexistent_id_returns_500(api_client, resource):
    # Observed quirk: an unknown id on PUT yields 500 rather than 404.
    resp = api_client.put(f"/{resource}/999999", json={"title": "x"})
    assert resp.status_code == 500
