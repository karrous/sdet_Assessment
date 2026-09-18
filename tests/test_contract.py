"""Cross-resource contract tests, parametrized over all six resources."""
import pytest

from conftest import RESOURCES

pytestmark = pytest.mark.contract


@pytest.mark.parametrize("resource", RESOURCES)
def test_list_returns_200_and_non_empty_array(api_client, resource):
    resp = api_client.get(f"/{resource}")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, list)
    assert len(body) > 0


@pytest.mark.parametrize("resource", RESOURCES)
def test_get_by_id_returns_200_and_matching_id(api_client, resource):
    resp = api_client.get(f"/{resource}/1")
    assert resp.status_code == 200
    body = resp.json()
    assert isinstance(body, dict)
    assert body["id"] == 1


@pytest.mark.negative
@pytest.mark.parametrize("resource", RESOURCES)
def test_get_nonexistent_id_returns_404(api_client, resource):
    resp = api_client.get(f"/{resource}/999999")
    assert resp.status_code == 404


@pytest.mark.parametrize("resource", RESOURCES)
def test_responses_are_json(api_client, resource):
    resp = api_client.get(f"/{resource}/1")
    assert resp.headers["Content-Type"].startswith("application/json")


@pytest.mark.parametrize("resource", RESOURCES)
def test_list_ids_are_unique(api_client, resource):
    ids = [item["id"] for item in api_client.get(f"/{resource}").json()]
    assert len(ids) == len(set(ids))


@pytest.mark.parametrize(
    "resource, expected_count",
    [("posts", 100), ("comments", 500), ("albums", 100), ("photos", 5000), ("todos", 200), ("users", 10)],
)
def test_list_returns_documented_number_of_items(api_client, resource, expected_count):
    assert len(api_client.get(f"/{resource}").json()) == expected_count
