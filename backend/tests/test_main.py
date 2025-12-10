from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_health_check():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_chat_placeholder():
    payload = {"content": "Hello"}
    response = client.post("/api/v1/chat", json=payload)
    assert response.status_code == 200
    assert "placeholder" in response.json()["reply"].lower()
