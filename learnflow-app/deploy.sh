#!/bin/bash
# LearnFlow Complete Platform Deployment Script
# Uses Skills with MCP Code Execution pattern for autonomous deployment
set -e

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m'

NAMESPACE="learnflow"
KAFKA_NAMESPACE="kafka"
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"

log() { echo -e "${GREEN}✓ $1${NC}"; }
warn() { echo -e "${YELLOW}⚠ $1${NC}"; }
step() { echo -e "\n${YELLOW}[$1] $2${NC}"; }

echo "======================================"
echo " LearnFlow Platform Deployment"
echo " Built with Skills + MCP Code Execution"
echo "======================================"

# Step 1: Create namespace
step "1/8" "Creating learnflow namespace..."
kubectl create namespace $NAMESPACE --dry-run=client -o yaml | kubectl apply -f -
log "Namespace ready"

# Step 2: Deploy Kafka (using kafka-k8s-setup skill pattern)
step "2/8" "Deploying Kafka cluster..."
if kubectl get pods -n $KAFKA_NAMESPACE 2>/dev/null | grep -q Running; then
    log "Kafka already running"
else
    helm repo add bitnami https://charts.bitnami.com/bitnami --force-update 2>/dev/null
    helm repo update
    helm upgrade --install kafka-cluster bitnami/kafka \
        --namespace $KAFKA_NAMESPACE \
        --create-namespace \
        --set replicaCount=1 \
        --set controller.replicaCount=1 \
        --set kraft.enabled=true \
        --set zookeeper.enabled=false \
        --set listeners.client.protocol=PLAINTEXT \
        --set listeners.controller.protocol=PLAINTEXT \
        --wait --timeout=300s
    log "Kafka deployed"
fi

# Step 3: Build all Docker images
step "3/8" "Building Docker images for all services..."
cd "$SCRIPT_DIR"

SERVICES=(
    "triage-service:8000"
    "concepts-service:8001"
    "debug-service:8002"
    "code-review-service:8003"
    "exercise-service:8004"
    "progress-service:8005"
)

for svc_port in "${SERVICES[@]}"; do
    svc="${svc_port%%:*}"
    if [ -f "services/$svc/Dockerfile" ]; then
        echo "  Building $svc..."
        docker build -t "$svc:latest" "services/$svc/" --quiet
        log "$svc image built"
    else
        warn "$svc: Dockerfile missing, skipping"
    fi
done

# Build frontend
if [ -f "../learnflow-frontend/Dockerfile" ]; then
    echo "  Building learnflow-frontend..."
    docker build -t learnflow-frontend:latest ../learnflow-frontend/ --quiet
    log "Frontend image built"
fi

# Step 4: Load images into Minikube
step "4/8" "Loading images into Minikube..."
for svc_port in "${SERVICES[@]}"; do
    svc="${svc_port%%:*}"
    if docker image inspect "$svc:latest" &>/dev/null; then
        minikube image load "$svc:latest"
        echo "  ✓ $svc loaded"
    fi
done

if docker image inspect learnflow-frontend:latest &>/dev/null; then
    minikube image load learnflow-frontend:latest
    echo "  ✓ learnflow-frontend loaded"
fi
log "All images loaded into Minikube"

# Step 5: Apply Dapr components
step "5/8" "Applying Dapr pub/sub components..."
if [ -d "dapr-components" ]; then
    kubectl apply -f dapr-components/ -n $NAMESPACE
    log "Dapr components applied"
else
    warn "dapr-components/ not found"
fi

# Step 6: Apply Kubernetes secrets
step "6/8" "Applying Kubernetes secrets..."
if [ -z "$OPENAI_API_KEY" ]; then
    warn "OPENAI_API_KEY not set in environment"
    warn "Update k8s/components/openai-secret.yaml with your API key"
else
    # Create secret from env var
    kubectl create secret generic openai-secret \
        --from-literal=api-key="$OPENAI_API_KEY" \
        --namespace $NAMESPACE \
        --dry-run=client -o yaml | kubectl apply -f -
    log "OpenAI secret created from environment"
fi

if [ -d "k8s/components" ]; then
    kubectl apply -f k8s/components/ -n $NAMESPACE 2>/dev/null || true
fi
log "Secrets applied"

# Step 7: Deploy all services
step "7/8" "Deploying all microservices..."
if [ -d "k8s/deployments" ]; then
    kubectl apply -f k8s/deployments/ -n $NAMESPACE
    log "All service deployments applied"
fi

# Deploy frontend if manifest exists
if [ -f "../learnflow-frontend/k8s/deployment.yaml" ]; then
    kubectl apply -f ../learnflow-frontend/k8s/ -n $NAMESPACE
    log "Frontend deployment applied"
fi

# Step 8: Wait for readiness
step "8/8" "Waiting for all pods to be Ready..."
echo "Waiting up to 5 minutes..."
sleep 10

for svc_port in "${SERVICES[@]}"; do
    svc="${svc_port%%:*}"
    if kubectl get deployment "$svc" -n $NAMESPACE &>/dev/null; then
        kubectl rollout status deployment/"$svc" -n $NAMESPACE --timeout=180s && \
            echo "  ✓ $svc ready" || warn "$svc not ready yet"
    fi
done

# Final status
echo ""
echo "======================================"
log "LearnFlow Platform Deployed!"
echo "======================================"
echo ""
echo "Pod Status:"
kubectl get pods -n $NAMESPACE -o wide
echo ""
echo "Services:"
kubectl get svc -n $NAMESPACE
echo ""
echo "Access Commands:"
echo "  Frontend:        kubectl port-forward svc/learnflow-frontend 3000:3000 -n $NAMESPACE"
echo "  Triage Service:  kubectl port-forward svc/triage-service 8000:80 -n $NAMESPACE"
echo "  Progress API:    kubectl port-forward svc/progress-service 8005:80 -n $NAMESPACE"
echo "  Docs:            kubectl port-forward svc/learnflow-docs 8080:80 -n $NAMESPACE"
echo ""
echo "Verify deployment:"
echo "  python verify.py"
