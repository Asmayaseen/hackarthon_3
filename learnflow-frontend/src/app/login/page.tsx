'use client'

import { useState } from 'react'
import Link from 'next/link'
import { useRouter } from 'next/navigation'
import { Button } from '@/components/ui/button'
import { Loader2, Brain, Eye, EyeOff } from 'lucide-react'
import { toast } from 'sonner'
import { ThemeToggle } from '@/components/ui/theme-toggle'

export default function LoginPage() {
  const router = useRouter()
  const [role, setRole] = useState<'student' | 'teacher'>('student')
  const [email, setEmail] = useState('')
  const [password, setPassword] = useState('')
  const [showPw, setShowPw] = useState(false)
  const [loading, setLoading] = useState(false)

  const DEMO_CREDENTIALS = {
    student: { email: 'maya@learnflow.ai', password: 'demo123' },
    teacher: { email: 'rodriguez@learnflow.ai', password: 'demo123' },
  }

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault()
    setLoading(true)
    // Simulate auth — replace with Better Auth integration
    await new Promise(r => setTimeout(r, 800))
    const demo = DEMO_CREDENTIALS[role]
    if (email === demo.email && password === demo.password) {
      toast.success(`Welcome back! Redirecting…`)
      setTimeout(() => router.push(role === 'teacher' ? '/teacher' : '/dashboard'), 500)
    } else {
      toast.error('Invalid credentials. Use the demo button to auto-fill.')
    }
    setLoading(false)
  }

  const fillDemo = () => {
    const creds = DEMO_CREDENTIALS[role]
    setEmail(creds.email)
    setPassword(creds.password)
  }

  return (
    <div className="min-h-screen bg-background flex flex-col items-center justify-center px-4">
      {/* Header */}
      <div className="absolute top-4 right-4">
        <ThemeToggle />
      </div>

      {/* Logo */}
      <Link href="/" className="flex items-center gap-2.5 mb-8 group">
        <div className="w-9 h-9 rounded-xl bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shadow-lg shadow-indigo-500/30">
          <Brain className="h-5 w-5 text-white" />
        </div>
        <span className="text-xl font-bold text-foreground">LearnFlow</span>
      </Link>

      {/* Card */}
      <div className="w-full max-w-sm bg-card border border-border rounded-2xl p-8 shadow-xl shadow-black/10">
        <h1 className="text-xl font-semibold text-foreground text-center mb-1">Welcome back</h1>
        <p className="text-sm text-muted-foreground text-center mb-6">Sign in to your LearnFlow account</p>

        {/* Role toggle */}
        <div className="flex items-center gap-1 p-1 bg-muted rounded-xl mb-6">
          {(['student', 'teacher'] as const).map(r => (
            <button
              key={r}
              onClick={() => setRole(r)}
              className={`flex-1 py-2 rounded-lg text-sm font-medium capitalize transition-all ${
                role === r
                  ? 'bg-background text-foreground shadow-sm border border-border'
                  : 'text-muted-foreground hover:text-foreground'
              }`}
            >
              {r}
            </button>
          ))}
        </div>

        <form onSubmit={handleLogin} className="space-y-4">
          {/* Email */}
          <div className="space-y-1.5">
            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Email</label>
            <input
              type="email"
              value={email}
              onChange={e => setEmail(e.target.value)}
              required
              placeholder={DEMO_CREDENTIALS[role].email}
              className="w-full px-3.5 py-2.5 bg-muted border border-border rounded-xl text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-ring transition-all"
            />
          </div>

          {/* Password */}
          <div className="space-y-1.5">
            <label className="text-xs font-medium text-muted-foreground uppercase tracking-wide">Password</label>
            <div className="relative">
              <input
                type={showPw ? 'text' : 'password'}
                value={password}
                onChange={e => setPassword(e.target.value)}
                required
                placeholder="••••••••"
                className="w-full px-3.5 py-2.5 pr-10 bg-muted border border-border rounded-xl text-sm text-foreground placeholder:text-muted-foreground/50 focus:outline-none focus:ring-2 focus:ring-ring transition-all"
              />
              <button
                type="button"
                onClick={() => setShowPw(v => !v)}
                className="absolute right-3 top-1/2 -translate-y-1/2 text-muted-foreground hover:text-foreground"
              >
                {showPw ? <EyeOff className="h-4 w-4" /> : <Eye className="h-4 w-4" />}
              </button>
            </div>
          </div>

          <Button
            type="submit"
            disabled={loading}
            className="w-full bg-gradient-to-r from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white border-0 h-10"
          >
            {loading ? <Loader2 className="h-4 w-4 animate-spin mr-2" /> : null}
            Sign In
          </Button>
        </form>

        {/* Demo shortcut */}
        <button
          onClick={fillDemo}
          className="w-full mt-3 py-2 text-xs text-muted-foreground hover:text-foreground border border-dashed border-border rounded-xl hover:border-primary/40 transition-all"
        >
          Fill demo {role} credentials
        </button>

        <p className="text-xs text-muted-foreground text-center mt-4">
          Demo: <span className="text-foreground font-mono">{DEMO_CREDENTIALS[role].email}</span> / demo123
        </p>
      </div>

      <p className="text-xs text-muted-foreground mt-6">
        Back to{' '}
        <Link href="/" className="text-primary hover:underline">home</Link>
      </p>
    </div>
  )
}
