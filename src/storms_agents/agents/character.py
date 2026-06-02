from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import (
    CharacterProfile,
    CharacterReply,
    ConversationMode,
    RetrievedContext,
)
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
        mode: ConversationMode = ConversationMode.CANON,
    ) -> AgentResult[CharacterReply]:
        with trace_span(
            self.name,
            "character.generate_canon_reply"
            if mode == ConversationMode.CANON
            else "character.generate_fiction_reply",
            model=self.gemini.status.model,
        ) as trace:
            if not contexts and mode == ConversationMode.CANON:
                response = (
                    f"I am {character.name}. I do not have grounded evidence in the book for "
                    "that question, so I should not invent an answer."
                )
                reply = CharacterReply(
                    character_id=character.character_id,
                    character_name=character.name,
                    mode=mode,
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
            response, confidence = self._generate_response(
                character,
                question,
                evidence,
                contexts,
                mode,
            )

            reply = CharacterReply(
                character_id=character.character_id,
                character_name=character.name,
                mode=mode,
                response=response,
                thought=(
                    "Use grounded context and stay inside canon constraints."
                    if mode == ConversationMode.CANON
                    else "Create a separated fiction branch anchored to book context."
                ),
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
        mode: ConversationMode,
    ) -> tuple[str, float]:
        if mode == ConversationMode.CANON and self._asks_beyond_canon(question):
            return (
                f"I am {character.name}. I cannot speak as canon about events beyond the book. "
                "I can only answer from what the story gives us.",
                0.88,
            )

        if not self.gemini.status.configured:
            return self._deterministic_response(character, evidence, mode), 0.82

        prompt = self._build_prompt(character, question, evidence, contexts, mode)
        try:
            generated = self.gemini.generate_text(
                prompt,
                system_instruction=self._system_instruction(character, mode),
            ).strip()
        except Exception:
            return self._deterministic_response(character, evidence, mode), 0.7

        if not generated:
            return self._deterministic_response(character, evidence, mode), 0.7
        return self._ensure_character_voice(character, generated), 0.9

    def _build_prompt(
        self,
        character: CharacterProfile,
        question: str,
        evidence: str,
        contexts: list[RetrievedContext],
        mode: ConversationMode,
    ) -> str:
        citations = ", ".join(context.section_id for context in contexts) or "none"
        mode_rules = (
            "Mode: CANON. Use only the supplied evidence. Do not invent plot events."
            if mode == ConversationMode.CANON
            else (
                "Mode: FICTION. Create an explicitly alternative continuation. Stay in the "
                "character voice and anchor the branch to the supplied evidence, but do not "
                "present new events as canon."
            )
        )
        return (
            f"Character: {character.name}\n"
            f"Personality: {character.personality}\n"
            f"Goals: {', '.join(character.goals) or 'unknown'}\n"
            f"Constraints: {', '.join(character.constraints) or 'stay in canon'}\n"
            f"{mode_rules}\n"
            f"Evidence citations: {citations}\n"
            f"Evidence: {evidence}\n"
            f"Reader question: {question}\n"
            "Answer in 2-4 sentences."
        )

    def _system_instruction(self, character: CharacterProfile, mode: ConversationMode) -> str:
        if mode == ConversationMode.FICTION:
            return (
                "You are a fiction-branch literary character agent. Answer in first person as "
                f"the character. Start with 'I am {character.name}.' Build an explicitly "
                "alternative continuation anchored in the supplied book evidence. Never claim "
                "the new branch is canon."
            )
        return (
            "You are a grounded literary character agent. Answer in first person as the "
            f"character. Start with 'I am {character.name}.' Use only the supplied "
            "evidence. Do not invent plot events."
        )

    def _deterministic_response(
        self,
        character: CharacterProfile,
        evidence: str,
        mode: ConversationMode,
    ) -> str:
        if mode == ConversationMode.FICTION:
            return (
                f"I am {character.name}. In this alternative branch, I begin from the book's "
                f"memory: {evidence} From there, we may imagine a new path, marked as fiction."
            )
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
