"""
Orchestrator — the system brain that connects analysis + mediation engines.
Currently returns STUB data so the API works immediately.
Replace stubs with real ML calls during integration phase.
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


# ────────────────────────────────────────
# ANALYZE
# ────────────────────────────────────────

async def analyze_message(text: str, context: str | None = None) -> AnalysisOut:
    """
    Analyze a message for emotion, intensity, risk, and toxicity.
    STUB — returns mock data. Will call analysis_engine.analyzer later.
    """
    text_lower = text.lower()

    # Simple keyword-based mock logic
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
# REWRITE
# ────────────────────────────────────────

async def rewrite_message(text: str, analysis: AnalysisOut | None = None) -> RewriteOut:
    """
    Rewrite a message with a calmer, constructive tone.
    STUB — returns mock rewrite. Will call mediator_engine.rewrite later.
    """
    emotion = analysis.emotion if analysis else "unknown"

    mock_rewrites = {
        "anger": f"I'd like to share how I feel about this situation calmly. {text.replace('!', '.')}",
        "sadness": f"I want you to understand that this is affecting me. {text}",
        "fear": f"I'm feeling uncertain about this and would appreciate your support. {text}",
    }

    rewritten = mock_rewrites.get(emotion, f"I'd like to express my thoughts constructively: {text}")

    return RewriteOut(
        original=text,
        rewritten=rewritten,
        tone="calm",
        emotion=emotion,
    )


# ────────────────────────────────────────
# APOLOGY (5-Component Psychology Model)
# ────────────────────────────────────────

async def generate_apology(text: str, analysis: AnalysisOut | None = None) -> ApologyOut:
    """
    Generate a heartfelt apology using the 5-component psychological model.
    STUB — returns mock apology. Will call mediator_engine.rewrite.generate_apology later.
    """
    components = ApologyComponents(
        acknowledgment=f"I realize that what I said was hurtful, and I understand the impact it had on you.",
        responsibility="That was entirely my fault. I take full responsibility for my words and actions.",
        remorse="I genuinely feel bad about how I handled the situation, and I'm sorry for the pain I caused.",
        repair="Going forward, I will be more mindful of my tone and think before I speak, especially when emotions are high.",
        invitation="I understand if you need time, but I want you to know I'm here whenever you're ready to talk.",
    )

    full_apology = (
        f"{components.acknowledgment} "
        f"{components.responsibility} "
        f"{components.remorse} "
        f"{components.repair} "
        f"{components.invitation}"
    )

    return ApologyOut(
        original=text,
        apology=full_apology,
        tone="empathetic",
        repair_type="acknowledgment + ownership + remorse + repair + invitation",
        components=components,
    )


# ────────────────────────────────────────
# TRIGGERS (Conversation Re-Engagement)
# ────────────────────────────────────────

async def detect_triggers(messages: list[str], context: str | None = None) -> TriggerOut:
    """
    Analyze a conversation for disengagement and suggest re-engagement triggers.
    STUB — returns mock triggers. Will call analysis_engine.analyzer later.
    """
    signals = []
    short_count = sum(1 for m in messages if len(m.split()) <= 3)
    question_count = sum(1 for m in messages if "?" in m)

    if short_count > len(messages) * 0.5:
        signals.append("short_responses")
    if question_count == 0:
        signals.append("no_questions")
    if len(set(messages)) < len(messages) * 0.7:
        signals.append("repetitive_content")

    if len(signals) >= 2:
        engagement = "low"
    elif len(signals) == 1:
        engagement = "medium"
    else:
        engagement = "high"

    suggested = []
    if engagement != "high":
        suggested = [
            SuggestedTrigger(
                strategy="curiosity_gap",
                suggestion="Something happened today that completely changed how I think about this — have you heard about it?",
                psychology="Loewenstein's Information Gap Theory (1994)",
            ),
            SuggestedTrigger(
                strategy="reciprocity_hook",
                suggestion="I've been meaning to ask you something — you're honestly the only person whose opinion I trust on this.",
                psychology="Cialdini's Principle of Reciprocity (1984)",
            ),
            SuggestedTrigger(
                strategy="open_ended_pivot",
                suggestion="What's been on your mind lately? I feel like we haven't really talked in a while.",
                psychology="Motivational Interviewing (Miller & Rollnick, 2002)",
            ),
        ]

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
    include_rewrite: bool = True,
    include_apology: bool = True,
    include_triggers: bool = False,
    conversation_history: list[str] | None = None,
) -> FullPipelineOut:
    """
    Run the complete Emotion Diffuser pipeline.
    Calls analyze → rewrite → apology → triggers based on flags.
    """
    # Step 1: Always analyze
    analysis = await analyze_message(text, context)

    # Step 2: Rewrite if requested
    rewrite = None
    if include_rewrite and config.ENABLE_REWRITE:
        rewrite = await rewrite_message(text, analysis)

    # Step 3: Apology if requested
    apology = None
    if include_apology and config.ENABLE_APOLOGY:
        apology = await generate_apology(text, analysis)

    # Step 4: Triggers if requested and history provided
    triggers = None
    if include_triggers and config.ENABLE_TRIGGERS and conversation_history:
        triggers = await detect_triggers(conversation_history, context)

    return FullPipelineOut(
        analysis=analysis,
        rewrite=rewrite,
        apology=apology,
        triggers=triggers,
    )
