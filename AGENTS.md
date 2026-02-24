# AGENTS.md — LearnFlow Platform

> AI Agent Context File | Hackathon III: Reusable Intelligence & Cloud-Native Mastery

## Overview
LearnFlow is an **AI-powered Python tutoring platform** built on cloud-native microservices.
Students chat with specialized AI agents, write code in Monaco Editor, take quizzes, and
track mastery progress. Teachers monitor class performance and assign custom exercises.

**Development Philosophy**: Skills are the product. Don't write code manually — write Skills
that teach Claude Code and Goose to build autonomously (MCP Code Execution pattern).

## Repository Structure
```
hackathon-3-all-phases/
├── .claude/skills/          # 7 hackathon skills + 40+ framework skills
│   ├── agents-md-gen/       # Generate AGENTS.md files
│   ├── kafka-k8s-setup/     # Deploy Kafka on Kubernetes
│   ├── postgres-k8s-setup/  # Deploy PostgreSQL + migrations
│   ├── fastapi-dapr-agent/  # Scaffold FastAPI + Dapr microservices
│   ├── mcp-code-execution/  # MCP code execution pattern
│   ├── nextjs-k8s-deploy/   # Deploy Next.js to Kubernetes
│   └── docusaurus-deploy/   # Deploy documentation site
├── learnflow-app/           # Main application
│   ├── services/            # 6 FastAPI microservices
│   ├── k8s/                 # Kubernetes manifests
│   ├── dapr-components/     # Dapr pub/sub configuration
│   ├── deploy.sh            # One-command deployment
│   └── verify.py            # Deployment verification
├── learnflow-frontend/      # Next.js + Monaco Editor UI
├── specs/                   # Feature specifications (SDD)
│   ├── 1-learnflow-core-services/
│   ├── 2-exercise-service/
│   ├── 3-progress-service/
│   └── 4-frontend-integration/
└── docs/                    # Documentation
    └── skill-development-guide.md
```

## Microservices Architecture
| Service | Port | Topic In | Topic Out | Purpose |
|---------|------|----------|-----------|---------|
| triage-service | 8000 | — | learning.query.explain, code.debug.request, etc. | Routes student queries |
| concepts-service | 8001 | learning.query.explain | learning.response.explanation | Explains Python concepts |
| debug-service | 8002 | code.debug.request | code.debug.response | Progressive debugging hints |
| exercise-service | 8004 | exercise.generate | exercise.graded | Generates + auto-grades exercises |
| code-review-service | 8003 | code.review.request | code.review.completed | PEP 8 + quality analysis |
| progress-service | 8005 | progress.update | struggle.alert | Mastery tracking + struggle detection |

## Development Commands
```bash
# Start local Kubernetes cluster
minikube start --cpus=4 --memory=8192 --driver=docker

# Deploy entire LearnFlow platform (one command)
cd learnflow-app && ./deploy.sh

# Verify deployment health
python learnflow-app/verify.py

# Check all pods
kubectl get pods -n learnflow

# Port-forward frontend
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow

# Port-forward a backend service for testing
kubectl port-forward svc/triage-service 8000:80 -n learnflow

# View logs
kubectl logs -l app=triage-service -n learnflow --tail=50

# Check Dapr components
kubectl get components -n learnflow
```

## Skills Usage
Use skills from `.claude/skills/` for all infrastructure tasks:
```bash
# Deploy Kafka
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh
python .claude/skills/kafka-k8s-setup/scripts/verify.py

# Deploy PostgreSQL
bash .claude/skills/postgres-k8s-setup/scripts/deploy.sh
python .claude/skills/postgres-k8s-setup/scripts/migrate.py

# Scaffold new microservice
bash .claude/skills/fastapi-dapr-agent/scripts/scaffold.sh quiz-service 8006

# Deploy frontend
bash .claude/skills/nextjs-k8s-deploy/scripts/deploy.sh all

# Deploy docs
bash .claude/skills/docusaurus-deploy/scripts/deploy.sh
```

## Coding Conventions
- **Python**: PEP 8, type hints required, async/await for all I/O
- **TypeScript**: strict mode, functional components, no `any`
- **APIs**: FastAPI + Pydantic v2, auto-generated OpenAPI docs
- **Events**: Always use Dapr pub/sub (never direct Kafka client)
- **Secrets**: Kubernetes secrets only — never hardcode
- **Tests**: pytest for backend, vitest for frontend
- **Commits**: `"Service: imperative action"` (e.g., `"Triage: add quiz routing"`)

## Business Rules (CRITICAL)
```
Mastery Score = 40% exercise completion
              + 30% quiz scores
              + 20% code quality ratings
              + 10% consistency (streak)

Levels: 0-40% Beginner | 41-70% Learning | 71-90% Proficient | 91-100% Mastered
```

## Struggle Detection — Triggers Alert
- Same error type 3+ times in a session
- Stuck on exercise > 10 minutes
- Quiz score < 50%
- Student says "I don't understand" or "I'm stuck"
- 5+ failed code executions in a row

## Kafka Event Topics
```
learning.query.explain        → concepts-service
learning.query.unclassified   → logging
code.debug.request            → debug-service
code.debug.response           → frontend
exercise.generate             → exercise-service
exercise.graded               → progress-service
code.review.request           → code-review-service
code.review.completed         → frontend
progress.update               → progress-service
progress.summary              → frontend
struggle.alert                → teacher dashboard
learning.response.explanation → frontend
```

## AI Agent Notes
- Dapr sidecar listens on port 3500 inside every container
- Services communicate via Dapr pub/sub, NOT direct HTTP between services
- All services read `OPENAI_API_KEY` from Kubernetes secret `openai-secret`
- Run `python verify.py` after any infrastructure change
- Skills in `.claude/skills/` each have `scripts/verify.py` — run these to check state
- MCP Code Execution: scripts execute outside context (0 tokens), only result enters context

## Environment Variables (per service)
```
OPENAI_API_KEY     - From K8s secret openai-secret
DAPR_HTTP_PORT     - 3500 (Dapr sidecar)
DAPR_PUBSUB_NAME   - kafka-pubsub
PORT               - Service-specific port
```

## Spec-Driven Development Workflow
1. `specs/<feature>/spec.md` — Define requirements
2. `/sp.plan` — Generate architecture plan
3. `/sp.tasks` — Break into testable tasks
4. `/sp.implement` — Execute implementation
5. PHR auto-created after every step
