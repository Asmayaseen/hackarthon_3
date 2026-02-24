---
name: docusaurus-deploy
description: Set up and deploy Docusaurus documentation site for LearnFlow platform on Kubernetes
triggers:
  - "deploy documentation"
  - "setup docusaurus"
  - "create docs site"
  - "deploy docs"
  - "documentation site"
---

# Docusaurus Deploy

## When to Use
- Setting up the LearnFlow documentation website
- Deploying API docs, skill guides, and architecture docs
- Publishing developer documentation to Kubernetes
- Auto-generating docs from code and specs

## Instructions

1. Initialize Docusaurus site:
   ```bash
   bash scripts/init.sh
   ```

2. Generate documentation from specs:
   ```bash
   python scripts/generate-docs.py
   ```

3. Build and deploy to Kubernetes:
   ```bash
   bash scripts/deploy.sh
   ```

4. Verify documentation is accessible:
   ```bash
   python scripts/verify.py
   ```

5. Access docs:
   ```bash
   kubectl port-forward svc/learnflow-docs 8080:80 -n learnflow
   ```
   Open: http://localhost:8080

## What Gets Generated
- Platform architecture overview
- API reference (from OpenAPI specs)
- Skill development guide
- Deployment runbook
- Student/Teacher user guides

## Validation
- [ ] Docusaurus site builds without errors
- [ ] Docs pod Running in learnflow namespace
- [ ] Homepage loads at http://localhost:8080
- [ ] API docs auto-generated from OpenAPI specs

See [REFERENCE.md](./REFERENCE.md) for Docusaurus configuration and content organization.
