from fastapi.testclient import TestClient

from storms_agents.api.main import app


def test_health() -> None:
    client = TestClient(app)
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "ok"


def test_web_demo() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200
    assert "Multi-agent literary intelligence" in response.text
    assert "Marketplace Admin" in response.text
    assert "Demo access" in response.text
    assert "Choose a demo account" in response.text
    assert "Submission readiness" in response.text
    assert "cleanupSessionInput" in response.text
    assert 'data-view="dashboard"' in response.text
    assert 'data-view="author"' in response.text


def test_static_asset() -> None:
    client = TestClient(app)
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "runEvaluation" in response.text
    assert "demo-login" in response.text
    assert "judge_access" in response.text
    assert "cleanupDemoSession" in response.text
    assert "/api/v1/admin/demo-sessions/" in response.text
    assert "fiction-detail" in response.text
    assert "/api/v1/demo/fiction/branches?" in response.text


def test_challenge_readiness() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/challenge/readiness")
    assert response.status_code == 200
    body = response.json()
    assert body["track"] == "All tracks - Build, Optimize, and Refactor"
    assert len(body["trackPortfolio"]) == 3
    assert body["projectIsolation"] == "new-project-no-cross-project-code"
    assert body["gemini"]["mode"] in {"gemini", "demo-fallback"}


def test_challenge_capabilities() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/challenge/capabilities")
    assert response.status_code == 200
    body = response.json()
    assert body["judgingCriteria"]["technicalImplementation"] == "30%"
    assert "Cloud Run" in body["googleCloudTarget"]
    assert "voice narration plan" in body["demoFlow"]
    assert "demo login and role switching" in body["demoFlow"]
    assert "judge access tour" in body["demoFlow"]
    assert "author manuscript workflow" in body["demoFlow"]
    assert "role-based administration" in body["demoFlow"]
    assert "publisher catalog console" in body["demoFlow"]
    assert "superadmin operations console" in body["demoFlow"]
    assert "canon character chat" in body["demoFlow"]
    assert "english primary language" in body["demoFlow"]
    assert "spanish secondary language" in body["demoFlow"]


def test_challenge_submission() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/challenge/submission")
    assert response.status_code == 200
    body = response.json()
    assert body["track"] == "All tracks - Build, Optimize, and Refactor"
    assert {item["track"] for item in body["trackPortfolio"]} == {
        "Track 1 - Build",
        "Track 2 - Optimize",
        "Track 3 - Refactor",
    }
    assert body["status"] == "public-demo-ready"
    assert body["recommendedJudgeAccount"]["user_id"] == "judge-demo"
    assert len(body["judgingCriteria"]) == 4
    assert any(item["name"] == "Functional judge demo" for item in body["deliverables"])
    assert any(item["name"] == "A2A agent card" for item in body["deliverables"])


def test_agent_card_is_public_track3_evidence() -> None:
    client = TestClient(app)
    response = client.get("/.well-known/agent-card.json")
    assert response.status_code == 200
    body = response.json()
    assert body["track"] == "All tracks - Build, Optimize, and Refactor"
    assert len(body["trackPortfolio"]) == 3
    capabilities = {item["id"] for item in body["capabilities"]}
    assert {"analyze_book", "chat_as_character", "create_fiction_branch"} <= capabilities
    assert body["googleCloud"]["runtime"] == "Cloud Run"


def test_demo_book() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/demo/book")
    assert response.status_code == 200
    body = response.json()
    assert body["bookId"] == "don-quijote"
    assert body["title"] == "Don Quijote de la Mancha"
    assert len(body["analysis"]["characters"]) == 3
    don_quijote = body["analysis"]["characters"][0]
    assert don_quijote["speech_style"]
    assert "ocean" in don_quijote["psychological_profile"]
    assert don_quijote["desires"]
    assert don_quijote["fears"]
    assert body["traces"]


def test_auth_demo_users() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/auth/demo-users")
    assert response.status_code == 200
    body = response.json()
    users = {user["user_id"]: user for user in body["users"]}
    assert {
        "reader-demo",
        "author-demo",
        "publisher-demo",
        "superadmin-demo",
        "judge-demo",
    } <= set(users)
    assert users["publisher-demo"]["role"] == "publisher_admin"
    assert users["judge-demo"]["role"] == "judge_access"
    assert "manage_catalog" in users["publisher-demo"]["permissions"]
    assert "manage_tenants" in users["judge-demo"]["permissions"]


