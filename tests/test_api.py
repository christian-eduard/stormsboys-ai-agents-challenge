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


def test_static_asset() -> None:
    client = TestClient(app)
    response = client.get("/static/app.js")
    assert response.status_code == 200
    assert "runEvaluation" in response.text


def test_challenge_readiness() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/challenge/readiness")
    assert response.status_code == 200
    body = response.json()
    assert body["track"] == "Track 3 - Refactor for Google Cloud Marketplace & Gemini Enterprise"
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
    assert "canon character chat" in body["demoFlow"]


def test_demo_book() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/demo/book")
    assert response.status_code == 200
    body = response.json()
    assert body["bookId"] == "don-quijote"
    assert body["title"] == "Don Quijote de la Mancha"
    assert len(body["analysis"]["characters"]) == 3
    assert body["traces"]


def test_demo_character_chat() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
            "question": "Why do you attack the windmills?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "CANON"
    assert body["reply"]["character_id"] == "don_quijote"
    assert body["reply"]["mode"] == "CANON"
    assert body["fictionBranch"] is None
    assert body["consistency"]["checks"]["has_grounding"] is True
    assert body["traces"]


def test_demo_character_chat_fiction_branch() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "FICTION",
            "question": "What if Sancho convinces you the giants are machines?",
        },
    )
    assert response.status_code == 200
    body = response.json()
    assert body["mode"] == "FICTION"
    assert body["reply"]["mode"] == "FICTION"
    assert body["fictionBranch"]["book_id"] == "don-quijote"
    assert body["fictionBranch"]["character_id"] == "don_quijote"
    assert body["consistency"]["checks"]["separated_from_canon"] is True
    assert any(trace["agent_name"] == "FictionBranchAgent" for trace in body["traces"])


def test_demo_character_chat_canon_rejects_future() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={
            "character_id": "don_quijote",
            "mode": "CANON",
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
    response = client.get("/api/v1/demo/publisher")
    assert response.status_code == 200
    body = response.json()
    assert body["report"]["quality_score"] == 1
    assert len(body["report"]["insights"]) == 3
    assert body["traces"][0]["agent_name"] == "PublisherInsightsAgent"


def test_demo_evaluation() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/demo/evaluation")
    assert response.status_code == 200
    body = response.json()
    assert body["track"] == "Track 3 primary, Track 2 quality evidence"
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
