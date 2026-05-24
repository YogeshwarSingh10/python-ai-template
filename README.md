# my-project

## Setup

```bash
conda activate ai-engineering
pip install -e .
cp .env.example .env   # fill in OPENROUTER_API_KEY
```

## Run

```bash
python src/my_project/main.py
```

## Validate after changes

```bash
pyright src/                   # type check
python tests/smoke_test.py     # smoke test (makes a real LLM call)
```

## Structure

```text
src/my_project/
├── config.py        # single bootstrap — env loading + logging setup
├── main.py          # entry point, call config.setup() first
├── core/            # business logic, no external calls
├── services/        # external integrations (LLM, vector store, embedder)
│   └── llm_client.py
├── models/          # pydantic schemas + ABCs
│   └── base.py
└── utils/           # pure stateless helpers
```

## Swapping models

Change `DEFAULT_MODEL` in `.env`. Any OpenRouter-supported model string works.
See [OpenRouter models](https://openrouter.ai/models) for available models.
