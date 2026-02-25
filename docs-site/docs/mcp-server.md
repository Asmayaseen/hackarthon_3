---
id: mcp-server
title: MCP Server
sidebar_position: 5
---

# LearnFlow MCP Server

The MCP Server provides AI agents real-time context about the LearnFlow platform.

## Why MCP?

Without MCP, agents must guess at system state. With the LearnFlow MCP Server:

- Agents know which pods are running
- Agents can check student progress
- Agents can see Kafka topic status
- Agents can diagnose service health

## Tools Available

| Tool | Description | Output |
|------|-------------|--------|
| `get_cluster_status` | K8s pod status for all services | `"✓ 8/8 pods running"` |
| `get_service_health` | Health check for specific service | `{status: "healthy"}` |
| `get_student_progress` | Student mastery and struggle data | `"4 topics @ 68% avg mastery"` |
| `get_kafka_topics` | All Kafka topics and routing | List of 6 topics |
| `get_recent_errors` | Recent error logs | Error count + top 5 |
| `get_system_overview` | Full platform summary | Compact system state |

## Token Efficiency

Following the MCP Code Execution pattern:

```
Traditional MCP: kubectl MCP server loaded = ~15,000 tokens at startup
LearnFlow MCP:   /call tool invoked → minimal result = ~50 tokens
```

## Usage

```bash
# Start server locally
cd learnflow-app/services/mcp-server
uvicorn main:app --port 8006

# Get system overview
curl -X POST http://localhost:8006/tools/get_system_overview

# Call any tool
curl -X POST http://localhost:8006/call \
  -H "Content-Type: application/json" \
  -d '{"tool": "get_student_progress", "params": {"student_id": "maya"}}'
```

## API Docs

When running: [http://localhost:8006/docs](http://localhost:8006/docs)

## Integration with AI Agents

```python
# In a Skill script — calls MCP externally, only result enters context
import httpx, sys

resp = httpx.post("http://mcp-server:8006/tools/get_cluster_status")
data = resp.json()
print(data["summary"])  # "✓ 8/8 pods running" — ~5 tokens in context
sys.exit(0 if "✓" in data["summary"] else 1)
```
