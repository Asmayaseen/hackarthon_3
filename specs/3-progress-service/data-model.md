# Data Model: Progress Service

## StudentProgress
- student_id: UUID PK
- mastery_score: float (0-100)
- exercises_completed: int
- total_exercises: int
- avg_quiz_score: float
- avg_code_quality: float
- consistency_score: float
- last_activity: timestamp
- topics_mastered: JSON array
- topics_struggling: JSON array
- created_at/updated_at: timestamps
- Validation: scores 0-100

## StruggleAlert
- alert_id: UUID PK
- student_id: FK
- type: enum (completion_rate|repeated_failures|low_scores)
- severity: enum (low|medium|high)
- message: text
- recommendations: text[]
- timestamp: timestamp
- resolved: bool default false

Relationships: StudentProgress 1:1 Dapr state key (student_id)
