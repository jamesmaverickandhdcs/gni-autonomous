'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Usage {
  pipeline: string
  tokens_used: number
  requests_used: number
  created_at: string
  account: string
}

const DAILY_LIMIT = 100000
const SAFE_CEILING = 85000
const PIPELINE_TEXT: Record<string, string> = {
  gni_pipeline: 'text-blue-400',
  gni_mad: 'text-purple-400',
  gni_adaptive: 'text-orange-400',
  gni_heartbeat: 'text-green-400',
}
const ACCOUNT_LABEL: Record<string, string> = {
  morning: 'Morning account',
  evening: 'Evening account',
  not_mad: 'Not-MAD account',
  unknown: 'Untagged',
}

function pctColorText(p: number): string {
  return p >= 85 ? 'text-red-400' : p >= 70 ? 'text-orange-400' : 'text-green-400'
}
function pctColorBar(p: number): string {
  return p >= 85 ? 'bg-red-500' : p >= 70 ? 'bg-orange-500' : 'bg-green-500'
}

export default function QuotaPage() {
  const [usage, setUsage] = useState<Usage[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/quota', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setUsage(data.usage || []))
      .catch(() => setError('Failed to load data.'))
      .finally(() => setLoading(false))
  }, [])

  const today = new Date().toISOString().slice(0, 10)
  const todayUsage = usage.filter(u => u.created_at.startsWith(today))
  const todayTokens = todayUsage.reduce((s, u) => s + (u.tokens_used || 0), 0)

  // Per-account token sums for TODAY -- each account is its OWN 100K pool.
  const byAccountToday: Record<string, number> = {}
  todayUsage.forEach(u => {
    const a = u.account || 'unknown'
    byAccountToday[a] = (byAccountToday[a] || 0) + (u.tokens_used || 0)
  })
  const accountRows = Object.entries(byAccountToday).sort((a, b) => b[1] - a[1])
  const worstPct = accountRows.length
    ? Math.max(...accountRows.map(([, t]) => Math.round((t / DAILY_LIMIT) * 100)))
    : 0

  const todayByPipeline: Record<string, number> = {}
  todayUsage.forEach(u => {
    const p = u.pipeline || 'unknown'
    todayByPipeline[p] = (todayByPipeline[p] || 0) + (u.tokens_used || 0)
  })

  // 7-day history: each day's % is against (accounts active that day x 100K).
  const dayTokens: Record<string, number> = {}
  const dayAccounts: Record<string, Set<string>> = {}
  usage.forEach(u => {
    const day = u.created_at.slice(0, 10)
    dayTokens[day] = (dayTokens[day] || 0) + (u.tokens_used || 0)
    if (!dayAccounts[day]) dayAccounts[day] = new Set()
    dayAccounts[day].add(u.account || 'unknown')
  })
  const dailyEntries = Object.keys(dayTokens)
    .sort((a, b) => b.localeCompare(a))
    .slice(0, 7)
    .map(day => {
      const accts = dayAccounts[day]?.size || 1
      const tokens = dayTokens[day]
      const pct = Math.round((tokens / (accts * DAILY_LIMIT)) * 100)
      return { day, tokens, accts, pct }
    })

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/developer-hub" className="inline-flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">&larr; Dev Console</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">Token Quota Monitor</h1>
            <p className="text-sm text-gray-400">Groq free tier usage &mdash; per-account, $0.00/month proof for IEEE paper</p>
          </div>
