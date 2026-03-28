'use client'
import { useEffect, useState } from 'react'

interface PillarReport {
  id: string
  pillar: string
  title: string
  summary: string
  sentiment: string
  sentiment_score: number
  risk_level: string
  tickers_affected: string[]
  weakness_identified: string
  created_at: string
}

interface Report {
  id: string
  title: string
  escalation_score: number
  escalation_level: string
  sentiment: string
  created_at: string
}

export default function WeeklyDigestPage() {
  const [pillars, setPillars] = useState<PillarReport[]>([])
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    Promise.all([
      fetch('/api/pillar-reports').then(r => r.json()),
      fetch('/api/reports').then(r => r.json()),
    ]).then(([pd, rd]) => {
      setPillars(pd.reports || [])
      setReports(rd.reports || [])
    }).catch(() => {}).finally(() => setLoading(false))
  }, [])

  const geo  = pillars.find(p => p.pillar === 'geo')
  const tech = pillars.find(p => p.pillar === 'tech')
  const fin  = pillars.find(p => p.pillar === 'fin')

  const avgEscalation = reports.length > 0
    ? (reports.reduce((s, r) => s + (r.escalation_score || 0), 0) / reports.length).toFixed(1)
    : '0.0'

  const bearishCount = reports.filter(r => r.sentiment?.toLowerCase() === 'bearish').length
  const bullishCount = reports.filter(r => r.sentiment?.toLowerCase() === 'bullish').length

  const now = new Date()
  const weekStart = new Date(now)
  weekStart.setDate(now.getDate() - 7)

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/researcher" className="inline-flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 text-green-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Pattern Intelligence</a>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">Weekly Intelligence Digest</h1>
              <p className="text-sm text-gray-400">
                Week of {weekStart.toLocaleDateString('en-US', { month: 'short', day: 'numeric' })} &mdash; {now.toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
              </p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300">&larr; Dashboard</a>
          </div>
        
          {/* Cross-Navigation -- 4 main pages (GNI-R-140) */}
          <div className="flex flex-wrap gap-2 mt-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Pattern Intelligence
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
        {loading && <div className="text-center py-20 text-gray-400">Loading digest...</div>}

        {!loading && (
          <>
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Week Summary</div>
              <div className="grid grid-cols-3 gap-4">
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 text-center">
                  <div className="text-3xl font-bold text-white">{reports.length}</div>
                  <div className="text-xs text-gray-500 mt-1">Pipeline Runs</div>
                </div>
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 text-center">
                  <div className={`text-3xl font-bold ${parseFloat(avgEscalation) >= 7 ? 'text-red-400' : parseFloat(avgEscalation) >= 4 ? 'text-orange-400' : 'text-green-400'}`}>
                    {avgEscalation}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">Avg Escalation /10</div>
                </div>
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 text-center">
                  <div className={`text-2xl font-bold ${bearishCount > bullishCount ? 'text-red-400' : bullishCount > bearishCount ? 'text-green-400' : 'text-gray-400'}`}>
                    {bearishCount > bullishCount ? 'BEARISH' : bullishCount > bearishCount ? 'BULLISH' : 'NEUTRAL'}
                  </div>
                  <div className="text-xs text-gray-500 mt-1">{bearishCount} bearish / {bullishCount} bullish</div>
                </div>
              </div>
            </section>

            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Three Pillar Intelligence &mdash; Latest</div>
              <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                {[
                  { label: 'Geopolitical', emoji: '&#x1F30D;', report: geo, border: 'border-red-800', bg: 'bg-red-950', accent: 'text-red-400' },
                  { label: 'Technology', emoji: '&#x1F4BB;', report: tech, border: 'border-blue-800', bg: 'bg-blue-950', accent: 'text-blue-400' },
                  { label: 'Financial', emoji: '&#x1F4B0;', report: fin, border: 'border-green-800', bg: 'bg-green-950', accent: 'text-green-400' },
                ].map(({ label, emoji, report, border, bg, accent }) => (
                  <div key={label} className={`border rounded-xl p-4 ${border} ${bg}`}>
                    <div className="flex items-center gap-2 mb-3">
                      <span dangerouslySetInnerHTML={{ __html: emoji }} />
                      <span className={`text-xs font-bold uppercase ${accent}`}>{label}</span>
                    </div>
                    {report ? (
                      <>
                        <div className="text-sm font-bold text-white mb-2 line-clamp-2">{report.title}</div>
                        <div className="text-xs text-gray-400 line-clamp-3">{report.summary}</div>
                        {report.weakness_identified && (
                          <div className="mt-2 text-xs text-yellow-600 border-t border-gray-700 pt-2">
                            <span className="font-bold">Weakness: </span>{report.weakness_identified}
                          </div>
                        )}
                      </>
                    ) : (
                      <div className="text-xs text-gray-600 italic">Pending next run</div>
                    )}
                  </div>
                ))}
              </div>
            </section>

            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Recent Pipeline Runs</div>
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                {reports.slice(0, 7).map((r, i) => (
                  <div key={r.id} className="flex items-center justify-between px-4 py-3 border-b border-gray-800 text-sm">
                    <div className="flex items-center gap-3">
                      <span className="text-gray-600 text-xs w-6">#{i + 1}</span>
                      <span className="text-gray-200 line-clamp-1">{r.title}</span>
                    </div>
                    <div className="flex items-center gap-3 shrink-0">
                      <span className={`text-xs font-bold ${r.sentiment?.toLowerCase() === 'bearish' ? 'text-red-400' : r.sentiment?.toLowerCase() === 'bullish' ? 'text-green-400' : 'text-gray-400'}`}>
                        {r.sentiment?.toUpperCase()}
                      </span>
                      <span className={`text-xs font-bold ${(r.escalation_score || 0) >= 8 ? 'text-red-400' : (r.escalation_score || 0) >= 5 ? 'text-orange-400' : 'text-gray-500'}`}>
                        {(r.escalation_score || 0).toFixed(1)}/10
                      </span>
                      <span className="text-xs text-gray-600">
                        {new Date(r.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </section>
          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Weekly Digest | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}