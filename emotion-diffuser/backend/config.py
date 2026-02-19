"""
Configuration — environment variables, API keys, model settings, thresholds.
This file prevents secrets and settings from scattering across the project.
"""

import os
from dotenv import load_dotenv

load_dotenv()


# ────────────────────────────────────────
# API Keys
# ────────────────────────────────────────

OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY", "")
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "")

# ────────────────────────────────────────
# Model Configuration
# ────────────────────────────────────────

EMOTION_MODEL: str = os.getenv("EMOTION_MODEL", "j-hartmann/emotion-english-distilroberta-base")
TOXICITY_MODEL: str = os.getenv("TOXICITY_MODEL", "martin-ha/toxic-comment-model")
LLM_MODEL: str = os.getenv("LLM_MODEL", "gpt-3.5-turbo")

# ────────────────────────────────────────
# Thresholds
# ────────────────────────────────────────

# Emotion intensity above this → high risk
HIGH_RISK_THRESHOLD: float = float(os.getenv("HIGH_RISK_THRESHOLD", "0.75"))
# Emotion intensity above this → medium risk
MEDIUM_RISK_THRESHOLD: float = float(os.getenv("MEDIUM_RISK_THRESHOLD", "0.45"))
# Toxicity score above this → flagged as toxic
TOXICITY_THRESHOLD: float = float(os.getenv("TOXICITY_THRESHOLD", "0.6"))
# Engagement score below this → conversation is dying
ENGAGEMENT_LOW_THRESHOLD: float = float(os.getenv("ENGAGEMENT_LOW_THRESHOLD", "0.3"))

# ────────────────────────────────────────
# Feature Flags
# ────────────────────────────────────────

DEBUG: bool = os.getenv("DEBUG", "true").lower() == "true"
ENABLE_APOLOGY: bool = os.getenv("ENABLE_APOLOGY", "true").lower() == "true"
ENABLE_TRIGGERS: bool = os.getenv("ENABLE_TRIGGERS", "true").lower() == "true"
ENABLE_REWRITE: bool = os.getenv("ENABLE_REWRITE", "true").lower() == "true"

# ────────────────────────────────────────
# Server Settings
# ────────────────────────────────────────

API_VERSION: str = "v1"
API_TITLE: str = "Emotion Diffuser API"
API_DESCRIPTION: str = (
    "AI-powered conflict resolution and relationship repair system. "
    "Detects emotions, softens tone, generates heartfelt apologies, "
    "and suggests conversation re-engagement triggers — all backed by psychology research."
)
CORS_ORIGINS: list[str] = os.getenv("CORS_ORIGINS", "http://localhost:3000,http://localhost:8501").split(",")
