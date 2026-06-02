from dataclasses import dataclass
from typing import Any, Protocol

from storms_agents.config import Settings, get_settings


class GeminiClientProtocol(Protocol):
    @property
    def status(self) -> "GeminiStatus":
        """Return runtime and model configuration."""

    def generate_text(self, prompt: str, *, system_instruction: str | None = None) -> str:
        """Generate text from a prompt."""


@dataclass(frozen=True)
class GeminiStatus:
    mode: str
    model: str
    vertexai: bool
    configured: bool


class GeminiTool:
    def __init__(self, settings: Settings | None = None) -> None:
        self.settings = settings or get_settings()
        self._client: Any | None = None

    @property
    def status(self) -> GeminiStatus:
        configured = bool(self.settings.google_api_key) or bool(self.settings.google_cloud_project)
        return GeminiStatus(
            mode="gemini" if configured else "demo-fallback",
            model=self.settings.gemini_model,
            vertexai=self.settings.google_genai_use_vertexai,
            configured=configured,
        )

    def _get_client(self) -> Any:
        if self._client is not None:
            return self._client

        from google import genai

        if self.settings.google_genai_use_vertexai:
            self._client = genai.Client(
                vertexai=True,
                project=self.settings.google_cloud_project,
                location=self.settings.google_cloud_location,
            )
        else:
            self._client = genai.Client(api_key=self.settings.google_api_key)
        return self._client

    def generate_text(self, prompt: str, *, system_instruction: str | None = None) -> str:
        if not self.status.configured:
            return self._fallback_response(prompt, system_instruction=system_instruction)

        response = self._get_client().models.generate_content(
            model=self.settings.gemini_model,
            contents=prompt,
            config={"system_instruction": system_instruction} if system_instruction else None,
        )
        return response.text or ""

    def _fallback_response(self, prompt: str, *, system_instruction: str | None = None) -> str:
        instruction = system_instruction or "demo literary agent"
        compact_prompt = " ".join(prompt.split())[:260]
        return (
            f"[demo-fallback:{self.settings.gemini_model}] {instruction}. "
            f"Prompt summary: {compact_prompt}"
        )
