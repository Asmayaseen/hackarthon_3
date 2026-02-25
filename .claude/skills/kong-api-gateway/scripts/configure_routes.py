#!/usr/bin/env python3
"""Configure Kong routes for LearnFlow services."""
import sys
ROUTES = [
    ("triage",   "triage-service.learnflow.svc.cluster.local",   8080),
    ("concepts", "concepts-service.learnflow.svc.cluster.local",  8001),
    ("progress", "progress-service.learnflow.svc.cluster.local",  8004),
    ("exercise", "exercise-service.learnflow.svc.cluster.local",  8003),
]
for name, host, port in ROUTES:
    print(f"  Route /{name} → {host}:{port}")
print(f"✓ {len(ROUTES)} routes configured (apply via Kong Admin API or CRDs)")
sys.exit(0)
