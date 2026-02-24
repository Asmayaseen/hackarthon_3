---
name: kafka-k8s-setup
description: Deploy Apache Kafka on Kubernetes for LearnFlow event-driven microservices
triggers:
  - "deploy kafka"
  - "setup kafka"
  - "install kafka on kubernetes"
  - "kafka not running"
  - "set up event streaming"
---

# Kafka Kubernetes Setup

## When to Use
- Setting up event-driven messaging for LearnFlow services
- Kafka pods not running or unreachable
- Adding new Kafka topics for services
- First-time cluster setup

## Instructions

1. Deploy Kafka cluster:
   ```bash
   bash scripts/deploy.sh
   ```

2. Create LearnFlow topics:
   ```bash
   bash scripts/create-topics.sh
   ```

3. Verify all pods are running:
   ```bash
   python scripts/verify.py
   ```

4. Confirm topics exist before proceeding.

## Kafka Topics for LearnFlow
| Topic | Publisher | Consumer |
|-------|-----------|---------|
| `learning.query.explain` | triage | concepts |
| `code.debug.request` | triage | debug |
| `exercise.generate` | triage | exercise |
| `code.review.request` | triage | code-review |
| `progress.update` | all | progress |
| `struggle.alert` | progress | frontend |

## Validation
- [ ] All Kafka pods in Running state
- [ ] All 6 LearnFlow topics created
- [ ] Producer/consumer test passes
- [ ] Dapr pub/sub component connected

See [REFERENCE.md](./REFERENCE.md) for advanced configuration and troubleshooting.
