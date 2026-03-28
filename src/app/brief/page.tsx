'use client'
import { useEffect, useState } from 'react'

interface BriefData {
  title: string
  summary: string
  escalation_level: string
  escalation_score: number
  mad_verdict: string
  mad_confidence: number
  mad_action_recommendation: string
  mad_blind_spot: string
  tickers_affected: string[]
  sentiment: string
  sentiment_score: number
  created_at: string
  mad_bear_case: string
  mad_bull_case: string
}

const urgencyConfig = (level: string) => {
  switch (level?.toLowerCase()) {
    case 'critical': return { bg: 'bg-red-950', border: 'border-red-600', badge: 'bg-red-600 text-white', label: 'CRITICAL', dot: 'bg-red-500', text: 'text-red-300' }
    case 'high':     return { bg: 'bg-orange-950', border: 'border-orange-600', badge: 'bg-orange-600 text-white', label: 'HIGH', dot: 'bg-orange-500', text: 'text-orange-300' }
    case 'elevated': return { bg: 'bg-yellow-950', border: 'border-yellow-600', badge: 'bg-yellow-600 text-black', label: 'ELEVATED', dot: 'bg-yellow-500', text: 'text-yellow-300' }
    default:         return { bg: 'bg-green-950', border: 'border-green-700', badge: 'bg-green-700 text-white', label: 'MONITORING', dot: 'bg-green-500', text: 'text-green-300' }
  }
}

