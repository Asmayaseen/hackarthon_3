# AGENTS.md Format Reference

## Structure

```markdown
# AGENTS.md — [Project Name]

## Overview
Brief description of the project and its purpose.

## Repository Structure
\`\`\`
project/
├── services/        # Microservices
├── frontend/        # UI application
├── specs/           # Feature specifications
└── .claude/skills/  # AI agent skills
\`\`\`

## Tech Stack
- **Backend**: FastAPI + Python 3.11
- **Frontend**: Next.js + TypeScript
- **Messaging**: Kafka via Dapr
- **Orchestration**: Kubernetes + Helm

## Development Commands
\`\`\`bash
# Start local cluster
minikube start --cpus=4 --memory=8192

# Deploy all services
./deploy.sh

# Verify deployment
python verify.py

# Run tests
pytest services/*/tests/
\`\`\`

## Coding Conventions
- Python: PEP 8, type hints required, async/await for IO
- TypeScript: strict mode, functional components
- Commits: "Service: action description"
- PRs: must include tests and docs

## Service Endpoints
| Service | Port | Purpose |
|---------|------|---------|
| Triage | 8000 | Query routing |
| Concepts | 8001 | Explanations |
| Debug | 8002 | Error hints |

## AI Agent Notes
- Always use Dapr pub/sub for inter-service communication
- Never hardcode secrets; use Kubernetes secrets
- Run verify.py after any deployment change
- Skills in .claude/skills/ teach agents new capabilities
```

## Key Principles for AGENTS.md
1. **Actionable**: Every section should help AI complete tasks
2. **Precise**: Exact commands, not vague descriptions
3. **Current**: Reflects actual codebase state
4. **Concise**: Under 200 lines for fast loading
