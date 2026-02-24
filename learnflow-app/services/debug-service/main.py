"""
Debug Service - Parses Python errors and provides progressive hints

Following Constitution Article VII, Section 7.01:
- Input: Error message + code
- Logic: Identify root cause, provide progressive hints
- Output: Hint (not solution) + explanation

Progressive hints: 3 levels of hints, each more revealing than previous
"""

import asyncio
import json
import logging
import os
import re
import sys
import traceback
from datetime import datetime
from typing import List, Optional, Dict

import httpx
from dapr.clients import DaprClient
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from openai import AsyncOpenAI

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# FastAPI app
app = FastAPI(
    title="Debug Service",
    description="Provides progressive hints for Python errors without revealing full solution",
    version="1.0.0"
)

# Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

# OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Data Models
class DebugRequest(BaseModel):
    """Request for debugging help"""
    student_id: str
    error_message: str
    code_snippet: str
    error_type: Optional[str] = None
    traceback: Optional[str] = None
    student_level: str = "beginner"


class HintLevel(BaseModel):
    """A progressive hint level"""
    level: int  # 1, 2, or 3
    hint: str  # The hint text (progressively more revealing)
    explanation: str  # Why this is the issue
    concepts_to_review: List[str]  # Related concepts to study


class DebugResponse(BaseModel):
    """Debug response with progressive hints"""
    student_id: str
    request_id: str
    error_type: str
    root_cause: str
    hints: List[HintLevel]
    next_steps: List[str]
    timestamp: str


class CodeSubmission(BaseModel):
    """Code submission for review"""
    student_id: str
    code: str
    language: str = "python"
    problem_description: Optional[str] = None


# Error pattern matching for common Python errors
COMMON_ERRORS = {
    "NameError": r"name '(.+)' is not defined",
    "SyntaxError": r"invalid syntax",
    "TypeError": r"unsupported operand type",
    "IndentationError": r"unexpected indent",
    "AttributeError": r"'(.+)' object has no attribute '(.+)'",
    "IndexError": r"list index out of range",
    "KeyError": r"(.+)",
    "ValueError": r"invalid literal for int",
    "ImportError": r"No module named",
    "ZeroDivisionError": r"division by zero"
}


def extract_error_type(error_message: str) -> str:
    """Extract error type from error message"""
    for error_type in COMMON_ERRORS.keys():
        if error_type.lower() in error_message.lower():
            return error_type
    return "UnknownError"


def extract_line_from_traceback(tb: Optional[str]) -> Optional[int]:
    """Extract line number from traceback if available"""
    if not tb:
        return None

    # Look for line number in traceback
    # Typical format: File "filename.py", line 42, in function
    import re
    match = re.search(r'line (\d+)', tb)
    if match:
        return int(match.group(1))
    return None


async def generate_progressive_hints(
    error_type: str,
    error_message: str,
    code_snippet: str,
    traceback_str: Optional[str],
    student_level: str
) -> List[HintLevel]:
    """
    Generate 3 progressive hints using OpenAI

    Progressive hints start very general and get more specific:
    - Level 1: General direction (e.g., "Check your variable names")
    - Level 2: More specific (e.g., "The variable 'x' is used but not defined")
    - Level 3: Specific location (e.g., "On line 5, you reference 'x' before assigning it")

    This prevents giving away the solution while helping students learn debugging.
    """

    try:
        line_num = extract_line_from_traceback(traceback_str)
        line_info = f" at line {line_num}" if line_num else ""

        prompt = f"""You are a Python tutor helping a {student_level} student debug an error.

Error Type: {error_type}
Error Message: {error_message}
Code Snippet:
```python
{code_snippet}
```

Generate 3 progressive hints from general to specific.

Level 1 (General): Point them in the right direction without revealing specifics.
Level 2 (More Specific): Give more detail about the nature of the problem.
Level 3 (Specific): Tell them exactly where and what the issue is.

Respond with JSON:
{{
  "hints": [
    {{
      "level": 1,
      "hint": "string",
      "explanation": "why this matters",
      "concepts_to_review": ["concept1", "concept2"]
    }},
    {{
      "level": 2,
      "hint": "string",
      "explanation": "why this matters",
      "concepts_to_review": ["concept1", "concept2"]
    }},
    {{
      "level": 3,
      "hint": "string",
      "explanation": "why this matters",
      "concepts_to_review": ["concept1", "concept2"]
    }}
  ]
}}
"""

        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Python debugging tutor. Generate progressive hints."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        data = json.loads(result)

        hints = []
        for hint_data in data.get("hints", []):
            hints.append(HintLevel(
                level=hint_data["level"],
                hint=hint_data["hint"],
                explanation=hint_data["explanation"],
                concepts_to_review=hint_data.get("concepts_to_review", [])
            ))

        logger.info(f"Generated {len(hints)} progressive hints for {error_type}")
        return hints

    except Exception as e:
        logger.error(f"OpenAI error generating hints: {e}")

        # Fallback hints
        return [
            HintLevel(
                level=1,
                hint=f"There seems to be an issue with your code. Look carefully at the error message and see if you can identify what Python is telling you.",
                explanation="Understanding error messages is a key debugging skill",
                concepts_to_review=["Reading error messages", "Tracebacks"]
            ),
            HintLevel(
                level=2,
                hint=f"The error type is {error_type}. This usually means {get_error_meaning(error_type)}",
                explanation="Different error types indicate different kinds of problems",
                concepts_to_review=[error_type, "Python error types"]
            ),
            HintLevel(
                level=3,
                hint=f"Check your code around line {line_num or 'where the error occurred'}. The issue is likely related to {error_message.lower()}",
                explanation="Locating the exact line helps focus your debugging",
                concepts_to_review=["Debugging strategies", error_type]
            )
        ]


