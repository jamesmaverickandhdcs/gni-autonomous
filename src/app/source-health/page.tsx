'use client'

import { useEffect, useState } from 'react'

interface SourceRun {
  run_at: string
  article_count: number
  alert_sent: boolean
}

interface SourceStat {
  name: string
  pillar: string
  current: number
  avg: number
  status: string
  everFailed: boolean
  runs: SourceRun[]
  lastSeen: string
}

const PILLAR_CONFIG: Record<string, { label: string; color: string; emoji: string; bg: string }> = {
  geo:  { label: 'Geopolitical', color: 'text-emerald-400', emoji: '🌍', bg: 'bg-emerald-950 border-emerald-800' },
  fin:  { label: 'Financial',    color: 'text-blue-400',    emoji: '💰', bg: 'bg-blue-950 border-blue-800' },
  tech: { label: 'Technology',   color: 'text-purple-400',  emoji: '💻', bg: 'bg-purple-950 border-purple-800' },
}

const STATUS_CONFIG: Record<string, { label: string; color: string; dot: string }> = {
  healthy:  { label: 'Healthy',  color: 'text-green-400',  dot: 'bg-green-400' },
  degraded: { label: 'Degraded', color: 'text-yellow-400', dot: 'bg-yellow-400' },
  down:     { label: 'Down',     color: 'text-red-400',    dot: 'bg-red-400' },
}

function MiniChart({ runs }: { runs: SourceRun[] }) {
  if (!runs.length) return null
  const max = Math.max(...runs.map(r => r.article_count), 1)
  return (
    <div className="flex items-end gap-0.5 h-8 mt-2">
      {[...runs].reverse().map((run, i) => {
        const h = Math.max(2, (run.article_count / max) * 32)
        const col = run.alert_sent ? 'bg-red-500' :
                    run.article_count === 0 ? 'bg-red-800' :
                    run.article_count < max * 0.5 ? 'bg-yellow-500' : 'bg-green-500'
        return (
          <div key={i} className="flex-1 relative group">
            <div className="absolute bottom-full mb-1 hidden group-hover:block bg-gray-800 text-xs text-white px-1.5 py-0.5 rounded whitespace-nowrap z-10 left-1/2 -translate-x-1/2">
              {run.article_count} articles
            </div>
            <div className={`w-full rounded-sm ${col}`} style={{ height: h + 'px' }} />
          </div>
        )
      })}
    </div>
  )
}

export default function SourceHealthPage() {
  const [sources, setSources] = useState<SourceStat[]>([])
  const [loading, setLoading] = useState(true)
  const [pillarFilter, setPillarFilter] = useState('all')

  useEffect(() => {
    fetch('/api/source-health')
      .then(r => r.json())
      .then(data => setSources(data.sources || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const filtered = sources.filter(s => pillarFilter === 'all' || s.pillar === pillarFilter)
  const counts = {
    healthy:  sources.filter(s => s.status === 'healthy').length,
    degraded: sources.filter(s => s.status === 'degraded').length,
    down:     sources.filter(s => s.status === 'down').length,
  }
  const totalSources = sources.length

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">📡 Source Health Dashboard</h1>
              <p className="text-sm text-gray-400">
                Real-time RSS feed monitoring across {totalSources} intelligence sources.
              </p>
              <p className="text-xs text-gray-500 mt-1">
                Updated after every pipeline run. Admin alerted via Telegram when sources go down.
              </p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300 shrink-0">← Dashboard</a>
          </div>

          {/* Status summary */}
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-green-950 border border-green-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-green-400">{counts.healthy}</div>
              <div className="text-xs text-green-600">● Healthy</div>
            </div>
            <div className="bg-yellow-950 border border-yellow-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-yellow-400">{counts.degraded}</div>
              <div className="text-xs text-yellow-600">◐ Degraded</div>
            </div>
            <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-red-400">{counts.down}</div>
              <div className="text-xs text-red-600">○ Down</div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* Pillar filter */}
        <div className="flex gap-2 mb-6">
          {['all', 'geo', 'fin', 'tech'].map(p => (
            <button key={p} onClick={() => setPillarFilter(p)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                pillarFilter === p ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}>
              {p === 'all' ? 'All Sources' :
               PILLAR_CONFIG[p]?.emoji + ' ' + PILLAR_CONFIG[p]?.label}
            </button>
          ))}
        </div>

        {loading && <div className="text-center py-20 text-gray-400">Loading source health...</div>}

        {!loading && sources.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">📡</div>
            <p>No health data yet. Run the pipeline to start tracking.</p>
          </div>
        )}

        {/* Source grid */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {filtered.map(src => {
            const status = STATUS_CONFIG[src.status] || STATUS_CONFIG.healthy
            const pillar = PILLAR_CONFIG[src.pillar] || PILLAR_CONFIG.geo
            return (
              <div key={src.name}
                className={`bg-gray-900 border rounded-xl p-4 ${
                  src.status === 'down' ? 'border-red-800' :
                  src.status === 'degraded' ? 'border-yellow-800' : 'border-gray-700'
                }`}>
                <div className="flex items-start justify-between mb-2">
                  <div className="flex items-center gap-2">
                    <div className={`w-2 h-2 rounded-full ${status.dot} shrink-0 mt-0.5`} />
                    <span className="text-sm font-bold text-white">{src.name}</span>
                  </div>
                  <div className="flex items-center gap-2 shrink-0">
                    <span className={`text-xs ${pillar.color}`}>{pillar.emoji}</span>
                    {src.everFailed && (
                      <span className="text-xs bg-orange-900 text-orange-300 px-1.5 py-0.5 rounded">
                        ⚠ History
                      </span>
                    )}
                  </div>
                </div>

                <div className="grid grid-cols-3 gap-2 text-xs mb-2">
                  <div className="bg-gray-800 rounded p-2 text-center">
                    <div className={`text-lg font-bold ${status.color}`}>{src.current}</div>
                    <div className="text-gray-500">Current</div>
                  </div>
                  <div className="bg-gray-800 rounded p-2 text-center">
                    <div className="text-lg font-bold text-gray-300">{src.avg}</div>
                    <div className="text-gray-500">Avg</div>
                  </div>
                  <div className="bg-gray-800 rounded p-2 text-center">
                    <div className={`text-xs font-bold ${status.color}`}>{status.label}</div>
                    <div className="text-gray-500 text-xs">Status</div>
                  </div>
                </div>

                <MiniChart runs={src.runs} />

                <div className="text-xs text-gray-600 mt-2">
                  Last updated: {src.lastSeen ? new Date(src.lastSeen).toLocaleString() : 'Never'}
                </div>
              </div>
            )
          })}
        </div>

        {/* Legend */}
        <div className="mt-8 bg-gray-900 border border-gray-700 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">How Source Health Works</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-green-400 font-bold mb-1">● Healthy</div>
              <p className="text-gray-400">Source is returning articles at or above its rolling average. No action needed.</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-yellow-400 font-bold mb-1">◐ Degraded</div>
              <p className="text-gray-400">Source is returning fewer than 50% of its average articles. Monitor closely.</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-red-400 font-bold mb-1">○ Down</div>
              <p className="text-gray-400">Source returned 0 articles. Admin alerted via Telegram. RSS URL may have changed.</p>
            </div>
          </div>
          <div className="mt-3 text-xs text-gray-600">
            Mini chart: last 10 runs. Green = healthy, Yellow = degraded, Red = down, Dark red = 0 articles.
            ⚠ History badge = source has gone down at least once.
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights | Source Health Dashboard | 25 RSS sources monitored
        </div>
      </footer>
    </div>
  )
}
