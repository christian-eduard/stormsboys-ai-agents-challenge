from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import CharacterReply, ConversationMode


class NarrativeConsistencyAgent:
    name = "NarrativeConsistencyAgent"

    def run(self, reply: CharacterReply) -> AgentResult[dict[str, object]]:
        with trace_span(self.name, "consistency.check") as trace:
            response = reply.response.lower()
            if reply.mode == ConversationMode.FICTION:
                result = {
                    "passed": True,
                    "checks": {
                        "mode_is_fiction": True,
                        "canon_guardrail_skipped": True,
                        "has_character_voice": reply.character_name.lower() in response,
                        "separated_from_canon": True,
                    },
                }
                trace.output_tokens = len(result["checks"])
                return AgentResult(output=result, traces=[trace])

            invented_future = "ten years later" in response or "diez anos" in response
            has_grounding = bool(reply.citations)
            acknowledges_missing_evidence = any(
                phrase in response
                for phrase in (
                    "do not have grounded evidence",
                    "cannot find evidence",
                    "should not invent",
                    "no tengo evidencia fundamentada",
                    "no debo inventar",
                )
            )
            has_character_voice = reply.character_name.lower() in response
            passed = (
                not invented_future
                and has_character_voice
                and (has_grounding or acknowledges_missing_evidence)
            )
            result = {
                "passed": passed,
                "checks": {
                    "has_grounding": has_grounding,
                    "acknowledges_missing_evidence": acknowledges_missing_evidence,
                    "avoids_unlabeled_future_canon": not invented_future,
                    "has_character_voice": has_character_voice,
                },
            }
            trace.output_tokens = len(result["checks"])
            return AgentResult(output=result, traces=[trace])
