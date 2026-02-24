'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { CheckCircle, XCircle, Loader2 } from 'lucide-react'
import { toast } from 'sonner'

interface Question {
  id: number
  question: string
  options: string[]
  answer: number
  topic: string
}

interface QuizModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: (score: number) => void
}

export default function QuizModal({ open, onOpenChange, onSuccess }: QuizModalProps) {
  const [questions, setQuestions] = useState<Question[]>([])
  const [answers, setAnswers] = useState<Record<number, number>>({})
  const [submitted, setSubmitted] = useState(false)
  const [results, setResults] = useState<any>(null)
  const [loading, setLoading] = useState(false)

  useEffect(() => {
    if (open) {
      setAnswers({})
      setSubmitted(false)
      setResults(null)
      fetch('/api/quiz').then(r => r.json()).then(d => setQuestions(d.questions || []))
    }
  }, [open])

  const handleSubmit = async () => {
    if (Object.keys(answers).length < questions.length) {
      toast.warning('Please answer all questions first.')
      return
    }
    setLoading(true)
    try {
      const res = await fetch('/api/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ answers }),
      })
      const data = await res.json()
      setResults(data)
      setSubmitted(true)
      toast.success(`Quiz complete! Score: ${data.score}%`)
      onSuccess?.(data.score)
    } catch {
      toast.error('Failed to submit quiz.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-xl bg-card border-border text-foreground">
        <DialogHeader>
          <DialogTitle className="text-foreground text-xl">
            {submitted ? `Quiz Results — ${results?.score}%` : 'Python Quiz'}
          </DialogTitle>
        </DialogHeader>

        {!submitted ? (
          <div className="space-y-6 py-2">
            {questions.map((q, qi) => (
              <div key={q.id} className="space-y-2">
                <p className="font-medium text-foreground text-sm">
                  <span className="text-blue-400 mr-2">Q{qi + 1}.</span>{q.question}
                </p>
                <div className="grid grid-cols-2 gap-2">
                  {q.options.map((opt, oi) => (
                    <button
                      key={oi}
                      onClick={() => setAnswers(prev => ({ ...prev, [q.id]: oi }))}
                      className={`px-3 py-2 rounded-lg text-sm text-left border transition-all ${
                        answers[q.id] === oi
                          ? 'bg-primary border-primary text-primary-foreground'
                          : 'bg-muted border-border text-foreground hover:border-primary/50'
                      }`}
                    >
                      {opt}
                    </button>
                  ))}
                </div>
              </div>
            ))}
            <div className="flex justify-end gap-3 pt-2">
              <Button variant="outline" onClick={() => onOpenChange(false)} className="border-gray-600 text-gray-300">
                Cancel
              </Button>
              <Button
                onClick={handleSubmit}
                disabled={loading || Object.keys(answers).length < questions.length}
                className="bg-blue-600 hover:bg-blue-700"
              >
                {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
                Submit Quiz
              </Button>
            </div>
          </div>
        ) : (
          <div className="space-y-4 py-2">
            <div className={`text-center p-4 rounded-xl ${results.score >= 70 ? 'bg-green-900/30 border border-green-700' : 'bg-red-900/30 border border-red-700'}`}>
              <p className="text-3xl font-bold">{results.score}%</p>
              <p className="text-sm text-gray-400 mt-1">{results.correct}/{results.total} correct</p>
              {results.struggleDetected && (
                <p className="text-yellow-400 text-sm mt-2">💡 AI Sidekick will help you review the topics you missed!</p>
              )}
            </div>
            {results.results?.map((r: any) => (
              <div key={r.id} className="flex items-start gap-2 text-sm">
                {r.isCorrect
                  ? <CheckCircle className="h-4 w-4 text-green-400 mt-0.5 shrink-0" />
                  : <XCircle className="h-4 w-4 text-red-400 mt-0.5 shrink-0" />
                }
                <span className={r.isCorrect ? 'text-gray-300' : 'text-gray-400 line-through'}>{r.question}</span>
              </div>
            ))}
            <Button onClick={() => onOpenChange(false)} className="w-full bg-blue-600 hover:bg-blue-700">
              Close
            </Button>
          </div>
        )}
      </DialogContent>
    </Dialog>
  )
}
