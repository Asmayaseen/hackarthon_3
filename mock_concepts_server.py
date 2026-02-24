"""
Mock Concepts Service for Hackathon 3
Simple FastAPI server that returns hardcoded explanations
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Literal
import uvicorn
from datetime import datetime

app = FastAPI(title="Mock Concepts Service", version="1.0.0")

class ExplanationRequest(BaseModel):
    student_id: str
    query_id: str
    topic: str
    student_level: Literal["beginner", "intermediate", "advanced"]

class ExplanationResponse(BaseModel):
    student_id: str
    query_id: str
    explanation_text: str
    code_examples: List[str]
    common_pitfalls: List[str]
    related_topics: List[str]
    suggested_exercises: List[str]
    timestamp: str

@app.post("/generate-explanation")
async def generate_explanation_endpoint(request: ExplanationRequest):
    """Mock explanation endpoint"""
    return ExplanationResponse(
        student_id=request.student_id,
        query_id=request.query_id,
        explanation_text=f"Mock explanation for '{request.topic}' at {request.student_level} level",
        code_examples=[
            f"# Example 1: Basic {request.topic} usage",
            f"# Example 2: Advanced {request.topic} technique"
        ],
        common_pitfalls=[
            f"Forgetting semicolon in {request.topic} syntax",
            f"Misunderstanding {request.topic} scope"
        ],
        related_topics=["Variables", "Functions", "Control Flow"],
        suggested_exercises=[
            f"Write 3 examples of {request.topic}",
            f"Debug a {request.topic} code snippet"
        ],
        timestamp=datetime.utcnow().isoformat()
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mock-concepts", "timestamp": datetime.utcnow().isoformat()}

@app.get("/")
async def root():
    return {"message": "Mock Concepts Service - Returns hardcoded explanations", "version": "1.0.0"}

@app.get("/docs")
async def get_docs():
    return {"docs": "Mock API documentation", "endpoints": ["/generate-explanation", "/health", "/"]}

if __name__ == "__main__":
    print("Starting Mock Concepts Service on http://localhost:8001")
    print("API Documentation: http://localhost:8001/docs")
    uvicorn.run(app, host="0.0.0.0", port=8001)