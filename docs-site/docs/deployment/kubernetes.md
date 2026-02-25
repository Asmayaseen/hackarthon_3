---
id: kubernetes
title: Kubernetes Deployment
sidebar_position: 2
---

# Kubernetes Deployment

Deploy the complete LearnFlow platform to a local Minikube cluster.

## Prerequisites

```bash
minikube start --cpus=4 --memory=8192 --driver=docker
kubectl cluster-info
helm version
```

## Step 1: Infrastructure

```bash
# Deploy Kafka (Strimzi operator)
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh
bash .claude/skills/kafka-k8s-setup/scripts/create-topics.sh

# Deploy PostgreSQL (CloudNativePG)
bash .claude/skills/postgres-k8s-setup/scripts/deploy.sh
bash .claude/skills/postgres-k8s-setup/scripts/migrate.sh
```

## Step 2: Namespace & Dapr

```bash
kubectl create namespace learnflow

# Install Dapr
helm repo add dapr https://dapr.github.io/helm-charts/
helm install dapr dapr/dapr --namespace dapr-system --create-namespace

# Apply Dapr components
kubectl apply -f learnflow-app/dapr-components/ -n learnflow
```

## Step 3: Backend Services

```bash
# Build and load images into Minikube
eval $(minikube docker-env)
for svc in triage-service concepts-service debug-service exercise-service progress-service code-review-service mcp-server; do
  docker build -t learnflow/$svc:latest learnflow-app/services/$svc/
done

# Deploy all services
kubectl apply -f learnflow-app/k8s/ -n learnflow
```

## Step 4: Frontend

```bash
bash .claude/skills/nextjs-k8s-deploy/scripts/deploy.sh all
```

## Step 5: Verify

```bash
# Check all pods
kubectl get pods -n learnflow

# Port-forward frontend
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow &

# Verify with script
python learnflow-app/verify.py
```

## ArgoCD (GitOps)

```bash
# Install ArgoCD and configure auto-sync
bash learnflow-app/k8s/argocd/install-argocd.sh
```

After setup, every push to `main` automatically deploys to Kubernetes.
