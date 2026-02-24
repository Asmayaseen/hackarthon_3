#!/usr/bin/env python3
"""Verify a scaffolded FastAPI + Dapr service."""
import sys
import os
from pathlib import Path


def verify(service_name: str):
    root = Path.cwd()
    svc_dir = root / 'learnflow-app' / 'services' / service_name
    errors = []

    if not svc_dir.exists():
        print(f'✗ Service directory not found: {svc_dir}')
        sys.exit(1)

    # Check required files
    required_files = ['main.py', 'Dockerfile', 'requirements.txt']
    for f in required_files:
        path = svc_dir / f
        if path.exists():
            print(f'  ✓ {f} exists')
        else:
            errors.append(f'Missing: {f}')
            print(f'  ✗ {f} missing')

    # Check main.py has required endpoints
    main_py = svc_dir / 'main.py'
    if main_py.exists():
        content = main_py.read_text()
        endpoints = ['/health', '/dapr/subscribe', '/handle']
        for ep in endpoints:
            if ep in content:
                print(f'  ✓ Endpoint {ep} defined')
            else:
                errors.append(f'Missing endpoint: {ep}')
                print(f'  ✗ Endpoint {ep} missing')

        if 'OPENAI_API_KEY' in content:
            print('  ✓ OpenAI API key configuration present')
        else:
            errors.append('Missing OPENAI_API_KEY configuration')

    # Check K8s manifest
    k8s_manifest = root / 'learnflow-app' / 'k8s' / 'deployments' / f'{service_name}.yaml'
    if k8s_manifest.exists():
        k8s_content = k8s_manifest.read_text()
        if 'dapr.io/enabled' in k8s_content:
            print('  ✓ Dapr annotations present in K8s manifest')
        else:
            errors.append('K8s manifest missing Dapr annotations')
        print(f'  ✓ K8s manifest exists')
    else:
        errors.append(f'K8s manifest missing: {k8s_manifest}')
        print(f'  ✗ K8s manifest missing')

    if errors:
        print(f'\n✗ {len(errors)} error(s) found in {service_name}')
        sys.exit(1)

    print(f'\n✓ {service_name} scaffolded correctly')
    sys.exit(0)


def main():
    if len(sys.argv) < 2:
        print('Usage: python scripts/verify.py <service-name>')
        sys.exit(1)
    verify(sys.argv[1])


if __name__ == '__main__':
    main()
