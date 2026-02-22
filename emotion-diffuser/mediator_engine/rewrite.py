"""
LLM-powered message rewriting and apology generation.
"""

import json
import logging

from .client import call_llm
from .prompts import (
    REWRITE_SYSTEM_PROMPT, 
    REWRITE_USER_PROMPT, 
    APOLOGY_SYSTEM_PROMPT, 
    APOLOGY_USER_PROMPT, 
    TONE_RULES
)

logger = logging.getLogger(__name__)

# Fallback component values when JSON parsing fails
_EMPTY_COMPONENTS: dict[str, str] = {
    "acknowledgment": "",
    "responsibility": "",
    "remorse": "",
    "repair": "",
    "invitation": "",
}


def _get_tone_requirement(relationship: str = "neutral") -> str:
    """Get the specific tone requirement based on the relationship."""
    return TONE_RULES.get(relationship.lower(), TONE_RULES["neutral"])


async def rewrite_message_llm(text: str, analysis=None, relationship: str = "neutral") -> str:
    """Rewrite a message to be calmer and more constructive via the LLM."""
    tone_requirement = _get_tone_requirement(relationship)
    
    emotion_hint = ""
    if analysis:
        emotion_hint = f"\nDetected emotion: {analysis.emotion} (intensity {analysis.intensity})"

    user_prompt = REWRITE_USER_PROMPT.format(text=text, emotion_hint=emotion_hint)
    system_prompt = REWRITE_SYSTEM_PROMPT.format(tone_requirement=tone_requirement)

    return await call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )


async def generate_apology_llm(
    text: str, analysis=None, relationship: str = "neutral"
) -> tuple[str, dict[str, str]]:
    """
    Generate a structured apology via the LLM.

    Returns
    -------
    tuple[str, dict]
        (full_apology_text, components_dict) where components_dict has
        keys: acknowledgment, responsibility, remorse, repair, invitation.
    """
    tone_requirement = _get_tone_requirement(relationship)

    emotion_hint = ""
    if analysis:
        emotion_hint = f"\nDetected emotion: {analysis.emotion} (intensity {analysis.intensity})"

    user_prompt = APOLOGY_USER_PROMPT.format(text=text, emotion_hint=emotion_hint)
    system_prompt = APOLOGY_SYSTEM_PROMPT.format(tone_requirement=tone_requirement)

    raw = await call_llm(
        system_prompt=system_prompt,
        user_prompt=user_prompt,
    )

    # --- Parse structured JSON from the LLM response ---
    try:
        # LLM might sometimes include markdown code blocks
        clean_raw = raw.strip()
        if clean_raw.startswith("```"):
            clean_raw = clean_raw.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
            if clean_raw.startswith("json"):
                clean_raw = clean_raw[4:].strip()
                
        components = json.loads(clean_raw)
        # Validate expected keys are present
        for key in _EMPTY_COMPONENTS:
            components.setdefault(key, "")
    except (json.JSONDecodeError, TypeError, IndexError):
        logger.warning(f"Apology LLM did not return valid JSON — using raw text: {raw[:100]}...")
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