from importlib.resources import files

import uvicorn
from fastapi import FastAPI
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

from storms_agents import __version__
from storms_agents.agents.book_ingestion import BookIngestionAgent
from storms_agents.agents.character import CharacterAgent
from storms_agents.agents.consistency import NarrativeConsistencyAgent
from storms_agents.agents.fiction_branch import FictionBranchAgent
from storms_agents.agents.literary_analysis import LiteraryAnalysisAgent
from storms_agents.agents.narration import VoiceNarrationAgent
from storms_agents.agents.publisher_insights import PublisherInsightsAgent
from storms_agents.agents.retrieval import RetrievalAgent
from storms_agents.agents.scene_orchestrator import SceneOrchestratorAgent
from storms_agents.config import get_settings
from storms_agents.demo_data import DEMO_BOOK_ID, DEMO_BOOK_TEXT, DEMO_BOOK_TITLE
from storms_agents.evaluation import run_demo_evaluation
from storms_agents.schemas import AgentStatus, ConversationLanguage, ConversationMode
from storms_agents.storage.repository import StorageRepository
from storms_agents.tools.gemini import GeminiTool

settings = get_settings()
WEB_DIR = files("storms_agents").joinpath("web")
STATIC_DIR = WEB_DIR.joinpath("static")

app = FastAPI(
    title="Stormsboys AI Agents Challenge API",
    version=__version__,
    description="Clean challenge API for a multi-agent literary intelligence platform.",
)
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class CharacterChatRequest(BaseModel):
    character_id: str = "don_quijote"
    mode: ConversationMode = ConversationMode.CANON
    language: ConversationLanguage = ConversationLanguage.EN
    question: str


class SceneChatRequest(BaseModel):
    prompt: str


class NarrationRequest(BaseModel):
    scene_text: str = (
        "Don Quijote charges at the windmills while Sancho warns him from the road."
    )


@app.get("/", response_class=HTMLResponse)
def web_demo() -> str:
    return WEB_DIR.joinpath("index.html").read_text(encoding="utf-8")


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "version": __version__,
        "environment": settings.app_env,
    }


@app.get("/api/v1/challenge/readiness")
def challenge_readiness() -> dict[str, object]:
    gemini = GeminiTool().status
    return {
        "track": "Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise",
        "trackEvidence": "Track 2 evaluation remains available for quality evidence.",
        "projectIsolation": "new-project-no-cross-project-code",
        "agentLayer": "adk-first-python",
        "gemini": gemini.__dict__,
        "status": AgentStatus.SUCCESS,
        "demoMode": settings.demo_mode,
    }


@app.get("/api/v1/challenge/capabilities")
def challenge_capabilities() -> dict[str, object]:
    gemini = GeminiTool().status
    return {
        "judgingCriteria": {
            "technicalImplementation": "30%",
            "businessCase": "30%",
            "innovationCreativity": "20%",
            "demoPresentation": "20%",
        },
        "deliverables": [
            "public repository",
            "english description",
            "architecture diagram",
            "1-2 minute english demo video",
            "functional judge demo",
        ],
        "googleCloudTarget": [
            "Cloud Run",
            "Gemini API",
            "ADK-first agent layer",
            "Cloud SQL PostgreSQL + pgvector",
            "Cloud Logging",
            "Secret Manager",
        ],
        "demoFlow": [
            "book analysis",
            "reader",
            "role-based administration",
            "publisher catalog console",
            "superadmin operations console",
            "canon character chat",
            "fiction branch mode",
            "english primary language",
            "spanish secondary language",
            "character chat",
            "scene orchestration",
            "voice narration plan",
            "publisher insights",
            "Track 2 evaluation",
        ],
        "runtime": {
            "geminiMode": gemini.mode,
            "geminiModel": gemini.model,
            "vertexai": gemini.vertexai,
            "configured": gemini.configured,
        },
    }


