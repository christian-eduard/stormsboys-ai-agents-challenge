import json
from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from storms_agents.config import Settings, get_settings
from storms_agents.demo_data import DEMO_BOOK_SECTIONS
from storms_agents.schemas import (
    BookAnalysis,
    ConversationMemory,
    ConversationMode,
    FictionBranch,
    RetrievedContext,
    UploadedBook,
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
    CREATE TABLE IF NOT EXISTS uploaded_books (
      book_id TEXT PRIMARY KEY REFERENCES books(book_id) ON DELETE CASCADE,
      title TEXT NOT NULL,
      author TEXT NOT NULL DEFAULT 'Unknown',
      rights TEXT NOT NULL,
      owner_user_id TEXT NOT NULL,
      tenant_id TEXT NOT NULL,
      status TEXT NOT NULL DEFAULT 'ready_for_review',
      language TEXT NOT NULL DEFAULT 'en',
      analysis JSONB NOT NULL,
      sections INTEGER NOT NULL DEFAULT 0,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS uploaded_books_tenant_idx
      ON uploaded_books (tenant_id, created_at)
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
    """
    CREATE TABLE IF NOT EXISTS reader_events (
      event_id BIGSERIAL PRIMARY KEY,
      user_id TEXT NOT NULL,
      tenant_id TEXT NOT NULL,
      book_id TEXT NOT NULL,
      section_id TEXT NOT NULL,
      section_index INTEGER NOT NULL DEFAULT 0,
      event_type TEXT NOT NULL,
      note_text TEXT,
      progress_percent INTEGER,
      created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )
    """,
    """
    CREATE INDEX IF NOT EXISTS reader_events_lookup_idx
      ON reader_events (user_id, book_id, section_id, created_at)
    """,
    """
    CREATE INDEX IF NOT EXISTS reader_events_book_idx
      ON reader_events (book_id, event_type, created_at)
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

    def upsert_uploaded_book(
        self,
        book_id: str,
        title: str,
        author: str,
        rights: str,
        owner_user_id: str,
        tenant_id: str,
        language: str,
        sections: list[str],
        analysis: BookAnalysis,
    ) -> UploadedBook:
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
            connection.execute(
                text("DELETE FROM book_sections WHERE book_id = :book_id"),
                {"book_id": book_id},
            )
            for index, section in enumerate(sections):
                section_id = f"{book_id}-section-{index + 1}"
                connection.execute(
                    text(
                        """
                        INSERT INTO book_sections (
                          section_id, book_id, section_index, text, source
                        )
                        VALUES (:section_id, :book_id, :section_index, :text, 'book_section')
                        """
                    ),
                    {
                        "section_id": section_id,
                        "book_id": book_id,
                        "section_index": index,
                        "text": section,
                    },
                )
                embedding = self.embedding_provider.embed_document(section)
                connection.execute(
                    text(
                        """
                        INSERT INTO section_embeddings (section_id, embedding, model)
                        VALUES (:section_id, CAST(:embedding AS vector), :model)
                        """
                    ),
                    {
                        "section_id": section_id,
                        "embedding": vector_literal(embedding.vector),
                        "model": embedding.model,
                    },
                )
            connection.execute(
                text(
                    """
                    INSERT INTO uploaded_books (
                      book_id, title, author, rights, owner_user_id, tenant_id,
                      status, language, analysis, sections
                    )
                    VALUES (
                      :book_id, :title, :author, :rights, :owner_user_id, :tenant_id,
                      'ready_for_review', :language, CAST(:analysis AS jsonb), :sections
                    )
                    ON CONFLICT (book_id) DO UPDATE SET
                      title = EXCLUDED.title,
                      author = EXCLUDED.author,
                      rights = EXCLUDED.rights,
                      status = EXCLUDED.status,
                      language = EXCLUDED.language,
                      analysis = EXCLUDED.analysis,
                      sections = EXCLUDED.sections
                    """
                ),
                {
                    "book_id": book_id,
                    "title": title,
                    "author": author,
                    "rights": rights,
                    "owner_user_id": owner_user_id,
                    "tenant_id": tenant_id,
                    "language": language,
                    "analysis": analysis.model_dump_json(),
                    "sections": len(sections),
                },
            )
        return UploadedBook(
            book_id=book_id,
            title=title,
            author=author,
            rights=rights,
            owner_user_id=owner_user_id,
            tenant_id=tenant_id,
            language=language,
            sections=len(sections),
            characters=len(analysis.characters),
            scenes=len(analysis.scenes),
        )

    def list_uploaded_books(self, tenant_id: str | None = None) -> list[UploadedBook]:
        self.initialize_schema()
        tenant_filter = "WHERE tenant_id = :tenant_id" if tenant_id else ""
        params = {"tenant_id": tenant_id} if tenant_id else {}
        with self.engine.connect() as connection:
            rows = list(
                connection.execute(
                    text(
                        f"""
                        SELECT
                          book_id, title, author, rights, owner_user_id, tenant_id,
                          status, language, analysis, sections, created_at
                        FROM uploaded_books
                        {tenant_filter}
                        ORDER BY created_at DESC, title ASC
                        """
                    ),
                    params,
                ).mappings()
            )
        return [self._uploaded_book_from_row(row) for row in rows]

    def get_uploaded_book_analysis(self, book_id: str) -> BookAnalysis | None:
        self.initialize_schema()
        with self.engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                    SELECT analysis
                    FROM uploaded_books
                    WHERE book_id = :book_id
                    """
                    ),
                    {"book_id": book_id},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        analysis = row["analysis"]
        if isinstance(analysis, str):
            return BookAnalysis.model_validate_json(analysis)
        return BookAnalysis.model_validate(analysis)

    def get_uploaded_book(self, book_id: str) -> UploadedBook | None:
        self.initialize_schema()
        with self.engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                    SELECT
                      book_id, title, author, rights, owner_user_id, tenant_id,
                      status, language, analysis, sections, created_at
                    FROM uploaded_books
                    WHERE book_id = :book_id
                    """
                    ),
                    {"book_id": book_id},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        return self._uploaded_book_from_row(row)

    def list_book_sections(self, book_id: str) -> list[dict[str, object]]:
        self.initialize_schema()
        with self.engine.connect() as connection:
            rows = connection.execute(
                text(
                    """
                    SELECT section_id, section_index, text
                    FROM book_sections
                    WHERE book_id = :book_id
                    ORDER BY section_index
                    """
                ),
                {"book_id": book_id},
            ).mappings()
        return [
            {
                "section_id": row["section_id"],
                "index": row["section_index"],
                "text": row["text"],
            }
            for row in rows
        ]

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

    def record_reader_event(
        self,
        user_id: str,
        tenant_id: str,
        book_id: str,
        section_id: str,
        section_index: int,
        event_type: str,
        note_text: str | None = None,
        progress_percent: int | None = None,
    ) -> dict[str, object]:
        self.initialize_schema()
        with self.engine.begin() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        INSERT INTO reader_events (
                          user_id, tenant_id, book_id, section_id, section_index,
                          event_type, note_text, progress_percent
                        )
                        VALUES (
                          :user_id, :tenant_id, :book_id, :section_id, :section_index,
                          :event_type, :note_text, :progress_percent
                        )
                        RETURNING event_id, created_at
                        """
                    ),
                    {
                        "user_id": user_id,
                        "tenant_id": tenant_id,
                        "book_id": book_id,
                        "section_id": section_id,
                        "section_index": section_index,
                        "event_type": event_type,
                        "note_text": note_text,
                        "progress_percent": progress_percent,
                    },
                )
                .mappings()
                .one()
            )
        return {
            "event_id": row["event_id"],
            "user_id": user_id,
            "tenant_id": tenant_id,
            "book_id": book_id,
            "section_id": section_id,
            "section_index": section_index,
            "event_type": event_type,
            "note_text": note_text,
            "progress_percent": progress_percent,
            "created_at": row["created_at"].isoformat()
            if hasattr(row["created_at"], "isoformat")
            else str(row["created_at"]),
        }

    def latest_reader_progress(self, user_id: str, book_id: str) -> dict[str, object] | None:
        self.initialize_schema()
        with self.engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
                        SELECT
                          event_id, user_id, tenant_id, book_id, section_id,
                          section_index, progress_percent, created_at
                        FROM reader_events
                        WHERE user_id = :user_id
                          AND book_id = :book_id
                          AND event_type = 'progress'
                        ORDER BY created_at DESC, event_id DESC
                        LIMIT 1
                        """
                    ),
                    {"user_id": user_id, "book_id": book_id},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        return self._reader_event_from_row(row, event_type="progress")

    def list_reader_notes(
        self,
        user_id: str,
        book_id: str,
        section_id: str,
        limit: int = 20,
    ) -> list[dict[str, object]]:
        self.initialize_schema()
        with self.engine.connect() as connection:
            rows = list(
                connection.execute(
                    text(
                        """
                        SELECT
                          event_id, user_id, tenant_id, book_id, section_id,
                          section_index, event_type, note_text, created_at
                        FROM reader_events
                        WHERE user_id = :user_id
                          AND book_id = :book_id
                          AND section_id = :section_id
                          AND event_type IN ('note', 'favorite')
                        ORDER BY created_at DESC, event_id DESC
                        LIMIT :limit
                        """
                    ),
                    {
                        "user_id": user_id,
                        "book_id": book_id,
                        "section_id": section_id,
                        "limit": limit,
                    },
                ).mappings()
            )
        return [self._reader_event_from_row(row) for row in rows]

    def reader_engagement_summary(self) -> dict[str, object]:
        self.initialize_schema()
        with self.engine.connect() as connection:
            rows = list(
                connection.execute(
                    text(
                        """
                        SELECT
                          book_id,
                          COUNT(*) FILTER (WHERE event_type = 'progress') AS progress_events,
                          COUNT(*) FILTER (WHERE event_type = 'note') AS notes,
                          COUNT(*) FILTER (WHERE event_type = 'favorite') AS favorites,
                          COUNT(DISTINCT user_id) AS readers
                        FROM reader_events
                        GROUP BY book_id
                        ORDER BY MAX(created_at) DESC
                        LIMIT 10
                        """
                    )
                ).mappings()
            )
        return {
            "books": [
                {
                    "book_id": row["book_id"],
                    "progress_events": row["progress_events"],
                    "notes": row["notes"],
                    "favorites": row["favorites"],
                    "readers": row["readers"],
                }
                for row in rows
            ]
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

    def get_fiction_branch(
        self,
        session_id: str,
        branch_id: str,
    ) -> dict[str, object] | None:
        self.initialize_schema()
        with self.engine.connect() as connection:
            row = (
                connection.execute(
                    text(
                        """
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
                      AND branch_id = :branch_id
                    """
                    ),
                    {"session_id": session_id, "branch_id": branch_id},
                )
                .mappings()
                .first()
            )
        if row is None:
            return None
        return {
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

    def _reader_event_from_row(
        self,
        row: object,
        event_type: str | None = None,
    ) -> dict[str, object]:
        created_at = row["created_at"]
        event: dict[str, object] = {
            "event_id": row["event_id"],
            "user_id": row["user_id"],
            "tenant_id": row["tenant_id"],
            "book_id": row["book_id"],
            "section_id": row["section_id"],
            "section_index": row["section_index"],
            "event_type": event_type or row["event_type"],
            "created_at": created_at.isoformat()
            if hasattr(created_at, "isoformat")
            else str(created_at),
        }
        if "note_text" in row:
            event["note_text"] = row["note_text"]
        if "progress_percent" in row:
            event["progress_percent"] = row["progress_percent"]
        return event

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

    def _uploaded_book_from_row(self, row: object) -> UploadedBook:
        analysis_value = row["analysis"]
        if isinstance(analysis_value, str):
            analysis = BookAnalysis.model_validate_json(analysis_value)
        else:
            analysis = BookAnalysis.model_validate(analysis_value)
        return UploadedBook(
            book_id=row["book_id"],
            title=row["title"],
            author=row["author"],
            rights=row["rights"],
            owner_user_id=row["owner_user_id"],
            tenant_id=row["tenant_id"],
            status=row["status"],
            language=row["language"],
            sections=row["sections"],
            characters=len(analysis.characters),
            scenes=len(analysis.scenes),
            created_at=row["created_at"].isoformat()
            if hasattr(row["created_at"], "isoformat")
            else str(row["created_at"]),
        )

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
