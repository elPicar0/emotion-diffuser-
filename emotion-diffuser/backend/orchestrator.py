"""
Orchestrator — connects analysis + mediation engines.
Now wired to real mediator_engine and analysis_engine.
"""

from backend.schemas import (
    AnalysisOut,
    RewriteOut,
    ApologyOut,
    ApologyComponents,
    TriggerOut,
    SuggestedTrigger,
    FullPipelineOut,
)
from backend import config

# ✅ Real imports
from mediator_engine.rewrite import rewrite_message_llm, generate_apology_llm
from mediator_engine.prompts import SUGGESTED_TRIGGERS
from analysis_engine.analyzer import analyze_text
from analysis_engine.utils import detect_disengagement_signals


# ────────────────────────────────────────
# ANALYZE (Now using real analysis_engine)
# ────────────────────────────────────────

async def analyze_message(text: str, context: str | None = None) -> AnalysisOut:
    """
    Detect primary emotion, intensity, and risk level using HuggingFace models.
    """
    return await analyze_text(text, context)


# ────────────────────────────────────────
# REWRITE
# ────────────────────────────────────────

async def rewrite_message(
    text: str, analysis: AnalysisOut | None = None, relationship: str = "neutral"
) -> RewriteOut:
    """
    Produce a calmer, constructive version of a message using the LLM.
    """
    rewritten = await rewrite_message_llm(text, analysis, relationship)

    return RewriteOut(
        original=text,
        rewritten=rewritten,
        tone="calm",
        emotion=analysis.emotion if analysis else "unknown",
    )


# ────────────────────────────────────────
# APOLOGY
# ────────────────────────────────────────

async def generate_apology(
    text: str, analysis: AnalysisOut | None = None, relationship: str = "neutral"
) -> ApologyOut:
    """
    Generate a 5-component psychological apology using the LLM.
    """
    apology_text, components = await generate_apology_llm(text, analysis, relationship)

    return ApologyOut(
        original=text,
        apology=apology_text,
        tone="empathetic",
        repair_type="acknowledgment + ownership + remorse + repair + invitation",
        components=ApologyComponents(**components),
    )


# ────────────────────────────────────────
# TRIGGERS
# ────────────────────────────────────────

async def detect_triggers(
    messages: list[str], context: str | None = None, relationship: str = "neutral"
) -> TriggerOut:
    """
    Analyze a conversation for disengagement and suggest psychology-backed triggers.
    Triggers are relationship-specific.
    """
    signals = detect_disengagement_signals(messages)

    engagement = "low" if len(signals) >= 2 else "medium" if signals else "high"

    suggested = []
    if engagement != "high":
        # Pull mode-specific triggers, fallback to neutral
        mode_triggers = SUGGESTED_TRIGGERS.get(relationship.lower(), SUGGESTED_TRIGGERS["neutral"])
        suggested = [SuggestedTrigger(**t) for t in mode_triggers]

    return TriggerOut(
        engagement_level=engagement,
        signals_detected=signals,
        suggested_triggers=suggested,
    )


# ────────────────────────────────────────
# FULL PIPELINE
# ────────────────────────────────────────

async def full_pipeline(
    text: str,
    context: str | None = None,
    relationship: str = "neutral",
    include_rewrite: bool = True,
    include_apology: bool = True,
    include_triggers: bool = False,
    conversation_history: list[str] | None = None,
) -> FullPipelineOut:
    """
    Run analysis → rewrite → apology → triggers in a single unified flow.
    """
    analysis = await analyze_message(text, context)

    rewrite = None
    if include_rewrite and config.ENABLE_REWRITE:
        rewrite = await rewrite_message(text, analysis, relationship)

    apology = None
    if include_apology and config.ENABLE_APOLOGY:
        apology = await generate_apology(text, analysis, relationship)

    triggers = None
    if include_triggers and config.ENABLE_TRIGGERS and conversation_history:
        triggers = await detect_triggers(conversation_history, context, relationship)

    return FullPipelineOut(
        analysis=analysis,
        rewrite=rewrite,
        apology=apology,
        triggers=triggers,
    )
