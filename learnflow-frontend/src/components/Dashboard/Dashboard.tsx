'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useProgress } from '@/hooks/useProgress'
import { toast } from 'sonner'
import MasteryChart from './MasteryChart'
import QuizModal from './QuizModal'
import AISidekick from './AISidekick'
import CodeEditor from './CodeEditor'

export default function Dashboard() {
  const [isQuizOpen, setIsQuizOpen] = useState(false)
  const [activeTab, setActiveTab] = useState<'progress' | 'editor'>('progress')

  const {
    data: progressData,
    struggleDetected,
    isLoading: progressIsLoading,
    mutate: mutateProgress,
  } = useProgress()

  useEffect(() => {
    if (struggleDetected) {
      toast('Struggle Detected!', {
        description: 'AI Sidekick is ready to help you. Click the chat button!',
      })
    }
  }, [struggleDetected])

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900 px-8 py-4 flex items-center justify-between">
        <div className="flex items-center gap-3">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-blue-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm">L</div>
          <span className="font-semibold text-lg">LearnFlow</span>
          <span className="text-gray-500 text-sm">| AI Python Tutor</span>
        </div>
        <div className="flex items-center gap-3">
          <span className="text-sm text-gray-400">Student: Maya</span>
          <div className="w-8 h-8 rounded-full bg-gradient-to-br from-blue-400 to-purple-500 flex items-center justify-center text-sm font-bold">M</div>
        </div>
      </header>

      <div className="px-8 py-6 space-y-6">
        {/* Page title + tabs */}
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Dashboard</h1>
            <p className="text-gray-400 text-sm mt-1">Track your Python learning progress</p>
          </div>
          <div className="flex gap-2">
            <button
              onClick={() => setActiveTab('progress')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'progress' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
            >
              Progress
            </button>
            <button
              onClick={() => setActiveTab('editor')}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${activeTab === 'editor' ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:text-white'}`}
            >
              Code Editor
            </button>
          </div>
        </div>

        {activeTab === 'progress' && (
          <>
            {/* Stats row */}
            <div className="grid grid-cols-3 gap-4">
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <p className="text-gray-500 text-xs uppercase tracking-wide">Current Module</p>
                <p className="text-white font-semibold mt-1">Module 2: Loops</p>
                <div className="w-full bg-gray-800 rounded-full h-1.5 mt-2">
                  <div className="bg-blue-500 h-1.5 rounded-full" style={{ width: '60%' }} />
                </div>
                <p className="text-gray-500 text-xs mt-1">60% complete</p>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-4">
                <p className="text-gray-500 text-xs uppercase tracking-wide">Overall Mastery</p>
                <p className="text-white font-bold text-2xl mt-1">
                  {progressData.length > 0
                    ? Math.round(progressData.reduce((s, d) => s + d.mastery, 0) / progressData.length)
                    : 0}%
                </p>
                <p className="text-gray-500 text-xs mt-1">across all topics</p>
              </div>
              <div className={`border rounded-xl p-4 ${struggleDetected ? 'bg-red-900/20 border-red-700' : 'bg-gray-900 border-gray-800'}`}>
                <p className="text-gray-500 text-xs uppercase tracking-wide">Status</p>
                <p className={`font-semibold mt-1 ${struggleDetected ? 'text-red-400' : 'text-green-400'}`}>
                  {struggleDetected ? '⚠️ Needs Help' : '✅ On Track'}
                </p>
                <p className="text-gray-500 text-xs mt-1">{struggleDetected ? 'AI Sidekick activated' : 'Keep it up!'}</p>
              </div>
            </div>

            {/* Mastery Chart */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
              <div className="flex justify-between items-center mb-4">
                <h2 className="text-lg font-semibold text-white">Topic Mastery</h2>
                <Button
                  onClick={() => setIsQuizOpen(true)}
                  className="bg-blue-600 hover:bg-blue-700 text-white text-sm"
                >
                  Take Quiz
                </Button>
              </div>
              <MasteryChart data={progressData || []} isLoading={progressIsLoading} />
            </div>
          </>
        )}

        {activeTab === 'editor' && <CodeEditor />}
      </div>

      <QuizModal
        open={isQuizOpen}
        onOpenChange={setIsQuizOpen}
        onSuccess={(score) => {
          mutateProgress()
          if (score < 50) {
            toast.warning('Struggle detected! Opening AI Sidekick...')
          }
        }}
      />
      <AISidekick struggleDetected={struggleDetected} />
    </div>
  )
}
