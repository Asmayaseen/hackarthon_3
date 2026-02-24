# ADR-001: Event-Driven Architecture with Dapr and Kafka

**Date**: 2026-01-20
**Status**: Accepted
**Champions**: Claude (AI Assistant)

## Context

The LearnFlow platform requires multiple AI agents (Triage, Concepts, Debug, Code Review, Exercise, Progress) to communicate seamlessly while maintaining loose coupling and horizontal scalability. Traditional direct HTTP/API calls would create tight coupling and prevent independent deployment.

### Problems with Synchronous Communication

- **Tight Coupling**: Services would depend on each other's availability
- **Blocking Operations**: One slow service affects the entire system
- **Difficult Scaling**: Cannot scale services independently based on load
- **Single Point of Failure**: One service failure can cascade
- **Deployment Coupling**: Must deploy all services together

## Decision

We will implement an **event-driven architecture** where all communication between AI agents occurs through Dapr pub/sub components with Kafka as the underlying message broker.

### Implementation Details

**Technology Stack**:
- Dapr (Distributed Application Runtime) as the abstraction layer
- Kafka as the message broker (single-node for Minikube, clustered for production)
- Event-driven communication via publish/subscribe pattern
- Stateless services with no direct service-to-service HTTP calls

**Event Flow**:
1. Triage-Service classifies query → Publishes to `learning.query.explain` topic
2. Concepts-Service subscribes → Consumes from topic → Generates explanation
3. Concepts-Service publishes response to `learning.response.explanation` topic
4. Frontend or Progress Service consumes responses for display/storage

**Dapr Component Configuration**:
- Located at: `learnflow-app/dapr-components/kafka-pubsub.yaml`
- Configured topics:
  - `learning.query.explain`
  - `learning.query.routed`
  - `learning.response.explanation`
  - `code.debug.request`
  - `code.review.request`
  - `exercise.generate`
  - `progress.summary`
  - `struggle.detected`

## Rationale

### Pros

✅ **Loose Coupling**: Services don't know about each other's existence
✅ **Independent Scaling**: Scale Triage-Service and Concepts-Service independently
✅ **Resilience**: One service failure doesn't affect others
✅ **Independent Deployment**: Deploy services separately without downtime
✅ **Extensibility**: Easy to add new agents by subscribing to existing topics
✅ **Observability**: Events can be traced through the system
✅ **Replayability**: Can replay events for debugging or analysis
✅ **Dapr Abstraction**: Can switch from Kafka to Redis without code changes

### Cons

❌ **Eventual Consistency**: Not immediate response (requires async UX)
❌ **Complexity**: More complex than simple HTTP calls
❌ **Debugging**: Harder to trace request-response flow
❌ **Testing**: Requires integration testing with message broker
❌ **Operational Overhead**: Need to manage Kafka cluster

### Trade-offs

We accept the operational complexity and debugging challenges in exchange for:
- Highly scalable system that can handle 100+ concurrent students
- Ability to evolve agents independently as we learn from production usage
- Foundation for future multi-cloud deployment
- Compliance with Constitution Article III (event-driven microservices)

## Alternatives Considered

### Alternative 1: Direct HTTP Communication

**Description**: Services call each other directly via HTTP/REST APIs

**Rejected Because**:
- Violates Constitution Article III (stateless event-driven microservices)
- Creates tight coupling between agents
- No horizontal scalability
- Service mesh required for service discovery
- Single point of failure risk

### Alternative 2: gRPC with Service Mesh

**Description**: Use gRPC for synchronous calls with Istio/Linkerd for service mesh

**Rejected Because**:
- More complex than event-driven approach
- Still synchronous (blocking) communication
- Service mesh adds significant operational overhead
- Doesn't support replayability or event sourcing easily
- Doesn't align with event-driven curriculum tracking

## Consequences

### Positive

1. **Improved Scalability**: Can independently scale agents based on load patterns
2. **Better Resilience**: System degrades gracefully under partial failures
3. **Flexibility**: Easy to add new specialized agents (Debug, Review, Exercise, Progress)
4. **Event Sourcing**: All state changes captured as events for analytics and replay
5. **Constitutional Compliance**: Follows Article III mandates for Dapr + Kafka

### Negative

1. **Debugging Complexity**: Need distributed tracing to understand event flow
2. **Operational Knowledge**: Team must understand Kafka and Dapr operations
3. **Testing Infrastructure**: Need integration tests with Kafka/Dapr
4. **Event Ordering**: Must handle out-of-order events and duplicate messages
5. **Monitoring**: Need to monitor Kafka consumer lag and event delays

### Mitigation Strategies

1. **Distributed Tracing**: Implement correlation IDs in all events
2. **Observability**: Use Dapr observability features + Prometheus/Grafana
3. **Dead Letter Queues**: Route failed events to DLQ for manual review
4. **Idempotency**: All consumers must handle duplicate events gracefully
5. **Local Development**: Provide Docker Compose for local Kafka/Dapr

## References

- Constitution.md: Article III (Technical Stack & Infrastructure)
- Constitution.md: Article II (MCP Code Execution Pattern)
- Specification: specs/1-learnflow-core-services/spec.md
- Dapr Documentation: dapr.io
- Kafka Documentation: kafka.apache.org

## Status

✅ **Accepted** - Implementation complete with both Triage and Concepts services using Dapr + Kafka pub/sub pattern

## Related ADRs

- ADR-002: OpenAI Integration for Agent Intelligence
- ADR-004: Multi-Agent Specialized Architecture
