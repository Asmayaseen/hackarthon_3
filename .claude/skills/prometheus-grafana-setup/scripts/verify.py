#!/usr/bin/env python3
import subprocess, sys

def pod_running(label, ns):
    r = subprocess.run(
        f"kubectl get pods -n {ns} -l {label} --no-headers | grep Running",
        shell=True, capture_output=True, text=True
    )
    return r.returncode == 0

checks = {
    "prometheus running": pod_running("app.kubernetes.io/name=prometheus", "monitoring"),
    "grafana running":    pod_running("app.kubernetes.io/name=grafana", "monitoring"),
}
for name, ok in checks.items():
    print(f"{'✓' if ok else '✗'} {name}")
all_ok = all(checks.values())
print(f"\n{'✓ Monitoring stack healthy' if all_ok else '✗ Issues detected'}")
sys.exit(0 if all_ok else 1)
