from storms_agents.agents.base import AgentResult
from storms_agents.demo_data import DEMO_BOOK_SECTIONS
from storms_agents.observability import trace_span
from storms_agents.schemas import RetrievedContext
from storms_agents.storage.repository import StorageRepository


class RetrievalAgent:
    name = "RetrievalAgent"

    def __init__(self, storage: StorageRepository | None = None) -> None:
        self.storage = storage or StorageRepository()

    def run(self, book_id: str, query: str, limit: int = 3) -> AgentResult[list[RetrievedContext]]:
        status = self.storage.status
        operation = (
            "retrieval.pgvector_search"
            if status.configured and status.pgvector_ready
            else "retrieval.search"
        )
        with trace_span(self.name, operation) as trace:
            if status.configured and status.pgvector_ready:
                try:
                    contexts = self.storage.search_sections(book_id, query, limit)
                    trace.output_tokens = len(contexts)
                    return AgentResult(output=contexts, traces=[trace])
                except Exception:
                    trace.operation = "retrieval.search_fallback"

            query_words = {word.strip(".,?!").lower() for word in query.split() if len(word) > 2}
            scored: list[RetrievedContext] = []
            for section in DEMO_BOOK_SECTIONS:
                section_words = {
                    word.strip(".,?!").lower() for word in section["text"].split() if len(word) > 2
                }
                overlap = len(query_words & section_words)
                score = overlap / max(len(query_words), 1)
                if score > 0:
                    scored.append(
                        RetrievedContext(
                            section_id=section["section_id"],
                            book_id=book_id,
                            text=section["text"],
                            score=round(score, 3),
                            source="book_section",
                        )
                    )
            contexts = sorted(scored, key=lambda item: item.score, reverse=True)[:limit]
            trace.output_tokens = len(contexts)
            return AgentResult(output=contexts, traces=[trace])
