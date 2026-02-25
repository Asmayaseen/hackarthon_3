"""
LearnFlow AI Tutor – HuggingFace Spaces Demo
============================================
A Gradio-powered demo of the LearnFlow Python tutoring platform.

Features:
  • AI Chat tutor (explain / debug / exercise / review modes)
  • Code execution sandbox
  • Progress tracking simulation

Deploy:
  huggingface-cli upload <your-org>/learnflow-tutor . --repo-type=space
  Space type: Gradio  |  SDK: gradio  |  Python: 3.11

Environment variables (set in Space secrets):
  OPENAI_API_KEY   – OpenAI key (or Groq key with OPENAI_BASE_URL)
  OPENAI_BASE_URL  – Optional; set to https://api.groq.com/openai/v1 for Groq
  AI_MODEL         – Default: gpt-4o-mini
"""

import os
import subprocess
import sys
import json
from typing import Generator

import gradio as gr

# ── OpenAI / Groq client ───────────────────────────────────────────────────────
try:
    from openai import OpenAI
    _kwargs = {"api_key": os.getenv("OPENAI_API_KEY", "demo-key")}
    if os.getenv("OPENAI_BASE_URL"):
        _kwargs["base_url"] = os.getenv("OPENAI_BASE_URL")
    client = OpenAI(**_kwargs)
    AI_MODEL = os.getenv("AI_MODEL", "gpt-4o-mini")
    AI_AVAILABLE = bool(os.getenv("OPENAI_API_KEY"))
except ImportError:
    client = None
    AI_AVAILABLE = False

SYSTEM_PROMPTS = {
    "Explain": (
        "You are a friendly Python tutor. Explain concepts clearly with simple language "
        "and concrete examples. Keep responses to 3–5 paragraphs. Use markdown code blocks."
    ),
    "Debug": (
        "You are a Python debugging expert. Identify the root cause, explain why it happened, "
        "then provide the fix. Be concise and educational."
    ),
    "Exercise": (
        "You are a Python exercise generator. Create a coding challenge appropriate for the "
        "student's level. Include a problem statement, example I/O, and a starter code template."
    ),
    "Review": (
        "You are a Python code reviewer. Check for correctness, PEP 8 style, efficiency, "
        "and readability. Rate the code 1–10 and be encouraging."
    ),
}

DEMO_RESPONSES = {
    "Explain": (
        "### For Loops in Python\n\n"
        "A `for` loop lets you iterate over any sequence — lists, strings, ranges, and more.\n\n"
        "```python\n# Basic for loop\nfruits = ['apple', 'banana', 'cherry']\nfor fruit in fruits:\n    print(fruit)\n```\n\n"
        "**Key points:**\n- The loop variable (`fruit`) takes each value in turn\n"
        "- Use `range(n)` to loop `n` times: `for i in range(5):`\n"
        "- `break` exits the loop early; `continue` skips to the next iteration"
    ),
    "Debug": (
        "### Debugging Your Code\n\n"
        "The most common Python errors:\n\n"
        "| Error | Cause | Fix |\n|-------|-------|-----|\n"
        "| `TypeError` | Wrong type operation | Check variable types |\n"
        "| `IndexError` | List index out of range | Check list length |\n"
        "| `NameError` | Variable not defined | Check spelling/scope |\n\n"
        "```python\n# Before (buggy)\ndef add(a, b):\n    return a + b\nresult = add('5', 3)  # TypeError!\n\n"
        "# After (fixed)\nresult = add(int('5'), 3)  # ✓\n```"
    ),
    "Exercise": (
        "### Exercise: FizzBuzz\n\n"
        "**Problem:** Print numbers 1–20. For multiples of 3 print `Fizz`, "
        "for multiples of 5 print `Buzz`, for multiples of both print `FizzBuzz`.\n\n"
        "**Example output:**\n```\n1\n2\nFizz\n4\nBuzz\nFizz\n...\n```\n\n"
        "**Starter code:**\n```python\nfor i in range(1, 21):\n    # your code here\n    pass\n```"
    ),
    "Review": (
        "### Code Review\n\n**Score: 7/10** 👍\n\n"
        "**Strengths:**\n- Clear variable names\n- Good use of functions\n\n"
        "**Improvements:**\n- Add docstrings to functions\n- Use list comprehension for conciseness\n\n"
        "```python\n# Original\ndef get_evens(numbers):\n    result = []\n    for n in numbers:\n        if n % 2 == 0:\n            result.append(n)\n    return result\n\n"
        "# Improved\ndef get_evens(numbers: list) -> list:\n    \"\"\"Return only even numbers from the list.\"\"\"\n    return [n for n in numbers if n % 2 == 0]\n```"
    ),
}


