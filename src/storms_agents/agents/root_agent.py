from google.adk.agents.llm_agent import Agent

from storms_agents.config import get_settings

settings = get_settings()


def describe_submission_scope() -> dict[str, str]:
    """Return the challenge scope without accessing external project data."""
    return {
        "track": "Track 2 - Optimize Existing Agents",
        "product": "Multi-agent literary intelligence platform",
        "rule": "No code, config, data, or resource IDs from other projects",
    }


root_agent = Agent(
    model=settings.gemini_model,
    name="stormsboys_literary_orchestrator",
    description="Coordinates literary agents for the Stormsboys AI Agents Challenge.",
    instruction=(
        "You are the root orchestrator for a new, isolated challenge project. "
        "Do not reference, copy, or depend on any unrelated project. "
        "Coordinate analysis, retrieval, character, scene, consistency, voice, "
        "publisher insight, and evaluation agents for a literary intelligence demo."
    ),
    tools=[describe_submission_scope],
)
