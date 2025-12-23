"""JSON-backed storage for blueprints, sessions, and conversation history."""
from __future__ import annotations

import json
import threading
from collections import OrderedDict
from pathlib import Path
from typing import Dict, List

from app.core.config import get_settings
from app.models.bot import BotBlueprint, ChatTurn


class JsonStore:
    def __init__(
        self,
        storage_path: str | Path | None = None,
        *,
        max_sessions_per_bot: int | None = None,
        max_turns_per_session: int | None = None,
    ) -> None:
        settings = get_settings()
        path_value = storage_path if storage_path is not None else settings.store_path
        self._memory_only = not path_value or str(path_value).lower() == ":memory:"
        self._path = None if self._memory_only else Path(path_value).resolve()
        if self._path is not None:
            self._path.parent.mkdir(parents=True, exist_ok=True)

        sessions_cap = max_sessions_per_bot or settings.store_max_sessions_per_bot
        turns_cap = max_turns_per_session or settings.store_max_turns_per_session
        if sessions_cap < 1 or turns_cap < 1:
            raise ValueError("Storage limits must be positive integers")

        self._max_sessions_per_bot = sessions_cap
        self._max_turns_per_session = turns_cap

        self._blueprints: Dict[str, BotBlueprint] = {}
        self._history: Dict[str, OrderedDict[str, List[ChatTurn]]] = {}
        self._session_map: Dict[str, str] = {}
        self._lock = threading.Lock()

        self._load()

    # ---------------------------------------------------------------------
    # Persistence helpers
    # ---------------------------------------------------------------------
    def _load(self) -> None:
        if self._memory_only or self._path is None or not self._path.exists():
            return

        try:
            raw = json.loads(self._path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            return

        blueprints = raw.get("blueprints", {})
        history = raw.get("history", {})
        sessions = raw.get("sessions", {})

        self._blueprints = {bot_id: BotBlueprint(**data) for bot_id, data in blueprints.items()}
        self._history = {
            bot_id: OrderedDict(
                (session_id, [ChatTurn(**turn) for turn in turns or []])
                for session_id, turns in session_map.items()
            )
            for bot_id, session_map in history.items()
        }
        self._session_map = {session_id: bot_id for session_id, bot_id in sessions.items()}

    def _save_locked(self) -> None:
        if self._memory_only or self._path is None:
            return

        payload = {
            "blueprints": {bot_id: blueprint.model_dump() for bot_id, blueprint in self._blueprints.items()},
            "history": {
                bot_id: {
                    session_id: [turn.model_dump() for turn in turns]
                    for session_id, turns in session_map.items()
                }
                for bot_id, session_map in self._history.items()
            },
            "sessions": dict(self._session_map),
        }
        self._path.write_text(json.dumps(payload, indent=2, ensure_ascii=False), encoding="utf-8")

    # ---------------------------------------------------------------------
    # Blueprint APIs
    # ---------------------------------------------------------------------
    def save_blueprint(self, blueprint: BotBlueprint) -> None:
        with self._lock:
            self._blueprints[blueprint.bot_id] = blueprint
            self._history.setdefault(blueprint.bot_id, OrderedDict())
            self._save_locked()

    def get_blueprint(self, bot_id: str) -> BotBlueprint | None:
        with self._lock:
            return self._blueprints.get(bot_id)

    # ---------------------------------------------------------------------
    # Session association
    # ---------------------------------------------------------------------
    def assign_session(self, bot_id: str, session_id: str) -> None:
        if not session_id:
            return
        with self._lock:
            previous_bot = self._session_map.get(session_id)
            if previous_bot and previous_bot in self._history:
                self._history[previous_bot].pop(session_id, None)
            self._session_map[session_id] = bot_id
            bot_sessions = self._history.setdefault(bot_id, OrderedDict())
            if session_id in bot_sessions:
                bot_sessions.move_to_end(session_id)
            else:
                bot_sessions[session_id] = []
            self._trim_sessions_for_bot(bot_id)
            self._save_locked()

    def get_session_state(self, session_id: str) -> tuple[BotBlueprint | None, List[ChatTurn]]:
        with self._lock:
            bot_id = self._session_map.get(session_id)
            if not bot_id:
                return None, []
            blueprint = self._blueprints.get(bot_id)
            turns = list(self._history.get(bot_id, {}).get(session_id, []))
            return blueprint, turns

    # ---------------------------------------------------------------------
    # Conversation history
    # ---------------------------------------------------------------------
    def reset_history_for_bot(self, bot_id: str) -> None:
        with self._lock:
            if bot_id in self._history:
                self._history[bot_id] = OrderedDict()
            self._save_locked()

    def append_turn(self, bot_id: str, session_id: str, turn: ChatTurn) -> None:
        with self._lock:
            bot_sessions = self._history.setdefault(bot_id, OrderedDict())
            turns = bot_sessions.setdefault(session_id, [])
            turns.append(turn)
            if len(turns) > self._max_turns_per_session:
                del turns[: len(turns) - self._max_turns_per_session]
            bot_sessions.move_to_end(session_id)
            self._save_locked()

    def get_history(self, bot_id: str, session_id: str) -> List[ChatTurn]:
        with self._lock:
            turns = self._history.get(bot_id, OrderedDict()).get(session_id, [])
            return list(turns)

    # ------------------------------------------------------------------
    # Utilities (primarily for tests/admin tasks)
    # ------------------------------------------------------------------
    def clear(self) -> None:
        with self._lock:
            self._blueprints.clear()
            self._history.clear()
            self._session_map.clear()
            if not self._memory_only and self._path and self._path.exists():
                try:
                    self._path.unlink()
                except OSError:
                    pass

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _trim_sessions_for_bot(self, bot_id: str) -> None:
        bot_sessions = self._history.get(bot_id)
        if not bot_sessions:
            return
        while len(bot_sessions) > self._max_sessions_per_bot:
            oldest_session_id, _ = bot_sessions.popitem(last=False)
            self._session_map.pop(oldest_session_id, None)


store = JsonStore()
