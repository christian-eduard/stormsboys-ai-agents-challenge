from __future__ import annotations

from storms_agents.schemas import FictionBranch
from storms_agents.storage.repository import StorageRepository


class FictionBranchStore:
    """Fiction branch history with Cloud SQL persistence and local fallback."""

    _branches: dict[str, list[FictionBranch]] = {}

    def __init__(self, repository: StorageRepository | None = None) -> None:
        self.repository = repository or StorageRepository()

    def record(self, session_id: str, branch: FictionBranch) -> FictionBranch:
        persisted = self._record_persisted(session_id, branch)
        if persisted is not None:
            return persisted
        self._branches.setdefault(session_id, []).append(branch)
        self._branches[session_id] = self._branches[session_id][-20:]
        return branch

    def list(
        self,
        session_id: str,
        character_id: str | None = None,
        limit: int = 5,
    ) -> dict[str, object]:
        persisted = self._list_persisted(session_id, character_id, limit)
        if persisted is not None:
            return {
                "session_id": session_id,
                "character_id": character_id,
                "provider": "cloud-sql-postgresql",
                "branches": persisted,
            }
        branches = [
            branch
            for branch in self._branches.get(session_id, [])
            if character_id is None or branch.character_id == character_id
        ]
        return {
            "session_id": session_id,
            "character_id": character_id,
            "provider": "local-process-memory",
            "branches": [
                branch.model_dump()
                for branch in reversed(branches[-limit:])
            ],
        }

    def reset(self) -> None:
        self._branches.clear()

    def _record_persisted(
        self,
        session_id: str,
        branch: FictionBranch,
    ) -> FictionBranch | None:
        try:
            if not self.repository.status.configured:
                return None
            return self.repository.append_fiction_branch(session_id, branch)
        except Exception:
            return None

    def _list_persisted(
        self,
        session_id: str,
        character_id: str | None,
        limit: int,
    ) -> list[dict[str, object]] | None:
        try:
            if not self.repository.status.configured:
                return None
            return self.repository.list_fiction_branches(
                session_id=session_id,
                character_id=character_id,
                limit=limit,
            )
        except Exception:
            return None
