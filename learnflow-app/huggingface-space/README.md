---
title: LearnFlow AI Tutor
emoji: 🎓
colorFrom: blue
colorTo: indigo
sdk: gradio
sdk_version: 4.44.0
app_file: app.py
pinned: false
license: mit
short_description: Interactive Python tutoring with AI agents
---

# LearnFlow AI Tutor

An AI-powered Python learning platform demo built for Hackathon III.

## Features
- **AI Tutor Chat** — Explain, Debug, Exercise, Review modes
- **Code Runner** — Execute Python in a sandboxed environment
- **Progress Tracking** — Simulated mastery score dashboard

## Environment Variables
Set these as Space secrets:
- `OPENAI_API_KEY` — OpenAI API key (or Groq key)
- `OPENAI_BASE_URL` — Optional; `https://api.groq.com/openai/v1` for Groq
- `AI_MODEL` — Model name (default: `gpt-4o-mini`)

## Deploy
```bash
huggingface-cli upload <your-org>/learnflow-tutor . --repo-type=space
```
