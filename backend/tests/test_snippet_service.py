from types import SimpleNamespace

import pytest

from app.models.bot import BotBlueprint
from app.services import snippet_service
from app.services.exceptions import BlueprintNotFoundError


def _blueprint() -> BotBlueprint:
    return BotBlueprint(
        bot_id="bot-snippet",
        bot_name="Snippet Bot",
        tagline="Ships code",
        tone="direct",
        language="en",
        knowledge_base=["kb"],
        system_prompt="Follow instructions",
        sample_questions=["hello"],
        sample_responses=["world"],
    )


def test_generate_snippet_returns_payload(monkeypatch):
    blueprint = _blueprint()
    monkeypatch.setattr(snippet_service.store, "get_blueprint", lambda bot_id: blueprint)
    payload = SimpleNamespace(bot_id=blueprint.bot_id, language="py", code="pass", instructions="copy")
    monkeypatch.setattr(snippet_service, "build_snippet_payload", lambda bp, lang: payload)

    response = snippet_service.generate_snippet(blueprint.bot_id, "py")

    assert response == payload


def test_generate_snippet_requires_blueprint(monkeypatch):
    monkeypatch.setattr(snippet_service.store, "get_blueprint", lambda bot_id: None)

    with pytest.raises(BlueprintNotFoundError):
        snippet_service.generate_snippet("missing", "py")
