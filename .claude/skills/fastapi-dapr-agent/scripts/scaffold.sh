#!/bin/bash
# Scaffold a new FastAPI + Dapr microservice for LearnFlow
set -e

SERVICE_NAME="${1:-new-service}"
PORT="${2:-8000}"
SERVICES_DIR="learnflow-app/services"

if [ -z "$1" ]; then
  echo "Usage: bash scripts/scaffold.sh <service-name> [port]"
  echo "Example: bash scripts/scaffold.sh quiz-service 8006"
  exit 1
fi

SERVICE_DIR="$SERVICES_DIR/$SERVICE_NAME"
mkdir -p "$SERVICE_DIR"

echo "Scaffolding $SERVICE_NAME on port $PORT..."

# Generate main.py
cat > "$SERVICE_DIR/main.py" << PYEOF
"""$SERVICE_NAME - LearnFlow AI tutoring microservice."""
import os
import json
import asyncio
import logging
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI
import httpx

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="$SERVICE_NAME")
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))

DAPR_URL = f"http://localhost:{os.getenv('DAPR_HTTP_PORT', 3500)}"
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")
INPUT_TOPIC = "change.me.input"
OUTPUT_TOPIC = "change.me.output"

SYSTEM_PROMPT = """You are a specialized AI tutor for the LearnFlow platform.
Your role: [DEFINE YOUR ROLE HERE]
Always be encouraging and pedagogically appropriate."""


class ServiceRequest(BaseModel):
    student_id: str
    query: str
    context: dict = {}


@app.get("/dapr/subscribe")
async def subscribe():
    return [{"pubsubname": PUBSUB_NAME, "topic": INPUT_TOPIC, "route": "/handle"}]


@app.post("/handle")
async def handle_event(payload: dict):
    data = payload.get("data", {})
    student_id = data.get("student_id", "unknown")
    logger.info(f"Processing event for student {student_id}")

    try:
        response = await client.chat.completions.create(
            model="gpt-4o-mini",
            messages=[
                {"role": "system", "content": SYSTEM_PROMPT},
                {"role": "user", "content": json.dumps(data)}
            ],
            temperature=0.3
        )
        result = response.choices[0].message.content

        async with httpx.AsyncClient() as http:
            await http.post(
                f"{DAPR_URL}/v1.0/publish/{PUBSUB_NAME}/{OUTPUT_TOPIC}",
                json={"student_id": student_id, "result": result},
                timeout=10.0
            )
        return {"status": "processed", "student_id": student_id}
    except Exception as e:
        logger.error(f"Error processing event: {e}")
        return {"status": "error", "detail": str(e)}


@app.post("/process")
async def process_request(req: ServiceRequest):
    """Direct endpoint for testing."""
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": req.query}
        ]
    )
    return {"result": response.choices[0].message.content, "student_id": req.student_id}


@app.get("/health")
async def health():
    return {"status": "healthy", "service": "$SERVICE_NAME", "port": $PORT}


@app.get("/")
async def root():
    return {
        "service": "$SERVICE_NAME",
        "endpoints": ["/process", "/handle", "/health", "/dapr/subscribe"]
    }
PYEOF

# Generate Dockerfile
cat > "$SERVICE_DIR/Dockerfile" << DFEOF
FROM python:3.11-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:\$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1000 appuser
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:\$PATH"
COPY main.py .
RUN chown -R appuser:appuser /app
USER appuser
EXPOSE $PORT
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD python -c "import httpx; httpx.get('http://localhost:$PORT/health')" || exit 1
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "$PORT"]
DFEOF

# Generate requirements.txt
cat > "$SERVICE_DIR/requirements.txt" << REQEOF
fastapi==0.109.0
uvicorn[standard]==0.27.0
pydantic==2.5.3
openai==1.6.1
httpx==0.26.0
python-dotenv==1.0.0
dapr==1.12.0
REQEOF

# Generate K8s manifest
mkdir -p "learnflow-app/k8s/deployments"
cat > "learnflow-app/k8s/deployments/$SERVICE_NAME.yaml" << K8SEOF
apiVersion: apps/v1
kind: Deployment
metadata:
  name: $SERVICE_NAME
  namespace: learnflow
  labels:
    app: $SERVICE_NAME
spec:
  replicas: 1
  selector:
    matchLabels:
      app: $SERVICE_NAME
  template:
    metadata:
      labels:
        app: $SERVICE_NAME
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "$SERVICE_NAME"
        dapr.io/app-port: "$PORT"
    spec:
      containers:
      - name: $SERVICE_NAME
        image: $SERVICE_NAME:latest
        imagePullPolicy: IfNotPresent
        ports:
        - containerPort: $PORT
        env:
        - name: PORT
          value: "$PORT"
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_PUBSUB_NAME
          value: "kafka-pubsub"
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        resources:
          requests:
            memory: "128Mi"
            cpu: "100m"
          limits:
            memory: "256Mi"
            cpu: "200m"
        livenessProbe:
          httpGet:
            path: /health
            port: $PORT
          initialDelaySeconds: 30
          periodSeconds: 10
        readinessProbe:
          httpGet:
            path: /health
            port: $PORT
          initialDelaySeconds: 10
          periodSeconds: 5
---
apiVersion: v1
kind: Service
metadata:
  name: $SERVICE_NAME
  namespace: learnflow
spec:
  selector:
    app: $SERVICE_NAME
  ports:
  - port: 80
    targetPort: $PORT
  type: ClusterIP
K8SEOF

echo "✓ Scaffolded $SERVICE_NAME at $SERVICE_DIR"
echo "✓ K8s manifest at learnflow-app/k8s/deployments/$SERVICE_NAME.yaml"
echo ""
echo "Next steps:"
echo "  1. Edit $SERVICE_DIR/main.py - set INPUT_TOPIC, OUTPUT_TOPIC, SYSTEM_PROMPT"
echo "  2. Run: python scripts/verify.py $SERVICE_NAME"
echo "  3. Run: bash scripts/build.sh $SERVICE_NAME"
