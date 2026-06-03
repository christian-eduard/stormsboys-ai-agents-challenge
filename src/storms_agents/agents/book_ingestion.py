from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span


class BookIngestionAgent:
    name = "BookIngestionAgent"

    def run(self, book_id: str, text: str) -> AgentResult[list[str]]:
        with trace_span(self.name, "book.ingest") as trace:
            paragraphs = [part.strip() for part in text.split("\n\n") if part.strip()]
            if not paragraphs:
                paragraphs = [text.strip()] if text.strip() else []
            sections = []
            for paragraph in paragraphs:
                words = paragraph.replace("\n", " ").split()
                if len(words) <= 180:
                    sections.append(" ".join(words))
                    continue
                for start in range(0, len(words), 160):
                    chunk = words[start : start + 180]
                    if len(chunk) >= 20:
                        sections.append(" ".join(chunk))
            trace.output_tokens = len(sections)
            return AgentResult(output=sections, traces=[trace])
