from types import SimpleNamespace

import pytest

from app.services import ai_service


@pytest.fixture(autouse=True)
def reset_chat_sessions():
    ai_service.chat_sessions.clear()
    yield
    ai_service.chat_sessions.clear()


@pytest.fixture(autouse=True)
def stub_settings(monkeypatch):
    monkeypatch.setattr(ai_service, "settings", SimpleNamespace(gemini_api_key="key"))


def test_generate_ai_reply_returns_text(monkeypatch):
    fake_response = SimpleNamespace(text="hi there")
    monkeypatch.setattr(ai_service, "generate_with_fallback", lambda prompt: (fake_response, "model"))

    assert ai_service.generate_ai_reply("hello") == "hi there"


def test_generate_ai_reply_returns_none_without_key(monkeypatch):
    monkeypatch.setattr(ai_service, "settings", SimpleNamespace(gemini_api_key=None))

    assert ai_service.generate_ai_reply("hello") is None


def test_generate_ai_reply_with_context_tracks_history(monkeypatch):
    fake_response = SimpleNamespace(text="response")
    monkeypatch.setattr(ai_service, "generate_with_fallback", lambda history: (fake_response, "model"))

    reply = ai_service.generate_ai_reply_with_context("session-1", "Hi")

    assert reply == "response"
    history = ai_service.chat_sessions["session-1"]
    assert history[0]["parts"][0]["text"] == "Hi"
    assert history[1]["parts"][0]["text"] == "response"


def test_generate_ai_reply_with_context_rolls_back_on_error(monkeypatch):
    def _raise(history):
        raise RuntimeError("boom")

    monkeypatch.setattr(ai_service, "generate_with_fallback", _raise)

    result = ai_service.generate_ai_reply_with_context("session-err", "Hi")

    assert result.startswith("Error: boom")
    assert ai_service.chat_sessions["session-err"] == []