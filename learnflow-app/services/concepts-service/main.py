"""
Concepts Service - Generates adaptive Python concept explanations

Following Constitution:
- Article III: FastAPI + Dapr microservice
- Article VII: Multi-agent system (Concepts Agent)
- Article II: Event-driven architecture with Kafka
"""

import asyncio
import json
import logging
import os
from datetime import datetime
from typing import Literal, Optional, List
from enum import Enum
import time

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

import httpx
from dapr.clients import DaprClient  # type: ignore
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

from openai import AsyncOpenAI

import datetime as dt  # Add this import for datetime operations """

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Concepts Service",
    description="Generates adaptive Python concept explanations for students",
    version="1.0.0"
)

# Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# OpenAI client
openai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)


# Data Models
class ExplanationRequest(BaseModel):
    """Request for generating concept explanation"""
    student_id: str
    query_id: str
    topic: str
    student_level: Literal["beginner", "intermediate", "advanced"]


class ExplanationResponse(BaseModel):
    """Explanation response"""
    student_id: str
    query_id: str
    explanation_text: str
    code_examples: list[str]
    common_pitfalls: list[str]
    related_topics: list[str]
    suggested_exercises: list[str]
    timestamp: str


# Kafka Consumer - Subscribes to learning.query.explain topic
async def process_explanation_request():
    """Continuously consume explanation requests from Kafka"""

    logger.info("Starting Kafka consumer for explanation requests...")

    while True:
        try:
            # Subscribe to topic via Dapr pub/sub
            async with DaprClient() as client:
                subscription = client.subscribe(
                    pubsub_name=DAPR_PUBSUB_NAME,
                    topic="learning.query.explain"
                )

                logger.info("Successfully subscribed to learning.query.explain")

                # Process incoming messages
                async for event in subscription:
                    try:
                        data = event.data

                        if isinstance(data, bytes):
                            data = json.loads(data.decode('utf-8'))

                        logger.info(f"Received explanation request for student {data.get('student_id')}")

                        # Generate explanation
                        explanation = await generate_explanation(
                            topic=data.get('topic', data.get('query_text', 'Python')),
                            student_level=data.get('student_level', 'beginner'),
                            student_id=data.get('student_id')
                        )

                        # Publish explanation response
                        await publish_explanation_response(
                            student_id=data.get('student_id'),
                            query_id=data.get('query_id'),
                            explanation=explanation
                        )

                        # Complete with success status
                        event.respond_with_succeeded()

                    except Exception as e:
                        logger.error(f"Error processing explanation request: {e}")
                        # Continue processing other events
                        event.respond_with_failed("Processing error")

        except Exception as e:
            logger.error(f"Consumer error: {e}")
            logger.info("Retrying in 5 seconds...")
            await asyncio.sleep(5)


async def generate_explanation(topic: str, student_level: str, student_id: str) -> dict:
    """
    Generate adaptive explanation using OpenAI

    Args:
        topic: Python topic to explain
        student_level: Student's experience level
        student_id: Student identifier

    Returns:
        Explanation with text, code, pitfalls, and exercises
    """

    try:
        # Craft level-appropriate prompt
        level_context = {
            "beginner": "Use simple analogies, avoid jargon, provide basic examples",
            "intermediate": "Include practical examples and common use cases",
            "advanced": "Discuss edge cases, optimizations, and alternative approaches"
        }

        prompt = f"""You are a Python programming tutor. Explain "{topic}" to a {student_level} level student.

        Guidelines: {level_context.get(student_level, "Provide clear explanation")}

        Respond with this JSON structure:
        {{
          "explanation_text": "Clear explanation in 2-3 paragraphs",
          "code_examples": ["first example", "second example"],
          "common_pitfalls": ["pitfall 1", "pitfall 2"],
          "related_topics": ["topic1", "topic2"],
          "suggested_exercises": ["exercise description 1", "exercise description 2"]
        }}
        """

        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Python programming tutor. Generate structured explanations with examples."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        explanation_data = json.loads(result)

        logger.info(f"Generated explanation for topic: {topic}")

        return explanation_data

    except Exception as e:
        logger.error(f"OpenAI error generating explanation: {e}")

        # Fallback explanation
        return {
            "explanation_text": f"Topic: {topic}. This is a fundamental Python concept. Learn it through practice.",
            "code_examples": ["# Example 1\nexample = 'code'"],
            "common_pitfalls": ["Forgetting syntax", "Not practicing enough"],
            "related_topics": ["Variables", "Functions"],
            "suggested_exercises": ["Write 5 examples", "Debug sample code"]
        }


async def publish_explanation_response(student_id: str, query_id: str, explanation: dict):
    """Publish generated explanation to Kafka via Dapr"""

    try:
        response_data = {
            "student_id": student_id,
            "query_id": query_id,
            "explanation_text": explanation.get("explanation_text", ""),
            "code_examples": explanation.get("code_examples", []),
            "common_pitfalls": explanation.get("common_pitfalls", []),
            "related_topics": explanation.get("related_topics", []),
            "suggested_exercises": explanation.get("suggested_exercises", []),
            "timestamp": datetime.utcnow().isoformat()
        }

        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/learning.response.explanation"

            response = await client.post(
                dapr_url,
                json=response_data,
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if response.status_code == 204:
                logger.info(f"Published explanation response for query {query_id}")
            else:
                logger.error(f"Failed to publish explanation: {response.status_code}")

    except Exception as e:
        logger.error(f"Error publishing explanation: {e}")


# FastAPI endpoints for health and manual testing
@app.get("/")
async def root():
    return {"message": "Concepts Service - Generates Python explanations", "version": "1.0.0"}


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "timestamp": datetime.utcnow().isoformat()}


@app.post("/generate-explanation")
async def generate_explanation_endpoint(request: ExplanationRequest):
    """Manual endpoint for testing explanations"""
    try:
        explanation = await generate_explanation(
            topic=request.topic,
            student_level=request.student_level,
            student_id=request.student_id
        )

        return {
            "student_id": request.student_id,
            "query_id": request.query_id,
            **explanation,
            "timestamp": datetime.utcnow().isoformat()
        }

    except Exception as e:
        logger.error(f"Error generating explanation: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# Startup event to begin consuming Kafka messages
@app.on_event("startup")
async def startup_event():
    """Start Kafka consumer on startup"""
    logger.info("Concepts Service starting...")
    asyncio.create_task(process_explanation_request())


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8001)
