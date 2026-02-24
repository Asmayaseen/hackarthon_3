'use client'

import { useState } from 'react'
import Editor from '@monaco-editor/react'
import { Button } from '@/components/ui/button'
import { Play, RotateCcw, Loader2, Send } from 'lucide-react'
import { toast } from 'sonner'
import { useTheme } from 'next-themes'

const STARTER_CODE = `# LearnFlow Python Editor
# Write your Python code here and press Run!

def greet(name):
    return f"Hello, {name}! Welcome to LearnFlow."

# Try it out:
print(greet("Maya"))

# Now try writing your own:
for i in range(1, 6):
    print(f"Count: {i}")
`

export default function CodeEditor() {
  const [code, setCode] = useState(STARTER_CODE)
  const [output, setOutput] = useState('')
  const [error, setError] = useState('')
  const [running, setRunning] = useState(false)
  const [reviewing, setReviewing] = useState(false)
  const [review, setReview] = useState('')
  const { resolvedTheme } = useTheme()
  const monacoTheme = resolvedTheme === 'dark' ? 'vs-dark' : 'light'

  const runCode = async () => {
    setRunning(true)
    setOutput('')
    setError('')
    setReview('')
    try {
      const res = await fetch('/api/execute', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      })
      const data = await res.json()
      setOutput(data.output || '')
      setError(data.error || '')
    } catch {
      setError('Failed to run code. Server error.')
    } finally {
      setRunning(false)
    }
  }

  const reviewCode = async () => {
    if (!code.trim()) return
    setReviewing(true)
    setReview('')
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `Please review this Python code for correctness, style (PEP 8), and efficiency:\n\`\`\`python\n${code}\n\`\`\``,
          student_id: 'demo-student',
        }),
      })
      const data = await res.json()
      setReview(data.reply || '')
    } catch {
      toast.error('Code review failed.')
    } finally {
      setReviewing(false)
    }
  }

  return (
    <div className="grid grid-cols-2 gap-4 h-[calc(100vh-220px)]">
      {/* Editor panel */}
      <div className="bg-card border border-border rounded-xl overflow-hidden flex flex-col">
        <div className="px-4 py-3 border-b border-border flex items-center justify-between">
          <span className="text-sm font-medium text-foreground">Python Editor</span>
          <div className="flex gap-2">
            <Button
              variant="ghost"
              size="sm"
              className="h-7 px-2 text-muted-foreground hover:text-foreground"
              onClick={() => { setCode(STARTER_CODE); setOutput(''); setError(''); setReview('') }}
            >
              <RotateCcw className="h-3.5 w-3.5" />
            </Button>
            <Button
              size="sm"
              onClick={runCode}
              disabled={running}
              className="h-7 px-3 bg-emerald-600 hover:bg-emerald-700 text-white text-xs border-0"
            >
              {running ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" /> : <Play className="h-3.5 w-3.5 mr-1" />}
              Run
            </Button>
            <Button
              size="sm"
              onClick={reviewCode}
              disabled={reviewing}
              className="h-7 px-3 bg-violet-600 hover:bg-violet-700 text-white text-xs border-0"
            >
              {reviewing ? <Loader2 className="h-3.5 w-3.5 animate-spin mr-1" /> : <Send className="h-3.5 w-3.5 mr-1" />}
              Review
            </Button>
          </div>
        </div>
        <div className="flex-1">
          <Editor
            height="100%"
            language="python"
            value={code}
            onChange={v => setCode(v || '')}
            theme={monacoTheme}
            options={{
              minimap: { enabled: false },
              fontSize: 13,
              lineNumbers: 'on',
              scrollBeyondLastLine: false,
              wordWrap: 'on',
              padding: { top: 12 },
            }}
          />
        </div>
      </div>

      {/* Output + Review panel */}
      <div className="flex flex-col gap-3">
        {/* Terminal output */}
        <div className="bg-muted/30 border border-border rounded-xl overflow-hidden flex flex-col flex-1">
          <div className="px-4 py-2 border-b border-border flex items-center gap-2">
            <div className="flex gap-1.5">
              <div className="w-3 h-3 rounded-full bg-red-500" />
              <div className="w-3 h-3 rounded-full bg-yellow-500" />
              <div className="w-3 h-3 rounded-full bg-green-500" />
            </div>
            <span className="text-xs text-muted-foreground font-mono">terminal</span>
          </div>
          <div className="flex-1 p-4 font-mono text-sm overflow-y-auto">
            {!output && !error && !running && (
              <p className="text-muted-foreground/50">Press Run to execute your code...</p>
            )}
            {running && <p className="text-yellow-500">Running...</p>}
            {output && <pre className="text-emerald-500 whitespace-pre-wrap">{output}</pre>}
            {error && <pre className="text-red-500 whitespace-pre-wrap">{error}</pre>}
          </div>
        </div>

        {/* AI Review panel */}
        {(review || reviewing) && (
          <div className="bg-card border border-violet-500/30 rounded-xl overflow-hidden flex flex-col max-h-[45%]">
            <div className="px-4 py-2 border-b border-border">
              <span className="text-xs text-purple-400 font-medium">AI Code Review</span>
            </div>
            <div className="flex-1 p-4 overflow-y-auto text-sm text-muted-foreground">
              {reviewing ? (
                <div className="flex items-center gap-2">
                  <Loader2 className="h-4 w-4 animate-spin text-violet-400" />
                  Analyzing your code...
                </div>
              ) : (
                <pre className="whitespace-pre-wrap font-sans text-foreground">{review}</pre>
              )}
            </div>
          </div>
        )}
      </div>
    </div>
  )
}
