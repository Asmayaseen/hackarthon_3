"""
Unit tests for Triage Service

Tests:
- Health endpoint
- Query classification routing (mock OpenAI)
- Kafka topic mapping
- /answer endpoint response shape
"""

import pytest
from unittest.mock import AsyncMock, patch, MagicMock
from fastapi.testclient import TestClient

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from main import app, get_kafka_topic, QueryClassification


# ── Fixtures ──────────────────────────────────────────────────────────────────

@pytest.fixture
def client():
    return TestClient(app)


# ── Unit tests ─────────────────────────────────────────────────────────────────

class TestKafkaTopicMapping:
    def test_explain_maps_to_correct_topic(self):
        topic, event = get_kafka_topic("explain")
        assert topic == "learning.query.explain"
        assert "Explanation" in event

    def test_debug_maps_to_correct_topic(self):
        topic, event = get_kafka_topic("debug")
        assert topic == "code.debug.request"

    def test_exercise_maps_to_correct_topic(self):
        topic, event = get_kafka_topic("exercise")
        assert topic == "exercise.generate"

    def test_unknown_maps_to_unclassified(self):
        topic, _ = get_kafka_topic("unknown_type")
        assert topic == "learning.query.unclassified"


class TestHealthEndpoint:
    def test_health_returns_200(self, client):
        resp = client.get("/health")
        assert resp.status_code == 200

    def test_health_includes_status_key(self, client):
        resp = client.get("/health")
        body = resp.json()
        assert "status" in body
        assert body["status"] == "healthy"


class TestRootEndpoint:
    def test_root_returns_200(self, client):
        resp = client.get("/")
        assert resp.status_code == 200

    def test_root_includes_message(self, client):
        body = client.get("/").json()
        assert "message" in body


class TestQueryEndpoint:
    @patch("main.classify_query_with_openai", new_callable=AsyncMock)
    @patch("main.publish_to_kafka", new_callable=AsyncMock)
    def test_query_returns_classification(self, mock_publish, mock_classify, client):
        mock_classify.return_value = QueryClassification(
            classification="explain",
            confidence=0.95,
            reason="Conceptual question"
        )
        mock_publish.return_value = True

        resp = client.post("/query", json={
            "student_id": "student-1",
            "query_text": "How do for loops work?",
            "student_level": "beginner"
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["classification"] == "explain"
        assert body["confidence"] == 0.95

    @patch("main.classify_query_with_openai", new_callable=AsyncMock)
    @patch("main.publish_to_kafka", new_callable=AsyncMock)
    def test_query_handles_kafka_failure_gracefully(self, mock_publish, mock_classify, client):
        mock_classify.return_value = QueryClassification(
            classification="debug",
            confidence=0.8,
            reason="Error question"
        )
        mock_publish.return_value = False  # Kafka down

        resp = client.post("/query", json={
            "student_id": "student-2",
            "query_text": "I got a TypeError, help!",
            "student_level": "beginner"
        })
        # Should still return 200 despite Kafka failure
        assert resp.status_code == 200


class TestAnswerEndpoint:
    @patch("main.classify_query_with_openai", new_callable=AsyncMock)
    @patch("main.generate_ai_response", new_callable=AsyncMock)
    def test_answer_returns_reply(self, mock_generate, mock_classify, client):
        mock_classify.return_value = QueryClassification(
            classification="explain",
            confidence=0.9,
            reason="Concept"
        )
        mock_generate.return_value = "A for loop iterates over a sequence..."

        resp = client.post("/answer", json={
            "student_id": "student-1",
            "message": "Explain for loops",
            "student_level": "beginner"
        })
        assert resp.status_code == 200
        body = resp.json()
        assert "reply" in body
        assert "classification" in body
        assert body["reply"] == "A for loop iterates over a sequence..."
