"""Models (chapters 02 and 05). Anything with `complete(system, user) -> str` is a model.

RulesModel runs offline with no key, so the harness works on any laptop. LLMModel talks to any
OpenAI-compatible endpoint (Groq, OpenAI, a local Ollama) using only the standard library.
"""

import json
import os
import urllib.request
from typing import Protocol


class Model(Protocol):
    name: str

    def complete(self, system: str, user: str) -> str: ...


class RulesModel:
    """A keyword baseline. Deliberately simple, so the evals have something to catch."""

    name = "rules"

    KEYWORDS = {
        "billing": ("charge", "refund", "invoice", "billed", "payment", "price"),
        "account": ("password", "log in", "login", "sign in", "2fa", "email address"),
        "bug": ("error", "crash", "broken", "doesn't work", "500", "fails"),
        "feature_request": ("would be great", "please add", "feature", "could you add"),
    }
    URGENT = ("can't", "cannot", "urgent", "blocked", "down", "lost")

    def complete(self, system: str, user: str) -> str:
        text = user.lower()
        category = next(
            (name for name, words in self.KEYWORDS.items() if any(w in text for w in words)),
            "other",
        )
        urgency = "high" if any(word in text for word in self.URGENT) else "normal"
        return json.dumps({"category": category, "urgency": urgency})


class LLMModel:
    """Any OpenAI-compatible chat completions endpoint, configured with environment variables."""

    def __init__(self, base_url: str, api_key: str, model: str, timeout: float = 30) -> None:
        self.base_url = base_url.rstrip("/")
        self.api_key = api_key
        self.name = model
        self.timeout = timeout

    @classmethod
    def from_env(cls) -> "LLMModel":
        missing = [k for k in ("LLM_BASE_URL", "LLM_MODEL") if not os.environ.get(k)]
        if missing:
            raise SystemExit(f"Set {', '.join(missing)} to use a real model (see chapter 05).")
        return cls(
            base_url=os.environ["LLM_BASE_URL"],
            api_key=os.environ.get("LLM_API_KEY", ""),
            model=os.environ["LLM_MODEL"],
        )

    def complete(self, system: str, user: str) -> str:
        body = {
            "model": self.name,
            "temperature": 0,
            "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
        }
        request = urllib.request.Request(
            f"{self.base_url}/chat/completions",
            data=json.dumps(body).encode(),
            headers={"Content-Type": "application/json", "Authorization": f"Bearer {self.api_key}"},
        )
        with urllib.request.urlopen(request, timeout=self.timeout) as response:
            data = json.load(response)
        return str(data["choices"][0]["message"]["content"])
