"""
Model Loading Layer — abstracts HuggingFace pipeline initialization.
Caches models globally to avoid redundant loading.
"""

from transformers import pipeline
from backend import config

# Global cache for pipelines
_emotion_pipe = None
_toxicity_pipe = None

def get_emotion_pipeline():
    """Returns the singleton emotion classification pipeline."""
    global _emotion_pipe
    if _emotion_pipe is None:
        print(f"[LOAD] Loading emotion model: {config.EMOTION_MODEL}...")
        _emotion_pipe = pipeline(
            "text-classification",
            model=config.EMOTION_MODEL,
            top_k=None  # Return all scores
        )
    return _emotion_pipe

def get_toxicity_pipeline():
    """Returns the singleton toxicity classification pipeline."""
    global _toxicity_pipe
    if _toxicity_pipe is None:
        print(f"[LOAD] Loading toxicity model: {config.TOXICITY_MODEL}...")
        _toxicity_pipe = pipeline(
            "text-classification",
            model=config.TOXICITY_MODEL
        )
    return _toxicity_pipe
