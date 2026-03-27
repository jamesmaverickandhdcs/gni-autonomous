'use client'
import { useEffect, useState } from 'react'

interface Usage {
  pipeline: string
  tokens_used: number
  requests_used: number
  created_at: string
}

const DAILY_LIMIT = 100000
const SAFE_CEILING = 85000
const PIPELINE_COLORS: Record<string, string> = {
  gni_pipeline: 'bg-blue-500',
  gni_mad: 'bg-purple-500',
  gni_adaptive: 'bg-orange-500',
  gni_heartbeat: 'bg-green-500',
}
const PIPELINE_TEXT: Record<string, string> = {
  gni_pipeline: 'text-blue-400',
  gni_mad: 'text-purple-400',
  gni_adaptive: 'text-orange-400',
  gni_heartbeat: 'text-green-400',
}

export default function QuotaPage() {
  const [usage, setUsage] = useState<Usage[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/quota')
      .then(r => r.json())
      .then(data => setUsage(data.usage || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const today = new Date().toISOString().slice(0, 10)
  const todayUsage = usage.filter(u => u.created_at.startsWith(today))
  const todayTokens = todayUsage.reduce((s, u) => s + (u.tokens_used || 0), 0)

  const byPipeline: Record<string, { tokens: number; runs: number }> = {}
  usage.forEach(u => {
    const p = u.pipeline || 'unknown'
    if (!byPipeline[p]) byPipeline[p] = { tokens: 0, runs: 0 }
    byPipeline[p].tokens += u.tokens_used || 0
    byPipeline[p].runs += 1
  })

  const todayByPipeline: Record<string, number> = {}
  todayUsage.forEach(u => {
    const p = u.pipeline || 'unknown'
    todayByPipeline[p] = (todayByPipeline[p] || 0) + (u.tokens_used || 0)
  })

  const pct = Math.round((todayTokens / DAILY_LIMIT) * 100)
  const safePct = Math.round((todayTokens / SAFE_CEILING) * 100)
  const barColor = pct >= 85 ? 'bg-red-500' : pct >= 70 ? 'bg-orange-500' : 'bg-green-500'

  // Group by day for last 7 days
  const dailyMap: Record<string, number> = {}
  usage.forEach(u => {
    const day = u.created_at.slice(0, 10)
    dailyMap[day] = (dailyMap[day] || 0) + (u.tokens_used || 0)
  })
  const dailyEntries = Object.entries(dailyMap).sort((a, b) => b[0].localeCompare(a[0])).slice(0, 7)

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">Token Quota Monitor</h1>
            <p className="text-sm text-gray-400">Groq free tier usage — $0.00/month proof for IEEE paper</p>
          </div>
          <a href="/" className="text-sm text-blue-400 hover:text-blue-300">&larr; Dashboard</a>
        
          {/* Cross-Navigation -- 4 main pages (GNI-R-140) */}
          <div className="flex flex-wrap gap-2 mt-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Researcher
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Developer
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
          </div>
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {loading && <div className="text-center py-20 text-gray-400">Loading quota data...</div>}

        {!loading && (
          <>
            {/* Today summary */}
            <section className="mb-8">
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Today&apos;s Usage</div>
                    <div className="text-4xl font-bold text-white">{todayTokens.toLocaleString()}</div>
                    <div className="text-sm text-gray-400 mt-1">tokens used today</div>
                  </div>
                  <div className="text-right">
                    <div className={`text-3xl font-bold ${pct >= 85 ? 'text-red-400' : pct >= 70 ? 'text-orange-400' : 'text-green-400'}`}>
                      {pct}%
                    </div>
                    <div className="text-xs text-gray-500">of 100K limit</div>
                    <div className="text-xs text-gray-600 mt-1">{safePct}% of 85K safe ceiling</div>
                  </div>
                </div>
                <div className="w-full bg-gray-800 rounded-full h-4 mb-2">
                  <div className={`h-4 rounded-full ${barColor} transition-all`} style={{ width: pct + '%' }} />
                </div>
                <div className="flex justify-between text-xs text-gray-600">
                  <span>0</span>
                  <span className="text-yellow-600">85K safe ceiling</span>
                  <span>100K hard limit</span>
                </div>
                <div className="mt-4 grid grid-cols-2 gap-4">
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-xl font-bold text-green-400">{(DAILY_LIMIT - todayTokens).toLocaleString()}</div>
                    <div className="text-xs text-gray-500">tokens remaining</div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-xl font-bold text-white">$0.00</div>
                    <div className="text-xs text-gray-500">cost today (free tier)</div>
                  </div>
                </div>
              </div>
            </section>

            {/* Per pipeline today */}
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Today by Pipeline</div>
              <div className="space-y-3">
                {Object.entries(todayByPipeline).map(([pipeline, tokens]) => {
                  const pipelinePct = Math.round((tokens / DAILY_LIMIT) * 100)
                  return (
                    <div key={pipeline} className="bg-gray-900 border border-gray-700 rounded-xl p-4">
                      <div className="flex items-center justify-between mb-2">
                        <span className={`font-mono font-bold text-sm ${PIPELINE_TEXT[pipeline] || 'text-gray-400'}`}>{pipeline}</span>
                        <div className="text-right">
                          <span className="text-white font-bold">{tokens.toLocaleString()}</span>
                          <span className="text-gray-500 text-xs ml-1">tokens ({pipelinePct}%)</span>
                        </div>
                      </div>
                      <div className="w-full bg-gray-800 rounded-full h-2">
                        <div className={`h-2 rounded-full ${PIPELINE_COLORS[pipeline] || 'bg-gray-500'}`} style={{ width: pipelinePct + '%' }} />
                      </div>
                    </div>
                  )
                })}
                {Object.keys(todayByPipeline).length === 0 && (
                  <div className="text-center py-8 text-gray-600">No pipeline runs today yet</div>
                )}
              </div>
            </section>

            {/* 7-day history */}
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">7-Day History</div>
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="grid grid-cols-3 gap-2 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase">
                  <div>Date</div>
                  <div className="text-right">Tokens</div>
                  <div className="text-right">% of limit</div>
                </div>
                {dailyEntries.map(([day, tokens]) => {
                  const dayPct = Math.round((tokens / DAILY_LIMIT) * 100)
                  return (
                    <div key={day} className="grid grid-cols-3 gap-2 px-4 py-3 border-b border-gray-800 text-sm">
                      <div className="text-gray-300 font-mono">{day}</div>
                      <div className="text-right text-white font-bold">{tokens.toLocaleString()}</div>
                      <div className={`text-right font-bold ${dayPct >= 85 ? 'text-red-400' : dayPct >= 70 ? 'text-orange-400' : 'text-green-400'}`}>
                        {dayPct}%
                      </div>
                    </div>
                  )
                })}
              </div>
            </section>

            {/* IEEE proof */}
            <section>
              <div className="bg-green-950 border border-green-800 rounded-xl p-5">
                <div className="text-sm font-bold text-green-300 mb-2">IEEE Paper Evidence — $0.00/month claim</div>
                <div className="text-xs text-gray-400 leading-relaxed">
                  GNI_Autonomous runs entirely on free tiers. Groq provides 100,000 tokens/day at no cost.
                  All 4 pipelines (gni_pipeline, gni_mad, gni_heartbeat, gni_adaptive) operate within this limit.
                  Total monthly cost: $0.00. This page provides real-time verification of that claim.
                </div>
                <div className="mt-3 grid grid-cols-3 gap-3 text-center text-xs">
                  <div className="bg-green-900 rounded-lg p-2">
                    <div className="font-bold text-green-300">Groq</div>
                    <div className="text-gray-400">100K tokens/day free</div>
                  </div>
                  <div className="bg-green-900 rounded-lg p-2">
                    <div className="font-bold text-green-300">Supabase</div>
                    <div className="text-gray-400">500MB free tier</div>
                  </div>
                  <div className="bg-green-900 rounded-lg p-2">
                    <div className="font-bold text-green-300">Vercel + GitHub</div>
                    <div className="text-gray-400">Free tier unlimited</div>
                  </div>
                </div>
              </div>
            </section>
          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Token Quota Monitor | Groq free tier | $0.00/month | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}