@app.get("/api/v1/admin/roles")
def admin_roles() -> dict[str, object]:
    return {
        "accessModel": "demo-role-console",
        "productionTarget": "Cloud Identity / Identity Platform with tenant-scoped RBAC",
        "roles": [
            {
                "role": "reader",
                "label": "Reader",
                "description": (
                    "Reads available books, chats with characters, explores scenes, "
                    "and saves progress."
                ),
                "permissions": [
                    "read_public_books",
                    "chat_with_characters",
                    "create_fiction_branches",
                    "listen_to_narration",
                ],
            },
            {
                "role": "author",
                "label": "Author",
                "description": (
                    "Uploads owned or public-domain books and reviews generated analysis "
                    "before publishing."
                ),
                "permissions": [
                    "upload_owned_books",
                    "review_analysis",
                    "test_character_agents",
                    "submit_for_publication",
                ],
            },
            {
                "role": "publisher_admin",
                "label": "Publisher Admin",
                "description": (
                    "Manages a publisher catalog, availability, engagement metrics, "
                    "and title-level quality."
                ),
                "permissions": [
                    "manage_catalog",
                    "publish_titles",
                    "view_engagement_metrics",
                    "review_agent_quality",
                    "export_catalog_insights",
                ],
            },
            {
                "role": "super_admin",
                "label": "Super Admin",
                "description": (
                    "Operates the whole platform, tenants, users, costs, agent health, "
                    "and compliance state."
                ),
                "permissions": [
                    "manage_tenants",
                    "manage_users",
                    "audit_books",
                    "monitor_agent_runtime",
                    "review_costs",
                    "configure_marketplace_listing",
                ],
            },
        ],
    }


@app.get("/api/v1/admin/marketplace")
def admin_marketplace() -> dict[str, object]:
    gemini = GeminiTool().status
    storage = StorageRepository()
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, [DEMO_BOOK_TEXT]).output
    evaluation = run_demo_evaluation()
    return {
        "listingReadiness": {
            "track": "Track 3 - Google Cloud Marketplace & Gemini Enterprise",
            "businessModel": (
                "B2B SaaS for publishers, authors, education platforms, and reading apps"
            ),
            "deployment": "Cloud Run public demo with managed service account",
            "intelligence": gemini.model,
            "retrieval": "Cloud SQL PostgreSQL + pgvector"
            if storage.status.pgvector_ready
            else "in-memory fallback",
            "identityPlan": "Cloud Identity / Identity Platform tenant RBAC",
            "marketplaceStatus": "demo-ready, listing-contract-ready",
        },
        "tenant": {
            "tenant_id": "publisher-demo-pronexus",
            "name": "Pronexus Publisher Demo",
            "plan": "Marketplace Pilot",
            "region": "EMEA",
            "billing": "challenge-credit-backed demo project",
        },
        "catalog": [
            {
                "book_id": DEMO_BOOK_ID,
                "title": DEMO_BOOK_TITLE,
                "rights": "public-domain demo title",
                "owner_role": "publisher_admin",
                "availability": "published",
                "characters": len(analysis.characters),
                "scenes": len(analysis.scenes),
                "languages": ["en", "es"],
                "agent_modes": ["CANON", "FICTION"],
                "quality_score": round(evaluation.optimized_passed / evaluation.total_cases, 2),
            }
        ],
        "operations": {
            "users": 4,
            "tenants": 1,
            "publishedBooks": 1,
            "pendingBooks": 0,
            "agentHealth": "healthy",
            "optimizedEvaluationCases": evaluation.optimized_passed,
            "totalEvaluationCases": evaluation.total_cases,
        },
    }


@app.get("/api/v1/challenge/storage")
def challenge_storage() -> dict[str, object]:
    storage = StorageRepository()
    status = storage.status
    embedding = storage.embedding_provider.status
    return {
        "status": status.__dict__,
        "schema": storage.schema_sql(),
        "target": "Cloud SQL PostgreSQL + pgvector",
        "embedding": embedding.__dict__,
        "runtimeBehavior": "Falls back to in-memory demo retrieval when DATABASE_URL is unset.",
    }


@app.get("/api/v1/challenge/storage/demo-seed")
def challenge_storage_demo_seed() -> dict[str, object]:
    storage = StorageRepository()
    status = storage.status
    if not status.configured or not status.pgvector_ready:
        return {
            "seeded": False,
            "sections": 0,
            "reason": status.detail,
        }
    sections = storage.seed_demo_book(DEMO_BOOK_ID, DEMO_BOOK_TITLE)
    return {
        "seeded": True,
        "bookId": DEMO_BOOK_ID,
        "sections": sections,
        "embedding": storage.embedding_provider.status.__dict__,
    }


