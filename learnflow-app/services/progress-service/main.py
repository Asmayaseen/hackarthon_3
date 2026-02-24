"""
Progress Service - Calculates mastery scores and detects student struggle patterns

Following Constitution Article VI (Mastery Calculation) and Article VI.05 (Struggle Detection):
- Input: Student events from Kafka (exercise completions, quiz scores, code reviews)
- Logic: Calculate mastery scores, detect struggle patterns, generate progress insights
- Output: Progress updates and struggle alerts

Per Article VI.04, mastery score components:
- Exercise completion: 40%
- Quiz scores: 30%
- Code quality: 20%
- Consistency: 10%
"""

import asyncio
import json
import logging
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel

import httpx
from dapr.clients import DaprClient
from fastapi import FastAPI, HTTPException
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Progress Service",
    description="Calculates student mastery scores and detects struggle patterns",
    version="1.0.0"
)

# Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
DAPR_STATE_STORE = os.getenv("DAPR_STATE_STORE", "statestore")

# OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Data Models
class StudentProgress(BaseModel):
    """Student progress data"""
    student_id: str
    mastery_score: float  # 0-100
    exercises_completed: int
    total_exercises: int
    average_quiz_score: float
    average_code_quality: float
    consistency_score: float
    last_activity: str
    topics_mastered: List[str]
    topics_struggling: List[str]
    recommendations: List[str]


class StruggleAlert(BaseModel):
    """Struggle detection alert"""
    student_id: str
    alert_type: str  # "completion_rate", "repeated_failures", "low_scores"
    severity: str  # "low", "medium", "high"
    message: str
    recommendations: List[str]
    timestamp: str


# In-memory storage (replace with Dapr state store in production)
student_progress_db: Dict[str, StudentProgress] = {}
student_events_db: Dict[str, List[Dict]] = {}


def calculate_mastery_score(
    exercise_completion_rate: float,
    average_quiz_score: float,
    average_code_quality: float,
    consistency_score: float
) -> float:
    """
    Calculate mastery score per Constitution Article VI.04:
    - Exercise completion: 40%
    - Quiz scores: 30%
    - Code quality: 20%
    - Consistency: 10%
    """
    mastery = (
        exercise_completion_rate * 0.4 +
        average_quiz_score * 0.3 +
        average_code_quality * 0.2 +
        consistency_score * 0.1
    )
    return round(mastery, 2)


def detect_struggle_patterns(student_id: str, events: List[Dict]) -> Optional[StruggleAlert]:
    """
    Detect struggle patterns per Constitution Article VI.05:
    - <50% exercise completion rate over 7 days
    - Repeated failures on same topic
    - 3 consecutive low scores (<60%)
    """
    try:
        # Filter recent events (last 7 days)
        week_ago = datetime.utcnow() - timedelta(days=7)
        recent_events = [
            e for e in events
            if datetime.fromisoformat(e["timestamp"]) > week_ago
        ]

        # Check 1: Low completion rate
        exercise_events = [e for e in recent_events if e["event_type"] == "exercise"]
        if len(exercise_events) >= 5:  # At least 5 exercises attempted
            completed = len([e for e in exercise_events if e.get("status") == "completed"])
            completion_rate = completed / len(exercise_events)

            if completion_rate < 0.5:
                return StruggleAlert(
                    student_id=student_id,
                    alert_type="completion_rate",
                    severity="high",
                    message=f"Low completion rate: {completion_rate:.0%} over last 7 days",
                    recommendations=[
                        "Consider easier exercises",
                        "Review foundational concepts",
                        "Increase hint usage"
                    ],
                    timestamp=datetime.utcnow().isoformat()
                )

        # Check 2: Repeated failures on same topic
        topic_failures = {}
        for event in exercise_events:
            if event.get("status") == "failed":
                topic = event.get("topic", "unknown")
                topic_failures[topic] = topic_failures.get(topic, 0) + 1

        for topic, failures in topic_failures.items():
            if failures >= 3:
                return StruggleAlert(
                    student_id=student_id,
                    alert_type="repeated_failures",
                    severity="medium",
                    message=f"Repeated failures on topic: {topic} ({failures} attempts)",
                    recommendations=[
                        f"Review {topic} fundamentals",
                        "Request concepts explanation",
                        "Try related easier exercises"
                    ],
                    timestamp=datetime.utcnow().isoformat()
                )

        # Check 3: Consecutive low scores
        graded_events = [e for e in recent_events if e["event_type"] == "graded" and "score" in e]
        graded_events.sort(key=lambda x: x["timestamp"])

        consecutive_low = 0
        for event in graded_events[-3:]:  # Check last 3
            if event["score"] < 60:
                consecutive_low += 1

        if consecutive_low >= 3:
            return StruggleAlert(
                student_id=student_id,
                alert_type="low_scores",
                severity="medium",
                message=f"Three consecutive low scores (<60%)",
                recommendations=[
                    "Review basic concepts",
                    "Use hints system more actively",
                    "Focus on one concept at a time"
                ],
                timestamp=datetime.utcnow().isoformat()
            )

        return None

    except Exception as e:
        logger.error(f"Struggle detection error: {e}")
        return None


