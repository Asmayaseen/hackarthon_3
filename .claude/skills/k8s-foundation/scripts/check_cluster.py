#!/usr/bin/env python3
"""Check Kubernetes cluster health — returns minimal status."""
import subprocess, sys, json

def run(cmd):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=10)
    return r.returncode == 0, r.stdout.strip()

checks = {
    "kubectl available":  run("kubectl version --client --short 2>/dev/null || kubectl version --client"),
    "cluster reachable":  run("kubectl cluster-info --request-timeout=5s"),
    "nodes ready":        run("kubectl get nodes --no-headers | grep -v NotReady"),
}

all_ok = all(ok for ok, _ in checks.values())
for name, (ok, _) in checks.items():
    print(f"{'✓' if ok else '✗'} {name}")

print(f"\n{'✓ Cluster healthy' if all_ok else '✗ Cluster issues detected'}")
sys.exit(0 if all_ok else 1)
