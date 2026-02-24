#!/bin/bash
# Build and deploy LearnFlow Next.js frontend to Kubernetes
set -e

NAMESPACE="learnflow"
IMAGE_NAME="learnflow-frontend"
FRONTEND_DIR="learnflow-frontend"
K8S_DIR="learnflow-frontend/k8s"

build() {
  echo "Building Next.js Docker image..."
  if [ ! -f "$FRONTEND_DIR/Dockerfile" ]; then
    echo "Dockerfile not found. Creating from template..."
    bash "$(dirname "$0")/create-dockerfile.sh"
  fi
  docker build -t "$IMAGE_NAME:latest" "$FRONTEND_DIR/"
  echo "✓ Image built: $IMAGE_NAME:latest"
}

load() {
  echo "Loading image into Minikube..."
  minikube image load "$IMAGE_NAME:latest"
  echo "✓ Image loaded into Minikube"
}

apply() {
  echo "Deploying to Kubernetes..."
  kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

  # Apply manifest if it exists
  if [ -d "$K8S_DIR" ]; then
    kubectl apply -f "$K8S_DIR/"
  else
    # Create manifest on the fly
    kubectl apply -f - << MANIFEST
apiVersion: apps/v1
kind: Deployment
metadata:
  name: learnflow-frontend
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: learnflow-frontend
  template:
    metadata:
      labels:
        app: learnflow-frontend
    spec:
      containers:
      - name: frontend
        image: learnflow-frontend:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: 3000
        env:
        - name: NODE_ENV
          value: "production"
        - name: TRIAGE_SERVICE_URL
          value: "http://triage-service.learnflow.svc.cluster.local"
        - name: PROGRESS_SERVICE_URL
          value: "http://progress-service.learnflow.svc.cluster.local"
        resources:
          requests:
            memory: "256Mi"
            cpu: "200m"
          limits:
            memory: "512Mi"
            cpu: "500m"
---
apiVersion: v1
kind: Service
metadata:
  name: learnflow-frontend
  namespace: learnflow
spec:
  selector:
    app: learnflow-frontend
  ports:
  - port: 3000
    targetPort: 3000
  type: ClusterIP
MANIFEST
  fi

  kubectl rollout status deployment/learnflow-frontend -n "$NAMESPACE" --timeout=120s
  echo "✓ Frontend deployed to namespace '$NAMESPACE'"
  echo "✓ Access: kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow"
}

# Main
COMMAND="${1:-all}"
case "$COMMAND" in
  build) build ;;
  load)  load ;;
  apply) apply ;;
  all)   build && load && apply ;;
  *)     echo "Usage: bash deploy.sh [build|load|apply|all]"; exit 1 ;;
esac
