from types import SimpleNamespace

from app.models.bot import BotBlueprint
from app.utils import snippets


def _blueprint() -> BotBlueprint:
    return BotBlueprint(
        bot_id="bot-abc",
        bot_name="Chat Couture",
        tagline="Designs every reply",
        tone="sleek",
        language="en",
        knowledge_base=["catalog", "orders"],
        system_prompt="Stay polished",
        sample_questions=["What is trending"],
        sample_responses=["Try the metallic set"],
    )


def test_build_snippet_payload_python(monkeypatch):
    blueprint = _blueprint()
    monkeypatch.setattr(snippets, "settings", SimpleNamespace(gemini_model="gemini-1.5-flash-latest"))

    response = snippets.build_snippet_payload(blueprint, "py")

    assert response.language == "py"
    assert "def ask_bot_abc" in response.code
    assert "gemini-1.5-flash-latest" in response.code
    assert "Set GEMINI_API_KEY" in response.instructions


def test_build_snippet_payload_javascript(monkeypatch):
    blueprint = _blueprint()
    monkeypatch.setattr(snippets, "settings", SimpleNamespace(gemini_model="gemini-pro"))

    response = snippets.build_snippet_payload(blueprint, "js")

    assert response.language == "js"
    assert "export async function ask" in response.code
    assert "gemini-pro" in response.code
    assert "@google/generative-ai" in response.instructions or "GEMINI_API_KEY" in response.instructions
