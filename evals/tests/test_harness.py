"""Tests for the harness itself: if the ruler is wrong, every measurement is wrong."""

import json
from pathlib import Path

import pytest

from triage.__main__ import CASES, main
from triage.feature import Triage, TriageError, parse
from triage.graders import category_matches, urgent_never_missed
from triage.run import compare, load, load_cases, run_eval, save


class FixedModel:
    """A model that always gives the same reply, so tests are deterministic."""

    def __init__(self, reply: str) -> None:
        self.name = "fixed"
        self.reply = reply

    def complete(self, system: str, user: str) -> str:
        return self.reply


def test_parse_accepts_json_in_a_code_fence() -> None:
    assert parse('```json\n{"category": "bug", "urgency": "high"}\n```') == Triage("bug", "high")


@pytest.mark.parametrize(
    ("reply", "problem"),
    [
        ("Sure! It's a bug.", "not JSON"),
        ("[1, 2]", "not an object"),
        ('{"category": "spam", "urgency": "low"}', "unknown category"),
        ('{"category": "bug", "urgency": "asap"}', "unknown urgency"),
    ],
)
def test_parse_explains_unusable_replies(reply: str, problem: str) -> None:
    with pytest.raises(TriageError, match=problem):
        parse(reply)


def test_urgent_never_missed_only_punishes_missed_urgency() -> None:
    urgent = {"category": "bug", "urgency": "high"}
    calm = {"category": "bug", "urgency": "low"}

    assert urgent_never_missed(Triage("bug", "normal"), urgent) == 0.0
    assert urgent_never_missed(Triage("bug", "high"), calm) == 1.0


def test_a_broken_reply_scores_zero_instead_of_crashing() -> None:
    cases = [{"id": "a", "message": "hi", "expected": {"category": "other", "urgency": "low"}}]

    report = run_eval(cases, FixedModel("not json"))

    assert report.overall() == 0.0
    assert report.results[0].error is not None


def test_a_perfect_model_scores_100_percent() -> None:
    cases = [{"id": "a", "message": "hi", "expected": {"category": "other", "urgency": "low"}}]

    report = run_eval(cases, FixedModel('{"category": "other", "urgency": "low"}'))

    assert report.overall() == 1.0
    assert category_matches(Triage("other", "low"), cases[0]["expected"]) == 1.0


def test_load_cases_names_the_broken_line(tmp_path: Path) -> None:
    bad = tmp_path / "cases.jsonl"
    bad.write_text('{"id": "a", "message": "hi"}\n')

    with pytest.raises(ValueError, match="line 1: missing 'expected'"):
        load_cases(bad)


def test_the_dataset_is_valid_and_ids_are_unique() -> None:
    cases = load_cases(CASES)

    assert len(cases) >= 15
    assert len({case["id"] for case in cases}) == len(cases)


def test_saved_runs_round_trip_and_compare(tmp_path: Path) -> None:
    cases = load_cases(CASES)
    good = run_eval(cases, FixedModel('{"category": "other", "urgency": "low"}'))
    bad = run_eval(cases, FixedModel("nope"))
    save(good, tmp_path / "good.json")

    assert load(tmp_path / "good.json").overall() == good.overall()
    assert "worse   thanks" in compare(good, bad)


def test_min_score_fails_the_command(capsys: pytest.CaptureFixture[str]) -> None:
    assert main(["run", "--min-score", "1.0"]) == 1
    assert "Below the minimum" in capsys.readouterr().out


def test_the_baseline_runs_offline_and_saves(tmp_path: Path) -> None:
    out = tmp_path / "baseline.json"

    assert main(["run", "--save", str(out)]) == 0
    assert json.loads(out.read_text())["model"] == "rules"
