from storms_agents.config import Settings
from storms_agents.memory import ConversationMemoryStore
from storms_agents.schemas import ConversationMemory, ConversationMode
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
    assert "conversation_memory_events" in schema


class FakePersistentMemoryRepository:
    def __init__(self) -> None:
        self.events: list[tuple[str, str, ConversationMode, str | None]] = []

    @property
    def status(self) -> object:
        return type("Status", (), {"configured": True})()

    def load_conversation_memory(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
    ) -> ConversationMemory:
        matching = [
            event
            for event in self.events
            if event[0] == session_id and event[1] == character_id and event[2] == mode
        ]
        return ConversationMemory(
            session_id=session_id,
            character_id=character_id,
            mode=mode,
            turn_count=len(matching),
            canon_memory=["persisted"] if matching and mode == ConversationMode.CANON else [],
            fiction_memory=["persisted"] if matching and mode == ConversationMode.FICTION else [],
            learned_reader_preferences=[event[3] for event in matching if event[3]],
            relationship_summary=f"{len(matching)} persisted turn(s).",
        )

    def append_conversation_memory(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
        question: str,
        response: str,
        memory_line: str,
        reader_preference: str | None,
    ) -> ConversationMemory:
        self.events.append((session_id, character_id, mode, reader_preference))
        return self.load_conversation_memory(session_id, character_id, mode)


def test_conversation_memory_store_uses_persistent_repository() -> None:
    repository = FakePersistentMemoryRepository()
    store = ConversationMemoryStore(repository=repository)  # type: ignore[arg-type]

    before = store.snapshot("session-1", "don_quijote", ConversationMode.CANON)
    after = store.record(
        "session-1",
        "don_quijote",
        ConversationMode.CANON,
        "Explain your psychology.",
        "I desire honor.",
    )

    assert before.turn_count == 0
    assert after.turn_count == 1
    assert "reader asks for psychological motivation" in after.learned_reader_preferences
    assert repository.events


def test_demo_embedding_contract() -> None:
    embedding = demo_embedding("Don Quijote attacks the windmills.")

    assert len(embedding) == 768
    assert vector_literal(embedding).startswith("[")
    assert vector_literal(embedding).endswith("]")


def test_embedding_provider_falls_back_without_google_config() -> None:
    provider = EmbeddingProvider(Settings(google_api_key=None, google_cloud_project=None))

    generated = provider.embed_query("Why does Don Quijote attack the windmills?")

    assert provider.status.mode == "demo-fallback"
    assert generated.model == DEMO_EMBEDDING_MODEL
    assert generated.mode == "demo-fallback"
    assert len(generated.vector) == 768
