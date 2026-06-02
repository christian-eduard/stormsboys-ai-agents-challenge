from collections.abc import Iterator
from contextlib import contextmanager
from time import perf_counter
from uuid import uuid4

from storms_agents.schemas import AgentStatus, AgentTrace


@contextmanager
def trace_span(agent_name: str, operation: str, model: str | None = None) -> Iterator[AgentTrace]:
    start = perf_counter()
    trace = AgentTrace(
        trace_id=f"trace_{uuid4().hex}",
        span_id=f"span_{uuid4().hex}",
        agent_name=agent_name,
        operation=operation,
        status=AgentStatus.SUCCESS,
        model=model,
    )
    try:
        yield trace
    except Exception:
        trace.status = AgentStatus.FAILED
        raise
    finally:
        trace.latency_ms = int((perf_counter() - start) * 1000)

