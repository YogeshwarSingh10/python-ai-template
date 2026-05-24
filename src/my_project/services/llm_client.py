from typing import cast

from openai import AsyncOpenAI
from openai.types.chat import ChatCompletionMessageParam

from my_project.config import settings
from my_project.models.base import (
    BaseLLMClient,
    LLMResponse,
    Message,
)


def _to_openai_messages(messages: list[Message]) -> list[ChatCompletionMessageParam]:
    return [
        cast(ChatCompletionMessageParam, {"role": msg.role, "content": msg.content})
        for msg in messages
    ]


class OpenRouterClient(BaseLLMClient):
    """
    OpenAI-compatible client pointed at OpenRouter.
    Swap base_url to use any other OpenAI-compatible provider.
    """

    def __init__(self) -> None:
        self._client = AsyncOpenAI(
            api_key=settings.openrouter_api_key,
            base_url=settings.llm.base_url,
        )

    async def complete(
        self,
        messages: list[Message],
        model: str = settings.llm.default_model,
        max_tokens: int | None = None,
    ) -> LLMResponse:
        response = await self._client.chat.completions.create(
            model=model,
            messages=_to_openai_messages(messages),
            max_tokens=max_tokens if max_tokens is not None else settings.llm.max_tokens,
            temperature=settings.llm.temperature,
        )
        choice = response.choices[0]
        usage = response.usage

        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )
