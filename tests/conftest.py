import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent / "src"))

from api_client import ApiClient  # noqa: E402

RESOURCES = ["posts", "comments", "albums", "photos", "todos", "users"]


@pytest.fixture(scope="session")
def api_client():
    return ApiClient()
