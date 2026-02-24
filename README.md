# LearnFlow Platform

> Hackathon III: Reusable Intelligence and Cloud-Native Mastery
> Built with Skills + MCP Code Execution Pattern

**LearnFlow** is an AI-powered Python tutoring platform built on cloud-native microservices.
Students chat with specialized AI tutors, write code in Monaco Editor, take quizzes, and track
mastery progress. Teachers monitor class performance and assign custom exercises.

## Architecture

```
┌──────────────────────────────────────────────────────────┐
│                   KUBERNETES CLUSTER                     │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐           │
│  │ Next.js  │    │ Triage   │    │ Concepts │           │
│  │ Frontend │    │ Service  │    │ Service  │           │
│  │+Monaco   │    │+Dapr+AI  │    │+Dapr+AI  │           │
│  └────┬─────┘    └────┬─────┘    └────┬─────┘           │
│       │               │               │                  │
│       └───────────────┴───────────────┘                  │
│                       ▼                                  │
│  ┌─────────────────────────────────────────────────┐     │
│  │                   KAFKA                         │     │
│  │  learning.* | code.* | exercise.* | struggle.*  │     │
│  └──────────────────┬──────────────────────────────┘     │
│          ┌──────────┴──────────┐                         │
│          ▼                     ▼                         │
│  ┌──────────────┐    ┌──────────────────┐                │
│  │  PostgreSQL  │    │  Debug/Exercise/ │                │
│  │  (Progress   │    │  CodeReview/     │                │
│  │   tracking)  │    │  Progress Svcs   │                │
│  └──────────────┘    └──────────────────┘                │
└──────────────────────────────────────────────────────────┘
```

## Quick Start

```bash
# 1. Start Kubernetes
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Set your OpenAI API key
export OPENAI_API_KEY=your-key-here

# 3. Deploy everything
cd learnflow-app && ./deploy.sh

# 4. Verify
python verify.py

# 5. Open LearnFlow
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow
# Visit: http://localhost:3000
```

## Microservices

| Service | Port | Purpose |
|---------|------|---------|
| triage-service | 8000 | Routes student queries to specialists |
| concepts-service | 8001 | Explains Python concepts adaptively |
| debug-service | 8002 | Progressive debugging hints (3 levels) |
| code-review-service | 8003 | PEP 8 + code quality analysis |
| exercise-service | 8004 | Generates + auto-grades Python exercises |
| progress-service | 8005 | Tracks mastery, detects struggle |
| learnflow-frontend | 3000 | Next.js + Monaco Editor UI |

## Skills Library (MCP Code Execution Pattern)

All infrastructure is deployed via AI Skills — reusable agent capabilities that achieve
**80-98% token reduction** vs direct MCP integration.

```
.claude/skills/
├── agents-md-gen/        # Generate AGENTS.md files
├── kafka-k8s-setup/      # Deploy Kafka + create topics
├── postgres-k8s-setup/   # Deploy PostgreSQL + migrations
├── fastapi-dapr-agent/   # Scaffold new microservices
├── mcp-code-execution/   # MCP code execution pattern
├── nextjs-k8s-deploy/    # Deploy Next.js to K8s
└── docusaurus-deploy/    # Deploy documentation site
```

### Using Skills with Claude Code or Goose

```bash
# Single prompt → autonomous deployment (no manual intervention):
"Deploy Kafka for LearnFlow"
# → Loads kafka-k8s-setup/SKILL.md (~100 tokens)
# → Runs scripts/deploy.sh (0 tokens in context)
# → Returns "✓ Kafka deployed" (~8 tokens)
# Total: ~108 tokens vs ~50,000 with direct MCP
```

## Tech Stack

| Layer | Technology |
|-------|-----------|
| AI Agents | Claude Code + Goose |
| Frontend | Next.js 14 + Monaco Editor + TypeScript |
| Backend | FastAPI + Python 3.11 |
| AI/LLM | OpenAI GPT-4o-mini |
| Service Mesh | Dapr (pub/sub, state) |
| Messaging | Apache Kafka |
| Database | PostgreSQL (CloudNativePG) |
| Orchestration | Kubernetes + Helm |
| Containerization | Docker (multi-stage) |

## Development Workflow

This project uses **Spec-Driven Development (SDD)** with SpecKit Plus:

```bash
# 1. Write spec
specs/<feature>/spec.md

# 2. Plan architecture
/sp.plan

# 3. Generate tasks
/sp.tasks

# 4. Let AI implement
/sp.implement
```

## Requirements

- Minikube (local Kubernetes)
- Docker Desktop
- Helm 3.x
- kubectl
- OpenAI API key
- Claude Code or Goose

## Verification

```bash
python learnflow-app/verify.py
```

Expected output:
```
✓ All pods running
✓ Dapr sidecars attached
✓ PostgreSQL connected
✓ Kafka pub/sub component exists
✓ Progress service healthy
✓ Struggle detection working
```

## Documentation

- Architecture docs: `specs/`
- Skills guide: `docs/skill-development-guide.md`
- AGENTS.md: AI agent context file
- API contracts: `specs/*/contracts/openapi.yaml`

## License

MIT — Built for Hackathon III: Reusable Intelligence and Cloud-Native Mastery
