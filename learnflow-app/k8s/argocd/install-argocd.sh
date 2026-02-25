#!/bin/bash
# Install ArgoCD on Minikube and configure LearnFlow application
set -e

echo "Installing ArgoCD..."
kubectl create namespace argocd --dry-run=client -o yaml | kubectl apply -f -
kubectl apply -n argocd -f https://raw.githubusercontent.com/argoproj/argo-cd/stable/manifests/install.yaml

echo "Waiting for ArgoCD server to be ready..."
kubectl wait --for=condition=available deployment/argocd-server -n argocd --timeout=300s

echo "Getting ArgoCD admin password..."
ARGOCD_PASSWORD=$(kubectl get secret argocd-initial-admin-secret -n argocd -o jsonpath="{.data.password}" | base64 -d)
echo "Admin password: $ARGOCD_PASSWORD"

echo "Port-forwarding ArgoCD UI (background)..."
kubectl port-forward svc/argocd-server -n argocd 8081:443 &

echo "Applying LearnFlow ArgoCD application..."
kubectl apply -f learnflow-app/k8s/argocd/application.yaml

echo ""
echo "✓ ArgoCD installed"
echo "  UI: https://localhost:8081"
echo "  User: admin"
echo "  Pass: $ARGOCD_PASSWORD"
echo "  App: learnflow (auto-syncs from main branch)"
