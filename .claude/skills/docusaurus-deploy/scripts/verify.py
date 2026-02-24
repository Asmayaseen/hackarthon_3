#!/usr/bin/env python3
"""Verify Docusaurus documentation deployment."""
import subprocess
import json
import sys


def run(cmd: list) -> tuple[str, int]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def check_pod() -> bool:
    out, rc = run(['kubectl', 'get', 'pods', '-n', 'learnflow',
                   '-l', 'app=learnflow-docs', '-o', 'json'])
    if rc != 0:
        print('✗ Cannot check docs pods')
        return False
    pods = json.loads(out).get('items', [])
    if not pods:
        print('✗ No docs pods found — run: bash scripts/deploy.sh')
        return False
    running = sum(1 for p in pods if p['status'].get('phase') == 'Running')
    if running > 0:
        print(f'✓ Docs pod(s) running: {running}/{len(pods)}')
        return True
    print(f'✗ Docs pods not ready: {running}/{len(pods)}')
    return False


def check_service() -> bool:
    _, rc = run(['kubectl', 'get', 'svc', 'learnflow-docs', '-n', 'learnflow'])
    if rc == 0:
        print('✓ learnflow-docs Service exists')
        return True
    print('✗ learnflow-docs Service not found')
    return False


def check_docs_dir() -> bool:
    import os
    if os.path.isdir('learnflow-docs'):
        print('✓ learnflow-docs/ directory exists')
        return True
    print('⚠ learnflow-docs/ not found — run: bash scripts/init.sh')
    return True  # Warning only


def main():
    checks = [check_docs_dir, check_pod, check_service]
    results = [check() for check in checks]
    failed = results.count(False)
    if failed > 0:
        print(f'\n✗ {failed} check(s) failed')
        sys.exit(1)
    print('\n✓ Docusaurus docs deployed')
    print('  Access: kubectl port-forward svc/learnflow-docs 8080:80 -n learnflow')
    sys.exit(0)


if __name__ == '__main__':
    main()
