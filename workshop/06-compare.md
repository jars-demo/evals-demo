# Compare runs

> Save a run, change one thing, run again, and see exactly which cases moved.

**Time:** 15 minutes

## Goal

Judge a prompt or model change on evidence: case by case, not just one average.

## Save a baseline

```bash
uv run python -m triage run --model llm --save runs/before.json
```

## Change one thing

Edit the last line of `PROMPT` in `evals/triage/feature.py`, for example add:

```text
Urgency is "low" for questions, praise and feature ideas.
```

Then run again and save it under a new name:

```bash
uv run python -m triage run --model llm --save runs/after.json
```

## Compare

```bash
uv run python -m triage compare runs/before.json runs/after.json
```

The output looks like this (your cases and numbers will differ):

```text
better  invoice-copy
better  dark-mode
worse   price-question

overall  81% -> 88%
```

From `evals/triage/run.py`, the comparison adds up each case's scores in both runs:

```python
delta = sum(result.scores.values()) - old[result.id]
if delta < 0:
    lines.append(f"worse   {result.id}")
elif delta > 0:
    lines.append(f"better  {result.id}")
```

The average went up, but one case got worse. Now you can decide on purpose whether that trade is
acceptable, instead of never knowing it happened.

## Rules for fair comparisons

- Change one thing at a time: the prompt, or the model, never both.
- Same cases in both runs.
- `temperature: 0`, and if results still wobble, run each side twice.

## Check it works

`compare` prints the cases that moved and the overall score before and after.

## Exercise

Improve the offline `RulesModel` so it answers `low` for questions and praise. Compare the
baseline before and after your change.
