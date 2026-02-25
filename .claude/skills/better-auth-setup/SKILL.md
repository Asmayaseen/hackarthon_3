---
name: better-auth-setup
description: Configure Better Auth for JWT-based authentication in LearnFlow with student and teacher roles
triggers:
  - "setup authentication"
  - "add better auth"
  - "jwt auth"
  - "student login"
  - "teacher auth"
---

# Better Auth Setup

## When to Use
- Adding authentication to LearnFlow frontend and API
- Configuring student/teacher role-based access control
- Setting up JWT token issuance and verification
- Integrating OAuth providers (Google, GitHub)

## Instructions

1. Install Better Auth:
   ```bash
   bash scripts/install.sh
   ```

2. Generate auth configuration:
   ```bash
   python scripts/configure.py
   ```

3. Apply database migrations:
   ```bash
   bash scripts/migrate.sh
   ```

4. Verify auth endpoints:
   ```bash
   python scripts/verify.py
   ```

## Auth Roles
| Role | Access |
|------|--------|
| `student` | Dashboard, code editor, quizzes, AI chat |
| `teacher` | Student monitoring, exercise generation, struggle alerts |
| `admin` | Full access, user management |

## Endpoints Added
- `POST /auth/login` — Email/password login
- `POST /auth/register` — New account creation
- `GET /auth/session` — Current session
- `POST /auth/logout` — Sign out

## Validation
- [ ] Auth tables created in PostgreSQL
- [ ] JWT tokens issued on login
- [ ] Role-based routes protected
- [ ] Session cookie set correctly

See [REFERENCE.md](./REFERENCE.md) for OAuth setup and JWKS endpoint config.
