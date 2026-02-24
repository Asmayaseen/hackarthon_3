import { NextRequest, NextResponse } from 'next/server'
import { execSync } from 'child_process'
import { writeFileSync, unlinkSync } from 'fs'
import { tmpdir } from 'os'
import { join } from 'path'

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

    // Write code to temp file
    const tmpFile = join(tmpdir(), `learnflow_${Date.now()}.py`)
    writeFileSync(tmpFile, code)

    try {
      const output = execSync(`timeout 5 python3 ${tmpFile} 2>&1`, {
        timeout: 6000,
        encoding: 'utf-8',
        maxBuffer: 50 * 1024,
      })
      unlinkSync(tmpFile)
      return NextResponse.json({ output: output || '(no output)', error: null })
    } catch (err: any) {
      unlinkSync(tmpFile)
      const errOutput = err.stdout || err.stderr || err.message || 'Execution failed'
      return NextResponse.json({ output: '', error: errOutput })
    }
  } catch {
    return NextResponse.json({ output: '', error: 'Server error during execution' })
  }
}
