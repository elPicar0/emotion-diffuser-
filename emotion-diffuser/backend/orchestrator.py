"""
Orchestrator — connects analysis + mediation engines.
Now wired to real mediator_engine instead of stubs.
"""

from backend.schemas import (
    AnalysisOut,
    EmotionDetail,
    RewriteOut,
    ApologyOut,
    ApologyComponents,
    TriggerOut,
    SuggestedTrigger,
    FullPipelineOut,
)
from backend import config

# ✅ Correct imports (NO emotion_diffuser prefix)
from mediator_engine.rewrite import rewrite_message_llm, generate_apology_llm


# ────────────────────────────────────────
# ANALYZE (still stub for now)
# ────────────────────────────────────────

async def analyze_message(text: str, context: str | None = None) -> AnalysisOut:
    text_lower = text.lower()

    if any(word in text_lower for word in ["angry", "hate", "furious", "rage", "yell"]):
        emotion, intensity, risk = "anger", 0.85, "high"
    elif any(word in text_lower for word in ["sad", "cry", "depressed", "hurt", "pain"]):
        emotion, intensity, risk = "sadness", 0.72, "medium"
    elif any(word in text_lower for word in ["happy", "great", "love", "wonderful", "amazing"]):
        emotion, intensity, risk = "joy", 0.80, "low"
    elif any(word in text_lower for word in ["scared", "afraid", "anxious", "worried", "fear"]):
        emotion, intensity, risk = "fear", 0.65, "medium"
    else:
        emotion, intensity, risk = "neutral", 0.30, "low"

    is_toxic = any(word in text_lower for word in ["idiot", "stupid", "shut up", "hate you", "dumb"])
    toxicity_score = 0.88 if is_toxic else 0.05

    return AnalysisOut(
        emotion=emotion,
        intensity=intensity,
        risk=risk,
        is_toxic=is_toxic,
        toxicity_score=toxicity_score,
        all_emotions=[
            EmotionDetail(label=emotion, score=intensity),
            EmotionDetail(label="neutral", score=round(1 - intensity, 2)),
        ],
    )


# ────────────────────────────────────────
# REWRITE (real mediator_engine call)
# ────────────────────────────────────────

async def rewrite_message(text: str, analysis: AnalysisOut | None = None) -> RewriteOut:
    rewritten = await rewrite_message_llm(text, analysis)

    return RewriteOut(
        original=text,
        rewritten=rewritten,
        tone="calm",
        emotion=analysis.emotion if analysis else "unknown",
    )


# ────────────────────────────────────────
# APOLOGY (real mediator_engine call)
# ────────────────────────────────────────

async def generate_apology(text: str, analysis: AnalysisOut | None = None) -> ApologyOut:
    apology_text, components = await generate_apology_llm(text, analysis)

    return ApologyOut(
        original=text,
        apology=apology_text,
        tone="empathetic",
        repair_type="acknowledgment + ownership + remorse + repair + invitation",
        components=ApologyComponents(**components),
    )


# ────────────────────────────────────────
# TRIGGERS (still stub)
# ────────────────────────────────────────

async def detect_triggers(messages: list[str], context: str | None = None) -> TriggerOut:
    signals = []
    short_count = sum(1 for m in messages if len(m.split()) <= 3)
    question_count = sum(1 for m in messages if "?" in m)

    if short_count > len(messages) * 0.5:
        signals.append("short_responses")
    if question_count == 0:
        signals.append("no_questions")

    engagement = "low" if len(signals) >= 2 else "medium" if signals else "high"

    return TriggerOut(
        engagement_level=engagement,
        signals_detected=signals,
        suggested_triggers=[],
    )


# ────────────────────────────────────────
# FULL PIPELINE
# ────────────────────────────────────────

async def full_pipeline(
    text: str,
    context: str | None = None,
    include_rewrite: bool = True,
    include_apology: bool = True,
    include_triggers: bool = False,
    conversation_history: list[str] | None = None,
) -> FullPipelineOut:

    analysis = await analyze_message(text, context)

    rewrite = None
    if include_rewrite and config.ENABLE_REWRITE:
        rewrite = await rewrite_message(text, analysis)

    apology = None
    if include_apology and config.ENABLE_APOLOGY:
        apology = await generate_apology(text, analysis)

    triggers = None
    if include_triggers and config.ENABLE_TRIGGERS and conversation_history:
        triggers = await detect_triggers(conversation_history, context)

    return FullPipelineOut(
        analysis=analysis,
        rewrite=rewrite,
        apology=apology,
        triggers=triggers,
    )