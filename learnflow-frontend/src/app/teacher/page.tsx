'use client'

import { useState, useEffect } from 'react'
import Link from 'next/link'
import { Button } from '@/components/ui/button'
import { toast } from 'sonner'
import Navbar from '@/components/Navbar'
import {
  Users, AlertTriangle, TrendingUp, BookOpen,
  Loader2, Send, ChevronDown, ChevronUp, Brain
} from 'lucide-react'

// ── Types ──────────────────────────────────────────────────────────────────────

interface StudentRow {
  id: string
  name: string
  avatar: string
  mastery: number
  topic: string
  status: 'on-track' | 'struggling' | 'idle'
  lastActive: string
  topics: number
}

interface ExerciseRequest {
  topic: string
  difficulty: 'easy' | 'medium' | 'hard'
  count: number
}

// ── Mock data ──────────────────────────────────────────────────────────────────

const STUDENTS: StudentRow[] = [
  { id: 's1', name: 'Maya Chen',       avatar: 'M', mastery: 68, topic: 'Control Flow',    status: 'on-track',   lastActive: '2m ago',  topics: 4 },
  { id: 's2', name: 'James Williams',  avatar: 'J', mastery: 34, topic: 'Lists',           status: 'struggling', lastActive: '5m ago',  topics: 2 },
  { id: 's3', name: 'Priya Sharma',    avatar: 'P', mastery: 92, topic: 'OOP',             status: 'on-track',   lastActive: '1h ago',  topics: 7 },
  { id: 's4', name: 'Alex Johnson',    avatar: 'A', mastery: 51, topic: 'Functions',       status: 'on-track',   lastActive: '15m ago', topics: 3 },
  { id: 's5', name: 'Sarah Kim',       avatar: 'S', mastery: 22, topic: 'Variables',       status: 'struggling', lastActive: '20m ago', topics: 1 },
  { id: 's6', name: 'Carlos Mendez',   avatar: 'C', mastery: 79, topic: 'Data Structures', status: 'on-track',   lastActive: '30m ago', topics: 5 },
]

// ── Component ──────────────────────────────────────────────────────────────────

