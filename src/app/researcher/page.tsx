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
              <h1 className="text-xl font-bold text-green-300">📊 Pattern Intelligence</h1>
              <p className="text-xs text-gray-400">What patterns emerge over time and how reliable is GNI?</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Dev Console
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        

</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* Intro */}
        <div className="bg-green-950 border border-green-700 border-l-4 border-l-green-400 rounded-xl p-5 mb-6">
          <p className="text-sm text-gray-100 leading-relaxed">
            Pattern Intelligence is GNI&apos;s long-term research hub, designed for analysts and researchers who want to go beyond the latest report and understand how global intelligence evolves over time.
            Every pipeline run produces structured data -- escalation scores, sentiment scores, MAD verdicts, and confidence intervals -- all of which are tracked, stored, and available for deep analysis here.
            The GPVS (GNI Prediction Validation Standard) system continuously scores each agent&apos;s directional predictions against reality, building an evidence-based accuracy record over multiple horizons (7d, 30d, 180d).
            Confidence interval analysis using the t-distribution (t=4.303, n=3, alpha=0.05) provides statistical rigor to every sentiment score, making GNI&apos;s outputs IEEE paper-citable.
            All datasets are available for download via the Export API, enabling full replication of GNI&apos;s methodology for academic research and external validation.
          </p>
        </div>
        {/* Stats Row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-green-950 border border-green-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">{reports.length}</div>
            <div className="text-xs text-gray-500 mt-1">Total Pipeline Runs</div>
          </div>
          <div className="bg-green-950 border border-green-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">{avgEsc}</div>
            <div className="text-xs text-gray-500 mt-1">Avg Escalation Score</div>
          </div>
          <div className="bg-green-950 border border-green-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">{avgConf}%</div>
            <div className="text-xs text-gray-500 mt-1">Avg MAD Confidence</div>
          </div>
        </div>

        {/* Escalation Trend Sparkline */}
        {last7.length >= 2 && (
          <div className="bg-gray-900 border border-green-800 rounded-xl p-4 mb-6">
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
        <div className="text-xs text-green-400 uppercase tracking-wider mb-4 font-bold">Research Pages</div>
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">

          {/* History */}
          <a href="/history" className="bg-gray-900 border border-gray-700 hover:border-green-500 hover:bg-green-950 rounded-xl p-4 transition-colors group">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-bold text-green-400 bg-green-950 border border-green-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">01</span>
              <span className="text-lg">📋</span>
              <div className="text-sm font-bold text-white">History</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">{reports.length} pipeline runs are stored and available for analysis. Each run captures escalation score, sentiment score, MAD verdict, and confidence interval width. Scroll back through history to identify escalation patterns, trend reversals, and structural shifts over time.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-green-200 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 transition-colors">View History →</span>
            </div>
          </a>

          {/* Research */}
          <a href="/research" className="bg-gray-900 border border-gray-700 hover:border-green-500 hover:bg-green-950 rounded-xl p-4 transition-colors group">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-bold text-green-400 bg-green-950 border border-green-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">02</span>
              <span className="text-lg">🔬</span>
              <div className="text-sm font-bold text-white">Research</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">A full research workspace with escalation trend charts, confidence interval width over time, and per-agent MAD accuracy tracking. Compare how Bull, Bear, Black Swan, and Ostrich agents perform across different geopolitical conditions. Designed for deep statistical analysis and IEEE paper evidence gathering.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-green-200 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 transition-colors">View Research →</span>
            </div>
          </a>

          {/* Correlations */}
          <a href="/correlations" className="bg-gray-900 border border-gray-700 hover:border-green-500 hover:bg-green-950 rounded-xl p-4 transition-colors group">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-bold text-green-400 bg-green-950 border border-green-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">03</span>
              <span className="text-lg">📊</span>
              <div className="text-sm font-bold text-white">Correlations</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">Cross-horizon Forecast Analysis (CFA) tracks GNI prediction accuracy across three time horizons: 7-day, 30-day, and 180-day. Per-agent accuracy scores reveal which MAD agents perform best under different market conditions. This is the statistical proof layer for GNI&apos;s GPVS standard -- essential for IEEE paper validation.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-green-200 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 transition-colors">View Correlations →</span>
            </div>
          </a>

          {/* Weekly Digest */}
          <a href="/weekly-digest" className="bg-gray-900 border border-gray-700 hover:border-green-500 hover:bg-green-950 rounded-xl p-4 transition-colors group">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-bold text-green-400 bg-green-950 border border-green-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">04</span>
              <span className="text-lg">📅</span>
              <div className="text-sm font-bold text-white">Weekly Digest</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">Weekly digests compiled every Sunday provide a macro-level view of geopolitical escalation trends. Week-over-week escalation delta is one of GNI&apos;s most reliable structural trend signals -- consistent increases indicate sustained threat buildup. Use the digest time series to identify multi-week escalation cycles that single pipeline runs might miss.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-green-200 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 transition-colors">View Digest →</span>
            </div>
          </a>

          {/* Methodology */}
          <a href="/methodology" className="bg-gray-900 border border-gray-700 hover:border-green-500 hover:bg-green-950 rounded-xl p-4 transition-colors group">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-bold text-green-400 bg-green-950 border border-green-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">05</span>
              <span className="text-lg">📝</span>
              <div className="text-sm font-bold text-white">Methodology</div>
              <span className="text-xs bg-green-900 text-green-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400">Documents the complete scientific methodology behind GNI: the confidence interval formula using t-distribution (t=4.303, n=3, alpha=0.05), the Quadratic MAD agent design based on the Johari Window framework, and the GPVS prediction validation standard. All methodology is IEEE paper-citable and designed for academic peer review. Start here if you are writing a research paper that references GNI.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-green-200 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 transition-colors">View Methodology →</span>
            </div>
          </a>
          

          

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