def get_error_meaning(error_type: str) -> str:
    """Get human-readable meaning of error type"""
    meanings = {
        "NameError": "you're trying to use a variable that hasn't been defined yet",
        "TypeError": "you're trying to perform an operation on incompatible types",
        "SyntaxError": "you have invalid Python syntax (typos, missing punctuation)",
        "IndentationError": "your indentation is inconsistent",
        "AttributeError": "you're trying to access an attribute that doesn't exist",
        "IndexError": "you're trying to access an index that doesn't exist",
        "KeyError": "you're trying to access a dictionary key that doesn't exist",
        "ValueError": "you're trying to convert or use a value inappropriately",
        "ImportError": "Python can't find the module you're trying to import",
        "ZeroDivisionError": "you're trying to divide by zero"
    }
    return meanings.get(error_type, "there's a problem with this type of error")


async def publish_debug_response(response: DebugResponse) -> bool:
    """Publish debug response to Kafka via Dapr"""
    try:
        response_data = {
            "student_id": response.student_id,
            "request_id": response.request_id,
            "error_type": response.error_type,
            "root_cause": response.root_cause,
            "hints": [h.dict() for h in response.hints],
            "next_steps": response.next_steps,
            "timestamp": response.timestamp
        }

        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/code.debug.response"

            resp = await client.post(
                dapr_url,
                json=response_data,
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if resp.status_code == 204:
                logger.info(f"Published debug response for request {response.request_id}")
                return True
            else:
                logger.error(f"Failed to publish debug response: {resp.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing debug response: {e}")
        return False


# HTTP Endpoints
@app.post("/debug", response_model=DebugResponse)
async def debug_error(request: DebugRequest):
    """
    Debug a Python error and return progressive hints
    """
    try:
        logger.info(f"Debug request from {request.student_id}: {request.error_message[:50]}...")

        # Extract error type if not provided
        error_type = request.error_type or extract_error_type(request.error_message)
        line_num = extract_line_from_traceback(request.traceback)

        # Generate progressive hints
        hints = await generate_progressive_hints(
            error_type=error_type,
            error_message=request.error_message,
            code_snippet=request.code_snippet,
            traceback_str=request.traceback,
            student_level=request.student_level
        )

        import uuid
        request_id = str(uuid.uuid4())

        # Create response
        response = DebugResponse(
            student_id=request.student_id,
            request_id=request_id,
            error_type=error_type,
            root_cause=f"{error_type} occurred{ ' at line ' + str(line_num) if line_num else ''}: {request.error_message}",
            hints=hints,
            next_steps=[
                "Read the hints starting from Level 1",
                "Try to fix the error based on the hint",
                "If stuck, review the concepts mentioned",
                "Attempt Level 2 hint if Level 1 wasn't enough",
                "Use Level 3 hint as a final guide before checking solution"
            ],
            timestamp=datetime.utcnow().isoformat()
        )

        # Publish to Kafka for tracking
        await publish_debug_response(response)

        return response

    except Exception as e:
        logger.error(f"Debug processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "debug-service",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    return {
        "message": "Debug Service - Progressive hints for Python errors",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8002)
