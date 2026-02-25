---
id: quickstart
title: Quick Start
sidebar_position: 2
---

# Quick Start

## Prerequisites

```bash
# Required tools
docker --version    # Docker 24+
minikube version    # Minikube 1.33+
kubectl version     # kubectl 1.29+
helm version        # Helm 3.14+
claude --version    # Claude Code
goose --version     # Goose
```

## 1. Clone & Setup

```bash
git clone https://github.com/Asmayaseen/hackarthon_3
cd hackarthon_3
```

## 2. Start Minikube

```bash
minikube start --cpus=4 --memory=8192 --driver=docker
```

## 3. Deploy Infrastructure

```bash
# Deploy Kafka
bash .claude/skills/kafka-k8s-setup/scripts/deploy.sh

# Deploy PostgreSQL
bash .claude/skills/postgres-k8s-setup/scripts/deploy.sh
```

## 4. Deploy LearnFlow Services

```bash
cd learnflow-app
bash deploy.sh
```

## 5. Access the App

```bash
# Frontend
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow
open http://localhost:3000

# MCP Server
kubectl port-forward svc/mcp-server 8006:8006 -n learnflow
open http://localhost:8006/docs

# Docs
kubectl port-forward svc/learnflow-docs 8080:80 -n learnflow
open http://localhost:8080
```

## Running Locally (No K8s)

```bash
# Backend services
cd learnflow-app
pip install -r requirements.txt
python main.py

# Frontend
cd learnflow-frontend
npm install && npm run dev

# Open
open http://localhost:3000
```

## Demo Credentials

| Role | Email | Password |
|------|-------|---------|
| Student | maya@learnflow.ai | demo123 |
| Teacher | rodriguez@learnflow.ai | demo123 |
