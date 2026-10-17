"""The bring-your-provider server: local only, clear errors, and a real run of the baseline."""

import json
import threading
import urllib.error
import urllib.request
from collections.abc import Iterator
from http.server import ThreadingHTTPServer

import pytest

from triage.web import Handler, model_from, provider_error


@pytest.fixture
def server() -> Iterator[str]:
    httpd = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
    thread = threading.Thread(target=httpd.serve_forever, daemon=True)
    thread.start()
    yield f"http://127.0.0.1:{httpd.server_address[1]}"
    httpd.shutdown()
    httpd.server_close()


def call(url: str, body: dict | None = None, headers: dict | None = None) -> tuple[int, dict | str]:
    data = None if body is None else json.dumps(body).encode()
    request = urllib.request.Request(url, data=data, headers=headers or {})
    if data is not None:
        request.add_header("Content-Type", "application/json")
    try:
        with urllib.request.urlopen(request) as response:
            raw = response.read().decode()
            return response.status, raw if raw.startswith("<!") else json.loads(raw)
    except urllib.error.HTTPError as error:
        return error.code, json.loads(error.read().decode())


def test_the_page_is_served_locally(server: str) -> None:
    status, body = call(f"{server}/")

    assert status == 200
    assert "Bring your provider" in str(body)


def test_requests_from_another_host_or_page_are_refused(server: str) -> None:
    assert call(f"{server}/", headers={"Host": "evil.example"})[0] == 403
    assert call(f"{server}/api/run", {}, headers={"Origin": "https://evil.example"})[0] == 403


def test_running_the_offline_baseline_returns_a_scorecard(server: str) -> None:
    status, body = call(f"{server}/api/run", {"provider": "baseline"})

    assert status == 200
    assert isinstance(body, dict)
    assert body["model"] == "rules"
    assert len(body["results"]) == 16
    assert 0 < body["overall"] < 1


def test_a_bad_provider_config_is_a_400_with_a_reason(server: str) -> None:
    status, body = call(f"{server}/api/check", {"base_url": "ftp://x", "model": "m"})

    assert status == 400
    assert isinstance(body, dict)
    assert "base URL" in body["error"]


def test_an_unreachable_provider_is_a_502_with_a_reason(server: str) -> None:
    unreachable = {"base_url": "http://127.0.0.1:9", "model": "m", "api_key": "secret-key"}

    status, body = call(f"{server}/api/check", unreachable)

    assert status == 502
    assert isinstance(body, dict)
    assert "could not reach" in body["error"]
    assert "secret-key" not in json.dumps(body)


def test_model_from_needs_a_url_and_a_model() -> None:
    with pytest.raises(ValueError):
        model_from({"base_url": "https://api.example.com/v1", "model": ""})


def test_provider_errors_explain_common_http_failures() -> None:
    rejected = urllib.error.HTTPError("https://x", 401, "Unauthorized", {}, None)  # type: ignore[arg-type]

    assert provider_error(rejected) == "HTTP 401: the API key was rejected"


def test_a_missing_key_is_named_as_the_problem() -> None:
    forbidden = urllib.error.HTTPError("https://x", 403, "Forbidden", {}, None)  # type: ignore[arg-type]

    assert "no API key was given" in provider_error(forbidden, has_key=False)
