'use client'

import Link from 'next/link'
import { usePathname } from 'next/navigation'
import { ThemeToggle } from '@/components/ui/theme-toggle'
import { Github, LogIn } from 'lucide-react'

export default function Navbar() {
  const pathname = usePathname()

  return (
    <nav className="sticky top-0 z-50 w-full border-b border-border bg-background/80 glass">
      <div className="max-w-7xl mx-auto px-6 h-16 flex items-center justify-between">
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2.5 group">
          <div className="w-8 h-8 rounded-lg bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center text-white font-bold text-sm shadow-lg shadow-indigo-500/30 group-hover:scale-105 transition-transform">
            L
          </div>
          <span className="font-bold text-lg text-foreground">LearnFlow</span>
        </Link>

        {/* Nav links */}
        <div className="hidden md:flex items-center gap-1">
          {[
            { href: '/', label: 'Home' },
            { href: '/dashboard', label: 'Dashboard' },
            { href: '/teacher', label: 'Teacher' },
          ].map(({ href, label }) => (
            <Link
              key={href}
              href={href}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-all ${
                pathname === href
                  ? 'bg-primary/10 text-primary'
                  : 'text-muted-foreground hover:text-foreground hover:bg-accent'
              }`}
            >
              {label}
            </Link>
          ))}
        </div>

        {/* Right side */}
        <div className="flex items-center gap-2">
          <a
            href="https://github.com/Asmayaseen/hackarthon_3"
            target="_blank"
            rel="noreferrer"
            className="w-9 h-9 rounded-lg flex items-center justify-center border border-border bg-background hover:bg-accent transition-all duration-200 hover:scale-105"
            aria-label="GitHub"
          >
            <Github className="h-4 w-4 text-muted-foreground" />
          </a>
          <Link
            href="/login"
            className="flex items-center gap-1.5 px-3 py-1.5 rounded-lg text-xs font-medium bg-primary/10 text-primary hover:bg-primary/20 transition-all"
          >
            <LogIn className="h-3.5 w-3.5" />
            Sign In
          </Link>
          <ThemeToggle />
        </div>
      </div>
    </nav>
  )
}
