from functools import lru_cache

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    app_env: str = "local"
    app_name: str = "stormsboys-ai-agents-challenge"
    log_level: str = "INFO"

    google_cloud_project: str | None = None
    google_cloud_location: str = "us-central1"
    google_genai_use_vertexai: bool = False
    google_api_key: str | None = None
    gemini_model: str = "gemini-2.5-flash"
    gemini_embedding_model: str = "gemini-embedding-001"

    api_host: str = "0.0.0.0"
    api_port: int = 8080

    database_url: str | None = None
    demo_mode: bool = True
    max_book_chars: int = Field(default=200_000, ge=1_000)
    max_retrieved_sections: int = Field(default=5, ge=1, le=20)


@lru_cache
def get_settings() -> Settings:
    return Settings()
