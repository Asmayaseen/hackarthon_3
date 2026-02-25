'use client'

import React, { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { useProgress } from '@/hooks/useProgress'
import { toast } from 'sonner'
import MasteryChart from './MasteryChart'
import QuizModal from './QuizModal'
import AISidekick from './AISidekick'
import CodeEditor from './CodeEditor'
import Navbar from '@/components/Navbar'
import { BarChart3, Code2, Trophy, AlertTriangle, TrendingUp, Target } from 'lucide-react'

export default function Dashboard() {
  const [isQuizOpen, setIsQuizOpen] = useState(false)
  const [activeTab, setActiveTab] = useState<'progress' | 'editor'>('progress')

  const {
    data: progressData,
    struggleDetected,
    isLoading: progressIsLoading,
    mutate: mutateProgress,
  } = useProgress()

  const avgMastery = progressData.length > 0
    ? Math.round(progressData.reduce((s, d) => s + d.mastery, 0) / progressData.length)
    : 0

  useEffect(() => {
    if (struggleDetected) {
      toast.warning('Struggle Detected!', {
        description: 'Your AI Sidekick is ready to help. Click the chat button!',
      })
    }
  }, [struggleDetected])

  const tabs = [
    { id: 'progress', label: 'Progress', icon: BarChart3 },
    { id: 'editor', label: 'Code Editor', icon: Code2 },
  ] as const

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 sm:py-8 space-y-5 sm:space-y-6">

        {/* Page header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Welcome back, Maya 👋</h1>
            <p className="text-muted-foreground text-sm mt-1">Continue your Python journey</p>
          </div>
          {/* Tab switcher */}
          <div className="flex items-center gap-1 p-1 bg-muted rounded-xl">
            {tabs.map(({ id, label, icon: Icon }) => (
              <button
                key={id}
                onClick={() => setActiveTab(id)}
                className={`flex items-center gap-2 px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                  activeTab === id
                    ? 'bg-background text-foreground shadow-sm border border-border'
                    : 'text-muted-foreground hover:text-foreground'
                }`}
              >
                <Icon className="h-4 w-4" />
                {label}
              </button>
            ))}
          </div>
        </div>

        {activeTab === 'progress' && (
          <>
            {/* Stats grid */}
            <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
              <StatCard
                icon={Target}
                label="Current Module"
                value="Module 2"
                sub="Loops — 60% done"
                color="text-blue-500"
                bg="bg-blue-500/10"
              />
              <StatCard
                icon={Trophy}
                label="Overall Mastery"
                value={`${avgMastery}%`}
                sub="across all topics"
                color="text-amber-500"
                bg="bg-amber-500/10"
              />
              <StatCard
                icon={TrendingUp}
                label="Topics Covered"
                value={`${progressData.length}`}
                sub="of 8 modules"
                color="text-emerald-500"
                bg="bg-emerald-500/10"
              />
              <div className={`p-4 rounded-xl border transition-all ${
                struggleDetected
                  ? 'border-red-500/30 bg-red-500/10'
                  : 'border-border bg-card'
              }`}>
                <div className={`w-8 h-8 rounded-lg flex items-center justify-center mb-2 ${
                  struggleDetected ? 'bg-red-500/20' : 'bg-emerald-500/10'
                }`}>
                  <AlertTriangle className={`h-4 w-4 ${struggleDetected ? 'text-red-400' : 'text-emerald-500'}`} />
                </div>
                <p className="text-xs text-muted-foreground uppercase tracking-wide">Status</p>
                <p className={`font-bold mt-0.5 ${struggleDetected ? 'text-red-400' : 'text-emerald-400'}`}>
                  {struggleDetected ? 'Needs Help' : 'On Track'}
                </p>
                <p className="text-xs text-muted-foreground mt-0.5">
                  {struggleDetected ? 'AI Sidekick activated' : 'Keep it up!'}
                </p>
              </div>
            </div>

            {/* Mastery Chart */}
            <div className="rounded-2xl border border-border bg-card p-6">
              <div className="flex items-center justify-between mb-6">
                <div>
                  <h2 className="font-semibold text-foreground">Topic Mastery</h2>
                  <p className="text-sm text-muted-foreground">Weekly progress across Python modules</p>
                </div>
                <Button
                  onClick={() => setIsQuizOpen(true)}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white shadow-lg shadow-indigo-500/20 border-0"
                >
                  Take Quiz
                </Button>
              </div>
              <MasteryChart data={progressData || []} isLoading={progressIsLoading} />
            </div>

            {/* Module progress */}
            <div className="rounded-2xl border border-border bg-card p-6">
              <h2 className="font-semibold text-foreground mb-4">Python Curriculum</h2>
              <div className="grid md:grid-cols-2 gap-3">
                {[
                  { module: '1. Variables & Types', pct: 95, status: 'mastered' },
                  { module: '2. Control Flow', pct: 60, status: 'learning' },
                  { module: '3. Data Structures', pct: 45, status: 'learning' },
                  { module: '4. Functions', pct: 30, status: 'beginner' },
                  { module: '5. OOP', pct: 10, status: 'beginner' },
                  { module: '6. File I/O', pct: 0, status: 'locked' },
                  { module: '7. Error Handling', pct: 0, status: 'locked' },
                  { module: '8. Libraries', pct: 0, status: 'locked' },
                ].map(({ module, pct, status }) => (
                  <div key={module} className="flex items-center gap-3 p-3 rounded-lg bg-muted/40 hover:bg-muted/70 transition-colors">
                    <div className={`w-2 h-2 rounded-full flex-shrink-0 ${
                      status === 'mastered' ? 'bg-emerald-400' :
                      status === 'learning' ? 'bg-blue-400' :
                      status === 'beginner' ? 'bg-amber-400' : 'bg-muted-foreground/30'
                    }`} />
                    <div className="flex-1 min-w-0">
                      <div className="flex justify-between items-center mb-1">
                        <span className="text-sm text-foreground truncate">{module}</span>
                        <span className="text-xs text-muted-foreground ml-2 flex-shrink-0">{pct}%</span>
                      </div>
                      <div className="w-full bg-border rounded-full h-1.5">
                        <div
                          className={`h-1.5 rounded-full transition-all ${
                            status === 'mastered' ? 'bg-emerald-400' :
                            status === 'learning' ? 'bg-blue-400' :
                            status === 'beginner' ? 'bg-amber-400' : 'bg-muted-foreground/20'
                          }`}
                          style={{ width: `${pct}%` }}
                        />
                      </div>
                    </div>
                  </div>
                ))}
              </div>
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
            toast.warning('AI Sidekick activated to help you review weak areas!')
          }
        }}
      />
      <AISidekick struggleDetected={struggleDetected} />
    </div>
  )
}

function StatCard({ icon: Icon, label, value, sub, color, bg }: {
  icon: React.ElementType; label: string; value: string; sub: string; color: string; bg: string
}) {
  return (
    <div className="p-4 rounded-xl border border-border bg-card hover:border-primary/30 transition-all">
      <div className={`w-8 h-8 rounded-lg ${bg} flex items-center justify-center mb-2`}>
        <Icon className={`h-4 w-4 ${color}`} />
      </div>
      <p className="text-xs text-muted-foreground uppercase tracking-wide">{label}</p>
      <p className="font-bold text-foreground mt-0.5">{value}</p>
      <p className="text-xs text-muted-foreground mt-0.5">{sub}</p>
    </div>
  )
}
