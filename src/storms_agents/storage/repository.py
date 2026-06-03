import json
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from storms_agents.config import Settings, get_settings
from storms_agents.demo_data import DEMO_BOOK_SECTIONS
from storms_agents.schemas import (
    ConversationMemory,
    ConversationMode,
    FictionBranch,
    RetrievedContext,
)
from storms_agents.storage.embedding import (
    EmbeddingProvider,
    EmbeddingProviderProtocol,
    vector_literal,
)

SCHEMA_STATEMENTS = [
    "CREATE EXTENSION IF NOT EXISTS vector",
    """
    CREATE TABLE IF NOT EXISTS books (
      book_id TEXT PRIMARY KEY,
      title TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS book_sections (
      section_id TEXT PRIMARY KEY,
      book_id TEXT NOT NULL REFERENCES books(book_id) ON DELETE CASCADE,
      section_index INTEGER NOT NULL,
      text TEXT NOT NULL,
      source TEXT NOT NULL DEFAULT 'book_section'
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS section_embeddings (
      section_id TEXT PRIMARY KEY REFERENCES book_sections(section_id) ON DELETE CASCADE,
      embedding vector(768) NOT NULL,
      model TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS section_embeddings_vector_idx
      ON section_embeddings USING ivfflat (embedding vector_cosine_ops)
    """,
    """
    CREATE TABLE IF NOT EXISTS conversation_memory_events (
      memory_id BIGSERIAL PRIMARY KEY,
      session_id TEXT NOT NULL,
      character_id TEXT NOT NULL,
      mode TEXT NOT NULL,
      question TEXT NOT NULL,
      response TEXT NOT NULL,
      memory_line TEXT NOT NULL,
      reader_preference TEXT,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS conversation_memory_lookup_idx
      ON conversation_memory_events (session_id, character_id, mode, created_at)
    """,
    """
    CREATE TABLE IF NOT EXISTS fiction_branches (
      branch_id TEXT PRIMARY KEY,
      session_id TEXT NOT NULL,
      book_id TEXT NOT NULL,
      character_id TEXT NOT NULL,
      seed_prompt TEXT NOT NULL,
      premise TEXT NOT NULL,
      canon_anchor_citations JSONB NOT NULL DEFAULT '[]'::jsonb,
      continuation TEXT NOT NULL,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS fiction_branches_lookup_idx
      ON fiction_branches (session_id, character_id, created_at)
    """,
]


@dataclass(frozen=True)
class StorageStatus:
    configured: bool
    provider: str
    pgvector_ready: bool
    detail: str


