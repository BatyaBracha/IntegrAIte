from fastapi.testclient import TestClient

from app.main import app
from app.models.bot import BotBlueprint, BotSnippetResponse

client = TestClient(app)


def test_health_check() -> None:
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_endpoint(monkeypatch) -> None:
    def fake_reply(session_id: str, prompt: str) -> str:  # noqa: ARG001 - signature must match
        return "mocked answer"

    monkeypatch.setattr("app.routers.ai_router.generate_ai_reply_with_context", fake_reply)
    payload = {"content": "Hello"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    assert response.json()["reply"] == "mocked answer"


def test_create_blueprint_endpoint(monkeypatch) -> None:
    blueprint = BotBlueprint(
        bot_id="bot-123",
        bot_name="Pizza Pro",
        tagline="Your personal pizza sales hero",
        tone="friendly",
        language="he",
        knowledge_base=["Menu", "Promotions"],
        system_prompt="Always sell pizza",
        sample_questions=["מה יש היום?"],
        sample_responses=["היי!"],
    )

    monkeypatch.setattr("app.routers.ai_router.create_bot_blueprint", lambda payload: blueprint)

    payload = {
        "business_name": "My Pizza",
        "business_description": "We sell artisan pizzas with fresh toppings and drinks.",
        "desired_bot_role": "Help customers pick pizzas",
        "target_audience": "Families",
        "preferred_tone": "Friendly",
        "preferred_language": "he",
    }

    response = client.post("/api/v1/bots/blueprint", json=payload)
    assert response.status_code == 200
    assert response.json()["bot_id"] == "bot-123"


def test_playground_endpoint(monkeypatch) -> None:
    monkeypatch.setattr(
        "app.routers.ai_router.chat_with_bot",
        lambda bot_id, session_id, message: f"reply to {message}",
    )

    response = client.post(
        "/api/v1/bots/bot-123/playground",
        json={"content": "מה המומלץ?"},
        headers={"X-Session-ID": "sess-1"},
    )
    assert response.status_code == 200
    assert response.json()["reply"] == "reply to מה המומלץ?"


def test_snippet_endpoint(monkeypatch) -> None:
    snippet = BotSnippetResponse(
        bot_id="bot-123",
        language="py",
        code="print('hi')",
        instructions="do it",
    )

    monkeypatch.setattr("app.routers.ai_router.generate_snippet", lambda bot_id, lang: snippet)

    response = client.get("/api/v1/bots/bot-123/snippet?lang=py")
    assert response.status_code == 200
    assert response.json()["code"] == "print('hi')"
