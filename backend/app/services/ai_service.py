"""AI service powered by Google Gemini SDK with session-based chat memory."""

import google.generativeai as genai
from typing import Optional, Dict

from app.core.config import get_settings

settings = get_settings()


def _model_name() -> str:
    return getattr(settings, "gemini_model", "gemini-2.0-flash")


# Configure Gemini
if settings.gemini_api_key:
    genai.configure(api_key=settings.gemini_api_key)

# In-memory chat sessions
chat_sessions: Dict[str, any] = {}


def get_or_create_chat(session_id: str):
    """Get existing chat or create new one."""
    if session_id not in chat_sessions:
        model = genai.GenerativeModel(_model_name())
        chat_sessions[session_id] = model.start_chat(history=[])
    return chat_sessions[session_id]


def generate_ai_reply(prompt: str) -> Optional[str]:
    """Generate AI reply (stateless)."""
    if not prompt or not settings.gemini_api_key:
        return None
    
    try:
        model = genai.GenerativeModel(_model_name())
        response = model.generate_content(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"


def generate_ai_reply_with_context(session_id: str, prompt: str) -> Optional[str]:
    """Generate AI reply with conversation history."""
    if not prompt or not settings.gemini_api_key:
        return None
    
    try:
        chat = get_or_create_chat(session_id)
        response = chat.send_message(prompt)
        return response.text
    except Exception as e:
        return f"Error: {str(e)}"
