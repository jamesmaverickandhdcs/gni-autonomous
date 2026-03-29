'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface PillarReport {
  id: string
  pillar: string
  title: string
  summary: string
  sentiment: string
  sentiment_score: number
  risk_level: string
  location_name: string
  tickers_affected: string[]
  market_impact: string
  weakness_identified: string
  threat_horizon: string
  dark_side_detected: string
  quality_score: number
  run_id: string
  created_at: string
}

const PILLAR_CONFIG = {
  geo: { label: 'Geopolitical', emoji: '&#x1F30D;', border: 'border-red-800', bg: 'bg-red-950', accent: 'text-red-400', desc: 'Conflict, diplomacy, alliances, sanctions' },
  tech: { label: 'Technology', emoji: '&#x1F4BB;', border: 'border-blue-800', bg: 'bg-blue-950', accent: 'text-blue-400', desc: 'Cyber, AI, surveillance, semiconductors' },
  fin: { label: 'Financial', emoji: '&#x1F4B0;', border: 'border-green-800', bg: 'bg-green-950', accent: 'text-green-400', desc: 'Markets, trade, sanctions, inflation' },
}

const riskColor = (r: string) => {
  switch (r?.toLowerCase()) {
    case 'critical': return 'bg-red-600 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    default: return 'bg-green-500 text-white'
  }
}

const sentimentColor = (s: string) => {
  switch (s?.toLowerCase()) {
    case 'bearish': return 'text-red-400'
    case 'bullish': return 'text-green-400'
    default: return 'text-gray-400'
  }
}

