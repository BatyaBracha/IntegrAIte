"""Simple in-memory storage for blueprints and conversation history."""
from __future__ import annotations

import threading
from typing import Dict, List, Tuple

from app.models.bot import BotBlueprint, ChatTurn


class InMemoryStore:
    def __init__(self) -> None:
        self._blueprints: Dict[str, BotBlueprint] = {}
        self._history: Dict[Tuple[str, str], List[ChatTurn]] = {}
        self._lock = threading.Lock()

    def save_blueprint(self, blueprint: BotBlueprint) -> None:
        with self._lock:
            self._blueprints[blueprint.bot_id] = blueprint

    def get_blueprint(self, bot_id: str) -> BotBlueprint | None:
        with self._lock:
            return self._blueprints.get(bot_id)

    def reset_history_for_bot(self, bot_id: str) -> None:
        with self._lock:
            keys_to_remove = [key for key in self._history if key[0] == bot_id]
            for key in keys_to_remove:
                self._history.pop(key, None)

    def append_turn(self, bot_id: str, session_id: str, turn: ChatTurn) -> None:
        key = (bot_id, session_id)
        with self._lock:
            if key not in self._history:
                self._history[key] = []
            self._history[key].append(turn)

    def get_history(self, bot_id: str, session_id: str) -> List[ChatTurn]:
        key = (bot_id, session_id)
        with self._lock:
            turns = self._history.get(key, [])
            return list(turns)


store = InMemoryStore()
