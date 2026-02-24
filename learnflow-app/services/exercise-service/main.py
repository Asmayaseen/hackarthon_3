"""
Exercise Service - Generates Python coding challenges and auto-grades submissions

Following Constitution Article VII, Section 7.01:
- Input: Exercise generation request or code submission for grading
- Logic: Generate challenges based on topic/difficulty, auto-grade with test cases
- Output: Generated exercise or grading results with feedback

Provides progressive difficulty and topic-based exercise generation.
"""

import asyncio
import json
import logging
import os
import sys
from datetime import datetime
from typing import List, Optional, Dict, Any
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
    title="Exercise Service",
    description="Generates Python exercises and auto-grades submissions",
    version="1.0.0"
)

# Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

# OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Data Models
class ExerciseRequest(BaseModel):
    """Request to generate a new exercise"""
    student_id: str
    difficulty: str  # "easy", "medium", "hard"
    topic: str  # "loops", "functions", "classes", "lists", "dictionaries", "recursion"
    request_id: Optional[str] = None


class Exercise(BaseModel):
    """Generated exercise"""
    exercise_id: str
    title: str
    description: str
    difficulty: str
    topic: str
    starter_code: Optional[str] = None
    test_cases: List[Dict[str, Any]]
    hints: List[str]
    solution: Optional[str] = None


class CodeSubmission(BaseModel):
    """Student code submission for grading"""
    student_id: str
    exercise_id: str
    code: str
    language: str = "python"


class TestResult(BaseModel):
    """Result of running a single test case"""
    test_id: str
    passed: bool
    expected_output: str
    actual_output: str
    error_message: Optional[str] = None


class GradingResult(BaseModel):
    """Complete grading results"""
    student_id: str
    exercise_id: str
    request_id: str
    score: float  # 0-100
    total_tests: int
    passed_tests: int
    test_results: List[TestResult]
    feedback: str
    passed: bool  # True if score >= 70
    timestamp: str


# Exercise templates by topic and difficulty
EXERCISE_TEMPLATES = {
    "loops": {
        "easy": {
            "title": "Sum Numbers with Loop",
            "description": "Write a function that sums all numbers from 1 to n using a loop.",
            "starter_code": "def sum_to_n(n):\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "sum_to_n(5)", "expected": 15},
                {"input": "sum_to_n(10)", "expected": 55},
                {"input": "sum_to_n(1)", "expected": 1}
            ],
            "hints": [
                "Use a for loop to iterate from 1 to n",
                "Initialize a variable to 0 before the loop",
                "Add each number to the variable inside the loop"
            ]
        },
        "medium": {
            "title": "Find Prime Numbers",
            "description": "Write a function that returns all prime numbers up to n.",
            "starter_code": "def find_primes(n):\n    # Your code here\n    pass",
            "test_cases": [
                {"input": "find_primes(10)", "expected": [2, 3, 5, 7]},
                {"input": "find_primes(20)", "expected": [2, 3, 5, 7, 11, 13, 17, 19]}
            ],
            "hints": [
                "A prime number is only divisible by 1 and itself",
                "Use a helper function to check if a number is prime",
                "Loop through numbers from 2 to n"
            ]
        }
    },
    "functions": {
        "easy": {
            "title": "Calculate Factorial",
            "description": "Write a recursive function to calculate factorial of n.",
            "starter_code": "def factorial(n):\n    # Your code here - use recursion\n    pass",
            "test_cases": [
                {"input": "factorial(5)", "expected": 120},
                {"input": "factorial(0)", "expected": 1},
                {"input": "factorial(3)", "expected": 6}
            ],
            "hints": [
                "Base case: factorial(0) = 1",
                "Recursive case: n * factorial(n-1)",
                "Make sure to handle n = 0"
            ]
        }
    },
    "classes": {
        "easy": {
            "title": "Bank Account Class",
            "description": "Create a BankAccount class with deposit and withdraw methods.",
            "starter_code": "class BankAccount:\n    def __init__(self, balance=0):\n        self.balance = balance\n\n    # Add methods here\n    pass",
            "test_cases": [
                {"input": "acc = BankAccount(100); acc.deposit(50); acc.balance", "expected": 150},
                {"input": "acc = BankAccount(100); acc.withdraw(30); acc.balance", "expected": 70}
            ],
            "hints": [
                "Define deposit method that adds to balance",
                "Define withdraw method that subtracts from balance",
                "Return the new balance after each operation"
            ]
        }
    }
}


