#!/usr/bin/env python3
import subprocess, sys
r = subprocess.run(
    "kubectl get applications -n argocd --no-headers 2>/dev/null",
    shell=True, capture_output=True, text=True
)
if r.returncode == 0 and r.stdout.strip():
    print(f"✓ ArgoCD applications: {len(r.stdout.strip().splitlines())} found")
    print(r.stdout.strip())
    sys.exit(0)
print("✗ No ArgoCD applications found or ArgoCD not installed")
sys.exit(1)
