"""
Mock Triage Service for Hackathon 3
Simple FastAPI server that returns hardcoded JSON
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional, Literal
import uvicorn

app = FastAPI(title="Mock Triage Service", version="1.0.0")

class QueryClassification(BaseModel):
    classification: Literal["explain", "debug", "exercise", "review", "progress", "unclassified"]
    confidence: float
    reason: str

class StudentQuery(BaseModel):
    student_id: str
    query_text: str
    current_module_id: Optional[str] = None
    student_level: Literal["beginner", "intermediate", "advanced"] = "beginner"

@app.post("/query")
async def triage_student_query(query: StudentQuery):
    """Mock classification endpoint"""
    return QueryClassification(
        classification="explain",
        confidence=0.95,
        reason="Mock: Query classified as 'explain' for testing"
    )

@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "mock-triage"}

@app.get("/")
async def root():
    return {"message": "Mock Triage Service - Returns hardcoded responses", "version": "1.0.0"}

@app.get("/docs")
async def get_docs():
    return {"docs": "Mock API documentation", "endpoints": ["/query", "/health", "/"]}

if __name__ == "__main__":
    print("Starting Mock Triage Service on http://localhost:8000")
    print("API Documentation: http://localhost:8000/docs")
    uvicorn.run(app, host="0.0.0.0", port=8000)