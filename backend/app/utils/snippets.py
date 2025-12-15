"""Generate copy-paste ready code snippets for embedding bots."""
from __future__ import annotations

import json
from textwrap import dedent

from app.core.config import get_settings
from app.models.bot import BotBlueprint, BotSnippetResponse, SnippetLanguage

settings = get_settings()


def _python_template(blueprint: BotBlueprint) -> str:
    safe_fn = blueprint.bot_id.replace("-", "_")
    model_name = getattr(settings, "gemini_model", "gemini-2.0-flash")
    template = """
import os
import google.generativeai as genai

GEMINI_MODEL = os.getenv("GEMINI_MODEL", "{model_name}")
SYSTEM_PROMPT = {system_prompt}


def init_model():
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("Missing GEMINI_API_KEY")
    genai.configure(api_key=api_key)
    return genai.GenerativeModel(GEMINI_MODEL)


def ask_{safe_fn}(message, history=None):
    history = history or []
    model = init_model()
    system_header = "System: {bot_name} | {tagline}"
    compiled_prompt = "\n".join([
        system_header,
        SYSTEM_PROMPT,
        *history,
        f"User: {{message}}",
    ])
    response = model.generate_content(compiled_prompt)
    return response.text.strip()


if __name__ == "__main__":
    print(ask_{safe_fn}("Hi there! What can you do?"))
"""
    return dedent(template).strip().format(
        model_name=model_name,
        system_prompt=json.dumps(blueprint.system_prompt),
        bot_name=blueprint.bot_name.replace("\"", "'"),
        tagline=blueprint.tagline.replace("\"", "'"),
        safe_fn=safe_fn,
    )


def _javascript_template(blueprint: BotBlueprint) -> str:
    export_name = f"ask{blueprint.bot_id.replace('-', '').title()}"
    model_name = getattr(settings, "gemini_model", "gemini-2.0-flash")
    template = """
import 'dotenv/config';
import {{ GoogleGenerativeAI }} from "@google/generative-ai";

const modelName = process.env.GEMINI_MODEL || "{model_name}";
const systemPrompt = {system_prompt};

function initModel() {{
    const apiKey = process.env.GEMINI_API_KEY;
    if (!apiKey) throw new Error('Missing GEMINI_API_KEY');
    const genAI = new GoogleGenerativeAI(apiKey);
    return genAI.getGenerativeModel({{ model: modelName }});
}}

export async function {export_name}(message, history = []) {{
    const model = initModel();
    const compiledPrompt = [
        "System: {bot_name} | {tagline}",
        systemPrompt,
        ...history,
        `User: ${{message}}`,
    ].join('\n');
    const result = await model.generateContent(compiledPrompt);
    return result.response.text().trim();
}}
"""
    return (
        dedent(template)
        .strip()
        .format(
            model_name=model_name,
            system_prompt=json.dumps(blueprint.system_prompt),
            bot_name=blueprint.bot_name.replace("\"", "'"),
            tagline=blueprint.tagline.replace("\"", "'"),
            export_name=export_name,
        )
    )


def build_snippet_payload(blueprint: BotBlueprint, language: SnippetLanguage) -> BotSnippetResponse:
    code = _python_template(blueprint) if language == "py" else _javascript_template(blueprint)
    instructions = (
        "Set GEMINI_API_KEY (and optionally GEMINI_MODEL), install google-generativeai, then copy this snippet into your project."
        if language == "py"
        else "Install @google/generative-ai and dotenv, set GEMINI_API_KEY, then import the exported function."
    )
    return BotSnippetResponse(
        bot_id=blueprint.bot_id,
        language=language,
        code=code,
        instructions=instructions,
    )
