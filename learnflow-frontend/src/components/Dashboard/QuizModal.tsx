'use client'

import React, { useState, useEffect } from 'react'
import { Dialog, DialogContent, DialogHeader, DialogTitle } from '@/components/ui/dialog'
import { Button } from '@/components/ui/button'
import { CheckCircle2, XCircle, Loader2, Trophy, ChevronRight, ChevronLeft, Brain } from 'lucide-react'
import { toast } from 'sonner'

interface Question {
  id: number
  question: string
  options: string[]
  answer: number
  topic: string
}

interface QuizResult {
  id: number
  question: string
  isCorrect: boolean
  correctAnswer: string
  correctLabel: string
  yourAnswer: string
}

interface QuizResults {
  score?: number
  total: number
  correct?: number
  struggleDetected?: boolean
  results?: QuizResult[]
}

interface QuizModalProps {
  open: boolean
  onOpenChange: (open: boolean) => void
  onSuccess?: (score: number) => void
}

type Phase = 'loading' | 'quiz' | 'results'

export default function QuizModal({ open, onOpenChange, onSuccess }: QuizModalProps) {
  const [questions, setQuestions] = useState<Question[]>([])
  const [answers, setAnswers] = useState<Record<number, number>>({})
  const [current, setCurrent] = useState(0)
  const [phase, setPhase] = useState<Phase>('loading')
  const [results, setResults] = useState<QuizResults | null>(null)
  const [submitting, setSubmitting] = useState(false)

  useEffect(() => {
    if (open) {
      setPhase('loading')
      setAnswers({})
      setCurrent(0)
      setResults(null)
      fetch('/api/quiz')
        .then(r => r.json())
        .then(d => { setQuestions(d.questions || []); setPhase('quiz') })
        .catch(() => setPhase('quiz'))
    }
  }, [open])

  const q = questions[current]
  const answered = Object.keys(answers).length
  const progress = questions.length > 0 ? (answered / questions.length) * 100 : 0

  const handleSelect = (optionIdx: number) => {
    if (!q) return
    setAnswers(prev => ({ ...prev, [q.id]: optionIdx }))
  }

  const handleSubmit = async () => {
    if (answered < questions.length) {
      toast.warning(`Please answer all ${questions.length} questions first.`)
      return
    }
    setSubmitting(true)
    try {
      const res = await fetch('/api/quiz', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          answers,
          questionIds: questions.map(q => q.id),
        }),
      })
      const data = await res.json()
      setResults(data)
      setPhase('results')
      onSuccess?.(data.score)
    } catch {
      toast.error('Failed to submit quiz.')
    } finally {
      setSubmitting(false)
    }
  }

  const score = results?.score ?? 0
  const scoreColor = score >= 80 ? 'text-emerald-500' : score >= 50 ? 'text-amber-500' : 'text-red-500'
  const scoreBg = score >= 80 ? 'bg-emerald-500/10 border-emerald-500/30' : score >= 50 ? 'bg-amber-500/10 border-amber-500/30' : 'bg-red-500/10 border-red-500/30'

  return (
    <Dialog open={open} onOpenChange={onOpenChange}>
      <DialogContent className="max-w-lg w-full bg-card border-border text-foreground p-0 overflow-hidden">

        {/* Header */}
        <div className="px-6 pt-6 pb-4 border-b border-border">
          <DialogHeader>
            <DialogTitle className="flex items-center gap-2 text-foreground text-lg">
              <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                <Brain className="h-4 w-4 text-primary" />
              </div>
              {phase === 'results' ? 'Quiz Results' : 'Python Quiz'}
            </DialogTitle>
          </DialogHeader>

          {/* Progress bar (quiz phase) */}
          {phase === 'quiz' && questions.length > 0 && (
            <div className="mt-4 space-y-2">
              <div className="flex justify-between text-xs text-muted-foreground">
                <span>Question {current + 1} of {questions.length}</span>
                <span>{answered}/{questions.length} answered</span>
              </div>
              <div className="w-full bg-muted rounded-full h-1.5">
                <div
                  className="bg-primary h-1.5 rounded-full transition-all duration-500"
                  style={{ width: `${progress}%` }}
                />
              </div>
            </div>
          )}
        </div>

        {/* Body */}
        <div className="px-6 py-5">

          {/* Loading */}
          {phase === 'loading' && (
            <div className="flex flex-col items-center justify-center py-12 gap-3">
              <Loader2 className="h-8 w-8 animate-spin text-primary" />
              <p className="text-muted-foreground text-sm">Loading questions...</p>
            </div>
          )}

          {/* Quiz */}
          {phase === 'quiz' && q && (
            <div className="space-y-5">
              {/* Topic tag */}
              <span className="inline-block px-2.5 py-0.5 text-xs font-medium bg-primary/10 text-primary rounded-full">
                {q.topic}
              </span>

              {/* Question */}
              <p className="text-foreground font-medium text-base leading-relaxed">
                {q.question}
              </p>

              {/* Options */}
              <div className="space-y-2.5">
                {q.options.map((opt, i) => {
                  const selected = answers[q.id] === i
                  return (
                    <button
                      key={i}
                      onClick={() => handleSelect(i)}
                      className={`w-full text-left px-4 py-3 rounded-xl border text-sm font-medium transition-all duration-150 ${
                        selected
                          ? 'bg-primary border-primary text-primary-foreground shadow-md shadow-primary/20'
                          : 'bg-muted/50 border-border text-foreground hover:border-primary/50 hover:bg-accent'
                      }`}
                    >
                      <span className={`inline-flex items-center justify-center w-5 h-5 rounded-full text-xs mr-3 border ${selected ? 'border-primary-foreground/50 bg-primary-foreground/20' : 'border-muted-foreground/40'}`}>
                        {String.fromCharCode(65 + i)}
                      </span>
                      {opt}
                    </button>
                  )
                })}
              </div>

              {/* Navigation */}
              <div className="flex items-center justify-between pt-2">
                <Button
                  variant="outline"
                  size="sm"
                  onClick={() => setCurrent(c => Math.max(0, c - 1))}
                  disabled={current === 0}
                  className="gap-1"
                >
                  <ChevronLeft className="h-4 w-4" /> Prev
                </Button>

                {current < questions.length - 1 ? (
                  <Button
                    size="sm"
                    onClick={() => setCurrent(c => Math.min(questions.length - 1, c + 1))}
                    className="gap-1 bg-primary hover:bg-primary/90 text-primary-foreground border-0"
                  >
                    Next <ChevronRight className="h-4 w-4" />
                  </Button>
                ) : (
                  <Button
                    size="sm"
                    onClick={handleSubmit}
                    disabled={submitting || answered < questions.length}
                    className="gap-1 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white border-0"
                  >
                    {submitting ? <Loader2 className="h-4 w-4 animate-spin mr-1" /> : null}
                    Submit Quiz
                  </Button>
                )}
              </div>

              {/* Question dots */}
              <div className="flex justify-center gap-1.5 pt-1">
                {questions.map((_, i) => (
                  <button
                    key={i}
                    onClick={() => setCurrent(i)}
                    className={`w-2 h-2 rounded-full transition-all ${
                      i === current ? 'bg-primary w-4' :
                      answers[questions[i].id] !== undefined ? 'bg-primary/50' : 'bg-muted-foreground/30'
                    }`}
                  />
                ))}
              </div>
            </div>
          )}

          {/* Results */}
          {phase === 'results' && results && (
            <div className="space-y-5">
              {/* Score card */}
              <div className={`rounded-xl border p-5 text-center ${scoreBg}`}>
                <Trophy className={`h-8 w-8 mx-auto mb-2 ${scoreColor}`} />
                <p className={`text-4xl font-extrabold ${scoreColor}`}>{score}%</p>
                <p className="text-muted-foreground text-sm mt-1">
                  {results.correct} of {results.total} correct
                </p>
                {results.struggleDetected && (
                  <p className="text-amber-500 text-xs mt-2 font-medium">
                    💡 AI Sidekick will help you review missed topics!
                  </p>
                )}
              </div>

              {/* Per-question breakdown */}
              <div className="space-y-2 max-h-52 overflow-y-auto pr-1">
                {results.results?.map((r: QuizResult, i: number) => (
                  <div key={r.id} className={`flex items-start gap-2.5 p-3 rounded-lg border text-sm ${r.isCorrect ? 'bg-emerald-500/5 border-emerald-500/20' : 'bg-red-500/5 border-red-500/20'}`}>
                    {r.isCorrect
                      ? <CheckCircle2 className="h-4 w-4 text-emerald-500 shrink-0 mt-0.5" />
                      : <XCircle className="h-4 w-4 text-red-500 shrink-0 mt-0.5" />
                    }
                    <div className="min-w-0">
                      <p className="text-foreground font-medium truncate">Q{i+1}. {r.question}</p>
                      {!r.isCorrect && (
                        <p className="text-xs text-muted-foreground mt-0.5">
                          Correct: <span className="text-emerald-500">{r.correctLabel}</span>
                        </p>
                      )}
                    </div>
                  </div>
                ))}
              </div>

              <Button
                onClick={() => onOpenChange(false)}
                className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white border-0"
              >
                Close
              </Button>
            </div>
          )}
        </div>
      </DialogContent>
    </Dialog>
  )
}
