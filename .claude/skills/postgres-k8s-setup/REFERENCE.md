# PostgreSQL Kubernetes Reference

## Architecture
LearnFlow uses CloudNativePG operator for production-grade PostgreSQL with automatic failover.

```
[FastAPI Service] → [Dapr State Store / Direct asyncpg] → [pg-cluster-rw:5432]
                                                                    ↓
                                                          [pg-cluster-ro:5432] (reads)
```

## Connection Details
```bash
# Read-write (for writes)
host: pg-cluster-rw.learnflow.svc.cluster.local
port: 5432
database: learnflow

# Read-only (for reads - load balanced)
host: pg-cluster-ro.learnflow.svc.cluster.local
port: 5432
database: learnflow

# Get credentials from secret
kubectl get secret pg-cluster-app -n learnflow -o jsonpath='{.data.uri}' | base64 -d
```

## Schema
```sql
-- Students
CREATE TABLE students (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name VARCHAR(255) NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    level VARCHAR(50) DEFAULT 'beginner',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Progress tracking
CREATE TABLE student_progress (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    topic VARCHAR(100) NOT NULL,
    mastery_score DECIMAL(5,2) DEFAULT 0,
    exercises_completed INTEGER DEFAULT 0,
    quiz_average DECIMAL(5,2) DEFAULT 0,
    code_quality_avg DECIMAL(5,2) DEFAULT 0,
    consistency_score DECIMAL(5,2) DEFAULT 0,
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Exercise submissions
CREATE TABLE exercise_submissions (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    exercise_id VARCHAR(100) NOT NULL,
    code TEXT NOT NULL,
    score DECIMAL(5,2),
    passed BOOLEAN DEFAULT FALSE,
    feedback TEXT,
    submitted_at TIMESTAMPTZ DEFAULT NOW()
);

-- Quiz results
CREATE TABLE quiz_results (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    topic VARCHAR(100) NOT NULL,
    score DECIMAL(5,2) NOT NULL,
    total_questions INTEGER,
    correct_answers INTEGER,
    taken_at TIMESTAMPTZ DEFAULT NOW()
);

-- Struggle alerts
CREATE TABLE struggle_alerts (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    student_id UUID REFERENCES students(id),
    alert_type VARCHAR(100) NOT NULL,
    severity VARCHAR(20) DEFAULT 'medium',
    message TEXT,
    resolved BOOLEAN DEFAULT FALSE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);
```

## Common Operations
```bash
# Connect to database (psql)
kubectl exec -it -n learnflow \
  $(kubectl get pod -n learnflow -l cnpg.io/cluster=pg-cluster -o name | head -1) \
  -- psql -U learnflow -d learnflow

# Backup
kubectl apply -f k8s/postgres-backup.yaml

# Scale replicas
kubectl patch cluster pg-cluster -n learnflow \
  --type=merge -p '{"spec":{"instances":3}}'
```

## Troubleshooting
```bash
# Check cluster status
kubectl get cluster -n learnflow

# View cluster events
kubectl describe cluster pg-cluster -n learnflow

# Check pod logs
kubectl logs -n learnflow -l cnpg.io/cluster=pg-cluster --tail=50
```
