import requests

BASE_URL = "https://jsonplaceholder.typicode.com"
DEFAULT_TIMEOUT = 10


class ApiClient:
    """Thin wrapper around requests.Session for the JSONPlaceholder API."""

    def __init__(self, base_url: str = BASE_URL, timeout: int = DEFAULT_TIMEOUT):
        self.base_url = base_url
        self.timeout = timeout
        self.session = requests.Session()

    def _request(self, method: str, path: str, **kwargs) -> requests.Response:
        kwargs.setdefault("timeout", self.timeout)
        return self.session.request(method, f"{self.base_url}{path}", **kwargs)

    def get(self, path: str, **kwargs) -> requests.Response:
        return self._request("GET", path, **kwargs)

    def post(self, path: str, json: dict | None = None, **kwargs) -> requests.Response:
        return self._request("POST", path, json=json, **kwargs)

    def put(self, path: str, json: dict | None = None, **kwargs) -> requests.Response:
        return self._request("PUT", path, json=json, **kwargs)

    def patch(self, path: str, json: dict | None = None, **kwargs) -> requests.Response:
        return self._request("PATCH", path, json=json, **kwargs)

    def delete(self, path: str, **kwargs) -> requests.Response:
        return self._request("DELETE", path, **kwargs)
