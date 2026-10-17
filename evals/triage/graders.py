"""Graders (chapter 04): small functions that score one answer. Each returns a value from 0 to 1.

Start with the cheapest grader that captures what you care about. Exact checks on structured
output beat a second model judging the first.
"""

from collections.abc import Callable

from triage.feature import Triage

Grader = Callable[[Triage, dict[str, str]], float]


def category_matches(answer: Triage, expected: dict[str, str]) -> float:
    return 1.0 if answer.category == expected["category"] else 0.0


def urgency_matches(answer: Triage, expected: dict[str, str]) -> float:
    return 1.0 if answer.urgency == expected["urgency"] else 0.0


def urgent_never_missed(answer: Triage, expected: dict[str, str]) -> float:
    """The costly mistake: a blocked customer marked as not urgent. Over-alerting is fine."""
    return 0.0 if expected["urgency"] == "high" and answer.urgency != "high" else 1.0


GRADERS: dict[str, Grader] = {
    "category": category_matches,
    "urgency": urgency_matches,
    "urgent_never_missed": urgent_never_missed,
}
