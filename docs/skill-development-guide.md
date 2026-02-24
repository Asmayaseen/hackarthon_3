# Skill Development Guide

## What is a Skill?

A Skill is the emerging industry standard for teaching AI agents capabilities.
Skills work across **Claude Code**, **Goose**, and **OpenAI Codex** without any changes.

```
.claude/skills/<skill-name>/
├── SKILL.md        # Agent instructions (~100 tokens) — LOADED
├── REFERENCE.md    # Deep docs (0 tokens) — loaded only when needed
└── scripts/
    ├── deploy.sh   # Bash scripts (0 tokens) — EXECUTED
    └── verify.py   # Python scripts (0 tokens) — EXECUTED
```

## Why MCP Code Execution?

| Approach | Tokens Used | Context Available |
|----------|-------------|-------------------|
| 5 direct MCP servers | ~50,000 | 75% wasted |
| Skills + Scripts | ~110 | 97% FREE |

**Result: 80-98% token reduction** — the agent can do far more work.

## Creating a New Skill

### Step 1: Create Directory Structure

```bash
mkdir -p .claude/skills/my-skill/scripts
```

### Step 2: Write SKILL.md (keep under 200 tokens)

```markdown
---
name: my-skill
description: One-line description of what this skill does
triggers:
  - "user phrase that triggers this skill"
  - "another trigger phrase"
---

# My Skill Title

## When to Use
- Specific scenario 1
- Specific scenario 2

## Instructions

1. Run deploy script:
   ```bash
   bash scripts/deploy.sh
   ```

2. Verify:
   ```bash
   python scripts/verify.py
   ```

## Validation
- [ ] Checkpoint 1
- [ ] Checkpoint 2

See [REFERENCE.md](./REFERENCE.md) for details.
```

### Step 3: Write Executable Scripts

**deploy.sh** — Does the heavy lifting (0 tokens in context):
```bash
#!/bin/bash
set -e
# Your deployment commands here
echo "✓ Deployment complete"  # Only this enters agent context
```

**verify.py** — Returns minimal result (0 tokens in context):
```python
#!/usr/bin/env python3
import subprocess, sys

result = subprocess.run(['kubectl', 'get', 'pods', '-n', 'myns', '-o', 'json'],
                       capture_output=True, text=True)
# Process result...
running = 3  # computed
print(f"✓ All {running} pods running")  # Only this enters context
sys.exit(0)
```

### Step 4: Write REFERENCE.md (loaded only when needed)

Put detailed documentation, configuration examples, and troubleshooting here.
This file is NOT loaded by default — it only enters context when the agent
needs deep information.

## Skill Design Principles

### 1. Minimal SKILL.md
- Target: **< 150 tokens**
- Include: when to use, numbered steps, validation checklist
- Link to REFERENCE.md for details
- No verbose explanations

### 2. Scripts Do the Work
- Scripts are **executed**, not loaded into context
- All heavy lifting happens in scripts
- Scripts output only minimal, actionable results
- Always use `sys.exit(0)` success, `sys.exit(1)` failure

### 3. Output Rules for Scripts
```python
# Good: Minimal, actionable
print("✓ All 3 pods running")

# Bad: Dumps raw data into context
print(json.dumps(full_pod_list))  # thousands of tokens!
```

### 4. Cross-Agent Compatibility
Skills work on both Claude Code AND Goose because:
- Both read `.claude/skills/` directory
- SKILL.md YAML frontmatter is the standard format
- Scripts use standard bash/python (universal)

Test your skill on both agents!

## Hackathon Required Skills

| Skill | Required Components |
|-------|---------------------|
| `agents-md-gen` | SKILL.md + scripts/analyze_repo.py + scripts/generate.py + scripts/verify.py |
| `kafka-k8s-setup` | SKILL.md + REFERENCE.md + scripts/deploy.sh + scripts/create-topics.sh + scripts/verify.py |
| `postgres-k8s-setup` | SKILL.md + REFERENCE.md + scripts/deploy.sh + scripts/migrate.py + scripts/verify.py |
| `fastapi-dapr-agent` | SKILL.md + REFERENCE.md + scripts/scaffold.sh + scripts/verify.py |
| `mcp-code-execution` | SKILL.md + REFERENCE.md + scripts/mcp_client.py + scripts/verify.py |
| `nextjs-k8s-deploy` | SKILL.md + REFERENCE.md + scripts/deploy.sh + scripts/verify.py + templates/Dockerfile |
| `docusaurus-deploy` | SKILL.md + REFERENCE.md + scripts/init.sh + scripts/generate-docs.py + scripts/deploy.sh + scripts/verify.py |

## Testing Your Skill

### Manual Testing
```bash
# Test with Claude Code
claude "Deploy Kafka for LearnFlow"

# Test with Goose
goose "Deploy Kafka for LearnFlow"

# Both should:
# 1. Load kafka-k8s-setup/SKILL.md (~100 tokens)
# 2. Execute scripts/deploy.sh (0 tokens)
# 3. Return "✓ Kafka deployed" (~5 tokens)
```

### Automated Verification
```bash
# Check all hackathon skills are MCP Code Execution compliant
python .claude/skills/mcp-code-execution/scripts/verify.py
```

## Example: How `kafka-k8s-setup` Works

1. Agent receives: "Deploy Kafka for LearnFlow"
2. Agent loads `kafka-k8s-setup/SKILL.md` → **~100 tokens in context**
3. Agent executes: `bash scripts/deploy.sh` → **0 tokens** (runs in shell)
4. Shell output: `✓ Kafka deployed to namespace 'kafka'` → **~8 tokens in context**
5. Agent executes: `python scripts/verify.py` → **0 tokens**
6. Verify output: `✓ All 3 Kafka pods running` → **~7 tokens in context**

**Total: ~115 tokens vs ~50,000 with direct MCP** = 99.8% reduction!

## Common Pitfalls

### Don't: Load heavy data into context
```python
# BAD: dumps thousands of tokens into agent context
result = kubectl.get_pods()
print(json.dumps(result))  # ❌
```

### Do: Summarize in script
```python
# GOOD: only summary enters context
pods = kubectl.get_pods()
running = sum(1 for p in pods if p.is_running)
print(f"✓ {running}/{len(pods)} pods running")  # ✅
```

### Don't: Put reference docs in SKILL.md
```markdown
# BAD SKILL.md - too verbose, too many tokens
[Full Kafka configuration guide with 50 code examples...]
```

### Do: Link to REFERENCE.md
```markdown
# GOOD SKILL.md
See [REFERENCE.md](./REFERENCE.md) for configuration options.
```

## Resources

- Hackathon Doc: `hackathon-3-doc`
- MCP Code Execution Pattern: https://www.anthropic.com/engineering/code-execution-with-mcp
- Skills Format: https://block.github.io/goose/docs/guides/context-engineering/using-skills
- OpenAI Codex Skills: https://github.com/openai/codex/blob/main/docs/skills.md
