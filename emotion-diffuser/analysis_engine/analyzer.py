"""
Core Analyzer Logic — coordinates model inference and result processing.
"""

import logging
from backend.schemas import AnalysisOut
from .models import get_emotion_pipeline, get_toxicity_pipeline
from .utils import format_emotion_results, calculate_risk_level

logger = logging.getLogger(__name__)

async def analyze_text(text: str, context: str | None = None) -> AnalysisOut:
    """
    Analyze a piece of text for emotions and toxicity.
    
    Parameters
    ----------
    text : str
        The user input to analyze.
    context : str, optional
        Additional context for the analysis.
        
    Returns
    -------
    AnalysisOut
        Structured analysis results.
    """
    try:
        # Load pipelines (singleton/cached)
        emotion_pipe = get_emotion_pipeline()
        toxicity_pipe = get_toxicity_pipeline()
        
        # Run inference
        raw_emotions = emotion_pipe(text)[0]  # HF returns list of lists for top_k=None
        raw_toxicity = toxicity_pipe(text)[0] # HF returns list for single input
        
        # Process emotions
        top_emotion, intensity, all_emotions = format_emotion_results(raw_emotions)
        
        # Process toxicity
        # Note: martin-ha/toxic-comment-model returns [{'label': 'toxic/non-toxic', 'score': float}]
        # The label is usually binary.
        is_toxic = False
        toxicity_score = 0.0
        
        if raw_toxicity['label'].lower() == 'toxic':
            is_toxic = True
            toxicity_score = round(raw_toxicity['score'], 3)
        else:
            # If non-toxic, the score is often for 'non-toxic', so we invert it for risk calculation
            toxicity_score = round(1.0 - raw_toxicity['score'], 3)

        # Calculate escalation risk
        risk = calculate_risk_level(toxicity_score, intensity)
        
        return AnalysisOut(
            emotion=top_emotion,
            intensity=intensity,
            risk=risk,
            is_toxic=is_toxic,
            toxicity_score=toxicity_score,
            all_emotions=all_emotions
        )

    except Exception as e:
        logger.error(f"Analysis failed: {str(e)}")
        # Fallback to neutral if ML fails
        return AnalysisOut(
            emotion="neutral",
            intensity=0.1,
            risk="low",
            is_toxic=False,
            toxicity_score=0.01,
            all_emotions=[]
        )
