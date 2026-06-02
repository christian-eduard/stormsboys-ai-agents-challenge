from storms_agents.config import Settings
from storms_agents.tools.gemini import GeminiTool


def test_gemini_tool_fallback_without_credentials() -> None:
    tool = GeminiTool(
        Settings(
            google_api_key=None,
            google_cloud_project=None,
            gemini_model="gemini-test",
        )
    )

    response = tool.generate_text(
        "Explain why Don Quijote attacks the windmills.",
        system_instruction="Stay grounded in the book.",
    )

    assert tool.status.mode == "demo-fallback"
    assert "gemini-test" in response
    assert "Don Quijote attacks" in response
