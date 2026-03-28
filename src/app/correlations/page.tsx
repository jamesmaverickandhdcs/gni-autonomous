'use client'
import { useEffect, useState } from 'react'

interface Correlation {
  escalation_level: string
  avg_escalation_score: number
  spy_change_3d: number | null
  spy_change_7d: number | null
  spy_change_30d: number | null
  spy_change_180d: number | null
  accuracy_3d: number | null
  accuracy_7d: number | null
  accuracy_30d: number | null
  accuracy_180d: number | null
  bull_accuracy: number | null
  bear_accuracy: number | null
  swan_accuracy: number | null
  ostrich_accuracy: number | null
  narrow_ci_accuracy: number | null
  wide_ci_accuracy: number | null
  sample_count: number
}

interface Pattern {
  pattern_type: string
  pattern_key: string
  avg_spy_3d: number | null
  avg_spy_30d: number | null
  avg_spy_180d: number | null
  accuracy_3d: number | null
  accuracy_30d: number | null
  sample_count: number
}

const LEVEL_COLORS: Record<string, { border: string; bg: string; text: string }> = {
  CRITICAL: { border: 'border-red-800',    bg: 'bg-red-950',    text: 'text-red-400'    },
  HIGH:     { border: 'border-orange-800', bg: 'bg-orange-950', text: 'text-orange-400' },
  ELEVATED: { border: 'border-yellow-800', bg: 'bg-yellow-950', text: 'text-yellow-400' },
  MODERATE: { border: 'border-blue-800',   bg: 'bg-blue-950',   text: 'text-blue-400'   },
  LOW:      { border: 'border-green-800',  bg: 'bg-green-950',  text: 'text-green-400'  },
}

function PctBar({ value }: { value: number | null }) {
  if (value === null || value === undefined) return <span className="text-gray-600 text-xs">N/A</span>
  const color = value >= 75 ? 'bg-green-500' : value >= 50 ? 'bg-yellow-500' : 'bg-red-500'
  return (
    <div className="flex items-center gap-1.5">
      <div className="flex-1 bg-gray-700 rounded-full h-1.5 min-w-12">
        <div className={`h-1.5 rounded-full ${color}`} style={{ width: Math.min(100, value) + '%' }} />
      </div>
      <span className="text-xs text-gray-300 w-8 text-right shrink-0">{value.toFixed(0)}%</span>
    </div>
  )
}

function SpyChange({ value }: { value: number | null }) {
  if (value === null || value === undefined) return <span className="text-gray-600">N/A</span>
  const color = value >= 0 ? 'text-green-400' : 'text-red-400'
  return <span className={`font-bold ${color}`}>{value >= 0 ? '+' : ''}{value.toFixed(1)}%</span>
}