# ── Simulated student progress ─────────────────────────────────────────────────

def get_progress_html(sessions: int, level: str) -> str:
    base = {"beginner": 30, "intermediate": 60, "advanced": 85}[level]
    mastery = min(100, base + sessions * 2)
    topics = {
        "beginner":     ["Variables", "Loops", "Functions"],
        "intermediate": ["Variables", "Loops", "Functions", "OOP", "Exceptions"],
        "advanced":     ["Variables", "Loops", "Functions", "OOP", "Exceptions",
                         "Decorators", "Generators", "Async"],
    }[level]
    topics_html = "".join(
        f'<span style="background:#22c55e;color:white;padding:2px 8px;border-radius:12px;margin:2px;font-size:12px">{t}</span>'
        for t in topics
    )
    return f"""
    <div style="font-family:sans-serif;padding:12px;background:#0f172a;border-radius:8px;color:#e2e8f0">
      <h3 style="margin:0 0 8px;color:#60a5fa">📊 Progress Dashboard</h3>
      <div style="margin:4px 0">
        <span style="color:#94a3b8">Mastery Score: </span>
        <b style="color:#22c55e">{mastery}%</b>
      </div>
      <div style="background:#1e293b;border-radius:6px;height:10px;margin:6px 0">
        <div style="background:#22c55e;width:{mastery}%;height:10px;border-radius:6px"></div>
      </div>
      <div style="margin:6px 0">
        <span style="color:#94a3b8">Sessions: </span><b>{sessions + 1}</b> &nbsp;
        <span style="color:#94a3b8">Level: </span><b style="color:#f59e0b">{level.capitalize()}</b>
      </div>
      <div style="margin-top:8px;color:#94a3b8;font-size:12px">Topics mastered:</div>
      <div style="margin-top:4px">{topics_html}</div>
    </div>
    """


# ── Chat function ──────────────────────────────────────────────────────────────

def chat(
    message: str,
    history: list,
    mode: str,
    level: str,
    session_count: int,
) -> tuple[str, list, int, str]:
    if not message.strip():
        return "", history, session_count, get_progress_html(session_count, level)

    history = history or []

    if AI_AVAILABLE and client:
        messages = [{"role": "system", "content": SYSTEM_PROMPTS[mode]}]
        for h in history[-8:]:
            messages.append({"role": "user",      "content": h[0]})
            messages.append({"role": "assistant", "content": h[1]})
        messages.append({"role": "user", "content": f"[Level: {level}] {message}"})
        try:
            resp = client.chat.completions.create(
                model=AI_MODEL, messages=messages, temperature=0.7, max_tokens=600
            )
            reply = resp.choices[0].message.content
        except Exception as e:
            reply = f"⚠️ AI unavailable: {e}\n\n{DEMO_RESPONSES.get(mode, 'Try again.')}"
    else:
        reply = (
            f"**[Demo mode – no API key]**\n\n{DEMO_RESPONSES.get(mode, 'Please set OPENAI_API_KEY.')}"
        )

    history.append((message, reply))
    session_count += 1
    return "", history, session_count, get_progress_html(session_count, level)


# ── Code execution ─────────────────────────────────────────────────────────────

def run_code(code: str) -> str:
    if not code.strip():
        return "# Write some Python code and click Run ▶"
    try:
        result = subprocess.run(
            [sys.executable, "-c", code],
            capture_output=True, text=True, timeout=10
        )
        output = result.stdout.strip()
        err    = result.stderr.strip()
        if err:
            return f"❌ Error:\n{err}"
        return output or "✓ Ran successfully (no output)"
    except subprocess.TimeoutExpired:
        return "⏱ Execution timed out (10s limit)"
    except Exception as e:
        return f"❌ {e}"


# ── Gradio UI ──────────────────────────────────────────────────────────────────

THEME = gr.themes.Soft(
    primary_hue="blue",
    secondary_hue="slate",
    neutral_hue="slate",
)

