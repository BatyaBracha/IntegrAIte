from __future__ import annotations

from typing import List, Optional

from pydantic import BaseModel, Field

from app.models.bot import BotBlueprint, ChatTurn


class SessionState(BaseModel):
    """Serialized representation of a saved session."""

    blueprint: Optional[BotBlueprint] = None
    history: List[ChatTurn] = Field(default_factory=list)
