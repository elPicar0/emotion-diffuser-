"""
Analysis Utilities — handles categorization, thresholds, and risk scoring.
"""

from typing import List, Tuple
from backend.schemas import EmotionDetail
from backend import config


def calculate_risk_level(toxicity_score: float, max_emotion_score: float) -> str:
    """Determine escalation risk (high, medium, low) based on toxicity and emotion intensity."""
    if toxicity_score > config.TOXICITY_THRESHOLD or max_emotion_score > config.HIGH_RISK_THRESHOLD:
        return "high"
    if toxicity_score > config.TOXICITY_THRESHOLD * 0.5 or max_emotion_score > config.MEDIUM_RISK_THRESHOLD:
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

def detect_disengagement_signals(messages: List[str]) -> List[str]:
    """
    Analyze a list of messages for disengagement signals (heuristic-based).
    """
    signals = []
    if not messages:
        return signals

    short_count = sum(1 for m in messages if len(m.split()) <= 3)
    question_count = sum(1 for m in messages if "?" in m)

    # If more than 50% of responses are very short
    if short_count > len(messages) * 0.5:
        signals.append("short_responses")
    
    # If no questions are being asked to keep the conversation going
    if question_count == 0:
        signals.append("no_questions")

    return signals
