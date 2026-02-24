#!/usr/bin/env python3
"""Generate AGENTS.md file from repository analysis."""
import json
import argparse
from pathlib import Path
from datetime import date


def format_tree(tree: dict, indent: int = 0) -> str:
    """Format directory tree as text."""
    lines = []
    items = list(tree.items())
    for i, (name, subtree) in enumerate(items):
        is_last = (i == len(items) - 1)
        prefix = '└── ' if is_last else '├── '
        lines.append('│   ' * indent + prefix + name)
        if subtree:
            lines.extend(format_tree(subtree, indent + 1).splitlines())
    return '\n'.join(lines)


def generate_agents_md(analysis: dict) -> str:
    """Generate AGENTS.md content from analysis."""
    services = analysis.get('services', [])
    tech_stack = analysis.get('tech_stack', {})
    skills = analysis.get('skills', [])

    service_table = '\n'.join([
        f"| {s['name'].replace('-service', '').title()} | {8000 + i} | AI tutoring agent |"
        for i, s in enumerate(services)
    ])

    skills_list = '\n'.join([f"- `{s}`" for s in skills[:10]])

    tech_lines = '\n'.join([
        f"- **{k.replace('_', ' ').title()}**: {v}"
        for k, v in tech_stack.items()
    ])

    content = f"""# AGENTS.md — LearnFlow Platform

> Generated: {date.today().isoformat()} | AI Agent Context File

## Overview
LearnFlow is an AI-powered Python tutoring platform built on cloud-native microservices.
Students chat with specialized AI tutors, write code in Monaco Editor, take quizzes,
and track their mastery progress. Teachers monitor class performance and assign exercises.

This repository follows **Spec-Driven Development (SDD)** using Skills with MCP Code Execution.
AI agents should use skills in `.claude/skills/` to build and deploy components.

## Repository Structure
```
{format_tree(analysis.get('tree', {}))}
```

## Tech Stack
{tech_lines if tech_lines else "- Python/FastAPI (backend)\n- Next.js/TypeScript (frontend)\n- Kubernetes + Helm (orchestration)\n- Apache Kafka via Dapr (messaging)\n- Docker (containerization)"}

## AI Agent Services
| Service | Port | Purpose |
|---------|------|---------|
{service_table if service_table else "| triage-service | 8000 | Routes student queries to specialized agents |\n| concepts-service | 8001 | Explains Python concepts adaptively |\n| debug-service | 8002 | Provides progressive debugging hints |\n| exercise-service | 8004 | Generates and auto-grades coding challenges |\n| code-review-service | 8003 | Analyzes code quality (PEP 8) |\n| progress-service | 8005 | Tracks mastery scores, detects struggles |"}

## Development Commands
```bash
# Start local Kubernetes cluster
minikube start --cpus=4 --memory=8192 --driver=docker

# Deploy entire LearnFlow platform
cd learnflow-app && ./deploy.sh

# Verify deployment health
python learnflow-app/verify.py

# Check all pods
kubectl get pods -n learnflow

# Port-forward frontend for testing
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow

# View service logs
kubectl logs -l app=triage-service -n learnflow --tail=50
```

## Available Skills (Use These!)
{skills_list if skills_list else "- `agents-md-gen`\n- `kafka-k8s-setup`\n- `postgres-k8s-setup`\n- `fastapi-dapr-agent`\n- `mcp-code-execution`\n- `nextjs-k8s-deploy`\n- `docusaurus-deploy`"}

## Coding Conventions
- **Python**: PEP 8, type hints required, async/await for all I/O operations
- **TypeScript**: strict mode enabled, functional React components only
- **API**: FastAPI with Pydantic v2 models, OpenAPI auto-generated
- **Events**: Always publish via Dapr pub/sub (never direct Kafka client calls)
- **Secrets**: Kubernetes secrets only — never hardcode credentials
- **Commits**: "Service: imperative action" (e.g., "Triage: add quiz routing")

## Spec-Driven Development Workflow
1. Write spec: `specs/<feature>/spec.md`
2. Create plan: Run `/sp.plan`
3. Generate tasks: Run `/sp.tasks`
4. Implement: Run `/sp.implement`
5. Create PHR: Automatic after every step

## Mastery Business Rules
```
Topic Mastery = 40% exercise completion + 30% quiz scores
              + 20% code quality ratings + 10% consistency

Levels: 0-40% Beginner | 41-70% Learning | 71-90% Proficient | 91-100% Mastered
```

## Struggle Detection Triggers
- Same error type 3+ times
- Stuck on exercise > 10 minutes
- Quiz score < 50%
- Student says "I don't understand" or "I'm stuck"
- 5+ failed code executions in a row

## Event Topics (Kafka via Dapr)
| Topic | Publisher | Consumer |
|-------|-----------|---------|
| `learning.query.explain` | triage | concepts |
| `code.debug.request` | triage | debug |
| `exercise.generate` | triage | exercise |
| `code.review.request` | triage | code-review |
| `progress.update` | all services | progress |
| `struggle.alert` | progress | frontend |

## AI Agent Notes
- Use `learnflow-k8s-deployer` skill for full platform deployment
- Use `kafka-k8s-setup` skill to deploy/verify Kafka
- Use `postgres-k8s-setup` skill for database setup
- Use `fastapi-dapr-agent` skill to scaffold new microservices
- Always run `python verify.py` after deployment changes
- Dapr sidecar port is always 3500 inside containers
"""
    return content


def main():
    parser = argparse.ArgumentParser(description='Generate AGENTS.md from repo analysis')
    parser.add_argument('--output', default='AGENTS.md', help='Output file path')
    parser.add_argument('--analysis', default='.repo-analysis.json', help='Analysis JSON file')
    args = parser.parse_args()

    root = Path.cwd()
    analysis_file = root / args.analysis

    if analysis_file.exists():
        with open(analysis_file) as f:
            analysis = json.load(f)
    else:
        print(f"Analysis file not found: {analysis_file}")
        print("Run: python scripts/analyze_repo.py first")
        print("Generating with defaults...")
        analysis = {}

    content = generate_agents_md(analysis)
    output_path = root / args.output
    with open(output_path, 'w') as f:
        f.write(content)

    print(f"AGENTS.md generated at: {output_path}")
    print(f"Lines: {len(content.splitlines())}")


if __name__ == '__main__':
    main()
