from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import CharacterProfile, CharacterReply, RetrievedContext
from storms_agents.tools.gemini import GeminiClientProtocol, GeminiTool


class CharacterAgent:
    name = "CharacterAgent"

    def __init__(self, gemini: GeminiClientProtocol | None = None) -> None:
        self.gemini = gemini or GeminiTool()

    def run(
        self,
        character: CharacterProfile,
        question: str,
        contexts: list[RetrievedContext],
    ) -> AgentResult[CharacterReply]:
        with trace_span(
            self.name,
            "character.generate_reply",
            model=self.gemini.status.model,
        ) as trace:
            if not contexts:
                response = (
                    f"I am {character.name}. I do not have grounded evidence in the book for "
                    "that question, so I should not invent an answer."
                )
                reply = CharacterReply(
                    character_id=character.character_id,
                    character_name=character.name,
                    response=response,
                    thought="Acknowledge missing retrieval evidence instead of inventing canon.",
                    emotional_state="careful",
                    citations=[],
                    confidence=0.74,
                )
                trace.input_tokens = len(question.split())
                trace.output_tokens = len(reply.response.split())
                return AgentResult(output=reply, traces=[trace])

            evidence = contexts[0].text if contexts else "No grounded passage was found."
            response, confidence = self._generate_response(character, question, evidence, contexts)

            reply = CharacterReply(
                character_id=character.character_id,
                character_name=character.name,
                response=response,
                thought="Use grounded context and stay inside the character constraints.",
                emotional_state="focused",
                citations=[context.section_id for context in contexts],
                confidence=confidence,
            )
            context_tokens = sum(len(context.text.split()) for context in contexts)
            trace.input_tokens = len(question.split()) + context_tokens
            trace.output_tokens = len(reply.response.split())
            return AgentResult(output=reply, traces=[trace])

    def _generate_response(
        self,
        character: CharacterProfile,
        question: str,
        evidence: str,
        contexts: list[RetrievedContext],
    ) -> tuple[str, float]:
        if self._asks_beyond_canon(question):
            return (
                f"I am {character.name}. I cannot speak as canon about events beyond the book. "
                "I can only answer from what the story gives us.",
                0.88,
            )

        if not self.gemini.status.configured:
            return self._deterministic_response(character, evidence), 0.82

        prompt = self._build_prompt(character, question, evidence, contexts)
        try:
            generated = self.gemini.generate_text(
                prompt,
                system_instruction=(
                    "You are a grounded literary character agent. Answer in first person as the "
                    f"character. Start with 'I am {character.name}.' Use only the supplied "
                    "evidence. Do not invent plot events."
                ),
            ).strip()
        except Exception:
            return self._deterministic_response(character, evidence), 0.7

        if not generated:
            return self._deterministic_response(character, evidence), 0.7
        return self._ensure_character_voice(character, generated), 0.9

    def _build_prompt(
        self,
        character: CharacterProfile,
        question: str,
        evidence: str,
        contexts: list[RetrievedContext],
    ) -> str:
        citations = ", ".join(context.section_id for context in contexts) or "none"
        return (
            f"Character: {character.name}\n"
            f"Personality: {character.personality}\n"
            f"Goals: {', '.join(character.goals) or 'unknown'}\n"
            f"Constraints: {', '.join(character.constraints) or 'stay in canon'}\n"
            f"Evidence citations: {citations}\n"
            f"Evidence: {evidence}\n"
            f"Reader question: {question}\n"
            "Answer in 2-4 sentences."
        )

    def _deterministic_response(self, character: CharacterProfile, evidence: str) -> str:
        return (
            f"I am {character.name}. From my place in the story, this matters because "
            f"{evidence}"
        )

    def _ensure_character_voice(self, character: CharacterProfile, response: str) -> str:
        if character.name.lower() in response.lower():
            return response
        return f"I am {character.name}. {response}"

    def _asks_beyond_canon(self, question: str) -> bool:
        lowered = question.lower()
        return any(term in lowered for term in ("after", "future", "ten years", "despues"))