@app.get("/api/v1/demo/book")
def demo_book() -> dict[str, object]:
    ingestion = BookIngestionAgent().run(DEMO_BOOK_ID, DEMO_BOOK_TEXT)
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, ingestion.output)
    return {
        "bookId": DEMO_BOOK_ID,
        "title": analysis.output.title,
        "analysis": analysis.output.model_dump(),
        "traces": [trace.model_dump() for trace in ingestion.traces + analysis.traces],
    }


@app.post("/api/v1/demo/chat/character")
def demo_character_chat(request: CharacterChatRequest) -> dict[str, object]:
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, [DEMO_BOOK_TEXT]).output
    character = next(
        (item for item in analysis.characters if item.character_id == request.character_id),
        analysis.characters[0],
    )
    retrieval = RetrievalAgent().run(
        DEMO_BOOK_ID,
        request.question,
        settings.max_retrieved_sections,
    )
    reply = CharacterAgent().run(
        character,
        request.question,
        retrieval.output,
        request.mode,
        request.language,
    )
    consistency = NarrativeConsistencyAgent().run(reply.output)
    fiction_branch = None
    fiction_traces = []
    if request.mode == ConversationMode.FICTION:
        fiction = FictionBranchAgent().run(
            DEMO_BOOK_ID,
            character,
            request.question,
            retrieval.output,
            reply.output.response,
        )
        fiction_branch = fiction.output.model_dump()
        fiction_traces = fiction.traces
    return {
        "mode": request.mode,
        "language": request.language,
        "reply": reply.output.model_dump(),
        "fictionBranch": fiction_branch,
        "consistency": consistency.output,
        "contexts": [context.model_dump() for context in retrieval.output],
        "traces": [
            trace.model_dump()
            for trace in retrieval.traces + reply.traces + fiction_traces + consistency.traces
        ],
    }


@app.post("/api/v1/demo/chat/scene")
def demo_scene_chat(request: SceneChatRequest) -> dict[str, object]:
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, [DEMO_BOOK_TEXT]).output
    retrieval = RetrievalAgent().run(
        DEMO_BOOK_ID,
        request.prompt,
        settings.max_retrieved_sections,
    )
    scene = SceneOrchestratorAgent().run(analysis.characters, request.prompt, retrieval.output)
    return {
        "scene": [reply.model_dump() for reply in scene.output],
        "contexts": [context.model_dump() for context in retrieval.output],
        "traces": [trace.model_dump() for trace in retrieval.traces + scene.traces],
    }


@app.post("/api/v1/demo/narration")
def demo_narration(request: NarrationRequest) -> dict[str, object]:
    narration = VoiceNarrationAgent().run(request.scene_text)
    return {
        "narration": narration.output.model_dump(),
        "traces": [trace.model_dump() for trace in narration.traces],
    }


@app.get("/api/v1/demo/publisher")
def demo_publisher() -> dict[str, object]:
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, [DEMO_BOOK_TEXT]).output
    evaluation = run_demo_evaluation()
    summary = {
        "totalCases": evaluation.total_cases,
        "baselinePassed": evaluation.baseline_passed,
        "optimizedPassed": evaluation.optimized_passed,
        "improvementRate": evaluation.improvement_rate,
    }
    report = PublisherInsightsAgent().run(analysis, summary)
    return {
        "report": report.output.model_dump(),
        "evaluationSummary": summary,
        "traces": [trace.model_dump() for trace in report.traces],
    }


@app.get("/api/v1/demo/evaluation")
def demo_evaluation() -> dict[str, object]:
    report = run_demo_evaluation()
    return {
        "track": "Track 3 primary, Track 2 quality evidence",
        "summary": {
            "totalCases": report.total_cases,
            "baselinePassed": report.baseline_passed,
            "optimizedPassed": report.optimized_passed,
            "improvementRate": report.improvement_rate,
        },
        "cases": [result.model_dump() for result in report.cases],
    }


def run() -> None:
    uvicorn.run(
        "storms_agents.api.main:app",
        host=settings.api_host,
        port=settings.api_port,
        reload=settings.app_env == "local",
    )


if __name__ == "__main__":
    run()