def test_auth_demo_login() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/auth/demo-login", json={"user_id": "superadmin-demo"})
    assert response.status_code == 200
    body = response.json()
    assert body["token"] == "demo-token:superadmin-demo"
    assert body["user"]["role"] == "super_admin"
    assert body["access"]["canOperatePlatform"] is True


def test_author_can_upload_manuscript_and_chat_with_generated_character() -> None:
    client = TestClient(app)
    sample = (
        "Mara crossed the Silent Bridge at dawn. Mara carried a small atlas and a "
        "promise to return the lost bell to the city. Tomas waited near the archive, "
        "afraid that Mara would discover the council's secret. The city listened as "
        "the river moved below them. Mara wanted truth, Tomas wanted safety, and both "
        "knew the bridge would decide who could be trusted. "
    )

    upload = client.post(
        "/api/v1/books/upload",
        headers={"authorization": "Bearer demo-token:author-demo"},
        data={
            "title": "The Silent Bridge",
            "author": "Challenge Author",
            "rights": "owned_or_public_domain",
            "language": "en",
        },
        files={"file": ("silent-bridge.txt", sample, "text/plain")},
    )

    assert upload.status_code == 200
    body = upload.json()
    assert body["book"]["book_id"].startswith("upload-the-silent-bridge")
    assert body["book"]["sections"] >= 1
    assert body["analysis"]["title"] == "The Silent Bridge"
    assert body["analysis"]["characters"]
    first_character = body["analysis"]["characters"][0]["character_id"]

    catalog = client.get(
        "/api/v1/books/catalog",
        headers={"authorization": "Bearer demo-token:author-demo"},
    )
    assert catalog.status_code == 200
    assert any(
        item["book_id"] == body["book"]["book_id"] for item in catalog.json()["uploadedBooks"]
    )

    chat = client.post(
        "/api/v1/demo/chat/character",
        json={
            "book_id": body["book"]["book_id"],
            "character_id": first_character,
            "mode": "CANON",
            "language": "en",
            "session_id": "uploaded-chat-test",
            "question": "What do you want near the bridge?",
        },
    )
    assert chat.status_code == 200
    chat_body = chat.json()
    assert chat_body["bookId"] == body["book"]["book_id"]
    assert chat_body["characterProfile"]["character_id"] == first_character
    assert chat_body["reply"]["response"]


def test_judge_demo_login_has_full_review_access() -> None:
    client = TestClient(app)
    response = client.post("/api/v1/auth/demo-login", json={"user_id": "judge-demo"})
    assert response.status_code == 200
    body = response.json()
    assert body["token"] == "demo-token:judge-demo"
    assert body["user"]["role"] == "judge_access"
    assert body["access"]["canOperatePlatform"] is True
    assert body["access"]["canPublish"] is True


def test_protected_marketplace_requires_demo_token() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/admin/marketplace")
    assert response.status_code == 401


def test_reader_cannot_access_marketplace_admin() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/admin/marketplace",
        headers={"authorization": "Bearer demo-token:reader-demo"},
    )
    assert response.status_code == 403


def test_admin_roles() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/admin/roles")
    assert response.status_code == 200
    body = response.json()
    roles = {role["role"]: role for role in body["roles"]}
    assert {"reader", "author", "publisher_admin", "super_admin", "judge_access"} <= set(roles)
    assert "manage_catalog" in roles["publisher_admin"]["permissions"]
    assert "manage_tenants" in roles["super_admin"]["permissions"]
    assert "monitor_agent_runtime" in roles["judge_access"]["permissions"]


