---
id: intro
title: Introduction
sidebar_position: 1
slug: /
---

# LearnFlow Documentation

**LearnFlow** is an AI-powered Python tutoring platform built for Hackathon III.
It demonstrates reusable agentic intelligence using Skills, MCP Code Execution,
Claude Code, and Goose.

## What is LearnFlow?

LearnFlow helps students learn Python programming through:

- 💬 **AI Tutor Chat** — Ask questions, get concept explanations
- 💻 **Monaco Code Editor** — Write and run Python in the browser
- 🧠 **Adaptive Quizzes** — Test knowledge, track mastery
- 📊 **Progress Dashboard** — Visual mastery chart per topic
- 👩‍🏫 **Teacher Dashboard** — Monitor students, generate exercises

## Architecture

LearnFlow is built on a **microservices architecture** with 7 AI agents:

| Service | Port | Role |
|---------|------|------|
| Triage Agent | 8080 | Routes queries to specialist agents |
| Concepts Agent | 8001 | Explains Python concepts |
| Debug Agent | 8002 | Parses errors and suggests fixes |
| Exercise Agent | 8003 | Generates coding exercises |
| Progress Agent | 8004 | Tracks mastery scores |
| Code Review Agent | 8005 | Reviews code quality (PEP 8) |
| MCP Server | 8006 | Provides AI agents with platform context |
| Frontend | 3000 | Next.js + Monaco Editor |

Services communicate via **Kafka** (6 topics) and use **Dapr** for service mesh.

## Quick Start

```bash
# 1. Clone the repository
git clone https://github.com/Asmayaseen/hackarthon_3

# 2. Start all services
cd learnflow-app
bash deploy.sh

# 3. Open the app
open http://localhost:3000
```

## The Skills Philosophy

> "The Skills are the product, not just documentation."

LearnFlow was built by teaching AI agents — Claude Code and Goose — using
**Skills with MCP Code Execution**. Each Skill:

- Has a `SKILL.md` (~100 tokens) that tells the agent what to do
- Has `scripts/` that execute externally (0 tokens in context)
- Returns only minimal results to the agent context

This achieves **80-98% token reduction** vs direct MCP tool loading.

```
Before: 5 MCP servers × 10k tokens = 50,000 tokens at startup
After:  SKILL.md × 100 tokens + script results × 10 tokens = 110 tokens total
```
