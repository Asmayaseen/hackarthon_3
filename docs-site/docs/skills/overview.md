---
id: overview
title: Skills Overview
sidebar_position: 1
---

# Skills Guide

LearnFlow was built using **7 reusable Skills** that work on both Claude Code and Goose.

## What are Skills?

Skills are the emerging standard for teaching AI agents capabilities:

```
.claude/skills/<skill-name>/
├── SKILL.md          # ~100 tokens — what the agent loads
├── recipe.yaml       # Goose compatibility
├── REFERENCE.md      # Deep docs — loaded only on demand
└── scripts/
    ├── deploy.sh     # 0 tokens — executed, never loaded
    ├── verify.py     # 0 tokens — returns minimal result
    └── ...
```

**Token efficiency:**
| Component | Tokens |
|-----------|--------|
| SKILL.md | ~100 |
| REFERENCE.md | 0 (on-demand) |
| scripts/ | 0 (executed) |
| Final output | ~10 |
| **Total** | **~110 vs 50,000+ with direct MCP** |

## Available Skills

| Skill | Purpose |
|-------|---------|
| [agents-md-gen](./agents-md-gen) | Generate AGENTS.md for repositories |
| [kafka-k8s-setup](./kafka-k8s-setup) | Deploy Kafka on Kubernetes |
| [postgres-k8s-setup](./postgres-k8s-setup) | Deploy PostgreSQL on Kubernetes |
| [fastapi-dapr-agent](./fastapi-dapr-agent) | Scaffold FastAPI + Dapr microservices |
| [mcp-code-execution](./mcp-code-execution) | Implement MCP Code Execution pattern |
| [nextjs-k8s-deploy](./nextjs-k8s-deploy) | Deploy Next.js to Kubernetes |
| [docusaurus-deploy](./docusaurus-deploy) | Deploy Docusaurus docs site |

## Cross-Agent Compatibility

All Skills work with **both Claude Code and Goose**:

```bash
# Claude Code
claude  # Skills auto-loaded from .claude/skills/

# Goose
goose run --recipe .claude/skills/kafka-k8s-setup/recipe.yaml
```

The same `.claude/skills/` directory serves both agents — no duplication needed.
