import Link from 'next/link'
import Navbar from '@/components/Navbar'
import {
  Bot, Code2, BarChart3, BookOpen, Bug, CheckCircle2,
  Zap, Shield, Globe, ArrowRight, Github, Layers
} from 'lucide-react'

const features = [
  {
    icon: Bot,
    title: 'AI Python Tutor',
    desc: 'Real-time answers from Groq-powered AI. Ask anything about Python — loops, OOP, debugging — and get clear explanations instantly.',
    color: 'from-blue-500 to-cyan-500',
    bg: 'bg-blue-500/10 dark:bg-blue-500/10',
  },
  {
    icon: Code2,
    title: 'Live Code Editor',
    desc: 'Monaco-powered Python editor with syntax highlighting, run code in a secure sandbox, and get instant output.',
    color: 'from-violet-500 to-purple-600',
    bg: 'bg-violet-500/10',
  },
  {
    icon: BarChart3,
    title: 'Progress Tracking',
    desc: 'Visual mastery charts showing your progress across 8 Python modules. See exactly where you excel and where to focus.',
    color: 'from-emerald-500 to-teal-500',
    bg: 'bg-emerald-500/10',
  },
  {
    icon: BookOpen,
    title: 'Smart Quizzes',
    desc: 'Auto-graded multiple-choice quizzes that adapt to your level. Struggle detection activates AI help when you need it most.',
    color: 'from-orange-500 to-amber-500',
    bg: 'bg-orange-500/10',
  },
  {
    icon: Bug,
    title: 'Debug Assistant',
    desc: 'Paste your error message and get a step-by-step debug walkthrough. Understand the root cause, not just the fix.',
    color: 'from-red-500 to-rose-500',
    bg: 'bg-red-500/10',
  },
  {
    icon: CheckCircle2,
    title: 'Code Review',
    desc: 'AI reviews your code for PEP 8 compliance, logic errors, efficiency improvements, and readability — like having a senior dev mentor.',
    color: 'from-pink-500 to-fuchsia-500',
    bg: 'bg-pink-500/10',
  },
]

const stack = [
  { label: 'Next.js 16', color: 'bg-black dark:bg-white/10 text-white' },
  { label: 'FastAPI', color: 'bg-teal-600/20 text-teal-400' },
  { label: 'Dapr', color: 'bg-blue-600/20 text-blue-400' },
  { label: 'Kafka', color: 'bg-orange-600/20 text-orange-400' },
  { label: 'Groq AI', color: 'bg-violet-600/20 text-violet-400' },
  { label: 'Neon PostgreSQL', color: 'bg-emerald-600/20 text-emerald-400' },
  { label: 'Kubernetes', color: 'bg-blue-600/20 text-blue-300' },
  { label: 'Monaco Editor', color: 'bg-indigo-600/20 text-indigo-400' },
]

const services = [
  { name: 'Triage Agent', desc: 'Routes queries to the right specialist', port: '8080' },
  { name: 'Concepts Agent', desc: 'Explains Python concepts adaptively', port: '8001' },
  { name: 'Debug Agent', desc: 'Parses errors and provides hints', port: '8002' },
  { name: 'Code Review', desc: 'PEP 8, logic, efficiency analysis', port: '8003' },
  { name: 'Exercise Agent', desc: 'Generates & auto-grades challenges', port: '8004' },
  { name: 'Progress Agent', desc: 'Mastery scores & struggle detection', port: '8005' },
]

