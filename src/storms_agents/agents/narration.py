from storms_agents.agents.base import AgentResult
from storms_agents.observability import trace_span
from storms_agents.schemas import NarrationPlan


class VoiceNarrationAgent:
    name = "VoiceNarrationAgent"

    def run(
        self,
        scene_text: str,
        *,
        voice_id: str = "en-GB-literary-warm",
    ) -> AgentResult[NarrationPlan]:
        with trace_span(self.name, "voice.prepare_narration") as trace:
            script = " ".join(scene_text.split())[:420]
            ssml = (
                f'<speak><voice name="{voice_id}">'
                f'<prosody rate="medium" pitch="-1st">{script}</prosody>'
                "</voice></speak>"
            )
            plan = NarrationPlan(
                voice_id=voice_id,
                style="warm literary narration with restrained dramatic pacing",
                script=script,
                ssml=ssml,
                ready_for_tts=True,
                estimated_seconds=max(8, round(len(script.split()) / 2.4)),
            )
            trace.input_tokens = len(scene_text.split())
            trace.output_tokens = len(plan.script.split())
            return AgentResult(output=plan, traces=[trace])
