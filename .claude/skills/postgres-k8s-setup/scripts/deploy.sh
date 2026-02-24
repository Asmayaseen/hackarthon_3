#!/bin/bash
# Deploy PostgreSQL on Kubernetes using CloudNativePG operator
set -e

NAMESPACE="learnflow"
CLUSTER_NAME="pg-cluster"

echo "Deploying PostgreSQL on Kubernetes..."

# Install CloudNativePG operator
kubectl apply --server-side -f \
  https://raw.githubusercontent.com/cloudnative-pg/cloudnative-pg/release-1.22/releases/cnpg-1.22.0.yaml

echo "Waiting for CNPG operator..."
kubectl wait --for=condition=Available \
  deployment/cnpg-controller-manager \
  -n cnpg-system --timeout=120s

# Create namespace
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Create PostgreSQL cluster
cat <<EOF | kubectl apply -f -
apiVersion: postgresql.cnpg.io/v1
kind: Cluster
metadata:
  name: $CLUSTER_NAME
  namespace: $NAMESPACE
spec:
  instances: 1
  primaryUpdateStrategy: unsupervised
  storage:
    size: 2Gi
  bootstrap:
    initdb:
      database: learnflow
      owner: learnflow
      secret:
        name: pg-cluster-superuser
EOF

echo "Waiting for PostgreSQL to be ready..."
kubectl wait --for=condition=Ready cluster/$CLUSTER_NAME \
  -n "$NAMESPACE" --timeout=300s

echo "✓ PostgreSQL deployed to namespace '$NAMESPACE'"
echo "✓ RW endpoint: $CLUSTER_NAME-rw.$NAMESPACE:5432"
echo "✓ RO endpoint: $CLUSTER_NAME-ro.$NAMESPACE:5432"
