from app.models.bot import BotBlueprint, ChatTurn
from app.utils import prompts


def _blueprint() -> BotBlueprint:
    return BotBlueprint(
        bot_id="bot-9",
        bot_name="Chef Nova",
        tagline="Makes every dinner sparkle",
        tone="excited",
        language="en",
        knowledge_base=["menu"],
        system_prompt="Cook boldly",
        sample_questions=["What pairs with salmon?"],
        sample_responses=["Try citrus"],
    )


def test_build_blueprint_prompt_injects_details():
    prompt_text = prompts.build_blueprint_prompt(
        business_name="Nova",
        business_description="We sell futuristic dining experiences.",
        desired_bot_role="Plan meals",
        target_audience="Home chefs",
        preferred_tone="excited",
        preferred_language="en",
    )

    assert "futuristic dining" in prompt_text
    assert "Preferred language: en" in prompt_text


def test_build_playground_prompt_handles_empty_history():
    blueprint = _blueprint()
    prompt_text = prompts.build_playground_prompt(blueprint, [], "Hello")

    assert "(no previous messages)" in prompt_text
    assert "Hello" in prompt_text


def test_build_playground_prompt_renders_turns():
    blueprint = _blueprint()
    turns = [
        ChatTurn(role="user", content="Hi"),
        ChatTurn(role="assistant", content="Welcome"),
    ]

    prompt_text = prompts.build_playground_prompt(blueprint, turns, "Next")

    assert "User: Hi" in prompt_text
    assert f"{blueprint.bot_name}: Welcome" in prompt_text
