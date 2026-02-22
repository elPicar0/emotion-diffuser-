"""
Pydantic schemas — the JSON contracts for the entire Emotion Diffuser API.
Every team member builds against these structures.
"""

from pydantic import BaseModel, Field
from typing import Optional


# ────────────────────────────────────────
# INPUTS
# ────────────────────────────────────────

class MessageIn(BaseModel):
    """Single message for analysis, rewrite, or apology."""
    text: str = Field(..., min_length=1, description="The message text to process")
    context: Optional[str] = Field(None, description="Optional context (e.g. 'argument with friend')")
    sender_name: Optional[str] = Field(None, description="Optional sender name for personalization")
    relationship: str = Field("neutral", description="Relationship with recipient (parent, friend, partner, professional, etc.)")



class ConversationIn(BaseModel):
    """Multiple messages for engagement/trigger analysis."""
    messages: list[str] = Field(..., min_length=1, description="List of messages in conversation order")
    context: Optional[str] = Field(None, description="Optional context about the conversation")
    relationship: str = Field("neutral", description="Relationship with recipient (parent, sibling, friend, partner, professional)")


class FullPipelineIn(BaseModel):
    """Full pipeline request — toggle which outputs you want."""
    text: str = Field(..., min_length=1, description="The message text to process")
    context: Optional[str] = Field(None, description="Optional context")
    relationship: str = Field("neutral", description="Relationship with recipient")
    include_rewrite: bool = Field(True, description="Include calm rewrite in response")
    include_apology: bool = Field(True, description="Include heartfelt apology in response")
    include_triggers: bool = Field(False, description="Include re-engagement triggers")
    conversation_history: Optional[list[str]] = Field(None, description="Previous messages (needed if include_triggers=True)")



class BatchIn(BaseModel):
    """Batch processing — analyze multiple messages at once."""
    messages: list[MessageIn] = Field(..., min_length=1, description="List of messages to analyze")


# ────────────────────────────────────────
# OUTPUTS — Individual Components
# ────────────────────────────────────────

class EmotionDetail(BaseModel):
    """A single emotion with its confidence score."""
    label: str = Field(..., description="Emotion label (anger, joy, sadness, etc.)")
    score: float = Field(..., ge=0, le=1, description="Confidence score 0-1")


class AnalysisOut(BaseModel):
    """Emotion analysis result."""
    emotion: str = Field(..., description="Primary detected emotion")
    intensity: float = Field(..., ge=0, le=1, description="Emotion intensity 0-1")
    risk: str = Field(..., description="Risk level: low, medium, or high")
    is_toxic: bool = Field(False, description="Whether toxicity was detected")
    toxicity_score: float = Field(0.0, ge=0, le=1, description="Toxicity confidence 0-1")
    all_emotions: Optional[list[EmotionDetail]] = Field(None, description="All detected emotions with scores")


class RewriteOut(BaseModel):
    """Tone-softened rewrite result."""
    original: str = Field(..., description="Original input text")
    rewritten: str = Field(..., description="Calmer, constructive version")
    tone: str = Field(..., description="Detected tone of rewrite (calm, neutral, empathetic)")
    emotion: str = Field(..., description="Original emotion that was softened")


class ApologyComponents(BaseModel):
    """The 5 psychology-backed components of a genuine apology."""
    acknowledgment: str = Field(..., description="Names the specific harm done")
    responsibility: str = Field(..., description="Takes ownership without excuses")
    remorse: str = Field(..., description="Expresses genuine regret")
    repair: str = Field(..., description="Offers corrective action for the future")
    invitation: Optional[str] = Field(None, description="Optional invitation for the other person to respond")


class ApologyOut(BaseModel):
    """Heartfelt apology result — follows 5-component psychological model."""
    original: str = Field(..., description="Original input text")
    apology: str = Field(..., description="Full generated apology text")
    tone: str = Field(..., description="Apology tone (empathetic, sincere, gentle)")
    repair_type: str = Field(..., description="e.g. acknowledgment + ownership + repair")
    components: ApologyComponents = Field(..., description="Breakdown of apology into 5 psychological components")


class SuggestedTrigger(BaseModel):
    """A single re-engagement trigger suggestion."""
    strategy: str = Field(..., description="Strategy name (curiosity_gap, reciprocity_hook, etc.)")
    suggestion: str = Field(..., description="The actual suggested message")
    psychology: str = Field(..., description="The psychology principle behind it")


class TriggerOut(BaseModel):
    """Conversation re-engagement analysis result."""
    engagement_level: str = Field(..., description="low, medium, or high")
    signals_detected: list[str] = Field(default_factory=list, description="Detected disengagement signals")
    suggested_triggers: list[SuggestedTrigger] = Field(default_factory=list, description="Re-engagement suggestions")


# ────────────────────────────────────────
# OUTPUTS — Combined / Pipeline
# ────────────────────────────────────────

class FullPipelineOut(BaseModel):
    """Combined response from the full pipeline."""
    analysis: AnalysisOut
    rewrite: Optional[RewriteOut] = None
    apology: Optional[ApologyOut] = None
    triggers: Optional[TriggerOut] = None


class BatchOut(BaseModel):
    """Batch analysis results."""
    results: list[AnalysisOut] = Field(..., description="Analysis results for each message")
    count: int = Field(..., description="Number of messages processed")


class ErrorOut(BaseModel):
    """Standardized error response."""
    error: str = Field(..., description="Error type")
    detail: str = Field(..., description="Human-readable error description")
    code: int = Field(..., description="HTTP status code")
