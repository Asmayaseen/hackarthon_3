'use client'

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts'

interface ChartData {
  week: string
  mastery: number
}

interface MasteryChartProps {
  data: ChartData[]
  isLoading?: boolean
}

export default function MasteryChart({ data = [], isLoading = false }: MasteryChartProps) {
  if (isLoading) {
    return <div className="h-[300px] bg-muted rounded-lg animate-pulse" />
  }

  return (
    <ResponsiveContainer width="100%" height={300}>
      <LineChart data={data}>
        <CartesianGrid strokeDasharray="3 3" strokeOpacity={0.5} />
        <XAxis dataKey="week" />
        <YAxis />
        <Tooltip />
        <Line type="monotone" dataKey="mastery" stroke="#8884d8" strokeWidth={3} dot={{ fill: '#8884d8', strokeWidth: 2 }} />
      </LineChart>
    </ResponsiveContainer>
  )
}