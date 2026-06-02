from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import BookAnalysis, CharacterProfile


class LiteraryAnalysisAgent:
    name = "LiteraryAnalysisAgent"

    def run(self, title: str, sections: list[str]) -> AgentResult[BookAnalysis]:
        with trace_span(self.name, "book.analyze") as trace:
            analysis = BookAnalysis(
                title=title,
                summary=(
                    "A young archivist, a skeptical clockmaker, and an ink guardian "
                    "must decide whether memory should be protected or returned."
                ),
                characters=[
                    CharacterProfile(
                        character_id="mara",
                        name="Mara",
                        description="Young archivist who believes memory belongs to people.",
                        personality="curious, brave, careful with power",
                        goals=["Return the lost names", "Protect Narael"],
                        constraints=["Does not claim knowledge beyond the story"],
                    ),
                    CharacterProfile(
                        character_id="eloy",
                        name="Eloy",
                        description="Skeptical clockmaker who trusts mechanisms before miracles.",
                        personality="practical, doubtful, loyal when convinced",
                        goals=["Understand the warning", "Keep Mara alive"],
                        constraints=["Avoids mystical certainty"],
                    ),
                    CharacterProfile(
                        character_id="sarin",
                        name="Sarin",
                        description="Guardian made of ink and shadow protecting the lost names.",
                        personality="solemn, protective, bound by duty",
                        goals=["Prevent memory from becoming power"],
                        constraints=["Cannot casually betray the names"],
                    ),
                ],
                places=["Narael", "Underground archive", "Silent Gate"],
                scenes=[
                    "The forbidden volume answers Mara",
                    "The tower bells ring without hands",
                    "The confrontation at the Silent Gate",
                ],
            )
            trace.input_tokens = sum(len(section.split()) for section in sections)
            trace.output_tokens = (
                len(analysis.characters) + len(analysis.places) + len(analysis.scenes)
            )
            return AgentResult(output=analysis, traces=[trace])
