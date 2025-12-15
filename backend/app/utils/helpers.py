import json
import re
import uuid
from typing import Any


_JSON_BLOCK = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def generate_session_id() -> str:
    """Create a simple session identifier for stateless frontends that still need correlation."""
    return str(uuid.uuid4())


def extract_json_from_text(raw_text: str) -> Any:
    """Best-effort extraction of a JSON object from a Gemini response."""
    if not raw_text:
        raise ValueError("Empty response from Gemini")

    candidate = raw_text.strip()
    match = _JSON_BLOCK.search(candidate)
    if match:
        candidate = match.group(1)

    try:
        return json.loads(candidate)
    except json.JSONDecodeError as exc:  # noqa: TRY003 - provide context
        raise ValueError("Gemini response is not valid JSON") from exc
