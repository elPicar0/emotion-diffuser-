"""
OpenAI client — singleton async client and LLM helper.
"""

from typing import Optional
from openai import AsyncOpenAI
from backend import config

_client: Optional[AsyncOpenAI] = None


def get_client() -> AsyncOpenAI:
    """Return (or create) the singleton AsyncOpenAI client."""
    global _client

    if _client is None:
        if not config.OPENAI_API_KEY:
            raise RuntimeError("OPENAI_API_KEY not set in environment.")

        _client = AsyncOpenAI(api_key=config.OPENAI_API_KEY)

    return _client


async def call_llm(
    system_prompt: str,
    user_prompt: str,
    model: str = config.LLM_MODEL,
    temperature: float = 0.7,
) -> str:
    """Send a system + user prompt to the configured LLM and return the text response."""
    client = get_client()

    response = await client.chat.completions.create(
        model=model,
        temperature=temperature,
        messages=[
            {"role": "system", "content": system_prompt.strip()},
            {"role": "user", "content": user_prompt.strip()},
        ],
    )

    return response.choices[0].message.content.strip()
