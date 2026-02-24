from typing import Optional
from sqlmodel import SQLModel, Field
from datetime import datetime

class StudentProgress(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    student_id: str = Field(index=True)
    mastery_score: float = 0.0
    exercises_completed: int = 0
    total_exercises: int = 0
    avg_quiz_score: float = 0.0
    avg_code_quality: float = 0.0
    consistency_score: float = 0.0
    last_activity: datetime = Field(default_factory=datetime.utcnow)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
