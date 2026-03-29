'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Report {
  id: string
  title: string
  sentiment: string
  sentiment_score: number
  mad_verdict: string
  mad_confidence: number
  escalation_score: number
  escalation_level: string
  created_at: string
  risk_level: string
}

const isDisagree = (sentiment: string, madVerdict: string): boolean => {
  const s = sentiment?.toLowerCase()
  const m = madVerdict?.toLowerCase()
  if (!s || !m) return false
  if (s === m) return false
  if (s === 'neutral' || m === 'neutral') return false
  return true
}

const sentimentColor = (s: string) => {
  switch (s?.toLowerCase()) {
    case 'bearish': return 'text-red-400'
    case 'bullish': return 'text-green-400'
    default: return 'text-gray-400'
  }
}

const sentimentIcon = (s: string) => {
  switch (s?.toLowerCase()) {
    case 'bearish': return '▼'
    case 'bullish': return '▲'
    default: return '◆'
  }
}

const riskColor = (risk: string) => {
  switch (risk?.toLowerCase()) {
    case 'critical': return 'bg-red-600 text-white'
    case 'high': return 'bg-orange-500 text-white'
    case 'medium': return 'bg-yellow-500 text-black'
    case 'low': return 'bg-green-500 text-white'
    default: return 'bg-gray-500 text-white'
  }
}

const escalationColor = (score: number) => {
  if (score >= 8) return 'text-red-400'
  if (score >= 6) return 'text-orange-400'
  if (score >= 4) return 'text-yellow-400'
  return 'text-green-400'
}

