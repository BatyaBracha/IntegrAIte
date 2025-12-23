from app.models.bot import BotBlueprint, ChatTurn
from app.services.store import JsonStore


def _blueprint(bot_id: str = "bot-1") -> BotBlueprint:
    return BotBlueprint(
        bot_id=bot_id,
        bot_name="Pizza Guide",
        tagline="Helps you pick the right pizza",
        tone="playful",
        language="he",
        knowledge_base=["menu", "allergens"],
        system_prompt="Always suggest a pizza",
        sample_questions=["מה טעים"],
        sample_responses=["נסה מרגריטה"],
    )


def _turn(role: str, content: str) -> ChatTurn:
    return ChatTurn(role=role, content=content)


def test_save_and_get_blueprint() -> None:
    store = JsonStore(":memory:")
    blueprint = _blueprint()

    store.save_blueprint(blueprint)

    assert store.get_blueprint("bot-1") == blueprint
    assert store.get_blueprint("missing") is None


def test_history_is_isolated_and_resettable() -> None:
    store = JsonStore(":memory:")
    store.append_turn("bot-1", "sess", _turn("user", "hi"))
    store.append_turn("bot-2", "sess", _turn("assistant", "hey"))

    history = store.get_history("bot-1", "sess")
    history.append(_turn("assistant", "mutated"))

    assert store.get_history("bot-1", "sess") == [_turn("user", "hi")]

    store.reset_history_for_bot("bot-1")

    assert store.get_history("bot-1", "sess") == []
    assert store.get_history("bot-2", "sess") == [_turn("assistant", "hey")]


def test_session_assignment_and_state() -> None:
    store = JsonStore(":memory:")
    blueprint = _blueprint("bot-xyz")
    store.save_blueprint(blueprint)
    store.assign_session(blueprint.bot_id, "sess-9")
    store.append_turn(blueprint.bot_id, "sess-9", _turn("user", "hi"))
    store.append_turn(blueprint.bot_id, "sess-9", _turn("assistant", "hello"))

    state_blueprint, history = store.get_session_state("sess-9")

    assert state_blueprint == blueprint
    assert history == [_turn("user", "hi"), _turn("assistant", "hello")]


def test_session_limit_discards_oldest_sessions() -> None:
    store = JsonStore(":memory:", max_sessions_per_bot=2)
    blueprint = _blueprint("bot-limit")
    store.save_blueprint(blueprint)

    store.assign_session(blueprint.bot_id, "sess-1")
    store.assign_session(blueprint.bot_id, "sess-2")
    store.assign_session(blueprint.bot_id, "sess-3")  # pushes out sess-1

    missing_blueprint, missing_history = store.get_session_state("sess-1")
    assert missing_blueprint is None
    assert missing_history == []

    _, still_there = store.get_session_state("sess-2")
    assert still_there == []
    _, newest = store.get_session_state("sess-3")
    assert newest == []


def test_turn_limit_keeps_recent_messages_only() -> None:
    store = JsonStore(":memory:", max_turns_per_session=3)
    blueprint = _blueprint("bot-turns")
    store.save_blueprint(blueprint)
    store.assign_session(blueprint.bot_id, "sess-cut")

    store.append_turn(blueprint.bot_id, "sess-cut", _turn("user", "m1"))
    store.append_turn(blueprint.bot_id, "sess-cut", _turn("assistant", "a1"))
    store.append_turn(blueprint.bot_id, "sess-cut", _turn("user", "m2"))
    store.append_turn(blueprint.bot_id, "sess-cut", _turn("assistant", "a2"))

    assert store.get_history(blueprint.bot_id, "sess-cut") == [
        _turn("assistant", "a1"),
        _turn("user", "m2"),
        _turn("assistant", "a2"),
    ]
