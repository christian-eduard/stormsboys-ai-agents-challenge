from importlib.resources import files

import uvicorn
from fastapi import FastAPI, Header, HTTPException, Query
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
from storms_agents.fiction_history import FictionBranchStore
from storms_agents.memory import ConversationMemoryStore
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
    session_id: str = "judge-demo-session"
    question: str


class DemoLoginRequest(BaseModel):
    user_id: str


class SceneChatRequest(BaseModel):
    prompt: str


class NarrationRequest(BaseModel):
    scene_text: str = (
        "Don Quijote charges at the windmills while Sancho warns him from the road."
    )


def _role_permissions() -> dict[str, list[str]]:
    return {
        "reader": [
            "read_public_books",
            "chat_with_characters",
            "create_fiction_branches",
            "listen_to_narration",
        ],
        "author": [
            "upload_owned_books",
            "review_analysis",
            "test_character_agents",
            "submit_for_publication",
        ],
        "publisher_admin": [
            "manage_catalog",
            "publish_titles",
            "view_engagement_metrics",
            "review_agent_quality",
            "export_catalog_insights",
        ],
        "super_admin": [
            "manage_tenants",
            "manage_users",
            "audit_books",
            "monitor_agent_runtime",
            "review_costs",
            "configure_marketplace_listing",
        ],
        "judge_access": [
            "read_public_books",
            "chat_with_characters",
            "create_fiction_branches",
            "listen_to_narration",
            "manage_catalog",
            "view_engagement_metrics",
            "review_agent_quality",
            "manage_tenants",
            "monitor_agent_runtime",
            "configure_marketplace_listing",
        ],
    }


def _demo_users() -> list[dict[str, object]]:
    permissions = _role_permissions()
    return [
        {
            "user_id": "reader-demo",
            "name": "Reader Demo",
            "email": "reader@stormsdemo.dev",
            "role": "reader",
            "tenant_id": "public-readers",
            "permissions": permissions["reader"],
        },
        {
            "user_id": "author-demo",
            "name": "Author Demo",
            "email": "author@stormsdemo.dev",
            "role": "author",
            "tenant_id": "independent-authors",
            "permissions": permissions["author"],
        },
        {
            "user_id": "publisher-demo",
            "name": "Publisher Admin Demo",
            "email": "publisher@pronexus.demo",
            "role": "publisher_admin",
            "tenant_id": "publisher-demo-pronexus",
            "permissions": permissions["publisher_admin"],
        },
        {
            "user_id": "superadmin-demo",
            "name": "Super Admin Demo",
            "email": "admin@stormsdemo.dev",
            "role": "super_admin",
            "tenant_id": "platform",
            "permissions": permissions["super_admin"],
        },
        {
            "user_id": "judge-demo",
            "name": "Judge Access",
            "email": "judge@stormsdemo.dev",
            "role": "judge_access",
            "tenant_id": "challenge-review",
            "permissions": permissions["judge_access"],
        },
    ]


def _role_labels() -> dict[str, str]:
    return {
        "reader": "Reader",
        "author": "Author",
        "publisher_admin": "Publisher Admin",
        "super_admin": "Super Admin",
        "judge_access": "Judge Access",
    }


def _token_user(authorization: str | None) -> dict[str, object]:
    if not authorization or not authorization.startswith("Bearer demo-token:"):
        raise HTTPException(status_code=401, detail="Demo login token required.")
    user_id = authorization.removeprefix("Bearer demo-token:")
    user = next((item for item in _demo_users() if item["user_id"] == user_id), None)
    if user is None:
        raise HTTPException(status_code=401, detail="Invalid demo login token.")
    return user


def _require_any_permission(
    authorization: str | None,
    permissions: set[str],
) -> dict[str, object]:
    user = _token_user(authorization)
    user_permissions = set(user["permissions"])
    if user_permissions.isdisjoint(permissions):
        raise HTTPException(status_code=403, detail="Role does not have access.")
    return user


@app.get("/", response_class=HTMLResponse)
def web_demo() -> str:
    return WEB_DIR.joinpath("index.html").read_text(encoding="utf-8")


