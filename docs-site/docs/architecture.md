---
id: architecture
title: Platform Architecture
sidebar_position: 2
---

# Platform Architecture

## System Diagram

```
┌──────────────────────────────────────────────────────────────────┐
│                         KUBERNETES CLUSTER                       │
│  ┌─────────────────────────────────────────────────────────────┐ │
│  │  ┌─────────────┐    ┌─────────────┐    ┌─────────────┐     │ │
│  │  │   Next.js   │    │   Triage    │    │  Concepts   │     │ │
│  │  │  Frontend   │    │   Service   │    │   Service   │     │ │
│  │  │ +Monaco Ed  │    │   :8080     │    │   :8001     │     │ │
│  │  └──────┬──────┘    └──────┬──────┘    └──────┬──────┘     │ │
│  │         │                  │                  │            │ │
│  │         └──────────────────┼──────────────────┘            │ │
│  │                            ▼                               │ │
│  │  ┌─────────────────────────────────────────────────────┐   │ │
│  │  │                      KAFKA                          │   │ │
│  │  │  learning.* | code.* | exercise.* | struggle.*      │   │ │
│  │  └─────────────────────────────────────────────────────┘   │ │
│  │                            │                               │ │
│  │         ┌──────────────────┤──────────────────┐            │ │
│  │         ▼                  ▼                  ▼            │ │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐        │ │
│  │  │ PostgreSQL  │  │  Progress   │  │  MCP Server │        │ │
│  │  │   (CNPG)    │  │   :8004     │  │   :8006     │        │ │
│  │  └─────────────┘  └─────────────┘  └─────────────┘        │ │
│  └─────────────────────────────────────────────────────────────┘ │
└──────────────────────────────────────────────────────────────────┘
```

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| AI Agents | Claude Code + Goose | Execute Skills to build the platform |
| Frontend | Next.js 16 + Monaco | UI with code editor |
| Backend | FastAPI + OpenAI SDK | AI tutoring microservices |
| Auth | Better Auth | JWT authentication |
| Service Mesh | Dapr | Pub/sub, state, service invocation |
| Messaging | Kafka (Strimzi) | Event-driven communication |
| Database | PostgreSQL (CNPG) | Student data and progress |
| AI Context | MCP Server | Real-time platform context for agents |
| Orchestration | Kubernetes | Container management |
| CD | ArgoCD + GitHub Actions | GitOps continuous delivery |
| Docs | Docusaurus | This documentation site |

## Event Flow

When a student asks "How do for loops work?":

1. Frontend sends POST `/api/chat` to Next.js API route
2. API route forwards to **Triage Service** (`POST /answer`)
3. Triage classifies intent → `explain`
4. Publishes `{query}` to Kafka topic `learning.query.explain`
5. **Concepts Service** consumes the event
6. Concepts Agent generates explanation with code examples
7. Response published to `learning.response` topic
8. Frontend receives response via SSE or polling
9. **Progress Service** updates mastery score

## Dapr Pub/Sub

All services use Dapr sidecars for messaging:

```yaml
# Subscribe to Kafka via Dapr
POST /dapr/subscribe
→ returns: [{pubsubname: "kafka-pubsub", topic: "learning.query.explain", route: "/explain"}]
```

See [Kafka Topics](./kafka-topics) for complete topic mapping.
