from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.core.config import get_settings
from app.routers.ai_router import router as api_router

settings = get_settings()

app = FastAPI(title="IntegrAIte Backend", version="0.1.0")

# Ensure allowed_origins is a list of strings
origins = settings.allowed_origins
if isinstance(origins, str):
    origins = [o.strip() for o in origins.split(",")]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
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