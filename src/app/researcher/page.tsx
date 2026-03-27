'use client'
import { useEffect, useState } from 'react'

interface ReportSummary {
  escalation_score: number
  sentiment_score: number
  created_at: string
  mad_confidence: number
}

export default function ResearcherHub() {
  const [reports, setReports] = useState<ReportSummary[]>([])

  useEffect(() => {
    fetch('/api/reports')
      .then(r => r.json())
      .then(data => setReports(data.reports || []))
      .catch(() => {})
  }, [])

  const last7 = reports.slice(0, 7).reverse()
  const avgEsc = reports.length > 0
    ? (reports.reduce((s, r) => s + (r.escalation_score || 0), 0) / reports.length).toFixed(2)
    : 'N/A'
  const avgConf = reports.length > 0
    ? Math.round(reports.reduce((s, r) => s + (r.mad_confidence || 0), 0) / reports.length * 100)
    : 0

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-green-300">\U0001f4ca Pattern Intelligence</h1>
              <p className="text-xs text-gray-400">What patterns emerge over time and how reliable is GNI?</p>
            </div>
            <a href="/" className="text-xs text-blue-400 border border-blue-800 hover:border-blue-500 rounded px-3 py-1 transition-colors">
              \u2190 Quantum Strategist
            </a>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              \U0001f3af Quantum Strategist
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              \U0001f9e0 Dev Console
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              \U0001f3af Feedback Loop
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              \U0001f31f About
            </a>
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
              🧠 Developer
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
          </div>
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 border border-green-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">{reports.length}</div>
            <div className="text-xs text-gray-500 mt-1">Total Pipeline Runs</div>
          </div>
          <div className="bg-gray-900 border border-green-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">{avgEsc}</div>
            <div className="text-xs text-gray-500 mt-1">Avg Escalation Score</div>
          </div>
          <div className="bg-gray-900 border border-green-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">{avgConf}%</div>
            <div className="text-xs text-gray-500 mt-1">Avg MAD Confidence</div>
          </div>
        </div>

        {/* Escalation Trend Sparkline */}
        {last7.length >= 2 && (
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 mb-6">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Escalation Trend -- Last 7 Runs</div>
            <svg width="100%" height="60" viewBox="0 0 400 60" preserveAspectRatio="none">
              <polyline
                points={last7.map((r, i) => {
                  const x = (i / (last7.length - 1)) * 400
                  const y = 60 - ((r.escalation_score || 0) / 10) * 60
                  return `${x},${y}`
                }).join(' ')}
                fill="none"
                stroke="#22c55e"
                strokeWidth="2"
                strokeLinejoin="round"
              />
            </svg>
            <div className="flex justify-between text-xs text-gray-600 mt-1">
              <span>Oldest</span><span>Latest</span>
            </div>
          </div>
        )}

        {/* Sub-page Hub Previews */}
        <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Research Pages</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">

          {/* History */}
          <a href="/history" className="bg-gray-900 border border-gray-700 hover:border-green-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-lg">\U0001f4cb</span>
              <div className="text-sm font-bold text-white">History</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">{reports.length} pipeline runs available. Scroll back to find escalation patterns over time.</p>
          </a>

          {/* Research */}
          <a href="/research" className="bg-gray-900 border border-gray-700 hover:border-green-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-lg">\U0001f52c</span>
              <div className="text-sm font-bold text-white">Research</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">Escalation trend charts, CI width over time, per-agent accuracy. Full research workspace.</p>
          </a>

          {/* Correlations */}
          <a href="/correlations" className="bg-gray-900 border border-gray-700 hover:border-green-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-lg">\U0001f4ca</span>
              <div className="text-sm font-bold text-white">Correlations</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">3-horizon CFA (7d/30d/180d). Per-agent accuracy. CI width analysis. Statistical proof layer.</p>
          </a>

          {/* Weekly Digest */}
          <a href="/weekly-digest" className="bg-gray-900 border border-gray-700 hover:border-green-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-lg">\U0001f4c5</span>
              <div className="text-sm font-bold text-white">Weekly Digest</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">Sunday digests as a time series. Week-over-week escalation delta = structural trend signal.</p>
          </a>

          {/* Methodology */}
          <a href="/methodology" className="bg-gray-900 border border-gray-700 hover:border-green-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-lg">\U0001f4dd</span>
              <div className="text-sm font-bold text-white">Methodology</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">CI formula (t=4.303, n=3). MAD agent design. GPVS standard. CFA horizon justification. IEEE-citable.</p>
          </a>

          {/* About */}
          <a href="/about" className="bg-gray-900 border border-gray-700 hover:border-green-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-lg">\U0001f31f</span>
              <div className="text-sm font-bold text-white">About GNI</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">$0.00 cost proof. Bloomberg comparison. L4 to L7 journey. SUM affiliation. Research context.</p>
          </a>

        </div>

        {/* API Export */}
        <div className="bg-gray-900 border border-green-800 rounded-xl p-4 mb-6">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-lg">\U0001f4e5</span>
            <div className="text-sm font-bold text-white">Dataset Export API</div>
            <span className="text-xs bg-yellow-900 text-yellow-300 px-2 py-0.5 rounded-full ml-auto">COMING SOON</span>
          </div>
          <p className="text-xs text-gray-400 mb-3">Download full GNI dataset for external analysis and IEEE paper replication.</p>
          <div className="space-y-1">
            <div className="font-mono text-xs text-green-400 bg-gray-800 rounded px-3 py-1.5">GET /api/export/reports?format=csv&days=30</div>
            <div className="font-mono text-xs text-green-400 bg-gray-800 rounded px-3 py-1.5">GET /api/export/predictions</div>
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Pattern Intelligence Hub | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
