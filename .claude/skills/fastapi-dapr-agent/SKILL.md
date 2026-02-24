---
name: fastapi-dapr-agent
description: Scaffold a new FastAPI microservice with Dapr integration and OpenAI agent for LearnFlow
triggers:
  - "create new service"
  - "scaffold microservice"
  - "add fastapi service"
  - "new dapr agent"
  - "create tutoring agent"
---

# FastAPI + Dapr Agent Scaffolder

## When to Use
- Adding a new AI tutoring microservice to LearnFlow
- Creating a service that publishes/subscribes to Kafka events via Dapr
- Building an OpenAI-powered agent endpoint
- Setting up a new service with Kubernetes deployment

## Instructions

1. Scaffold new service from template:
   ```bash
   bash scripts/scaffold.sh <service-name> <port>
   ```
   Example: `bash scripts/scaffold.sh quiz-service 8006`

2. Verify the scaffold is correct:
   ```bash
   python scripts/verify.py <service-name>
   ```

3. Build and load image:
   ```bash
   bash scripts/build.sh <service-name>
   ```

## What Gets Created
```
learnflow-app/services/<service-name>/
├── main.py           # FastAPI app with Dapr pub/sub + OpenAI agent
├── Dockerfile        # Multi-stage production build
├── requirements.txt  # Python dependencies
└── k8s/
    └── deployment.yaml  # Kubernetes manifest with Dapr annotations
```

## Service Template Pattern
- FastAPI with Pydantic v2 models
- Dapr pub/sub subscription endpoint (`/dapr/subscribe`)
- OpenAI GPT-4o-mini agent with system prompt
- Health check endpoint (`/health`)
- Publishes responses to Kafka topics via Dapr

## Validation
- [ ] Service directory created
- [ ] main.py has `/health`, `/dapr/subscribe` endpoints
- [ ] Dockerfile builds successfully
- [ ] K8s manifest has Dapr annotations
- [ ] requirements.txt has all dependencies

See [REFERENCE.md](./REFERENCE.md) for FastAPI + Dapr patterns and OpenAI agent setup.
