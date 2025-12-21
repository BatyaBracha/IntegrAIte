"""Centralized settings management."""
from functools import lru_cache
from typing import List, Optional

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

DEFAULT_GEMINI_MODELS: List[str] = [
    "gemini-1.5-pro",
    "gemini-1.5-pro-latest",
    "gemini-1.5-flash",
    "gemini-1.5-flash-latest",
    "gemini-2.5-flash",
    "gemini-2.5-pro",
    "gemini-2.5-flash-preview-09-2025",
    "gemini-2.5-flash-lite",
    "gemini-2.5-flash-lite-preview-09-2025",
    "gemini-2.5-flash-image",
    "gemini-2.5-flash-image-preview",
    "gemini-2.5-flash-preview-tts",
    "gemini-2.5-pro-preview-tts",
    "gemini-2.5-computer-use-preview-10-2025",
    "gemini-2.0-flash",
    "gemini-2.0-flash-001",
    "gemini-2.0-flash-exp",
    "gemini-2.0-flash-exp-image-generation",
    "gemini-2.0-flash-lite",
    "gemini-2.0-flash-lite-001",
    "gemini-2.0-flash-lite-preview",
    "gemini-2.0-flash-lite-preview-02-05",
    "gemini-3-pro-preview",
    "gemini-3-pro-image-preview",
    "gemini-flash-latest",
    "gemini-flash-lite-latest",
    "gemini-pro-latest",
    "gemini-exp-1206",
]


class Settings(BaseSettings):
    gemini_api_key: Optional[str] = Field(default=None, alias="GEMINI_API_KEY")
    gemini_model: str = Field(default="gemini-flash-latest", alias="GEMINI_MODEL")
    gemini_models: Optional[List[str]] = Field(default=None, alias="GEMINI_MODELS")
    frontend_origins: str = Field(default="http://localhost:3000", alias="FRONTEND_ORIGINS")

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

    @field_validator("gemini_model", mode="before")
    @classmethod
    def _validate_model(cls, value: str) -> str:
        if value and value not in DEFAULT_GEMINI_MODELS:
            raise ValueError(
                f"Unknown GEMINI_MODEL '{value}'. Choose one of: {', '.join(DEFAULT_GEMINI_MODELS)}"
            )
        return value

    @field_validator("gemini_models", mode="before")
    @classmethod
    def _split_models(cls, value):
        if isinstance(value, str):
            return [item.strip() for item in value.split(",") if item.strip()]
        return value

    @field_validator("gemini_models")
    @classmethod
    def _validate_models(cls, value: Optional[List[str]]):
        if not value:
            return value
        unknown = [model for model in value if model not in DEFAULT_GEMINI_MODELS]
        if unknown:
            raise ValueError(
                "Unknown GEMINI_MODELS entries: "
                f"{', '.join(unknown)}. Choose values from: {', '.join(DEFAULT_GEMINI_MODELS)}"
            )
        return value

    @property
    def allowed_origins(self) -> list[str]:
        """Normalized list of origins allowed by CORS."""
        return [origin.strip() for origin in self.frontend_origins.split(",") if origin.strip()]

    @property
    def available_models(self) -> List[str]:
        return DEFAULT_GEMINI_MODELS

    @property
    def preferred_models(self) -> List[str]:
        models = self.gemini_models or [self.gemini_model]
        ordered: List[str] = []
        for model in models:
            if model and model not in ordered:
                ordered.append(model)
        return ordered


@lru_cache(maxsize=1)
def get_settings() -> Settings:
    """Cached settings loader."""
    return Settings()
