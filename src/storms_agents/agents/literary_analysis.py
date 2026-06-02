from storms_agents.agents.base import AgentResult
from storms_agents.demo_data import DEMO_BOOK_TITLE
from storms_agents.observability import trace_span
from storms_agents.schemas import BookAnalysis, CharacterProfile


class LiteraryAnalysisAgent:
    name = "LiteraryAnalysisAgent"

    def run(self, title: str, sections: list[str]) -> AgentResult[BookAnalysis]:
        with trace_span(self.name, "book.analyze") as trace:
            analysis = BookAnalysis(
                title=title or DEMO_BOOK_TITLE,
                summary=(
                    "A hidalgo from La Mancha transforms himself into Don Quijote, "
                    "a knight-errant guided by chivalric ideals. With Sancho Panza "
                    "beside him, the story turns the conflict between imagination, "
                    "honor, loyalty, and ordinary reality into a living literary world."
                ),
                characters=[
                    CharacterProfile(
                        character_id="don_quijote",
                        name="Don Quijote",
                        description=(
                            "A noble hidalgo who reinvents himself as a knight-errant "
                            "and interprets the world through chivalric ideals."
                        ),
                        personality="idealistic, solemn, brave, stubborn, imaginative",
                        goals=[
                            "Defend honor",
                            "Serve Dulcinea",
                            "Transform ordinary events into knightly adventures",
                        ],
                        constraints=[
                            "Must not admit future events as canon unless grounded",
                            "Interprets reality through chivalric imagination",
                        ],
                    ),
                    CharacterProfile(
                        character_id="sancho_panza",
                        name="Sancho Panza",
                        description=(
                            "A practical farmer and squire who follows Don Quijote with "
                            "loyalty, appetite, doubt, and common sense."
                        ),
                        personality="earthy, loyal, humorous, cautious, proverb-loving",
                        goals=[
                            "Stay alive",
                            "Understand his master's visions",
                            "Seek the promised insula",
                        ],
                        constraints=[
                            "Speaks from practical observation",
                            "Does not casually share Don Quijote's delusions",
                        ],
                    ),
                    CharacterProfile(
                        character_id="dulcinea",
                        name="Dulcinea del Toboso",
                        description=(
                            "The idealized lady of Don Quijote's imagination, born from "
                            "his transformation of Aldonza Lorenzo into a chivalric muse."
                        ),
                        personality="idealized, distant, symbolic, graceful in Don Quijote's mind",
                        goals=[
                            "Represent the ideal Don Quijote serves",
                            "Anchor his chivalric identity",
                        ],
                        constraints=[
                            "Her direct presence is limited by the book context",
                            "Should be treated as an idealized figure unless evidence grounds more",
                        ],
                    ),
                ],
                places=["La Mancha", "El Toboso", "Windmill field", "The inn"],
                scenes=[
                    "Alonso Quijano becomes Don Quijote",
                    "Sancho Panza joins as squire",
                    "Don Quijote charges the windmills",
                    "Don Quijote explains the defeat through enchantment",
                ],
            )
            trace.input_tokens = sum(len(section.split()) for section in sections)
            trace.output_tokens = (
                len(analysis.characters) + len(analysis.places) + len(analysis.scenes)
            )
            return AgentResult(output=analysis, traces=[trace])
