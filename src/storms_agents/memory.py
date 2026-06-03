from __future__ import annotations

from dataclasses import dataclass, field

from storms_agents.schemas import ConversationMemory, ConversationMode
from storms_agents.storage.repository import StorageRepository


@dataclass
class _MemoryBucket:
    canon_memory: list[str] = field(default_factory=list)
    fiction_memory: list[str] = field(default_factory=list)
    learned_reader_preferences: list[str] = field(default_factory=list)
    turn_count: int = 0


class ConversationMemoryStore:
    """Conversation memory with Cloud SQL persistence and local fallback."""

    _buckets: dict[tuple[str, str, ConversationMode], _MemoryBucket] = {}

    def __init__(self, repository: StorageRepository | None = None) -> None:
        self.repository = repository or StorageRepository()

    def snapshot(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
    ) -> ConversationMemory:
        persisted = self._load_persisted(session_id, character_id, mode)
        if persisted is not None:
            return persisted
        bucket = self._bucket(session_id, character_id, mode)
        return self._to_model(session_id, character_id, mode, bucket)

    def record(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
        question: str,
        response: str,
    ) -> ConversationMemory:
        memory_line = self._memory_line(question, response)
        preference = self._reader_preference(question)
        persisted = self._record_persisted(
            session_id=session_id,
            character_id=character_id,
            mode=mode,
            question=question,
            response=response,
            memory_line=memory_line,
            preference=preference,
        )
        if persisted is not None:
            return persisted

        bucket = self._bucket(session_id, character_id, mode)
        bucket.turn_count += 1
        if preference and preference not in bucket.learned_reader_preferences:
            bucket.learned_reader_preferences.append(preference)
        if mode == ConversationMode.FICTION:
            bucket.fiction_memory.append(memory_line)
            bucket.fiction_memory = bucket.fiction_memory[-5:]
        else:
            bucket.canon_memory.append(memory_line)
            bucket.canon_memory = bucket.canon_memory[-5:]
        return self._to_model(session_id, character_id, mode, bucket)

    def reset(self) -> None:
        self._buckets.clear()

    def _load_persisted(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
    ) -> ConversationMemory | None:
        try:
            if not self.repository.status.configured:
                return None
            return self.repository.load_conversation_memory(session_id, character_id, mode)
        except Exception:
            return None

    def _record_persisted(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
        question: str,
        response: str,
        memory_line: str,
        preference: str | None,
    ) -> ConversationMemory | None:
        try:
            if not self.repository.status.configured:
                return None
            return self.repository.append_conversation_memory(
                session_id=session_id,
                character_id=character_id,
                mode=mode,
                question=question,
                response=response,
                memory_line=memory_line,
                reader_preference=preference,
            )
        except Exception:
            return None

    def _bucket(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
    ) -> _MemoryBucket:
        return self._buckets.setdefault((session_id, character_id, mode), _MemoryBucket())

    def _to_model(
        self,
        session_id: str,
        character_id: str,
        mode: ConversationMode,
        bucket: _MemoryBucket,
    ) -> ConversationMemory:
        if bucket.turn_count:
            relationship = (
                f"{bucket.turn_count} remembered turn(s). The character can adapt tone and "
                "recall the reader's interests without changing canon."
            )
        else:
            relationship = "No prior turns for this character, mode, and session."
        return ConversationMemory(
            session_id=session_id,
            character_id=character_id,
            mode=mode,
            turn_count=bucket.turn_count,
            canon_memory=bucket.canon_memory,
            fiction_memory=bucket.fiction_memory,
            learned_reader_preferences=bucket.learned_reader_preferences,
            relationship_summary=relationship,
        )

    def _reader_preference(self, question: str) -> str | None:
        lowered = question.lower()
        if "psychology" in lowered or "psicolog" in lowered:
            return "reader asks for psychological motivation"
        if "voice" in lowered or "voz" in lowered:
            return "reader cares about character voice"
        if "fiction" in lowered or "ficcion" in lowered or "what if" in lowered:
            return "reader explores alternative fiction branches"
        if "canon" in lowered or "real" in lowered:
            return "reader checks canon truth"
        return None

    def _memory_line(self, question: str, response: str) -> str:
        compact_question = " ".join(question.split())[:120]
        compact_response = " ".join(response.split())[:160]
        return f"Reader asked: {compact_question} | Character answered: {compact_response}"
