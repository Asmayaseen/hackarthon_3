#!/usr/bin/env python3
import subprocess, sys
r = subprocess.run(
    "kubectl get components -n learnflow --no-headers 2>/dev/null",
    shell=True, capture_output=True, text=True
)
if r.returncode == 0 and "kafka-pubsub" in r.stdout:
    print("✓ Dapr kafka-pubsub component deployed")
    sys.exit(0)
print("✗ kafka-pubsub component not found in learnflow namespace")
sys.exit(1)
