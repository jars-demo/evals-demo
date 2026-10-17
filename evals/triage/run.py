"""Running an eval (chapters 03, 04 and 06): cases in, scores out, saved so runs can be compared."""

import json
from dataclasses import asdict, dataclass, field
from pathlib import Path

from triage.feature import TriageError, triage
from triage.graders import GRADERS
from triage.models import Model


@dataclass
class CaseResult:
    id: str
    scores: dict[str, float]
    answer: dict[str, str] | None = None
    error: str | None = None


@dataclass
class Report:
    model: str
    results: list[CaseResult] = field(default_factory=list)

    def score(self, grader: str) -> float:
        """Mean score for one grader. A case the model failed to answer scores 0."""
        if not self.results:
            return 0.0
        return sum(r.scores.get(grader, 0.0) for r in self.results) / len(self.results)

    def overall(self) -> float:
        return sum(self.score(name) for name in GRADERS) / len(GRADERS)


def load_cases(path: Path) -> list[dict]:
    cases = []
    for number, line in enumerate(path.read_text(encoding="utf-8").splitlines(), start=1):
        if not line.strip():
            continue
        case = json.loads(line)
        for key in ("id", "message", "expected"):
            if key not in case:
                raise ValueError(f"{path.name} line {number}: missing {key!r}")
        cases.append(case)
    return cases


def run_eval(cases: list[dict], model: Model) -> Report:
    report = Report(model=model.name)
    for case in cases:
        try:
            answer = triage(case["message"], model)
        except TriageError as error:
            # A broken reply is a failed case, not a crash: it scores 0 everywhere.
            zero = dict.fromkeys(GRADERS, 0.0)
            report.results.append(CaseResult(case["id"], zero, error=str(error)))
            continue
        scores = {name: grade(answer, case["expected"]) for name, grade in GRADERS.items()}
        report.results.append(CaseResult(case["id"], scores, answer=asdict(answer)))
    return report


def save(report: Report, path: Path) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(asdict(report), indent=2) + "\n", encoding="utf-8")


def load(path: Path) -> Report:
    data = json.loads(path.read_text(encoding="utf-8"))
    return Report(model=data["model"], results=[CaseResult(**r) for r in data["results"]])


def compare(before: Report, after: Report) -> list[str]:
    """Cases that got worse or better between two runs, so a change is judged on evidence."""
    old = {r.id: sum(r.scores.values()) for r in before.results}
    lines = []
    for result in after.results:
        if result.id not in old:
            continue
        delta = sum(result.scores.values()) - old[result.id]
        if delta < 0:
            lines.append(f"worse   {result.id}")
        elif delta > 0:
            lines.append(f"better  {result.id}")
    return lines
