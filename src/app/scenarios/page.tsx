'use client'
import { useEffect, useState } from 'react'

interface Report {
  id: string
  title: string
  summary: string
  sentiment: string
  sentiment_score: number
  risk_level: string
  location_name: string
  created_at: string
  quality_score: number
  mad_verdict: string
  mad_confidence: number
  mad_bull_case: string
  mad_bear_case: string
  mad_black_swan_case: string
  mad_ostrich_case: string
  mad_blind_spot: string
  mad_action_recommendation: string
  short_focus_threats: string
  long_shoot_threats: string
  escalation_score: number
  escalation_level: string
}

const riskColor = (risk: string) => {
  switch (risk?.toLowerCase()) {
    case 'critical': return 'bg-red-600 text-white'
    case 'high':     return 'bg-orange-500 text-white'
    case 'medium':   return 'bg-yellow-500 text-black'
    case 'low':      return 'bg-green-500 text-white'
    default:         return 'bg-gray-500 text-white'
  }
}

const confidenceColor = (c: number) => {
  if (c >= 0.7) return 'text-green-400'
  if (c >= 0.5) return 'text-yellow-400'
  return 'text-red-400'
}

function ScenarioCard({ report }: { report: Report }) {
  const [expanded, setExpanded] = useState(false)

  const scenarios = [
    {
      label: 'Base Case',
      icon: '⚖️',
      color: 'border-gray-600',
      bg: 'bg-gray-800',
      accent: 'text-gray-300',
      header: 'bg-gray-700',
      content: report.mad_bear_case,
      note: 'Known risks playing out -- most likely path',
    },
    {
      label: 'Upside Case',
      icon: '🐂',
      color: 'border-green-700',
      bg: 'bg-green-950',
      accent: 'text-green-300',
      header: 'bg-green-900',
      content: report.mad_bull_case,
      note: 'Opportunity cost -- what happens if we act on known positives',
    },
    {
      label: 'Downside Case',
      icon: '🦢🦦',
      color: 'border-red-700',
      bg: 'bg-red-950',
      accent: 'text-red-300',
      header: 'bg-red-900',
      content: report.mad_black_swan_case || report.mad_ostrich_case || '',
      note: 'Black Swan + Ostrich combined -- unknown and ignored threats',
    },
  ]

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden mb-4">
      <button
        onClick={() => setExpanded(!expanded)}
        className="w-full text-left px-6 py-4 hover:bg-gray-800 transition-colors"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2 flex-wrap">
              <span className="text-sm font-bold text-blue-400">
                {new Date(report.created_at).toLocaleDateString('en-US', {
                  weekday: 'short', month: 'short', day: 'numeric',
                  hour: '2-digit', minute: '2-digit'
                })}
              </span>
              <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${riskColor(report.risk_level)}`}>
                {report.risk_level?.toUpperCase()}
              </span>
              {report.mad_verdict && (
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  report.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300' :
                  report.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300' :
                  'bg-gray-700 text-gray-300'
                }`}>
                  {report.mad_verdict === 'bullish' ? '🐂' : '🐻'} {report.mad_verdict?.toUpperCase()} {report.mad_confidence ? Math.round(report.mad_confidence * 100) + '%' : ''}
                </span>
              )}
              {report.quality_score > 0 && (
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                  report.quality_score >= 8 ? 'bg-green-700 text-green-100' :
                  report.quality_score >= 6 ? 'bg-blue-700 text-blue-100' :
                  'bg-gray-700 text-gray-300'
                }`}>
                  Q:{report.quality_score}/10
                </span>
              )}
            </div>
            <h3 className="text-white font-semibold text-sm">{report.title}</h3>
          </div>
          <span className="text-gray-600 text-xs shrink-0">{expanded ? 'Hide' : 'Show'}</span>
        </div>
      </button>

      {expanded && (
        <div className="border-t border-gray-800 px-6 py-4 space-y-4">

          <div className="bg-yellow-950 border border-yellow-800 rounded-lg p-3 text-xs text-yellow-300">
            ⚠️ <strong>Indicative only</strong> -- Scenario reliability improves as correlation data accumulates (target: 100+ GPVS verifications).
          </div>

          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {scenarios.map(({ label, icon, color, bg, accent, header, content, note }) => (
              <div key={label} className={`border rounded-xl overflow-hidden ${color} ${bg}`}>
                <div className={`px-4 py-2 ${header} flex items-center gap-2`}>
                  <span>{icon}</span>
                  <span className={`text-xs font-bold uppercase tracking-wider ${accent}`}>{label}</span>
                </div>
                <div className="p-4">
                  <p className="text-xs text-gray-300 leading-relaxed mb-3">
                    {content || <span className="italic text-gray-600">No data for this scenario yet.</span>}
                  </p>
                  <p className="text-xs text-gray-600 italic border-t border-gray-700 pt-2">{note}</p>
                </div>
              </div>
            ))}
          </div>

          {(report.short_focus_threats || report.long_shoot_threats) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {report.short_focus_threats && (
                <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                  <div className="text-xs text-blue-400 font-bold mb-1">🔮 Short Focus (7-30 days)</div>
                  <p className="text-xs text-gray-300 leading-relaxed">{report.short_focus_threats}</p>
                </div>
              )}
              {report.long_shoot_threats && (
                <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                  <div className="text-xs text-blue-400 font-bold mb-1">🎯 Long Shoots (3-24 months)</div>
                  <p className="text-xs text-gray-300 leading-relaxed">{report.long_shoot_threats}</p>
                </div>
              )}
            </div>
          )}

          {(report.mad_blind_spot || report.mad_action_recommendation) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {report.mad_blind_spot && (
                <div className="bg-gray-800 border border-orange-800 rounded-lg p-3">
                  <div className="text-xs text-orange-400 font-bold mb-1">🔍 Blind Spot</div>
                  <p className="text-xs text-gray-300 leading-relaxed">{report.mad_blind_spot}</p>
                </div>
              )}
              {report.mad_action_recommendation && (
                <div className="bg-gray-800 border border-green-800 rounded-lg p-3">
                  <div className="text-xs text-green-400 font-bold mb-1">⚡ Action Recommendation</div>
                  <p className="text-xs text-gray-300 leading-relaxed">{report.mad_action_recommendation}</p>
                </div>
              )}
            </div>
          )}

          {report.mad_confidence > 0 && (
            <div>
              <div className="flex justify-between text-xs text-gray-500 mb-1">
                <span>MAD Confidence</span>
                <span className={confidenceColor(report.mad_confidence)}>
                  {Math.round(report.mad_confidence * 100)}%
                  {report.mad_confidence >= 0.7 ? ' -- Strong consensus' :
                   report.mad_confidence >= 0.5 ? ' -- Moderate consensus' :
                   ' -- Contested'}
                </span>
              </div>
              <div className="h-1.5 bg-gray-800 rounded-full">
                <div
                  className={`h-1.5 rounded-full ${report.mad_confidence >= 0.7 ? 'bg-green-500' : report.mad_confidence >= 0.5 ? 'bg-yellow-500' : 'bg-red-500'}`}
                  style={{ width: Math.round(report.mad_confidence * 100) + '%' }}
                />
              </div>
            </div>
          )}
        </div>
      )}
    </div>
  )
}

export default function ScenariosPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'high' | 'critical'>('all')

  useEffect(() => {
    fetch('/api/reports')
      .then(r => r.json())
      .then(data => setReports(data.reports || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const withScenarios = reports.filter(r => r.mad_bull_case || r.mad_bear_case || r.mad_black_swan_case)
  const filtered = withScenarios.filter(r => {
    if (filter === 'critical') return r.risk_level?.toLowerCase() === 'critical'
    if (filter === 'high') return ['critical', 'high'].includes(r.risk_level?.toLowerCase())
    return true
  })

  const criticalCount = withScenarios.filter(r => r.risk_level?.toLowerCase() === 'critical').length
  const highCount = withScenarios.filter(r => ['critical', 'high'].includes(r.risk_level?.toLowerCase())).length

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/" className="inline-flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Quantum Strategist</a>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">📊 Scenario Planning</h1>
              <p className="text-sm text-gray-400">Base / Upside / Downside scenarios from Quadratic MAD debate</p>
              <p className="text-xs text-gray-600 mt-1">Reliability improves as GPVS correlation data accumulates.</p>
            </div>
            
          </div>
          {reports.length > 0 && (
            <div className="grid grid-cols-3 gap-3 mt-4">
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-white">{withScenarios.length}</div>
                <div className="text-xs text-gray-500">Scenarios Available</div>
              </div>
              <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-red-400">{criticalCount}</div>
                <div className="text-xs text-red-600">Critical Risk</div>
              </div>
              <div className="bg-orange-950 border border-orange-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-orange-400">{highCount}</div>
                <div className="text-xs text-orange-600">High+ Risk</div>
              </div>
            </div>
          )}
        
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

        {loading && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">⌛</div>
            <p>Loading scenarios...</p>
          </div>
        )}

        {!loading && withScenarios.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">📊</div>
            <p>No scenario data yet. Pipeline runs at 02:00 and 10:00 UTC.</p>
          </div>
        )}

        {!loading && withScenarios.length > 0 && (
          <>
            <div className="flex items-center justify-between mb-6">
              <div className="text-xs text-gray-500 uppercase tracking-wider">
                {filtered.length} scenario{filtered.length !== 1 ? 's' : ''} shown
              </div>
              <div className="flex gap-2">
                {([
                  { key: 'all', label: 'All Runs' },
                  { key: 'high', label: 'High+ Risk' },
                  { key: 'critical', label: 'Critical Only' },
                ] as const).map(({ key, label }) => (
                  <button
                    key={key}
                    onClick={() => setFilter(key)}
                    className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                      filter === key
                        ? 'bg-gray-700 border-gray-500 text-white'
                        : 'bg-gray-900 border-gray-700 text-gray-400 hover:border-gray-500'
                    }`}
                  >
                    {label}
                  </button>
                ))}
              </div>
            </div>

            <div className="bg-gray-900 border border-gray-700 rounded-xl p-5 mb-6">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">💡 How to Read Scenarios</div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs text-gray-400">
                <div>
                  <div className="text-gray-300 font-bold mb-1">⚖️ Base Case</div>
                  <p>Bear agent -- known risks playing out. Most likely path.</p>
                </div>
                <div>
                  <div className="text-green-400 font-bold mb-1">🐂 Upside Case</div>
                  <p>Bull agent -- opportunity cost of inaction on known positives.</p>
                </div>
                <div>
                  <div className="text-red-400 font-bold mb-1">🦢 Downside Case</div>
                  <p>Black Swan -- unknown threats nobody is modelling.</p>
                </div>
              </div>
            </div>

            {filtered.map(report => (
              <ScenarioCard key={report.id} report={report} />
            ))}
          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights | Scenario Planning | Team Geeks | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
