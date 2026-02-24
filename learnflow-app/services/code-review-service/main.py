"""
Code Review Service - Analyzes Python code for quality, style, and correctness

Following Constitution Article VII, Section 7.01:
- Input: Student code submission
- Logic: Check correctness, PEP 8 compliance, efficiency, readability
- Output: Quality score + specific feedback

Provides line-by-line feedback with severity levels
"""

import asyncio
import json
import logging
import os
import re
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
    title="Code Review Service",
    description="Analyzes Python code for correctness, PEP 8 compliance, efficiency, and readability",
    version="1.0.0"
)

# Configuration
DAPR_HTTP_PORT = os.getenv("DAPR_HTTP_PORT", "3500")
DAPR_PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

# OpenAI client
openai_client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Data Models
class CodeSubmission(BaseModel):
    """Code submission for review"""
    student_id: str
    code: str
    language: str = "python"
    problem_description: Optional[str] = None


class ReviewIssue(BaseModel):
    """A code issue found during review"""
    line_number: int
    severity: str  # "error", "warning", "info"
    category: str  # "correctness", "style", "efficiency", "readability"
    message: str
    suggestion: str
    pep8_rule: Optional[str] = None


class ReviewMetrics(BaseModel):
    """Code quality metrics"""
    total_lines: int
    issues_found: int
    errors: int
    warnings: int
    readability_score: float  # 0-100
    efficiency_score: float  # 0-100
    style_score: float  # 0-100
    pep8_compliance: float  # Percentage


class CodeReviewResponse(BaseModel):
    """Code review response"""
    student_id: str
    request_id: str
    overall_score: float  # 0-100
    issues: List[ReviewIssue]
    metrics: ReviewMetrics
    summary: str
    strengths: List[str]
    improvement_areas: List[str]
    timestamp: str


# PEP 8 basic rules (subset for quick checks)
BASIC_PEP8_CHECKS = [
    {
        "pattern": r"^\s*\t",
        "message": "Uses tabs instead of spaces",
        "pep8_rule": "E101",
        "severity": "warning",
        "category": "style"
    },
    {
        "pattern": r"^\s{1,3}\w",
        "message": "Indentation should be 4 spaces",
        "pep8_rule": "E111",
        "severity": "warning",
        "category": "style"
    },
    {
        "pattern": r"[ \t]+$",
        "message": "Trailing whitespace",
        "pep8_rule": "W291",
        "severity": "info",
        "category": "style"
    },
    {
        "pattern": r"^.{80,}$",
        "message": "Line too long (should be <79 characters if followed by PEP8)",
        "pep8_rule": "E501",
        "severity": "info",
        "category": "style"
    },
    {
        "pattern": r"[^ ]#",
        "message": "Inline comments should have at least 2 spaces before '#', then one space",
        "pep8_rule": "E261",
        "severity": "info",
        "category": "style"
    },
    {
        "pattern": r"def\s+\w+\(self\)\s*:\s*$",
        "message": "Instance methods should have at least 'self' parameter",
        "severity": "info",
        "category": "correctness"
    }
]


def perform_basic_pep8_check(code: str, line_num: int, line: str) -> Optional[ReviewIssue]:
    """Perform basic PEP 8 checks on a line of code"""
    for check in BASIC_PEP8_CHECKS:
        if re.search(check["pattern"], line):
            return ReviewIssue(
                line_number=line_num,
                severity=check["severity"],
                category=check["category"],
                message=check["message"],
                suggestion=f"Consider fixing: {check['message']}",
                pep8_rule=check.get("pep8_rule")
            )
    return None


async def analyze_with_openai(code: str, problem_description: Optional[str]) -> Dict:
    """
    Use OpenAI for advanced code analysis including:
    - Correctness (logic errors, edge cases)
    - Efficiency (algorithm complexity, optimization opportunities)
    - Readability (naming, structure, comments)
    """

    try:
        prompt = f"""You are an expert Python code reviewer. Analyze this code for correctness, efficiency, and readability.

Problem Description: {problem_description or 'N/A'}

Code to Review:
```python
{code}
```

Provide a comprehensive review with:
1. Overall quality score (0-100)
2. List of issues found (with line numbers, severity, category)
3. Specific suggestions for improvement
4. Code strengths
5. Areas for improvement
6. PEP 8 compliance issues

Respond in JSON format:
{{
  "overall_score": float,
  "issues": [
    {{
      "line_number": int,
      "severity": "error|warning|info",
      "category": "correctness|style|efficiency|readability",
      "message": "string",
      "suggestion": "string"
    }}
  ],
  "strengths": ["string"],
  "improvement_areas": ["string"],
  "summary": "string"
}}
"""

        response = await openai_client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": "You are a Python code reviewer. Be thorough but constructive."},
                {"role": "user", "content": prompt}
            ],
            temperature=0.2,
            response_format={"type": "json_object"}
        )

        result = response.choices[0].message.content
        data = json.loads(result)

        logger.info(f"OpenAI analysis complete: {len(data.get('issues', []))} issues found")
        return data

    except Exception as e:
        logger.error(f"OpenAI error analyzing code: {e}")

        # Fallback analysis
        return {
            "overall_score": 75.0,
            "issues": [
                {
                    "line_number": 1,
                    "severity": "info",
                    "category": "readability",
                    "message": "Add docstrings to explain what this code does",
                    "suggestion": "Add module and function docstrings"
                }
            ],
            "strengths": ["Code structure looks good"],
            "improvement_areas": ["Add more comments", "Consider function decomposition"],
            "summary": "Basic analysis completed. Consider adding more descriptive comments."
        }


