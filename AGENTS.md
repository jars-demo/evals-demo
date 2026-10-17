# AGENTS.md

Guidance for AI coding agents and developers. Humans: start with [README.md](README.md).

## What this is

A short workshop, "Evals, not vibes": a tiny eval harness for one LLM feature (support ticket
triage). The harness in `evals/` and the chapters in `workshop/` are the product; `frontend/` is
the site.

## Map

```text
evals/triage/feature.py   PROMPT, parse() and triage(): the feature under test
evals/triage/models.py    RulesModel (offline baseline) and LLMModel (OpenAI-compatible, stdlib)
evals/triage/graders.py   graders, each (answer, expected) -> 0..1, registered in GRADERS
evals/triage/run.py       load_cases, run_eval, save/load, compare
evals/triage/__main__.py  CLI: run [--model] [--save] [--min-score], compare, serve
evals/triage/web.py       serve: local-only provider page (127.0.0.1, Host and Origin checks,
                          no logging); the page itself is web.html
evals/data/cases.jsonl    the dataset, one case per line
workshop/NN-slug.md       chapters; code quoted from evals/ must match it exactly
frontend/                 Next.js site; reads ../workshop at build time
```

## Commands

```bash
cd evals && uv sync && uv run pytest && uv run python -m triage run
cd frontend && npm ci && npm run verify
```

## Rules

1. **No runtime dependencies** in `evals/`. Standard library only, so it runs anywhere.
2. **The offline baseline stays imperfect.** Chapters rely on its failures; change cases or
   `RulesModel` and update chapters 02 and 06 in the same commit.
3. **Chapters quote real code.** A unit test checks the prompt quoted in chapter 05 and every file
   path chapters mention.
4. **Writing style.** Plain English, short sentences, no em dashes. Conventional Commits, no AI
   attribution trailers.
