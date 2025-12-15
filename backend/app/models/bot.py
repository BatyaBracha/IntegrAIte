"""Pydantic models describing bot blueprints and playground payloads."""
from __future__ import annotations

from typing import List, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class BotBlueprintRequest(BaseModel):
    """Information collected during the "Interview" stage."""

    business_name: str = Field(..., min_length=2, description="Displayed business name")
    business_description: str = Field(
        ..., min_length=20, description="Free text describing the business and offering"
    )
    desired_bot_role: str = Field(
        ..., min_length=10, description="Goal for the bot (e.g. customer support, sales)"
    )
    target_audience: Optional[str] = Field(
        default=None, description="Who the bot primarily serves"
    )
    preferred_tone: Optional[str] = Field(
        default=None,
        description="Desired tone of voice (friendly, expert, playful, etc.)",
    )
    preferred_language: str = Field(
        default="he",
        description="Primary language for the bot responses (defaults to Hebrew)",
    )

    @field_validator("preferred_language")
    @classmethod
    def normalize_language(cls, value: str) -> str:
        return value.lower()


class BotBlueprint(BaseModel):
    """Structured definition of a generated bot."""

    bot_id: str
    bot_name: str
    tagline: str
    tone: str
    language: str
    knowledge_base: List[str]
    system_prompt: str
    sample_questions: List[str]
    sample_responses: List[str]


class ChatTurn(BaseModel):
    role: Literal["user", "assistant"]
    content: str = Field(..., min_length=1)


class PlaygroundMessage(BaseModel):
    content: str = Field(..., min_length=1)


SnippetLanguage = Literal["py", "js"]


class BotSnippetResponse(BaseModel):
    bot_id: str
    language: SnippetLanguage
    code: str
    instructions: str
