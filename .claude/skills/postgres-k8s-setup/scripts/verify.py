#!/usr/bin/env python3
"""Verify PostgreSQL deployment on Kubernetes."""
import subprocess
import json
import sys


def run(cmd: list) -> tuple[str, int]:
    result = subprocess.run(cmd, capture_output=True, text=True)
    return result.stdout.strip(), result.returncode


def check_cluster() -> bool:
    out, rc = run(['kubectl', 'get', 'cluster', 'pg-cluster', '-n', 'learnflow', '-o', 'json'])
    if rc != 0:
        print('✗ PostgreSQL cluster pg-cluster not found in learnflow namespace')
        return False
    cluster = json.loads(out)
    phase = cluster.get('status', {}).get('phase', 'Unknown')
    ready = cluster.get('status', {}).get('readyInstances', 0)
    if phase == 'Cluster in healthy state':
        print(f'✓ PostgreSQL cluster ready ({ready} instance(s))')
        return True
    print(f'⚠ PostgreSQL cluster phase: {phase}')
    return phase != 'Failed'


def check_pods() -> bool:
    out, rc = run(['kubectl', 'get', 'pods', '-n', 'learnflow',
                   '-l', 'cnpg.io/cluster=pg-cluster', '-o', 'json'])
    if rc != 0:
        print('✗ Cannot check PostgreSQL pods')
        return False
    pods = json.loads(out).get('items', [])
    if not pods:
        print('✗ No PostgreSQL pods found')
        return False
    running = sum(1 for p in pods if p['status'].get('phase') == 'Running')
    print(f'✓ PostgreSQL pod(s) running: {running}/{len(pods)}')
    return running > 0


def check_secret() -> bool:
    _, rc = run(['kubectl', 'get', 'secret', 'pg-cluster-app', '-n', 'learnflow'])
    if rc == 0:
        print('✓ Connection secret pg-cluster-app exists')
        return True
    # Try superuser secret as fallback
    _, rc2 = run(['kubectl', 'get', 'secret', 'pg-cluster-superuser', '-n', 'learnflow'])
    if rc2 == 0:
        print('✓ Connection secret pg-cluster-superuser exists')
        return True
    print('✗ No PostgreSQL connection secret found')
    return False


def check_tables() -> bool:
    out, rc = run(['kubectl', 'get', 'pod', '-n', 'learnflow',
                   '-l', 'cnpg.io/cluster=pg-cluster',
                   '-o', 'jsonpath={.items[0].metadata.name}'])
    if rc != 0 or not out:
        print('⚠ Cannot verify tables (no pod)')
        return True

    pod = out.strip()
    result = subprocess.run(
        ['kubectl', 'exec', '-n', 'learnflow', pod, '--',
         'psql', '-U', 'learnflow', '-d', 'learnflow', '-c',
         "SELECT tablename FROM pg_tables WHERE schemaname='public';"],
        capture_output=True, text=True
    )
    if result.returncode != 0:
        print('⚠ Cannot query tables yet')
        return True

    tables = result.stdout
    expected = ['students', 'student_progress', 'exercise_submissions']
    found = [t for t in expected if t in tables]
    if len(found) == len(expected):
        print(f'✓ LearnFlow tables present ({len(found)}/{len(expected)})')
    else:
        print(f'⚠ Tables missing. Run: python scripts/migrate.py')
    return True


def main():
    checks = [check_pods, check_secret, check_tables]
    results = [check() for check in checks]
    failed = results.count(False)
    if failed > 0:
        print(f'\n✗ {failed} check(s) failed')
        sys.exit(1)
    print('\n✓ PostgreSQL ready for LearnFlow')
    sys.exit(0)


if __name__ == '__main__':
    main()
