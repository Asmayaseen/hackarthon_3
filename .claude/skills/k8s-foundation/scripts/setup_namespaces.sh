#!/bin/bash
set -e
for ns in learnflow kafka dapr-system; do
  kubectl create namespace "$ns" --dry-run=client -o yaml | kubectl apply -f -
  echo "✓ namespace/$ns ready"
done
