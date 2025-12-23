# IntegrAIte Backend (FastAPI)

Stateless FastAPI skeleton with a placeholder AI endpoint (ready to connect to Gemini). No database is used; each request is independent.

## Quickstart

```bash
python -m venv .venv
.venv\Scripts\activate  # Windows
pip install -r requirements.txt
uvicorn app.main:app --reload
```

Then open http://localhost:8000/docs for interactive API docs.

## Configuration
- Place environment variables in a `.env` file at the project root (loaded automatically).
- `GEMINI_API_KEY` (optional) — required once you wire Gemini in `services/ai_service.py`.
- `STORE_PATH` (default `data/store.json`) — filesystem location for the JSON store that keeps bot blueprints and chat history. Set to `:memory:` to disable persistence.
- `STORE_MAX_SESSIONS` (default `10`) — maximum number of sessions preserved per bot. Oldest sessions are discarded first.
- `STORE_MAX_TURNS` (default `200`) — maximum conversation turns retained per session. Oldest turns are trimmed.

## Tests

```bash
pytest
```

## Docker

```bash
# build
docker build -t integraite-backend .
# run
docker run -p 8000:8000 integraite-backend
```

## Endpoints
- `GET /health` – liveness probe
- `GET /api/v1/ping` – simple ping
- `POST /api/v1/chat` – accepts `{ "content": "..." }` and returns a placeholder reply

## Next steps
- Replace `services/ai_service.py` with real Gemini API calls.
- Add request/session context if you later want per-session memory.
- Add authentication and rate limiting as needed.
