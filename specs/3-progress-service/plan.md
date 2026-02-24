# Implementation Plan: Progress Service (3-progress-service)

**Feature ID**: 3-progress-service
**Status**: Planning Complete
**Branch**: 3-progress-service

## 1. Scope and Dependencies
**In Scope**: Mastery calc (FR1), struggle detection (FR2-4), event processing (FR5), state storage (FR6), teacher API (FR7-8)
**Out of Scope**: Frontend dashboard, ML predictions
**Dependencies**: Kafka (pub/sub), Dapr (state/pubsub), Postgres (migrations via Alembic), other services publish events

## 2. Key Decisions
- **Stack**: FastAPI + SQLModel + Alembic + Dapr + Kafka (Constitution III)
- **State**: Dapr Postgres state store (key: student_id)
- **Events**: Consume learning.*, exercise.*, code.* → publish progress.updated, struggle.detected
**Rationale**: Event-driven, stateless microservice
**Alternatives**: Direct Postgres queries (rejected: Dapr mandate)

📋 ADR Suggestion: Dapr vs Direct Kafka? Run `/sp.adr dapr-kafka-integration` if needed.

## 3. Interfaces
- **Inbound**: Dapr pub/sub (Kafka topics), HTTP /health, /progress/{id}, /struggles
- **Outbound**: Dapr pub/sub (struggle.detected), state save
- **Errors**: 4xx client, 5xx internal; idempotent consumers
- OpenAPI: specs/3-progress-service/contracts/openapi.yaml

## 4. NFRs
- **Perf**: Event proc <500ms p95, API <200ms
- **Reliability**: At-least-once processing, dead-letter queue
- **Security**: JWT via Kong, no secrets in code
- **Cost**: Serverless Neon, managed Kafka

## 5. Data Management
- **Models**: SQLModel (StudentProgress, StruggleAlert)
- **Migrations**: Alembic init → autogenerate on model changes
- **Retention**: Events 7d (Kafka), state TTL 30d

## 6. Operational
- **Observability**: Structured logs (structlog), Prometheus metrics
- **Deployment**: Helm chart, ArgoCD
- **Health**: /health checks Dapr, Kafka, Postgres

## 7. Risks
- Event ordering → Mitigation: topic partitioning by student_id
- Dupe events → Idempotency via event_id
- Calc drift → Unit tests w/ fixtures

## 8. Evaluation
- **DoD**: All FRs pass quickstart.md, verify.py includes health/Postgres
- **Tests**: Unit (calc), integration (events)

Ready for `/sp.tasks` → `/sp.implement`
