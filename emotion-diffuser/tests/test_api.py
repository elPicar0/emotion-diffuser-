"""
Integration tests for the Emotion Diffuser API endpoints.

Note: Tests that require LLM calls (rewrite, apologize, pipeline) are skipped
if OPENAI_API_KEY is not set, since they depend on an external service.
"""

import os
import pytest
from fastapi.testclient import TestClient
from backend.main import app

client = TestClient(app)

OPENAI_KEY_SET = bool(os.getenv("OPENAI_API_KEY"))


# ── Health ──────────────────────────────

def test_root_endpoint():
    """Root should return a running message."""
    response = client.get("/")
    assert response.status_code == 200
    assert "Emotion Diffuser" in response.json()["message"]


def test_health_endpoint():
    """Health check lives under /api/v1/health."""
    response = client.get("/api/v1/health")
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "healthy"
    assert "features" in data


# ── Analyze ─────────────────────────────

def test_analyze_endpoint():
    """Analyze should return emotion/intensity/risk."""
    response = client.post(
        "/api/v1/analyze",
        json={"text": "I am so angry right now!", "relationship": "friend"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "emotion" in data
    assert "intensity" in data
    assert "risk" in data
    assert data["risk"] in ("low", "medium", "high")


def test_analyze_empty_text_rejected():
    """Empty text should be rejected by validation."""
    response = client.post("/api/v1/analyze", json={"text": ""})
    assert response.status_code == 422  # Pydantic validation


# ── Rewrite (LLM-dependent) ────────────

@pytest.mark.skipif(not OPENAI_KEY_SET, reason="OPENAI_API_KEY not set")
def test_rewrite_endpoint():
    response = client.post(
        "/api/v1/rewrite",
        json={"text": "You always forget things!", "relationship": "partner"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "rewritten" in data
    assert data["tone"] == "calm"


# ── Apologize (LLM-dependent) ──────────

@pytest.mark.skipif(not OPENAI_KEY_SET, reason="OPENAI_API_KEY not set")
def test_apologize_endpoint():
    response = client.post(
        "/api/v1/apologize",
        json={"text": "I'm sorry I was late.", "relationship": "professional"},
    )
    assert response.status_code == 200
    data = response.json()
    assert "apology" in data
    assert "components" in data


# ── Pipeline (LLM-dependent) ───────────

@pytest.mark.skipif(not OPENAI_KEY_SET, reason="OPENAI_API_KEY not set")
def test_pipeline_endpoint():
    response = client.post(
        "/api/v1/pipeline",
        json={
            "text": "I hate it when you do that.",
            "relationship": "parent",
            "include_rewrite": True,
            "include_apology": True,
        },
    )
    assert response.status_code == 200
    data = response.json()
    assert data["analysis"] is not None
    assert data["rewrite"] is not None
    assert data["apology"] is not None


# ── Triggers ────────────────────────────

def test_triggers_endpoint():
    """Triggers should detect disengagement from short messages."""
    response = client.post(
        "/api/v1/triggers",
        json={"messages": ["Ok", "Yes", "Fine"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["engagement_level"] in ("low", "medium", "high")
    assert "signals_detected" in data
