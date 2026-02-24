---
name: learnflow-k8s-deployer
description: Deploy LearnFlow platform on Kubernetes
tags: [k8s, kafka, dapr, postgres, fastapi, nextjs]
author: hackathon-3-team
version: 1.0.0
---

# LearnFlow Kubernetes Deployment Skill

## When to Use
- Deploying LearnFlow platform on Minikube
- Setting up complete event-driven microservices
- Testing hackathon 3 demo scenario

## Instructions
1. Navigate to learnflow-app directory
2. Run deployment script: `./deploy.sh`
3. Verify all services are running
4. Port forward for local access

## Validation Checklist
- [ ] Kafka cluster deployed and running
- [ ] PostgreSQL database available
- [ ] Triage service responding on port 8000
- [ ] Concepts service responding on port 8001
- [ ] Frontend accessible on port 3000
- [ ] All pods in Running state

## Quick Commands
```bash
cd /mnt/d/hackathon-3-all-phases/learnflow-app
./deploy.sh
```

## See Also
- Hackathon 3 documentation for architecture details
- Constitution for deployment principles