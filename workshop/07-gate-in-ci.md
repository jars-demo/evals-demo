# Make it a gate

> Fail the build when the score drops below a line you choose.

**Time:** 10 minutes

## Goal

Run the eval on every change, automatically, and block changes that make the feature worse.

## A minimum score

`--min-score` makes the command exit with code 1 below a threshold, which fails any CI job:

```python
if args.min_score is not None and report.overall() < args.min_score:
    print(f"\nBelow the minimum of {args.min_score:.0%}.")
    return 1
```

```bash
uv run python -m triage run --min-score 0.6
```

## In GitHub Actions

This repository's `.github/workflows/evals.yml` runs the tests and the offline eval on every
change:

```yaml
- name: Eval (offline baseline)
  run: uv run python -m triage run --min-score 0.6 --save runs/ci.json
```

To gate a real model, store the key as a repository secret and pass it in:

```yaml
- name: Eval (real model)
  env:
    LLM_BASE_URL: https://api.groq.com/openai/v1
    LLM_API_KEY: ${{ secrets.LLM_API_KEY }}
    LLM_MODEL: openai/gpt-oss-20b
  run: uv run python -m triage run --model llm --min-score 0.85
```

## Choosing the line

- Start just below today's score, so the gate only catches regressions.
- Raise it as the feature improves. Never lower it quietly.
- Gate the costly grader separately if it matters most, like `urgent_never_missed`.

## Check it works

Run `uv run python -m triage run --min-score 0.99`. It prints the scorecard, then `Below the
minimum of 99%.` and `echo $?` prints `1`.

## Exercise

You made it. Pick one AI feature of your own, write ten cases and one grader, and run it twice:
once before and once after a prompt change.
