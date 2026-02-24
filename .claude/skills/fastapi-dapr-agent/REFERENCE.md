# FastAPI + Dapr Agent Reference

## Service Architecture
Each LearnFlow microservice follows this pattern:
```
Student Request → Triage (classifies) → Kafka Topic → Service (subscribes) → OpenAI → Response Topic
```

## FastAPI Service Template
```python
from fastapi import FastAPI
from pydantic import BaseModel
from openai import AsyncOpenAI
import httpx, os, json, asyncio

app = FastAPI(title="<Service> Service")
client = AsyncOpenAI(api_key=os.getenv("OPENAI_API_KEY"))
DAPR_URL = f"http://localhost:{os.getenv('DAPR_HTTP_PORT', 3500)}"
PUBSUB_NAME = os.getenv("DAPR_PUBSUB_NAME", "kafka-pubsub")

# Dapr subscription config
@app.get("/dapr/subscribe")
async def subscribe():
    return [{"pubsubname": PUBSUB_NAME, "topic": "your.input.topic", "route": "/handle"}]

# Event handler
@app.post("/handle")
async def handle_event(payload: dict):
    data = payload.get("data", {})
    # Process with OpenAI
    response = await client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "system", "content": SYSTEM_PROMPT},
                  {"role": "user", "content": json.dumps(data)}]
    )
    result = response.choices[0].message.content

    # Publish to output topic
    async with httpx.AsyncClient() as http:
        await http.post(
            f"{DAPR_URL}/v1.0/publish/{PUBSUB_NAME}/your.output.topic",
            json={"data": result, "student_id": data.get("student_id")}
        )
    return {"status": "processed"}

@app.get("/health")
async def health():
    return {"status": "healthy", "service": "your-service"}
```

## Kubernetes Deployment Template
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: your-service
  namespace: learnflow
spec:
  replicas: 1
  selector:
    matchLabels:
      app: your-service
  template:
    metadata:
      labels:
        app: your-service
      annotations:
        dapr.io/enabled: "true"
        dapr.io/app-id: "your-service"
        dapr.io/app-port: "8000"
    spec:
      containers:
      - name: your-service
        image: your-service:latest
        ports:
        - containerPort: 8000
        env:
        - name: OPENAI_API_KEY
          valueFrom:
            secretKeyRef:
              name: openai-secret
              key: api-key
        - name: DAPR_HTTP_PORT
          value: "3500"
        - name: DAPR_PUBSUB_NAME
          value: "kafka-pubsub"
```

## Dockerfile Template (Multi-stage)
```dockerfile
FROM python:3.11-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY main.py .
EXPOSE 8000
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## Dapr Pub/Sub Component
```yaml
apiVersion: dapr.io/v1alpha1
kind: Component
metadata:
  name: kafka-pubsub
  namespace: learnflow
spec:
  type: pubsub.kafka
  version: v1
  metadata:
  - name: brokers
    value: "kafka-cluster-kafka-bootstrap.kafka:9092"
  - name: authType
    value: "none"
```