def _agent_card() -> dict[str, object]:
    return {
        "name": "Stormsboys Literary Agent Platform",
        "description": (
            "Google Cloud-native literary agent system for publishers, authors, readers, "
            "and enterprise catalog operators."
        ),
        "version": __version__,
        "provider": {"organization": "Pronexus / Stormsboys", "region": "EMEA"},
        "url": "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app",
        "protocols": ["A2A-ready agent card", "HTTP JSON"],
        "track": "Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise",
        "authentication": {
            "demo": "Public reader endpoints plus demo bearer tokens for protected admin views.",
            "productionTarget": "Identity Platform or Cloud Identity tenant RBAC.",
        },
        "capabilities": [
            {
                "id": "analyze_book",
                "name": "Analyze owned or public-domain books",
                "endpoint": "/api/v1/demo/book",
            },
            {
                "id": "chat_as_character",
                "name": "Canon-safe character conversation with psychology and memory",
                "endpoint": "/api/v1/demo/chat/character",
            },
            {
                "id": "create_fiction_branch",
                "name": "Alternative fiction branch separated from canon",
                "endpoint": "/api/v1/demo/chat/character",
            },
            {
                "id": "publisher_insights",
                "name": "Publisher catalog and engagement insights",
                "endpoint": "/api/v1/demo/publisher",
            },
            {
                "id": "marketplace_admin",
                "name": "Tenant roles, readiness, and operations console",
                "endpoint": "/api/v1/admin/marketplace",
            },
        ],
        "googleCloud": {
            "runtime": "Cloud Run",
            "intelligence": "Gemini / Vertex AI target",
            "memoryTarget": "Cloud SQL PostgreSQL + pgvector",
            "observability": "Cloud Logging and structured traces",
        },
    }


@app.get("/.well-known/agent-card.json")
def well_known_agent_card() -> dict[str, object]:
    return _agent_card()


@app.get("/a2a/agent-card.json")
def a2a_agent_card() -> dict[str, object]:
    return _agent_card()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "version": __version__,
        "environment": settings.app_env,
    }


@app.get("/api/v1/auth/demo-users")
def auth_demo_users() -> dict[str, object]:
    return {
        "authModel": "demo-login",
        "productionTarget": "Identity Platform or Cloud Identity with tenant RBAC",
        "users": _demo_users(),
    }


@app.post("/api/v1/auth/demo-login")
def auth_demo_login(request: DemoLoginRequest) -> dict[str, object]:
    user = next((item for item in _demo_users() if item["user_id"] == request.user_id), None)
    if user is None:
        user = _demo_users()[0]
    return {
        "token": f"demo-token:{user['user_id']}",
        "user": user,
        "access": {
            "canRead": "read_public_books" in user["permissions"],
            "canChat": "chat_with_characters" in user["permissions"],
            "canPublish": "manage_catalog" in user["permissions"],
            "canOperatePlatform": "manage_tenants" in user["permissions"],
        },
    }


