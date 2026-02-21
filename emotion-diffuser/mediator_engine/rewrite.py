"""
LLM-powered message rewriting and apology generation.
"""

import json
import logging

from .client import call_llm
from .prompts import REWRITE_SYSTEM_PROMPT, APOLOGY_SYSTEM_PROMPT

logger = logging.getLogger(__name__)

# Fallback component values when JSON parsing fails
_EMPTY_COMPONENTS: dict[str, str] = {
    "acknowledgment": "",
    "responsibility": "",
    "remorse": "",
    "repair": "",
    "invitation": "",
}


async def rewrite_message_llm(text: str, analysis=None) -> str:
    """Rewrite a message to be calmer and more constructive via the LLM."""
    emotion_hint = ""
    if analysis:
        emotion_hint = f"\nDetected emotion: {analysis.emotion} (intensity {analysis.intensity})"

    user_prompt = f"""\
User Message:
{text}
{emotion_hint}"""

    return await call_llm(
        system_prompt=REWRITE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )


async def generate_apology_llm(
    text: str, analysis=None
) -> tuple[str, dict[str, str]]:
    """
    Generate a structured apology via the LLM.

    Returns
    -------
    tuple[str, dict]
        (full_apology_text, components_dict) where components_dict has
        keys: acknowledgment, responsibility, remorse, repair, invitation.
    """
    emotion_hint = ""
    if analysis:
        emotion_hint = f"\nDetected emotion: {analysis.emotion} (intensity {analysis.intensity})"

    user_prompt = f"""\
Original Message:
{text}
{emotion_hint}"""

    raw = await call_llm(
        system_prompt=APOLOGY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    # --- Parse structured JSON from the LLM response ---
    try:
        components = json.loads(raw)
        # Validate expected keys are present
        for key in _EMPTY_COMPONENTS:
            components.setdefault(key, "")
    except (json.JSONDecodeError, TypeError):
        logger.warning("Apology LLM did not return valid JSON — using raw text.")
        components = dict(_EMPTY_COMPONENTS)

    # Build a natural full-text apology from the components
    full_apology = " ".join(
        v for v in [
            components.get("acknowledgment", ""),
            components.get("responsibility", ""),
            components.get("remorse", ""),
            components.get("repair", ""),
            components.get("invitation", ""),
        ]
        if v
    )

    # If components parsed but the joined text is empty, fall back to raw
    if not full_apology.strip():
        full_apology = raw

    return full_apology, components