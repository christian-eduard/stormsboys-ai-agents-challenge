from dataclasses import dataclass

from sqlalchemy import text
from sqlalchemy.engine import Engine
from sqlalchemy.exc import SQLAlchemyError

from storms_agents.config import Settings, get_settings
from storms_agents.demo_data import DEMO_BOOK_SECTIONS
from storms_agents.schemas import RetrievedContext
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

    def seed_demo_book(self, book_id: str, title: str) -> int:
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
