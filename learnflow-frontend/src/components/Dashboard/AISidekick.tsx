'use client'

import { useState, useEffect } from 'react'
import { Button } from '@/components/ui/button'
import { MessageCircle, Send } from 'lucide-react'
import { motion, AnimatePresence } from 'framer-motion'
import { toast } from 'sonner'

interface Message {
  role: 'user' | 'ai'
  content: string
}

interface AISidekickProps {
  struggleDetected: boolean
}

export default function AISidekick({ struggleDetected }: AISidekickProps) {
  const [isOpen, setIsOpen] = useState(false)
  const [messages, setMessages] = useState<Message[]>([])
  const [input, setInput] = useState('')

  useEffect(() => {
    if (struggleDetected && !isOpen) {
      setIsOpen(true)
      setMessages([
        {
          role: 'ai',
          content: "I see you're stuck on Loops. Want a hint?"
        }
      ])
    }
  }, [struggleDetected])

  const handleSend = () => {
    if (!input.trim()) return

    const userMsg: Message = { role: 'user', content: input }
    setMessages(prev => [...prev, userMsg])
    setInput('')

    // Mock AI response
    setTimeout(() => {
      const aiMsg: Message = { role: 'ai', content: 'For loops in Python: for i in range(5): print(i). Try iterating over your list!' }
      setMessages(prev => [...prev, aiMsg])
    }, 1000)
  }

  return (
    <>
      <motion.div
        className="fixed bottom-6 right-6 z-50"
        initial={{ scale: 0 }}
        animate={{ scale: 1 }}
        transition={{ type: 'spring', stiffness: 400, damping: 20 }}
      >
        <Button
          size="lg"
          className="w-14 h-14 rounded-full p-0 shadow-2xl bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700"
          onClick={() => setIsOpen(true)}
        >
          <MessageCircle className="h-6 w-6" />
        </Button>
      </motion.div>

      <AnimatePresence>
        {isOpen && (
          <motion.div
            className="fixed bottom-24 right-6 w-80 max-h-[500px] bg-white/90 backdrop-blur-md border border-white/20 rounded-2xl shadow-2xl overflow-hidden flex flex-col z-50"
            initial={{ opacity: 0, y: 20, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: 20, scale: 0.95 }}
            transition={{ type: 'spring', stiffness: 300, damping: 25 }}
          >
            <div className="p-4 border-b border-gray-100 bg-gradient-to-r from-blue-50 to-purple-50">
              <h3 className="font-semibold text-gray-900 flex items-center gap-2">
                AI Sidekick
              </h3>
              <Button
                variant="ghost"
                size="sm"
                className="h-6 px-2 mt-1 -ml-2 text-xs"
                onClick={() => setIsOpen(false)}
              >
                Close
              </Button>
            </div>

            <div className="flex-1 p-4 overflow-y-auto space-y-3">
              {messages.map((msg, idx) => (
                <div
                  key={idx}
                  className={`flex ${msg.role === 'ai' ? 'justify-start' : 'justify-end'}`}
                >
                  <div
                    className={`max-w-[80%] p-3 rounded-2xl ${
                      msg.role === 'ai'
                        ? 'bg-blue-100 text-blue-900'
                        : 'bg-purple-500 text-white'
                    }`}
                  >
                    {msg.content}
                  </div>
                </div>
              ))}
            </div>

            <div className="p-4 border-t border-gray-100 bg-white">
              <div className="flex gap-2">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask AI Sidekick..."
                  className="flex-1 px-3 py-2 border border-gray-200 rounded-xl focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-transparent"
                  onKeyDown={(e) => e.key === 'Enter' && handleSend()}
                />
                <Button
                  size="sm"
                  onClick={handleSend}
                  disabled={!input.trim()}
                  className="px-4"
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