# MCP Code Execution Reference

## Token Cost Comparison

| Approach | Tokens | Context Usage |
|----------|--------|--------------|
| 5 direct MCP servers | ~50,000 | 25% of context before typing |
| SKILL.md + scripts | ~110 | <1% — 97% FREE |

## Pattern: Data Filtering in Script
```python
# INEFFICIENT - all data into context
# TOOL CALL: gdrive.getSheet(sheetId: 'abc123')
# → returns 10,000 rows into context

# EFFICIENT - filter in script, only result in context
async def get_pending_items():
    all_rows = await gdrive.get_sheet(sheet_id='abc123')
    pending = [r for r in all_rows if r['status'] == 'pending']
    print(f"✓ {len(pending)} pending items")  # Only this enters context
```

## Pattern: Kubernetes MCP → Script
```python
#!/usr/bin/env python3
# scripts/get_pods.py - Replaces: kubernetes.getPods()
import subprocess, json, sys

def main():
    ns = sys.argv[1] if len(sys.argv) > 1 else 'learnflow'
    result = subprocess.run(
        ['kubectl', 'get', 'pods', '-n', ns, '-o', 'json'],
        capture_output=True, text=True
    )
    pods = json.loads(result.stdout)['items']
    running = sum(1 for p in pods if p['status']['phase'] == 'Running')
    total = len(pods)
    # Only this enters agent context:
    if running == total:
        print(f"✓ All {total} pods running in {ns}")
        sys.exit(0)
    else:
        print(f"✗ {running}/{total} pods running")
        sys.exit(1)

main()
```

## Pattern: Database MCP → Script
```python
#!/usr/bin/env python3
# scripts/check_progress.py - Replaces: postgres.query()
import subprocess, sys

def main():
    student_id = sys.argv[1]
    pod = subprocess.run(
        ['kubectl', 'get', 'pod', '-n', 'learnflow',
         '-l', 'cnpg.io/cluster=pg-cluster',
         '-o', 'jsonpath={.items[0].metadata.name}'],
        capture_output=True, text=True
    ).stdout.strip()

    result = subprocess.run(
        ['kubectl', 'exec', '-n', 'learnflow', pod, '--',
         'psql', '-U', 'learnflow', '-d', 'learnflow', '-t', '-c',
         f"SELECT topic, mastery_score FROM student_progress WHERE student_id='{student_id}'"],
        capture_output=True, text=True
    )
    # Minimal output - only summary
    rows = [r.strip() for r in result.stdout.strip().split('\n') if r.strip()]
    print(f"✓ {len(rows)} topic(s) tracked for student {student_id[:8]}...")
    for row in rows[:3]:  # Max 3 rows in context
        print(f"  {row}")

main()
```

## Pattern: API MCP → Script
```python
#!/usr/bin/env python3
# scripts/check_service.py - Replaces: api.getStatus()
import subprocess, sys

def main():
    svc = sys.argv[1] if len(sys.argv) > 1 else 'triage-service'
    result = subprocess.run(
        ['kubectl', 'exec', '-n', 'learnflow',
         f'deployment/{svc}', '--',
         'curl', '-sf', 'http://localhost:8000/health'],
        capture_output=True, text=True
    )
    if result.returncode == 0:
        print(f"✓ {svc} is healthy")
        sys.exit(0)
    else:
        print(f"✗ {svc} health check failed")
        sys.exit(1)

main()
```

## Script Output Rules
1. Print ✓ for success, ✗ for failure
2. Maximum 5 lines of output
3. Exit 0 for success, 1 for failure
4. Never dump raw JSON — always summarize
5. Include only actionable information

## Directory Structure for Each Skill
```
.claude/skills/<skill-name>/
├── SKILL.md          # ~100 tokens — agent instructions
├── REFERENCE.md      # 0 tokens — loaded only when needed
└── scripts/
    ├── deploy.sh     # 0 tokens — executed, not loaded
    ├── verify.py     # 0 tokens — executed, not loaded
    └── *.py          # 0 tokens — executed, not loaded
```
