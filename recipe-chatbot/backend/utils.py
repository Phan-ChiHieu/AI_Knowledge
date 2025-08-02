from __future__ import annotations

"""Utility helpers for the recipe chatbot backend.

This module centralises the system prompt, environment loading, and the
wrapper around litellm so the rest of the application stays decluttered.
"""

import os
from typing import Final, List, Dict

import litellm  # type: ignore
from dotenv import load_dotenv

# Ensure the .env file is loaded as early as possible.
load_dotenv(override=False)

# --- Constants -------------------------------------------------------------------

# base
# SYSTEM_PROMPT: Final[str] = (
#     "You are an expert chef recommending delicious and useful recipes. "
#     "Present only one recipe at a time. If the user doesn't specify what ingredients "
#     "they have available, assume only basic ingredients are available."
#     "Be descriptive in the steps of the recipe, so it is easy to follow."
#     "Have variety in your recipes, don't just recommend the same thing over and over."
#     "You MUST suggest a complete recipe; don't ask follow-up questions."
#     "Mention the serving size in the recipe. If not specified, assume 2 people."
# )

# custom
SYSTEM_PROMPT: Final[str] = (
    "You are a friendly and creative culinary assistant. Your role is to help users find, understand, and execute recipes that are easy to follow, practical, and enjoyable.\n\n"
    "Always:\n"
    "- Provide an enticing title as a Level 2 Markdown heading (## Title of Recipe).\n"
    "- Follow with a 1-3 sentence engaging description.\n"
    "- Use Markdown formatting throughout your response.\n"
    "- Include three sections in order:\n"
    "    1. ### Ingredients — Use bullet points (*).\n"
    "    2. ### Instructions — Use numbered steps (1., 2., 3., ...).\n"
    "    3. Optional: Add ### Tips, ### Variations, or ### Notes if relevant.\n\n"
    "Never:\n"
    "- Recommend ingredients that are rare, expensive, or hard to find unless you give accessible alternatives.\n"
    "- Use offensive, derogatory, or culturally insensitive language.\n"
    "- Suggest unsafe, unethical, or harmful recipes. Politely decline if the request is inappropriate.\n\n"
    "Creativity:\n"
    "- You may suggest common variations or substitutions.\n"
    "- If no exact recipe exists, you may creatively combine known recipes, but clearly say so.\n"
    "- Feel free to invent new recipes — just make sure to flag them as original creations.\n\n"
    "Your tone should be friendly, concise, and informative. Responses must be structured, well-formatted, and helpful to home cooks of all skill levels."
)


# Fetch configuration *after* we loaded the .env file.
MODEL_NAME: Final[str] = os.environ.get("MODEL_NAME", "gpt-4o-mini")


# --- Agent wrapper ---------------------------------------------------------------


def get_agent_response(
    messages: List[Dict[str, str]],
) -> List[Dict[str, str]]:  # noqa: WPS231
    """Call the underlying large-language model via *litellm*.

    Parameters
    ----------
    messages:
        The full conversation history. Each item is a dict with "role" and "content".

    Returns
    -------
    List[Dict[str, str]]
        The updated conversation history, including the assistant's new reply.
    """

    # litellm is model-agnostic; we only need to supply the model name and key.
    # The first message is assumed to be the system prompt if not explicitly provided
    # or if the history is empty. We'll ensure the system prompt is always first.
    current_messages: List[Dict[str, str]]
    if not messages or messages[0]["role"] != "system":
        current_messages = [{"role": "system", "content": SYSTEM_PROMPT}] + messages
    else:
        current_messages = messages

    completion = litellm.completion(
        model=MODEL_NAME,
        messages=current_messages,  # Pass the full history
    )

    assistant_reply_content: str = completion["choices"][0]["message"][
        "content"
    ].strip()  # type: ignore[index]

    # Append assistant's response to the history
    updated_messages = current_messages + [
        {"role": "assistant", "content": assistant_reply_content}
    ]
    return updated_messages
