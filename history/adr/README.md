# Architecture Decision Records

This directory contains Architecture Decision Records (ADRs) for the LearnFlow platform following Spec-Kit Plus and Constitution requirements.

## What are ADRs?

ADRs document significant architectural decisions made during the project, including:
- The context and problem
- The decision and implementation
- The rationale (pros/cons)
- Alternatives considered
- Consequences and trade-offs

## ADR Index

### Approved ADRs

| ADR | Title | Date | Status |
|-----|-------|------|--------|
| [ADR-001](001-event-driven-architecture-with-dapr-kafka.md) | Event-Driven Architecture with Dapr and Kafka | 2026-01-20 | ✅ Accepted |
| [ADR-002](002-openai-integration-for-agent-intelligence.md) | OpenAI Integration for Agent Intelligence | 2026-01-20 | ✅ Accepted |

### Proposed ADRs

| ADR | Title | Status |
|-----|-------|--------|
| ADR-003 | Neon PostgreSQL as Dapr State Store | 📝 Draft |
| ADR-004 | Multi-Agent Specialized Architecture | 📝 Draft |
| ADR-005 | Token Reduction via Code Execution Pattern | 📝 Draft |

## Creating New ADRs

To create a new ADR:

1. Copy the template from `.specify/templates/adr-template.md`
2. Name it `NNN-short-title.md` (NNN = next number)
3. Fill all sections with details
4. Update this README
5. Link to related ADRs

## Templates

- ADR Template: `.specify/templates/adr-template.md`
- Located in project root

## Constitution Reference

Per Constitution Article X (Development Guidelines):
> "All significant architectural decisions must be documented in ADRs per Spec-Kit Plus requirements"
