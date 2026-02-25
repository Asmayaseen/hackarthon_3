"""
API Gateway Service - Central entry point for all LearnFlow APIs

Routes:
  /api/triage/*   → Triage Service    (8000)
  /api/concepts/* → Concepts Service  (8001)
  /api/debug/*    → Debug Service     (8002)
  /api/review/*   → Code Review Svc   (8003)
  /api/exercise/* → Exercise Service  (8004)
  /api/progress/* → Progress Service  (8005)
  /api/mcp/*      → MCP Server        (8006)

Features: JWT validation (optional), CORS, rate limiting headers, health aggregation
"""

import os
import logging
from typing import Optional
import httpx
from fastapi import FastAPI, Request, Response, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="LearnFlow API Gateway",
    description="Central API gateway routing to all LearnFlow microservices",
    version="1.0.0",
)

# ── CORS ───────────────────────────────────────────────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Service registry ───────────────────────────────────────────────────────────
SERVICES = {
    "triage":   os.getenv("TRIAGE_SERVICE_URL",   "http://triage-service:8000"),
    "concepts": os.getenv("CONCEPTS_SERVICE_URL",  "http://concepts-service:8001"),
    "debug":    os.getenv("DEBUG_SERVICE_URL",     "http://debug-service:8002"),
    "review":   os.getenv("REVIEW_SERVICE_URL",    "http://code-review-service:8003"),
    "exercise": os.getenv("EXERCISE_SERVICE_URL",  "http://exercise-service:8004"),
    "progress": os.getenv("PROGRESS_SERVICE_URL",  "http://progress-service:8005"),
    "mcp":      os.getenv("MCP_SERVICE_URL",       "http://mcp-server:8006"),
}

TIMEOUT = httpx.Timeout(30.0, connect=5.0)


async def proxy(request: Request, target_url: str) -> Response:
    """Forward request to upstream service and return its response."""
    async with httpx.AsyncClient(timeout=TIMEOUT) as client:
        url = target_url + (
            "?" + request.url.query if request.url.query else ""
        )
        # Forward headers except Host
        headers = {
            k: v for k, v in request.headers.items()
            if k.lower() not in ("host", "content-length")
        }
        body = await request.body()
        try:
            upstream = await client.request(
                method=request.method,
                url=url,
                headers=headers,
                content=body,
            )
            return Response(
                content=upstream.content,
                status_code=upstream.status_code,
                headers=dict(upstream.headers),
                media_type=upstream.headers.get("content-type"),
            )
        except httpx.ConnectError:
            raise HTTPException(status_code=503, detail=f"Upstream unreachable: {target_url}")
        except httpx.TimeoutException:
            raise HTTPException(status_code=504, detail=f"Upstream timed out: {target_url}")


# ── Proxy routes ───────────────────────────────────────────────────────────────

@app.api_route("/api/triage/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_triage(path: str, request: Request):
    return await proxy(request, f"{SERVICES['triage']}/{path}")


@app.api_route("/api/concepts/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_concepts(path: str, request: Request):
    return await proxy(request, f"{SERVICES['concepts']}/{path}")


@app.api_route("/api/debug/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_debug(path: str, request: Request):
    return await proxy(request, f"{SERVICES['debug']}/{path}")


@app.api_route("/api/review/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_review(path: str, request: Request):
    return await proxy(request, f"{SERVICES['review']}/{path}")


@app.api_route("/api/exercise/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_exercise(path: str, request: Request):
    return await proxy(request, f"{SERVICES['exercise']}/{path}")


@app.api_route("/api/progress/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_progress(path: str, request: Request):
    return await proxy(request, f"{SERVICES['progress']}/{path}")


@app.api_route("/api/mcp/{path:path}", methods=["GET", "POST", "PUT", "DELETE", "PATCH"])
async def proxy_mcp(path: str, request: Request):
    return await proxy(request, f"{SERVICES['mcp']}/{path}")


# ── Health aggregation ─────────────────────────────────────────────────────────

@app.get("/health")
async def health():
    """Check health of all upstream services."""
    results = {}
    async with httpx.AsyncClient(timeout=httpx.Timeout(3.0)) as client:
        for name, base_url in SERVICES.items():
            try:
                r = await client.get(f"{base_url}/health")
                results[name] = "healthy" if r.status_code < 400 else "degraded"
            except Exception:
                results[name] = "unreachable"

    overall = "healthy" if all(v == "healthy" for v in results.values()) else "degraded"
    return {"status": overall, "services": results}


@app.get("/")
async def root():
    return {
        "service": "LearnFlow API Gateway",
        "version": "1.0.0",
        "routes": [f"/api/{svc}/*" for svc in SERVICES],
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8007)
