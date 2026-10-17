"""Bring your provider (chapter 05): a small local page to check a model provider and run the eval
against it, without editing code.

It listens on 127.0.0.1 only and refuses requests from other hosts or web pages. The API key you
type is used for that one request and kept nowhere: not on disk, not in logs.
"""

import json
import time
import urllib.error
from dataclasses import asdict
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path

from triage.graders import GRADERS
from triage.models import LLMModel, RulesModel
from triage.run import load_cases, run_eval

PAGE = Path(__file__).with_name("web.html")
CASES = Path(__file__).resolve().parent.parent / "data" / "cases.jsonl"
MAX_BODY = 10_000
LOCAL_HOSTS = ("127.0.0.1", "localhost")

HINTS = {
    401: "the API key was rejected",
    403: "this key may not use this model",
    404: "the base URL or the model name is wrong",
    429: "rate limited, wait a moment and try again",
}


def provider_error(error: Exception, has_key: bool = True) -> str:
    """A short, useful explanation of why a provider call failed."""
    if isinstance(error, urllib.error.HTTPError) and error.code in (401, 403) and not has_key:
        return f"HTTP {error.code}: no API key was given, and this provider needs one"
    if isinstance(error, urllib.error.HTTPError):
        return f"HTTP {error.code}: {HINTS.get(error.code, error.reason)}"
    if isinstance(error, urllib.error.URLError):
        return f"could not reach the provider ({error.reason})"
    if isinstance(error, TimeoutError):
        return "the provider took too long to answer"
    return f"unexpected reply from the provider ({type(error).__name__})"


def model_from(body: dict) -> LLMModel:
    base_url = str(body.get("base_url", "")).strip()
    model = str(body.get("model", "")).strip()
    if not base_url.startswith(("http://", "https://")) or not model:
        raise ValueError("Give a base URL starting with http:// or https:// and a model name.")
    return LLMModel(base_url=base_url, api_key=str(body.get("api_key", "")), model=model)


def check(body: dict) -> dict:
    """One tiny request, to prove the URL, key and model work before running the whole eval."""
    model = model_from(body)
    started = time.perf_counter()
    reply = model.complete(system="Reply with the single word: ok", user="ping")
    return {
        "model": model.name,
        "ms": round((time.perf_counter() - started) * 1000),
        "reply": reply.strip()[:80],
    }


def evaluate(body: dict) -> dict:
    model = RulesModel() if body.get("provider") == "baseline" else model_from(body)
    report = run_eval(load_cases(CASES), model)
    return {
        "model": report.model,
        "overall": report.overall(),
        "scores": {name: report.score(name) for name in GRADERS},
        "results": [asdict(result) for result in report.results],
    }


class Handler(BaseHTTPRequestHandler):
    def _is_local(self) -> bool:
        # Host and Origin checks stop other web pages (and DNS tricks) from using this server.
        host = self.headers.get("Host", "").rsplit(":", 1)[0]
        origin = self.headers.get("Origin")
        same_origin = origin is None or origin.startswith(
            tuple(f"http://{name}:" for name in LOCAL_HOSTS)
        )
        return host in LOCAL_HOSTS and same_origin

    def _send(self, status: int, body: object, content_type: str = "application/json") -> None:
        data = body if isinstance(body, bytes) else json.dumps(body).encode()
        self.send_response(status)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(data)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        self.end_headers()
        self.wfile.write(data)

    def do_GET(self) -> None:
        if not self._is_local():
            return self._send(403, {"error": "local requests only"})
        if self.path == "/":
            return self._send(200, PAGE.read_bytes(), "text/html; charset=utf-8")
        return self._send(404, {"error": "not found"})

    def do_POST(self) -> None:
        if not self._is_local():
            return self._send(403, {"error": "local requests only"})
        body: dict = {}
        length = int(self.headers.get("Content-Length") or 0)
        if length > MAX_BODY:
            return self._send(413, {"error": "request too large"})
        try:
            body = json.loads(self.rfile.read(length) or b"{}")
            if not isinstance(body, dict):
                raise ValueError("send a JSON object")
            if self.path == "/api/check":
                return self._send(200, check(body))
            if self.path == "/api/run":
                return self._send(200, evaluate(body))
            return self._send(404, {"error": "not found"})
        except ValueError as error:
            return self._send(400, {"error": str(error)})
        except Exception as error:  # a provider failure, explained without echoing secrets
            has_key = bool(body.get("api_key"))
            return self._send(502, {"error": provider_error(error, has_key)})

    def log_message(self, format: str, *args: object) -> None:
        """Stay quiet: requests can carry an API key, so nothing about them is logged."""


def serve(port: int) -> None:
    server = ThreadingHTTPServer(("127.0.0.1", port), Handler)
    print(f"Bring your provider: http://localhost:{port}   (Ctrl+C to stop)")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        pass
    finally:
        server.server_close()