</div>
          </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {loading && <div className="text-center py-20 text-gray-400">Loading quota data...</div>}


        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">&#9888;&#65039;</div>
            <p>{error}</p>
          </div>
        )}
        {!loading && (
          <>
            {/* Today summary -- per account */}
            <section className="mb-8">
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
                <div className="flex items-center justify-between mb-4">
                  <div>
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Today&apos;s Usage</div>
                    <div className="text-4xl font-bold text-white">{todayTokens.toLocaleString()}</div>
                    <div className="text-sm text-gray-400 mt-1">tokens used today &middot; across {accountRows.length || 0} account{accountRows.length === 1 ? '' : 's'}</div>
                  </div>
                  <div className="text-right">
                    <div className={`text-3xl font-bold ${pctColorText(worstPct)}`}>{worstPct}%</div>
                    <div className="text-xs text-gray-500">worst account vs its 100K</div>
                    <div className="text-xs text-gray-600 mt-1">each account = own free-tier pool</div>
                  </div>
                </div>

                {accountRows.length === 0 && (
                  <div className="text-center py-8 text-gray-600">No pipeline runs today yet (UTC day just started)</div>
                )}

                {accountRows.map(([acct, tokens]) => {
                  const p = Math.round((tokens / DAILY_LIMIT) * 100)
                  const safeP = Math.round((tokens / SAFE_CEILING) * 100)
                  return (
                    <div key={acct} className="mb-4 last:mb-0">
                      <div className="flex items-center justify-between mb-1">
                        <span className="text-sm font-bold text-gray-200">{ACCOUNT_LABEL[acct] || acct}</span>
                        <div className="text-right">
                          <span className="text-white font-bold">{tokens.toLocaleString()}</span>
                          <span className={`text-xs ml-2 font-bold ${pctColorText(p)}`}>{p}%</span>
                        </div>
                      </div>
                      <div className="w-full bg-gray-800 rounded-full h-3">
                        <div className={`h-3 rounded-full ${pctColorBar(p)} transition-all`} style={{ width: Math.min(p, 100) + '%' }} />
                      </div>
                      <div className="flex justify-between text-xs text-gray-600 mt-1">
                        <span>{safeP}% of 85K safe ceiling</span>
                        <span>{(DAILY_LIMIT - tokens).toLocaleString()} remaining</span>
                      </div>
                    </div>
                  )
                })}

                <div className="mt-4 bg-gray-800 rounded-lg p-3 text-center">
                  <div className="text-xl font-bold text-white">$0.00</div>
                  <div className="text-xs text-gray-500">cost today (free tier)</div>
                </div>
              </div>
            </section>

            {/* Per pipeline today -- raw tokens (A1: no per-account ceiling math) */}
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Today by Pipeline</div>
              <div className="space-y-3">
                {Object.entries(todayByPipeline).map(([pipeline, tokens]) => (
                  <div key={pipeline} className="bg-gray-900 border border-gray-700 rounded-xl p-4">
                    <div className="flex items-center justify-between">
                      <span className={`font-mono font-bold text-sm ${PIPELINE_TEXT[pipeline] || 'text-gray-400'}`}>{pipeline}</span>
                      <div className="text-right">
                        <span className="text-white font-bold">{tokens.toLocaleString()}</span>
                        <span className="text-gray-500 text-xs ml-1">tokens</span>
                      </div>
                    </div>
                  </div>
                ))}
                {Object.keys(todayByPipeline).length === 0 && (
                  <div className="text-center py-8 text-gray-600">No pipeline runs today yet</div>
                )}
              </div>
            </section>

            {/* 7-day history -- % against accounts-active x 100K */}
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">7-Day History</div>
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="grid grid-cols-4 gap-2 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase">
                  <div>Date</div>
                  <div className="text-right">Tokens</div>
                  <div className="text-right">Accounts</div>
                  <div className="text-right">% of pooled</div>
                </div>
                {dailyEntries.map(({ day, tokens, accts, pct }) => (
                  <div key={day} className="grid grid-cols-4 gap-2 px-4 py-3 border-b border-gray-800 text-sm">
                    <div className="text-gray-300 font-mono">{day}</div>
                    <div className="text-right text-white font-bold">{tokens.toLocaleString()}</div>
                    <div className="text-right text-gray-400">{accts}</div>
                    <div className={`text-right font-bold ${pctColorText(pct)}`}>{pct}%</div>
                  </div>
                ))}
              </div>
            </section>

            {/* IEEE proof */}
            <section>
              <div className="bg-green-950 border border-green-800 rounded-xl p-5">
                <div className="text-sm font-bold text-green-300 mb-2">IEEE Paper Evidence &mdash; $0.00/month claim</div>
                <div className="text-xs text-gray-400 leading-relaxed">
                  GNI_Autonomous runs entirely on free tiers. Groq provides 100,000 tokens/day per account at no cost.
                  MAD is split across dedicated morning and evening accounts, each drawing on its own 100K pool.
                  Total monthly cost: $0.00. This page provides real-time per-account verification of that claim.
                </div>
                <div className="mt-3 grid grid-cols-3 gap-3 text-center text-xs">
                  <div className="bg-green-900 rounded-lg p-2">
                    <div className="font-bold text-green-300">Groq</div>
                    <div className="text-gray-400">100K tokens/day/account</div>
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

      
      {/* DISCLAIMER */}
      <div className="max-w-6xl mx-auto px-6 pb-2 text-center">
        <p className="text-xs text-gray-600">&#9888;&#65039; GNI data is for informational purposes only. Not financial advice.</p>
      </div>
      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Token Quota Monitor | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
