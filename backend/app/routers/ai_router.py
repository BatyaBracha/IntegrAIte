from fastapi import APIRouter, Header, HTTPException, Query

from app.models.bot import (
    BotBlueprint,
    BotBlueprintRequest,
    BotSnippetResponse,
    PlaygroundMessage,
    SnippetLanguage,
)
from app.models.message import ChatMessage, ChatResponse
from app.services.ai_service import generate_ai_reply_with_context
from app.services.blueprint_service import create_bot_blueprint
from app.services.exceptions import (
    AIServiceError,
    BlueprintNotFoundError,
    MissingConfigurationError,
)
from app.services.playground_service import chat_with_bot
from app.services.snippet_service import generate_snippet

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


@router.post(
    "/bots/blueprint",
    response_model=BotBlueprint,
    summary="Create a bot blueprint from interview answers",
)
def create_blueprint(payload: BotBlueprintRequest) -> BotBlueprint:
    try:
        return create_bot_blueprint(payload)
    except MissingConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.post(
    "/bots/{bot_id}/playground",
    response_model=ChatResponse,
    summary="Talk to a freshly generated bot",
)
def playground_chat(
    bot_id: str,
    message: PlaygroundMessage,
    session_id: str = Header(default="default", alias="X-Session-ID"),
) -> ChatResponse:
    try:
        reply = chat_with_bot(bot_id, session_id, message.content)
        return ChatResponse(reply=reply)
    except MissingConfigurationError as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc
    except BlueprintNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
    except AIServiceError as exc:
        raise HTTPException(status_code=502, detail=str(exc)) from exc


@router.get(
    "/bots/{bot_id}/snippet",
    response_model=BotSnippetResponse,
    summary="Return deployment code for the generated bot",
)
def export_snippet(
    bot_id: str,
    lang: SnippetLanguage = Query(default="py", description="Output language: py or js"),
) -> BotSnippetResponse:
    try:
        return generate_snippet(bot_id, lang)
    except BlueprintNotFoundError as exc:
        raise HTTPException(status_code=404, detail=str(exc)) from exc
