---
name: argocd-app-deployment
description: Deploy and manage LearnFlow applications using ArgoCD GitOps continuous delivery
triggers:
  - "setup argocd"
  - "gitops deployment"
  - "argocd sync"
  - "continuous delivery"
  - "deploy with argocd"
---

# ArgoCD Application Deployment

## When to Use
- Setting up GitOps-based continuous delivery for LearnFlow
- Automating K8s deployments from Git commits
- Managing multi-environment deployments (staging, production)

## Instructions

1. Install ArgoCD on the cluster:
   ```bash
   bash scripts/install.sh
   ```

2. Apply LearnFlow application manifests:
   ```bash
   bash scripts/apply_apps.sh
   ```

3. Verify sync status:
   ```bash
   python scripts/verify.py
   ```

4. Access ArgoCD UI:
   ```bash
   kubectl port-forward svc/argocd-server -n argocd 8081:443
   ```
   Open: https://localhost:8081

## GitOps Flow
```
Git push → GitHub Actions builds image → Updates K8s manifest →
ArgoCD detects change → Syncs to cluster → Pods updated
```

## Validation
- [ ] ArgoCD server Running in argocd namespace
- [ ] learnflow Application shows Synced + Healthy
- [ ] Auto-sync triggers on manifest change

See [REFERENCE.md](./REFERENCE.md) for ApplicationSet patterns and RBAC config.