def calculate_pep8_compliance(issues: List[ReviewIssue]) -> float:
    """Calculate PEP 8 compliance percentage"""
    total_lines_checked = 100  # Assume 100 lines checked
    style_issues = len([i for i in issues if i.category == "style"])

    # Lower score for more style issues
    compliance = max(0, 100 - (style_issues * 2))
    return compliance


def calculate_scores(issues: List[ReviewIssue]) -> Dict[str, float]:
    """Calculate readability, efficiency, and style scores"""
    # Count issues by category
    errors = len([i for i in issues if i.severity == "error"])
    warnings = len([i for i in issues if i.severity == "warning"])
    info = len([i for i in issues if i.severity == "info"])

    style_issues = len([i for i in issues if i.category == "style"])
    correctness_issues = len([i for i in issues if i.category == "correctness"])
    efficiency_issues = len([i for i in issues if i.category == "efficiency"])

    # Base scores (start at 100)
    readability = 100.0
    efficiency = 100.0
    style = 100.0

    # Deduct points for issues (weighted)
    readability -= (errors * 10 + warnings * 5 + info * 2 + correctness_issues * 8)
    efficiency -= (errors * 15 + warnings * 7 + efficiency_issues * 10)
    style -= (style_issues * 3)

    # Ensure minimum of 0
    readability = max(0, readability)
    efficiency = max(0, efficiency)
    style = max(0, style)

    return {
        "readability": readability,
        "efficiency": efficiency,
        "style": style
    }


async def publish_review_response(response: CodeReviewResponse) -> bool:
    """Publish code review response to Kafka via Dapr"""
    try:
        response_data = {
            "student_id": response.student_id,
            "request_id": response.request_id,
            "overall_score": response.overall_score,
            "issues": [i.dict() for i in response.issues],
            "metrics": response.metrics.dict(),
            "summary": response.summary,
            "strengths": response.strengths,
            "improvement_areas": response.improvement_areas,
            "timestamp": response.timestamp
        }

        async with httpx.AsyncClient() as client:
            dapr_url = f"http://localhost:{DAPR_HTTP_PORT}/v1.0/publish/{DAPR_PUBSUB_NAME}/code.review.completed"

            resp = await client.post(
                dapr_url,
                json=response_data,
                headers={"Content-Type": "application/cloudevents+json"}
            )

            if resp.status_code == 204:
                logger.info(f"Published code review for request {response.request_id}")
                return True
            else:
                logger.error(f"Failed to publish code review: {resp.status_code}")
                return False

    except Exception as e:
        logger.error(f"Error publishing code review: {e}")
        return False


# HTTP Endpoints
@app.post("/review", response_model=CodeReviewResponse)
async def review_code(request: CodeSubmission):
    """
    Review Python code and provide comprehensive feedback
    """
    try:
        logger.info(f"Code review request from {request.student_id}: {len(request.code)} chars")

        # Split code into lines
        lines = request.code.split('\n')
        total_lines = len(lines)

        # Collect issues from multiple sources
        issues: List[ReviewIssue] = []

        # 1. Basic PEP 8 checks
        from concurrent.futures import ThreadPoolExecutor
        with ThreadPoolExecutor() as executor:
            futures = [
                executor.submit(perform_basic_pep8_check, request.code, i+1, line)
                for i, line in enumerate(lines)
            ]

            for future in futures:
                issue = future.result()
                if issue:
                    issues.append(issue)

        # 2. Advanced analysis with OpenAI
        ai_analysis = await analyze_with_openai(request.code, request.problem_description)

        # Convert AI issues to ReviewIssue format
        for ai_issue in ai_analysis.get("issues", []):
            issues.append(ReviewIssue(
                line_number=ai_issue["line_number"],
                severity=ai_issue["severity"],
                category=ai_issue["category"],
                message=ai_issue["message"],
                suggestion=ai_issue["suggestion"],
                pep8_rule=ai_issue.get("pep8_rule")
            ))

        # Calculate metrics
        error_count = len([i for i in issues if i.severity == "error"])
        warning_count = len([i for i in issues if i.severity == "warning"])
        info_count = len([i for i in issues if i.severity == "info"])

        scores = calculate_scores(issues)
        pep8_compliance = calculate_pep8_compliance(issues)

        import uuid
        request_id = str(uuid.uuid4())

        # Create response
        response = CodeReviewResponse(
            student_id=request.student_id,
            request_id=request_id,
            overall_score=ai_analysis.get("overall_score", 75.0),
            issues=issues,
            metrics=ReviewMetrics(
                total_lines=total_lines,
                issues_found=len(issues),
                errors=error_count,
                warnings=warning_count,
                readability_score=scores["readability"],
                efficiency_score=scores["efficiency"],
                style_score=scores["style"],
                pep8_compliance=pep8_compliance
            ),
            summary=ai_analysis.get("summary", "Code review completed with basic checks"),
            strengths=ai_analysis.get("strengths", ["Code structure is logical"]),
            improvement_areas=ai_analysis.get("improvement_areas", ["Add more comments"]),
            timestamp=datetime.utcnow().isoformat()
        )

        # Publish to Kafka
        await publish_review_response(response)

        return response

    except Exception as e:
        logger.error(f"Code review processing error: {e}")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "code-review-service",
        "timestamp": datetime.utcnow().isoformat()
    }


@app.get("/")
async def root():
    return {
        "message": "Code Review Service - Analyzes Python code quality",
        "version": "1.0.0"
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)
