from storms_agents.agents.base import AgentResult
from storms_agents.agents.character import CharacterAgent
from storms_agents.schemas import CharacterProfile, CharacterReply, RetrievedContext


class SceneOrchestratorAgent:
    name = "SceneOrchestratorAgent"

    def __init__(self) -> None:
        self.character_agent = CharacterAgent()

    def run(
        self,
        characters: list[CharacterProfile],
        prompt: str,
        contexts: list[RetrievedContext],
    ) -> AgentResult[list[CharacterReply]]:
        replies: list[CharacterReply] = []
        traces = []
        for character in characters[:3]:
            result = self.character_agent.run(character, prompt, contexts)
            replies.append(result.output)
            traces.extend(result.traces)
        return AgentResult(output=replies, traces=traces)
