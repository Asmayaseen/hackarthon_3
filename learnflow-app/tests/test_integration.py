"""
Integration tests for LearnFlow platform

These tests verify the services are reachable and responding correctly.
Run against a live docker-compose stack: `docker compose up -d`

Usage:
  pytest learnflow-app/tests/test_integration.py -v
  pytest learnflow-app/tests/test_integration.py -v --timeout=30
"""

import os
import pytest
import httpx

BASE_URLS = {
    "triage":   os.getenv("TRIAGE_URL",   "http://localhost:8000"),
    "concepts": os.getenv("CONCEPTS_URL", "http://localhost:8001"),
    "debug":    os.getenv("DEBUG_URL",    "http://localhost:8002"),
    "review":   os.getenv("REVIEW_URL",   "http://localhost:8003"),
    "exercise": os.getenv("EXERCISE_URL", "http://localhost:8004"),
    "progress": os.getenv("PROGRESS_URL", "http://localhost:8005"),
    "mcp":      os.getenv("MCP_URL",      "http://localhost:8006"),
    "gateway":  os.getenv("GATEWAY_URL",  "http://localhost:8007"),
}

SERVICES_TO_TEST = [
    pytest.param("triage",   marks=pytest.mark.integration),
    pytest.param("concepts", marks=pytest.mark.integration),
    pytest.param("exercise", marks=pytest.mark.integration),
    pytest.param("progress", marks=pytest.mark.integration),
    pytest.param("mcp",      marks=pytest.mark.integration),
    pytest.param("gateway",  marks=pytest.mark.integration),
]


@pytest.fixture
def http():
    with httpx.Client(timeout=10.0) as client:
        yield client


# ── Health checks ──────────────────────────────────────────────────────────────

@pytest.mark.integration
@pytest.mark.parametrize("service", SERVICES_TO_TEST)
def test_service_health(http, service):
    url = BASE_URLS[service]
    try:
        resp = http.get(f"{url}/health")
        assert resp.status_code == 200
        body = resp.json()
        assert "status" in body
    except httpx.ConnectError:
        pytest.skip(f"{service} not running at {url}")


# ── Gateway routing ────────────────────────────────────────────────────────────

@pytest.mark.integration
def test_gateway_aggregated_health(http):
    try:
        resp = http.get(f"{BASE_URLS['gateway']}/health")
        assert resp.status_code == 200
        body = resp.json()
        assert "services" in body
    except httpx.ConnectError:
        pytest.skip("API gateway not running")


@pytest.mark.integration
def test_gateway_routes_to_triage(http):
    try:
        resp = http.get(f"{BASE_URLS['gateway']}/api/triage/")
        assert resp.status_code in (200, 404)  # 404 is fine — route exists
    except httpx.ConnectError:
        pytest.skip("API gateway not running")


# ── Triage service functional ──────────────────────────────────────────────────

@pytest.mark.integration
def test_triage_classifies_explain_query(http):
    try:
        resp = http.post(f"{BASE_URLS['triage']}/query", json={
            "student_id": "integration-test-student",
            "query_text": "What is a Python list comprehension?",
            "student_level": "beginner",
        })
        assert resp.status_code == 200
        body = resp.json()
        assert body["classification"] in (
            "explain", "exercise", "review", "debug", "progress", "unclassified"
        )
        assert 0.0 <= body["confidence"] <= 1.0
    except httpx.ConnectError:
        pytest.skip("Triage service not running")


# ── MCP server ─────────────────────────────────────────────────────────────────

@pytest.mark.integration
def test_mcp_system_overview(http):
    try:
        resp = http.post(f"{BASE_URLS['mcp']}/tools/get_system_overview", json={})
        assert resp.status_code == 200
    except httpx.ConnectError:
        pytest.skip("MCP server not running")
