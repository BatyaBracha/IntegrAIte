from pydantic import BaseModel, Field


class ChatMessage(BaseModel):
    content: str = Field(..., min_length=1, description="User message content")


class ChatResponse(BaseModel):
    reply: str = Field(..., description="AI-generated reply")
