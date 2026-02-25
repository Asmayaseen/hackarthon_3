#!/usr/bin/env python3
"""Scaffold a new MCP server from template."""
import argparse, os, sys

TEMPLATE = '''"""
{name} MCP Server
Provides AI agents context about: {name}
Token efficiency: Each tool returns < 100 tokens.
"""
from fastapi import FastAPI
from pydantic import BaseModel
from typing import Any, Dict
import json

app = FastAPI(title="{name}-mcp", version="1.0.0")

@app.get("/health")
async def health():
    return {{"status": "healthy", "service": "{name}-mcp"}}

@app.get("/tools")
async def list_tools():
    return {{"tools": [
        {{"name": "get_{name_snake}", "description": "Get {name} data"}}
    ]}}

@app.post("/tools/get_{name_snake}")
async def get_{name_snake}():
    # TODO: implement your tool
    return {{"summary": "✓ {name} data retrieved", "count": 0}}
'''

parser = argparse.ArgumentParser()
parser.add_argument("--name", default="my-tool")
parser.add_argument("--port", default="8010", type=int)
args = parser.parse_args()

name = args.name
name_snake = name.replace("-", "_")
content = TEMPLATE.format(name=name, name_snake=name_snake)

out_dir = f"learnflow-app/services/{name}"
os.makedirs(out_dir, exist_ok=True)
with open(f"{out_dir}/main.py", "w") as f:
    f.write(content)

print(f"✓ MCP server scaffolded at {out_dir}/main.py")
print(f"  Port: {args.port}")
sys.exit(0)
