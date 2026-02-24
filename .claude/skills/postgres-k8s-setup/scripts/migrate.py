#!/usr/bin/env python3
"""Run LearnFlow database migrations via kubectl port-forward."""
import subprocess
import sys
import time


MIGRATIONS = [
    """
    CREATE TABLE IF NOT EXISTS students (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        name VARCHAR(255) NOT NULL,
        email VARCHAR(255) UNIQUE NOT NULL,
        level VARCHAR(50) DEFAULT 'beginner',
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS student_progress (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        student_id UUID REFERENCES students(id) ON DELETE CASCADE,
        topic VARCHAR(100) NOT NULL,
        mastery_score DECIMAL(5,2) DEFAULT 0,
        exercises_completed INTEGER DEFAULT 0,
        quiz_average DECIMAL(5,2) DEFAULT 0,
        code_quality_avg DECIMAL(5,2) DEFAULT 0,
        consistency_score DECIMAL(5,2) DEFAULT 0,
        updated_at TIMESTAMPTZ DEFAULT NOW(),
        UNIQUE(student_id, topic)
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS exercise_submissions (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        student_id UUID REFERENCES students(id) ON DELETE CASCADE,
        exercise_id VARCHAR(100) NOT NULL,
        code TEXT NOT NULL,
        score DECIMAL(5,2),
        passed BOOLEAN DEFAULT FALSE,
        feedback TEXT,
        submitted_at TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS quiz_results (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        student_id UUID REFERENCES students(id) ON DELETE CASCADE,
        topic VARCHAR(100) NOT NULL,
        score DECIMAL(5,2) NOT NULL,
        total_questions INTEGER,
        correct_answers INTEGER,
        taken_at TIMESTAMPTZ DEFAULT NOW()
    );
    """,
    """
    CREATE TABLE IF NOT EXISTS struggle_alerts (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        student_id UUID REFERENCES students(id) ON DELETE CASCADE,
        alert_type VARCHAR(100) NOT NULL,
        severity VARCHAR(20) DEFAULT 'medium',
        message TEXT,
        resolved BOOLEAN DEFAULT FALSE,
        created_at TIMESTAMPTZ DEFAULT NOW()
    );
    """,
]


def get_pg_pod() -> str:
    result = subprocess.run(
        ['kubectl', 'get', 'pod', '-n', 'learnflow',
         '-l', 'cnpg.io/cluster=pg-cluster',
         '-o', 'jsonpath={.items[0].metadata.name}'],
        capture_output=True, text=True
    )
    return result.stdout.strip()


def run_sql(pod: str, sql: str) -> bool:
    result = subprocess.run(
        ['kubectl', 'exec', '-n', 'learnflow', pod, '--',
         'psql', '-U', 'learnflow', '-d', 'learnflow', '-c', sql],
        capture_output=True, text=True
    )
    return result.returncode == 0


def main():
    pod = get_pg_pod()
    if not pod:
        print('✗ PostgreSQL pod not found. Deploy first: bash scripts/deploy.sh')
        sys.exit(1)

    print(f'Running migrations on pod: {pod}')
    tables = ['students', 'student_progress', 'exercise_submissions', 'quiz_results', 'struggle_alerts']

    for i, (migration, table) in enumerate(zip(MIGRATIONS, tables), 1):
        if run_sql(pod, migration.strip()):
            print(f'  ✓ Table {table} ready')
        else:
            print(f'  ✗ Migration {i} failed for table {table}')
            sys.exit(1)

    print(f'✓ All {len(MIGRATIONS)} migrations applied successfully')


if __name__ == '__main__':
    main()