async def generate_with_openai(topic: str, difficulty: str) -> Exercise:
    """Generate exercise using OpenAI"""
    try:
        prompt = f"""Generate a Python programming exercise about {topic} with {difficulty} difficulty.

Create:
1. A clear title
2. Description of what the student should implement
3. Starter code (optional)
4. 3 test cases with inputs and expected outputs
5. 3 progressive hints (from general to specific)
6. A solution

Respond in JSON format:
{{
  "title": "Exercise title",
  "description": "Exercise description",
  "starter_code": "def function():\n    pass",  // optional
  "test_cases": [
    {{
      "input": "function(arg)",
      "expected": "result"
    }}
  ],
  "hints": ["hint1", "hint2", "hint3"],
  "solution": "complete solution code"
}}
"""

        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a programming exercise generator. Create educational Python exercises."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.3,
            response_format={"type": "json_object"}
        )

        result = json.loads(response.choices[0].message.content)
        import uuid

        return Exercise(
            exercise_id=str(uuid.uuid4()),
            title=result["title"],
            description=result["description"],
            difficulty=difficulty,
            topic=topic,
            starter_code=result.get("starter_code"),
            test_cases=result["test_cases"],
            hints=result["hints"],
            solution=result["solution"]
        )

    except Exception as e:
        logger.error(f"OpenAI error generating exercise: {e}")

        # Fallback to template
        template = EXERCISE_TEMPLATES.get(topic, {}).get(difficulty)
        if template:
            import uuid
            return Exercise(
                exercise_id=str(uuid.uuid4()),
                title=template["title"],
                description=template["description"],
                difficulty=difficulty,
                topic=topic,
                starter_code=template.get("starter_code"),
                test_cases=template["test_cases"],
                hints=template["hints"]
            )

        raise HTTPException(status_code=500, detail="Failed to generate exercise")


def run_test_case(code: str, test_input: str, expected_output: Any) -> TestResult:
    """Run a single test case"""
    import uuid
    test_id = str(uuid.uuid4())

    try:
        # Create a safe execution environment
        exec_globals = {}
        exec(code, exec_globals)

        # Execute the test input
        result = eval(test_input, exec_globals)

        # Compare with expected output
        passed = result == expected_output

        return TestResult(
            test_id=test_id,
            passed=passed,
            expected_output=str(expected_output),
            actual_output=str(result),
            error_message=None
        )

    except Exception as e:
        return TestResult(
            test_id=test_id,
            passed=False,
            expected_output=str(expected_output),
            actual_output="",
            error_message=str(e)
        )


async def grade_submission(submission: CodeSubmission, exercise: Exercise, request_id: str) -> GradingResult:
    """Grade a code submission against test cases"""
    try:
        # Run all test cases
        test_results = []
        for test_case in exercise.test_cases:
            result = run_test_case(submission.code, test_case["input"], test_case["expected"])
            test_results.append(result)

        # Calculate score
        total_tests = len(test_results)
        passed_tests = len([r for r in test_results if r.passed])
        score = (passed_tests / total_tests * 100) if total_tests > 0 else 0

        # Generate feedback
        if score == 100:
            feedback = "Excellent! All tests passed."
        elif score >= 70:
            feedback = f"Good work! You passed {passed_tests} out of {total_tests} tests."
        else:
            feedback = f"Keep trying! You passed {passed_tests} out of {total_tests} tests. Check the failed tests and try again."

        return GradingResult(
            student_id=submission.student_id,
            exercise_id=submission.exercise_id,
            request_id=request_id,
            score=score,
            total_tests=total_tests,
            passed_tests=passed_tests,
            test_results=test_results,
            feedback=feedback,
            passed=score >= 70,
            timestamp=datetime.utcnow().isoformat()
        )

    except Exception as e:
        logger.error(f"Error grading submission: {e}")
        raise HTTPException(status_code=500, detail=f"Grading failed: {str(e)}")