def test_admin_marketplace() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/admin/marketplace",
        headers={"authorization": "Bearer demo-token:publisher-demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["listingReadiness"]["track"] == "Track 1 + Track 2 + Track 3 challenge evidence"
    assert body["currentUser"]["role"] == "publisher_admin"
    assert body["tenant"]["plan"] == "Marketplace Pilot"
    assert body["catalog"][0]["book_id"] == "don-quijote"
    assert body["catalog"][0]["languages"] == ["en", "es"]
    assert body["operations"]["agentHealth"] == "healthy"
    assert body["operations"]["users"] == 5


def test_judge_can_access_marketplace_admin() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/admin/marketplace",
        headers={"authorization": "Bearer demo-token:judge-demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["currentUser"]["role"] == "judge_access"
    assert body["listingReadiness"]["marketplaceStatus"].startswith("demo-ready")


def test_demo_author_workflow_requires_author_access() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/demo/author-workflow",
        headers={"authorization": "Bearer demo-token:reader-demo"},
    )
    assert response.status_code == 403


def test_demo_author_workflow() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/demo/author-workflow",
        headers={"authorization": "Bearer demo-token:author-demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["currentUser"]["role"] == "author"
    assert body["manuscript"]["status"] == "ready_for_publisher_review"
    assert body["analysisSummary"]["characters"] == 3
    assert len(body["generatedAgents"]) == 3
    assert body["approvalChecklist"][0]["status"] == "passed"


def test_admin_operations_requires_superadmin_access() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/admin/operations",
        headers={"authorization": "Bearer demo-token:publisher-demo"},
    )
    assert response.status_code == 403


def test_admin_operations() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/admin/operations",
        headers={"authorization": "Bearer demo-token:superadmin-demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["currentUser"]["role"] == "super_admin"
    assert body["tenantOperations"]["users"] == 5
    assert body["qualityGate"]["totalCases"] == 12
    assert "Secret Manager supplies DATABASE_URL" in body["governance"]


def test_demo_character_chat() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "en",
            "session_id": "test-canon-001",
            "question": "Why do you attack the windmills?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "CANON"
    assert body["language"] == "en"
    assert body["reply"]["character_id"] == "don_quijote"
    assert body["reply"]["mode"] == "CANON"
    assert body["reply"]["language"] == "en"
    assert body["characterProfile"]["psychological_profile"]["ocean"]
    assert body["reply"]["profile_signals"]
    assert body["memory"]["turn_count"] == 1
    assert body["memory"]["mode"] == "CANON"
    assert body["fictionBranch"] is None
    assert body["consistency"]["checks"]["has_grounding"] is True
    assert body["traces"]


def test_demo_character_chat_spanish_language() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "es",
            "session_id": "test-es-001",
            "question": "Por que atacas los molinos?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["language"] == "es"
    assert body["reply"]["language"] == "es"
    assert body["reply"]["response"].startswith("Soy Don Quijote")
    assert body["fictionBranch"] is None
    assert body["contexts"]
    assert body["consistency"]["checks"]["has_grounding"] is True


def test_demo_character_chat_learns_reader_preferences() -> None:
    client = TestClient(app)
    session_id = "test-memory-psychology-001"
    first = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "en",
            "session_id": session_id,
            "question": "Explain your psychology when you see the windmills.",
        },
    )
    second = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "en",
            "session_id": session_id,
            "question": "Remember my interest in psychology and answer again.",
        },
    )
    assert first.status_code == 200
    assert second.status_code == 200
    body = second.json()
    assert body["memory"]["turn_count"] == 2
    assert (
        "reader asks for psychological motivation" in body["memory"]["learned_reader_preferences"]
    )
    assert "remember 1 turn" in body["reply"]["response"].lower()


def test_demo_character_memory_history() -> None:
    client = TestClient(app)
    session_id = "test-memory-history-001"
    client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "en",
            "session_id": session_id,
            "question": "Explain your psychology near the windmills.",
        },
    )
    response = client.get(
        "/api/v1/demo/chat/memory",
        params={
            "session_id": session_id,
            "character_id": "don_quijote",
            "mode": "CANON",
        },
    )

    assert response.status_code == 200
    body = response.json()
    assert body["provider"] in {"local-process-memory", "cloud-sql-postgresql"}
    assert body["events"]
    assert body["events"][0]["question"] == "Explain your psychology near the windmills."


