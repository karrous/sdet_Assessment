# SDET Technical Assessment – API Test Automation

Automated API test suite for the [JSONPlaceholder](https://jsonplaceholder.typicode.com) REST API, built with Python, pytest, `requests` and `jsonschema`.

## Overview

The suite exercises all six JSONPlaceholder resources (`/posts`, `/comments`, `/albums`, `/photos`, `/todos`, `/users`).

- `src/api_client.py`: thin `requests.Session` wrapper (`get/post/put/patch/delete`) with a base URL and default timeout, so tests never hardcode URLs.
- `tests/conftest.py`: session-scoped `api_client` fixture and the shared list of resources.
- `tests/schemas.py`: JSON schemas for posts, comments and users (including nested `address` and `company`).
- `tests/test_contract.py`: one parametrized set of checks run against all six resources instead of six near-duplicate files.
- `tests/test_posts.py`: deep dive on `/posts` (schema, filtering, nested route, full CRUD, negative cases).
- `tests/test_crud.py`: POST / PUT / PATCH / DELETE and related negative cases, parametrized across all six resources.
- `tests/test_routes.py`: every documented nested route, unknown routes and nonexistent parents.
- `tests/test_users.py`: nested-object schema validation and data integrity for users.
- `tests/test_filters.py`: single- and multi-parameter query filtering.
- `tests/test_smoke.py`: reachability check.

### Assumptions

- JSONPlaceholder is a fake API: writes (POST/PUT/PATCH/DELETE) are echoed but **never persisted**. Tests therefore assert only on the response of the call that made the change and never depend on ordering or on earlier writes.
- The API does not validate input. Tests assert the **observed** behaviour and flag surprises in comments rather than what a strict API should do:
  - `POST /posts` with `{}` returns `201` with only a generated `id`.
  - Malformed or unknown ids (`abc`, `-1`, `0`, `999999`) return `404`, not `400`.
  - `PUT` on a nonexistent id (e.g. `/posts/999999`) returns `500`, not `404`.
  - `PATCH` returns the full resource with the patched field merged in.
- The dataset is static (100 posts, 500 comments, 100 albums, 5000 photos, 200 todos, 10 users), so counts are asserted.
- Tests need internet access to `jsonplaceholder.typicode.com`.

### Scope of testing completed

- **Contract (all 6 resources):** list is 200, a non-empty array with unique ids and the documented item count; `GET /{id}` is 200 with matching id; unknown id is 404; `Content-Type` is JSON.
- **Posts:** schema validation (list and single), `userId` filter (match and no match), `/posts/1/comments` nested route, POST / PUT / PATCH / DELETE, non-persistence of writes, and negative cases (empty body, invalid ids, update of a nonexistent post).
- **Write operations (all 6 resources):** POST (201, echoed fields, next generated id), PUT, PATCH (only the patched field changes), DELETE (200, `{}`), writes not persisted, empty POST body, PUT on a nonexistent id.
- **Routes:** all five nested routes (`/posts/{id}/comments`, `/albums/{id}/photos`, `/users/{id}/albums|todos|posts`), unknown routes (404), nested route of a nonexistent parent (empty list).
- **Users:** schema validation with nested objects, unique emails.
- **Filters:** single- and multi-parameter filters (`postId`, `userId`, `albumId`, `completed`).

## Execution Instructions

### 1. Install dependencies

Requires Python 3.10+.

```bash
python -m venv .venv --prompt sdet_Assessment
# Windows
.venv\Scripts\activate
# macOS/Linux
source .venv/bin/activate

pip install -r requirements.txt
```

### 2. Build

Not applicable: this is a pure-Python project with no compile or packaging step. Installing the dependencies is all the setup needed.

### 3. Run the test suite

```bash
pytest
```

Run a subset with markers, e.g. `pytest -m smoke`, `pytest -m negative`, `pytest -m schema`, `pytest -m contract`.

### 4. View test results

```bash
pytest --html=report.html --self-contained-html
```

Open `report.html` in a browser. On GitHub Actions the same report is published as a downloadable workflow artifact (`pytest-report`) on every push and PR (see the **Actions** tab).

## Coverage Summary

| Area | Coverage |
|---|---|
| Routes | `GET` list and by id, plus `POST`, `PUT`, `PATCH`, `DELETE`, on all 6 resources; all 5 nested routes |
| Validation types | Status codes, JSON schema (posts, comments, users), response headers, data values, list sizes, uniqueness, query-parameter filtering |
| Negative cases | Nonexistent and malformed ids, unknown routes, empty POST body, PUT on a nonexistent id, non-persistence of writes, filter with no match |

**Intentionally omitted (time box / not applicable):**

- Full JSON-schema coverage for albums, photos and todos (covered by contract-level shape checks).
- Property-based or fuzz testing, load and concurrency testing.
- Auth testing (the API has no auth).

## CI/CD

Every push and pull request to `main` runs the suite via GitHub Actions ([.github/workflows/ci.yml](.github/workflows/ci.yml)) and publishes an HTML report as a build artifact.
