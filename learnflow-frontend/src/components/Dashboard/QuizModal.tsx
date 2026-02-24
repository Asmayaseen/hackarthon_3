'use client'

import React, { useState } from 'react'
import { Dialog, DialogContent, DialogDescription, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import dynamic from 'next/dynamic'
import Editor from '@monaco-editor/react'
import { useToast } from '@/components/ui/use-toast'

const API_BASE = '/api'

interface QuizModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: () => void
}

export default function QuizModal({ open, onOpenChange, onSuccess }: QuizModalProps) {
  const [code, setCode] = useState('')
  const [loading, setLoading] = useState(false)
  const { toast } = useToast()

  const handleSubmit = async () => {
    if (!code.trim()) return

    setLoading(true)
    try {
      const res = await fetch(`${API_BASE}/query`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ code }),
      })
      if (!res.ok) throw new Error('Submission failed')
      const data = await res.json()
      toast({
        title: 'Quiz Submitted',
        description: data.result || 'Code processed successfully.',
      })
      setCode('')
      onOpenChange(false)
      onSuccess?.()
    } catch (error) {
      toast({
        variant: 'destructive',
        title: 'Error',
        description: 'Failed to submit quiz. Check console.',
      })
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-2xl">
        <DialogHeader>
          <DialogTitle>Take Quiz</DialogTitle>
          <DialogDescription>
            Write code to solve: "Implement a function isPrime(n) that returns true if n is prime."
          </DialogDescription>
        </DialogHeader>
        <div className="space-y-4 py-4">
          <div className="h-[300px] font-mono">
            <Editor
              height="300px"
              language="python"
              value={code}
              onChange={(value) => setCode(value || '')}
              theme="vs-dark"
              options={{
                minimap: { enabled: false },
                scrollBeyondLastLine: false,
                fontSize: 14,
                wordWrap: 'on',
              }}
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button type="button" variant="outline" onClick={() => onOpenChange(false)}>
              Cancel
            </Button>
            <Button
              onClick={handleSubmit}
              disabled={loading || !code.trim()}
            >
              {loading ? 'Submitting...' : 'Submit & Check'}
            </Button>
          </div>
        </div>
      </DialogContent>
    </Dialog>
  )
}