# Graders

> Small functions that score one answer. Measure what actually matters.

**Time:** 10 minutes

## Goal

Read the three graders, and write one of your own.

## A grader is a function

From `evals/triage/graders.py`:

```python
def category_matches(answer: Triage, expected: dict[str, str]) -> float:
    return 1.0 if answer.category == expected["category"] else 0.0
```

It takes the answer and the expected values, and returns a score from 0 to 1.

## Measure the costly mistake

Not all errors cost the same. Marking a happy customer as urgent wastes a minute. Marking a
customer who cannot log in as low priority loses them. So one grader looks only at that:

```python
def urgent_never_missed(answer: Triage, expected: dict[str, str]) -> float:
    """The costly mistake: a blocked customer marked as not urgent. Over-alerting is fine."""
    return 0.0 if expected["urgency"] == "high" and answer.urgency != "high" else 1.0
```

Watch this number more closely than the overall score.

## Cheapest grader first

| Grader                  | Good for                              | Cost                                  |
| ----------------------- | ------------------------------------- | ------------------------------------- |
| exact match on a field  | structured output like this           | free, instant, never wrong            |
| contains or regex       | free text that must mention something | free                                  |
| a second model as judge | open-ended writing, tone              | slow, costs money, needs its own eval |

Structured output plus exact checks takes you very far. Reach for a model as judge last.

## Broken replies score zero

If the model replies with anything but valid triage JSON, `parse` raises `TriageError` and the
runner records the case as failed, with the reason, instead of crashing the run.

## Check it works

Run the tests for the harness itself: `uv run pytest`. Every test passes.

## Exercise

Add a grader `billing_never_missed` that scores 0 when a billing message is put in any other
category. Register it in `GRADERS` and see how the baseline does.

### More to try

- Write a grader that gives 0.5 when the urgency is one step off (`low` instead of `normal`) and 1 when exact.
- Remove a grader from `GRADERS`, run again, and notice how the overall score can hide a weak spot.
