"""
Analysis Utilities — handles categorization, thresholds, and risk scoring.
"""

from typing import List, Tuple
from backend.schemas import EmotionDetail

# Risk thresholds
TOXICITY_HIGH_THRESHOLD = 0.7
TOXICITY_MEDIUM_THRESHOLD = 0.3

EMOTION_INTENSITY_HIGH_THRESHOLD = 0.8
EMOTION_INTENSITY_MEDIUM_THRESHOLD = 0.5

def calculate_risk_level(toxicity_score: float, max_emotion_score: float) -> str:
    """Determine escalation risk (high, medium, low) based on toxicity and emotion intensity."""
    if toxicity_score > TOXICITY_HIGH_THRESHOLD or max_emotion_score > EMOTION_INTENSITY_HIGH_THRESHOLD:
        return "high"
    if toxicity_score > TOXICITY_MEDIUM_THRESHOLD or max_emotion_score > EMOTION_INTENSITY_MEDIUM_THRESHOLD:
        return "medium"
    return "low"

def format_emotion_results(raw_scores: List[dict]) -> Tuple[str, float, List[EmotionDetail]]:
    """
    Sort raw HF scores and return (top_label, top_score, formatted_list).
    """
    # Sort by score descending
    sorted_scores = sorted(raw_scores, key=lambda x: x['score'], reverse=True)
    
    top_emotion = sorted_scores[0]['label']
    top_score = round(sorted_scores[0]['score'], 3)
    
    details = [
        EmotionDetail(label=item['label'], score=round(item['score'], 3))
        for item in sorted_scores
    ]
    
    return top_emotion, top_score, details
