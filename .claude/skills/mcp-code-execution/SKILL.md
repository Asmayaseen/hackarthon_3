---
name: mcp-code-execution
description: Implement the MCP Code Execution pattern - wrap MCP server calls in scripts to achieve 80-98% token reduction
triggers:
  - "mcp code execution"
  - "wrap mcp in script"
  - "reduce token usage"
  - "mcp server bloat"
  - "implement code execution pattern"
---

# MCP Code Execution Pattern

## When to Use
- Replacing direct MCP tool calls that consume excessive context tokens
- Wrapping any MCP server (K8s, database, file system) in efficient scripts
- Achieving 80-98% token reduction vs direct MCP integration
- Building Skills that execute code instead of loading tools into context

## The Problem
Direct MCP: 5 tools × ~10k tokens = **50,000 tokens before typing anything**

## The Solution
```
SKILL.md (~100 tokens) + scripts/*.py (0 tokens) = only minimal result in context
```

## Instructions

1. Identify the MCP server to wrap:
   ```bash
   python scripts/analyze_mcp.py
   ```

2. Generate an efficient script wrapper:
   ```bash
   python scripts/generate_wrapper.py --mcp-server <name> --operation <op>
   ```

3. Test the wrapper returns minimal output:
   ```bash
   python scripts/test_wrapper.py
   ```

4. Verify token efficiency:
   ```bash
   python scripts/verify.py
   ```

## Pattern Template

BEFORE (Direct MCP - loads 50,000+ tokens):
```
TOOL CALL: kubernetes.getPods(namespace: 'learnflow')
  → returns full JSON (thousands of tokens into context)
```

AFTER (Script - loads ~10 tokens):
```
python scripts/get_pods.py learnflow
  → "✓ All 6 pods running"
```

## Validation
- [ ] Script produces < 50 tokens of output
- [ ] Script exits 0 on success, 1 on failure
- [ ] No MCP tools loaded at startup
- [ ] SKILL.md under 200 tokens total

See [REFERENCE.md](./REFERENCE.md) for all MCP wrapping patterns.
