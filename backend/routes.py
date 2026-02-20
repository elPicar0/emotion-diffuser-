from fastapi import APIRouter, HTTPException
from backend.schemas import (
    MessageIn, 
    AnalysisOut, 
    RewriteOut, 
    ApologyOut, 
    TriggerOut, 
    FullAnalysisOut,
    HealthOut
)

router = APIRouter()


@router.get("/health", response_model=HealthOut)
def health():
    """Health check endpoint"""
    return HealthOut(status="healthy")


@router.post("/analyze", response_model=AnalysisOut)
def analyze_message(message: MessageIn):
    """Analyze emotion and escalation level from text"""
    try:
        # TODO: Call orchestrator.analyze_emotion()
        # Placeholder logic for now
        text = message.text.lower()
        
        if any(word in text for word in ["angry", "mad", "furious", "hate"]):
            emotion = "anger"
            intensity = 0.8
            risk = "high"
        elif any(word in text for word in ["happy", "excited", "great", "love"]):
            emotion = "joy"
            intensity = 0.7
            risk = "low"
        elif any(word in text for word in ["sad", "depressed", "cry", "hurt"]):
            emotion = "sadness"
            intensity = 0.6
            risk = "medium"
        else:
            emotion = "neutral"
            intensity = 0.3
            risk = "low"
        
        return AnalysisOut(
            emotion=emotion,
            intensity=intensity,
            risk=risk
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/rewrite", response_model=RewriteOut)
def rewrite_message(message: MessageIn):
    """Rewrite message with calmer tone"""
    try:
        # TODO: Call orchestrator.rewrite_message()
        # Placeholder logic
        text = message.text
        rewritten = f"I understand you're feeling strongly about this. Let's discuss this calmly: {text}"
        
        return RewriteOut(
            original=text,
            rewritten=rewritten,
            tone="calm"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/apologize", response_model=ApologyOut)
def generate_apology(message: MessageIn):
    """Generate heartfelt apology based on message"""
    try:
        # TODO: Call orchestrator.generate_apology()
        # Placeholder logic
        text = message.text
        apology = f"I realize what I said was hurtful. I take full responsibility for my words and I'm committed to communicating more thoughtfully in the future."
        
        return ApologyOut(
            original=text,
            apology=apology,
            tone="empathetic",
            repair_type="acknowledgment + ownership + repair"
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/full-analysis", response_model=FullAnalysisOut)
def full_analysis(message: MessageIn):
    """Complete pipeline: analyze + rewrite + apologize"""
    try:
        # TODO: Call orchestrator.full_pipeline()
        # For now, call individual endpoints
        analysis = analyze_message(message)
        rewrite = rewrite_message(message)
        apology = generate_apology(message)
        
        return FullAnalysisOut(
            analysis=analysis,
            rewrite=rewrite,
            apology=apology
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/triggers", response_model=TriggerOut)
def detect_engagement_triggers(message: MessageIn):
    """Detect conversation disengagement and suggest re-engagement triggers"""
    try:
        # TODO: Call orchestrator.detect_triggers()
        # Placeholder logic
        text = message.text.lower()
        
        signals = []
        if len(text.split()) < 3:
            signals.append("short_response")
        if "?" not in text:
            signals.append("no_questions")
        
        engagement_level = "low" if len(signals) >= 2 else "medium"
        
        suggested_trigger = {
            "strategy": "curiosity_gap",
            "suggestion": "Something interesting happened today that I think you'd want to hear about...",
            "psychology": "Loewenstein's Information Gap Theory"
        }
        
        return TriggerOut(
            engagement_level=engagement_level,
            signals_detected=signals,
            suggested_trigger=suggested_trigger
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
