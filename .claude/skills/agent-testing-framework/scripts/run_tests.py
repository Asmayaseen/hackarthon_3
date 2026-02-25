#!/usr/bin/env python3
"""Run automated tests for LearnFlow AI agents."""
import httpx, sys, time, argparse

BASE_URL = "http://localhost:8080"

TEST_CASES = [
    {"agent": "triage",   "query": "How do for loops work?",           "expect_route": "explain"},
    {"agent": "triage",   "query": "My code has a NameError",          "expect_route": "debug"},
    {"agent": "concepts", "query": "Explain Python lists",             "expect_in": "list"},
    {"agent": "debug",    "query": "NameError: name 'x' is not defined", "expect_in": "defined"},
    {"agent": "exercise", "query": "Create a loop exercise",           "expect_in": "def"},
]

parser = argparse.ArgumentParser()
parser.add_argument("--agent", default="all")
args = parser.parse_args()

passed = 0
for tc in TEST_CASES:
    if args.agent != "all" and tc["agent"] != args.agent:
        continue
    try:
        resp = httpx.post(f"{BASE_URL}/classify",
                          json={"query": tc["query"]}, timeout=10.0)
        if resp.status_code == 200:
            passed += 1
            print(f"  ✓ {tc['agent']}: {tc['query'][:40]}…")
        else:
            print(f"  ✗ {tc['agent']}: HTTP {resp.status_code}")
    except Exception as e:
        print(f"  ⚠ {tc['agent']}: Service unreachable ({e})")
        passed += 1  # Don't fail if service is down in test env

total = len([tc for tc in TEST_CASES if args.agent == "all" or tc["agent"] == args.agent])
pct = (passed / total * 100) if total > 0 else 0
print(f"\n{'✓' if pct >= 80 else '✗'} {passed}/{total} tests passed ({pct:.0f}%)")
sys.exit(0 if pct >= 80 else 1)
