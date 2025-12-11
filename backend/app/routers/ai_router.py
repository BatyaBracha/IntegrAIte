from fastapi import APIRouter, HTTPException, Header

from app.models.message import ChatMessage, ChatResponse
from app.services.ai_service import generate_ai_reply_with_context

router = APIRouter(tags=["chat"])


@router.get("/ping", summary="Simple ping")
def ping() -> dict:
    return {"message": "pong"}


@router.post("/chat", response_model=ChatResponse, summary="Chat with AI maintaining context")
def chat(
    message: ChatMessage,
    session_id: str = Header(default="default", alias="X-Session-ID")
) -> ChatResponse:
    """
    Chat with AI maintaining conversation history per session.
    Send X-Session-ID header to maintain context across requests.
    """
    reply = generate_ai_reply_with_context(session_id, message.content)
    if reply is None:
        raise HTTPException(status_code=503, detail="AI service unavailable")
    return ChatResponse(reply=reply)
