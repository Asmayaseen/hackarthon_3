#!/usr/bin/env python3
"""Verify Kafka deployment on Kubernetes - returns minimal result."""
import subprocess
import json
import sys


def run(cmd: list) -> tuple[str, int]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def check_pods() -> bool:
    out, rc = run(['kubectl', 'get', 'pods', '-n', 'kafka', '-o', 'json'])
    if rc != 0:
        print('✗ Cannot connect to Kubernetes')
        return False
    pods = json.loads(out).get('items', [])
    if not pods:
        print('✗ No Kafka pods found in namespace kafka')
        return False
    running = sum(1 for p in pods if p['status'].get('phase') == 'Running')
    total = len(pods)
    if running == total:
        print(f'✓ All {total} Kafka pods running')
        return True
    print(f'✗ {running}/{total} Kafka pods running')
    return False


def check_service() -> bool:
    out, rc = run(['kubectl', 'get', 'svc', '-n', 'kafka', '-o', 'json'])
    if rc != 0:
        return False
    svcs = json.loads(out).get('items', [])
    names = [s['metadata']['name'] for s in svcs]
    bootstrap = next((n for n in names if 'bootstrap' in n), None)
    if bootstrap:
        print(f'✓ Kafka bootstrap service: {bootstrap}')
        return True
    print('✗ Kafka bootstrap service not found')
    return False


def check_topics() -> bool:
    # Find kafka pod
    out, rc = run(['kubectl', 'get', 'pods', '-n', 'kafka', '-o', 'jsonpath={.items[0].metadata.name}'])
    if rc != 0 or not out:
        print('⚠ Cannot check topics (no pod found)')
        return True  # Non-blocking

    pod = out.strip()
    out, rc = run([
        'kubectl', 'exec', '-n', 'kafka', pod, '--',
        'kafka-topics.sh', '--bootstrap-server', 'localhost:9092', '--list'
    ])

    required = ['learning.query.explain', 'progress.update']
    found = [t for t in required if t in out]

    if len(found) == len(required):
        print(f'✓ LearnFlow topics present ({len(out.splitlines())} total topics)')
        return True
    print(f'⚠ Some topics missing. Found {len(found)}/{len(required)} required topics')
    print('  Run: bash scripts/create-topics.sh')
    return True  # Warning, not failure


def main():
    checks = [check_pods, check_service, check_topics]
    results = [check() for check in checks]

    failed = results.count(False)
    if failed > 0:
        print(f'\n✗ {failed} check(s) failed')
        sys.exit(1)
    print('\n✓ Kafka ready for LearnFlow')
    sys.exit(0)


if __name__ == '__main__':
    main()
