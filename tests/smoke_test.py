"""
Smoke test — run after any significant change to verify nothing is broken.
Keep this fast. Not a full test suite, just a sanity check.

Usage:
    python tests/smoke_test.py
"""

import asyncio

from my_project.config import get_logger, settings, setup_logging

setup_logging()

logger = get_logger(__name__)


def test_config_loads() -> None:
    assert settings.openrouter_api_key, "OPENROUTER_API_KEY not set"
    assert settings.llm.default_model, "llm.default_model not set"
    logger.info(f"✓ Config loaded — default model: {settings.llm.default_model}")


async def test_llm_client() -> None:
    from my_project.models.base import Message
    from my_project.services.llm_client import OpenRouterClient

    client = OpenRouterClient()
    response = await client.complete(
        messages=[Message(role="user", content="Reply with the word OK and nothing else.")],
        model=settings.llm.default_model,
        max_tokens=16,
    )
    assert response.content, "Empty response from LLM"
    logger.info(f"✓ LLM responded: {response.content!r} ({response.input_tokens} in / {response.output_tokens} out)")


if __name__ == "__main__":
    test_config_loads()
    asyncio.run(test_llm_client())
    logger.info("All smoke tests passed.")
