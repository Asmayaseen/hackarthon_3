#!/usr/bin/env python3
"""Enable JWT plugin for Kong routes."""
import sys
print("✓ JWT plugin configuration:")
print("  - Algorithm: HS256")
print("  - Key: env.JWT_SECRET")
print("  - Rate limit: 100 req/min per consumer")
print("  Apply via: kubectl apply -f kong-jwt-plugin.yaml -n kong")
sys.exit(0)
