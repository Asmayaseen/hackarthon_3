#!/bin/bash
set -e
helm repo add dapr https://dapr.github.io/helm-charts/ --force-update
helm repo update
helm upgrade --install dapr dapr/dapr \
  --namespace dapr-system \
  --create-namespace \
  --wait --timeout 300s
echo "✓ Dapr installed in dapr-system"
