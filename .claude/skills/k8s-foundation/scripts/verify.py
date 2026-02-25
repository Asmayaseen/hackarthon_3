#!/usr/bin/env python3
import subprocess, sys

def check(cmd, expect=""):
    r = subprocess.run(cmd, shell=True, capture_output=True, text=True, timeout=15)
    return r.returncode == 0

ok = all([
    check("kubectl get ns learnflow"),
    check("kubectl get ns kafka"),
    check("kubectl get ns dapr-system"),
])
print("✓ All namespaces ready" if ok else "✗ Some namespaces missing")
sys.exit(0 if ok else 1)
