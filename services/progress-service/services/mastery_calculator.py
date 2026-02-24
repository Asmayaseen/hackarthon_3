from models.student_progress import StudentProgress
from datetime import datetime

def calculate_mastery(progress: StudentProgress) -> float:
    """Article VI Section 6.04: Weighted average"""
    exercise_rate = (progress.exercises_completed / max(progress.total_exercises, 1)) * 40
    quiz_weight = progress.avg_quiz_score * 30
    code_weight = progress.avg_code_quality * 20
    consistency = progress.consistency_score * 10  # Streak logic TBD

    return min(100.0, max(0.0, exercise_rate + quiz_weight + code_weight + consistency))
