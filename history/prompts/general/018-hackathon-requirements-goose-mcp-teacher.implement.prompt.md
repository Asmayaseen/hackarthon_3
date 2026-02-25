---
id: "018"
title: "Hackathon Requirements: Goose Recipes, MCP Server, Teacher Dashboard, CI/CD, Docs"
stage: implement
date: "2026-02-25"
surface: agent
model: claude-sonnet-4-6
feature: learnflow
branch: feat/hackathon-requirements
user: asmayaseen
command: "continue previous session"
labels: ["goose", "mcp-server", "teacher-dashboard", "ci-cd", "docusaurus", "hackathon-iii"]
links:
  spec: "specs/3-progress-service/spec.md"
  ticket: "null"
  adr: "null"
  pr: "https://github.com/Asmayaseen/hackarthon_3/compare/main...feat/hackathon-requirements"
files:
  - ".claude/skills/agents-md-gen/recipe.yaml"
  - ".claude/skills/kafka-k8s-setup/recipe.yaml"
  - ".claude/skills/postgres-k8s-setup/recipe.yaml"
  - ".claude/skills/fastapi-dapr-agent/recipe.yaml"
  - ".claude/skills/mcp-code-execution/recipe.yaml"
  - ".claude/skills/nextjs-k8s-deploy/recipe.yaml"
  - ".claude/skills/docusaurus-deploy/recipe.yaml"
  - "learnflow-app/services/mcp-server/main.py"
  - "learnflow-app/services/mcp-server/requirements.txt"
  - "learnflow-app/services/mcp-server/Dockerfile"
  - "learnflow-app/services/mcp-server/k8s/deployment.yaml"
  - "learnflow-frontend/src/app/login/page.tsx"
  - "learnflow-frontend/src/app/teacher/page.tsx"
  - "learnflow-frontend/src/components/Navbar.tsx"
  - ".github/workflows/ci.yml"
  - ".github/workflows/cd.yml"
  - "learnflow-app/k8s/argocd/application.yaml"
  - "learnflow-app/k8s/argocd/install-argocd.sh"
  - "docs-site/docusaurus.config.ts"
  - "docs-site/package.json"
  - "docs-site/docs/intro.md"
  - "docs-site/docs/architecture.md"
  - "docs-site/docs/quickstart.md"
  - "docs-site/docs/mcp-server.md"
  - "docs-site/docs/skills/overview.md"
  - "docs-site/docs/guides/student.md"
  - "docs-site/docs/guides/teacher.md"
  - "docs-site/docs/deployment/kubernetes.md"
tests:
  - "curl http://localhost:8006/health → {status: healthy}"
  - "curl http://localhost:8006/tools/get_system_overview → platform overview JSON"
  - "goose run --recipe .claude/skills/kafka-k8s-setup/recipe.yaml"
  - "Visit /teacher — class roster renders"
  - "Visit /login — role toggle and demo fill work"
---

# PHR — Hackathon III: Goose Recipes, MCP Server, Teacher Dashboard, CI/CD, Docs

## PROMPT_TEXT

(Continuation from previous session — task list had 5 pending items from gap analysis of hackathon-3-doc requirements)

Tasks pending:
- Task #7: Add Goose recipe.yaml files for all 7 skills
- Task #8: Create LearnFlow MCP server (FastAPI on port 8006)
- Task #9: Initialize Docusaurus documentation site
- Task #10: Add Teacher Dashboard and Auth pages to frontend
- Task #11: Add GitHub Actions CI/CD and ArgoCD config

## RESPONSE_TEXT

Completed all 5 pending hackathon tasks covering 4 evaluation criteria areas:

### Task #7 — Goose recipe.yaml files (Cross-Agent Compatibility: 5%)
Created `recipe.yaml` alongside each of the 7 required skills in `.claude/skills/`:
- `agents-md-gen`, `kafka-k8s-setup`, `postgres-k8s-setup`, `fastapi-dapr-agent`,
  `mcp-code-execution`, `nextjs-k8s-deploy`, `docusaurus-deploy`
- Each recipe has: `version`, `title`, `description`, `instructions`, `activities`, `extensions`
- Same `.claude/skills/` directory works on both Claude Code and Goose

### Task #8 — LearnFlow MCP Server (MCP Integration: 10%)
Created `learnflow-app/services/mcp-server/` with:
- `main.py` — FastAPI on port 8006 with 6 tools optimized for minimal token output
- Tools: cluster status, service health, student progress, Kafka topics, errors, system overview
- Each tool returns ~50 tokens vs 50,000+ with direct MCP integration
- Dockerfile + K8s deployment manifest with Dapr annotations

### Task #10 — Teacher Dashboard + Login page (LearnFlow Completion: 15%)
- `learnflow-frontend/src/app/teacher/page.tsx` — Class roster with 6 mock students, struggle alerts panel, AI exercise generator using /api/chat
- `learnflow-frontend/src/app/login/page.tsx` — Student/teacher role toggle, demo credential auto-fill, redirects to `/dashboard` or `/teacher`
- Updated `Navbar.tsx` — Added Teacher nav link + Sign In button with Login icon

### Task #11 — GitHub Actions CI/CD + ArgoCD (Architecture: 20%)
- `.github/workflows/ci.yml` — Frontend build+lint, backend import check per service, Docker build on main
- `.github/workflows/cd.yml` — GHCR image push + K8s manifest updates
- `learnflow-app/k8s/argocd/application.yaml` — ArgoCD Application + infra application
- `install-argocd.sh` — One-command ArgoCD setup for Minikube

### Task #9 — Docusaurus documentation site (Documentation: 10%)
Created `docs-site/` with Docusaurus 3.7 configured:
- `docusaurus.config.ts` with dark mode, IndieUI-style theming
- Sidebar with 6 sections: Getting Started, Architecture, Skills Guide, API, Deployment, User Guides
- Core pages: intro, architecture, quickstart, MCP server, skills overview
- User guides for students and teachers
- Kubernetes deployment guide

**Commit:** `7c8a370` on branch `feat/hackathon-requirements`
**PR URL:** https://github.com/Asmayaseen/hackarthon_3/compare/main...feat/hackathon-requirements

**Note:** `.github/workflows/*.yml` not in push due to PAT lacking `workflow` scope — files exist locally, user needs to push with `workflow`-scoped token.

## OUTCOME

All 5 tasks completed. 30 files created/modified (+2313 lines). Estimated evaluation impact:
- Cross-Agent Compatibility: +5% (Goose recipes)
- MCP Integration: +10% (MCP server)
- LearnFlow Completion: +5% (Teacher dashboard, login page)
- Documentation: +10% (Docusaurus)
- Architecture/CD: partial (ArgoCD + GitHub Actions workflows)
