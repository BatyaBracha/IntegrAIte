
# 🚀 IntegrAIte: From Zero to AI Hero

> **Spin up a bespoke AI agent for your business in minutes.**
>
> IntegrAIte is a full-stack, production-ready platform that lets you design, test, and deploy custom AI agents—no ML expertise required.

---

## 🧩 What’s Inside?

- **Backend:** FastAPI + Gemini (Google AI) orchestration
- **Frontend:** Modern React SPA (Interview, Playground, Snippet Export)
- **CI/CD Ready:** Docker, Jenkins, and production-grade configs

---

## ✨ Features

- **Lightning-fast onboarding:** Answer 3 questions, generate a unique AI persona for your business.
- **Live Playground:** Chat with your bot instantly—see how it thinks before you deploy.
- **One-click Export:** Get production-ready code snippets (Python/JS) for instant integration.
- **Session persistence:** Close your browser and your last bot + chat come right back, thanks to a JSON-backed store.
- **Day/Night Mode:** Beautiful, modern UI with seamless light/dark switching.
- **Database optional:** Bots + chat history live in `data/store.json` by default—no external DB needed.

---

## 🛠️ Quickstart

### Prerequisites
- Python 3.11+
- Node.js 20+
- Docker + Docker Compose (for full-stack containerized workflow)

### Environment Setup

```bash
cp backend/.env.example backend/.env       # Add your GEMINI_API_KEY
cp frontend/.env.example frontend/.env     # (Optional) Frontend overrides
```

**Key variables:**
- `GEMINI_API_KEY` – required for Gemini API (backend)
- `GEMINI_MODEL` – defaults to `gemini-2.0-flash`
- `REACT_APP_API_BASE` – frontend API base (default: `http://localhost:8000/api/v1`)
- `STORE_PATH` – where bot/session JSON lives (default: `data/store.json`)

### Local Development

**Backend:**
```bash
cd backend
python -m venv .venv && .venv/Scripts/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

**Frontend:**
```bash
cd frontend
npm install
npm start
```

Open [http://localhost:3000](http://localhost:3000) — the SPA proxies API calls to FastAPI at [http://localhost:8000](http://localhost:8000).

---

## 🐳 Docker Workflow

```bash
docker compose up --build
```

- **Backend:** [http://localhost:8000](http://localhost:8000) (API docs: `/docs`)
- **Frontend:** [http://localhost:3000](http://localhost:3000) (served by Nginx, auto-wired to backend)
- **Persistent data:** `backend/data` is mounted into the backend container so `data/store.json` survives restarts. Back it up or change `STORE_PATH` to suit your infra.

---

## 🧪 Testing

- **Backend:** `cd backend && python -m pytest`
- **Frontend:** `cd frontend && npm test -- --watchAll=false`

---

## 🚀 Deployment & CI/CD

- Production-ready Dockerfiles (multi-stage for frontend, slim Python for backend)
- Jenkinsfile included for easy CI/CD integration
- Add your own steps for cloud deploys, secrets, and monitoring

---

## 💡 Why IntegrAIte?

- **Instant value:** Go from idea to working AI agent in minutes
- **No vendor lock-in:** Export and run anywhere
- **Modern UX:** Beautiful, accessible, and responsive
- **Open & hackable:** Tweak, extend, or self-host with ease

---

**Ready to build your next AI agent?**

Clone, configure, and launch your own IntegrAIte instance today!