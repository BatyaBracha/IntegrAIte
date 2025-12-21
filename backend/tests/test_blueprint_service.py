import json
from types import SimpleNamespace

import pytest

from app.models.bot import BotBlueprintRequest
from app.services import blueprint_service
from app.services.exceptions import AIServiceError, MissingConfigurationError


@pytest.fixture(autouse=True)
def stub_settings(monkeypatch):
    monkeypatch.setattr(blueprint_service, "settings", SimpleNamespace(gemini_api_key="key"))


def _make_request() -> BotBlueprintRequest:
    return BotBlueprintRequest(
        business_name="Pizza Planet",
        business_description="We craft artisan pizzas with bold flavors and fast delivery.",
        desired_bot_role="Guide customers to the perfect pizza",
        target_audience="Families",
        preferred_tone="friendly",
        preferred_language="he",
    )


def test_create_bot_blueprint_persists_and_returns(monkeypatch):
    payload = {
        "bot_name": "Pizza Guru",
        "tagline": "Your pizza partner",
        "tone": "friendly",
        "language": "he",
        "knowledge_base": ["menu"],
        "system_prompt": "Serve pizza",
        "sample_questions": ["מה מומלץ"],
        "sample_responses": ["פיצה מרגריטה"],
    }
    fake_response = SimpleNamespace(text=json.dumps(payload))

    monkeypatch.setattr(blueprint_service, "generate_with_fallback", lambda prompt: (fake_response, "model"))

    saved = []
    resets = []
    monkeypatch.setattr(blueprint_service.store, "save_blueprint", lambda blueprint: saved.append(blueprint))
    monkeypatch.setattr(blueprint_service.store, "reset_history_for_bot", lambda bot_id: resets.append(bot_id))

    blueprint = blueprint_service.create_bot_blueprint(_make_request())

    assert blueprint.bot_name == "Pizza Guru"
    assert saved and saved[0] == blueprint
    assert resets == [blueprint.bot_id]


def test_create_bot_blueprint_raises_on_invalid_json(monkeypatch):
    fake_response = SimpleNamespace(text="not json")
    monkeypatch.setattr(blueprint_service, "generate_with_fallback", lambda prompt: (fake_response, "model"))

    with pytest.raises(AIServiceError, match="valid JSON"):
        blueprint_service.create_bot_blueprint(_make_request())


def test_create_bot_blueprint_requires_api_key(monkeypatch):
    monkeypatch.setattr(blueprint_service, "settings", SimpleNamespace(gemini_api_key=None))

    with pytest.raises(MissingConfigurationError):
        blueprint_service.create_bot_blueprint(_make_request())