class StorageRepository:
    def __init__(
        self,
        settings: Settings | None = None,
        engine: Engine | None = None,
        embedding_provider: EmbeddingProviderProtocol | None = None,
    ) -> None:
        self.settings = settings or get_settings()
        self._engine = engine
        self.embedding_provider = embedding_provider or EmbeddingProvider(self.settings)

    @property
    def status(self) -> StorageStatus:
        if not self.settings.database_url:
            return StorageStatus(
                configured=False,
                provider="demo-memory",
                pgvector_ready=False,
                detail="DATABASE_URL is not set; demo retrieval uses in-memory sections.",
            )

        try:
            with self.engine.connect() as connection:
                connection.execute(text("SELECT 1"))
                pgvector_ready = bool(
                    connection.execute(
                        text("SELECT EXISTS (SELECT 1 FROM pg_extension WHERE extname = 'vector')")
                    ).scalar()
                )
        except SQLAlchemyError as exc:
            return StorageStatus(
                configured=True,
                provider="cloud-sql-postgresql",
                pgvector_ready=False,
                detail=f"Database connection failed: {exc.__class__.__name__}",
            )

        return StorageStatus(
            configured=True,
            provider="cloud-sql-postgresql",
            pgvector_ready=pgvector_ready,
            detail="Database connection succeeded.",
        )

    @property
    def engine(self) -> Engine:
        if self._engine is None:
            from sqlalchemy import create_engine

            self._engine = create_engine(self.settings.database_url, pool_pre_ping=True)
        return self._engine

    def schema_sql(self) -> list[str]:
        return [" ".join(statement.split()) for statement in SCHEMA_STATEMENTS]

    def initialize_schema(self) -> None:
        with self.engine.begin() as connection:
            for statement in SCHEMA_STATEMENTS:
                connection.execute(text(statement))

    def seed_demo_book(self, book_id: str, title: str) -> int:
        self.initialize_schema()
        with self.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO books (book_id, title)
                    VALUES (:book_id, :title)
                    ON CONFLICT (book_id) DO UPDATE SET title = EXCLUDED.title
                    """
                ),
                {"book_id": book_id, "title": title},
            )
            for index, section in enumerate(DEMO_BOOK_SECTIONS):
                connection.execute(
                    text(
                        """
                        INSERT INTO book_sections (
                          section_id, book_id, section_index, text, source
                        )
                        VALUES (:section_id, :book_id, :section_index, :text, :source)
                        ON CONFLICT (section_id) DO UPDATE SET
                          text = EXCLUDED.text,
                          section_index = EXCLUDED.section_index,
                          source = EXCLUDED.source
                        """
                    ),
                    {
                        "section_id": section["section_id"],
                        "book_id": book_id,
                        "section_index": index,
                        "text": section["text"],
                        "source": section["source"],
                    },
                )
                embedding = self.embedding_provider.embed_document(section["text"])
                connection.execute(
                    text(
                        """
                        INSERT INTO section_embeddings (section_id, embedding, model)
                        VALUES (:section_id, CAST(:embedding AS vector), :model)
                        ON CONFLICT (section_id) DO UPDATE SET
                          embedding = EXCLUDED.embedding,
                          model = EXCLUDED.model
                        """
                    ),
                    {
                        "section_id": section["section_id"],
                        "embedding": vector_literal(embedding.vector),
                        "model": embedding.model,
                    },
                )
        return len(DEMO_BOOK_SECTIONS)

    def search_sections(self, book_id: str, query: str, limit: int) -> list[RetrievedContext]:
        query_embedding = vector_literal(self.embedding_provider.embed_query(query).vector)
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT
                      s.section_id,
                      s.book_id,
                      s.text,
                      s.source,
                      1 - (e.embedding <=> CAST(:embedding AS vector)) AS score
                    FROM section_embeddings e
                    JOIN book_sections s ON s.section_id = e.section_id
                    WHERE s.book_id = :book_id
                    ORDER BY e.embedding <=> CAST(:embedding AS vector)
                    LIMIT :limit
                    """
                ),
                {
                    "book_id": book_id,
                    "embedding": query_embedding,
                    "limit": limit,
                },
            ).mappings()
            contexts = [
                RetrievedContext(
                    section_id=row["section_id"],
                    book_id=row["book_id"],
                    text=row["text"],
                    score=round(float(row["score"]), 3),
                    source=row["source"],
                )
                for row in rows
            ]
        return [context for context in contexts if context.score > 0]

    def load_conversation_memory(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
    ) -> ConversationMemory:
        with self.engine.connect() as connection:
            rows = list(
                connection.execute(
                    text(
                        """
                        SELECT memory_line, reader_preference
                        FROM conversation_memory_events
                        WHERE session_id = :session_id
                          AND character_id = :character_id
                          AND mode = :mode
                        ORDER BY created_at ASC, memory_id ASC
                        """
                    ),
                    {
                        "session_id": session_id,
                        "character_id": character_id,
                        "mode": mode.value,
                    },
                ).mappings()
            )
        lines = [str(row["memory_line"]) for row in rows][-5:]
        preferences = []
        for row in rows:
            preference = row["reader_preference"]
            if preference and preference not in preferences:
                preferences.append(str(preference))
        return self._memory_model(
            session_id=session_id,
            character_id=character_id,
            mode=mode,
            turn_count=len(rows),
            memory_lines=lines,
            preferences=preferences,
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
        with self.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO conversation_memory_events (
                      session_id, character_id, mode, question, response,
                      memory_line, reader_preference
                    )
                    VALUES (
                      :session_id, :character_id, :mode, :question, :response,
                      :memory_line, :reader_preference
                    )
                    """
                ),
                {
                    "session_id": session_id,
                    "character_id": character_id,
                    "mode": mode.value,
                    "question": question,
                    "response": response,
                    "memory_line": memory_line,
                    "reader_preference": reader_preference,
                },
            )
        return self.load_conversation_memory(session_id, character_id, mode)

    def list_conversation_memory_events(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
        limit: int = 5,
    ) -> list[dict[str, object]]:
        with self.engine.connect() as connection:
            rows = list(
                connection.execute(
                    text(
                        """
                        SELECT
                          memory_id,
                          question,
                          response,
                          memory_line,
                          reader_preference,
                          created_at
                        FROM conversation_memory_events
                        WHERE session_id = :session_id
                          AND character_id = :character_id
                          AND mode = :mode
                        ORDER BY created_at DESC, memory_id DESC
                        LIMIT :limit
                        """
                    ),
                    {
                        "session_id": session_id,
                        "character_id": character_id,
                        "mode": mode.value,
                        "limit": limit,
                    },
                ).mappings()
            )
        return [
            {
                "memory_id": row["memory_id"],
                "question": row["question"],
                "response": row["response"],
                "memory_line": row["memory_line"],
                "reader_preference": row["reader_preference"],
                "created_at": row["created_at"].isoformat()
                if hasattr(row["created_at"], "isoformat")
                else str(row["created_at"]),
            }
            for row in rows
        ]

    def delete_demo_session(self, session_id: str) -> dict[str, int]:
        self.initialize_schema()
        with self.engine.begin() as connection:
            memory_result = connection.execute(
                text(
                    """
                    DELETE FROM conversation_memory_events
                    WHERE session_id = :session_id
                    """
                ),
                {"session_id": session_id},
            )
            fiction_result = connection.execute(
                text(
                    """
                    DELETE FROM fiction_branches
                    WHERE session_id = :session_id
                    """
                ),
                {"session_id": session_id},
            )
        return {
            "memory_events": memory_result.rowcount or 0,
            "fiction_branches": fiction_result.rowcount or 0,
        }

    def append_fiction_branch(
        self,
        session_id: str,
        branch: FictionBranch,
    ) -> FictionBranch:
        self.initialize_schema()
        with self.engine.begin() as connection:
            connection.execute(
                text(
                    """
                    INSERT INTO fiction_branches (
                      branch_id, session_id, book_id, character_id, seed_prompt,
                      premise, canon_anchor_citations, continuation
                    )
                    VALUES (
                      :branch_id, :session_id, :book_id, :character_id, :seed_prompt,
                      :premise, CAST(:canon_anchor_citations AS jsonb), :continuation
                    )
                    ON CONFLICT (branch_id) DO UPDATE SET
                      seed_prompt = EXCLUDED.seed_prompt,
                      premise = EXCLUDED.premise,
                      canon_anchor_citations = EXCLUDED.canon_anchor_citations,
                      continuation = EXCLUDED.continuation
                    """
                ),
                {
                    "branch_id": branch.branch_id,
                    "session_id": session_id,
                    "book_id": branch.book_id,
                    "character_id": branch.character_id,
                    "seed_prompt": branch.seed_prompt,
                    "premise": branch.premise,
                    "canon_anchor_citations": json.dumps(branch.canon_anchor_citations),
                    "continuation": branch.continuation,
                },
            )
        return branch

    def list_fiction_branches(
        self,
        session_id: str,
        character_id: str | None = None,
        limit: int = 5,
    ) -> list[dict[str, object]]:
        self.initialize_schema()
        character_filter = "AND character_id = :character_id" if character_id else ""
        params: dict[str, object] = {"session_id": session_id, "limit": limit}
        if character_id:
            params["character_id"] = character_id
        with self.engine.connect() as connection:
            rows = list(
                connection.execute(
                    text(
                        f"""
                        SELECT
                          branch_id,
                          book_id,
                          character_id,
                          seed_prompt,
                          premise,
                          canon_anchor_citations,
                          continuation,
                          created_at
                        FROM fiction_branches
                        WHERE session_id = :session_id
                          {character_filter}
                        ORDER BY created_at DESC, branch_id DESC
                        LIMIT :limit
                        """
                    ),
                    params,
                ).mappings()
            )
        return [
            {
                "branch_id": row["branch_id"],
                "book_id": row["book_id"],
                "character_id": row["character_id"],
                "seed_prompt": row["seed_prompt"],
                "premise": row["premise"],
                "canon_anchor_citations": self._decode_json_list(row["canon_anchor_citations"]),
                "continuation": row["continuation"],
                "created_at": row["created_at"].isoformat()
                if hasattr(row["created_at"], "isoformat")
                else str(row["created_at"]),
            }
            for row in rows
        ]

    def _decode_json_list(self, value: object) -> list[str]:
        if isinstance(value, list):
            return [str(item) for item in value]
        if isinstance(value, str):
            try:
                parsed = json.loads(value)
            except json.JSONDecodeError:
                return []
            if isinstance(parsed, list):
                return [str(item) for item in parsed]
        return []

    def _memory_model(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
        turn_count: int,
        memory_lines: list[str],
        preferences: list[str],
    ) -> ConversationMemory:
        relationship = (
            f"{turn_count} persisted turn(s). The character can adapt tone and recall "
            "reader interests without changing canon."
            if turn_count
            else "No prior persisted turns for this character, mode, and session."
        )
        return ConversationMemory(
            session_id=session_id,
            character_id=character_id,
            mode=mode,
            turn_count=turn_count,
            canon_memory=memory_lines if mode == ConversationMode.CANON else [],
            fiction_memory=memory_lines if mode == ConversationMode.FICTION else [],
            learned_reader_preferences=preferences,
            relationship_summary=relationship,
        )