async def publish_exercise_generated(exercise: Exercise, student_id: str, request_id: str):
    """Publish exercise generated event"""
    try:
        event_data = {
            "student_id": student_id,
            "exercise_id": exercise.exercise_id,
            "request_id": request_id,
            "title": exercise.title,
            "difficulty": exercise.difficulty,
            "topic": exercise.topic,
            "timestamp": datetime.utcnow().isoformat()
        }

        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/exercise.generated"

            resp = await client.post(
                dapr_url,
                json=event_data,
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if resp.status_code == 204:
                logger.info(f"Published exercise generation event: {exercise.exercise_id}")
                return True
            else:
                logger.error(f"Failed to publish exercise event: {resp.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing exercise event: {e}")
        return False


async def publish_grading_result(result: GradingResult):
    """Publish grading result event"""
    try:
        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/exercise.graded"

            resp = await client.post(
                dapr_url,
                json=result.dict(),
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if resp.status_code == 204:
                logger.info(f"Published grading result for: {result.student_id}")
                return True
            else:
                logger.error(f"Failed to publish grading result: {resp.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing grading result: {e}")
        return False


# HTTP Endpoints
@app.post("/generate-exercise", response_model=Exercise)
async def generate_exercise(request: ExerciseRequest):
    """
    Generate a new programming exercise based on topic and difficulty
    """
    try:
        logger.info(f"Generating {request.difficulty} exercise for topic: {request.topic}")

        import uuid
        request_id = request.request_id or str(uuid.uuid4())

        # Generate exercise
        exercise = await generate_with_openai(request.topic, request.difficulty)

        # Publish event
        await publish_exercise_generated(exercise, request.student_id, request_id)

        logger.info(f"Generated exercise: {exercise.title}")
        return exercise

    except Exception as e:
        logger.error(f"Exercise generation error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/grade-submission", response_model=GradingResult)
async def grade_submission_endpoint(submission: CodeSubmission):
    """
    Grade a student's code submission
    """
    try:
        logger.info(f"Grading submission from student: {submission.student_id}")

        # Note: In production, fetch exercise from database/state store
        # For now, we'll use a placeholder exercise
        import uuid
        request_id = str(uuid.uuid4())

        # Create a sample exercise for grading (in production, fetch from DB)
        exercise = Exercise(
            exercise_id=submission.exercise_id,
            title="Sample Exercise",
            description="Sample exercise for grading",
            difficulty="easy",
            topic="functions",
            test_cases=[
                {"input": "sample_func()", "expected": "sample_output"}
            ],
            hints=[]
        )

        # Grade submission
        result = await grade_submission(submission, exercise, request_id)

        # Publish result
        await publish_grading_result(result)

        logger.info(f"Graded submission: {result.score}%")
        return result

    except Exception as e:
        logger.error(f"Grading error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/topics")
async def get_topics():
    """Get available exercise topics"""
    return {
        "topics": ["loops", "functions", "classes", "lists", "dictionaries", "recursion"],
        "difficulties": ["easy", "medium", "hard"]
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "exercise-service",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    return {
        "message": "Exercise Service - Generates Python challenges and auto-grades submissions",
        "version": "1.0.0",
        "endpoints": [
            "POST /generate-exercise",
            "POST /grade-submission",
            "GET /topics",
            "GET /health"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8004)
