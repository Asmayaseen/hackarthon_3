#!/bin/bash
set -e
helm repo add kong https://charts.konghq.com
helm repo update
kubectl create namespace kong --dry-run=client -o yaml | kubectl apply -f -
helm upgrade --install kong kong/kong \
  --namespace kong \
  --set ingressController.installCRDs=false \
  --set proxy.type=NodePort \
  --wait --timeout 300s
echo "✓ Kong deployed in kong namespace"
