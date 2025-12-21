from types import SimpleNamespace

import pytest

from app.models.bot import BotBlueprint, ChatTurn
from app.services import playground_service
from app.services.exceptions import AIServiceError, BlueprintNotFoundError, MissingConfigurationError


def _blueprint() -> BotBlueprint:
    return BotBlueprint(
        bot_id="bot-123",
        bot_name="Pizza Sherpa",
        tagline="Guides every order",
        tone="friendly",
        language="he",
        knowledge_base=["menu"],
        system_prompt="Always help the user",
        sample_questions=["מה מומלץ"],
        sample_responses=["נסה מרגריטה"],
    )


def _history() -> list[ChatTurn]:
    return [ChatTurn(role="user", content="hi there")]


def _fake_store(monkeypatch, blueprint=None):
    class _Store:
        def __init__(self):
            self.appended: list[tuple[str, str, ChatTurn]] = []

        def get_blueprint(self, bot_id: str):
            if blueprint and bot_id == blueprint.bot_id:
                return blueprint
            return None

        def get_history(self, bot_id: str, session_id: str):
            return _history()

        def append_turn(self, bot_id: str, session_id: str, turn: ChatTurn):
            self.appended.append((bot_id, session_id, turn))

    instance = _Store()
    monkeypatch.setattr(playground_service, "store", instance)
    return instance


def _configure_settings(monkeypatch, api_key: str | None = "key") -> None:
    monkeypatch.setattr(playground_service, "settings", SimpleNamespace(gemini_api_key=api_key))


def test_chat_with_bot_returns_clean_reply(monkeypatch):
    blueprint = _blueprint()
    fake_store = _fake_store(monkeypatch, blueprint)
    _configure_settings(monkeypatch)
    monkeypatch.setattr(playground_service, "build_playground_prompt", lambda *args: "prompt")
    monkeypatch.setattr(
        playground_service,
        "generate_with_fallback",
        lambda prompt: (SimpleNamespace(text="  hi  "), "model"),
    )

    reply = playground_service.chat_with_bot("bot-123", "sess-1", "שלום")

    assert reply == "hi"
    assert [turn.role for *_, turn in fake_store.appended] == ["user", "assistant"]
    assert fake_store.appended[-1][2].content == "hi"


def test_chat_with_bot_requires_blueprint(monkeypatch):
    _fake_store(monkeypatch, blueprint=None)
    _configure_settings(monkeypatch)

    with pytest.raises(BlueprintNotFoundError):
        playground_service.chat_with_bot("missing", "sess", "hi")


def test_chat_with_bot_requires_api_key(monkeypatch):
    _fake_store(monkeypatch, _blueprint())
    _configure_settings(monkeypatch, api_key=None)

    with pytest.raises(MissingConfigurationError):
        playground_service.chat_with_bot("bot-123", "sess", "hi")


def test_chat_with_bot_validates_reply(monkeypatch):
    _fake_store(monkeypatch, _blueprint())
    _configure_settings(monkeypatch)
    monkeypatch.setattr(playground_service, "build_playground_prompt", lambda *args: "prompt")
    monkeypatch.setattr(
        playground_service,
        "generate_with_fallback",
        lambda prompt: (SimpleNamespace(text="   "), "model"),
    )

    with pytest.raises(AIServiceError, match="empty"):
        playground_service.chat_with_bot("bot-123", "sess", "hi")


def test_chat_with_bot_wraps_unknown_errors(monkeypatch):
    _fake_store(monkeypatch, _blueprint())
    _configure_settings(monkeypatch)
    monkeypatch.setattr(playground_service, "build_playground_prompt", lambda *args: "prompt")

    def _boom(prompt):  # noqa: ARG001 - signature defined by dependency
        raise RuntimeError("explode")

    monkeypatch.setattr(playground_service, "generate_with_fallback", _boom)

    with pytest.raises(AIServiceError, match="explode"):
        playground_service.chat_with_bot("bot-123", "sess", "hi")
