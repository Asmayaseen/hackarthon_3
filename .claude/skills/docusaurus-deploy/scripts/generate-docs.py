#!/usr/bin/env python3
"""Generate Docusaurus documentation from LearnFlow specs and code."""
import os
import shutil
from pathlib import Path
from datetime import date


def copy_specs_as_docs(root: Path, docs_dir: Path):
    """Convert spec files to Docusaurus docs."""
    specs_dir = root / 'specs'
    if not specs_dir.exists():
        print('⚠ specs/ directory not found')
        return 0

    count = 0
    arch_dir = docs_dir / 'docs' / 'architecture'
    arch_dir.mkdir(parents=True, exist_ok=True)

    for spec_feature in sorted(specs_dir.iterdir()):
        if not spec_feature.is_dir():
            continue
        for md_file in spec_feature.glob('*.md'):
            dest = arch_dir / f'{spec_feature.name}-{md_file.name}'
            shutil.copy2(md_file, dest)
            count += 1

    print(f'  ✓ Copied {count} spec files to docs/architecture/')
    return count


def generate_skills_doc(root: Path, docs_dir: Path):
    """Generate skills documentation."""
    skills_dir = root / '.claude' / 'skills'
    out_dir = docs_dir / 'docs' / 'skills'
    out_dir.mkdir(parents=True, exist_ok=True)

    hackathon_skills = [
        'agents-md-gen', 'kafka-k8s-setup', 'postgres-k8s-setup',
        'fastapi-dapr-agent', 'mcp-code-execution',
        'nextjs-k8s-deploy', 'docusaurus-deploy'
    ]

    content = f"""---
sidebar_position: 1
---

# Skills Library

LearnFlow uses MCP Code Execution Skills — reusable AI agent capabilities
that achieve 80-98% token reduction vs direct MCP integration.

## Hackathon Skills

| Skill | Purpose |
|-------|---------|
| `agents-md-gen` | Generate AGENTS.md for AI agent context |
| `kafka-k8s-setup` | Deploy Apache Kafka on Kubernetes |
| `postgres-k8s-setup` | Deploy PostgreSQL with migrations |
| `fastapi-dapr-agent` | Scaffold FastAPI + Dapr microservices |
| `mcp-code-execution` | Wrap MCP calls in efficient scripts |
| `nextjs-k8s-deploy` | Build and deploy Next.js to Kubernetes |
| `docusaurus-deploy` | Deploy documentation site |

## How Skills Work

```
SKILL.md (~100 tokens) → Agent loads instructions
scripts/*.py (0 tokens) → Executes externally
Result (~10 tokens) → Only this enters context
```

**Total: ~110 tokens vs 50,000+ with direct MCP**

## Using a Skill

In Claude Code or Goose:
```
Deploy Kafka for LearnFlow
```
The agent loads `kafka-k8s-setup` skill and runs:
```bash
bash scripts/deploy.sh     # 0 tokens
python scripts/verify.py   # returns "✓ All 3 pods running"
```

"""
    # Add individual skill details
    for skill_name in hackathon_skills:
        skill_dir = skills_dir / skill_name
        skill_md = skill_dir / 'SKILL.md'
        if skill_md.exists():
            skill_content = skill_md.read_text()
            # Extract description
            for line in skill_content.splitlines():
                if 'description:' in line:
                    desc = line.split('description:')[1].strip()
                    content += f"### `{skill_name}`\n{desc}\n\n"
                    break

    (out_dir / 'README.md').write_text(content)
    print(f'  ✓ Skills documentation generated')


def generate_api_docs(root: Path, docs_dir: Path):
    """Generate API reference from OpenAPI specs."""
    out_dir = docs_dir / 'docs' / 'api'
    out_dir.mkdir(parents=True, exist_ok=True)

    api_content = """---
sidebar_position: 1
---

# API Reference

LearnFlow exposes REST APIs from each microservice via Kubernetes services.

## Services

| Service | Internal URL | Port |
|---------|-------------|------|
| Triage | `http://triage-service.learnflow` | 80 |
| Concepts | `http://concepts-service.learnflow` | 80 |
| Debug | `http://debug-service.learnflow` | 80 |
| Exercise | `http://exercise-service.learnflow` | 80 |
| Code Review | `http://code-review-service.learnflow` | 80 |
| Progress | `http://progress-service.learnflow` | 80 |

## Triage Service

### POST /query
Route a student query to the appropriate AI agent.

**Request:**
```json
{
  "student_id": "uuid",
  "query_text": "How do for loops work?",
  "current_module_id": "module-2",
  "student_level": "beginner"
}
```

**Response:**
```json
{
  "classification": "explain",
  "confidence": 0.95,
  "reason": "Student asking for concept explanation",
  "routed_to": "concepts-service"
}
```

## Progress Service

### GET /progress/{student_id}
Get student mastery scores.

**Response:**
```json
{
  "student_id": "uuid",
  "overall_mastery": 68.5,
  "topics": {
    "variables": 85.0,
    "loops": 68.0,
    "functions": 52.0
  }
}
```

### POST /process-event
Update progress from a learning event.

See OpenAPI specs in `specs/*/contracts/` for full schema details.
"""
    (out_dir / 'README.md').write_text(api_content)
    print('  ✓ API documentation generated')


def generate_deployment_docs(root: Path, docs_dir: Path):
    """Generate deployment guide."""
    out_dir = docs_dir / 'docs' / 'deployment'
    out_dir.mkdir(parents=True, exist_ok=True)

    deploy_content = """---
sidebar_position: 1
---

# Deployment Guide

## Prerequisites

- Docker installed and running
- Minikube (local K8s)
- Helm 3.x
- kubectl
- OpenAI API key

## Quick Deploy

```bash
# 1. Start Kubernetes
minikube start --cpus=4 --memory=8192 --driver=docker

# 2. Deploy everything
cd learnflow-app && ./deploy.sh

# 3. Verify
python verify.py

# 4. Access frontend
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow
```

## Step-by-Step Deployment

### 1. Deploy Kafka
```bash
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh
python .claude/skills/kafka-k8s-setup/scripts/verify.py
```

### 2. Deploy PostgreSQL
```bash
bash .claude/skills/postgres-k8s-setup/scripts/deploy.sh
python .claude/skills/postgres-k8s-setup/scripts/migrate.py
```

### 3. Deploy Backend Services
```bash
cd learnflow-app
docker build -t triage-service:latest services/triage-service/
minikube image load triage-service:latest
kubectl apply -f k8s/deployments/
```

### 4. Deploy Frontend
```bash
bash .claude/skills/nextjs-k8s-deploy/scripts/deploy.sh all
```

## Verification

```bash
python learnflow-app/verify.py
```

Expected output:
```
✓ All pods running
✓ Dapr sidecars attached
✓ Kafka topics present
✓ Progress service healthy
```
"""
    (out_dir / 'README.md').write_text(deploy_content)
    print('  ✓ Deployment documentation generated')


def main():
    root = Path.cwd()
    docs_dir = root / 'learnflow-docs'

    if not docs_dir.exists():
        print('⚠ learnflow-docs/ not found. Run: bash scripts/init.sh first')
        docs_dir.mkdir(exist_ok=True)

    print('Generating LearnFlow documentation...')
    copy_specs_as_docs(root, docs_dir)
    generate_skills_doc(root, docs_dir)
    generate_api_docs(root, docs_dir)
    generate_deployment_docs(root, docs_dir)

    print(f'\n✓ Documentation generated in {docs_dir}')
    print('Next: bash scripts/deploy.sh')


if __name__ == '__main__':
    main()
