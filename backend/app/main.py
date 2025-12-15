from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers.ai_router import router as api_router

settings = get_settings()

app = FastAPI(title="IntegrAIte Backend", version="0.1.0")

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/health", tags=["system"])
def health_check() -> dict:
    """Lightweight liveness probe."""
    return {"status": "ok"}


# Mount versioned API router
app.include_router(api_router, prefix="/api/v1")
