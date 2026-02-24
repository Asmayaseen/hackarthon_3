'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useProgress } from '@/hooks/useProgress'
import { toast } from 'sonner'
import MasteryChart from './MasteryChart'
import QuizModal from './QuizModal'
import AISidekick from './AISidekick'

export default function Dashboard() {
  const [isQuizOpen, setIsQuizOpen] = useState(false)

  const {
    data: progressData,
    struggleDetected,
    isLoading: progressIsLoading,
    mutate: mutateProgress,
  } = useProgress()

  useEffect(() => {
    if (struggleDetected) {
      toast('Struggle Detected! AI Sidekick is ready to assist.', {
        description: `Let's review concepts together.`,
      })
    }
  }, [struggleDetected])

  return (
    <div className="p-8 space-y-8">
      <div>
        <h1 className="text-3xl font-bold">Dashboard</h1>
        <p className="text-muted-foreground">Your learning progress.</p>
      </div>
      <div>
        <div className="flex justify-between items-center mb-4">
          <h2 className="text-2xl font-semibold">Mastery Chart</h2>
          <Button onClick={() => setIsQuizOpen(true)}>
            Take Quiz
          </Button>
        </div>
        <MasteryChart data={progressData || []} isLoading={progressIsLoading} />
      </div>
      <QuizModal open={isQuizOpen} onOpenChange={setIsQuizOpen} onSuccess={mutateProgress} />
      <AISidekick struggleDetected={struggleDetected} />
    </div>
  )
}