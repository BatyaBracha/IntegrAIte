from app.models.bot import BotBlueprint, ChatTurn
from app.services.store import InMemoryStore


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
    store = InMemoryStore()
    blueprint = _blueprint()

    store.save_blueprint(blueprint)

    assert store.get_blueprint("bot-1") == blueprint
    assert store.get_blueprint("missing") is None


def test_history_is_isolated_and_resettable() -> None:
    store = InMemoryStore()
    store.append_turn("bot-1", "sess", _turn("user", "hi"))
    store.append_turn("bot-2", "sess", _turn("assistant", "hey"))

    history = store.get_history("bot-1", "sess")
    history.append(_turn("assistant", "mutated"))

    assert store.get_history("bot-1", "sess") == [_turn("user", "hi")]

    store.reset_history_for_bot("bot-1")

    assert store.get_history("bot-1", "sess") == []
    assert store.get_history("bot-2", "sess") == [_turn("assistant", "hey")]
