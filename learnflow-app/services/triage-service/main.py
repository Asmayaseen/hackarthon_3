"""
Triage Service - Routes student queries to appropriate specialized agents

Following Constitution:
- Article III: FastAPI + Dapr microservice
- Article VII: Multi-agent system architecture
- Article II: Event-driven communication via Kafka
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import Literal, Optional
import httpx
import os
import asyncio
import logging

from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Triage Service",
    description="Routes student queries to appropriate AI agents",
    version="1.0.0"
)

# Dapr configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
KNOWLEDGE_BASE_API = os.getenv("KNOWLEDGE_BASE_API", "http://localhost:8001")

# OpenAI client (supports Groq via OPENAI_BASE_URL env var)
_openai_kwargs = {"api_key": os.getenv("OPENAI_API_KEY")}
if os.getenv("OPENAI_BASE_URL"):
    _openai_kwargs["base_url"] = os.getenv("OPENAI_BASE_URL")
openai_client = AsyncOpenAI(**_openai_kwargs)
AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")


# Models
class StudentQuery(BaseModel):
    """Student query request"""
    student_id: str
    query_text: str
    current_module_id: Optional[str] = None
    student_level: Literal["beginner", "intermediate", "advanced"] = "beginner"


class QueryClassification(BaseModel):
    """Classification result"""
    classification: Literal["explain", "debug", "exercise", "review", "progress", "unclassified"]
    confidence: float
    reason: str


class RoutedQuery(BaseModel):
    """Routed query event"""
    student_id: str
    query_id: str
    query_text: str
    classification: str
    confidence: float
    student_level: str
    current_module_id: Optional[str] = None
    timestamp: str


# Helper functions
async def classify_query_with_openai(query_text: str, student_level: str) -> QueryClassification:
    """Classify student query using OpenAI"""

    try:
        response = await openai_client.chat.completions.create(
            model=AI_MODEL,
            messages=[
                {"role": "system", "content": """You are a Python programming tutor. Classify student queries into these categories:
- "explain": Student wants to understand a concept (e.g., "How do loops work?")
- "debug": Student has an error and needs help fixing it (e.g., "I got TypeError, what does it mean?")
- "exercise": Student wants practice problems (e.g., "Give me exercises on functions")
- "review": Student wants code review (e.g., "Review my code for style issues")
- "progress": Student wants to see their progress (e.g., "How am I doing?")

Respond with JSON format:
{
  "classification": "explain|debug|exercise|review|progress|unclassified",
  "confidence": 0.0-1.0,
  "reason": "brief explanation"
}"""},
                {"role": "user", "content": f"Student level: {student_level}\nQuery: {query_text}"}
            ],
            temperature=0.1,
            response_format={"type": "json_object"}
        )

        result = eval(response.choices[0].message.content)

        return QueryClassification(
            classification=result["classification"],
            confidence=float(result["confidence"]),
            reason=result["reason"]
        )

    except Exception as e:
        logger.error(f"OpenAI classification failed: {e}")
        # Default to unclassified if AI fails
        return QueryClassification(
            classification="unclassified",
            confidence=0.0,
            reason=f"Classification error: {str(e)}"
        )


def get_kafka_topic(classification: str) -> tuple[str, str]:
    """Map classification to Kafka topic and event type"""
    mapping = {
        "explain": ("learning.query.explain", "Query for Concept Explanation"),
        "debug": ("code.debug.request", "Debug Help Request"),
        "exercise": ("exercise.generate", "Exercise Generation Request"),
        "review": ("code.review.request", "Code Review Request"),
        "progress": ("progress.summary", "Progress Summary Request"),
        "unclassified": ("learning.query.unclassified", "Unclassified Query")
    }
    return mapping.get(classification, ("learning.query.unclassified", "Unclassified"))


async def publish_to_kafka(topic: str, data: dict) -> bool:
    """Publish event to Kafka via Dapr"""
    try:
        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/{topic}"

            response = await client.post(
                dapr_url,
                json=data,
                headers={"Content-Type": "application/json"}
            )

            if response.status_code == 204:
                logger.info(f"Published to {topic}")
                return True
            else:
                logger.error(f"Failed to publish to {topic}: {response.status_code}")
                return False

    except Exception as e:
        logger.error(f"Kafka publish error: {e}")
        return False


class ChatRequest(BaseModel):
    student_id: str
    message: str
    student_level: Literal["beginner", "intermediate", "advanced"] = "beginner"
    conversation_history: Optional[list] = None


class ChatResponse(BaseModel):
    reply: str
    classification: str
    confidence: float


SYSTEM_PROMPTS = {
    "explain": """You are a friendly Python tutor. Explain Python concepts clearly with:
