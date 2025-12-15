"""Service powering the live Playground chat flow."""
from __future__ import annotations

import google.generativeai as genai

from app.core.config import get_settings
from app.models.bot import ChatTurn
from app.services.exceptions import AIServiceError, BlueprintNotFoundError, MissingConfigurationError
from app.services.store import store
from app.utils.prompts import build_playground_prompt

settings = get_settings()


def _ensure_configured() -> None:
    if not settings.gemini_api_key:
        raise MissingConfigurationError("Gemini API key missing. Set GEMINI_API_KEY in the environment.")
    genai.configure(api_key=settings.gemini_api_key)


def _resolve_model_name() -> str:
    return getattr(settings, "gemini_model", "gemini-2.0-flash")


def chat_with_bot(bot_id: str, session_id: str, user_message: str) -> str:
    """Send the Playground message through Gemini and persist history."""
    _ensure_configured()

    blueprint = store.get_blueprint(bot_id)
    if blueprint is None:
        raise BlueprintNotFoundError(f"Bot with id {bot_id} was not found")

    turns = store.get_history(bot_id, session_id)
    prompt = build_playground_prompt(blueprint, turns, user_message)

    try:
        model = genai.GenerativeModel(_resolve_model_name())
        response = model.generate_content(prompt)
        reply = (response.text or "").strip()
    except Exception as exc:  # noqa: BLE001
        raise AIServiceError(str(exc)) from exc

    if not reply:
        raise AIServiceError("Gemini returned an empty response")

    store.append_turn(bot_id, session_id, ChatTurn(role="user", content=user_message))
    store.append_turn(bot_id, session_id, ChatTurn(role="assistant", content=reply))

    return reply
