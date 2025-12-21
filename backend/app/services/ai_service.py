"""AI service powered by Google Gemini SDK with session-based chat memory."""

from __future__ import annotations
# Ensure TLS uses a proper CA bundle on Windows (avoid CERTIFICATE_VERIFY_FAILED)
# import os
# try:
#     import certifi
#     os.environ.setdefault("SSL_CERT_FILE", certifi.where())
#     os.environ.setdefault("REQUESTS_CA_BUNDLE", certifi.where())
# except Exception:
#     pass
from typing import Any, Dict, List, Optional

from app.core.config import get_settings
from app.services.gemini_client import generate_with_fallback

settings = get_settings()


# In-memory chat sessions (history is a list of Gemini content dicts)
ChatEntry = Dict[str, Any]
chat_sessions: Dict[str, List[ChatEntry]] = {}


def _user_message(text: str) -> ChatEntry:
    return {"role": "user", "parts": [{"text": text}]}


def _model_message(text: str) -> ChatEntry:
    return {"role": "model", "parts": [{"text": text}]}


def get_or_create_history(session_id: str) -> List[ChatEntry]:
    """Return mutable conversation history for a session."""
    return chat_sessions.setdefault(session_id, [])


def generate_ai_reply(prompt: str) -> Optional[str]:
    """Generate AI reply (stateless)."""
    if not prompt or not settings.gemini_api_key:
        return None
    
    try:
        response, _ = generate_with_fallback(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def generate_ai_reply_with_context(session_id: str, prompt: str) -> Optional[str]:
    """Generate AI reply with conversation history."""
    if not prompt or not settings.gemini_api_key:
        return None
    
    history = get_or_create_history(session_id)
    history.append(_user_message(prompt))

    try:
        response, _ = generate_with_fallback(history)
        history.append(_model_message(response.text))
        return response.text
    except Exception as e:
        # Remove the user turn we appended so the history stays consistent.
        history.pop()
        return f"Error: {str(e)}"
