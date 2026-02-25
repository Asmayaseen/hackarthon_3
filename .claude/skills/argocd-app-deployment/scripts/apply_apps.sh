#!/bin/bash
set -e
kubectl apply -f learnflow-app/k8s/argocd/application.yaml
echo "✓ LearnFlow ArgoCD applications applied — auto-sync enabled"
