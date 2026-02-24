#!/usr/bin/env python3
"""Verify Next.js frontend deployment on Kubernetes."""
import subprocess
import json
import sys


def run(cmd: list) -> tuple[str, int]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def check_pods() -> bool:
    out, rc = run(['kubectl', 'get', 'pods', '-n', 'learnflow',
                   '-l', 'app=learnflow-frontend', '-o', 'json'])
    if rc != 0:
        print('✗ Cannot check frontend pods')
        return False
    pods = json.loads(out).get('items', [])
    if not pods:
        print('✗ No frontend pods found — run: bash scripts/deploy.sh all')
        return False
    running = sum(1 for p in pods if p['status'].get('phase') == 'Running')
    if running > 0:
        print(f'✓ Frontend pod(s) running: {running}/{len(pods)}')
        return True
    print(f'✗ Frontend pods not ready: {running}/{len(pods)}')
    return False


def check_service() -> bool:
    _, rc = run(['kubectl', 'get', 'svc', 'learnflow-frontend', '-n', 'learnflow'])
    if rc == 0:
        print('✓ learnflow-frontend Service exists')
        return True
    print('✗ learnflow-frontend Service not found')
    return False


def check_image() -> bool:
    out, rc = run(['minikube', 'image', 'ls'])
    if rc != 0:
        print('⚠ Cannot check Minikube images')
        return True  # Non-blocking
    if 'learnflow-frontend' in out:
        print('✓ learnflow-frontend image loaded in Minikube')
        return True
    print('⚠ Image not found in Minikube — run: bash scripts/deploy.sh load')
    return True  # Warning only


def main():
    checks = [check_pods, check_service, check_image]
    results = [check() for check in checks]
    failed = results.count(False)
    if failed > 0:
        print(f'\n✗ {failed} check(s) failed')
        sys.exit(1)
    print('\n✓ LearnFlow frontend deployed and ready')
    print('  Access: kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow')
    sys.exit(0)


if __name__ == '__main__':
    main()
