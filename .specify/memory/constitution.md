# LearnFlow Platform - Project Constitution

## Preamble

This constitution establishes the foundational principles, architectural mandates, and operational guidelines for building the LearnFlow AI-powered tutoring platform. This is not merely a coding project - it represents a paradigm shift from **Coder to Teacher**, where we architect reusable intelligence through Skills rather than writing application code manually.

**Core Mandate:** *Don't Build Agents, Build Skills Instead*

---

## Article I: Foundational Philosophy

### Section 1.01: The Teaching Paradigm
We transition from writing code to teaching machines how to build systems. Our product is not the LearnFlow application - **our product is the Skills we create** that enable AI agents to build autonomously.

- **Coder Mentality:** Write code → Code runs → Application works
- **Teacher Mentality:** Write Skills → AI learns patterns → AI writes code → Application works

### Section 1.02: Reusable Intelligence as Product
Skills must be treated as first-class products, not documentation. Each Skill must:
- Work autonomously with single-prompt-to-deployment capability
- Execute consistently across Claude Code and Goose without modification
- Demonstrate 98% token reduction vs. direct MCP integration
- Encapsulate best practices and architectural patterns

### Section 1.03: Cross-Agent Compatibility Mandate
Every Skill must be compatible with both primary agents:
- **Claude Code** (Anthropic's cloud-first agent)
- **Goose** (AAIF open-source standard, local-first agent)

Skills must be stored in `.claude/skills/<skill-name>/` directory structure and work identically across both platforms.

---

## Article II: MCP Code Execution Architecture

### Section 2.01: The Token Crisis and Solution
**Problem:** Direct MCP server integration consumes 50,000+ tokens at startup (25% of context window)
**Solution:** Skills + Code Execution pattern achieves ~100 token overhead (98% reduction)

### Section 2.02: Prohibited Patterns (Strictly Forbidden)
Direct MCP server integration with coding agents is **PROHIBITED**:
- No MCP servers loaded in agent startup configuration
- No direct tool calls from agents to MCP servers
- No streaming of intermediate results through agent context

**Rationale:** This pattern causes exponential token bloat and prevents autonomous operation.

### Section 2.03: Required Pattern: Skills with Code Execution
All MCP interactions must follow this exact structure:

```
.claude/skills/<skill-name>/
├── SKILL.md              # Agent instructions (~100 tokens)
├── REFERENCE.md          # Deep documentation (loaded on-demand)
└── scripts/
    ├── *.sh             # Bash execution scripts (0 tokens)
    └── *.py             # Python execution scripts (0 tokens)
```

**Execution Flow:**
1. Agent loads SKILL.md (~100 tokens)
2. Agent executes scripts via system calls (0 tokens in context)
3. Scripts interact with MCP servers via APIs
4. Only final result returns to agent context (~10 tokens)

**Token Reduction:** 50,000 → ~110 tokens (98% reduction)

### Section 2.04: Token Budget Requirements
- SKILL.md files: Maximum 150 tokens
- Script execution: Zero tokens (external process)
- Final result: Maximum 50 tokens
- Total per Skill execution: <200 tokens
- Token reduction target: 98% vs. direct MCP approach

**Example Token Budget:**
```
SKILL.md: ~100 tokens (loaded)
scripts/deploy.sh: 0 tokens (executed)
scripts/verify.py: 0 tokens (executed)
Final output: ~10 tokens (result)
---------------------------------
Total: ~110 tokens vs. 50,000+ direct MCP
```

---

## Article III: Technical Stack & Infrastructure

### Section 3.01: Core Technology Stack
The LearnFlow platform must be built using these technologies:

**Orchestration Layer:**
- Kubernetes (Minikube for local development, cloud K8s for production)
- Helm for package management
- Argo CD for GitOps continuous delivery

**Event-Driven Architecture:**
- Apache Kafka for event streaming
- Topics: `learning.*`, `code.*`, `exercise.*`, `struggle.*`
- Dapr (Distributed Application Runtime) for service mesh

**Application Layer:**
- Next.js (Frontend with Monaco Editor)
- FastAPI (Backend microservices)
- Better Auth (Authentication framework)
- Neon PostgreSQL (Serverless database)
- Kong API Gateway (Ingress and JWT handling)

**AI Agent System:**
- Multi-agent architecture with specialized agents
- OpenAI Agents SDK for agent orchestration
- Code execution sandbox (5s timeout, 50MB memory, restricted imports)

### Section 3.02: Microservices Architecture Principles
**Mandate:** Stateless, event-driven microservices with Dapr sidecars

Each microservice must:
1. Be independently deployable via Helm chart
2. Communicate via Kafka topics (async) or Dapr service invocation (sync)
3. Store no local state (use Dapr state stores)
4. Emit events for all state changes
5. Consume events idempotently

**Required Services:**
- Triage Service (routes student queries)
- Concepts Service (explains Python topics)
- Code Review Service (analyzes code quality)
- Debug Service (parses errors and provides hints)
- Exercise Service (generates and grades challenges)
- Progress Service (calculates mastery scores)

### Section 3.03: Dapr Implementation Standards
All microservices must:
- Run with Dapr sidecar in Kubernetes
- Use Dapr for: pub/sub messaging, state management, service invocation
- Follow Dapr idiom: `dapr-app-id` annotations, pub/sub component configs
- Implement health checks for Dapr sidecar readiness

**Required Dapr Components:**
- Pub/sub: Kafka component (`kafka-pubsub.yaml`)
- State store: PostgreSQL component (`statestore.yaml`)
- Bindings: Cron for scheduled tasks (`cron.yaml`)

### Section 3.04: Kafka Topic Naming Convention
All event topics must follow pattern: `<domain>.<event-type>.<version>`

**Required Topics:**
- `learning.module.started`
- `learning.module.completed`
- `code.submitted`
- `code.executed`
- `exercise.generated`
- `exercise.graded`
- `struggle.detected`
- `progress.updated`

Each topic must have:
- Avro/JSON schema definition
- Retention policy (7 days default)
- Replication factor (3 for production, 1 for Minikube)
- Partition count based on throughput requirements

---

## Article IV: Skill Development Standards

### Section 4.01: Skill Directory Structure
Every Skill must follow this exact structure:

```
.claude/skills/<skill-name>/
├── SKILL.md              # Required: Instructions for AI agent
├── REFERENCE.md          # Optional: Detailed reference documentation
└── scripts/
    ├── deploy.sh         # Required: Deployment script
    ├── verify.py         # Required: Verification script
    └── *.py/*.sh         # Optional: Additional utility scripts
```

### Section 4.02: SKILL.md Specification
Each SKILL.md must include:

```yaml
---
name: skill-name-kebab-case
description: One-line description of what the skill does
tags: [k8s, kafka, dapr, postgres, nextjs, fastapi]
author: your-name
version: 1.0.0
---

# Skill Name

## When to Use
- Bullet list of use cases

## Instructions
1. Step-by-step instructions for AI agent
2. Include exact commands: `./scripts/deploy.sh`
3. Include verification steps: `python scripts/verify.py`

## Validation Checklist
- [ ] Observable outcome 1
- [ ] Observable outcome 2
- [ ] Observable outcome 3

## See Also
- [REFERENCE.md](./REFERENCE.md) for configuration options
- Link to relevant spec documents
```

### Section 4.03: Script Execution Requirements
All scripts must:
- Be executable (`chmod +x *.sh`)
- Return non-zero exit code on failure
- Print minimal output to stdout (one-line status messages)
- Accept configuration via environment variables or config files
- Include error handling and validation
- Be idempotent (safe to run multiple times)

**Example Script Pattern:**
```bash
#!/bin/bash
set -euo pipefail

# Configuration
NAMESPACE=${NAMESPACE:-"default"}

# Idempotent operation
kubectl create namespace "$NAMESPACE" --dry-run=client -o yaml | kubectl apply -f -

# Minimal output
echo "✓ Namespace '$NAMESPACE' ready"
```

### Section 4.04: Verification Script Standards
Every Skill must include a verification script that:
1. Checks actual state (not just exit codes)
2. Returns structured output (JSON or minimal text)
3. Exits with 0 on success, non-zero on failure
4. Validates all critical components

**Python Verification Pattern:**
```python
#!/usr/bin/env python3
import subprocess, json, sys

def verify_deployment():
    result = subprocess.run(
        ["kubectl", "get", "pods", "-n", "kafka", "-o", "json"],
        capture_output=True, text=True, check=True
    )
    pods = json.loads(result.stdout)["items"]

    running = sum(1 for p in pods if p["status"]["phase"] == "Running")
    total = len(pods)

    if running == total:
        print(f"✓ All {total} pods running")
        return 0
    else:
        print(f"✗ {running}/{total} pods running")
        return 1

if __name__ == "__main__":
    sys.exit(verify_deployment())
```

### Section 4.05: Required Skills for LearnFlow
Minimum Skills to be developed:

1. **agents-md-gen** - Generate AGENTS.md files from codebase
2. **kafka-k8s-setup** - Deploy Kafka on Kubernetes
3. **postgres-k8s-setup** - Deploy PostgreSQL with migrations
4. **fastapi-dapr-agent** - Scaffold FastAPI service with Dapr
5. **nextjs-k8s-deploy** - Deploy Next.js frontend
6. **mcp-code-execution** - Template for MCP wrapper pattern
7. **dapr-pubsub-binding** - Configure Dapr pub/sub components
8. **docusaurus-deploy** - Deploy documentation site

---

## Article V: Agentic Workflow & Autonomy

### Section 5.01: Single-Prompt-to-Deployment Principle
The gold standard: AI agents must complete tasks with **zero manual intervention** after the initial prompt.

**Example Workflow:**
```
User: "Deploy Kafka cluster for LearnFlow"
↓
Claude/Goose loads kafka-k8s-setup skill
↓
Executes ./scripts/deploy.sh
↓
Executes python scripts/verify.py
↓
Reports: "✓ Kafka deployed, 3 pods running"
```

**Zero manual steps allowed.** If intervention is required, the Skill is incomplete.

### Section 5.02: Skill Discovery and Loading
- Skills discovered automatically from `.claude/skills/` directory
- AI agents load SKILL.md on-demand when task matches skill description
- REFERENCE.md loaded only when explicitly requested (on-demand documentation)
- Scripts never loaded into context (executed externally)

### Section 5.03: Error Handling and Recovery
Skills must include:
1. Pre-flight checks (validate prerequisites)
2. Idempotent operations (safe to retry)
3. Rollback mechanisms for failed deployments
4. Clear error messages with remediation steps
5. Verification steps that validate actual state

**Autonomy Requirement:** Agents must be able to recover from common failures without human intervention.

### Section 5.04: Manual Code Prohibition
**STRICT PROHIBITION:** Writing application code manually is not allowed.

Permitted actions:
- ✅ Write SKILL.md files
- ✅ Write execution scripts (bash, Python)
- ✅ Write verification scripts
- ✅ Write infrastructure as code (Helm charts, K8s manifests)
- ✅ Review and test AI-generated code

Prohibited actions:
- ❌ Write FastAPI service code manually
- ❌ Write Next.js component code manually
- ❌ Write business logic manually
- ❌ Write agent implementations manually

**Exception:** Fixing critical bugs in AI-generated code (must document in git commit).

---

## Article VI: Data Architecture & State Management

### Section 6.01: Source of Truth
- **Neon PostgreSQL**: Primary database for relational data
- **Dapr State Stores**: Service state and ephemeral data
- **Kafka Topics**: Event log (source of truth for event-driven state)

### Section 6.02: Database Schema Standards
- Use SQLModel (SQLAlchemy + Pydantic) for schema definitions
- All models must include: `id`, `created_at`, `updated_at`
- Implement soft deletes (use `deleted_at` timestamp)
- Include version tracking for schema migrations

**Required Tables:**
- `students` - Student profiles
- `teachers` - Teacher profiles
- `modules` - Python curriculum modules
- `exercises` - Coding challenges
- `submissions` - Code submissions
- `quiz_results` - Quiz scores
- `progress` - Mastery tracking
- `struggle_events` - Struggle detection log

### Section 6.03: Event Sourcing Requirements
All state changes must emit events:
1. Command executed → Event published to Kafka
2. Event consumed by interested services
3. Services update their local state
4. Dapr state stores maintain materialized views

**Event Schema:**
```json
{
  "event_id": "uuid",
  "event_type": "learning.module.completed",
  "timestamp": "2026-01-20T10:30:00Z",
  "source": "progress-service",
  "version": "1.0",
  "data": { /* event-specific payload */ }
}
```

### Section 6.04: Mastery Calculation Algorithm
Topic Mastery Score = Weighted average:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality ratings: 20%
- Consistency (streak): 10%

**Mastery Levels:**
- 0-40%: Beginner (Red)
- 41-70%: Learning (Yellow)
- 71-90%: Proficient (Green)
- 91-100%: Mastered (Blue)

### Section 6.05: Struggle Detection Rules
Trigger struggle alerts when:
1. Same error type encountered 3+ times
2. Stuck on exercise > 10 minutes
3. Quiz score < 50%
4. Student explicitly states "I don't understand" or "I'm stuck"
5. 5+ failed code executions in a row

Struggle events published to `struggle.detected` topic with student_id, module_id, and struggle_type.

---

## Article VII: AI Agent System Architecture

### Section 7.01: Multi-Agent System Design
LearnFlow implements specialized agents for different tutoring functions:

**Agent Responsibilities:**
1. **Triage Agent** - Routes queries to appropriate specialist
   - Input: Student message
   - Logic: Classifies intent (explain, debug, exercise, review)
   - Output: Routed to specialist agent

2. **Concepts Agent** - Explains Python concepts
   - Input: Topic query, student level
   - Logic: Generate adaptive explanations with examples
   - Output: Explanation + code examples + visualizations

3. **Code Review Agent** - Analyzes code quality
   - Input: Student code submission
   - Logic: Check correctness, PEP 8 compliance, efficiency
   - Output: Quality score + specific feedback

4. **Debug Agent** - Parses errors and provides hints
   - Input: Error message + code
   - Logic: Identify root cause, provide progressive hints
   - Output: Hint (not solution) + explanation

5. **Exercise Agent** - Generates and grades challenges
   - Input: Topic, difficulty level
   - Logic: Generate exercises, auto-grade submissions
   - Output: Exercise description + test cases

6. **Progress Agent** - Tracks mastery and provides summaries
   - Input: Student activity events
   - Logic: Calculate mastery scores, detect patterns
   - Output: Progress dashboard + recommendations

### Section 7.02: Code Execution Sandbox
All student code execution must use secure sandbox:
- **Timeout**: 5 seconds maximum
- **Memory**: 50MB limit
- **Filesystem**: No access (temporary only)
- **Network**: Disabled
- **Imports**: Standard library only (MVP phase)

Implementation: Use restricted Python subprocess or specialized sandboxing library.

### Section 7.03: Agent Communication Protocol
Agents communicate via:
1. **Dapr Service Invocation** (synchronous)
2. **Kafka Events** (asynchronous)

**Dapr Invocation:**
```python
# Dapr sidecar handles service discovery and load balancing
response = requests.post(
    "http://localhost:3500/v1.0/invoke/concepts-agent/method/explain",
    json={"topic": "for-loops", "level": "beginner"}
)
```

**Kafka Events:**
```python
# Dapr pub/sub API for event publishing
await dapr_client.publish_event(
    pubsub_name="kafka-pubsub",
    topic_name="code.submitted",
    data=event_data
)
```

---

## Article VIII: Testing & Quality Assurance

### Section 8.01: Skill Testing Requirements
Each Skill must be tested with both Claude Code and Goose:
- **Test 1**: Single-prompt deployment scenario
- **Test 2**: Idempotency test (run twice, expect same result)
- **Test 3**: Error recovery test (simulate failure, verify rollback)
- **Test 4**: Verification validation (confirm verify.py detects issues)

**Test Record:** Document test results in `skills-library/docs/<skill-name>-test-results.md`

### Section 8.02: Application Testing
AI-generated code must pass:
1. Unit tests (pytest for FastAPI)
2. Integration tests (Docker Compose test suite)
3. End-to-end tests (Playwright for frontend)
4. Load tests (k6 for API performance)
5. Security scans (Snyk, Trivy)

### Section 8.03: Token Efficiency Validation
For each Skill, measure:
- Tokens loaded: Count tokens in SKILL.md
- Tokens in result: Count tokens returned from verify.py
- Token reduction: (Direct MCP tokens - Skill tokens) / Direct MCP tokens

**Target:** 98% token reduction (50,000 → 1,000 tokens or less)

---

## Article IX: Documentation Standards

### Section 9.01: Docusaurus Documentation Site
All documentation must be published via Docusaurus:
- Architecture decisions
- Skill usage guides
- API documentation
- Deployment runbooks
- Troubleshooting guides

**Deployment:** Automated via `docusaurus-deploy` Skill

### Section 9.02: Self-Documenting Infrastructure
All infrastructure must include:
1. README.md in repository root
2. AGENTS.md with repository structure and conventions
3. Skill REFERENCE.md files for advanced configuration
4. Inline comments in Helm charts and manifests
5. Architecture Decision Records (ADRs) for major decisions

### Section 9.03: Agentic Workflow Documentation
Document in commit messages:
- "Claude: implemented [feature] using [skill-name] skill"
- "Goose: deployed [service] using [skill-name] skill"
- "Manual fix: [reason] after AI generation"

---

## Article X: Deployment & Operations

### Section 10.01: GitOps Workflow
Use Argo CD for continuous delivery:
1. GitHub repository as source of truth
2. Argo CD monitors repository changes
3. Automatic sync to Kubernetes cluster
4. Health checks and auto-retry on failure

### Section 10.02: Local Development with Minikube
All development must work on Minikube:
```bash
minikube start --cpus=4 --memory=8192 --driver=docker
```

**Requirements:**
- Services must deploy successfully to Minikube
- Kafka must run in single-node mode for local
- All services must be testable locally
- Port forwarding for frontend access

### Section 10.03: Production Deployment
Cloud deployment on Azure, Google Cloud, or Oracle Cloud:
- Multi-node Kubernetes cluster
- Managed Kafka (Confluent Cloud or AWS MSK)
- Managed PostgreSQL (Neon or Cloud SQL)
- CI/CD with GitHub Actions + Argo CD
- Monitoring with Prometheus + Grafana

---

## Article XI: Evaluation Criteria Alignment

### Section 11.01: Skills Autonomy (15% weight)
**Gold Standard:** Single prompt → Running deployment → Zero manual intervention

**Success Metrics:**
- Can deploy entire LearnFlow with one prompt
- No human intervention required
- All verifications pass automatically

### Section 11.02: Token Efficiency (10% weight)
**Gold Standard:** 98% token reduction through code execution pattern

**Success Metrics:**
- SKILL.md < 150 tokens
- Total execution < 200 tokens
- Verified token reduction calculation

### Section 11.03: Cross-Agent Compatibility (5% weight)
**Gold Standard:** Same skill works identically on Claude Code and Goose

**Success Metrics:**
- Skills placed in `.claude/skills/` directory
- Works on both agents without modification
- Tested and documented for both

### Section 11.04: Architecture (20% weight)
**Gold Standard:** Correct Dapr patterns, Kafka pub/sub, stateless microservices

**Success Metrics:**
- All microservices use Dapr sidecars
- All communication via Kafka or Dapr
- State stored in Dapr state stores
- No local state in services

### Section 11.05: MCP Integration (10% weight)
**Gold Standard:** MCP server provides rich context for debugging

**Success Metrics:**
- MCP server deployed separately
- Skills wrap MCP calls in scripts
- Actions logged and observable

### Section 11.06: Documentation (10% weight)
**Gold Standard:** Comprehensive Docusaurus site deployed via Skill

**Success Metrics:**
- Complete API documentation
- Architecture diagrams
- Deployment guides
- Troubleshooting section

### Section 11.07: Spec-Kit Plus Usage (15% weight)
**Gold Standard:** High-level specs translate cleanly to agentic instructions

**Success Metrics:**
- specs/ directory with feature specifications
- Skills reference spec documents
- Traceability from spec to implementation

### Section 11.08: LearnFlow Completion (15% weight)
**Gold Standard:** Application built entirely via Skills

**Success Metrics:**
- Zero manual code in application layer
- All features implemented by AI agents
- Working demo scenario passes

---

## Article XII: Commitment to Excellence

### Section 12.01: Continuous Skill Refinement
Skills are not static. They must evolve through:
- Testing with different scenarios
- Incorporating feedback from failed attempts
- Measuring token efficiency improvements
- Documenting edge cases and workarounds

### Section 12.02: Knowledge Sharing
All Skills must be:
- Documented with clear examples
- Shared across the team
- Tested by multiple people
- Version controlled with meaningful commits

### Section 12.03: Winning Mindset
Our goal is not to complete the project - our goal is to:
- Demonstrate 98% token reduction
- Achieve single-prompt-to-deployment
- Build reusable Skills that work across agents
- Win by showcasing mastery of agentic development

---

## Amendment Process

This constitution is a living document. Amendments require:
1. Architectural Decision Record (ADR) proposing changes
2. Review and approval from team lead
3. Update to version number
4. Communication to all team members

---

## Ratification

This constitution becomes effective immediately upon ratification by the project team. All members commit to upholding these principles and contributing to the project's success.

**Ratified:** 2026-01-20
**Version:** 1.0.0
**Project:** LearnFlow - Hackathon III

---

**Remember:** We are not coders - we are teachers of machines. Our Skills are our product. Our success is measured by the autonomy we enable.

[GOVERNANCE_RULES]
<!-- Example: All PRs/reviews must verify compliance; Complexity must be justified; Use [GUIDANCE_FILE] for runtime development guidance -->

**Version**: [CONSTITUTION_VERSION] | **Ratified**: [RATIFICATION_DATE] | **Last Amended**: [LAST_AMENDED_DATE]
<!-- Example: Version: 2.1.1 | Ratified: 2025-06-13 | Last Amended: 2025-07-16 -->
