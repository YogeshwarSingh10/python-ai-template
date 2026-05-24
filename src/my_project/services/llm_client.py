from openai import OpenAI

from my_project import config
from my_project.models.base import BaseLLMClient, LLMResponse, Message


class OpenRouterClient(BaseLLMClient):
    """
    OpenAI-compatible client pointed at OpenRouter.
    Swap base_url to use any other OpenAI-compatible provider.
    """

    def __init__(self) -> None:
        self._client = OpenAI(
            api_key=config.OPENROUTER_API_KEY,
            base_url=config.OPENROUTER_BASE_URL,
        )

    def complete(
        self,
        messages: list[Message],
        model: str = config.DEFAULT_MODEL,
    ) -> LLMResponse:
        response = self._client.chat.completions.create(
            model=model,
            messages=[m.model_dump() for m in messages],
        )
        choice = response.choices[0]
        usage = response.usage

        return LLMResponse(
            content=choice.message.content or "",
            model=response.model,
            input_tokens=usage.prompt_tokens if usage else 0,
            output_tokens=usage.completion_tokens if usage else 0,
        )
