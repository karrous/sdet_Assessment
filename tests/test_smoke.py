import pytest


@pytest.mark.smoke
def test_api_is_reachable(api_client):
    assert api_client.get("/posts/1").status_code == 200
