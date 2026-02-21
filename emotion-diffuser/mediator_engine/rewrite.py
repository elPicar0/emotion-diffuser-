from .client import call_llm
from .prompts import REWRITE_SYSTEM_PROMPT, APOLOGY_SYSTEM_PROMPT


async def rewrite_message_llm(text: str, analysis=None) -> str:
    user_prompt = f"""
User Message:
{text}
"""

    return await call_llm(
        system_prompt=REWRITE_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )


async def generate_apology_llm(text: str, analysis=None):
    user_prompt = f"""
Original Message:
{text}
"""

    apology_text = await call_llm(
        system_prompt=APOLOGY_SYSTEM_PROMPT,
        user_prompt=user_prompt,
    )

    components = {
        "acknowledgment": "",
        "responsibility": "",
        "remorse": "",
        "repair": "",
        "invitation": "",
    }

    return apology_text, components