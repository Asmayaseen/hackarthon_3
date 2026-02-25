#!/usr/bin/env python3
"""Test Dapr pub/sub by publishing to a test topic via Dapr HTTP API."""
import httpx, sys, json

DAPR_PORT = 3500
try:
    resp = httpx.post(
        f"http://localhost:{DAPR_PORT}/v1.0/publish/kafka-pubsub/test.topic",
        json={"message": "ping", "source": "skill-test"},
        timeout=5.0
    )
    if resp.status_code in (200, 204):
        print("✓ Message published to test.topic successfully")
        sys.exit(0)
    print(f"✗ Publish failed: HTTP {resp.status_code}")
except Exception as e:
    print(f"✗ Dapr not reachable on port {DAPR_PORT}: {e}")
    print("  Run: kubectl port-forward svc/dapr-api 3500:80 -n dapr-system")
sys.exit(1)
