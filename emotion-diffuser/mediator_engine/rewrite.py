"""
Rewrite & Apology Logic

This file:
- Builds prompts
- Calls the LLM client
- Returns generated text

No model loading here.
"""

from .client import generate
from .prompts import REWRITE_SYSTEM_PROMPT, APOLOGY_SYSTEM_PROMPT


def rewrite_message(text: str) -> str:
    """
    Rewrite emotionally charged text into calm, constructive communication.
    """

    prompt = f"""
{REWRITE_SYSTEM_PROMPT}

Original Message:
{text}

Rewritten Message:
"""

    return generate(prompt)


def generate_apology(text: str) -> str:
    """
    Generate a structured 5-component apology.
    """

    prompt = f"""
{APOLOGY_SYSTEM_PROMPT}

Original Message:
{text}

Apology:
"""

    return generate(prompt, max_tokens=300)
