from fastapi import FastAPI

from app.routers.ai_router import router as api_router

app = FastAPI(title="IntegrAIte Backend", version="0.1.0")


@app.get("/health", tags=["system"])
def health_check() -> dict:
    """Lightweight liveness probe."""
    return {"status": "ok"}


# Mount versioned API router
app.include_router(api_router, prefix="/api/v1")