@app.get("/api/v1/challenge/readiness")
def challenge_readiness() -> dict[str, object]:
    gemini = GeminiTool().status
    return {
        "track": "Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise",
        "trackEvidence": "Track 2 evaluation remains available for quality evidence.",
        "projectIsolation": "new-project-no-cross-project-code",
        "agentLayer": "adk-first-python",
        "memory": "Cloud SQL persisted when DATABASE_URL is configured, local fallback otherwise",
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
            "demo login and role switching",
            "judge access tour",
            "author manuscript workflow",
            "book analysis",
            "reader",
            "role-based administration",
            "publisher catalog console",
            "superadmin operations console",
            "canon character chat",
            "fiction branch mode",
            "persisted conversation memory",
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


@app.get("/api/v1/challenge/submission")
def challenge_submission() -> dict[str, object]:
    return {
        "track": "Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise",
        "region": "EMEA",
        "deadline": "2026-06-05 17:00 PT",
        "status": "public-demo-ready",
        "publicDemo": "https://stormsboys-agents-api-5mpmuf566a-uc.a.run.app",
        "repository": "https://github.com/christian-eduard/stormsboys-ai-agents-challenge",
        "judgingCriteria": [
            {
                "name": "Technical Implementation",
                "weight": "30%",
                "evidence": (
                    "Cloud Run, Gemini/Vertex, ADK-first agents, Cloud SQL pgvector, "
                    "protected APIs."
                ),
            },
            {
                "name": "Business Case",
                "weight": "30%",
                "evidence": (
                    "B2B catalog product for publishers, authors, education, and reading apps."
                ),
            },
            {
                "name": "Innovation and Creativity",
                "weight": "20%",
                "evidence": (
                    "Books become governed character, scene, fiction branch, voice, "
                    "and analytics agents."
                ),
            },
            {
                "name": "Demo and Presentation",
                "weight": "20%",
                "evidence": (
                    "Judge Access role, guided dashboard, bilingual demo, runtime proof, "
                    "and smoke-tested URL."
                ),
            },
        ],
        "deliverables": [
            {"name": "Public repository", "status": "ready"},
            {"name": "English description", "status": "ready"},
            {"name": "Architecture diagram", "status": "ready"},
            {"name": "Functional judge demo", "status": "ready"},
            {"name": "A2A agent card", "status": "ready"},
            {"name": "1-2 minute English video", "status": "planned-final-step"},
        ],
        "recommendedJudgeAccount": {
            "user_id": "judge-demo",
            "name": "Judge Access",
            "role": "judge_access",
        },
    }


@app.get("/api/v1/admin/roles")
def admin_roles() -> dict[str, object]:
    permissions = _role_permissions()
    labels = _role_labels()
    return {
        "accessModel": "demo-role-console",
        "productionTarget": "Cloud Identity / Identity Platform with tenant-scoped RBAC",
        "roles": [
            {
                "role": "reader",
                "label": labels["reader"],
                "description": (
                    "Reads available books, chats with characters, explores scenes, "
                    "and saves progress."
                ),
                "permissions": permissions["reader"],
            },
            {
                "role": "author",
                "label": labels["author"],
                "description": (
                    "Uploads owned or public-domain books and reviews generated analysis "
                    "before publishing."
                ),
                "permissions": permissions["author"],
            },
            {
                "role": "publisher_admin",
                "label": labels["publisher_admin"],
                "description": (
                    "Manages a publisher catalog, availability, engagement metrics, "
                    "and title-level quality."
                ),
                "permissions": permissions["publisher_admin"],
            },
            {
                "role": "super_admin",
                "label": labels["super_admin"],
                "description": (
                    "Operates the whole platform, tenants, users, costs, agent health, "
                    "and compliance state."
                ),
                "permissions": permissions["super_admin"],
            },
            {
                "role": "judge_access",
                "label": labels["judge_access"],
                "description": (
                    "Reviews the complete challenge flow with access to reader, publisher, "
                    "admin, runtime, and evaluation views."
                ),
                "permissions": permissions["judge_access"],
            },
        ],
    }


@app.get("/api/v1/admin/marketplace")
def admin_marketplace(authorization: str | None = Header(default=None)) -> dict[str, object]:
    user = _require_any_permission(authorization, {"manage_catalog", "manage_tenants"})
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
        "currentUser": user,
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
            "users": len(_demo_users()),
            "tenants": 1,
            "publishedBooks": 1,
            "pendingBooks": 0,
            "agentHealth": "healthy",
            "optimizedEvaluationCases": evaluation.optimized_passed,
            "totalEvaluationCases": evaluation.total_cases,
        },
    }


@app.get("/api/v1/demo/author-workflow")
def demo_author_workflow(authorization: str | None = Header(default=None)) -> dict[str, object]:
    user = _require_any_permission(
        authorization,
        {"upload_owned_books", "review_analysis", "manage_tenants"},
    )
    ingestion = BookIngestionAgent().run(DEMO_BOOK_ID, DEMO_BOOK_TEXT)
    analysis = LiteraryAnalysisAgent().run(DEMO_BOOK_TITLE, ingestion.output)
    evaluation = run_demo_evaluation()
    return {
        "currentUser": user,
        "manuscript": {
            "book_id": DEMO_BOOK_ID,
            "title": DEMO_BOOK_TITLE,
            "rights": "public-domain demo title",
            "languagePolicy": ["en", "es"],
            "status": "ready_for_publisher_review",
        },
        "analysisSummary": {
            "characters": len(analysis.output.characters),
            "places": len(analysis.output.places),
            "scenes": len(analysis.output.scenes),
            "canonMode": "grounded in retrieved book sections",
            "fictionMode": "separate branch with explicit non-canon state",
        },
        "generatedAgents": [
            {
                "character_id": character.character_id,
                "name": character.name,
                "personality": character.personality,
                "goals": character.goals,
                "constraints": character.constraints,
            }
            for character in analysis.output.characters
        ],
        "approvalChecklist": [
            {
                "item": "ownership_or_public_domain",
                "status": "passed",
                "evidence": "Don Quijote public-domain demo title",
            },
            {
                "item": "character_grounding",
                "status": "passed",
                "evidence": (
                    f"{evaluation.optimized_passed}/{evaluation.total_cases} optimized cases"
                ),
            },
            {
                "item": "bilingual_reader_access",
                "status": "passed",
                "evidence": "English primary, Spanish secondary",
            },
        ],
        "traces": [trace.model_dump() for trace in ingestion.traces + analysis.traces],
    }


