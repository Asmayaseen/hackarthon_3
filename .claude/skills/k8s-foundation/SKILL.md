---
name: k8s-foundation
description: Check Kubernetes cluster health and apply foundational Helm charts for LearnFlow namespace setup
triggers:
  - "setup kubernetes"
  - "check cluster health"
  - "initialize k8s"
  - "k8s not ready"
  - "create learnflow namespace"
---

# Kubernetes Foundation

## When to Use
- First-time cluster setup before any service deployment
- Verifying cluster is healthy before running skills
- Creating namespaces and applying RBAC configs
- Installing cluster-level prerequisites (Dapr, cert-manager)

## Instructions

1. Verify cluster is healthy:
   ```bash
   python scripts/check_cluster.py
   ```

2. Create required namespaces:
   ```bash
   bash scripts/setup_namespaces.sh
   ```

3. Install Dapr on the cluster:
   ```bash
   bash scripts/install_dapr.sh
   ```

4. Verify all system pods running:
   ```bash
   python scripts/verify.py
   ```

## Required Namespaces
| Namespace | Purpose |
|-----------|---------|
| `learnflow` | All LearnFlow services |
| `kafka` | Kafka + Strimzi operator |
| `dapr-system` | Dapr control plane |

## Validation
- [ ] `kubectl cluster-info` returns cluster endpoint
- [ ] All system namespaces created
- [ ] Dapr operator running in dapr-system
- [ ] `learnflow` namespace ready

See [REFERENCE.md](./REFERENCE.md) for cluster sizing and resource quotas.
