#!/usr/bin/env python3
import httpx, sys
try:
    resp = httpx.get("http://localhost:3000/api/auth/session", timeout=5.0)
    print(f"✓ Auth endpoint reachable (HTTP {resp.status_code})")
    sys.exit(0)
except Exception as e:
    print(f"⚠ Auth endpoint not reachable: {e}")
    print("  Start frontend: cd learnflow-frontend && npm run dev")
    sys.exit(0)  # Not a hard failure in dev
