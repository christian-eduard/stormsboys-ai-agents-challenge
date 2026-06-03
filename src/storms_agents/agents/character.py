import re

from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import (
    CharacterProfile,
    CharacterReply,
    ConversationLanguage,
    ConversationMemory,
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
        language: ConversationLanguage = ConversationLanguage.EN,
        memory: ConversationMemory | None = None,
    ) -> AgentResult[CharacterReply]:
        with trace_span(
            self.name,
            "character.generate_canon_reply"
            if mode == ConversationMode.CANON
            else "character.generate_fiction_reply",
            model=self.gemini.status.model,
        ) as trace:
            if not contexts and mode == ConversationMode.CANON:
                response = self._missing_evidence_response(character, language)
                reply = CharacterReply(
                    character_id=character.character_id,
                    character_name=character.name,
                    mode=mode,
                    language=language,
                    response=response,
                    thought="Acknowledge missing retrieval evidence instead of inventing canon.",
                    emotional_state="careful",
                    profile_signals=self._profile_signals(character, memory),
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
                language,
                memory,
            )

            reply = CharacterReply(
                character_id=character.character_id,
                character_name=character.name,
                mode=mode,
                language=language,
                response=response,
                thought=(
                    "Use grounded context and stay inside canon constraints."
                    if mode == ConversationMode.CANON
                    else "Create a separated fiction branch anchored to book context."
                ),
                emotional_state=character.emotional_baseline or "focused",
                profile_signals=self._profile_signals(character, memory),
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
        language: ConversationLanguage,
        memory: ConversationMemory | None,
    ) -> tuple[str, float]:
        if mode == ConversationMode.CANON and self._asks_beyond_canon(question):
            return (
                self._beyond_canon_response(character, language),
                0.88,
            )

        if not self.gemini.status.configured:
            return self._deterministic_response(
                character,
                evidence,
                mode,
                language,
                memory,
            ), 0.84

        prompt = self._build_prompt(character, question, evidence, contexts, mode, language, memory)
        try:
            generated = self.gemini.generate_text(
                prompt,
                system_instruction=self._system_instruction(character, mode, language),
            ).strip()
        except Exception:
            return self._deterministic_response(
                character,
                evidence,
                mode,
                language,
                memory,
            ), 0.72

        if not generated:
            return self._deterministic_response(
                character,
                evidence,
                mode,
                language,
                memory,
            ), 0.72
        cleaned = self._strip_inline_citations(generated)
        voiced = self._ensure_character_voice(character, cleaned, language)
        return self._enrich_generated_response(character, voiced, language, memory), 0.9

    def _build_prompt(
        self,
        character: CharacterProfile,
        question: str,
        evidence: str,
        contexts: list[RetrievedContext],
        mode: ConversationMode,
        language: ConversationLanguage,
        memory: ConversationMemory | None,
    ) -> str:
        citations = ", ".join(context.section_id for context in contexts) or "none"
        memory_summary = memory.relationship_summary if memory else "No prior memory."
        language_rule = (
            "Answer in English." if language == ConversationLanguage.EN else "Responde en espanol."
        )
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
            f"Speech style: {character.speech_style or 'character-specific first person'}\n"
            f"Psychology: {character.psychological_profile}\n"
            f"Desires: {', '.join(character.desires) or 'unknown'}\n"
            f"Fears: {', '.join(character.fears) or 'unknown'}\n"
            f"Memory policy: {character.memory_policy}\n"
            f"Conversation memory: {memory_summary}\n"
            f"Goals: {', '.join(character.goals) or 'unknown'}\n"
            f"Constraints: {', '.join(character.constraints) or 'stay in canon'}\n"
            f"{mode_rules}\n"
            f"Language: {language.value}. {language_rule}\n"
            f"Evidence citations: {citations}\n"
            f"Evidence: {evidence}\n"
            f"Reader question: {question}\n"
            "Answer in 2-4 sentences."
        )

    def _system_instruction(
        self,
        character: CharacterProfile,
        mode: ConversationMode,
        language: ConversationLanguage,
    ) -> str:
        language_rule = (
            f"Answer in English and start with 'I am {character.name}.'"
            if language == ConversationLanguage.EN
            else f"Responde siempre en espanol y empieza con 'Soy {character.name}.'"
        )
        if mode == ConversationMode.FICTION:
            return (
                "You are a fiction-branch literary character agent. Answer in first person as "
                "the character. Build an explicitly "
                "alternative continuation anchored in the supplied book evidence. Never claim "
                f"the new branch is canon. {language_rule}"
            )
        return (
            "You are a grounded literary character agent. Answer in first person as the "
            f"character. Use only the supplied evidence. Do not invent plot events. "
            f"{language_rule}"
        )

    def _deterministic_response(
        self,
        character: CharacterProfile,
        evidence: str,
        mode: ConversationMode,
        language: ConversationLanguage,
        memory: ConversationMemory | None,
    ) -> str:
        memory_clause_en = self._memory_clause(memory, ConversationLanguage.EN)
        memory_clause_es = self._memory_clause(memory, ConversationLanguage.ES)
        evidence_es = self._localize_evidence(evidence, ConversationLanguage.ES)
        if mode == ConversationMode.FICTION:
            if language == ConversationLanguage.ES:
                return (
                    f"Soy {character.name}. Mi animo sigue gobernado por mi codigo: "
                    f"{self._psychology_summary(character, language)} {memory_clause_es} "
                    "En esta rama alternativa parto de una verdad del libro, no de un capricho: "
                    f"{evidence_es} Desde ahi podemos abrir otra senda, marcada siempre como "
                    "ficcion."
                )
            return (
                f"I am {character.name}. My inner law is still this: "
                f"{self._psychology_summary(character, language)} {memory_clause_en} "
                f"In this alternative branch I begin from book evidence, not from chaos: "
                f"{evidence} From there, we may open a new path, always marked as fiction."
            )
        if language == ConversationLanguage.ES:
            return (
                f"Soy {character.name}. No embisto por simple furia, sino porque mi deseo y mi "
                f"temor se encuentran: {self._psychology_summary(character, language)} "
                f"{memory_clause_es} En el canon debo ajustarme a esta prueba del libro: "
                f"{evidence_es}"
            )
        return (
            f"I am {character.name}. I do not act from noise alone; my desire and my fear meet "
            f"inside the vow: {self._psychology_summary(character, language)} "
            f"{memory_clause_en} In canon I must stay with this book evidence: {evidence}"
        )

    def _missing_evidence_response(
        self,
        character: CharacterProfile,
        language: ConversationLanguage,
    ) -> str:
        if language == ConversationLanguage.ES:
            return (
                f"Soy {character.name}. No tengo evidencia fundamentada en el libro para "
                "esa pregunta, asi que no debo inventar una respuesta. Puedo hablar de mi "
                "animo y de mis limites, pero no convertir una duda en canon."
            )
        return (
            f"I am {character.name}. I do not have grounded evidence in the book for "
            "that question, so I should not invent an answer. I can reveal my temperament "
            "and limits, but I cannot turn uncertainty into canon."
        )

    def _beyond_canon_response(
        self,
        character: CharacterProfile,
        language: ConversationLanguage,
    ) -> str:
        if language == ConversationLanguage.ES:
            return (
                f"Soy {character.name}. No puedo hablar como canon sobre acontecimientos "
                "posteriores al libro. Solo puedo responder desde lo que la historia nos da."
            )
        return (
            f"I am {character.name}. I cannot speak as canon about events beyond the book. "
            "I can only answer from what the story gives us."
        )

    def _ensure_character_voice(
        self,
        character: CharacterProfile,
        response: str,
        language: ConversationLanguage,
    ) -> str:
        if character.name.lower() in response.lower():
            return response
        if language == ConversationLanguage.ES:
            return f"Soy {character.name}. {response}"
        return f"I am {character.name}. {response}"

    def _strip_inline_citations(self, response: str) -> str:
        cleaned = re.sub(r"\s*\((?:quijote-section-\d+\s*,?\s*)+\)", "", response)
        cleaned = re.sub(r"\s+quijote-section-\d+", "", cleaned)
        return " ".join(cleaned.split())

    def _enrich_generated_response(
        self,
        character: CharacterProfile,
        response: str,
        language: ConversationLanguage,
        memory: ConversationMemory | None,
    ) -> str:
        if not character.desires and not character.fears:
            return response
        lowered = response.lower()
        has_psychology = any(term in lowered for term in ("deseo", "temo", "desire", "fear"))
        additions: list[str] = []
        if not has_psychology:
            additions.append(self._psychology_sentence(character, language))
        has_memory_reference = "recuerdo" in lowered or "remember" in lowered
        if memory and memory.turn_count > 0 and not has_memory_reference:
            additions.append(self._memory_sentence(memory, language))
        if not additions:
            return response
        return f"{response} {' '.join(additions)}"

    def _asks_beyond_canon(self, question: str) -> bool:
        lowered = question.lower()
        future_markers = (
            "future",
            "ten years",
            "years later",
            "after the ending",
            "after the book",
            "after the novel",
            "tomorrow",
            "next year",
            "futuro",
            "diez anos",
            "diez años",
            "anos despues",
            "años despues",
            "anos después",
            "años después",
            "despues del final",
            "después del final",
            "despues del libro",
            "después del libro",
            "despues de la novela",
            "después de la novela",
        )
        return any(term in lowered for term in future_markers)

    def _profile_signals(
        self,
        character: CharacterProfile,
        memory: ConversationMemory | None,
    ) -> list[str]:
        speech = (
            f"speech: {character.speech_style}"
            if character.speech_style
            else "speech: first person"
        )
        emotion = (
            f"emotion: {character.emotional_baseline}"
            if character.emotional_baseline
            else "emotion: focused"
        )
        signals = [
            speech,
            emotion,
            f"memory turns: {memory.turn_count if memory else 0}",
        ]
        if character.desires:
            signals.append(f"desire: {character.desires[0]}")
        if character.fears:
            signals.append(f"fear: {character.fears[0]}")
        return signals

    def _psychology_summary(
        self,
        character: CharacterProfile,
        language: ConversationLanguage,
    ) -> str:
        desire = character.desires[0] if character.desires else character.goals[0]
        fear = character.fears[0] if character.fears else "betraying the story"
        if language == ConversationLanguage.ES:
            desire = self._localize_profile_phrase(desire)
            fear = self._localize_profile_phrase(fear)
            return f"deseo {desire}; temo {fear}."
        return f"I desire {desire}; I fear {fear}."

    def _memory_clause(
        self,
        memory: ConversationMemory | None,
        language: ConversationLanguage,
    ) -> str:
        if memory is None or memory.turn_count == 0:
            return (
                "Aun no guardo recuerdos previos de esta conversacion."
                if language == ConversationLanguage.ES
                else "I do not yet carry previous memories from this conversation."
            )
        preferences = ", ".join(memory.learned_reader_preferences) or "your earlier questions"
        if language == ConversationLanguage.ES:
            return (
                f"Recuerdo {memory.turn_count} turno(s) contigo y ajusto mi tono a: "
                f"{preferences}, sin cambiar el canon."
            )
        return (
            f"I remember {memory.turn_count} turn(s) with you and adapt to: "
            f"{preferences}, without changing canon."
        )

    def _psychology_sentence(
        self,
        character: CharacterProfile,
        language: ConversationLanguage,
    ) -> str:
        summary = self._psychology_summary(character, language)
        if language == ConversationLanguage.ES:
            return f"En lo profundo de mi animo, {summary}"
        return f"Deep in my temperament, {summary}"

    def _memory_sentence(
        self,
        memory: ConversationMemory,
        language: ConversationLanguage,
    ) -> str:
        if language == ConversationLanguage.ES:
            return (
                f"Recuerdo {memory.turn_count} turno(s) contigo y no permito que ese "
                "aprendizaje altere el canon."
            )
        return (
            f"I remember {memory.turn_count} turn(s) with you, and that learning does "
            "not rewrite canon."
        )

    def _localize_profile_phrase(self, phrase: str) -> str:
        translations = {
            "Prove that chivalric virtue still matters": (
                "probar que la virtud caballeresca todavia importa"
            ),
            "Being merely Alonso Quijano again": "volver a ser solo Alonso Quijano",
            "Protect himself and his master": "protegerse y proteger a su amo",
            "Beatings, hunger, and pointless danger": (
                "los golpes, el hambre y el peligro sin sentido"
            ),
        }
        return translations.get(phrase, phrase)

    def _localize_evidence(self, evidence: str, language: ConversationLanguage) -> str:
        if language == ConversationLanguage.EN:
            return evidence
        translations = {
            (
                "In the windmill scene, Don Quijote believes the windmills are giants. "
                "Sancho warns him that they are only windmills, but Don Quijote charges "
                "and is knocked down by the turning sails."
            ): (
                "En la escena de los molinos, Don Quijote cree que los molinos son "
                "gigantes. Sancho le advierte que solo son molinos, pero Don Quijote "
                "carga y cae derribado por las aspas."
            ),
            (
                "After the fall, Don Quijote explains that an enchanter changed the giants "
                "into windmills to rob him of glory. The scene reveals the conflict between "
                "his chivalric imagination and Sancho's practical reality."
            ): (
                "Tras la caida, Don Quijote explica que un encantador transformo los "
                "gigantes en molinos para robarle la gloria. La escena revela el conflicto "
                "entre su imaginacion caballeresca y la realidad practica de Sancho."
            ),
        }
        return translations.get(evidence, evidence)
