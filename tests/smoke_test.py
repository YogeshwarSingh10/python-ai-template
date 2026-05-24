"""
Smoke test — run after any significant change to verify nothing is broken.
Keep this fast. Not a full test suite, just a sanity check.

Usage:
    python tests/smoke_test.py
"""

from my_project import config

config.setup()

logger = config.get_logger(__name__)


def test_config_loads() -> None:
    assert config.OPENROUTER_API_KEY, "OPENROUTER_API_KEY not set"
    assert config.DEFAULT_MODEL, "DEFAULT_MODEL not set"
    logger.info(f"✓ Config loaded — default model: {config.DEFAULT_MODEL}")


def test_llm_client() -> None:
    from my_project.services.llm_client import OpenRouterClient
    from my_project.models.base import Message

    client = OpenRouterClient()
    response = client.complete(
        messages=[Message(role="user", content="Reply with the word OK and nothing else.")],
        model=config.DEFAULT_MODEL,
    )
    assert response.content, "Empty response from LLM"
    logger.info(f"✓ LLM responded: {response.content!r} ({response.input_tokens} in / {response.output_tokens} out)")


if __name__ == "__main__":
    test_config_loads()
    test_llm_client()
    logger.info("All smoke tests passed.")
