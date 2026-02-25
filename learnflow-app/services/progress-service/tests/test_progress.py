"""
Unit tests for Progress Service

Tests:
- Mastery score calculation (Article VI.04 weights)
- Health endpoint
- Progress GET endpoint
- Struggle detection thresholds
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock

import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app, calculate_mastery_score


@pytest.fixture
def client():
    return TestClient(app)


# ── Mastery score calculation ──────────────────────────────────────────────────

class TestMasteryScoreCalculation:
    def test_perfect_score_returns_100(self):
        score = calculate_mastery_score(100.0, 100.0, 100.0, 100.0)
        assert score == 100.0

    def test_zero_score_returns_0(self):
        score = calculate_mastery_score(0.0, 0.0, 0.0, 0.0)
        assert score == 0.0

    def test_weights_sum_to_correct_value(self):
        # Only exercise completion = 1.0, rest = 0
        score = calculate_mastery_score(100.0, 0.0, 0.0, 0.0)
        assert score == pytest.approx(40.0, rel=1e-3)

    def test_quiz_weight_is_30_percent(self):
        score = calculate_mastery_score(0.0, 100.0, 0.0, 0.0)
        assert score == pytest.approx(30.0, rel=1e-3)

    def test_code_quality_weight_is_20_percent(self):
        score = calculate_mastery_score(0.0, 0.0, 100.0, 0.0)
        assert score == pytest.approx(20.0, rel=1e-3)

    def test_consistency_weight_is_10_percent(self):
        score = calculate_mastery_score(0.0, 0.0, 0.0, 100.0)
        assert score == pytest.approx(10.0, rel=1e-3)

    def test_typical_student_score(self):
        # 80% exercise, 75% quiz, 70% code quality, 90% consistency
        score = calculate_mastery_score(80.0, 75.0, 70.0, 90.0)
        expected = 80 * 0.4 + 75 * 0.3 + 70 * 0.2 + 90 * 0.1
        assert score == pytest.approx(expected, rel=1e-3)

    def test_score_is_rounded_to_2_decimals(self):
        score = calculate_mastery_score(33.333, 33.333, 33.333, 33.333)
        assert score == round(score, 2)


# ── Health endpoint ────────────────────────────────────────────────────────────

class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_has_status_key(self, client):
        body = client.get("/health").json()
        assert "status" in body


# ── Progress endpoint ──────────────────────────────────────────────────────────

class TestProgressEndpoint:
    def test_unknown_student_returns_404(self, client):
        resp = client.get("/progress/nonexistent-student")
        assert resp.status_code == 404

    def test_existing_student_returns_progress(self, client):
        # Seed in-memory DB
        from main import student_progress_db, StudentProgress
        student_progress_db["test-student"] = StudentProgress(
            student_id="test-student",
            mastery_score=72.5,
            exercises_completed=8,
            total_exercises=10,
            average_quiz_score=75.0,
            average_code_quality=70.0,
            consistency_score=80.0,
            last_activity="2026-02-25T10:00:00",
            topics_mastered=["variables", "loops"],
            topics_struggling=["recursion"],
            recommendations=["Practice recursion problems"],
        )
        resp = client.get("/progress/test-student")
        assert resp.status_code == 200
        body = resp.json()
        assert body["student_id"] == "test-student"
        assert body["mastery_score"] == 72.5
