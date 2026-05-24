from abc import ABC, abstractmethod
from pydantic import BaseModel


# ── Shared Pydantic schemas ───────────────────────────────────────────────────

class Message(BaseModel):
    role: str
    content: str


class LLMResponse(BaseModel):
    content: str
    model: str
    input_tokens: int
    output_tokens: int

class SearchResult(BaseModel):
    id: str
    score: float
    metadata: dict


# ── ABCs ──────────────────────────────────────────────────────────────────────

class BaseLLMClient(ABC):
    @abstractmethod
    def complete(
        self,
        messages: list[Message],
        model: str,
    ) -> LLMResponse: ...


class BaseEmbedder(ABC):
    @abstractmethod
    def embed(self, text: str) -> list[float]: ...


class BaseVectorStore(ABC):
    @abstractmethod
    def upsert(self, id: str, embedding: list[float], metadata: dict) -> None: ...

    @abstractmethod
    def query(self, embedding: list[float], top_k: int) -> list[SearchResult]: ...