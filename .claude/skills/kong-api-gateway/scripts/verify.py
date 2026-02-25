#!/usr/bin/env python3
import subprocess, sys
r = subprocess.run(
    "kubectl get pods -n kong -l app.kubernetes.io/name=kong --no-headers 2>/dev/null | grep Running",
    shell=True, capture_output=True, text=True
)
ok = r.returncode == 0 and r.stdout.strip()
print("✓ Kong gateway running" if ok else "✗ Kong not running")
sys.exit(0 if ok else 1)
