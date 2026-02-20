from pydantic import BaseModel
from typing import Optional, Literal


class MessageIn(BaseModel):
    text: str


class AnalysisOut(BaseModel):
    emotion: str
    intensity: float
    risk: Literal["low", "medium", "high"]


class RewriteOut(BaseModel):
    original: str
    rewritten: str
    tone: str


class ApologyOut(BaseModel):
    original: str
    apology: str
    tone: str
    repair_type: str


class TriggerOut(BaseModel):
    engagement_level: Literal["low", "medium", "high"]
    signals_detected: list[str]
    suggested_trigger: dict


class FullAnalysisOut(BaseModel):
    analysis: AnalysisOut
    rewrite: RewriteOut
    apology: ApologyOut


class HealthOut(BaseModel):
    status: str
    version: str = "1.0.0"
