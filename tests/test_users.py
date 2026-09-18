"""/users: nested-object schema validation and data integrity."""
import pytest
from jsonschema import validate

from schemas import USER_SCHEMA


@pytest.mark.schema
def test_list_users_items_match_schema(api_client):
    for user in api_client.get("/users").json():
        validate(user, USER_SCHEMA)


@pytest.mark.schema
def test_get_user_by_id_matches_schema_including_nested_objects(api_client):
    resp = api_client.get("/users/1")
    assert resp.status_code == 200
    user = resp.json()
    validate(user, USER_SCHEMA)
    assert user["address"]["geo"]["lat"]
    assert user["company"]["name"]


def test_user_emails_are_unique(api_client):
    emails = [u["email"] for u in api_client.get("/users").json()]
    assert len(emails) == len(set(emails))
