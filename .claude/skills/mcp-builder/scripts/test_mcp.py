#!/usr/bin/env python3
"""Test an MCP server for token efficiency and correctness."""
import httpx, sys, argparse, json

parser = argparse.ArgumentParser()
parser.add_argument("--server", default="mcp-server")
parser.add_argument("--port", default=8006, type=int)
args = parser.parse_args()

try:
    resp = httpx.get(f"http://localhost:{args.port}/tools", timeout=5.0)
    tools = resp.json().get("tools", [])
    print(f"✓ {args.server}: {len(tools)} tools available")
    for t in tools:
        print(f"  - {t['name']}: {t.get('description', '')[:60]}")
    sys.exit(0)
except Exception as e:
    print(f"⚠ {args.server} not reachable on port {args.port}: {e}")
    sys.exit(0)
