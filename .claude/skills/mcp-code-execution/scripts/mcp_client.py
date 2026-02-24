#!/usr/bin/env python3
"""
MCP Code Execution Pattern - Example client wrapper.
This script demonstrates wrapping MCP server operations in efficient Python scripts.
Instead of loading MCP tools into agent context (50k tokens),
execute this script (0 tokens) and only the result enters context (~10 tokens).
"""
import subprocess
import json
import sys
import os
from typing import Optional


class MCPCodeExecutor:
    """Wraps MCP server operations as executable scripts."""

    def __init__(self, namespace: str = 'learnflow'):
        self.namespace = namespace
        self.dapr_port = os.getenv('DAPR_HTTP_PORT', '3500')

    def get_pods_status(self) -> dict:
        """Efficient pod status - returns summary only."""
        result = subprocess.run(
            ['kubectl', 'get', 'pods', '-n', self.namespace, '-o', 'json'],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            return {'error': result.stderr, 'running': 0, 'total': 0}

        pods = json.loads(result.stdout).get('items', [])
        running = sum(1 for p in pods if p['status'].get('phase') == 'Running')
        # Return SUMMARY not full JSON - key to token efficiency
        return {'running': running, 'total': len(pods), 'namespace': self.namespace}

    def publish_event(self, topic: str, data: dict) -> bool:
        """Publish to Kafka topic via Dapr - returns boolean only."""
        import urllib.request
        import urllib.error

        url = f"http://localhost:{self.dapr_port}/v1.0/publish/kafka-pubsub/{topic}"
        body = json.dumps(data).encode()

        try:
            req = urllib.request.Request(url, data=body,
                                         headers={'Content-Type': 'application/json'})
            urllib.request.urlopen(req, timeout=5)
            return True
        except (urllib.error.URLError, Exception):
            return False

    def get_kafka_topics(self) -> list:
        """Get Kafka topics - returns list of names only."""
        # Find kafka pod
        result = subprocess.run(
            ['kubectl', 'get', 'pod', '-n', 'kafka',
             '-o', 'jsonpath={.items[0].metadata.name}'],
            capture_output=True, text=True
        )
        if result.returncode != 0 or not result.stdout.strip():
            return []

        pod = result.stdout.strip()
        result = subprocess.run(
            ['kubectl', 'exec', '-n', 'kafka', pod, '--',
             'kafka-topics.sh', '--bootstrap-server', 'localhost:9092', '--list'],
            capture_output=True, text=True
        )
        return [t.strip() for t in result.stdout.split('\n') if t.strip()]

    def check_service_health(self, service: str, port: int = 8000) -> bool:
        """Check service health - returns bool only."""
        result = subprocess.run(
            ['kubectl', 'exec', '-n', self.namespace,
             f'deployment/{service}', '--',
             'curl', '-sf', f'http://localhost:{port}/health'],
            capture_output=True, text=True, timeout=10
        )
        return result.returncode == 0


def main():
    """Demonstrate MCP code execution pattern with minimal output."""
    executor = MCPCodeExecutor()
    command = sys.argv[1] if len(sys.argv) > 1 else 'status'

    if command == 'status':
        status = executor.get_pods_status()
        # Minimal output - only this enters agent context
        print(f"✓ {status['running']}/{status['total']} pods running in {status['namespace']}")

    elif command == 'topics':
        topics = executor.get_kafka_topics()
        print(f"✓ {len(topics)} Kafka topics available")
        for t in topics[:5]:  # Max 5 in context
            print(f"  - {t}")

    elif command == 'health':
        services = ['triage-service', 'concepts-service', 'progress-service']
        for svc in services:
            ok = executor.check_service_health(svc)
            print(f"{'✓' if ok else '✗'} {svc}")

    else:
        print(f"Usage: python mcp_client.py [status|topics|health]")
        sys.exit(1)


if __name__ == '__main__':
    main()