export default function ComparisonPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')
  const [filter, setFilter] = useState<'all' | 'disagree'>('all')

  useEffect(() => {
    fetch('/api/reports', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setReports(data.reports || []))
      .catch(() => setError('Failed to load data.'))
      .finally(() => setLoading(false))
  }, [])

  const latest = reports[0]
  const latestDisagree = latest ? isDisagree(latest.sentiment, latest.mad_verdict) : false
  const disagreeCount = reports.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length
  const agreeCount = reports.length - disagreeCount
  const filtered = filter === 'disagree'
    ? reports.filter(r => isDisagree(r.sentiment, r.mad_verdict))
    : reports

  const now = new Date()
  const daysAgo = (d: number) => new Date(now.getTime() - d * 24 * 60 * 60 * 1000)

  const inWindow = (r: Report, days: number) =>
    new Date(r.created_at) >= daysAgo(days)

  const trend7  = reports.filter(r => inWindow(r, 7))
  const trend15 = reports.filter(r => inWindow(r, 15))
  const trend30 = reports.filter(r => inWindow(r, 30))

  const disagree7  = trend7.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length
  const disagree15 = trend15.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length
  const disagree30 = trend30.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length

  const disagreeRate = (d: number, t: number) =>
    t === 0 ? 0 : Math.round((d / t) * 100)

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/" className="inline-flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Quantum Strategist</a>
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">&#x1F50D; Report vs Debate Comparison</h1>
              <p className="text-sm text-gray-400">When AI report and MAD debate disagree &mdash; that is the highest-value signal</p>
            </div>
          </div>
          {reports.length > 0 && (
            <div className="grid grid-cols-3 gap-3 mt-4">
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-white">{reports.length}</div>
                <div className="text-xs text-gray-500">Total Runs</div>
              </div>
              <div className="bg-green-950 border border-green-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-green-400">{agreeCount}</div>
                <div className="text-xs text-green-600">&#x2705; AGREE</div>
              </div>
              <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-red-400">{disagreeCount}</div>
                <div className="text-xs text-red-600">&#x26A0;&#xFE0F; DISAGREE</div>
              </div>
            </div>
          )}
          {reports.length > 0 && (
            <div className="mt-4 bg-gray-800 border border-gray-700 rounded-xl p-4">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">&#x26A0;&#xFE0F; DISAGREE Signal Trend</div>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: '7 Days', total: trend7.length, disagree: disagree7 },
                  { label: '15 Days', total: trend15.length, disagree: disagree15 },
                  { label: '30 Days', total: trend30.length, disagree: disagree30 },
                ].map(({ label, total, disagree }) => {
                  const rate = disagreeRate(disagree, total)
                  const barColor = rate >= 30 ? 'bg-red-500' : rate >= 15 ? 'bg-yellow-500' : 'bg-green-500'
                  return (
                    <div key={label}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-gray-400">{label}</span>
                        <span className={`font-bold ${rate >= 30 ? 'text-red-400' : rate >= 15 ? 'text-yellow-400' : 'text-green-400'}`}>
                          {disagree}/{total} runs ({rate}%)
                        </span>
                      </div>
                      <div className="h-2 bg-gray-700 rounded-full">
                        <div className={`h-2 rounded-full ${barColor}`} style={{ width: `${rate}%` }} />
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        {rate >= 30 ? 'High divergence' : rate >= 15 ? 'Moderate divergence' : 'Low divergence'}
                      </div>
                    </div>
                  )
                })}
              </div>
              <div className="mt-3 text-xs text-gray-600">
                Divergence rate above 30% = systematic disagreement between report AI and MAD debate. Investigate prompt quality or source bias.
              </div>
            </div>
          )}
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {loading && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">&#x231B;</div>
            <p>Loading comparison data...</p>
          </div>
        )}


        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">&#9888;&#65039;</div>
            <p>{error}</p>
          </div>
        )}
        {!loading && reports.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">&#x1F4E1;</div>
            <p>No reports yet. Pipeline runs at 02:00 and 10:00 UTC.</p>
          </div>
        )}

        {!loading && reports.length > 0 && (
          <>
            {/* Current Run */}
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Current Run &mdash; Latest Signal</div>

              {latestDisagree && (
                <div className="bg-red-950 border-2 border-red-500 rounded-xl p-4 mb-4 flex items-center gap-4">
                  <span className="text-3xl">&#x26A0;&#xFE0F;</span>
                  <div>
                    <div className="text-red-300 font-bold text-lg">DISAGREE SIGNAL DETECTED</div>
                    <div className="text-red-400 text-sm">
                      Report says <strong>{latest.sentiment?.toUpperCase()}</strong> but MAD debate says <strong>{latest.mad_verdict?.toUpperCase()}</strong>.
                      This divergence is the highest-value intelligence signal.
                    </div>
                  </div>
                </div>
              )}

              {!latestDisagree && latest && (
                <div className="bg-green-950 border border-green-800 rounded-xl p-4 mb-4 flex items-center gap-4">
                  <span className="text-2xl">&#x2705;</span>
                  <div>
                    <div className="text-green-300 font-bold">AGREE &mdash; Report and Debate Aligned</div>
                    <div className="text-green-500 text-sm">Both signals point {latest.sentiment?.toUpperCase()}. High confidence.</div>
                  </div>
                </div>
              )}

              {latest && (
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                  <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">&#x1F4CA; AI Report Analysis</div>
                    <div className="flex items-center gap-3 mb-4">
                      <span className={`text-2xl font-bold ${sentimentColor(latest.sentiment)}`}>
                        {sentimentIcon(latest.sentiment)} {latest.sentiment?.toUpperCase()}
                      </span>
                      <span className="text-gray-500 text-sm">score: {latest.sentiment_score?.toFixed(2)}</span>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500">Risk Level</span>
                        <span className={`font-bold px-2 py-0.5 rounded-full text-xs ${riskColor(latest.risk_level)}`}>
                          {latest.risk_level?.toUpperCase()}
                        </span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500">Escalation Score</span>
                        <span className={`font-bold ${escalationColor(latest.escalation_score)}`}>
                          {latest.escalation_score?.toFixed(1)}/10
                        </span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500">Generated</span>
                        <span className="text-gray-300">
                          {new Date(latest.created_at).toLocaleDateString('en-US', {
                            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                          })}
                        </span>
                      </div>
                    </div>
                  </div>

                  <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">&#x1F402;&#x1F43B;&#x1F9A2;&#x1F9A6; MAD Debate Verdict</div>
                    <div className="flex items-center gap-3 mb-4">
                      <span className={`text-2xl font-bold ${sentimentColor(latest.mad_verdict)}`}>
                        {sentimentIcon(latest.mad_verdict)} {latest.mad_verdict?.toUpperCase()}
                      </span>
                      <span className="text-gray-500 text-sm">
                        confidence: {latest.mad_confidence ? Math.round(latest.mad_confidence * 100) + '%' : 'N/A'}
                      </span>
                    </div>
                    <div className="mb-4">
                      <div className="flex justify-between text-xs text-gray-500 mb-1">
                        <span>MAD Confidence</span>
                        <span>{latest.mad_confidence ? Math.round(latest.mad_confidence * 100) + '%' : 'N/A'}</span>
                      </div>
                      <div className="h-2 bg-gray-800 rounded-full">
                        <div
                          className={`h-2 rounded-full ${latest.mad_confidence >= 0.7 ? 'bg-green-500' : latest.mad_confidence >= 0.5 ? 'bg-yellow-500' : 'bg-red-500'}`}
                          style={{ width: `${Math.round((latest.mad_confidence || 0) * 100)}%` }}
                        />
                      </div>
                    </div>
                    <div className="space-y-2">
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500">Escalation Level</span>
                        <span className={`font-bold ${escalationColor(latest.escalation_score)}`}>
                          {latest.escalation_level?.toUpperCase() ||
                            (latest.escalation_score >= 8 ? 'CRITICAL' :
                             latest.escalation_score >= 6 ? 'HIGH' :
                             latest.escalation_score >= 4 ? 'ELEVATED' : 'MODERATE')}
                        </span>
                      </div>
                      <div className="flex justify-between text-xs">
                        <span className="text-gray-500">Signal</span>
                        <span className={`font-bold px-2 py-0.5 rounded-full text-xs border ${
                          latestDisagree
                            ? 'bg-red-950 border-red-600 text-red-300'
                            : 'bg-green-950 border-green-600 text-green-300'
                        }`}>
                          {latestDisagree ? '⚠️ DISAGREE' : '✓ AGREE'}
                        </span>
                      </div>
                    </div>
                  </div>
                </div>
              )}
            </section>



            {/* Historical Timeline */}
            <section className="mb-8">
              <div className="flex items-center justify-between mb-3">
                <div className="text-xs text-gray-500 uppercase tracking-wider">Historical Timeline</div>
                <div className="flex gap-2">
                  <button
                    onClick={() => setFilter('all')}
                    className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                      filter === 'all'
                        ? 'bg-gray-700 border-gray-500 text-white'
                        : 'bg-gray-900 border-gray-700 text-gray-400 hover:border-gray-500'
                    }`}
                  >
                    All Runs
                  </button>
                  <button
                    onClick={() => setFilter('disagree')}
                    className={`text-xs px-3 py-1 rounded-full border transition-colors ${
                      filter === 'disagree'
                        ? 'bg-red-900 border-red-600 text-red-200'
                        : 'bg-gray-900 border-gray-700 text-gray-400 hover:border-red-700'
                    }`}
                  >
                    &#x26A0;&#xFE0F; DISAGREE Only ({disagreeCount})
                  </button>
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="grid grid-cols-12 gap-2 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase tracking-wider">
                  <div className="col-span-4">Report Title</div>
                  <div className="col-span-2 text-center">Report</div>
                  <div className="col-span-2 text-center">MAD Verdict</div>
                  <div className="col-span-2 text-center">Signal</div>
                  <div className="col-span-1 text-center">Escl.</div>
                  <div className="col-span-1 text-right">Date</div>
                </div>

                {filtered.length === 0 && (
                  <div className="text-center py-10 text-gray-600 text-sm">
                    No DISAGREE signals found yet.
                  </div>
                )}

                <div className="divide-y divide-gray-800">
                  {filtered.map((report, i) => {
                    const disagree = isDisagree(report.sentiment, report.mad_verdict)
                    return (
                      <div
                        key={report.id}
                        className={`grid grid-cols-12 gap-2 px-4 py-3 items-center text-xs transition-colors hover:bg-gray-800 ${
                          disagree ? 'bg-red-950 bg-opacity-30 border-l-2 border-red-600' : ''
                        }`}
                      >
                        <div className="col-span-4">
                          <div className="text-gray-200 font-medium line-clamp-1">{report.title}</div>
                          <div className="text-gray-600 text-xs mt-0.5">Run #{reports.length - i}</div>
                        </div>
                        <div className="col-span-2 text-center">
                          <span className={`font-bold ${sentimentColor(report.sentiment)}`}>
                            {sentimentIcon(report.sentiment)} {report.sentiment?.toUpperCase() || 'N/A'}
                          </span>
                          <div className="text-gray-600 mt-0.5">{report.sentiment_score?.toFixed(2)}</div>
                        </div>
                        <div className="col-span-2 text-center">
                          <span className={`font-bold ${sentimentColor(report.mad_verdict)}`}>
                            {sentimentIcon(report.mad_verdict)} {report.mad_verdict?.toUpperCase() || 'N/A'}
                          </span>
                          <div className="text-gray-600 mt-0.5">
                            {report.mad_confidence ? Math.round(report.mad_confidence * 100) + '%' : 'N/A'}
                          </div>
                        </div>
                        <div className="col-span-2 text-center">
                          {disagree ? (
                            <span className="bg-red-900 border border-red-600 text-red-300 px-2 py-0.5 rounded-full font-bold">
                              &#x26A0; DISAGREE
                            </span>
                          ) : (
                            <span className="bg-green-950 border border-green-800 text-green-500 px-2 py-0.5 rounded-full">
                              &#x2713; AGREE
                            </span>
                          )}
                        </div>
                        <div className="col-span-1 text-center">
                          <span className={`font-bold ${escalationColor(report.escalation_score)}`}>
                            {report.escalation_score?.toFixed(1) || 'N/A'}
                          </span>
                        </div>
                        <div className="col-span-1 text-right text-gray-500">
                          {new Date(report.created_at).toLocaleDateString('en-US', {
                            month: 'short', day: 'numeric'
                          })}
                        </div>
                      </div>
                    )
                  })}
                </div>
              </div>
              <div className="mt-3 text-xs text-gray-600 text-center">
                DISAGREE = Report sentiment and MAD debate verdict point in opposite directions. Highest-value intelligence signal.
              </div>
            </section>

            {/* Explanation */}
            <section className="mb-8">
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">&#x1F4A1; How to Read This Page</div>
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4 text-xs text-gray-400">
                  <div>
                    <div className="text-green-400 font-bold mb-1">&#x2705; AGREE Signal</div>
                    <p>The AI report analysis and the Quadratic MAD debate independently reached the same conclusion. High confidence directional signal.</p>
                  </div>
                  <div>
                    <div className="text-red-400 font-bold mb-1">&#x26A0;&#xFE0F; DISAGREE Signal</div>
                    <p>The report and debate diverge. MAD agents identified risks the consolidated report missed. Highest-value intelligence event &mdash; investigate further.</p>
                  </div>
                  <div>
                    <div className="text-yellow-400 font-bold mb-1">MAD Confidence</div>
                    <p>How strongly the 4 agents (Bull, Bear, Black Swan, Ostrich) agreed after 3 rounds. Above 70% = strong consensus. Below 50% = contested.</p>
                  </div>
                  <div>
                    <div className="text-orange-400 font-bold mb-1">Escalation Score</div>
                    <p>Pipeline escalation 0-10. Score 8+ = CRITICAL (runs every 30 min). Below 4 = LOW (12-hour interval).</p>
                  </div>
                </div>
              </div>
            </section>
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
          GNI Autonomous | Report vs Debate Comparison | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