export default function CorrelationsPage() {
  const [correlations, setCorrelations] = useState<Correlation[]>([])
  const [patterns, setPatterns] = useState<Pattern[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'escalation' | 'agents' | 'patterns'>('escalation')

  useEffect(() => {
    fetch('/api/correlations')
      .then(r => r.json())
      .then(data => { setCorrelations(data.correlations || []); setPatterns(data.patterns || []) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const totalSamples = correlations.reduce((a, b) => a + (b.sample_count || 0), 0)
  const locationPatterns = patterns.filter(p => p.pattern_type === 'location')
  const pillarPatterns   = patterns.filter(p => p.pattern_type === 'pillar')

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/researcher" className="inline-flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 text-green-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Pattern Intelligence</a>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">📊 Correlation Engine v2</h1>
              <p className="text-sm text-gray-400">
                Pattern intelligence from {totalSamples} verified predictions.
              </p>
              <p className="text-xs text-gray-500 mt-1">
                3 horizons: Short (7d) · Medium (30d) · Long (180d) — CFA + Geopolitical standard
              </p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300 shrink-0">← Dashboard</a>
          </div>

          {/* Horizon legend */}
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <div className="text-sm font-bold text-blue-400">⚡ Short</div>
              <div className="text-xs text-gray-500">7 days — immediate market reaction</div>
            </div>
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <div className="text-sm font-bold text-yellow-400">📅 Medium</div>
              <div className="text-xs text-gray-500">30 days — policy response</div>
            </div>
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <div className="text-sm font-bold text-purple-400">🌐 Long</div>
              <div className="text-xs text-gray-500">180 days — structural shifts</div>
            </div>
          </div>
        
          {/* Cross-Navigation -- 4 main pages (GNI-R-140) */}
          <div className="flex flex-wrap gap-2 mt-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Researcher
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Dev Console
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
          </div>
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        <div className="flex gap-2 mb-6">
          {([
            { key: 'escalation', label: '⚡ Escalation Patterns' },
            { key: 'agents',     label: '🐂🐻🦢🦦 Agent Accuracy' },
            { key: 'patterns',   label: '🌍 Location & Pillar' },
          ] as const).map(tab => (
            <button key={tab.key} onClick={() => setActiveTab(tab.key)}
              className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                activeTab === tab.key ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
              }`}>
              {tab.label}
            </button>
          ))}
        </div>

        {loading && <div className="text-center py-20 text-gray-400">Loading correlation data...</div>}

        {!loading && correlations.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">📊</div>
            <p>No correlation data yet.</p>
            <p className="text-xs mt-2 max-w-md mx-auto">
              Requires verified GPVS predictions. Short (7d) data accumulates first.
              Medium (30d) and Long (180d) data builds over time.
            </p>
          </div>
        )}

        {/* ESCALATION TAB */}
        {activeTab === 'escalation' && correlations.length > 0 && (
          <div className="space-y-4">
            {correlations.map(c => {
              const col = LEVEL_COLORS[c.escalation_level] || LEVEL_COLORS.MODERATE
              return (
                <div key={c.escalation_level} className={`border rounded-xl p-5 ${col.border} ${col.bg}`}>
                  <div className="flex items-center justify-between mb-4">
                    <div>
                      <div className={`text-lg font-bold ${col.text}`}>{c.escalation_level}</div>
                      <div className="text-xs text-gray-500">avg {c.avg_escalation_score?.toFixed(1)}/10 — {c.sample_count} samples</div>
                    </div>
                  </div>

                  {/* 3 Horizon Grid */}
                  <div className="grid grid-cols-3 gap-4 mb-4">
                    {[
                      { label: '⚡ Short (7d)', spy: c.spy_change_7d, acc: c.accuracy_7d, color: 'text-blue-300' },
                      { label: '📅 Medium (30d)', spy: c.spy_change_30d, acc: c.accuracy_30d, color: 'text-yellow-300' },
                      { label: '🌐 Long (180d)', spy: c.spy_change_180d, acc: c.accuracy_180d, color: 'text-purple-300' },
                    ].map(h => (
                      <div key={h.label} className="bg-black bg-opacity-20 rounded-lg p-3">
                        <div className={`text-xs font-bold mb-2 ${h.color}`}>{h.label}</div>
                        <div className="text-xl font-bold mb-1"><SpyChange value={h.spy} /></div>
                        <div className="text-xs text-gray-500 mb-1">avg SPY move</div>
                        <PctBar value={h.acc} />
                        <div className="text-xs text-gray-600 mt-0.5">directional accuracy</div>
                      </div>
                    ))}
                  </div>

                  {/* CI comparison */}
                  {(c.narrow_ci_accuracy !== null || c.wide_ci_accuracy !== null) && (
                    <div className="bg-black bg-opacity-20 rounded-lg p-3 text-xs">
                      <span className="text-gray-500">Confidence Interval: </span>
                      <span className="text-blue-300">Narrow CI: {c.narrow_ci_accuracy !== null ? c.narrow_ci_accuracy?.toFixed(0) + '%' : 'N/A'}</span>
                      <span className="text-gray-600 mx-2">vs</span>
                      <span className="text-gray-400">Wide CI: {c.wide_ci_accuracy !== null ? c.wide_ci_accuracy?.toFixed(0) + '%' : 'N/A'}</span>
                      <span className="text-gray-600 ml-2">accuracy</span>
                    </div>
                  )}
                </div>
              )
            })}
          </div>
        )}

        {/* AGENTS TAB */}
        {activeTab === 'agents' && correlations.length > 0 && (
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
              Agent Prediction Accuracy — Short Horizon (7d)
            </div>
            <div className="overflow-x-auto">
              <table className="w-full text-xs">
                <thead>
                  <tr className="text-gray-500 border-b border-gray-700">
                    <th className="text-left py-2 pr-6">Level</th>
                    <th className="text-left py-2 pr-6">🐂 Bull</th>
                    <th className="text-left py-2 pr-6">🐻 Bear</th>
                    <th className="text-left py-2 pr-6">🦢 Black Swan</th>
                    <th className="text-left py-2 pr-6">🦦 Ostrich</th>
                    <th className="text-right py-2">N</th>
                  </tr>
                </thead>
                <tbody>
                  {correlations.map(c => (
                    <tr key={c.escalation_level} className="border-b border-gray-800">
                      <td className={`py-3 pr-6 font-bold ${LEVEL_COLORS[c.escalation_level]?.text || 'text-gray-400'}`}>
                        {c.escalation_level}
                      </td>
                      <td className="py-3 pr-6 min-w-32"><PctBar value={c.bull_accuracy} /></td>
                      <td className="py-3 pr-6 min-w-32"><PctBar value={c.bear_accuracy} /></td>
                      <td className="py-3 pr-6 min-w-32"><PctBar value={c.swan_accuracy} /></td>
                      <td className="py-3 pr-6 min-w-32"><PctBar value={c.ostrich_accuracy} /></td>
                      <td className="py-3 text-right text-gray-500">{c.sample_count}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
            <div className="mt-4 text-xs text-gray-600">
              Black Swan and Ostrich accuracy requires Quadratic MAD reports (from March 23, 2026).
              Medium and Long horizon agent accuracy will populate as predictions mature.
            </div>
          </div>
        )}

        {/* PATTERNS TAB */}
        {activeTab === 'patterns' && (
          <div className="space-y-6">
            {pillarPatterns.length > 0 && (
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Intelligence Pillar Patterns</div>
                <div className="grid grid-cols-3 gap-4">
                  {pillarPatterns.map(p => (
                    <div key={p.pattern_key} className="bg-gray-800 rounded-xl p-4">
                      <div className="text-lg font-bold text-white mb-3 text-center">
                        {p.pattern_key === 'GEO' ? '🌍' : p.pattern_key === 'FIN' ? '💰' : '💻'} {p.pattern_key}
                      </div>
                      <div className="space-y-2 text-xs">
                        <div className="flex justify-between">
                          <span className="text-blue-300">⚡ Short (7d)</span>
                          <SpyChange value={p.avg_spy_3d} />
                        </div>
                        <div className="flex justify-between">
                          <span className="text-yellow-300">📅 Medium (30d)</span>
                          <SpyChange value={p.avg_spy_30d} />
                        </div>
                        <div className="flex justify-between">
                          <span className="text-purple-300">🌐 Long (180d)</span>
                          <SpyChange value={p.avg_spy_180d} />
                        </div>
                        <div className="mt-2 pt-2 border-t border-gray-700">
                          <PctBar value={p.accuracy_3d} />
                          <div className="text-gray-600 mt-0.5">{p.sample_count} samples</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {locationPatterns.length > 0 && (
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Location Patterns</div>
                <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
                  {locationPatterns.slice(0, 12).map(p => (
                    <div key={p.pattern_key} className="bg-gray-800 rounded-lg p-3">
                      <div className="flex items-center justify-between mb-2">
                        <div className="text-sm font-bold text-white">📍 {p.pattern_key}</div>
                        <div className="text-xs text-gray-500">{p.sample_count} events</div>
                      </div>
                      <div className="space-y-1 text-xs">
                        <div className="flex justify-between">
                          <span className="text-blue-300">Short</span><SpyChange value={p.avg_spy_3d} />
                        </div>
                        <div className="flex justify-between">
                          <span className="text-yellow-300">Medium</span><SpyChange value={p.avg_spy_30d} />
                        </div>
                        <PctBar value={p.accuracy_3d} />
                      </div>
                    </div>
                  ))}
                </div>
              </div>
            )}

            {patterns.length === 0 && (
              <div className="text-center py-20 text-gray-400">
                <p>No pattern data yet. Requires 3+ verified predictions per location/pillar.</p>
              </div>
            )}
          </div>
        )}

      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Correlation Engine v2 | Short · Medium · Long horizons | CFA + Geopolitical standard
        </div>
      </footer>
    </div>
  )
}
