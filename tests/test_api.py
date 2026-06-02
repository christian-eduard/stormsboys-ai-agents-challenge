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
    assert body["track"] == "Track 2 - Optimize Existing Agents"
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


def test_demo_book() -> None:
    client = TestClient(app)
    response = client.get("/api/v1/demo/book")
    assert response.status_code == 200
    body = response.json()
    assert body["bookId"] == "demo-book"
    assert len(body["analysis"]["characters"]) == 3
    assert body["traces"]


def test_demo_character_chat() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/character",
        json={"character_id": "sarin", "question": "Why do you protect the lost names?"},
    )
    assert response.status_code == 200
    body = response.json()
    assert body["reply"]["character_id"] == "sarin"
    assert body["consistency"]["checks"]["has_grounding"] is True
    assert body["traces"]


def test_demo_scene_chat() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/chat/scene",
        json={"prompt": "Discuss who made the hardest choice at the Silent Gate."},
    )
    assert response.status_code == 200
    body = response.json()
    assert len(body["scene"]) == 3
    assert body["contexts"]


def test_demo_narration() -> None:
    client = TestClient(app)
    response = client.post(
        "/api/v1/demo/narration",
        json={"scene_text": "Mara reads the lost names at the Silent Gate."},
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
    assert body["track"] == "Track 2 - Optimize Existing Agents"
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
