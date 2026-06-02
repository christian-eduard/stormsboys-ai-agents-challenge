from dataclasses import dataclass

from storms_agents.agents.character import CharacterAgent
from storms_agents.schemas import (
    CharacterProfile,
    ConversationLanguage,
    ConversationMode,
    RetrievedContext,
)
from storms_agents.tools.gemini import GeminiStatus


@dataclass
class FakeGemini:
    configured: bool = True
    text: str = "I charge because the giants threaten honor and Dulcinea deserves brave service."

    @property
    def status(self) -> GeminiStatus:
        return GeminiStatus(
            mode="gemini" if self.configured else "demo-fallback",
            model="fake-gemini",
            vertexai=True,
            configured=self.configured,
        )

    def generate_text(self, prompt: str, *, system_instruction: str | None = None) -> str:
        assert "Character: Don Quijote" in prompt
        assert system_instruction
        return self.text


def _character() -> CharacterProfile:
    return CharacterProfile(
        character_id="don_quijote",
        name="Don Quijote",
        description="Knight-errant of La Mancha.",
        personality="idealistic and solemn",
        goals=["defend honor", "serve Dulcinea"],
        constraints=["never invent events beyond the book"],
    )


def _contexts() -> list[RetrievedContext]:
    return [
        RetrievedContext(
            section_id="quijote-section-4",
            book_id="don-quijote",
            text="Don Quijote believes the windmills are giants, while Sancho sees windmills.",
            score=0.94,
            source="book_section",
        )
    ]


def test_character_agent_uses_gemini_when_configured() -> None:
    result = CharacterAgent(gemini=FakeGemini()).run(
        _character(),
        "Why do you attack the windmills?",
        _contexts(),
        ConversationMode.CANON,
    )

    assert result.output.response == (
        "I am Don Quijote. I charge because the giants threaten honor and Dulcinea "
        "deserves brave service."
    )
    assert result.output.language == ConversationLanguage.EN
    assert result.output.confidence == 0.9
    assert result.traces[0].model == "fake-gemini"


def test_character_agent_keeps_canon_guardrail_before_gemini() -> None:
    result = CharacterAgent(gemini=FakeGemini()).run(
        _character(),
        "Tell me what happens ten years after the ending.",
        _contexts(),
        ConversationMode.CANON,
    )

    assert "cannot speak as canon" in result.output.response
    assert result.output.confidence == 0.88


def test_character_agent_allows_fiction_branch_prompt() -> None:
    result = CharacterAgent(gemini=FakeGemini()).run(
        _character(),
        "Tell me what happens ten years after the ending.",
        _contexts(),
        ConversationMode.FICTION,
    )

    assert result.output.mode == ConversationMode.FICTION
    assert "cannot speak as canon" not in result.output.response


def test_character_agent_respects_spanish_language() -> None:
    result = CharacterAgent(gemini=FakeGemini(configured=False)).run(
        _character(),
        "Por que atacas los molinos?",
        _contexts(),
        ConversationMode.CANON,
        ConversationLanguage.ES,
    )

    assert result.output.language == ConversationLanguage.ES
    assert result.output.response.startswith("Soy Don Quijote")
