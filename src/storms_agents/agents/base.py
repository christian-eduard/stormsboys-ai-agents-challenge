from dataclasses import dataclass
from typing import Generic, TypeVar

from storms_agents.schemas import AgentTrace

T = TypeVar("T")


@dataclass(frozen=True)
class AgentResult(Generic[T]):
    output: T
    traces: list[AgentTrace]
