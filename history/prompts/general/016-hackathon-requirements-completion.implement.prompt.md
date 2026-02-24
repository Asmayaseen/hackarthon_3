---
id: 016
title: Hackathon Requirements Completion
stage: implement
date: 2026-02-24
surface: agent
model: claude-sonnet-4-6
feature: none
branch: 1-learnflow-core-services
user: asmayaseen
command: "hackathon-3-doc ko achi trhan se read karo aur mere project ko achi trhan se dekho aur document main jo jo requirment reh gayi hai wo pora karo"
labels: ["hackathon", "skills", "mcp-code-execution", "kubernetes", "dockerfiles", "agents-md"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .claude/skills/agents-md-gen/SKILL.md
  - .claude/skills/agents-md-gen/REFERENCE.md
  - .claude/skills/agents-md-gen/scripts/analyze_repo.py
  - .claude/skills/agents-md-gen/scripts/generate.py
  - .claude/skills/agents-md-gen/scripts/verify.py
  - .claude/skills/kafka-k8s-setup/SKILL.md
  - .claude/skills/kafka-k8s-setup/REFERENCE.md
  - .claude/skills/kafka-k8s-setup/scripts/deploy.sh
  - .claude/skills/kafka-k8s-setup/scripts/create-topics.sh
  - .claude/skills/kafka-k8s-setup/scripts/verify.py
  - .claude/skills/postgres-k8s-setup/SKILL.md
  - .claude/skills/postgres-k8s-setup/REFERENCE.md
  - .claude/skills/postgres-k8s-setup/scripts/deploy.sh
  - .claude/skills/postgres-k8s-setup/scripts/migrate.py
  - .claude/skills/postgres-k8s-setup/scripts/verify.py
  - .claude/skills/fastapi-dapr-agent/SKILL.md
  - .claude/skills/fastapi-dapr-agent/REFERENCE.md
  - .claude/skills/fastapi-dapr-agent/scripts/scaffold.sh
  - .claude/skills/fastapi-dapr-agent/scripts/verify.py
  - .claude/skills/mcp-code-execution/SKILL.md
  - .claude/skills/mcp-code-execution/REFERENCE.md
  - .claude/skills/mcp-code-execution/scripts/mcp_client.py
  - .claude/skills/mcp-code-execution/scripts/verify.py
  - .claude/skills/nextjs-k8s-deploy/SKILL.md
  - .claude/skills/nextjs-k8s-deploy/REFERENCE.md
  - .claude/skills/nextjs-k8s-deploy/scripts/deploy.sh
  - .claude/skills/nextjs-k8s-deploy/scripts/verify.py
  - .claude/skills/nextjs-k8s-deploy/templates/Dockerfile
  - .claude/skills/docusaurus-deploy/SKILL.md
  - .claude/skills/docusaurus-deploy/REFERENCE.md
  - .claude/skills/docusaurus-deploy/scripts/init.sh
  - .claude/skills/docusaurus-deploy/scripts/generate-docs.py
  - .claude/skills/docusaurus-deploy/scripts/deploy.sh
  - .claude/skills/docusaurus-deploy/scripts/verify.py
  - AGENTS.md
  - README.md
  - docs/skill-development-guide.md
  - learnflow-frontend/Dockerfile
  - learnflow-frontend/next.config.ts
  - learnflow-app/deploy.sh
  - learnflow-app/services/concepts-service/Dockerfile
  - learnflow-app/services/debug-service/Dockerfile
  - learnflow-app/services/debug-service/requirements.txt
  - learnflow-app/services/exercise-service/Dockerfile
  - learnflow-app/services/exercise-service/requirements.txt
  - learnflow-app/services/code-review-service/Dockerfile
  - learnflow-app/services/code-review-service/requirements.txt
  - learnflow-app/services/progress-service/Dockerfile
  - learnflow-app/services/progress-service/requirements.txt
tests:
  - "python .claude/skills/mcp-code-execution/scripts/verify.py (checks all hackathon skills)"
---

## Prompt

hackathon-3-doc ko achi trhan se read karo aur mere project ko achi trhan se dekho aur document main jo jo requirment reh gayi hai wo pora karo

## Response snapshot

Comprehensive gap analysis of hackathon requirements vs project state. Identified and implemented all missing items:

**7 Required Hackathon Skills Created** (with SKILL.md + REFERENCE.md + scripts/):
1. `agents-md-gen` - Generate AGENTS.md with analyze_repo.py + generate.py + verify.py
2. `kafka-k8s-setup` - Deploy Kafka with deploy.sh + create-topics.sh + verify.py
3. `postgres-k8s-setup` - Deploy PostgreSQL with deploy.sh + migrate.py + verify.py
4. `fastapi-dapr-agent` - Scaffold microservices with scaffold.sh + verify.py
5. `mcp-code-execution` - MCP pattern with mcp_client.py + verify.py
6. `nextjs-k8s-deploy` - Deploy Next.js with deploy.sh + verify.py + Dockerfile template
7. `docusaurus-deploy` - Deploy docs with init.sh + generate-docs.py + deploy.sh + verify.py

**Supporting Files**:
- `AGENTS.md` - Complete AI agent context file (150+ lines)
- `docs/skill-development-guide.md` - Comprehensive skill creation guide
- `learnflow-frontend/Dockerfile` - Multi-stage Next.js Docker build
- `learnflow-frontend/next.config.ts` - Added standalone output + API rewrites
- `learnflow-app/deploy.sh` - Updated to deploy all 6 services + frontend
- Dockerfiles + requirements.txt for: concepts, debug, exercise, code-review, progress services

## Outcome

- Impact: All 7 hackathon-required skills created with proper MCP Code Execution pattern (SKILL.md ~100 tokens + scripts executing outside context = 80-98% token reduction). All 6 microservices now have Dockerfiles. Complete AGENTS.md for AI agent navigation.
- Tests: python .claude/skills/mcp-code-execution/scripts/verify.py - checks all skills for compliance
- Files: 50+ files created/modified
- Next prompts: Test skills with Claude Code and Goose, deploy to Minikube, verify full platform
- Reflection: Hackathon 3 requirement is "Skills with MCP Code Execution" — not just skill documentation but actual executable scripts that do the heavy lifting outside agent context

## Evaluation notes (flywheel)

- Failure modes observed: None — all files created successfully
- Graders run and results: Bash verification script confirmed all 7 skills, 6 Dockerfiles, and key files present
- Prompt variant: N/A
- Next experiment: Test single-prompt-to-deployment for each skill with both Claude Code and Goose
