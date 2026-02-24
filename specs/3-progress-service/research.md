# Research for Progress Service

## Dapr + Kafka Pub/Sub Best Practices
- Decision: Use Dapr pub/sub component with Kafka backing (kafka-pubsub.yaml)
- Rationale: Constitution Section 3.03; abstracts broker details, handles retries/idempotency
- Alternatives: Direct Kafka client (confluent-kafka) - rejected for Dapr mandate

## Postgres Migrations with SQLModel
- Decision: Alembic for migrations, SQLModel for models
- Rationale: Schema evolution (Constitution 6.02), soft deletes
- Alternatives: SQLModel only (no migrations) - insufficient for prod

## Mastery Calc Implementation
- Decision: Weighted avg in Python service layer
- Rationale: Exact Article VI.04 formula; event-driven recalc
- Alternatives: DB stored proc - rejected for service logic

All clarifications resolved from spec/constitution.
