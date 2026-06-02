from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span


class BookIngestionAgent:
    name = "BookIngestionAgent"

    def run(self, book_id: str, text: str) -> AgentResult[list[str]]:
        with trace_span(self.name, "book.ingest") as trace:
            paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
            sections = [paragraph.replace("\n", " ") for paragraph in paragraphs]
            trace.output_tokens = len(sections)
            return AgentResult(output=sections, traces=[trace])

