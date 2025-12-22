# #!/usr/bin/env bash
# set -euo pipefail

# # Always run relative to the repository root so docker compose finds its config.
# REPO_ROOT="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# cd "$REPO_ROOT"

# echo "[deploy] Stopping previous stack (if any)..."
# docker-compose down || true

# echo "[deploy] Starting updated stack..."
# docker-compose up -d --build

# echo "[deploy] Stack is up. Services:"
# docker-compose ps
