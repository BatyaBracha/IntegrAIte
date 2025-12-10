"""Placeholder AI service that can be wired to Gemini later."""

from typing import Optional


def generate_ai_reply(prompt: str) -> Optional[str]:
    """Return a simple canned reply for now; swap with Gemini integration later."""
    if not prompt:
        return None
    return "This is a placeholder AI response. Connect Gemini here."
