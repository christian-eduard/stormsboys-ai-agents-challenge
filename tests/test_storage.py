from storms_agents.config import Settings
from storms_agents.storage.embedding import (
    DEMO_EMBEDDING_MODEL,
    EmbeddingProvider,
    demo_embedding,
    vector_literal,
)
from storms_agents.storage.repository import StorageRepository


def test_storage_status_without_database_url() -> None:
    storage = StorageRepository(Settings(database_url=None))

    status = storage.status

    assert status.configured is False
    assert status.provider == "demo-memory"
    assert status.pgvector_ready is False


def test_storage_schema_contains_pgvector_contract() -> None:
    schema = " ".join(StorageRepository(Settings(database_url=None)).schema_sql())

    assert "CREATE EXTENSION IF NOT EXISTS vector" in schema
    assert "section_embeddings" in schema
    assert "vector(768)" in schema


def test_demo_embedding_contract() -> None:
    embedding = demo_embedding("Sarin protects the lost names.")

    assert len(embedding) == 768
    assert vector_literal(embedding).startswith("[")
    assert vector_literal(embedding).endswith("]")


def test_embedding_provider_falls_back_without_google_config() -> None:
    provider = EmbeddingProvider(Settings(google_api_key=None, google_cloud_project=None))

    generated = provider.embed_query("Why does Sarin protect the lost names?")

    assert provider.status.mode == "demo-fallback"
    assert generated.model == DEMO_EMBEDDING_MODEL
    assert generated.mode == "demo-fallback"
    assert len(generated.vector) == 768
