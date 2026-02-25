#!/usr/bin/env python3
"""Validate that all required Skills have SKILL.md and recipe.yaml."""
import os, sys

SKILLS_DIR = ".claude/skills"
REQUIRED_SKILLS = [
    "agents-md-gen", "kafka-k8s-setup", "postgres-k8s-setup",
    "fastapi-dapr-agent", "mcp-code-execution", "nextjs-k8s-deploy",
    "docusaurus-deploy", "k8s-foundation", "prometheus-grafana-setup",
    "argocd-app-deployment", "dapr-pubsub-binding", "kong-api-gateway",
    "better-auth-setup", "huggingface-deploy",
]

passed = 0
for skill in REQUIRED_SKILLS:
    path = os.path.join(SKILLS_DIR, skill)
    has_skill = os.path.exists(os.path.join(path, "SKILL.md"))
    has_recipe = os.path.exists(os.path.join(path, "recipe.yaml"))
    ok = has_skill and has_recipe
    if ok:
        passed += 1
    print(f"  {'✓' if ok else '✗'} {skill} (SKILL.md={'✓' if has_skill else '✗'} recipe.yaml={'✓' if has_recipe else '✗'})")

print(f"\n{'✓' if passed == len(REQUIRED_SKILLS) else '⚠'} {passed}/{len(REQUIRED_SKILLS)} skills valid")
sys.exit(0 if passed == len(REQUIRED_SKILLS) else 1)
