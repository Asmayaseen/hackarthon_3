'use client'

import { useState, useCallback } from 'react'

interface ToastOptions {
  title?: string
  description?: string
  variant?: 'default' | 'destructive'
}

export function useToast() {
  const [toasts, setToasts] = useState<ToastOptions[]>([])

  const toast = useCallback((options: ToastOptions) => {
    setToasts((prev) => [...prev, options])
    // Auto-remove after 3s
    setTimeout(() => {
      setToasts((prev) => prev.slice(1))
    }, 3000)
  }, [])

  return { toast, toasts }
}
