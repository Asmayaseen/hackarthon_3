---
name: dapr-pubsub-binding
description: Configure Dapr pub/sub components for event-driven communication between LearnFlow microservices via Kafka
triggers:
  - "configure dapr pubsub"
  - "dapr not publishing"
  - "setup dapr kafka"
  - "event not received"
  - "dapr subscription"
---

# Dapr Pub/Sub Binding

## When to Use
- Wiring event-driven communication between LearnFlow services
- Dapr subscriptions not receiving messages
- Adding a new service to the Kafka event pipeline
- Configuring Dapr component for a new topic

## Instructions

1. Apply Dapr pub/sub component:
   ```bash
   kubectl apply -f scripts/kafka-pubsub.yaml -n learnflow
   ```

2. Test publish/subscribe:
   ```bash
   python scripts/test_pubsub.py
   ```

3. Verify subscriptions are active:
   ```bash
   python scripts/verify.py
   ```

## Dapr Component Pattern
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
spec:
  type: pubsub.kafka
  metadata:
    - name: brokers
      value: "my-cluster-kafka-bootstrap.kafka.svc.cluster.local:9092"
```

## LearnFlow Subscription Map
| Service | Subscribes to | Publishes to |
|---------|--------------|--------------|
| concepts | learning.query.explain | learning.response |
| debug | code.debug.request | code.debug.response |
| exercise | exercise.generate | exercise.result |
| progress | progress.update | struggle.alert |

## Validation
- [ ] Dapr component applied in learnflow namespace
- [ ] Test message published and received
- [ ] All services show subscriptions in Dapr dashboard

See [REFERENCE.md](./REFERENCE.md) for topic schema and payload formats.