export default function BriefPage() {
  const [brief, setBrief] = useState<BriefData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [now, setNow] = useState('')

  useEffect(() => {
    setNow(new Date().toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }))
    fetch('/api/reports')
      .then(r => r.json())
      .then(data => {
        const reports = data.reports || []
        if (reports.length > 0) setBrief(reports[0])
        else setError('No reports available yet.')
      })
      .catch(() => setError('Failed to load brief.'))
      .finally(() => setLoading(false))
  }, [])

  const cfg = urgencyConfig(brief?.escalation_level || '')

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <a href="/" className="inline-flex items-center gap-1.5 text-xs font-bold text-blue-200 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 transition-colors">← Quantum Strategist</a>
              <h1 className="text-lg font-bold text-white mt-1">30-Second Executive Brief</h1>
              <p className="text-xs text-gray-400">GNI Autonomous — {now}</p>
            </div>
            <div className="text-right text-xs text-gray-500">
              <div>Auto-generated</div>
              <div>Mobile-first</div>
            </div>
          </div>
          {/* Cross-nav */}
          <div className="flex flex-wrap gap-2">
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Researcher
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Developer
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Reports
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6">

        {loading && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">⌛</div>
            <p>Loading brief...</p>
          </div>
        )}

        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">⚠️</div>
            <p>{error}</p>
          </div>
        )}

        {!loading && brief && (
          <>
            {/* URGENCY BANNER */}
            <section className={`mb-4 rounded-xl border-2 ${cfg.border} ${cfg.bg} p-5`}>
              <div className="flex items-center gap-3 mb-3">
                <span className={`w-3 h-3 rounded-full shrink-0 animate-pulse ${cfg.dot}`} />
                <span className={`text-sm font-bold px-3 py-1 rounded-full ${cfg.badge}`}>
                  {cfg.label}
                </span>
                <span className="text-xs text-gray-400">
                  Escalation: <span className={`font-bold ${cfg.text}`}>{brief.escalation_score?.toFixed(1)}/10</span>
                </span>
              </div>
              <h2 className="text-base font-bold text-white leading-snug mb-1">{brief.title}</h2>
              <p className="text-xs text-gray-300 leading-relaxed">{brief.summary?.slice(0, 200)}{brief.summary?.length > 200 ? '...' : ''}</p>
            </section>

            {/* ACTION RECOMMENDATION */}
            <section className="mb-4 bg-gray-900 border border-blue-800 rounded-xl p-4">
              <div className="text-xs text-blue-400 font-bold uppercase tracking-wider mb-2">🎯 Action Recommendation</div>
              <p className="text-sm text-white leading-relaxed font-medium">
                {brief.mad_action_recommendation || 'Awaiting MAD arbitrator verdict.'}
              </p>
            </section>

            {/* MAD VERDICT */}
            <section className="mb-4 bg-gray-900 border border-gray-700 rounded-xl p-4">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">MAD Verdict</div>
              <div className="flex items-center gap-3 mb-3">
                <span className={`text-sm font-bold px-3 py-1 rounded-full ${
                  brief.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300 border border-green-700' :
                  brief.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300 border border-red-700' :
                  'bg-gray-700 text-gray-300'
                }`}>
                  {brief.mad_verdict === 'bullish' ? '🐂' : brief.mad_verdict === 'bearish' ? '🐻' : '◆'} {brief.mad_verdict?.toUpperCase() || 'PENDING'}
                </span>
                <div className="flex-1 bg-gray-800 rounded-full h-2">
                  <div className={`h-2 rounded-full ${brief.mad_verdict === 'bullish' ? 'bg-green-500' : brief.mad_verdict === 'bearish' ? 'bg-red-500' : 'bg-gray-500'}`}
                    style={{ width: Math.round((brief.mad_confidence || 0) * 100) + '%' }} />
                </div>
                <span className="text-xs text-white font-bold shrink-0">{brief.mad_confidence ? Math.round(brief.mad_confidence * 100) + '%' : 'N/A'}</span>
              </div>
              <div className="grid grid-cols-2 gap-2">
                <div className="bg-green-950 border border-green-900 rounded-lg p-3">
                  <div className="text-xs text-green-400 font-bold mb-1">🐂 Bull Case</div>
                  <p className="text-xs text-gray-300 leading-relaxed line-clamp-3">{brief.mad_bull_case || 'Pending'}</p>
                </div>
                <div className="bg-red-950 border border-red-900 rounded-lg p-3">
                  <div className="text-xs text-red-400 font-bold mb-1">🐻 Bear Case</div>
                  <p className="text-xs text-gray-300 leading-relaxed line-clamp-3">{brief.mad_bear_case || 'Pending'}</p>
                </div>
              </div>
            </section>

            {/* BLIND SPOT WARNING */}
            {brief.mad_blind_spot && (
              <section className="mb-4 bg-purple-950 border border-purple-800 rounded-xl p-4">
                <div className="text-xs text-purple-400 font-bold uppercase tracking-wider mb-2">🕶️ Blind Spot Warning</div>
                <p className="text-sm text-gray-300 leading-relaxed">{brief.mad_blind_spot}</p>
              </section>
            )}

            {/* TICKERS */}
            {brief.tickers_affected?.length > 0 && (
              <section className="mb-4 bg-gray-900 border border-gray-700 rounded-xl p-4">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Market Implications</div>
                <div className="flex flex-wrap gap-2">
                  {brief.tickers_affected.slice(0, 6).map(ticker => (
                    <span key={ticker} className={`text-sm font-mono font-bold px-3 py-1.5 rounded-lg border ${
                      brief.sentiment?.toLowerCase() === 'bearish'
                        ? 'bg-red-950 border-red-800 text-red-300'
                        : 'bg-green-950 border-green-800 text-green-300'
                    }`}>
                      {ticker}
                      <span className="text-xs ml-1 opacity-60">{brief.sentiment?.toLowerCase() === 'bearish' ? '↓' : '↑'}</span>
                    </span>
                  ))}
                </div>
                <p className="text-xs text-gray-500 mt-3">
                  Sentiment: <span className={`font-bold ${brief.sentiment?.toLowerCase() === 'bearish' ? 'text-red-400' : 'text-green-400'}`}>
                    {brief.sentiment} ({brief.sentiment_score?.toFixed(2)})
                  </span>
                </p>
              </section>
            )}

            {/* GENERATED AT */}
            <section className="mb-4 bg-gray-900 border border-gray-800 rounded-xl p-3 text-center">
              <p className="text-xs text-gray-600">
                Brief generated from latest pipeline run —{' '}
                {brief.created_at ? new Date(brief.created_at).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' }) : 'N/A'}
              </p>
              <p className="text-xs text-gray-700 mt-1">Updates every pipeline run (02:00 + 10:00 UTC)</p>
            </section>

            {/* DISCLAIMER */}
            <section className="mb-4 bg-yellow-950 border border-yellow-800 rounded-xl p-3">
              <p className="text-xs text-yellow-300">
                ⚠️ Not financial advice. GNI reports are for informational purposes only.
              </p>
            </section>

            {/* LINKS TO FULL PAGES */}
            <section className="grid grid-cols-2 gap-3 mb-4">
              <a href="/debate" className="bg-gray-900 border border-gray-700 hover:border-blue-600 rounded-xl p-3 text-center transition-colors">
                <div className="text-lg mb-1">🐻🐂</div>
                <div className="text-xs font-bold text-white">Full Debate</div>
                <div className="text-xs text-gray-500">4-agent MAD analysis</div>
              </a>
              <a href="/comparison" className="bg-gray-900 border border-gray-700 hover:border-blue-600 rounded-xl p-3 text-center transition-colors">
                <div className="text-lg mb-1">⚖️</div>
                <div className="text-xs font-bold text-white">Divergence</div>
                <div className="text-xs text-gray-500">Pipeline vs MAD signal</div>
              </a>
              <a href="/scenarios" className="bg-gray-900 border border-gray-700 hover:border-blue-600 rounded-xl p-3 text-center transition-colors">
                <div className="text-lg mb-1">🔮</div>
                <div className="text-xs font-bold text-white">Scenarios</div>
                <div className="text-xs text-gray-500">Base / Upside / Downside</div>
              </a>
              <a href="/map" className="bg-gray-900 border border-gray-700 hover:border-blue-600 rounded-xl p-3 text-center transition-colors">
                <div className="text-lg mb-1">🗺️</div>
                <div className="text-xs font-bold text-white">Event Map</div>
                <div className="text-xs text-gray-500">Geopolitical event pins</div>
              </a>
            </section>
          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          Global Nexus Insights (Autonomous) | 30-Second Executive Brief | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