def test_demo_character_chat_fiction_branch() -> None:
    client = TestClient(app)
    session_id = "test-fiction-001"
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "FICTION",
            "language": "en",
            "session_id": session_id,
            "question": "What if Sancho convinces you the giants are machines?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "FICTION"
    assert body["reply"]["mode"] == "FICTION"
    assert body["fictionBranch"]["book_id"] == "don-quijote"
    assert body["fictionBranch"]["character_id"] == "don_quijote"
    assert body["memory"]["mode"] == "FICTION"
    assert body["memory"]["fiction_memory"]
    assert body["consistency"]["checks"]["separated_from_canon"] is True
    assert any(trace["agent_name"] == "FictionBranchAgent" for trace in body["traces"])

    timeline = client.get(
        "/api/v1/demo/fiction/branches",
        params={
            "session_id": session_id,
            "character_id": "don_quijote",
        },
    )
    assert timeline.status_code == 200
    timeline_body = timeline.json()
    assert timeline_body["provider"] in {"local-process-memory", "cloud-sql-postgresql"}
    assert timeline_body["branches"]
    assert timeline_body["branches"][0]["branch_id"] == body["fictionBranch"]["branch_id"]

    detail = client.get(
        f"/api/v1/demo/fiction/branches/{body['fictionBranch']['branch_id']}",
        params={"session_id": session_id},
    )
    assert detail.status_code == 200
    detail_body = detail.json()
    assert detail_body["provider"] in {"local-process-memory", "cloud-sql-postgresql"}
    assert detail_body["branch"]["branch_id"] == body["fictionBranch"]["branch_id"]
    assert detail_body["branch"]["continuation"]
    assert detail_body["branch"]["canon_anchor_citations"]

    missing = client.get(
        "/api/v1/demo/fiction/branches/missing-branch",
        params={"session_id": session_id},
    )
    assert missing.status_code == 404


def test_admin_delete_demo_session_requires_superadmin_access() -> None:
    client = TestClient(app)
    response = client.delete(
        "/api/v1/admin/demo-sessions/test-session",
        headers={"authorization": "Bearer demo-token:reader-demo"},
    )

    assert response.status_code == 403


def test_admin_delete_demo_session_clears_memory_and_fiction_branch() -> None:
    client = TestClient(app)
    session_id = "test-cleanup-session-001"
    client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "en",
            "session_id": session_id,
            "question": "Explain your psychology near the windmills.",
        },
    )
    client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "FICTION",
            "language": "en",
            "session_id": session_id,
            "question": "What if Sancho convinces you the giants are machines?",
        },
    )

    response = client.delete(
        f"/api/v1/admin/demo-sessions/{session_id}",
        headers={"authorization": "Bearer demo-token:superadmin-demo"},
    )

    assert response.status_code == 200
    body = response.json()
    assert body["deleted"]["memory_events"] >= 1
    assert body["deleted"]["fiction_branches"] >= 1
    memory = client.get(
        "/api/v1/demo/chat/memory",
        params={
            "session_id": session_id,
            "character_id": "don_quijote",
            "mode": "CANON",
        },
    ).json()
    branches = client.get(
        "/api/v1/demo/fiction/branches",
        params={"session_id": session_id, "character_id": "don_quijote"},
    ).json()
    assert memory["events"] == []
    assert branches["branches"] == []


def test_demo_character_chat_canon_rejects_future() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "language": "en",
            "question": "Tell me what happens ten years after the ending.",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert "cannot speak as canon" in body["reply"]["response"]
    assert body["fictionBranch"] is None


def test_demo_scene_chat() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/scene",
        json={"prompt": "Discuss whether the windmills are giants or only windmills."},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["scene"]) == 3
    assert body["contexts"]


def test_demo_narration() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/narration",
        json={"scene_text": "Don Quijote charges at the windmills while Sancho warns him."},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["narration"]["ready_for_tts"] is True
    assert body["narration"]["ssml"].startswith("<speak>")
    assert body["traces"][0]["agent_name"] == "VoiceNarrationAgent"


def test_demo_publisher() -> None:
    client = TestClient(app)
    response = client.get(
        "/api/v1/demo/publisher",
        headers={"authorization": "Bearer demo-token:publisher-demo"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["currentUser"]["role"] == "publisher_admin"
    assert body["report"]["quality_score"] == 1
    assert len(body["report"]["insights"]) == 3
    assert body["traces"][0]["agent_name"] == "PublisherInsightsAgent"


def test_demo_evaluation() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/demo/evaluation")
    assert response.status_code == 200
    body = response.json()
    assert body["track"] == "Track 2 optimization evidence within the all-tracks submission"
    assert body["summary"]["totalCases"] == 12
    assert body["summary"]["optimizedPassed"] >= body["summary"]["baselinePassed"]
    assert len(body["cases"]) == 12
    assert {"category", "character_id", "expected_behavior"} <= set(body["cases"][0])


def test_challenge_storage() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/challenge/storage")
    assert response.status_code == 200
    body = response.json()
    assert body["target"] == "Cloud SQL PostgreSQL + pgvector"
    assert "schema" in body
    assert body["embedding"]["dimensions"] == 768


def test_challenge_storage_demo_seed_without_database() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/challenge/storage/demo-seed")
    assert response.status_code == 200
    body = response.json()
    assert body["seeded"] is False
