import { NextRequest, NextResponse } from 'next/server'

export async function POST(req: NextRequest) {
  try {
    const { code } = await req.json()

    if (!code || typeof code !== 'string') {
      return NextResponse.json({ error: 'No code provided' }, { status: 400 })
    }

    // Security: block dangerous imports
    const dangerous = ['import os', 'import sys', 'import subprocess', 'import socket', '__import__', 'open(', 'exec(', 'eval(', 'compile(']
    for (const d of dangerous) {
      if (code.toLowerCase().includes(d.toLowerCase())) {
        return NextResponse.json({ output: '', error: `Blocked: '${d}' is not allowed in the sandbox.` })
      }
    }

    // Use Piston API for remote code execution (Vercel has no Python runtime)
    const response = await fetch('https://emkc.org/api/v2/piston/execute', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        language: 'python',
        version: '3.10.0',
        files: [{ content: code }],
      }),
      signal: AbortSignal.timeout(10000),
    })

    if (!response.ok) {
      return NextResponse.json({ output: '', error: 'Code execution service unavailable. Please try again.' })
    }

    const result = await response.json()
    const run = result.run || {}
    const output = run.stdout || ''
    const stderr = run.stderr || ''

    if (run.code !== 0 && stderr) {
      return NextResponse.json({ output, error: stderr })
    }

    return NextResponse.json({ output: output || '(no output)', error: null })
  } catch (err: unknown) {
    const e = err as { name?: string }
    if (e.name === 'TimeoutError') {
      return NextResponse.json({ output: '', error: 'Execution timed out (10s limit).' })
    }
    return NextResponse.json({ output: '', error: 'Server error during execution' })
  }
}
