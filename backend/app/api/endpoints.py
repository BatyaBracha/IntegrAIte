from fastapi import APIRouter, HTTPException

from app.models.message import ChatMessage, ChatResponse
from app.services.ai_service import generate_ai_reply

router = APIRouter(tags=["chat"])


@router.get("/ping", summary="Simple ping")
def ping() -> dict:
    return {"message": "pong"}


@router.post("/chat", response_model=ChatResponse, summary="Chat with AI (stateless)")
def chat(message: ChatMessage) -> ChatResponse:
    """
    Accept a single message and return an AI-generated reply.
    This implementation is stateless and keeps no conversation history.
    """
    reply = generate_ai_reply(message.content)
    if reply is None:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    return ChatResponse(reply=reply)
