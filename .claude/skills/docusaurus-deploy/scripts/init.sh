#!/bin/bash
# Initialize Docusaurus documentation site for LearnFlow
set -e

DOCS_DIR="learnflow-docs"

if [ -d "$DOCS_DIR" ]; then
  echo "⚠ $DOCS_DIR already exists, skipping init"
  exit 0
fi

echo "Initializing Docusaurus for LearnFlow..."

# Create Docusaurus app
npx create-docusaurus@latest "$DOCS_DIR" classic --typescript

# Create LearnFlow docs structure
mkdir -p "$DOCS_DIR/docs/architecture"
mkdir -p "$DOCS_DIR/docs/api"
mkdir -p "$DOCS_DIR/docs/skills"
mkdir -p "$DOCS_DIR/docs/deployment"
mkdir -p "$DOCS_DIR/docs/guides"

# Create intro page
cat > "$DOCS_DIR/docs/intro.md" << 'MDEOF'
---
sidebar_position: 1
---

# LearnFlow Platform

LearnFlow is an **AI-powered Python tutoring platform** built on cloud-native microservices.

## What is LearnFlow?

LearnFlow helps students learn Python through conversational AI agents:
- **Chat with AI tutors** that adapt to your skill level
- **Write and run code** in the Monaco editor
- **Take quizzes** and track your mastery progress
- **Get instant debugging help** with progressive hints

## Architecture

LearnFlow is built with:
- **FastAPI** microservices with Dapr pub/sub
- **Apache Kafka** for event-driven communication
- **Kubernetes** for orchestration
- **OpenAI GPT-4o-mini** for all AI agents
- **Next.js** frontend with Monaco editor

## Quick Start

```bash
# Start Kubernetes cluster
minikube start --cpus=4 --memory=8192

# Deploy LearnFlow
cd learnflow-app && ./deploy.sh

# Access the platform
kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow
```

Open [http://localhost:3000](http://localhost:3000) to see LearnFlow.
MDEOF

# Create Dockerfile for docs
cat > "$DOCS_DIR/Dockerfile" << 'DFEOF'
FROM node:20-alpine AS builder
WORKDIR /app
COPY package*.json ./
RUN npm ci
COPY . .
RUN npm run build

FROM nginx:alpine
COPY --from=builder /app/build /usr/share/nginx/html
EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
DFEOF

echo "✓ Docusaurus initialized at $DOCS_DIR"
echo "Next: python scripts/generate-docs.py"
