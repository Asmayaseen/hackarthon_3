---
name: postgres-k8s-setup
description: Deploy PostgreSQL on Kubernetes for LearnFlow student data persistence
triggers:
  - "deploy postgres"
  - "setup database"
  - "install postgresql"
  - "database not running"
  - "set up postgres"
---

# PostgreSQL Kubernetes Setup

## When to Use
- Setting up persistent storage for LearnFlow student data
- Database pods not running or unreachable
- Running database migrations for progress/exercise tables
- First-time cluster setup requiring a database

## Instructions

1. Deploy PostgreSQL cluster:
   ```bash
   bash scripts/deploy.sh
   ```

2. Run LearnFlow migrations:
   ```bash
   python scripts/migrate.py
   ```

3. Verify database is ready:
   ```bash
   python scripts/verify.py
   ```

## LearnFlow Database Schema
| Table | Purpose |
|-------|---------|
| `students` | Student profiles and auth |
| `student_progress` | Mastery scores per topic |
| `exercise_submissions` | Code submissions + grades |
| `quiz_results` | Quiz scores history |
| `struggle_alerts` | Teacher notifications |

## Validation
- [ ] PostgreSQL pod in Running state
- [ ] Connection secret `pg-cluster-app` exists
- [ ] All 5 LearnFlow tables created
- [ ] Read-write and read-only endpoints available

See [REFERENCE.md](./REFERENCE.md) for schema details and connection strings.