with gr.Blocks(
    theme=THEME,
    title="LearnFlow AI Tutor",
    css="""
    .gradio-container { max-width: 900px !important; }
    footer { display: none !important; }
    """,
) as demo:

    # State
    session_count = gr.State(value=0)

    # Header
    gr.Markdown(
        """
        # 🎓 LearnFlow AI Tutor
        **Interactive Python learning powered by AI** · Built for Hackathon III
        """
    )

    with gr.Tabs():

        # ── Tab 1: AI Chat ─────────────────────────────────────────────────────
        with gr.Tab("💬 AI Tutor"):
            with gr.Row():
                with gr.Column(scale=3):
                    chatbot = gr.Chatbot(height=400, label="Conversation")
                    with gr.Row():
                        msg_box = gr.Textbox(
                            placeholder="Ask anything about Python…",
                            show_label=False, scale=4
                        )
                        send_btn = gr.Button("Send ▶", variant="primary", scale=1)
                    gr.Examples(
                        examples=[
                            "How do for loops work?",
                            "I got TypeError: unsupported operand type(s) — help!",
                            "Give me a beginner exercise on functions",
                            "Review this code: def add(a,b): return a+b",
                        ],
                        inputs=msg_box,
                        label="Try these",
                    )

                with gr.Column(scale=1):
                    mode = gr.Radio(
                        choices=["Explain", "Debug", "Exercise", "Review"],
                        value="Explain",
                        label="Mode",
                    )
                    level = gr.Dropdown(
                        choices=["beginner", "intermediate", "advanced"],
                        value="beginner",
                        label="Student Level",
                    )
                    progress_panel = gr.HTML(
                        get_progress_html(0, "beginner"),
                        label="Progress",
                    )

            # Wire chat
            send_inputs  = [msg_box, chatbot, mode, level, session_count]
            send_outputs = [msg_box, chatbot, session_count, progress_panel]
            msg_box.submit(chat, send_inputs, send_outputs)
            send_btn.click(chat, send_inputs, send_outputs)

            # Update progress when level changes
            level.change(
                lambda lv, sc: get_progress_html(sc, lv),
                inputs=[level, session_count],
                outputs=[progress_panel],
            )

        # ── Tab 2: Code Runner ─────────────────────────────────────────────────
        with gr.Tab("⚙️ Code Runner"):
            gr.Markdown("Write Python and run it in a sandboxed environment.")
            with gr.Row():
                with gr.Column():
                    code_editor = gr.Code(
                        value='# Your code here\nprint("Hello, LearnFlow!")',
                        language="python",
                        label="Python Code",
                        lines=14,
                    )
                    run_btn = gr.Button("Run ▶", variant="primary")
                with gr.Column():
                    code_output = gr.Textbox(
                        label="Output",
                        lines=14,
                        value="# Output will appear here",
                    )
            run_btn.click(run_code, inputs=code_editor, outputs=code_output)

            gr.Examples(
                examples=[
                    ['# FizzBuzz\nfor i in range(1, 21):\n    if i % 15 == 0:\n        print("FizzBuzz")\n    elif i % 3 == 0:\n        print("Fizz")\n    elif i % 5 == 0:\n        print("Buzz")\n    else:\n        print(i)'],
                    ['# List comprehension\nnumbers = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]\nevens = [n for n in numbers if n % 2 == 0]\nprint("Even numbers:", evens)'],
                    ['# Recursion: factorial\ndef factorial(n):\n    if n <= 1:\n        return 1\n    return n * factorial(n - 1)\n\nfor i in range(1, 8):\n    print(f"{i}! = {factorial(i)}")'],
                ],
                inputs=code_editor,
                label="Examples",
            )

        # ── Tab 3: About ───────────────────────────────────────────────────────
        with gr.Tab("ℹ️ About"):
            gr.Markdown(
                """
                ## LearnFlow Platform
                LearnFlow is an AI-powered Python learning platform built as part of **Hackathon III**.

                ### Architecture
                | Service | Port | Role |
                |---------|------|------|
                | Triage Service | 8000 | Routes student queries to AI agents |
                | Concepts Service | 8001 | Explains Python concepts |
                | Debug Service | 8002 | Helps fix code errors |
                | Code Review Service | 8003 | Reviews student code |
                | Exercise Service | 8004 | Generates coding challenges |
                | Progress Service | 8005 | Tracks mastery scores |
                | MCP Server | 8006 | Model Context Protocol integration |
                | API Gateway | 8007 | Central entry point |

                ### Tech Stack
                - **Backend:** FastAPI + Dapr + Kafka (event-driven microservices)
                - **Frontend:** Next.js 15 with dark/light mode
                - **AI:** OpenAI GPT-4o-mini / Groq LLaMA-3
                - **Infrastructure:** Kubernetes + ArgoCD GitOps
                - **Demo:** HuggingFace Spaces (this app)

                ### Links
                - 📦 [GitHub Repository](https://github.com/Asmayaseen/hackarthon_3)
                - 📖 [Documentation](https://learnflow.docs)
                """
            )

if __name__ == "__main__":
    demo.launch(server_name="0.0.0.0", server_port=7860, share=False)
