from dataclasses import dataclass

from storms_agents.agents.literary_analysis import LiteraryAnalysisAgent
from storms_agents.tools.gemini import GeminiStatus


@dataclass
class FakeGeminiAnalysis:
    configured: bool = True
    text: str = """
    {
      "summary": "Mara crosses a bridge to recover a bell while Tomas protects a secret.",
      "places": ["Silent Bridge", "Archive"],
      "scenes": ["Mara crosses the Silent Bridge", "Tomas waits near the archive"],
      "characters": [
        {
          "name": "Mara",
          "description": "A determined traveler carrying an atlas and a promise.",
          "personality": "curious, brave, truth-seeking",
          "speech_style": "Direct, observant, and quietly lyrical.",
          "emotional_baseline": "alert and morally focused",
          "desires": ["recover the bell", "discover the truth"],
          "fears": ["betraying the promise"],
          "relationships": {"Tomas": "guardian of the secret"}
        },
        {
          "name": "Tomas",
          "description": "A cautious archive keeper afraid of what Mara may learn.",
          "personality": "protective, anxious, loyal to the council",
          "speech_style": "Careful and restrained.",
          "emotional_baseline": "tense but loyal",
          "desires": ["protect the council secret"],
          "fears": ["Mara discovering too much"],
          "relationships": {"Mara": "dangerous truth seeker"}
        }
      ]
    }
    """

    @property
    def status(self) -> GeminiStatus:
        return GeminiStatus(
            mode="gemini" if self.configured else "demo-fallback",
            model="fake-gemini-analysis",
            vertexai=True,
            configured=self.configured,
        )

    def generate_text(self, prompt: str, *, system_instruction: str | None = None) -> str:
        assert "Analyze this uploaded manuscript" in prompt
        assert system_instruction
        return self.text


def test_uploaded_book_analysis_uses_gemini_json_when_configured() -> None:
    sections = [
        "Mara crossed the Silent Bridge at dawn. Tomas waited near the archive, "
        "afraid that Mara would discover the council's secret."
    ]

    result = LiteraryAnalysisAgent(gemini=FakeGeminiAnalysis()).run("The Silent Bridge", sections)

    assert result.output.summary.startswith("Mara crosses a bridge")
    assert [character.name for character in result.output.characters] == ["Mara", "Tomas"]
    assert result.output.characters[0].psychological_profile["analysis_provider"] == "gemini"
    assert result.output.places == ["Silent Bridge", "Archive"]
    assert result.traces[0].model == "fake-gemini-analysis"


def test_uploaded_book_analysis_falls_back_when_gemini_json_is_invalid() -> None:
    sections = [
        "Mara crossed the Silent Bridge at dawn. Tomas waited near the archive. "
        "Mara carried a small atlas and Tomas guarded the city records."
    ]
    gemini = FakeGeminiAnalysis(text="not-json")

    result = LiteraryAnalysisAgent(gemini=gemini).run("The Silent Bridge", sections)

    assert result.output.characters
    assert result.output.characters[0].name == "Mara"
    assert "real upload-to-agent path" in result.output.summary
