"""
Mediator Engine Client

Responsible for:
- Loading the LLM
- Running text generation
- Returning clean string output

This file is the ONLY place that talks to the model.
"""

from transformers import pipeline
from functools import lru_cache


MODEL_NAME = "google/flan-t5-base"


@lru_cache
def get_generator():
    """
    Load and cache the text generation pipeline.
    Ensures model loads only once.
    """
    return pipeline(
        "text2text-generation",
        model=MODEL_NAME,
        device=-1  # CPU (safe for hackathon/demo environments)
    )


def generate(prompt: str, max_tokens: int = 256) -> str:
    """
    Generate text from the model given a prompt.
    """
    generator = get_generator()

    output = generator(
        prompt,
        max_length=max_tokens,
        do_sample=True,
        temperature=0.7,
    )

    return output[0]["generated_text"].strip()
