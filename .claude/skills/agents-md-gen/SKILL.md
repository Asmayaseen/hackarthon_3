---
name: agents-md-gen
description: Generate AGENTS.md files that teach AI agents about a repository's structure, conventions, and guidelines
triggers:
  - "generate AGENTS.md"
  - "create agents file"
  - "document repository for AI"
  - "set up AI agent context"
---

# AGENTS.md Generator

## When to Use
- Setting up a new repository for AI agent development
- Helping AI agents (Claude Code, Goose, Codex) understand project structure
- Documenting coding conventions, architecture, and workflows
- Ensuring consistent AI behavior across the project

## Instructions

1. Analyze the repository structure:
   ```
   python scripts/analyze_repo.py
   ```

2. Generate the AGENTS.md file:
   ```
   python scripts/generate.py --output AGENTS.md
   ```

3. Verify the generated file:
   ```
   python scripts/verify.py
   ```

4. Confirm AGENTS.md is placed at repository root.

## What Gets Generated
- Repository overview and purpose
- Directory structure with explanations
- Tech stack and key dependencies
- Coding conventions and standards
- Common workflows and commands
- Service endpoints and APIs
- Testing patterns

## Validation
- [ ] AGENTS.md exists at repository root
- [ ] All major directories documented
- [ ] Tech stack listed
- [ ] Commands are accurate and runnable

See [REFERENCE.md](./REFERENCE.md) for AGENTS.md format specification.