export default function TeacherDashboard() {
  const [selected, setSelected] = useState<string | null>(null)
  const [exerciseReq, setExerciseReq] = useState<ExerciseRequest>({ topic: '', difficulty: 'medium', count: 3 })
  const [generating, setGenerating] = useState(false)
  const [generatedExercise, setGeneratedExercise] = useState('')
  const [expandedAlert, setExpandedAlert] = useState<string | null>(null)

  const struggling = STUDENTS.filter(s => s.status === 'struggling')
  const avgMastery = Math.round(STUDENTS.reduce((s, st) => s + st.mastery, 0) / STUDENTS.length)

  const generateExercise = async () => {
    if (!exerciseReq.topic.trim()) {
      toast.warning('Please enter a topic for the exercise.')
      return
    }
    setGenerating(true)
    setGeneratedExercise('')
    try {
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({
          message: `Generate ${exerciseReq.count} Python coding exercise(s) on "${exerciseReq.topic}" at ${exerciseReq.difficulty} difficulty. Format each with: Problem statement, starter code template, and expected output example.`,
          student_id: 'teacher',
        }),
      })
      const data = await res.json()
      setGeneratedExercise(data.reply || '')
    } catch {
      toast.error('Failed to generate exercise.')
    } finally {
      setGenerating(false)
    }
  }

  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      <div className="max-w-7xl mx-auto px-4 sm:px-6 py-6 space-y-6">

        {/* Header */}
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <h1 className="text-2xl font-bold text-foreground">Teacher Dashboard</h1>
            <p className="text-sm text-muted-foreground mt-1">Monitor your class and generate exercises</p>
          </div>
          <div className="flex gap-2">
            <Link href="/dashboard">
              <Button variant="outline" size="sm">Student View</Button>
            </Link>
          </div>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-2 lg:grid-cols-4 gap-3 sm:gap-4">
          <StatCard icon={Users}         label="Total Students"     value={`${STUDENTS.length}`}   sub="in your class"         color="text-blue-500"    bg="bg-blue-500/10" />
          <StatCard icon={TrendingUp}    label="Avg Mastery"        value={`${avgMastery}%`}        sub="across all topics"     color="text-emerald-500" bg="bg-emerald-500/10" />
          <StatCard icon={AlertTriangle} label="Need Help"          value={`${struggling.length}`} sub="struggle alerts today"  color="text-red-500"     bg="bg-red-500/10" />
          <StatCard icon={BookOpen}      label="Avg Topics Done"    value="3.7"                     sub="of 8 modules"          color="text-amber-500"   bg="bg-amber-500/10" />
        </div>

        {/* Struggle Alerts */}
        {struggling.length > 0 && (
          <div className="rounded-2xl border border-red-500/30 bg-red-500/5 p-6">
            <div className="flex items-center gap-2 mb-4">
              <AlertTriangle className="h-5 w-5 text-red-400" />
              <h2 className="font-semibold text-foreground">Struggle Alerts</h2>
              <span className="ml-auto text-xs bg-red-500/20 text-red-400 px-2 py-0.5 rounded-full font-medium">
                {struggling.length} students
              </span>
            </div>
            <div className="space-y-3">
              {struggling.map(s => (
                <div key={s.id} className="bg-card border border-red-500/20 rounded-xl p-4">
                  <div className="flex items-center gap-3">
                    <div className="w-9 h-9 rounded-full bg-red-500/20 flex items-center justify-center text-red-400 font-bold text-sm">
                      {s.avatar}
                    </div>
                    <div className="flex-1 min-w-0">
                      <p className="font-medium text-foreground text-sm">{s.name}</p>
                      <p className="text-xs text-muted-foreground">Struggling with {s.topic} · {s.mastery}% mastery · {s.lastActive}</p>
                    </div>
                    <button
                      onClick={() => {
                        setExerciseReq(p => ({ ...p, topic: s.topic, difficulty: 'easy' }))
                        toast.info(`Exercise generator pre-filled for ${s.topic}`)
                      }}
                      className="text-xs px-3 py-1.5 bg-red-500/20 hover:bg-red-500/30 text-red-400 rounded-lg transition-colors"
                    >
                      Create Exercise
                    </button>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Class Roster */}
        <div className="rounded-2xl border border-border bg-card p-6">
          <h2 className="font-semibold text-foreground mb-4">Class Progress</h2>
          <div className="space-y-2">
            {STUDENTS.map(s => (
              <div
                key={s.id}
                className={`flex items-center gap-3 p-3 rounded-xl border transition-all cursor-pointer ${
                  selected === s.id
                    ? 'border-primary/50 bg-primary/5'
                    : 'border-border hover:border-border/80 hover:bg-muted/40'
                }`}
                onClick={() => setSelected(selected === s.id ? null : s.id)}
              >
                {/* Avatar */}
                <div className={`w-9 h-9 rounded-full flex items-center justify-center text-sm font-bold flex-shrink-0 ${
                  s.status === 'struggling' ? 'bg-red-500/20 text-red-400' :
                  s.mastery > 80 ? 'bg-emerald-500/20 text-emerald-400' :
                  'bg-blue-500/20 text-blue-400'
                }`}>
                  {s.avatar}
                </div>

                {/* Name + topic */}
                <div className="flex-1 min-w-0">
                  <div className="flex items-center gap-2 mb-0.5">
                    <span className="text-sm font-medium text-foreground">{s.name}</span>
                    {s.status === 'struggling' && (
                      <AlertTriangle className="h-3 w-3 text-red-400 flex-shrink-0" />
                    )}
                  </div>
                  <span className="text-xs text-muted-foreground">{s.topic} · {s.lastActive}</span>
                </div>

                {/* Progress bar */}
                <div className="hidden sm:block w-32">
                  <div className="flex justify-between text-xs text-muted-foreground mb-1">
                    <span>{s.topics} topics</span>
                    <span>{s.mastery}%</span>
                  </div>
                  <div className="w-full bg-border rounded-full h-1.5">
                    <div
                      className={`h-1.5 rounded-full transition-all ${
                        s.status === 'struggling' ? 'bg-red-400' :
                        s.mastery > 80 ? 'bg-emerald-400' : 'bg-blue-400'
                      }`}
                      style={{ width: `${s.mastery}%` }}
                    />
                  </div>
                </div>

                {/* Status badge */}
                <span className={`hidden lg:inline text-xs px-2 py-0.5 rounded-full font-medium ${
                  s.status === 'struggling'
                    ? 'bg-red-500/15 text-red-400'
                    : 'bg-emerald-500/15 text-emerald-400'
                }`}>
                  {s.status === 'struggling' ? 'Needs Help' : 'On Track'}
                </span>

                {selected === s.id
                  ? <ChevronUp className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                  : <ChevronDown className="h-4 w-4 text-muted-foreground flex-shrink-0" />
                }
              </div>
            ))}
          </div>
        </div>

        {/* Exercise Generator */}
        <div className="rounded-2xl border border-border bg-card p-6">
          <div className="flex items-center gap-2 mb-5">
            <div className="w-8 h-8 rounded-lg bg-violet-500/10 flex items-center justify-center">
              <Brain className="h-4 w-4 text-violet-400" />
            </div>
            <h2 className="font-semibold text-foreground">AI Exercise Generator</h2>
          </div>

          <div className="grid sm:grid-cols-3 gap-3 mb-4">
            {/* Topic */}
            <div className="sm:col-span-1">
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide block mb-1.5">Topic</label>
              <input
                value={exerciseReq.topic}
                onChange={e => setExerciseReq(p => ({ ...p, topic: e.target.value }))}
                placeholder="e.g. list comprehensions"
                className="w-full px-3.5 py-2.5 bg-muted border border-border rounded-xl text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              />
            </div>

            {/* Difficulty */}
            <div>
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide block mb-1.5">Difficulty</label>
              <select
                value={exerciseReq.difficulty}
                onChange={e => setExerciseReq(p => ({ ...p, difficulty: e.target.value as any }))}
                className="w-full px-3.5 py-2.5 bg-muted border border-border rounded-xl text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              >
                <option value="easy">Easy</option>
                <option value="medium">Medium</option>
                <option value="hard">Hard</option>
              </select>
            </div>

            {/* Count */}
            <div>
              <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide block mb-1.5">Count</label>
              <select
                value={exerciseReq.count}
                onChange={e => setExerciseReq(p => ({ ...p, count: Number(e.target.value) }))}
                className="w-full px-3.5 py-2.5 bg-muted border border-border rounded-xl text-sm text-foreground focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              >
                {[1, 2, 3, 5].map(n => <option key={n} value={n}>{n} exercise{n > 1 ? 's' : ''}</option>)}
              </select>
            </div>
          </div>

          <Button
            onClick={generateExercise}
            disabled={generating}
            className="bg-gradient-to-r from-violet-600 to-indigo-600 hover:from-violet-500 hover:to-indigo-500 text-white border-0 gap-2"
          >
            {generating
              ? <><Loader2 className="h-4 w-4 animate-spin" /> Generating…</>
              : <><Send className="h-4 w-4" /> Generate Exercises</>
            }
          </Button>

          {generatedExercise && (
            <div className="mt-4 p-4 bg-muted/50 rounded-xl border border-border">
              <p className="text-xs font-medium text-violet-400 mb-2">Generated Exercises</p>
              <pre className="text-sm text-foreground whitespace-pre-wrap font-sans leading-relaxed">{generatedExercise}</pre>
            </div>
          )}
        </div>

      </div>
    </div>
  )
}

function StatCard({ icon: Icon, label, value, sub, color, bg }: {
  icon: any; label: string; value: string; sub: string; color: string; bg: string
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
