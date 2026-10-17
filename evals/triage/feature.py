"""The feature under test (chapter 01): turn a support message into a triage decision.

The model only has to return JSON. Everything around it (the prompt, parsing, the allowed values)
is ordinary code, and that is what the evals keep honest.
"""

import json
from dataclasses import dataclass

from triage.models import Model

CATEGORIES = ("billing", "bug", "account", "feature_request", "other")
URGENCIES = ("low", "normal", "high")

PROMPT = f"""You triage customer support messages.
Reply with JSON only, no prose, in exactly this shape:
{{"category": one of {list(CATEGORIES)}, "urgency": one of {list(URGENCIES)}}}
Urgency is "high" when the customer is blocked, losing money or data, or cannot log in."""


@dataclass(frozen=True)
class Triage:
    category: str
    urgency: str


class TriageError(ValueError):
    """The model replied, but not with a usable triage decision."""


def parse(reply: str) -> Triage:
    """Turn the model's reply into a Triage, or explain exactly what was wrong with it."""
    text = reply.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        data = json.loads(text)
    except json.JSONDecodeError as error:
        raise TriageError(f"not JSON: {error.msg}") from None
    if not isinstance(data, dict):
        raise TriageError("JSON is not an object")
    category, urgency = data.get("category"), data.get("urgency")
    if category not in CATEGORIES:
        raise TriageError(f"unknown category: {category!r}")
    if urgency not in URGENCIES:
        raise TriageError(f"unknown urgency: {urgency!r}")
    return Triage(category=category, urgency=urgency)


def triage(message: str, model: Model) -> Triage:
    return parse(model.complete(system=PROMPT, user=message))
