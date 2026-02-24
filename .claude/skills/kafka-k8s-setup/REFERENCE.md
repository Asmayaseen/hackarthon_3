# Kafka Kubernetes Reference

## Architecture
LearnFlow uses Apache Kafka deployed via Bitnami Helm chart with Dapr pub/sub as the integration layer.

```
[FastAPI Service] → [Dapr Sidecar] → [Kafka Broker] → [Dapr Sidecar] → [FastAPI Service]
                        :3500                                :3500
```

## Helm Chart Details
- **Chart**: bitnami/kafka
- **Version**: Latest stable
- **Namespace**: kafka
- **Replicas**: 1 (development), 3 (production)
- **Bootstrap**: `kafka-cluster-kafka-bootstrap.kafka:9092`

## Topic Configuration
```bash
# List all topics
kubectl exec -n kafka kafka-cluster-kafka-0 -- \
  kafka-topics.sh --bootstrap-server localhost:9092 --list

# Describe a topic
kubectl exec -n kafka kafka-cluster-kafka-0 -- \
  kafka-topics.sh --bootstrap-server localhost:9092 \
  --describe --topic learning.query.explain

# Test producer
kubectl exec -n kafka kafka-cluster-kafka-0 -- \
  kafka-console-producer.sh --bootstrap-server localhost:9092 \
  --topic learning.query.explain

# Test consumer
kubectl exec -n kafka kafka-cluster-kafka-0 -- \
  kafka-console-consumer.sh --bootstrap-server localhost:9092 \
  --topic learning.query.explain --from-beginning
```

## Dapr Component Configuration
```yaml
# learnflow-app/dapr-components/kafka-pubsub.yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: learnflow
spec:
  type: pubsub.kafka
  version: v1
  metadata:
    - name: brokers
      value: "kafka-cluster-kafka-bootstrap.kafka:9092"
    - name: authType
      value: "none"
    - name: maxMessageBytes
      value: "1024"
```

## Common Issues

### Pods stuck in Pending
```bash
kubectl describe pod -n kafka <pod-name>
# Check Events section for resource issues
# Fix: minikube start --memory=8192
```

### Connection refused from services
```bash
# Verify bootstrap service exists
kubectl get svc -n kafka
# Expected: kafka-cluster-kafka-bootstrap  ClusterIP  9092/TCP
```

### Topic creation fails
```bash
# Check broker is ready
kubectl get kafkatopics -n kafka
kubectl get pods -n kafka
```

## Monitoring
```bash
# Watch Kafka pod status
kubectl get pods -n kafka -w

# Get Kafka logs
kubectl logs -n kafka kafka-cluster-kafka-0 --tail=100
```
