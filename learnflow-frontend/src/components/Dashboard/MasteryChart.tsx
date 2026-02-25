'use client'

import {
  AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
} from 'recharts'
import { useTheme } from 'next-themes'

interface ChartData { week: string; mastery: number }

export default function MasteryChart({ data = [], isLoading = false }: { data: ChartData[]; isLoading?: boolean }) {
  const { resolvedTheme } = useTheme()
  const isDark = resolvedTheme === 'dark'

  if (isLoading) return <div className="h-[280px] bg-muted rounded-xl animate-pulse" />

  const gridColor = isDark ? '#1e293b' : '#e2e8f0'
  const textColor = isDark ? '#94a3b8' : '#64748b'
  const tooltipBg = isDark ? '#0f172a' : '#ffffff'
  const tooltipBorder = isDark ? '#1e293b' : '#e2e8f0'

  return (
    <ResponsiveContainer width="100%" height={280}>
      <AreaChart data={data} margin={{ top: 5, right: 10, left: -20, bottom: 0 }}>
        <defs>
          <linearGradient id="masteryGrad" x1="0" y1="0" x2="0" y2="1">
            <stop offset="5%" stopColor="#6366f1" stopOpacity={0.3} />
            <stop offset="95%" stopColor="#6366f1" stopOpacity={0} />
          </linearGradient>
        </defs>
        <CartesianGrid strokeDasharray="3 3" stroke={gridColor} vertical={false} />
        <XAxis
          dataKey="week"
          tick={{ fill: textColor, fontSize: 11 }}
          axisLine={false}
          tickLine={false}
          tickFormatter={v => v.replace(/ \(.*\)/, '')}
        />
        <YAxis
          tick={{ fill: textColor, fontSize: 11 }}
          axisLine={false}
          tickLine={false}
          domain={[0, 100]}
          tickFormatter={v => `${v}%`}
        />
        <Tooltip
          contentStyle={{
            background: tooltipBg,
            border: `1px solid ${tooltipBorder}`,
            borderRadius: 8,
            color: isDark ? '#f1f5f9' : '#0f172a',
            fontSize: 12,
          }}
          formatter={(value: number | undefined): [string, string] => [`${value ?? 0}%`, 'Mastery']}
        />
        <Area
          type="monotone"
          dataKey="mastery"
          stroke="#6366f1"
          strokeWidth={2.5}
          fill="url(#masteryGrad)"
          dot={{ fill: '#6366f1', strokeWidth: 0, r: 4 }}
          activeDot={{ r: 6, fill: '#6366f1', strokeWidth: 0 }}
        />
      </AreaChart>
    </ResponsiveContainer>
  )
}
