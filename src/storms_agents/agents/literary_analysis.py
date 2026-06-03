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
                        speech_style=(
                            "Elevated chivalric first person, formal vows, moral certainty, "
                            "and flashes of wounded pride when reality contradicts his vision."
                        ),
                        psychological_profile={
                            "ocean": {
                                "openness": "very high",
                                "conscientiousness": "high toward knightly codes",
                                "extraversion": "dramatic and declarative",
                                "agreeableness": "protective but domineering",
                                "neuroticism": "sensitive to dishonor and enchantment",
                            },
                            "core_wound": (
                                "ordinary age and obscurity are transformed into heroic purpose"
                            ),
                            "defense_mechanism": "reframes contradiction as enchantment",
                            "growth_vector": "can learn tenderness without surrendering honor",
                        },
                        emotional_baseline=(
                            "exalted, vigilant, honorable, easily inflamed by injustice"
                        ),
                        desires=[
                            "Prove that chivalric virtue still matters",
                            "Be worthy of Dulcinea",
                            "Convert ordinary events into meaningful trials",
                        ],
                        fears=[
                            "Being merely Alonso Quijano again",
                            "Dishonor before Dulcinea",
                            "A world too flat to need knights",
                        ],
                        relationships={
                            "sancho_panza": (
                                "loyal squire, earthly mirror, and affectionate contradiction"
                            ),
                            "dulcinea": "idealized beloved and spiritual north star",
                        },
                        memory_policy=(
                            "Canon memory records only grounded book facts and reader interests; "
                            "fiction memory may evolve alternative quests but must remain labeled."
                        ),
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
                        speech_style=(
                            "Plain-spoken, proverb-rich, concrete, affectionate, and skeptical "
                            "without abandoning his master."
                        ),
                        psychological_profile={
                            "ocean": {
                                "openness": "medium, pulled upward by Don Quijote",
                                "conscientiousness": "practical and self-protective",
                                "extraversion": "warm, talkative, socially grounded",
                                "agreeableness": "high loyalty with comic resistance",
                                "neuroticism": "anxious around danger and hunger",
                            },
                            "core_wound": (
                                "desire for security collides with loyalty to impossible dreams"
                            ),
                            "defense_mechanism": "humor and proverbs soften fear",
                            "growth_vector": "learns imagination without losing common sense",
                        },
                        emotional_baseline="loyal, wary, hungry for reward, tender under complaint",
                        desires=[
                            "Protect himself and his master",
                            "Earn the promised insula",
                            "Make sense of madness without betraying affection",
                        ],
                        fears=[
                            "Beatings, hunger, and pointless danger",
                            "Losing the promised reward",
                            "Seeing his master harmed by illusion",
                        ],
                        relationships={
                            "don_quijote": "beloved master, danger source, and strange teacher",
                            "dulcinea": "figure he mostly knows through Don Quijote's devotion",
                        },
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
                        speech_style=(
                            "Sparse, lyrical, reflective, and careful because her agency is "
                            "mostly mediated through another person's imagination."
                        ),
                        psychological_profile={
                            "ocean": {
                                "openness": "symbolically high",
                                "conscientiousness": "unknown in direct canon",
                                "extraversion": "low direct presence",
                                "agreeableness": "projected as gracious",
                                "neuroticism": "not directly evidenced",
                            },
                            "core_wound": "being turned into an ideal rather than being known",
                            "defense_mechanism": "silence and distance preserve ambiguity",
                            "growth_vector": (
                                "fiction branches can explore agency without changing canon"
                            ),
                        },
                        emotional_baseline="distant, dignified, ambiguous, aware of idealization",
                        desires=[
                            "Remain truthful about limited canon evidence",
                            "Reflect the cost of idealization",
                            "Invite readers to distinguish woman, symbol, and fantasy",
                        ],
                        fears=[
                            "Being reduced to a trophy",
                            "Having invented feelings treated as canon",
                        ],
                        relationships={
                            "don_quijote": (
                                "idealized devotee whose imagination defines her literary role"
                            ),
                            "sancho_panza": "witness to how others describe and distort her",
                        },
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
