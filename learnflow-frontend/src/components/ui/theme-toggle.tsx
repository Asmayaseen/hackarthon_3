'use client'

import { useTheme } from 'next-themes'
import { Sun, Moon } from 'lucide-react'
import { useEffect, useState } from 'react'

export function ThemeToggle() {
  const { theme, setTheme } = useTheme()
  const [mounted, setMounted] = useState(false)

  useEffect(() => {
    // eslint-disable-next-line react-hooks/set-state-in-effect
    setMounted(true)
  }, [])
  if (!mounted) return <div className="w-9 h-9" />

  return (
    <button
      onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
      className="w-9 h-9 rounded-lg flex items-center justify-center border border-border bg-background hover:bg-accent transition-all duration-200 hover:scale-105"
      aria-label="Toggle theme"
    >
      {theme === 'dark'
        ? <Sun className="h-4 w-4 text-yellow-400" />
        : <Moon className="h-4 w-4 text-slate-700" />
      }
    </button>
  )
}
