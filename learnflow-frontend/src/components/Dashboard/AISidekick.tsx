'use client'

import { useState, useEffect, useRef } from 'react'
import { Button } from '@/components/ui/button'
import { MessageCircle, Send, X, Loader2, Bot, User, Sparkles } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import ReactMarkdown from 'react-markdown'

interface Message {
  role: 'user' | 'ai'
  content: string
}

interface AISidekickProps {
  struggleDetected: boolean
  studentId?: string
}

const SUGGESTIONS = [
  'How do for loops work?',
  'Explain list comprehensions',
  'What is a Python class?',
  'How do I handle errors?',
]

export default function AISidekick({ struggleDetected, studentId = 'demo-student' }: AISidekickProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')
  const [loading, setLoading] = useState(false)
  const bottomRef = useRef<HTMLDivElement>(null)
  const inputRef = useRef<HTMLInputElement>(null)

  useEffect(() => {
    if (struggleDetected && !isOpen) {
      setIsOpen(true)
      setMessages([{
        role: 'ai',
        content: "I noticed you might be having some difficulty! I'm your **AI Python Tutor**. Ask me anything — I'm here to help you understand Python concepts clearly. 🐍",
      }])
    }
  }, [struggleDetected])

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: 'smooth' })
  }, [messages, loading])

  useEffect(() => {
    if (isOpen) setTimeout(() => inputRef.current?.focus(), 300)
  }, [isOpen])

  const sendMessage = async (text: string) => {
    if (!text.trim() || loading) return
    const userMsg: Message = { role: 'user', content: text }
    setMessages(prev => [...prev, userMsg])
    setInput('')
    setLoading(true)

    try {
      const history = messages.map(m => ({
        role: m.role === 'ai' ? 'assistant' : 'user',
        content: m.content,
      }))
      const res = await fetch('/api/chat', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ message: text, student_id: studentId, history }),
      })
      const data = await res.json()
      setMessages(prev => [...prev, { role: 'ai', content: data.reply }])
    } catch {
      setMessages(prev => [...prev, { role: 'ai', content: "Sorry, I couldn't connect. Please try again." }])
    } finally {
      setLoading(false)
    }
  }

  return (
    <>
      {/* Floating button */}
      <motion.button
        initial={{ scale: 0, opacity: 0 }}
        animate={{ scale: 1, opacity: 1 }}
        transition={{ type: 'spring', stiffness: 400, damping: 20, delay: 0.5 }}
        onClick={() => setIsOpen(o => !o)}
        className="fixed bottom-6 right-6 z-50 w-14 h-14 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 text-white shadow-2xl shadow-indigo-500/40 flex items-center justify-center hover:scale-110 transition-transform"
        aria-label="AI Tutor Chat"
      >
        <AnimatePresence mode="wait">
          {isOpen
            ? <motion.div key="x" initial={{ rotate: -90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: 90, opacity: 0 }} transition={{ duration: 0.15 }}><X className="h-5 w-5" /></motion.div>
            : <motion.div key="chat" initial={{ rotate: 90, opacity: 0 }} animate={{ rotate: 0, opacity: 1 }} exit={{ rotate: -90, opacity: 0 }} transition={{ duration: 0.15 }}><MessageCircle className="h-5 w-5" /></motion.div>
          }
        </AnimatePresence>
      </motion.button>

      {/* Chat panel */}
      <AnimatePresence>
        {isOpen && (
          <motion.div
            initial={{ opacity: 0, y: 16, scale: 0.96 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 16, scale: 0.96 }}
            transition={{ type: 'spring', stiffness: 320, damping: 28 }}
            className="fixed bottom-24 right-6 z-50 w-[92vw] sm:w-[400px] max-h-[75vh] sm:max-h-[560px] flex flex-col rounded-2xl border border-border bg-card shadow-2xl shadow-black/20 overflow-hidden"
          >
            {/* Header */}
            <div className="flex items-center justify-between px-4 py-3 border-b border-border bg-gradient-to-r from-indigo-500/10 to-purple-500/10">
              <div className="flex items-center gap-2.5">
                <div className="w-8 h-8 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center">
                  <Bot className="h-4 w-4 text-white" />
                </div>
                <div>
                  <p className="text-sm font-semibold text-foreground">AI Python Tutor</p>
                  <div className="flex items-center gap-1">
                    <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse" />
                    <span className="text-xs text-muted-foreground">Online</span>
                  </div>
                </div>
              </div>
              <button
                onClick={() => setIsOpen(false)}
                className="w-7 h-7 rounded-lg flex items-center justify-center text-muted-foreground hover:text-foreground hover:bg-accent transition-all"
              >
                <X className="h-4 w-4" />
              </button>
            </div>

            {/* Messages */}
            <div className="flex-1 overflow-y-auto p-4 space-y-3">
              {messages.length === 0 && (
                <div className="text-center py-6 space-y-3">
                  <div className="w-12 h-12 rounded-2xl bg-gradient-to-br from-indigo-500/20 to-purple-500/20 flex items-center justify-center mx-auto">
                    <Sparkles className="h-6 w-6 text-primary" />
                  </div>
                  <p className="text-sm text-muted-foreground">Ask me anything about Python!</p>
                  <div className="flex flex-wrap gap-2 justify-center">
                    {SUGGESTIONS.map(s => (
                      <button
                        key={s}
                        onClick={() => sendMessage(s)}
                        className="px-3 py-1.5 text-xs bg-muted hover:bg-accent border border-border rounded-full text-foreground transition-colors"
                      >
                        {s}
                      </button>
                    ))}
                  </div>
                </div>
              )}

              {messages.map((msg, idx) => (
                <div key={idx} className={`flex gap-2.5 ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
                  {msg.role === 'ai' && (
                    <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shrink-0 mt-0.5">
                      <Bot className="h-3.5 w-3.5 text-white" />
                    </div>
                  )}
                  <div className={`max-w-[80%] px-3.5 py-2.5 rounded-2xl text-sm leading-relaxed ${
                    msg.role === 'ai'
                      ? 'bg-muted text-foreground rounded-tl-sm'
                      : 'bg-primary text-primary-foreground rounded-tr-sm'
                  }`}>
                    {msg.role === 'ai' ? (
                      <div className="prose prose-sm dark:prose-invert max-w-none prose-p:my-1 prose-headings:my-1 prose-pre:my-1 prose-code:text-indigo-400">
                        <ReactMarkdown>{msg.content}</ReactMarkdown>
                      </div>
                    ) : msg.content}
                  </div>
                  {msg.role === 'user' && (
                    <div className="w-7 h-7 rounded-full bg-secondary border border-border flex items-center justify-center shrink-0 mt-0.5">
                      <User className="h-3.5 w-3.5 text-muted-foreground" />
                    </div>
                  )}
                </div>
              ))}

              {loading && (
                <div className="flex gap-2.5 items-center">
                  <div className="w-7 h-7 rounded-full bg-gradient-to-br from-indigo-500 to-purple-600 flex items-center justify-center shrink-0">
                    <Bot className="h-3.5 w-3.5 text-white" />
                  </div>
                  <div className="bg-muted px-4 py-3 rounded-2xl rounded-tl-sm">
                    <div className="flex gap-1">
                      <span className="w-2 h-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '0ms' }} />
                      <span className="w-2 h-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '150ms' }} />
                      <span className="w-2 h-2 rounded-full bg-muted-foreground/50 animate-bounce" style={{ animationDelay: '300ms' }} />
                    </div>
                  </div>
                </div>
              )}
              <div ref={bottomRef} />
            </div>

            {/* Input */}
            <div className="p-3 border-t border-border bg-card">
              <div className="flex gap-2 items-center">
                <input
                  ref={inputRef}
                  value={input}
                  onChange={e => setInput(e.target.value)}
                  onKeyDown={e => e.key === 'Enter' && !e.shiftKey && sendMessage(input)}
                  placeholder="Ask about Python..."
                  disabled={loading}
                  className="flex-1 px-3.5 py-2.5 bg-muted border border-border text-foreground placeholder:text-muted-foreground rounded-xl text-sm focus:outline-none focus:ring-2 focus:ring-ring focus:border-transparent transition-all"
                />
                <Button
                  size="sm"
                  onClick={() => sendMessage(input)}
                  disabled={!input.trim() || loading}
                  className="w-10 h-10 p-0 rounded-xl bg-gradient-to-br from-indigo-600 to-purple-600 hover:from-indigo-500 hover:to-purple-500 text-white border-0 shrink-0"
                >
                  <Send className="h-4 w-4" />
                </Button>
              </div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </>
  )
}
