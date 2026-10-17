"""The command line (all chapters).

uv run python -m triage run                       # offline baseline
uv run python -m triage run --model llm           # a real model, from LLM_* variables
uv run python -m triage run --save runs/a.json --min-score 0.8
uv run python -m triage compare runs/a.json runs/b.json
"""

import argparse
import sys
from pathlib import Path

from triage.graders import GRADERS
from triage.models import LLMModel, RulesModel
from triage.run import compare, load, load_cases, run_eval, save

CASES = Path(__file__).resolve().parent.parent / "data" / "cases.jsonl"


def print_report(report) -> None:
    for result in report.results:
        mark = "PASS" if all(v == 1.0 for v in result.scores.values()) else "FAIL"
        detail = result.error or f"{result.answer['category']}, {result.answer['urgency']}"
        print(f"{mark}  {result.id:<24} {detail}")
    print()
    for name in GRADERS:
        print(f"{name:<22} {report.score(name):6.0%}")
    cases = len(report.results)
    print(f"{'overall':<22} {report.overall():6.0%}   ({report.model}, {cases} cases)")


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="triage", description="Evals for ticket triage.")
    commands = parser.add_subparsers(dest="command", required=True)
    run = commands.add_parser("run", help="run the eval")
    run.add_argument("--model", choices=["rules", "llm"], default="rules")
    run.add_argument("--cases", type=Path, default=CASES)
    run.add_argument("--save", type=Path, help="write the results as JSON")
    run.add_argument("--min-score", type=float, help="exit 1 below this overall score (0 to 1)")
    diff = commands.add_parser("compare", help="show cases that got better or worse")
    diff.add_argument("before", type=Path)
    diff.add_argument("after", type=Path)
    args = parser.parse_args(argv)

    if args.command == "compare":
        before, after = load(args.before), load(args.after)
        print("\n".join(compare(before, after)) or "No case changed.")
        print(f"\noverall  {before.overall():.0%} -> {after.overall():.0%}")
        return 0

    model = RulesModel() if args.model == "rules" else LLMModel.from_env()
    report = run_eval(load_cases(args.cases), model)
    print_report(report)
    if args.save:
        save(report, args.save)
        print(f"\nSaved to {args.save}")
    if args.min_score is not None and report.overall() < args.min_score:
        print(f"\nBelow the minimum of {args.min_score:.0%}.")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
