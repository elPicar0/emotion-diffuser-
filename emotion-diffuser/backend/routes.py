"""
API Routes — all HTTP endpoints for Emotion Diffuser.
This file ONLY routes requests. No ML logic, no prompts, no business rules.
"""

from fastapi import APIRouter, HTTPException
from backend.schemas import (
    MessageIn,
    ConversationIn,
    FullPipelineIn,
    BatchIn,
    AnalysisOut,
    RewriteOut,
    ApologyOut,
    TriggerOut,
    FullPipelineOut,
    BatchOut,
    ErrorOut,
)
from backend import orchestrator, config

router = APIRouter()


# ────────────────────────────────────────
# HEALTH CHECK
# ────────────────────────────────────────

@router.get("/health", tags=["System"])
async def health_check():
    """Check if the server is running and which features are enabled."""
    return {
        "status": "healthy",
        "version": config.API_VERSION,
        "features": {
            "rewrite": config.ENABLE_REWRITE,
            "apology": config.ENABLE_APOLOGY,
            "triggers": config.ENABLE_TRIGGERS,
        },
        "debug": config.DEBUG,
    }


# ────────────────────────────────────────
# ANALYZE — Emotion + Risk Detection
# ────────────────────────────────────────

@router.post(
    "/analyze",
    response_model=AnalysisOut,
    responses={500: {"model": ErrorOut}},
    tags=["Analysis"],
    summary="Analyze emotion, intensity, and risk level",
)
async def analyze(data: MessageIn):
    """
    Detect the primary emotion, intensity (0-1), risk level (low/medium/high),
    and toxicity in a message.
    """
    try:
        return await orchestrator.analyze_message(data.text, data.context)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────
# REWRITE — Tone Softening
# ────────────────────────────────────────

@router.post(
    "/rewrite",
    response_model=RewriteOut,
    responses={500: {"model": ErrorOut}},
    tags=["Mediation"],
    summary="Rewrite a message with a calmer tone",
)
async def rewrite(data: MessageIn):
    """
    Analyze the message emotion, then produce a calmer,
    more constructive version of the same message.
    """
    try:
        if not config.ENABLE_REWRITE:
            raise HTTPException(status_code=403, detail="Rewrite feature is disabled")
        analysis = await orchestrator.analyze_message(data.text, data.context)
        return await orchestrator.rewrite_message(data.text, analysis, data.relationship)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────
# APOLOGIZE — Heartfelt Apology Generation
# ────────────────────────────────────────

@router.post(
    "/apologize",
    response_model=ApologyOut,
    responses={500: {"model": ErrorOut}},
    tags=["Mediation"],
    summary="Generate a heartfelt, psychology-backed apology",
)
async def apologize(data: MessageIn):
    """
    Generate a genuine apology using the 5-component psychological model.
    """
    try:
        if not config.ENABLE_APOLOGY:
            raise HTTPException(status_code=403, detail="Apology feature is disabled")
        analysis = await orchestrator.analyze_message(data.text, data.context)
        return await orchestrator.generate_apology(data.text, analysis, data.relationship)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────
# TRIGGERS — Conversation Re-Engagement
# ────────────────────────────────────────

@router.post(
    "/triggers",
    response_model=TriggerOut,
    responses={500: {"model": ErrorOut}},
    tags=["Engagement"],
    summary="Detect conversation disengagement and suggest re-engagement triggers",
)
async def triggers(data: ConversationIn):
    """
    Analyze a conversation for disengagement signals and suggest
    psychology-backed re-engagement strategies.
    """
    try:
        if not config.ENABLE_TRIGGERS:
            raise HTTPException(status_code=403, detail="Triggers feature is disabled")
        return await orchestrator.detect_triggers(data.messages, data.context, data.relationship)
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# ────────────────────────────────────────
# PIPELINE — Everything In One Call
# ────────────────────────────────────────

@router.post(
    "/pipeline",
    response_model=FullPipelineOut,
    responses={500: {"model": ErrorOut}},
    tags=["Pipeline"],
    summary="Run the full Emotion Diffuser pipeline in one call",
)
async def pipeline(data: FullPipelineIn):
    """
    Run analysis + rewrite + apology + triggers in a single request.
    Toggle outputs with include_rewrite, include_apology, include_triggers.
    """
    try:
        return await orchestrator.full_pipeline(
            text=data.text,
            context=data.context,
            relationship=data.relationship,
            include_rewrite=data.include_rewrite,
            include_apology=data.include_apology,
            include_triggers=data.include_triggers,
            conversation_history=data.conversation_history,
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



# ────────────────────────────────────────
# BATCH — Analyze Multiple Messages
# ────────────────────────────────────────

@router.post(
    "/batch",
    response_model=BatchOut,
    responses={500: {"model": ErrorOut}},
    tags=["Analysis"],
    summary="Analyze multiple messages at once",
)
async def batch_analyze(data: BatchIn):
    """
    Process a batch of messages and return analysis results for each.
    Useful for analyzing an entire conversation history.
    """
    try:
        results = []
        for msg in data.messages:
            result = await orchestrator.analyze_message(msg.text, msg.context)
            results.append(result)
        return BatchOut(results=results, count=len(results))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
