from abc import ABC, abstractmethod
from typing import Literal

from pydantic import BaseModel

MessageRole = Literal["system", "user", "assistant"]

# ── Shared Pydantic schemas ───────────────────────────────────────────────────


class Message(BaseModel):
    role: MessageRole
    content: str


class LLMResponse(BaseModel):
    content: str
    model: str
    input_tokens: int
    output_tokens: int


class SearchResult(BaseModel):
    id: str
    score: float
    metadata: dict[str, object]


# ── ABCs ──────────────────────────────────────────────────────────────────────


class BaseLLMClient(ABC):
    @abstractmethod
    async def complete(
        self,
        messages: list[Message],
        model: str,
        max_tokens: int | None = None,
    ) -> LLMResponse: ...


class BaseEmbedder(ABC):
    @abstractmethod
    async def embed(self, text: str) -> list[float]: ...


class BaseVectorStore(ABC):
    @abstractmethod
    async def upsert(self, id: str, embedding: list[float], metadata: dict[str, object]) -> None: ...

    @abstractmethod
    async def query(self, embedding: list[float], top_k: int) -> list[SearchResult]: ...
