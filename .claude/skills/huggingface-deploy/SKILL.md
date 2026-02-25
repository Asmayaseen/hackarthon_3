---
name: huggingface-deploy
description: Deploy LearnFlow AI tutor as a Gradio app on HuggingFace Spaces for public demo access
triggers:
  - "deploy to huggingface"
  - "huggingface spaces"
  - "gradio demo"
  - "public demo"
  - "deploy gradio"
---

# HuggingFace Deploy

## When to Use
- Creating a public demo of LearnFlow without K8s setup
- Showcasing the AI tutoring capabilities on HuggingFace Spaces
- Quick evaluation deployment for hackathon judges

## Instructions

1. Build the Gradio app:
   ```bash
   python scripts/build_app.py
   ```

2. Test locally:
   ```bash
   python learnflow-app/huggingface-space/app.py
   ```

3. Deploy to HuggingFace Spaces:
   ```bash
   bash scripts/deploy.sh
   ```

4. Verify deployment:
   ```bash
   python scripts/verify.py
   ```

## What Gets Deployed
- Gradio interface with Python tutor chat
- Code execution demo with Monaco-like editor
- Progress tracking simulation
- All powered by Groq/OpenAI API

## Validation
- [ ] Gradio app runs locally on port 7860
- [ ] HuggingFace Space shows "Running" status
- [ ] Chat interface responds to Python questions
- [ ] Code execution returns correct output

See [REFERENCE.md](./REFERENCE.md) for Space configuration and GPU requirements.
