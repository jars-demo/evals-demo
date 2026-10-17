# Why evals

> Trying a prompt five times and liking the answers is not a test. An eval is.

**Time:** 5 minutes

## Goal

Know what an eval is, why AI features need them, and what you build in the next hour.

## Vibes do not scale

You change a prompt, try three messages, and the answers look better. Did the change help? Did
it break something you did not try? With a language model you cannot tell by looking, because:

- the same change helps some inputs and hurts others;
- models change underneath you when the provider updates them;
- the failures that matter are rare, so a handful of tries never sees them.

## An eval is a test suite for behaviour

| Part    | What it is                                          | In this workshop          |
| ------- | --------------------------------------------------- | ------------------------- |
| Cases   | real inputs with the answer you expect              | `evals/data/cases.jsonl`  |
| Feature | the code under test, including the prompt           | `evals/triage/feature.py` |
| Graders | functions that score one answer from 0 to 1         | `evals/triage/graders.py` |
| Runner  | runs every case, averages the scores, saves the run | `evals/triage/run.py`     |

Run it before and after every change, and you get a number instead of an opinion.

## The feature we evaluate

**Ticket triage.** A support message comes in; the feature returns JSON with a `category`
(`billing`, `bug`, `account`, `feature_request`, `other`) and an `urgency` (`low`, `normal`,
`high`). Small, real, and easy to get subtly wrong.

The harness is plain Python with no dependencies. It runs offline with a keyword "model", and any
OpenAI-compatible model (Groq, OpenAI, a local Ollama) plugs in with three environment variables.

## Check it works

Nothing to run yet. Read `evals/data/cases.jsonl` and guess which messages a keyword matcher will
get wrong.

## Exercise

Name one AI feature you have shipped or used that you would not trust without an eval. What would
its first five cases be?