- Simple language for beginners
- Concrete code examples
- Common mistakes to avoid
Keep responses concise (3-5 paragraphs max). Use markdown for code blocks.""",

    "debug": """You are a Python debugging expert. Help students fix errors by:
- Identifying the root cause of the error
- Explaining WHY it happened
- Giving a hint (not the full solution) first
- Then showing the fix if they're stuck
Keep responses focused and practical.""",

    "exercise": """You are a Python exercise generator. Create coding challenges that:
- Are appropriate for the student's level
- Have clear problem statements
- Include example inputs/outputs
- Build on what they're learning
Format: Problem description, then starter code template.""",

    "review": """You are a Python code reviewer. Analyze student code for:
- Correctness and logic errors
- PEP 8 style compliance
- Efficiency improvements
- Readability suggestions
Be encouraging but thorough. Rate code 1-10.""",

    "progress": """You are a learning progress coach. Based on the student's question about progress:
- Summarize their learning journey
- Highlight strengths and areas to improve
- Suggest next steps
- Be motivating and specific.""",

    "unclassified": """You are a helpful Python tutor. Answer the student's question helpfully and suggest how LearnFlow can help them learn Python better."""
}


async def generate_ai_response(message: str, classification: str, student_level: str, history: list = None) -> str:
    """Generate AI tutoring response based on classification"""
    system_prompt = SYSTEM_PROMPTS.get(classification, SYSTEM_PROMPTS["unclassified"])

    messages = [{"role": "system", "content": system_prompt}]

    if history:
        for h in history[-6:]:  # last 6 messages for context
            messages.append({"role": h.get("role", "user"), "content": h.get("content", "")})

    messages.append({"role": "user", "content": message})

    response = await openai_client.chat.completions.create(
        model=AI_MODEL,
        messages=messages,
        temperature=0.7,
        max_tokens=600
    )
    return response.choices[0].message.content


@app.post("/answer", response_model=ChatResponse)
async def answer_student_query(req: ChatRequest):
    """Classify query AND generate full AI response — used by frontend chat"""
    try:
        classification = await classify_query_with_openai(req.message, req.student_level)
        reply = await generate_ai_response(
            req.message,
            classification.classification,
            req.student_level,
            req.conversation_history or []
        )
        return ChatResponse(
            reply=reply,
            classification=classification.classification,
            confidence=classification.confidence
        )
    except Exception as e:
        logger.error(f"Answer generation failed: {e}")
        raise HTTPException(status_code=500, detail=str(e))


# API Endpoints
@app.post("/query", response_model=QueryClassification)
async def triage_student_query(query: StudentQuery):
    """
    Accept student query and route to appropriate agent

    Body:
        {
            "student_id": "student-123",
            "query_text": "How do for loops work?",
            "current_module_id": "module-2",
            "student_level": "beginner"
        }
    """
    try:
        logger.info(f"Received query from {query.student_id}: {query.query_text}")

        # Classify the query
        classification = await classify_query_with_openai(query.query_text, query.student_level)

        # Generate query ID
        import uuid
        query_id = str(uuid.uuid4())

        # Prepare routed query event
        routed_query = RoutedQuery(
            student_id=query.student_id,
            query_id=query_id,
            query_text=query.query_text,
            classification=classification.classification,
            confidence=classification.confidence,
            student_level=query.student_level,
            current_module_id=query.current_module_id,
            timestamp=str(asyncio.get_event_loop().time())
        )

        # Get target Kafka topic
        topic, event_type = get_kafka_topic(classification.classification)

        # Publish to Kafka
        publish_success = await publish_to_kafka(topic, routed_query.dict())

        if not publish_success:
            logger.warning("Failed to publish to Kafka, but returning classification")

        # Also emit routing event for analytics
        if publish_success:
            await publish_to_kafka("learning.query.routed", {
                "query_id": query_id,
                "student_id": query.student_id,
                "classification": classification.classification,
                "confidence": classification.confidence,
                "timestamp": asyncio.get_event_loop().time()
            })

        return classification

    except Exception as e:
        logger.error(f"Error processing query: {e}")
        raise HTTPException(status_code=500, detail=f"Query processing failed: {str(e)}")


@app.get("/health")
async def health_check():
    """Health check endpoint for Kubernetes"""
    # Check Dapr connectivity
    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(f"http://localhost:{DAPR_HTTP_PORT}/v1.0/health")
            if response.status_code == 204:
                return {"status": "healthy", "dapr": "connected"}
    except Exception as e:
        logger.warning(f"Dapr health check failed: {e}")
    return {"status": "healthy", "dapr": "disconnected"}


@app.get("/")
async def root():
    return {"message": "Triage Service - Routes queries to AI agents", "version": "1.0.0"}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
