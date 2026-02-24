from fastapi import APIRouter, Request
from dapr.ext.fastapi import DaprApp
import json
from models.student_progress import StudentProgress
from services.mastery_calculator import calculate_mastery  # Will implement next

router = APIRouter()

@router.post("/events")
async def handle_events(request: Request):
    data = await request.json()
    topic = request.headers.get("ce-topic", "")

    if topic in ["code.review.completed", "exercise.graded"]:
        student_id = data.get("student_id")
        score = data.get("score", 0.0)  # quiz/code score
        event_type = data.get("event_type")

        # Load current progress (pseudo - use Dapr state)
        progress = get_progress(student_id)  # Impl with Dapr state get

        # Update metrics
        if event_type == "exercise":
            progress.exercises_completed += 1
            progress.total_exercises += 1
        # Update avgs, consistency...

        # Calc mastery
        progress.mastery_score = calculate_mastery(progress)
        progress.last_activity = datetime.utcnow()

        # Save to Dapr state
        save_progress(student_id, progress)

        # Check struggles...

    return {"status": "processed"}
