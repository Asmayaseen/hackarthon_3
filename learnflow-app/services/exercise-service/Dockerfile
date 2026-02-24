FROM python:3.11-slim AS builder
WORKDIR /app
RUN python -m venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

FROM python:3.11-slim
WORKDIR /app
RUN useradd -m -u 1000 exercise && apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=builder /opt/venv /opt/venv
ENV PATH="/opt/venv/bin:$PATH"
COPY main.py .
RUN chown -R exercise:exercise /app
USER exercise
EXPOSE 8004
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s \
  CMD curl -sf http://localhost:8004/health || exit 1
ENV PYTHONUNBUFFERED=1 PORT=8004
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8004"]
