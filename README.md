# Evals, not vibes

**A short, hands-on AI engineering workshop.** You changed a prompt and the answers look better.
Are they? Build a tiny eval harness for one LLM feature in plain Python, then compare prompts and
models with numbers instead of opinions.

[![Evals](https://github.com/jars-demo/evals-demo/actions/workflows/evals.yml/badge.svg)](https://github.com/jars-demo/evals-demo/actions/workflows/evals.yml)
[![License: MIT](https://img.shields.io/badge/license-MIT-166534.svg)](LICENSE)

Site: **[evals.jishanahmed.in](https://evals.jishanahmed.in)** · 7 chapters · about 70 minutes

## Run it

You need [uv](https://docs.astral.sh/uv/) and git.

```bash
git clone https://github.com/jars-demo/evals-demo.git
cd evals-demo/evals
uv sync
uv run python -m triage run
```

No dependencies (Python standard library only) and no API key: the first runs use an offline
keyword baseline. To evaluate a real model, set three variables for any OpenAI-compatible endpoint
(Groq, OpenAI, a local Ollama) and run `uv run python -m triage run --model llm`. Chapter 05 has
the details.

## What you build

| Part    | File                      | What it does                                            |
| ------- | ------------------------- | ------------------------------------------------------- |
| Cases   | `evals/data/cases.jsonl`  | 16 support messages with the expected triage            |
| Feature | `evals/triage/feature.py` | the prompt and the code that parses the model's JSON    |
| Models  | `evals/triage/models.py`  | an offline baseline and any OpenAI-compatible model     |
| Graders | `evals/triage/graders.py` | category, urgency, and "an urgent case is never missed" |
| Runner  | `evals/triage/run.py`     | runs, scores, saves and compares runs                   |

```bash
uv run python -m triage run --save runs/before.json   # save a run
uv run python -m triage compare runs/before.json runs/after.json
uv run python -m triage run --min-score 0.8           # exit 1 below 80%, for CI
uv run python -m triage serve                         # bring your provider, in the browser
```

`serve` opens a local page on <http://localhost:8765> where you pick a provider, check that the
URL, key and model work, and run the eval, without editing code. It listens on `127.0.0.1` only
and never stores or logs the key.

## Chapters

1. [Why evals](workshop/01-why-evals.md)
2. [Your first run](workshop/02-first-run.md)
3. [Write good cases](workshop/03-cases.md)
4. [Graders](workshop/04-graders.md)
5. [Plug in a real model](workshop/05-real-model.md)
6. [Compare runs](workshop/06-compare.md)
7. [Make it a gate](workshop/07-gate-in-ci.md)

## Layout

```text
evals/        the harness (Python, standard library only) and its tests
workshop/     the chapters
frontend/     the site (Next.js); deploy with Root Directory = frontend
```

## Checks

```bash
cd evals && uv run ruff check . && uv run pytest
cd frontend && npm ci && npm run verify && npm run test:e2e
```

## Licence

[MIT](LICENSE) · by [Jishanahmed AR Shaikh](https://github.com/jishanahmed-shaikh)
