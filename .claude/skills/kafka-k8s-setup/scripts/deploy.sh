#!/bin/bash
# Deploy Apache Kafka on Kubernetes for LearnFlow
# Uses Bitnami Helm chart - minimal context, maximal automation
set -e

KAFKA_NAMESPACE="kafka"
RELEASE_NAME="kafka-cluster"

echo "Deploying Kafka on Kubernetes..."

# Add Bitnami repo
helm repo add bitnami https://charts.bitnami.com/bitnami --force-update 2>/dev/null
helm repo update

# Create namespace
kubectl create namespace "$KAFKA_NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Deploy Kafka (single replica for dev)
helm upgrade --install "$RELEASE_NAME" bitnami/kafka \
  --namespace "$KAFKA_NAMESPACE" \
  --set replicaCount=1 \
  --set controller.replicaCount=1 \
  --set broker.replicaCount=1 \
  --set kraft.enabled=true \
  --set zookeeper.enabled=false \
  --set listeners.client.protocol=PLAINTEXT \
  --set listeners.controller.protocol=PLAINTEXT \
  --set listeners.interbroker.protocol=PLAINTEXT \
  --wait --timeout=300s

echo "✓ Kafka deployed to namespace '$KAFKA_NAMESPACE'"
echo "✓ Bootstrap: $RELEASE_NAME-kafka-bootstrap.$KAFKA_NAMESPACE:9092"
