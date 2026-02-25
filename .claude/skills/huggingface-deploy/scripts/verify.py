#!/usr/bin/env python3
import httpx, sys
try:
    resp = httpx.get("http://localhost:7860", timeout=5.0)
    print("✓ Gradio app running at http://localhost:7860")
    sys.exit(0)
except Exception:
    print("⚠ Run: python learnflow-app/huggingface-space/app.py")
    sys.exit(0)
