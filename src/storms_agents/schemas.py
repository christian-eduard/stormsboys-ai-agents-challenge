from enum import StrEnum
from typing import Literal

from pydantic import BaseModel, Field


class AgentStatus(StrEnum):
    SUCCESS = "success"
    RETRY = "retry"
    FAILED = "failed"


class ConversationMode(StrEnum):
    CANON = "CANON"
    FICTION = "FICTION"


class ConversationLanguage(StrEnum):
    EN = "en"
    ES = "es"


class AgentTrace(BaseModel):
    trace_id: str
    span_id: str
    agent_name: str
    operation: str
    status: AgentStatus
    latency_ms: int | None = None
    model: str | None = None
    input_tokens: int | None = None
    output_tokens: int | None = None


class RetrievedContext(BaseModel):
    section_id: str
    book_id: str
    text: str
    score: float = Field(ge=0)
    source: Literal["book_section", "scene", "character_profile", "publisher_note"]


class CharacterProfile(BaseModel):
    character_id: str
    name: str
    description: str
    personality: str
    speech_style: str = ""
    psychological_profile: dict[str, object] = Field(default_factory=dict)
    emotional_baseline: str = ""
    desires: list[str] = Field(default_factory=list)
    fears: list[str] = Field(default_factory=list)
    relationships: dict[str, str] = Field(default_factory=dict)
    memory_policy: str = (
        "Keep canon memory separate from fiction memory and never let fiction rewrite canon."
    )
    goals: list[str] = Field(default_factory=list)
    constraints: list[str] = Field(default_factory=list)


class ConversationMemory(BaseModel):
    session_id: str
    character_id: str
    mode: ConversationMode
    turn_count: int = 0
    canon_memory: list[str] = Field(default_factory=list)
    fiction_memory: list[str] = Field(default_factory=list)
    learned_reader_preferences: list[str] = Field(default_factory=list)
    relationship_summary: str


class CharacterReply(BaseModel):
    character_id: str
    character_name: str
    mode: ConversationMode = ConversationMode.CANON
    language: ConversationLanguage = ConversationLanguage.EN
    response: str
    thought: str | None = None
    emotional_state: str | None = None
    profile_signals: list[str] = Field(default_factory=list)
    citations: list[str] = Field(default_factory=list)
    confidence: float = Field(ge=0, le=1)


class FictionBranch(BaseModel):
    branch_id: str
    book_id: str
    character_id: str
    seed_prompt: str
    premise: str
    canon_anchor_citations: list[str] = Field(default_factory=list)
    continuation: str


class BookAnalysis(BaseModel):
    title: str
    summary: str
    characters: list[CharacterProfile]
    places: list[str] = Field(default_factory=list)
    scenes: list[str] = Field(default_factory=list)


class UploadedBook(BaseModel):
    book_id: str
    title: str
    author: str = "Unknown"
    rights: str
    owner_user_id: str
    tenant_id: str
    status: str = "ready_for_review"
    language: ConversationLanguage = ConversationLanguage.EN
    sections: int = Field(ge=0)
    characters: int = Field(ge=0)
    scenes: int = Field(ge=0)
    created_at: str | None = None


class NarrationPlan(BaseModel):
    voice_id: str
    style: str
    script: str
    ssml: str
    ready_for_tts: bool
    estimated_seconds: int = Field(ge=1)


class PublisherInsight(BaseModel):
    metric: str
    value: str
    recommendation: str


class PublisherReport(BaseModel):
    audience: str
    business_value: str
    engagement_score: float = Field(ge=0, le=1)
    quality_score: float = Field(ge=0, le=1)
    insights: list[PublisherInsight]
