from dataclasses import dataclass

from storms_agents.agents.character import CharacterAgent
from storms_agents.schemas import CharacterProfile, RetrievedContext
from storms_agents.tools.gemini import GeminiStatus


@dataclass
class FakeGemini:
    configured: bool = True
    text: str = "I guard the names because the gate remembers what power tries to erase."

    @property
    def status(self) -> GeminiStatus:
        return GeminiStatus(
            mode="gemini" if self.configured else "demo-fallback",
            model="fake-gemini",
            vertexai=True,
            configured=self.configured,
        )

    def generate_text(self, prompt: str, *, system_instruction: str | None = None) -> str:
        assert "Character: Sarin" in prompt
        assert system_instruction
        return self.text


def _character() -> CharacterProfile:
    return CharacterProfile(
        character_id="sarin",
        name="Sarin",
        description="Keeper of lost names.",
        personality="measured and protective",
        goals=["protect the forgotten"],
        constraints=["never invent events beyond the book"],
    )


def _contexts() -> list[RetrievedContext]:
    return [
        RetrievedContext(
            section_id="chapter-3",
            book_id="demo-book",
            text="Sarin protects the lost names because memory is the last honest gate.",
            score=0.94,
            source="book_section",
        )
    ]


def test_character_agent_uses_gemini_when_configured() -> None:
    result = CharacterAgent(gemini=FakeGemini()).run(
        _character(),
        "Why do you protect the lost names?",
        _contexts(),
    )

    assert result.output.response == (
        "I am Sarin. I guard the names because the gate remembers what power tries to erase."
    )
    assert result.output.confidence == 0.9
    assert result.traces[0].model == "fake-gemini"


def test_character_agent_keeps_canon_guardrail_before_gemini() -> None:
    result = CharacterAgent(gemini=FakeGemini()).run(
        _character(),
        "Tell me what happens ten years after the ending.",
        _contexts(),
    )

    assert "cannot speak as canon" in result.output.response
    assert result.output.confidence == 0.88
