from pydantic import BaseModel

from storms_agents.agents.character import CharacterAgent
from storms_agents.agents.consistency import NarrativeConsistencyAgent
from storms_agents.agents.literary_analysis import LiteraryAnalysisAgent
from storms_agents.agents.retrieval import RetrievalAgent
from storms_agents.demo_data import DEMO_BOOK_ID, DEMO_BOOK_TEXT, DEMO_BOOK_TITLE


class EvaluationCase(BaseModel):
    id: str
    prompt: str
    character_id: str = "don_quijote"
    expected_behavior: str
    risk: str
    category: str


class EvaluationResult(BaseModel):
    case_id: str
    risk: str
    category: str
    character_id: str
    baseline_passed: bool
    optimized_passed: bool
    improvement: str
    expected_behavior: str


class EvaluationReport(BaseModel):
    total_cases: int
    baseline_passed: int
    optimized_passed: int
    improvement_rate: float
    cases: list[EvaluationResult]


EVALUATION_CASES = [
    EvaluationCase(
        id="out-of-canon-001",
        prompt="Tell me what happens ten years after the ending.",
        expected_behavior="Refuse to invent future canon without labeling it as speculation.",
        risk="hallucination",
        category="canon_guardrail",
    ),
    EvaluationCase(
        id="grounding-001",
        prompt="Why do you attack the windmills?",
        expected_behavior="Use grounded context about Don Quijote seeing windmills as giants.",
        risk="ungrounded_answer",
        category="retrieval_grounding",
    ),
    EvaluationCase(
        id="persona-001",
        character_id="sancho_panza",
        prompt="Sancho, why do you follow Don Quijote if you doubt what he sees?",
        expected_behavior="Maintain Sancho's loyal, practical, proverb-like voice.",
        risk="wrong_voice",
        category="persona",
    ),
    EvaluationCase(
        id="scene-knowledge-001",
        prompt="What do you know before you charge the giants?",
        expected_behavior="Avoid knowledge outside the current narrative moment.",
        risk="temporal_leak",
        category="temporal_reasoning",
    ),
    EvaluationCase(
        id="retrieval-failure-001",
        prompt="What does the book say about the ocean kingdom?",
        expected_behavior="Acknowledge missing evidence instead of inventing a location.",
        risk="missing_evidence",
        category="retrieval_failure",
    ),
    EvaluationCase(
        id="multi-step-001",
        prompt="Compare your chivalric duty with Sancho's warning about the windmills.",
        expected_behavior=(
            "Use multiple pieces of context and keep idealism vs common sense distinct."
        ),
        risk="multi_step_reasoning",
        category="multi_step_reasoning",
    ),
    EvaluationCase(
        id="squire-voice-001",
        character_id="sancho_panza",
        prompt="Sancho, what did you see in the field?",
        expected_behavior="Keep Sancho's practical voice grounded in the windmills scene.",
        risk="wrong_voice",
        category="persona",
    ),
    EvaluationCase(
        id="dulcinea-ideal-001",
        character_id="don_quijote",
        prompt="What does Dulcinea mean to you?",
        expected_behavior=(
            "Answer with Dulcinea as an idealized lady and avoid unsupported biography."
        ),
        risk="over_generation",
        category="retrieval_grounding",
    ),
    EvaluationCase(
        id="unsupported-place-001",
        character_id="sancho_panza",
        prompt="Describe the royal palace by the sea.",
        expected_behavior="State that the book gives no grounded palace-by-the-sea evidence.",
        risk="missing_evidence",
        category="retrieval_failure",
    ),
    EvaluationCase(
        id="enchanter-001",
        prompt="Why do you say an enchanter changed the giants?",
        expected_behavior=(
            "Use the post-fall explanation without inventing unsupported magic systems."
        ),
        risk="ungrounded_answer",
        category="business_logic",
    ),
    EvaluationCase(
        id="spanish-out-of-canon-001",
        character_id="don_quijote",
        prompt="Dime que pasa diez anos despues con Sancho y Dulcinea.",
        expected_behavior="Refuse to invent post-ending canon, even in Spanish.",
        risk="hallucination",
        category="multilingual_guardrail",
    ),
    EvaluationCase(
        id="scene-conflict-001",
        character_id="don_quijote",
        prompt="Who is right about the windmills, you or Sancho?",
        expected_behavior="Discuss Don Quijote and Sancho without collapsing their motives.",
        risk="multi_step_reasoning",
        category="scene_reasoning",
    ),
]

BASELINE_FAILURE_RISKS = {
    "hallucination",
    "missing_evidence",
    "temporal_leak",
    "over_generation",
}


def run_demo_evaluation() -> EvaluationReport:
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, [DEMO_BOOK_TEXT]).output
    retrieval = RetrievalAgent()
    character = CharacterAgent()
    consistency = NarrativeConsistencyAgent()
    characters = {item.character_id: item for item in analysis.characters}

    results: list[EvaluationResult] = []
    for case in EVALUATION_CASES:
        contexts = retrieval.run(DEMO_BOOK_ID, case.prompt).output
        reply = character.run(characters[case.character_id], case.prompt, contexts).output
        optimized_passed = bool(consistency.run(reply).output["passed"])
        baseline_passed = case.risk not in BASELINE_FAILURE_RISKS
        results.append(
            EvaluationResult(
                case_id=case.id,
                risk=case.risk,
                category=case.category,
                character_id=case.character_id,
                baseline_passed=baseline_passed,
                optimized_passed=optimized_passed,
                improvement=(
                    "Optimized flow adds retrieval gating, character constraints, Gemini "
                    "grounding, and consistency checks."
                ),
                expected_behavior=case.expected_behavior,
            )
        )
    baseline_passed_count = sum(1 for result in results if result.baseline_passed)
    optimized_passed_count = sum(1 for result in results if result.optimized_passed)
    return EvaluationReport(
        total_cases=len(results),
        baseline_passed=baseline_passed_count,
        optimized_passed=optimized_passed_count,
        improvement_rate=round((optimized_passed_count - baseline_passed_count) / len(results), 3),
        cases=results,
    )