export default function Home() {
  return (
    <div className="min-h-screen bg-background">
      <Navbar />

      {/* ── Hero ──────────────────────────────────────── */}
      <section className="relative overflow-hidden pt-20 pb-32 px-6">
        {/* Background blobs */}
        <div className="absolute inset-0 -z-10 overflow-hidden">
          <div className="absolute top-0 left-1/4 w-96 h-96 bg-indigo-500/20 rounded-full blur-3xl" />
          <div className="absolute top-10 right-1/4 w-72 h-72 bg-purple-500/20 rounded-full blur-3xl" />
          <div className="absolute bottom-0 left-1/2 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl" />
        </div>

        <div className="max-w-5xl mx-auto text-center space-y-8">
          {/* Badge */}
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-indigo-500/30 bg-indigo-500/10 text-indigo-400 text-sm font-medium">
            <Zap className="h-3.5 w-3.5" />
            Hackathon III — Reusable Intelligence & Cloud-Native Mastery
          </div>

          {/* Headline */}
          <h1 className="text-5xl md:text-7xl font-extrabold tracking-tight leading-tight">
            <span className="text-foreground">Learn Python with</span>
            <br />
            <span className="gradient-text">AI-Powered Tutors</span>
          </h1>

          {/* Sub */}
          <p className="text-xl text-muted-foreground max-w-2xl mx-auto leading-relaxed">
            LearnFlow is a multi-agent AI tutoring platform built on
            FastAPI, Dapr, Kafka, and Kubernetes. Chat with specialized AI agents,
            write and run code live, take quizzes, and track your mastery — all in one place.
          </p>

          {/* CTAs */}
          <div className="flex justify-center pt-2">
            <Link
              href="/dashboard"
              className="group inline-flex items-center gap-2 px-10 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold rounded-xl shadow-xl shadow-indigo-500/30 transition-all hover:scale-105 hover:shadow-indigo-500/50"
            >
              Start Learning
              <ArrowRight className="h-4 w-4 group-hover:translate-x-1 transition-transform" />
            </Link>
            <a
              href="https://github.com/Asmayaseen/hackarthon_3"
              target="_blank"
              rel="noreferrer"
              className="hidden inline-flex items-center gap-2 px-8 py-4 bg-card border border-border text-foreground font-semibold rounded-xl hover:border-indigo-500/50 hover:bg-accent transition-all hover:scale-105"
            >
              <Github className="h-4 w-4" />
              View Source
            </a>
          </div>

          {/* Stats */}
          <div className="flex flex-wrap gap-8 justify-center pt-6 text-center">
            {[['6', 'AI Microservices'], ['7', 'Claude Skills'], ['8', 'Python Modules'], ['∞', 'Code Executions']].map(([num, lbl]) => (
              <div key={lbl}>
                <p className="text-3xl font-bold gradient-text">{num}</p>
                <p className="text-sm text-muted-foreground">{lbl}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Features ──────────────────────────────────── */}
      <section className="py-24 px-6 bg-muted/30">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 space-y-4">
            <p className="text-sm font-semibold text-primary uppercase tracking-widest">Features</p>
            <h2 className="text-4xl font-bold text-foreground">Everything you need to master Python</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">Six specialized AI agents working together to give you the best learning experience.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-6">
            {features.map(({ icon: Icon, title, desc, color, bg }) => (
              <div
                key={title}
                className="group p-6 rounded-2xl border border-border bg-card hover:border-primary/40 hover:shadow-xl hover:shadow-primary/5 transition-all duration-300 hover:-translate-y-1"
              >
                <div className={`w-12 h-12 rounded-xl ${bg} flex items-center justify-center mb-4 group-hover:scale-110 transition-transform`}>
                  <div className={`bg-gradient-to-br ${color} rounded-lg w-7 h-7 flex items-center justify-center`}>
                    <Icon className="h-4 w-4 text-white" />
                  </div>
                </div>
                <h3 className="font-semibold text-foreground mb-2">{title}</h3>
                <p className="text-sm text-muted-foreground leading-relaxed">{desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* ── Architecture ──────────────────────────────── */}
      <section className="py-24 px-6">
        <div className="max-w-6xl mx-auto">
          <div className="text-center mb-16 space-y-4">
            <p className="text-sm font-semibold text-primary uppercase tracking-widest">Architecture</p>
            <h2 className="text-4xl font-bold text-foreground">6 Microservices, 1 Platform</h2>
            <p className="text-muted-foreground max-w-xl mx-auto">Event-driven architecture with Kafka pub/sub and Dapr service mesh running on Kubernetes.</p>
          </div>

          <div className="grid md:grid-cols-3 gap-4">
            {services.map(({ name, desc, port }) => (
              <div key={name} className="p-5 rounded-xl border border-border bg-card hover:border-primary/30 transition-all group">
                <div className="flex items-start justify-between mb-3">
                  <div className="w-8 h-8 rounded-lg bg-primary/10 flex items-center justify-center">
                    <Layers className="h-4 w-4 text-primary" />
                  </div>
                  <span className="text-xs font-mono text-muted-foreground bg-muted px-2 py-0.5 rounded">:{port}</span>
                </div>
                <h3 className="font-semibold text-foreground text-sm mb-1">{name}</h3>
                <p className="text-xs text-muted-foreground">{desc}</p>
              </div>
            ))}
          </div>

          {/* Kafka event flow */}
          <div className="mt-8 p-6 rounded-2xl border border-border bg-card">
            <p className="text-xs font-semibold text-muted-foreground uppercase tracking-widest mb-4">Kafka Event Topics</p>
            <div className="flex flex-wrap gap-2">
              {['learning.query.explain', 'learning.query.routed', 'code.debug.request', 'code.review.request', 'exercise.generate', 'progress.summary', 'struggle.alert'].map(t => (
                <span key={t} className="px-3 py-1 text-xs font-mono bg-muted text-muted-foreground rounded-full border border-border hover:border-primary/40 transition-colors">
                  {t}
                </span>
              ))}
            </div>
          </div>
        </div>
      </section>

      {/* ── Tech Stack ────────────────────────────────── */}
      <section className="py-20 px-6 bg-muted/30">
        <div className="max-w-4xl mx-auto text-center space-y-10">
          <div className="space-y-4">
            <p className="text-sm font-semibold text-primary uppercase tracking-widest">Tech Stack</p>
            <h2 className="text-3xl font-bold text-foreground">Built with modern cloud-native tools</h2>
          </div>
          <div className="flex flex-wrap gap-3 justify-center">
            {stack.map(({ label, color }) => (
              <span key={label} className={`px-4 py-2 rounded-full text-sm font-medium ${color} border border-border`}>
                {label}
              </span>
            ))}
          </div>
        </div>
      </section>

      {/* ── CTA ───────────────────────────────────────── */}
      <section className="py-24 px-6">
        <div className="max-w-3xl mx-auto text-center space-y-8">
          <div className="inline-flex items-center gap-2 px-4 py-1.5 rounded-full border border-emerald-500/30 bg-emerald-500/10 text-emerald-400 text-sm">
            <Shield className="h-3.5 w-3.5" />
            Running live on localhost:3000
          </div>
          <h2 className="text-4xl font-bold text-foreground">Ready to start learning?</h2>
          <p className="text-muted-foreground text-lg">Jump into the dashboard and start your Python journey with your personal AI tutor.</p>
          <Link
            href="/dashboard"
            className="inline-flex items-center gap-2 px-10 py-4 bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white font-semibold rounded-xl shadow-xl shadow-indigo-500/30 transition-all hover:scale-105"
          >
            Open Dashboard
            <ArrowRight className="h-4 w-4" />
          </Link>
        </div>
      </section>

      {/* ── Footer ────────────────────────────────────── */}
      <footer className="border-t border-border py-8 px-6">
        <div className="max-w-6xl mx-auto flex flex-col md:flex-row items-center justify-between gap-4 text-sm text-muted-foreground">
          <div className="flex items-center gap-2">
            <div className="w-6 h-6 rounded bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white text-xs font-bold">L</div>
            <span>LearnFlow — Hackathon III</span>
          </div>
          <div className="flex items-center gap-2">
            <Globe className="h-4 w-4" />
            <span>Built with Claude Code · Spec-Driven Development</span>
          </div>
          <a href="https://github.com/Asmayaseen/hackarthon_3" target="_blank" rel="noreferrer" className="flex items-center gap-1 hover:text-foreground transition-colors">
            <Github className="h-4 w-4" />
            GitHub
          </a>
        </div>
      </footer>
    </div>
  )
}
