---
name: prometheus-grafana-setup
description: Deploy Prometheus + Grafana monitoring stack for LearnFlow on Kubernetes
triggers:
  - "setup monitoring"
  - "deploy prometheus"
  - "deploy grafana"
  - "add metrics"
  - "monitor services"
---

# Prometheus + Grafana Setup

## When to Use
- Adding observability to LearnFlow services
- Setting up dashboards for service latency, error rates
- Monitoring Kafka consumer lag and pod resource usage

## Instructions

1. Deploy monitoring stack:
   ```bash
   bash scripts/deploy.sh
   ```

2. Import LearnFlow dashboards:
   ```bash
   python scripts/import_dashboards.py
   ```

3. Verify stack is running:
   ```bash
   python scripts/verify.py
   ```

4. Access dashboards:
   ```bash
   kubectl port-forward svc/grafana 3001:80 -n monitoring
   ```
   Open: http://localhost:3001 (admin/admin)

## What Gets Deployed
- Prometheus (metrics collection, 15-day retention)
- Grafana (visualization dashboards)
- kube-state-metrics (K8s resource metrics)
- Pre-built LearnFlow dashboard (request rate, latency, error rate)

## Validation
- [ ] Prometheus pod Running in monitoring namespace
- [ ] Grafana pod Running in monitoring namespace
- [ ] LearnFlow services appear in Prometheus targets
- [ ] Dashboard loads at http://localhost:3001

See [REFERENCE.md](./REFERENCE.md) for dashboard JSON and alerting rules.
