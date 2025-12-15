"""Prompt templates for the Bot Factory flows."""
from __future__ import annotations

from typing import Iterable

from app.models.bot import BotBlueprint, ChatTurn


BLUEPRINT_PROMPT_TEMPLATE = """You are an expert AI product designer.
Given the following business context, craft a detailed persona and system prompt for a
custom chatbot. Respond ONLY with minified JSON following this schema:
{{
  "bot_name": "string",
  "tagline": "string",
  "tone": "string",
  "language": "string",
  "knowledge_base": ["string"],
  "system_prompt": "string",
  "sample_questions": ["string"],
  "sample_responses": ["string"]
}}
Avoid markdown fences. Be concise but vivid.

Business name: {business_name}
Business description: {business_description}
Desired bot role: {desired_bot_role}
Target audience: {target_audience}
Preferred tone: {preferred_tone}
Preferred language: {preferred_language}
"""


PLAYGROUND_PROMPT_TEMPLATE = """You are now acting as {bot_name}, a bespoke AI assistant.
Persona mission: {tagline}
Tone of voice: {tone}
Language: {language}

System instructions:
{system_prompt}

Conversation so far:
{history}

Latest user message:
{user_message}

Guidelines:
- Respond naturally in {language}.
- Maintain the persona above.
- Offer concrete suggestions or questions that move the user toward their goal.
- Keep responses under 180 words unless the user explicitly requests more detail.
"""


def build_blueprint_prompt(**kwargs: str) -> str:
    """Create the prompt for the blueprint generation call."""
    return BLUEPRINT_PROMPT_TEMPLATE.format(**kwargs)


def _format_history(bot: BotBlueprint, turns: Iterable[ChatTurn]) -> str:
    rendered = []
    for turn in turns:
        speaker = "User" if turn.role == "user" else bot.bot_name
        rendered.append(f"{speaker}: {turn.content}")
    return "\n".join(rendered) if rendered else "(no previous messages)"


def build_playground_prompt(bot: BotBlueprint, turns: Iterable[ChatTurn], user_message: str) -> str:
    """Create the full prompt for the Playground chat call."""
    history = _format_history(bot, turns)
    return PLAYGROUND_PROMPT_TEMPLATE.format(
        bot_name=bot.bot_name,
        tagline=bot.tagline,
        tone=bot.tone,
        language=bot.language,
        system_prompt=bot.system_prompt,
        history=history,
        user_message=user_message,
    )
