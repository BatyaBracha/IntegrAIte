"""Service that prepares deployment snippets for a bot blueprint."""
from __future__ import annotations

from app.models.bot import BotSnippetResponse, SnippetLanguage
from app.services.exceptions import BlueprintNotFoundError
from app.services.store import store
from app.utils.snippets import build_snippet_payload


def generate_snippet(bot_id: str, language: SnippetLanguage) -> BotSnippetResponse:
    blueprint = store.get_blueprint(bot_id)
    if blueprint is None:
        raise BlueprintNotFoundError(f"Bot with id {bot_id} was not found")
    return build_snippet_payload(blueprint, language)