async def update_progress_from_event(event_data: Dict):
    """Update student progress based on incoming event"""
    try:
        student_id = event_data.get("student_id")
        if not student_id:
            logger.warning("No student_id in event")
            return

        # Initialize student data if new
        if student_id not in student_progress_db:
            student_progress_db[student_id] = StudentProgress(
                student_id=student_id,
                mastery_score=0.0,
                exercises_completed=0,
                total_exercises=0,
                average_quiz_score=0.0,
                average_code_quality=0.0,
                consistency_score=0.0,
                last_activity=datetime.utcnow().isoformat(),
                topics_mastered=[],
                topics_struggling=[],
                recommendations=[]
            )

        # Store event
        if student_id not in student_events_db:
            student_events_db[student_id] = []
        student_events_db[student_id].append(event_data)

        # Update metrics based on event type
        progress = student_progress_db[student_id]
        event_type = event_data.get("event_type")

        if event_type == "exercise":
            progress.total_exercises += 1
            if event_data.get("status") == "completed":
                progress.exercises_completed += 1

        elif event_type == "quiz":
            score = event_data.get("score", 0)
            # Simple moving average calculation
            if progress.average_quiz_score == 0:
                progress.average_quiz_score = score
            else:
                progress.average_quiz_score = (progress.average_quiz_score + score) / 2

        elif event_type == "code_review":
            quality_score = event_data.get("quality_score", 0)
            if progress.average_code_quality == 0:
                progress.average_code_quality = quality_score
            else:
                progress.average_code_quality = (progress.average_code_quality + quality_score) / 2

        # Calculate exercise completion rate
        completion_rate = (
            progress.exercises_completed / progress.total_exercises
            if progress.total_exercises > 0
            else 0.0
        )

        # Update consistency (simplified: based on recent activity)
        progress.consistency_score = min(100.0, len(student_events_db[student_id]) * 5)

        # Recalculate mastery score
        progress.mastery_score = calculate_mastery_score(
            completion_rate,
            progress.average_quiz_score,
            progress.average_code_quality,
            progress.consistency_score
        )

        progress.last_activity = datetime.utcnow().isoformat()

        # Detect struggle patterns
        alert = detect_struggle_patterns(student_id, student_events_db[student_id])
        if alert:
            await publish_struggle_alert(alert)

        logger.info(f"Updated progress for {student_id}: mastery={progress.mastery_score}")

    except Exception as e:
        logger.error(f"Progress update error: {e}")


async def publish_progress_update(progress: StudentProgress):
    """Publish progress update event"""
    try:
        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/progress.updated"

            resp = await client.post(
                dapr_url,
                json=progress.dict(),
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if resp.status_code == 204:
                logger.info(f"Published progress update for: {progress.student_id}")
                return True
            else:
                logger.error(f"Failed to publish progress: {resp.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing progress: {e}")
        return False


async def publish_struggle_alert(alert: StruggleAlert):
    """Publish struggle alert event"""
    try:
        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/struggle.detected"

            resp = await client.post(
                dapr_url,
                json=alert.dict(),
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if resp.status_code == 204:
                logger.info(f"Published struggle alert for: {alert.student_id}")
                return True
            else:
                logger.error(f"Failed to publish struggle alert: {resp.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing struggle alert: {e}")
        return False


# HTTP Endpoints
@app.post("/process-event")
async def process_event(event_data: Dict):
    """
    Process student event and update progress
    """
    try:
        logger.info(f"Processing event: {event_data.get('event_type')} for {event_data.get('student_id')}")

        await update_progress_from_event(event_data)

        return {"status": "success", "message": "Event processed"}

    except Exception as e:
        logger.error(f"Event processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/progress/{student_id}", response_model=StudentProgress)
async def get_progress(student_id: str):
    """
    Get student progress data
    """
    try:
        if student_id not in student_progress_db:
            raise HTTPException(status_code=404, detail="Student not found")

        progress = student_progress_db[student_id]
        return progress

    except Exception as e:
        logger.error(f"Progress retrieval error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "progress-service",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    return {
        "message": "Progress Service - Tracks student learning progress",
        "version": "1.0.0",
        "endpoints": [
            "POST /process-event",
            "GET /progress/{student_id}",
            "GET /health"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8005)
