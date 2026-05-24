# python-ai-template

> Template — replace this README when starting a real project.

A reusable starting point for Python AI engineering projects. Comes with typed config, structured logging, an OpenAI-compatible LLM client, and a minimal but complete dev toolchain.

## Setup

```bash
# requires Python 3.11+
pip install -e .[dev]
cp .env.example .env   # then fill in OPENROUTER_API_KEY
```

## Validate

```bash
make check   # ruff + pyright + smoke test (makes a real LLM call)
```

Individual targets:

```bash
make format     # auto-format with ruff
make lint       # lint with ruff
make typecheck  # type-check with pyright
make test       # run pytest
```

## Project structure

```text
python-ai-template/
├── config.yaml              # non-secret config (model, temperature, etc.)
├── .env                     # secrets — never commit this
├── .env.example             # template for secrets
├── Makefile
├── pyproject.toml
└── src/my_project/
    ├── config.py            # Settings model + logging setup
    ├── main.py              # entrypoint
    ├── models/
    │   └── base.py          # shared Pydantic schemas + ABCs
    └── services/
        └── llm_client.py    # OpenAI-compatible LLM client
```

## Config

Two files, strict separation:

| File | What goes here |
|---|---|
| `.env` | Secrets — API keys, tokens |
| `config.yaml` | Everything else — model name, temperature, URLs |

Import and use anywhere:

```python
from my_project.config import settings

settings.openrouter_api_key   # from .env
settings.llm.default_model    # from config.yaml
settings.llm.temperature
settings.llm.max_tokens
```

Override any `config.yaml` value at runtime without touching files:

```bash
LLM__DEFAULT_MODEL=openai/gpt-4o make test
```

## Extending the template

### Add a new service (e.g. embedder)

1. Add settings to `config.py`:

```python
class EmbedderSettings(BaseModel):
    model: str
    dimensions: int

class Settings(BaseSettings):
    ...
    embedder: EmbedderSettings
```

2. Add the matching section to `config.yaml`:

```yaml
embedder:
  model: "text-embedding-3-small"
  dimensions: 1536
```

3. Add a new secret to `.env.example` / `.env` if needed, and a field to `Settings`:

```python
cohere_api_key: str   # picked up automatically from env
```

4. Implement the `BaseEmbedder` ABC from `models/base.py` in `services/`.

### Add a new LLM provider

`OpenRouterClient` uses a standard OpenAI-compatible client. To swap providers, create a new class implementing `BaseLLMClient` and point it at a different `base_url`. The rest of the codebase uses `BaseLLMClient` — nothing else changes.

### Add a new message role

Extend `MessageRole` in `models/base.py`:

```python
MessageRole = Literal["system", "user", "assistant", "tool"]
```

Then add the matching case in `llm_client.py` if the role needs special handling.

## Swapping models

Edit `config.yaml`. Any [OpenRouter-supported model](https://openrouter.ai/models) string works:

```yaml
llm:
  default_model: "anthropic/claude-3-5-sonnet"
```

No code changes needed.
