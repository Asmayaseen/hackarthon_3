'use client'

import useSWR from 'swr'

const API_BASE = '/api'

interface ProgressData {
  history: Array<{ week: string; mastery: number }>
  struggleDetected: boolean
}

const fetcher = (url: string) => fetch(url).then((res) => res.json())

export function useProgress(studentId: string = 'demo-student') {
  const { data, error, isLoading, mutate } = useSWR<ProgressData, Error>(
    `${API_BASE}/progress/${studentId}`,
    fetcher,
    {
      refreshInterval: 5000, // Poll every 5s
      revalidateOnFocus: true,
      revalidateOnReconnect: true,
    }
  )

  return {
    data: data?.history || [],
    struggleDetected: data?.struggleDetected || false,
    isLoading,
    error,
    mutate,
  }
}