"""Shared Gemini client helpers with fallback logic across models."""
from __future__ import annotations

import os
import logging
from typing import Any, List, Optional, Tuple

from google import genai
from google.api_core import exceptions as google_exceptions

from app.core.config import get_settings
from app.services.exceptions import MissingConfigurationError

_DEFAULT_CA_PATH = "/etc/ssl/certs/ca-certificates.crt"
for var in ("REQUESTS_CA_BUNDLE", "SSL_CERT_FILE", "GRPC_DEFAULT_SSL_ROOTS_FILE_PATH"):
    os.environ.setdefault(var, _DEFAULT_CA_PATH)

settings = get_settings()
_client: Optional[genai.Client] = None
logger = logging.getLogger(__name__)


def _ensure_client() -> genai.Client:
    global _client
    if not settings.gemini_api_key:
        raise MissingConfigurationError("Gemini API key missing. Set GEMINI_API_KEY in the environment.")
    if _client is None:
        _client = genai.Client(api_key=settings.gemini_api_key)
    return _client


def _model_candidates() -> List[str]:
    models = settings.preferred_models
    if not models:
        raise MissingConfigurationError("No Gemini models configured. Set GEMINI_MODEL or GEMINI_MODELS.")
    return models


def _is_retryable(exc: Exception) -> bool:
    if isinstance(exc, google_exceptions.ResourceExhausted):
        return True
    message = str(exc).upper()
    return "RESOURCE_EXHAUSTED" in message or "QUOTA" in message or "429" in message


def generate_with_fallback(contents: Any) -> Tuple[genai.types.GenerateContentResponse, str]:
    """Try each preferred model until one succeeds; raises last error otherwise."""
    client = _ensure_client()
    last_exc: Optional[Exception] = None

    for model_name in _model_candidates():
        try:
            response = client.models.generate_content(model=model_name, contents=contents)
            logger.info("Gemini call succeeded with model %s", model_name)
            return response, model_name
        except Exception as exc:  # pragma: no cover - passthrough to fallback logic
            last_exc = exc
            logger.warning(
                "Gemini call failed for model %s (%s): %s",
                model_name,
                exc.__class__.__name__,
                exc,
            )
            if not _is_retryable(exc):
                raise
    if last_exc:
        raise last_exc
    raise MissingConfigurationError("Unable to select a Gemini model.")