@app.get("/api/v1/admin/operations")
def admin_operations(authorization: str | None = Header(default=None)) -> dict[str, object]:
    user = _require_any_permission(authorization, {"manage_tenants"})
    gemini = GeminiTool().status
    storage = StorageRepository()
    evaluation = run_demo_evaluation()
    return {
        "currentUser": user,
        "runtime": {
            "cloudRunRevision": "managed by Cloud Run",
            "serviceAccount": "stormsboys-agents-runtime",
            "gemini": gemini.model if gemini.configured else "fallback",
            "retrieval": "pgvector" if storage.status.pgvector_ready else "in-memory fallback",
        },
        "tenantOperations": {
            "tenants": 1,
            "users": len(_demo_users()),
            "publisherCatalogs": 1,
            "publishedBooks": 1,
            "pendingReviews": 0,
        },
        "qualityGate": {
            "optimizedCases": evaluation.optimized_passed,
            "totalCases": evaluation.total_cases,
            "status": (
                "passed" if evaluation.optimized_passed == evaluation.total_cases else "review"
            ),
        },
        "governance": [
            "demo tokens only for judging",
            "production target is Identity Platform tenant RBAC",
            "Secret Manager supplies DATABASE_URL",
            "no local credential files required by runtime",
        ],
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
        "memoryTarget": "conversation_memory_events",
        "fictionTarget": "fiction_branches",
        "embedding": embedding.__dict__,
        "runtimeBehavior": (
            "Falls back to in-memory retrieval and memory when DATABASE_URL is unset."
        ),
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
    memory_store = ConversationMemoryStore()
    memory_before = memory_store.snapshot(
        request.session_id,
        character.character_id,
        request.mode,
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
        memory_before,
    )
    memory_after = memory_store.record(
        request.session_id,
        character.character_id,
        request.mode,
        request.question,
        reply.output.response,
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
        saved_branch = FictionBranchStore().record(request.session_id, fiction.output)
        fiction_branch = saved_branch.model_dump()
        fiction_traces = fiction.traces
    return {
        "mode": request.mode,
        "language": request.language,
        "sessionId": request.session_id,
        "characterProfile": character.model_dump(),
        "memory": memory_after.model_dump(),
        "reply": reply.output.model_dump(),
        "fictionBranch": fiction_branch,
        "consistency": consistency.output,
        "contexts": [context.model_dump() for context in retrieval.output],
        "traces": [
            trace.model_dump()
            for trace in retrieval.traces + reply.traces + fiction_traces + consistency.traces
        ],
    }


@app.get("/api/v1/demo/chat/memory")
def demo_chat_memory(
    session_id: str = "judge-demo-session",
    character_id: str = "don_quijote",
    mode: ConversationMode = ConversationMode.CANON,
    limit: int = Query(default=5, ge=1, le=20),
) -> dict[str, object]:
    return ConversationMemoryStore().history(
        session_id=session_id,
        character_id=character_id,
        mode=mode,
        limit=limit,
    )


@app.get("/api/v1/demo/fiction/branches")
def demo_fiction_branches(
    session_id: str = "judge-demo-session",
    character_id: str | None = None,
    limit: int = Query(default=5, ge=1, le=20),
) -> dict[str, object]:
    return FictionBranchStore().list(
        session_id=session_id,
        character_id=character_id,
        limit=limit,
    )


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
def demo_publisher(authorization: str | None = Header(default=None)) -> dict[str, object]:
    user = _require_any_permission(authorization, {"manage_catalog", "manage_tenants"})
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
        "currentUser": user,
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
