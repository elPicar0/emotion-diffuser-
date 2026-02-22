"""
Tests for analysis_engine utility functions.
"""

import pytest
from analysis_engine.utils import calculate_risk_level, detect_disengagement_signals, format_emotion_results


class TestCalculateRiskLevel:
    """Tests for calculate_risk_level()."""

    def test_high_risk_toxic(self):
        assert calculate_risk_level(0.8, 0.4) == "high"

    def test_high_risk_intense_emotion(self):
        assert calculate_risk_level(0.4, 0.9) == "high"

    def test_medium_risk(self):
        assert calculate_risk_level(0.4, 0.6) == "medium"

    def test_low_risk(self):
        assert calculate_risk_level(0.1, 0.2) == "low"


class TestDetectDisengagementSignals:
    """Tests for detect_disengagement_signals()."""

    def test_short_responses_detected(self):
        messages = ["Ok", "Yes", "Fine"]
        signals = detect_disengagement_signals(messages)
        assert "short_responses" in signals

    def test_no_questions_detected(self):
        messages = ["Ok", "Yes", "Fine"]
        signals = detect_disengagement_signals(messages)
        assert "no_questions" in signals

    def test_healthy_conversation(self):
        messages = [
            "How are you doing today?",
            "I'm feeling much better now.",
            "That's good to hear!",
        ]
        signals = detect_disengagement_signals(messages)
        assert "short_responses" not in signals
        assert "no_questions" not in signals

    def test_empty_messages(self):
        assert detect_disengagement_signals([]) == []


class TestFormatEmotionResults:
    """Tests for format_emotion_results()."""

    def test_sorts_by_score(self):
        raw = [
            {"label": "anger", "score": 0.1},
            {"label": "joy", "score": 0.8},
            {"label": "neutral", "score": 0.1},
        ]
        top_label, top_score, details = format_emotion_results(raw)
        assert top_label == "joy"
        assert top_score == 0.8
        assert len(details) == 3
        assert details[0].label == "joy"

    def test_single_emotion(self):
        raw = [{"label": "anger", "score": 0.95}]
        top_label, top_score, details = format_emotion_results(raw)
        assert top_label == "anger"
        assert top_score == 0.95
        assert len(details) == 1
