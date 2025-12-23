"""Business logic for generating bot blueprints via Gemini."""
from __future__ import annotations

import uuid
from typing import Any, Dict, Optional

from app.core.config import get_settings
from app.models.bot import BotBlueprint, BotBlueprintRequest
from app.services.exceptions import AIServiceError, MissingConfigurationError
from app.services.gemini_client import generate_with_fallback
from app.services.store import store
from app.utils.helpers import extract_json_from_text
from app.utils.prompts import build_blueprint_prompt

settings = get_settings()


def _ensure_configured() -> None:
    if not settings.gemini_api_key:
        raise MissingConfigurationError("Gemini API key missing. Set GEMINI_API_KEY in the environment.")


def _parse_blueprint_payload(payload: Dict[str, Any]) -> BotBlueprint:
    return BotBlueprint(
        bot_id=str(uuid.uuid4()),
        bot_name=payload.get("bot_name", "Custom AI Buddy"),
        tagline=payload.get("tagline", "An assistant tailored to your business"),
        tone=payload.get("tone", "friendly"),
        language=payload.get("language", "he"),
        knowledge_base=payload.get("knowledge_base", []),
        system_prompt=payload.get("system_prompt", "You are a helpful assistant."),
        sample_questions=payload.get("sample_questions", []),
        sample_responses=payload.get("sample_responses", []),
    )


def create_bot_blueprint(request: BotBlueprintRequest, session_id: Optional[str] = None) -> BotBlueprint:
    """Call Gemini to transform interview answers into a bot blueprint."""
    _ensure_configured()

    prompt = build_blueprint_prompt(
        business_name=request.business_name,
        business_description=request.business_description,
        desired_bot_role=request.desired_bot_role,
        target_audience=request.target_audience or "not specified",
        preferred_tone=request.preferred_tone or "balanced professional",
        preferred_language=request.preferred_language,
    )

    try:
        response, _ = generate_with_fallback(prompt)
        blueprint_dict = extract_json_from_text(response.text)
    except Exception as exc:  # noqa: BLE001 - want to wrap SDK errors
        raise AIServiceError(str(exc)) from exc

    if not isinstance(blueprint_dict, dict):
        import sys
        print(f"[ERROR] Gemini response is not a valid JSON object: {blueprint_dict}", file=sys.stderr)
        raise AIServiceError("Gemini response is not a valid JSON object")

    blueprint = _parse_blueprint_payload(blueprint_dict)
    store.save_blueprint(blueprint)
    store.reset_history_for_bot(blueprint.bot_id)
    if session_id:
        store.assign_session(blueprint.bot_id, session_id)
    return blueprint
