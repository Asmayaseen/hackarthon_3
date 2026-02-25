#!/bin/bash
set -e
# Requires: huggingface-cli login
if ! command -v huggingface-cli &>/dev/null; then
  pip install huggingface_hub -q
fi
echo "Deploying LearnFlow to HuggingFace Spaces..."
cd learnflow-app/huggingface-space
huggingface-cli upload . --repo-type space --repo-id learnflow-demo
echo "✓ Deployed to https://huggingface.co/spaces/learnflow-demo"
