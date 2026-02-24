#!/usr/bin/env python3
"""
LearnFlow Progress Service Verification Script
Constitution Article VIII Compliance: Dapr, Postgres, Kafka, Progress Endpoints, Trend Detection
"""

import asyncio
import json
import os
import sys
import time
from typing import Dict, List, Tuple

import aiohttp
import httpx
import asyncpg

# Config
NAMESPACE = os.getenv("NAMESPACE", "learnflow")
PROGRESS_SERVICE = os.getenv("PROGRESS_SERVICE", "http://progress-service")
POSTGRES_URL = os.getenv("POSTGRES_URL", "postgresql://user:pass@postgres/learnflow")
KAFKA_BROKER = os.getenv("KAFKA_BROKER", "kafka:9092")
DAPR_PORT = os.getenv("DAPR_HTTP_PORT", "3500")

def print_header(message: str) -> None:
    print(f"\n{'=' * 60}")
    print(f"  {message}")
    print(f"{'=' * 60}\n")

def print_test(name: str, status: bool, details: str = "") -> None:
    symbol = "✅" if status else "❌"
    print(f"{symbol} {name}")
    if details:
        print(f"   {details}")

async def check_kubernetes_pods() -> Tuple[bool, List[str]]:
    try:
        import subprocess
        result = subprocess.run(["kubectl", "get", "pods", "-n", NAMESPACE, "-o", "json"], capture_output=True, text=True, check=True)
        pods = json.loads(result.stdout)["items"]
        errors = []
        for pod in pods:
            name = pod["metadata"]["name"]
            phase = pod["status"]["phase"]
            if phase != "Running":
                errors.append(f"Pod {name}: {phase}")
        return len(errors) == 0, errors
    except Exception as e:
        return False, [str(e)]

async def check_dapr_sidecars() -> Tuple[bool, List[str]]:
    try:
        import subprocess
        result = subprocess.run(["kubectl", "get", "pods", "-n", NAMESPACE, "-o", "json"], capture_output=True, text=True, check=True)
        pods = json.loads(result.stdout)["items"]
        errors = []
        for pod in pods:
            containers = pod["spec"]["containers"]
            if not any(c["name"] == "daprd" for c in containers):
                errors.append(f"Pod {pod['metadata']['name']} missing Dapr sidecar")
        return len(errors) == 0, errors
    except Exception as e:
        return False, [str(e)]

async def check_postgres_connectivity() -> Tuple[bool, List[str]]:
    try:
        conn = await asyncpg.connect(POSTGRES_URL)
        await conn.close()
        return True, ["Postgres connected"]
    except Exception as e:
        return False, [str(e)]

async def check_kafka_pubsub() -> Tuple[bool, List[str]]:
    try:
        import subprocess
        # Check kafka-pubsub component
        result = subprocess.run(["kubectl", "get", "components.dapr.io", "kafka-pubsub", "-n", NAMESPACE, "-o", "json"], capture_output=True, text=True)
        if result.returncode != 0:
            return False, ["kafka-pubsub component missing"]
        return True, ["Kafka pub/sub ready"]
    except Exception as e:
        return False, [str(e)]

async def check_progress_endpoints() -> Tuple[bool, List[str]]:
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{PROGRESS_SERVICE}/health") as resp:
                if resp.status != 200:
                    return False, [f"Health: {resp.status}"]
            async with session.get(f"{PROGRESS_SERVICE}/progress/test-student") as resp:
                if resp.status != 200:
                    return False, [f"/progress: {resp.status}"]
            return True, ["Endpoints healthy"]
    except Exception as e:
        return False, [str(e)]

async def test_phase6_trend_detection() -> Tuple[bool, List[str]]:
    try:
        from dapr.clients import DaprClient
        dapr = DaprClient()
        # Mock 3 low scores for test-student
        low_scores = [55, 52, 48]
        for score in low_scores:
            await dapr.publish_event(
                pubsub_name="kafka-pubsub",
                topic_name="exercise.graded",
                data={"student_id": "test-student", "score": score, "topic": "loops"}
            )
            await asyncio.sleep(0.1)  # Process time
        # Check if alert generated (query state or endpoint)
        async with aiohttp.ClientSession() as session:
            async with session.get(f"{PROGRESS_SERVICE}/struggles?student_id=test-student") as resp:
                data = await resp.json()
                alerts = [a for a in data if "low_scores" in a.get("type", "")]
                if len(alerts) > 0:
                    return True, [f"Trend alert detected: {len(alerts)}"]
        return False, ["No trend alert"]
    except Exception as e:
        return False, [str(e)]

async def run_all_verifications() -> Dict:
    results = {}
    print_header("LearnFlow Verification")

    # Infra
    results["pods"] = await check_kubernetes_pods()
    results["dapr"] = await check_dapr_sidecars()

    # Connectivity
    results["postgres"] = await check_postgres_connectivity()
    results["kafka"] = await check_kafka_pubsub()

    # Services
    results["progress"] = await check_progress_endpoints()

    # Functional
    results["trend_test"] = await test_phase6_trend_detection()

    # Print results
    tests = [("Pods", results["pods"]), ("Dapr Sidecars", results["dapr"]),
             ("Postgres", results["postgres"]), ("Kafka Pub/Sub", results["kafka"]),
             ("Progress Endpoints", results["progress"]), ("Trend Detection", results["trend_test"])]
    for name, (status, details) in tests:
        print_test(name, status, ", ".join(details) if isinstance(details, list) else details)

    passed = sum(s[0] for s in tests)
    print(f"\nSummary: {passed}/6 passed")
    return {"status": "PASSED" if passed == 6 else "FAILED", "passed": passed}

if __name__ == "__main__":
    result = asyncio.run(run_all_verifications())
    sys.exit(0 if result["status"] == "PASSED" else 1)
