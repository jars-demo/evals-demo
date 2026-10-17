# Plug in a real model

> Point the harness at any OpenAI-compatible model and get its score.

**Time:** 10 minutes

## Goal

Run the same eval against a real language model, without changing any code.

## Three environment variables

`LLMModel` in `evals/triage/models.py` calls any OpenAI-compatible chat completions endpoint,
using only Python's standard library:

```python
body = {
    "model": self.name,
    "temperature": 0,
    "messages": [{"role": "system", "content": system}, {"role": "user", "content": user}],
}
```

`temperature: 0` makes answers as repeatable as the provider allows, which is what you want when
measuring.

Pick one provider:

```bash
# Groq (free tier): create a key at console.groq.com
export LLM_BASE_URL=https://api.groq.com/openai/v1
export LLM_API_KEY=your-key
export LLM_MODEL=openai/gpt-oss-20b

# Or a local model with Ollama, no key and no data leaves your machine
export LLM_BASE_URL=http://localhost:11434/v1
export LLM_MODEL=llama3.2
```

On Windows PowerShell use `$env:LLM_BASE_URL = "..."` instead of `export`.

## Run it

```bash
uv run python -m triage run --model llm
```

## Or bring your provider, in the browser

Prefer not to touch environment variables? Start the local page:

```bash
uv run python -m triage serve
```

Open <http://localhost:8765>, pick a provider (Groq, OpenAI, Ollama or any OpenAI-compatible
URL), paste a key, press **Check provider** to prove the URL, key and model work, then **Run
eval** for the full scorecard.

It is built for keys: from `evals/triage/web.py`, the server listens on `127.0.0.1` only, refuses
requests from other hosts or web pages, uses the key for that one request and logs nothing:

```python
def log_message(self, format: str, *args: object) -> None:
    """Stay quiet: requests can carry an API key, so nothing about them is logged."""
```

Errors come back in plain words, such as `HTTP 401: the API key was rejected` or
`HTTP 404: the base URL or the model name is wrong`.

## The prompt is part of the feature

From `evals/triage/feature.py`:

```python
PROMPT = f"""You triage customer support messages.
Reply with JSON only, no prose, in exactly this shape:
{{"category": one of {list(CATEGORIES)}, "urgency": one of {list(URGENCIES)}}}
Urgency is "high" when the customer is blocked, losing money or data, or cannot log in."""
```

Every word in it changes the score. That is exactly why you need the eval.

## Check it works

The scorecard shows your model's name in the last line, and most cases pass.

## Exercise

Run two different models from the same provider. Which one never misses an urgent case?

### More to try

- Use the Bring your provider page to compare two providers on the same cases. Which is faster, and which never misses an urgent case?
- Point the page at a wrong model name on purpose and read the error. Then try a wrong key.
