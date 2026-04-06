'use client'

import { useEffect, useState } from 'react'

function formatTime(date: Date, tz: string): string {
  return date.toLocaleTimeString('en-US', {
    timeZone: tz,
    hour: '2-digit',
    minute: '2-digit',
    second: '2-digit',
    hour12: false,
  })
}

function formatDate(date: Date, tz: string): string {
  return date.toLocaleDateString('en-US', {
    timeZone: tz,
    weekday: 'short',
    month: 'short',
    day: 'numeric',
  })
}

export default function LiveClock() {
  const [now, setNow] = useState<Date | null>(null)

  useEffect(() => {
    setNow(new Date())
    const id = setInterval(() => setNow(new Date()), 1000)
    return () => clearInterval(id)
  }, [])

  if (!now) return null

  return (
    <div className="flex items-center gap-6 px-4 py-2.5 bg-gray-800 border border-gray-700 rounded-xl w-fit text-sm mb-6">
      <span className="w-2 h-2 rounded-full bg-green-400 animate-pulse shrink-0" />
      <div className="flex items-baseline gap-2">
        <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">NYC</span>
        <span className="font-mono font-medium text-white tabular-nums">{formatTime(now, 'America/New_York')}</span>
        <span className="font-mono text-xs text-gray-400">{formatDate(now, 'America/New_York')}</span>
      </div>
      <div className="w-px h-7 bg-gray-600" />
      <div className="flex items-baseline gap-2">
        <span className="text-xs font-medium text-gray-400 uppercase tracking-wider">UTC</span>
        <span className="font-mono font-medium text-white tabular-nums">{formatTime(now, 'UTC')}</span>
        <span className="font-mono text-xs text-gray-400">{formatDate(now, 'UTC')}</span>
      </div>
    </div>
  )
}