export default function PillarsPage() {
  const [reports, setReports] = useState<PillarReport[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'latest' | 'history'>('latest')
  const [activePillar, setActivePillar] = useState<'all' | 'geo' | 'tech' | 'fin'>('all')

  useEffect(() => {
    fetch('/api/pillars', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setReports(data.reports || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  // Latest run = group by pillar, take most recent each
  const latest: Record<string, PillarReport> = {}
  reports.forEach(r => {
    if (!latest[r.pillar] || r.created_at > latest[r.pillar].created_at) {
      latest[r.pillar] = r
    }
  })

  const filtered = activePillar === 'all'
    ? reports
    : reports.filter(r => r.pillar === activePillar)

  const totalReports = reports.length
  const bearishCount = reports.filter(r => r.sentiment?.toLowerCase() === 'bearish').length
  const avgQuality = reports.filter(r => r.quality_score > 0).length > 0
    ? (reports.filter(r => r.quality_score > 0).reduce((s, r) => s + r.quality_score, 0) / reports.filter(r => r.quality_score > 0).length).toFixed(1)
    : 'N/A'

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/" className="inline-flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Quantum Strategist</a>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">&#x1F30D;&#x1F4BB;&#x1F4B0; Three Pillar Intelligence</h1>
              <p className="text-sm text-gray-400">Geopolitical + Technology + Financial — domain-specific AI analysis</p>
            </div>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-white">{totalReports}</div>
              <div className="text-xs text-gray-500">Total Pillar Reports</div>
            </div>
            <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-red-400">{bearishCount}</div>
              <div className="text-xs text-red-600">Bearish Signals</div>
            </div>
            <div className="bg-blue-950 border border-blue-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-blue-400">{avgQuality}</div>
              <div className="text-xs text-blue-600">Avg Quality Score</div>
            </div>
          </div>
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {loading && <div className="text-center py-20 text-gray-400">Loading pillar reports...</div>}

        {!loading && (
          <>
            {/* How it works */}
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 mb-6 text-xs text-gray-400 leading-relaxed">
              <span className="text-white font-bold">How Three Pillar Reports work: </span>
              Every pipeline run produces three separate AI analyses — Geopolitical (conflict, diplomacy),
              Technology (cyber, AI, surveillance), and Financial (markets, sanctions, trade).
              Each pillar uses the same top articles but focuses on its domain.
              This gives a multi-dimensional view of the same global events.
            </div>

            {/* Tabs */}
            <div className="flex gap-2 mb-6">
              {(['latest', 'history'] as const).map(tab => (
                <button key={tab} onClick={() => setActiveTab(tab)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium capitalize transition-colors ${
                    activeTab === tab ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}>
                  {tab === 'latest' ? 'Latest Run' : 'Full History'}
                </button>
              ))}
            </div>

            {/* LATEST TAB */}
            {activeTab === 'latest' && (
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {(['geo', 'tech', 'fin'] as const).map(pillar => {
                  const cfg = PILLAR_CONFIG[pillar]
                  const report = latest[pillar]
                  return (
                    <div key={pillar} className={`border rounded-xl p-5 ${cfg.border} ${cfg.bg}`}>
                      <div className="flex items-center gap-2 mb-4">
                        <span className="text-2xl" dangerouslySetInnerHTML={{ __html: cfg.emoji }} />
                        <div>
                          <div className={`text-sm font-bold uppercase ${cfg.accent}`}>{cfg.label}</div>
                          <div className="text-xs text-gray-500">{cfg.desc}</div>
                        </div>
                      </div>
                      {report ? (
                        <>
                          <div className="text-sm font-bold text-white mb-2 leading-tight">{report.title}</div>
                          <div className="text-xs text-gray-400 mb-3 leading-relaxed line-clamp-4">{report.summary}</div>
                          <div className="flex items-center justify-between mb-3">
                            <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${riskColor(report.risk_level)}`}>
                              {report.risk_level?.toUpperCase()}
                            </span>
                            <span className={`text-sm font-bold ${sentimentColor(report.sentiment)}`}>
                              {report.sentiment} {report.sentiment_score >= 0 ? '+' : ''}{report.sentiment_score?.toFixed(2)}
                            </span>
                          </div>
                          {report.market_impact && (
                            <div className="bg-black bg-opacity-20 rounded-lg p-3 mb-3">
                              <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Market Impact</div>
                              <p className="text-xs text-gray-300 leading-relaxed line-clamp-3">{report.market_impact}</p>
                            </div>
                          )}
                          {report.weakness_identified && (
                            <div className="text-xs text-yellow-600 border-t border-gray-700 pt-2 mt-2">
                              <span className="font-bold">Weakness: </span>
                              <span className="line-clamp-2">{report.weakness_identified}</span>
                            </div>
                          )}
                          {report.dark_side_detected && report.dark_side_detected !== 'None' && (
                            <div className="text-xs text-purple-400 mt-2">
                              <span className="font-bold">Dark side: </span>
                              <span className="line-clamp-2">{report.dark_side_detected}</span>
                            </div>
                          )}
                          {report.tickers_affected?.length > 0 && (
                            <div className="flex flex-wrap gap-1 mt-3">
                              {report.tickers_affected.slice(0, 4).map((t: string) => (
                                <span key={t} className="text-xs font-mono text-blue-400 bg-blue-950 px-1.5 py-0.5 rounded">{t}</span>
                              ))}
                            </div>
                          )}
                          {report.quality_score > 0 && (
                            <div className="mt-3 text-xs text-gray-600">
                              Quality: <span className={`font-bold ${report.quality_score >= 8 ? 'text-green-400' : report.quality_score >= 6 ? 'text-yellow-400' : 'text-red-400'}`}>
                                {report.quality_score?.toFixed(1)}/10
                              </span>
                            </div>
                          )}
                          <div className="mt-2 text-xs text-gray-600">
                            {new Date(report.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}
                          </div>
                        </>
                      ) : (
                        <div className="text-xs text-gray-600 italic py-8 text-center">Pending next pipeline run</div>
                      )}
                    </div>
                  )
                })}
              </div>
            )}

            {/* HISTORY TAB */}
            {activeTab === 'history' && (
              <>
                <div className="flex gap-2 mb-4">
                  {(['all', 'geo', 'tech', 'fin'] as const).map(p => (
                    <button key={p} onClick={() => setActivePillar(p)}
                      className={`px-3 py-1.5 rounded-lg text-xs font-medium capitalize transition-colors ${
                        activePillar === p ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                      }`}>
                      {p === 'all' ? 'All' : PILLAR_CONFIG[p].label} ({p === 'all' ? reports.length : reports.filter(r => r.pillar === p).length})
                    </button>
                  ))}
                </div>
                <div className="space-y-3">
                  {filtered.map(r => {
                    const cfg = PILLAR_CONFIG[r.pillar as keyof typeof PILLAR_CONFIG] || PILLAR_CONFIG.geo
                    return (
                      <div key={r.id} className={`border rounded-xl p-4 ${cfg.border} ${cfg.bg}`}>
                        <div className="flex items-start justify-between gap-4">
                          <div className="flex-1">
                            <div className="flex items-center gap-2 mb-1">
                              <span dangerouslySetInnerHTML={{ __html: cfg.emoji }} />
                              <span className={`text-xs font-bold uppercase ${cfg.accent}`}>{cfg.label}</span>
                            </div>
                            <div className="text-sm font-bold text-white mb-1">{r.title}</div>
                            <div className="text-xs text-gray-400 line-clamp-2">{r.summary}</div>
                          </div>
                          <div className="flex flex-col items-end gap-1 shrink-0">
                            <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${riskColor(r.risk_level)}`}>
                              {r.risk_level?.toUpperCase()}
                            </span>
                            <span className={`text-xs font-bold ${sentimentColor(r.sentiment)}`}>{r.sentiment}</span>
                            <span className="text-xs text-gray-600">
                              {new Date(r.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                            </span>
                          </div>
                        </div>
                        {r.tickers_affected?.length > 0 && (
                          <div className="flex flex-wrap gap-1 mt-2">
                            {r.tickers_affected.slice(0, 4).map((t: string) => (
                              <span key={t} className="text-xs font-mono text-blue-400">{t}</span>
                            ))}
                          </div>
                        )}
                      </div>
                    )
                  })}
                </div>
              </>
            )}
          </>
        )}
      </main>

      
      {/* DISCLAIMER */}
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">
            ⚠️ <strong>Disclaimer:</strong> GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.
          </p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Three Pillar Intelligence | Geo + Tech + Fin | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}