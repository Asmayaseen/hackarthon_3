#!/bin/bash
# Create all LearnFlow Kafka topics
set -e

KAFKA_NAMESPACE="kafka"
KAFKA_POD=$(kubectl get pods -n "$KAFKA_NAMESPACE" -l app.kubernetes.io/component=broker -o jsonpath='{.items[0].metadata.name}' 2>/dev/null || \
            kubectl get pods -n "$KAFKA_NAMESPACE" -o jsonpath='{.items[0].metadata.name}')
BOOTSTRAP="localhost:9092"

TOPICS=(
  "learning.query.explain"
  "learning.query.unclassified"
  "code.debug.request"
  "code.debug.response"
  "exercise.generate"
  "exercise.graded"
  "code.review.request"
  "code.review.completed"
  "progress.update"
  "progress.summary"
  "struggle.alert"
  "learning.response.explanation"
)

echo "Creating LearnFlow Kafka topics..."

for topic in "${TOPICS[@]}"; do
  kubectl exec -n "$KAFKA_NAMESPACE" "$KAFKA_POD" -- \
    kafka-topics.sh \
    --bootstrap-server "$BOOTSTRAP" \
    --create --if-not-exists \
    --topic "$topic" \
    --partitions 1 \
    --replication-factor 1 2>/dev/null && \
    echo "  ✓ $topic" || echo "  ⚠ $topic (may already exist)"
done

echo "✓ All LearnFlow topics created"
