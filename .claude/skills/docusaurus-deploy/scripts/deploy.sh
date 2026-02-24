#!/bin/bash
# Build and deploy Docusaurus documentation to Kubernetes
set -e

NAMESPACE="learnflow"
IMAGE_NAME="learnflow-docs"
DOCS_DIR="learnflow-docs"

if [ ! -d "$DOCS_DIR" ]; then
  echo "Docs directory not found. Initializing..."
  bash "$(dirname "$0")/init.sh"
fi

echo "Building Docusaurus documentation..."

# Build Docker image
docker build -t "$IMAGE_NAME:latest" "$DOCS_DIR/"
echo "✓ Docs image built"

# Load into Minikube
minikube image load "$IMAGE_NAME:latest"
echo "✓ Image loaded into Minikube"

# Create namespace
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Deploy
kubectl apply -f - << 'K8SEOF'
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learnflow-docs
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: learnflow-docs
  template:
    metadata:
      labels:
        app: learnflow-docs
    spec:
      containers:
      - name: docs
        image: learnflow-docs:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 80
        resources:
          requests:
            memory: "64Mi"
            cpu: "50m"
          limits:
            memory: "128Mi"
            cpu: "100m"
---
apiVersion: v1
kind: Service
metadata:
  name: learnflow-docs
  namespace: learnflow
spec:
  selector:
    app: learnflow-docs
  ports:
  - port: 80
    targetPort: 80
  type: ClusterIP
K8SEOF

kubectl rollout status deployment/learnflow-docs -n "$NAMESPACE" --timeout=120s
echo "✓ Documentation deployed to namespace '$NAMESPACE'"
echo "✓ Access: kubectl port-forward svc/learnflow-docs 8080:80 -n learnflow"
