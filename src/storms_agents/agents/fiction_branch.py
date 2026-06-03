from uuid import uuid4

from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import CharacterProfile, FictionBranch, RetrievedContext


class FictionBranchAgent:
    name = "FictionBranchAgent"

    def run(
        self,
        book_id: str,
        character: CharacterProfile,
        prompt: str,
        contexts: list[RetrievedContext],
        character_response: str,
    ) -> AgentResult[FictionBranch]:
        with trace_span(self.name, "fiction_branch.create") as trace:
            citations = [context.section_id for context in contexts]
            anchor = contexts[0].text if contexts else "No retrieved canon anchor was found."
            branch = FictionBranch(
                branch_id=f"fiction-{uuid4().hex[:12]}",
                book_id=book_id,
                character_id=character.character_id,
                seed_prompt=prompt,
                premise=(
                    "Alternative branch separated from canon. The character keeps the literary "
                    "voice and psychology, while new events are treated as fiction."
                ),
                canon_anchor_citations=citations,
                continuation=(
                    f"Canon anchor: {anchor}\n\nFiction continuation: {character_response}"
                ),
            )
            trace.input_tokens = len(prompt.split()) + sum(
                len(context.text.split()) for context in contexts
            )
            trace.output_tokens = len(branch.continuation.split())
            return AgentResult(output=branch, traces=[trace])
