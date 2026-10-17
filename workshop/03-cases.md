# Write good cases

> The dataset is the eval. Real, varied cases with clear expected answers.

**Time:** 10 minutes

## Goal

Know what makes a good case, and add your own.

## One case per line

`evals/data/cases.jsonl` holds one JSON object per line:

```text
{"id": "api-500", "message": "Your API returns 500 for every request since 9am. Production is down.", "expected": {"category": "bug", "urgency": "high"}}
```

- `id`: short and stable, so you can follow one case across runs.
- `message`: the real input, as a customer would write it.
- `expected`: the answer a careful human would give.

## What makes a good set

- **Real.** Copy from real tickets (with personal data removed), not from your imagination.
- **Varied.** Every category, every urgency, short and long, polite and angry.
- **Tricky on purpose.** `card-declined-blocked` is about billing, but the customer is blocked, so
  it is urgent. Cases like that are where features fail.
- **Agreed.** If two people disagree on the expected answer, fix the definitions first.

Start with 15 to 50 cases. A small, honest set beats a big generated one.

## The loader protects you

```python
for key in ("id", "message", "expected"):
    if key not in case:
        raise ValueError(f"{path.name} line {number}: missing {key!r}")
```

A broken line fails loudly with its line number, instead of quietly lowering the score.

## Check it works

Add this line to `cases.jsonl` and run the eval again:

```text
{"id": "refund-angry", "message": "This is the third time I ask: REFUND my last payment now.", "expected": {"category": "billing", "urgency": "normal"}}
```

You now see 17 cases.

## Exercise

Add two cases that you expect the baseline to get wrong, and check that it does.
