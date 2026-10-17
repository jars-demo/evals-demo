# Your first run

> Install, run the eval against an offline baseline, and read the scorecard.

**Time:** 10 minutes

## Goal

A first score on your screen, and an understanding of every line of it.

## Steps

1. Install [uv](https://docs.astral.sh/uv/). It installs Python and the two dev tools for you.
2. Get the code and run the eval:

   ```bash
   git clone https://github.com/jars-demo/evals-demo.git
   cd evals-demo/evals
   uv sync
   uv run python -m triage run
   ```

## Read the scorecard

```text
PASS  double-charge            billing, normal
FAIL  invoice-copy             billing, normal
FAIL  card-declined-blocked    other, normal
...
category                  69%
urgency                   38%
urgent_never_missed       94%
overall                   67%   (rules, 16 cases)
```

- Each line is one case: `PASS` only when every grader gave it full marks, then the answer given.
- Each percentage is one grader, averaged over all cases.
- `overall` is the average of the graders: one number to compare runs with.

## The baseline model

`RulesModel` in `evals/triage/models.py` matches keywords. It is deliberately simple, runs with
no key, and gives the harness something to catch:

```python
urgency = "high" if any(word in text for word in self.URGENT) else "normal"
```

It never answers `low`, which is why urgency scores so badly. The scorecard told you that in one
glance, without reading a single answer.

## Check it works

You see 16 case lines and an overall score of 67%.

## Exercise

Find the case where the baseline missed a high-urgency message (`urgent_never_missed` is below
100%). Why did the keywords miss it?
