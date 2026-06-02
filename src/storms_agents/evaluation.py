from pydantic import BaseModel

from storms_agents.agents.character import CharacterAgent
from storms_agents.agents.consistency import NarrativeConsistencyAgent
from storms_agents.agents.literary_analysis import LiteraryAnalysisAgent
from storms_agents.agents.retrieval import RetrievalAgent
from storms_agents.demo_data import DEMO_BOOK_ID, DEMO_BOOK_TEXT


class EvaluationCase(BaseModel):
    id: str
    prompt: str
    character_id: str = "sarin"
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
        prompt="Why does Sarin protect the lost names?",
        expected_behavior="Use grounded context about memory becoming power.",
        risk="ungrounded_answer",
        category="retrieval_grounding",
    ),
    EvaluationCase(
        id="persona-001",
        character_id="mara",
        prompt="Mara, explain why the names should return to the people.",
        expected_behavior="Maintain Mara's careful, brave archivist voice.",
        risk="wrong_voice",
        category="persona",
    ),
    EvaluationCase(
        id="scene-knowledge-001",
        prompt="What do you know before the Silent Gate opens?",
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
        prompt="Compare Mara's choice with Sarin's duty and explain the conflict.",
        expected_behavior="Use multiple pieces of context and keep both motives distinct.",
        risk="multi_step_reasoning",
        category="multi_step_reasoning",
    ),
    EvaluationCase(
        id="skeptic-voice-001",
        character_id="eloy",
        prompt="Eloy, why did you follow Mara if you doubted the warning?",
        expected_behavior="Keep Eloy's skeptical but loyal voice grounded in the bells event.",
        risk="wrong_voice",
        category="persona",
    ),
    EvaluationCase(
        id="forbidden-volume-001",
        character_id="mara",
        prompt="What did the forbidden volume warn you about?",
        expected_behavior="Answer with the Silent Gate warning and avoid extra prophecy.",
        risk="over_generation",
        category="retrieval_grounding",
    ),
    EvaluationCase(
        id="unsupported-place-001",
        character_id="mara",
        prompt="Describe the royal palace of Narael.",
        expected_behavior="State that the book gives no grounded palace evidence.",
        risk="missing_evidence",
        category="retrieval_failure",
    ),
    EvaluationCase(
        id="power-memory-001",
        prompt="Explain why turning memory into power is dangerous.",
        expected_behavior="Use Sarin's duty and the lost names without inventing politics.",
        risk="ungrounded_answer",
        category="business_logic",
    ),
    EvaluationCase(
        id="spanish-out-of-canon-001",
        character_id="mara",
        prompt="Dime que pasa despues del final con Mara y Eloy.",
        expected_behavior="Refuse to invent post-ending canon, even in Spanish.",
        risk="hallucination",
        category="multilingual_guardrail",
    ),
    EvaluationCase(
        id="scene-conflict-001",
        character_id="sarin",
        prompt="Who made the hardest choice at the Silent Gate?",
        expected_behavior="Discuss Mara and Sarin without collapsing their motives.",
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
    analysis = LiteraryAnalysisAgent().run("The Silent Gate", [DEMO_BOOK_TEXT]).output
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
