# IntegrAIte

From Zero to AI Hero – a full-stack factory that creates bespoke AI agents for any small business in minutes.

## Project structure

```
backend/   # FastAPI + Gemini orchestration
frontend/  # React SPA (Interview + Playground + Deploy snippet)
```

## Prerequisites

- Python 3.11+
- Node.js 20+
- Docker + Docker Compose (for the containerized workflow)

## Environment variables

```bash
cp backend/.env.example backend/.env       # add GEMINI_API_KEY inside
cp frontend/.env.example frontend/.env     # optional override for local dev
```

Key variables:

- `GEMINI_API_KEY` – required for all Gemini calls (backend).
- `GEMINI_MODEL` – defaults to `gemini-2.0-flash` but can be changed.
- `REACT_APP_API_BASE` – frontend base URL (defaults to `http://localhost:8000/api/v1`).

## Running locally (without Docker)

```bash
# backend
cd backend
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload

# frontend (another shell)
cd frontend
npm install
npm start
```

The SPA runs on http://localhost:3000 and proxies API calls to the FastAPI server on http://localhost:8000.

## Docker workflow

```bash
docker compose up --build
```

- Backend: http://localhost:8000 (FastAPI docs under `/docs`).
- Frontend: http://localhost:3000 (static build served by Nginx, configured` to call `http://backend:8000/api/v1`).

## Tests

- Backend: `cd backend && python -m pytest`
- Frontend: `cd frontend && npm test -- --watchAll=false`

## Deployment notes

- The Dockerfiles are production-ready (multi-stage for the frontend, slim Python image for backend).
- To integrate CI/CD, add steps for installing dependencies, running the tests above, and building both images before pushing.