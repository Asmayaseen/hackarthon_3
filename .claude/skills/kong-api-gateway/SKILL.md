---
name: kong-api-gateway
description: Deploy Kong API Gateway on Kubernetes with JWT auth, rate limiting, and routing to all LearnFlow services
triggers:
  - "deploy api gateway"
  - "setup kong"
  - "add jwt authentication"
  - "api rate limiting"
  - "route api traffic"
---

# Kong API Gateway

## When to Use
- Adding centralized JWT authentication for all LearnFlow APIs
- Rate limiting student requests to prevent abuse
- Single entry point routing to all backend services
- Adding CORS, logging, and request transformation

## Instructions

1. Deploy Kong via Helm:
   ```bash
   bash scripts/deploy.sh
   ```

2. Configure LearnFlow routes:
   ```bash
   python scripts/configure_routes.py
   ```

3. Add JWT authentication plugin:
   ```bash
   python scripts/setup_jwt.py
   ```

4. Verify gateway is routing:
   ```bash
   python scripts/verify.py
   ```

## Route Map
| Path | Upstream | Auth |
|------|----------|------|
| `/api/triage` | triage-service:8080 | JWT |
| `/api/concepts` | concepts-service:8001 | JWT |
| `/api/progress` | progress-service:8004 | JWT |
| `/api/execute` | frontend (sandbox) | JWT |
| `/health` | — | None |

## Validation
- [ ] Kong pod Running in kong namespace
- [ ] All service routes configured
- [ ] JWT plugin blocking unauthenticated requests
- [ ] Rate limiting active (100 req/min per student)

See [REFERENCE.md](./REFERENCE.md) for declarative config and plugin list.
