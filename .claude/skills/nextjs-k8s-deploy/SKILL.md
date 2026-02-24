---
name: nextjs-k8s-deploy
description: Build and deploy the LearnFlow Next.js frontend to Kubernetes with Docker
triggers:
  - "deploy frontend"
  - "deploy next.js"
  - "build frontend"
  - "frontend not running"
  - "deploy learnflow ui"
---

# Next.js Kubernetes Deploy

## When to Use
- Deploying LearnFlow frontend to Kubernetes
- Updating the UI after code changes
- Setting up the Next.js app for the first time
- Frontend pods crashing or not starting

## Instructions

1. Build the Docker image:
   ```bash
   bash scripts/deploy.sh build
   ```

2. Load image into Minikube:
   ```bash
   bash scripts/deploy.sh load
   ```

3. Deploy to Kubernetes:
   ```bash
   bash scripts/deploy.sh apply
   ```

4. Verify deployment:
   ```bash
   python scripts/verify.py
   ```

5. Access frontend (port-forward):
   ```bash
   kubectl port-forward svc/learnflow-frontend 3000:3000 -n learnflow
   ```
   Open: http://localhost:3000

## Or All-in-One
```bash
bash scripts/deploy.sh all
```

## Validation
- [ ] Frontend pod Running in learnflow namespace
- [ ] Dashboard loads at http://localhost:3000
- [ ] Monaco Editor renders correctly
- [ ] API calls to triage-service succeed

See [REFERENCE.md](./REFERENCE.md) for Next.js Dockerfile patterns and K8s config.
