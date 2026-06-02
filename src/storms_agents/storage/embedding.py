import hashlib
import math
from dataclasses import dataclass
from typing import Any, Protocol

from storms_agents.config import Settings, get_settings

EMBEDDING_DIMENSIONS = 768
DEMO_EMBEDDING_MODEL = "demo-hash-embedding-768"
DEFAULT_EMBEDDING_TASK_TYPE = "RETRIEVAL_DOCUMENT"


class EmbeddingProviderProtocol(Protocol):
    @property
    def status(self) -> "EmbeddingStatus":
        """Return the configured embedding runtime."""

    def embed_document(self, text: str) -> "GeneratedEmbedding":
        """Embed book/source text."""

    def embed_query(self, text: str) -> "GeneratedEmbedding":
        """Embed a retrieval query."""


@dataclass(frozen=True)
class EmbeddingStatus:
    mode: str
    model: str
    dimensions: int
    vertexai: bool
    configured: bool


@dataclass(frozen=True)
class GeneratedEmbedding:
    vector: list[float]
    model: str
    mode: str


def demo_embedding(text: str, dimensions: int = EMBEDDING_DIMENSIONS) -> list[float]:
    vector = [0.0] * dimensions
    words = [word.strip(".,?!:;()[]{}\"'").lower() for word in text.split()]
    for word in words:
        if len(word) < 3:
            continue
        digest = hashlib.sha256(word.encode("utf-8")).digest()
        index = int.from_bytes(digest[:4], "big") % dimensions
        sign = 1.0 if digest[4] % 2 == 0 else -1.0
        vector[index] += sign

    norm = math.sqrt(sum(value * value for value in vector))
    if norm == 0:
        return vector
    return [round(value / norm, 6) for value in vector]


def vector_literal(vector: list[float]) -> str:
    return "[" + ",".join(f"{value:.6f}" for value in vector) + "]"


class EmbeddingProvider:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: Any | None = None

    @property
    def status(self) -> EmbeddingStatus:
        configured = bool(self.settings.google_api_key) or bool(self.settings.google_cloud_project)
        return EmbeddingStatus(
            mode="gemini-embedding" if configured else "demo-fallback",
            model=self.settings.gemini_embedding_model if configured else DEMO_EMBEDDING_MODEL,
            dimensions=EMBEDDING_DIMENSIONS,
            vertexai=self.settings.google_genai_use_vertexai,
            configured=configured,
        )

    def embed_document(self, text: str) -> GeneratedEmbedding:
        return self._embed(text, task_type=DEFAULT_EMBEDDING_TASK_TYPE)

    def embed_query(self, text: str) -> GeneratedEmbedding:
        return self._embed(text, task_type="RETRIEVAL_QUERY")

    def _embed(self, text: str, *, task_type: str) -> GeneratedEmbedding:
        if not self.status.configured:
            return self._fallback(text)

        try:
            from google.genai import types

            response = self._get_client().models.embed_content(
                model=self.settings.gemini_embedding_model,
                contents=text,
                config=types.EmbedContentConfig(
                    taskType=task_type,
                    outputDimensionality=EMBEDDING_DIMENSIONS,
                ),
            )
            embedding = response.embeddings[0].values
        except Exception:
            return self._fallback(text)

        return GeneratedEmbedding(
            vector=[round(float(value), 6) for value in embedding],
            model=self.settings.gemini_embedding_model,
            mode="gemini-embedding",
        )

    def _fallback(self, text: str) -> GeneratedEmbedding:
        return GeneratedEmbedding(
            vector=demo_embedding(text),
            model=DEMO_EMBEDDING_MODEL,
            mode="demo-fallback",
        )

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client

        from google import genai

        if self.settings.google_genai_use_vertexai:
            self._client = genai.Client(
                vertexai=True,
                project=self.settings.google_cloud_project,
                location=self.settings.google_cloud_location,
            )
        else:
            self._client = genai.Client(api_key=self.settings.google_api_key)
        return self._client
