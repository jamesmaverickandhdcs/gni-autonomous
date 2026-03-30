'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Report {
  title: string
  sentiment: string
  sentiment_score: number
  escalation_score: number
  escalation_level: string
  mad_verdict: string
  mad_confidence: number
  mad_action_recommendation: string
  mad_blind_spot: string
  created_at: string
  risk_level: string
}
interface SourceWeight { source: string; weight: number; gpvs_score: number }

export default function AboutQuantumPage() {
  const [report, setReport] = useState<Report | null>(null)
  const [weights, setWeights] = useState<SourceWeight[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      fetch('/api/reports', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
      fetch('/api/source-weights', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
    ]).then(([rData, wData]) => {
      const reports = rData.reports || []
      if (reports.length > 0) setReport(reports[0])
      setWeights((wData.weights || []).slice(0, 5))
    }).catch(() => setError('Failed to load live data.')).finally(() => setLoading(false))
  }, [])

  const sColor = (s: string) => s?.toLowerCase() === 'bearish' ? 'text-red-400' : s?.toLowerCase() === 'bullish' ? 'text-green-400' : 'text-yellow-400'
  const vColor = (v: string) => v === 'bearish' ? 'bg-red-900 border-red-700 text-red-300' : v === 'bullish' ? 'bg-green-900 border-green-700 text-green-300' : 'bg-gray-800 border-gray-600 text-gray-300'

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/about" className="inline-flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">Back to About</a>
          <h1 className="text-2xl font-bold text-blue-400">Quantum Strategist -- Outcomes</h1>
          <p className="text-sm text-gray-400">What GNI decides, why it decides it, and what it means for global markets. This page shows the Quantum Strategist perspective -- actionable intelligence outcomes from the MAD Protocol, real-time threat verdicts, and market implications from 25 global news sources running 2x daily.</p>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        <div className="bg-blue-950 border border-blue-800 rounded-xl p-6">
          <div className="text-xs text-blue-400 uppercase tracking-wider mb-3">The Quantum Strategist Philosophy</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title: 'Speed over Perfection', desc: 'GNI delivers actionable intelligence within minutes of pipeline completion. In geopolitical risk, timeliness beats completeness. A verdict with 80% confidence delivered now beats a perfect analysis delivered tomorrow.' },
              { title: 'Multi-Agent Consensus', desc: 'No single AI perspective is trusted. Four agents -- Bull, Bear, Black Swan, Ostrich -- debate every scenario across the Johari Window framework. Only consensus after 3 coached rounds becomes a verdict.' },
              { title: 'Market-Linked Intelligence', desc: 'Every report connects geopolitical events to specific market instruments (SPY, GLD, USO, DXY). Intelligence without market linkage is academic. GNI links threat verdicts directly to investment implications.' },
            ].map(item => (
              <div key={item.title} className="bg-blue-900 bg-opacity-40 rounded-lg p-4">
                <div className="text-sm font-bold text-blue-300 mb-2">{item.title}</div>
                <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Live Latest MAD Verdict</div>
          {loading && <div className="text-center py-8 text-gray-500">Loading live data...</div>}
          {error && <div className="text-center py-8 text-red-400">{error}</div>}
          {!loading && report && (
            <div className="space-y-4">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div className="flex-1">
                  <h2 className="text-lg font-bold text-white mb-1">{report.title}</h2>
                  <p className="text-xs text-gray-500">{new Date(report.created_at).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
                </div>
                <div className={"px-4 py-2 rounded-lg border font-bold text-sm " + vColor(report.mad_verdict)}>
                  {report.mad_verdict?.toUpperCase() || 'PENDING'} {report.mad_confidence ? Math.round(report.mad_confidence * 100) + '%' : ''}
                </div>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { label: 'Sentiment', value: report.sentiment, color: sColor(report.sentiment) },
                  { label: 'Score', value: report.sentiment_score?.toFixed(2), color: 'text-white' },
                  { label: 'Escalation', value: (report.escalation_score?.toFixed(1) || '0') + '/10', color: 'text-orange-400' },
                  { label: 'Risk Level', value: report.risk_level?.toUpperCase(), color: 'text-yellow-400' },
                ].map(item => (
                  <div key={item.label} className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className={"text-lg font-bold " + item.color}>{item.value}</div>
                    <div className="text-xs text-gray-500 mt-1">{item.label}</div>
                  </div>
                ))}
              </div>
              {report.mad_action_recommendation && (
                <div className="bg-blue-950 border border-blue-800 rounded-lg p-4">
                  <div className="text-xs text-blue-400 font-bold uppercase mb-2">Action Recommendation</div>
                  <p className="text-sm text-white leading-relaxed">{report.mad_action_recommendation}</p>
                </div>
              )}
              {report.mad_blind_spot && (
                <div className="bg-purple-950 border border-purple-800 rounded-lg p-4">
                  <div className="text-xs text-purple-400 font-bold uppercase mb-2">Blind Spot Warning</div>
                  <p className="text-sm text-gray-300 leading-relaxed">{report.mad_blind_spot}</p>
                </div>
              )}
            </div>
          )}
          {!loading && !report && !error && (
            <div className="text-center py-8 text-gray-500">No reports available yet.</div>
          )}
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Outcome Framework -- What QS Produces</div>
          <div className="space-y-3">
            {[
              { step: '01', title: 'Threat Verdict', desc: 'BEARISH / BULLISH / NEUTRAL with confidence score 0-100%. Derived from 3 rounds of 4-agent MAD debate using Johari Window framework. Each verdict includes Arbitrator reasoning and coaching notes.' },
              { step: '02', title: 'Action Recommendation', desc: 'Specific diplomatic, economic, or strategic action for the next 4-6 weeks. Geopolitical posture recommendation based on full threat assessment across all four agent perspectives.' },
              { step: '03', title: 'Blind Spot Warning', desc: 'The Black Swan agent identifies one weak signal that all other agents are ignoring. This is the highest-value intelligence output -- the thing nobody else is watching but should be.' },
              { step: '04', title: 'Market Implications', desc: 'Specific tickers (SPY, GLD, USO, DXY) with directional bias. Links geopolitical threat directly to investable market instruments with sentiment scoring.' },
              { step: '05', title: 'Scenario Planning', desc: 'Base, Upside, and Downside scenarios with probability weights. Allows decision-makers to prepare for multiple futures simultaneously across 7-30 day and 3-24 month horizons.' },
            ].map(item => (
              <div key={item.step} className="flex gap-4 bg-gray-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-600 shrink-0 w-10 text-center">{item.step}</div>
                <div>
                  <div className="text-sm font-bold text-blue-300 mb-1">{item.title}</div>
                  <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {!loading && weights.length > 0 && (
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Top Intelligence Sources (Live GPVS Weights)</div>
            <div className="space-y-2">
              {weights.map((w, i) => (
                <div key={w.source} className="flex items-center gap-3 bg-gray-800 rounded-lg px-4 py-3">
                  <div className="text-sm font-bold text-gray-500 w-6">{i + 1}</div>
                  <div className="flex-1 text-sm font-bold text-white">{w.source}</div>
                  <div className="text-xs text-gray-400">GPVS: {w.gpvs_score ? (w.gpvs_score * 100).toFixed(0) + '%' : 'N/A'}</div>
                  <div className="text-sm font-bold text-green-400">Weight: {w.weight?.toFixed(2)}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="bg-gray-900 border border-yellow-800 rounded-xl p-6">
          <div className="text-xs text-yellow-600 uppercase tracking-wider mb-3">Academic Contribution -- Novel Contribution 1</div>
          <p className="text-sm text-gray-300 leading-relaxed mb-3">The Quantum Strategist represents Novel Contribution 1 in GNI&apos;s IEEE paper: the application of the Johari Window framework to AI-based geopolitical threat assessment. The four-quadrant Known/Unknown x Proactive/Ignored matrix provides a systematic way to ensure no threat dimension is overlooked.</p>
          <p className="text-sm text-gray-400 leading-relaxed">This approach goes beyond standard sentiment analysis by explicitly modeling what the system does not know (Black Swan) and what institutions are actively ignoring (Ostrich) -- dimensions absent from conventional intelligence platforms like Bloomberg Terminal or Stratfor.</p>
        </div>

      </main>
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">Warning: GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.</p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | About -- Quantum Strategist | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
