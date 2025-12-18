import json
import re
import uuid
from typing import Any


_JSON_BLOCK = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.DOTALL)


def _extract_braced_object(text: str) -> str | None:
    """Return the first balanced {...} block found in the text."""
    start = text.find("{")
    if start == -1:
        return None

    depth = 0
    for idx in range(start, len(text)):
        char = text[idx]
        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1
            if depth == 0:
                return text[start : idx + 1]
    return None


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
    except json.JSONDecodeError:
        fallback = _extract_braced_object(candidate)
        if fallback:
            try:
                return json.loads(fallback)
            except json.JSONDecodeError:
                pass
        raise ValueError("Gemini response is not valid JSON")
