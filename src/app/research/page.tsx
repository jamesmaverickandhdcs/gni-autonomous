'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Report {
  id: string
  title: string
  quality_score: number
  sentiment: string
  escalation_score: number
  analysis_runs: number
  confidence_interval_width: number
  created_at: string
}

export default function ResearchPage() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/reports', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setReports(data.reports || []))
      .catch(() => setError('Failed to load data.'))
      .finally(() => setLoading(false))
  }, [])

  const avgQuality = reports.filter(r => r.quality_score > 0).length > 0
    ? (reports.filter(r => r.quality_score > 0).reduce((s, r) => s + r.quality_score, 0) / reports.filter(r => r.quality_score > 0).length).toFixed(2)
    : 'N/A'

  const avgCI = reports.filter(r => r.confidence_interval_width > 0).length > 0
    ? (reports.filter(r => r.confidence_interval_width > 0).reduce((s, r) => s + r.confidence_interval_width, 0) / reports.filter(r => r.confidence_interval_width > 0).length).toFixed(3)
    : 'N/A'

  const multiRunReports = reports.filter(r => r.analysis_runs > 1).length

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/researcher" className="inline-flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 text-green-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">← Pattern Intelligence</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">&#x1F52C; Research Data</h1>
            <p className="text-sm text-gray-400">GNI intelligence for academic and research use — IEEE paper evidence</p>
          </div>
</div>
          </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* Key Stats for IEEE paper */}
        
        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">&#9888;&#65039;</div>
            <p>{error}</p>
          </div>
        )}

<section className="mb-8">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Key Research Metrics — IEEE Paper Evidence</div>
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            {[
              { label: 'Total Reports', value: reports.length, color: 'text-white', desc: 'Intelligence reports generated' },
              { label: 'Avg Quality Score', value: avgQuality, color: 'text-green-400', desc: 'Out of 10.0 (5 dimensions)' },
              { label: 'Avg CI Width', value: avgCI, color: 'text-blue-400', desc: '95% confidence interval' },
              { label: 'Multi-Run Reports', value: multiRunReports, color: 'text-purple-400', desc: '3-run CI analysis' },
            ].map(s => (
              <div key={s.label} className="bg-gray-900 border border-gray-700 rounded-xl p-4 text-center">
                <div className={`text-2xl font-bold ${s.color}`}>{s.value}</div>
                <div className="text-xs text-gray-400 mt-1 font-bold">{s.label}</div>
                <div className="text-xs text-gray-600 mt-0.5">{s.desc}</div>
              </div>
            ))}
          </div>
        </section>

        {/* Novel Contributions */}
        <section className="mb-8">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">4 Novel Contributions — IEEE Paper</div>
          <div className="space-y-3">
            {[
              {
                num: '1', title: 'Quadratic MAD Protocol',
                desc: 'Four AI agents (Bull, Bear, Black Swan, Ostrich) debate across the Johari Window matrix (Known/Unknown × Proactive/Ignored). After 3 rounds with Arbitrator coaching, a final verdict is reached. First application of Johari Window to AI geopolitical intelligence.',
                color: 'border-red-800 bg-red-950', accent: 'text-red-400'
              },
              {
                num: '2', title: 'GPVS — GNI Prediction Validation Standard',
                desc: 'Every MAD debate generates short (7d), medium (30d), and long (180d) horizon predictions. After verify dates, actual SPY market movement is compared. Correct predictions increase source trust weights via EMA. First automated geopolitical prediction validation framework.',
                color: 'border-blue-800 bg-blue-950', accent: 'text-blue-400'
              },
              {
                num: '3', title: 'CI-Augmented Sentiment Analysis',
                desc: 'Three independent LLM runs at different temperatures (0.1, 0.3, 0.7) generate 95% confidence intervals for sentiment scores. Uses t-distribution (t=4.303 for n=3). Adds statistical rigor to qualitative AI analysis. First CI framework for LLM-based geopolitical sentiment.',
                color: 'border-green-800 bg-green-950', accent: 'text-green-400'
              },
              {
                num: '4', title: '$0.00/month Autonomous Operation',
                desc: 'Full geopolitical intelligence platform running 4 autonomous pipelines (gni_pipeline, gni_mad, gni_heartbeat, gni_adaptive) entirely on free tiers. Groq 100K tokens/day + Supabase 500MB + Vercel + GitHub Actions. Zero cost, unlimited operation. Challenges assumption that AI research requires paid infrastructure.',
                color: 'border-yellow-800 bg-yellow-950', accent: 'text-yellow-400'
              },
            ].map(c => (
              <div key={c.num} className={`border rounded-xl p-5 ${c.color}`}>
                <div className="flex items-start gap-4">
                  <div className={`text-3xl font-bold ${c.accent} shrink-0`}>#{c.num}</div>
                  <div>
                    <div className={`text-sm font-bold mb-2 ${c.accent}`}>{c.title}</div>
                    <p className="text-xs text-gray-300 leading-relaxed">{c.desc}</p>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* Report quality table */}
        {!loading && reports.length > 0 && (
          <section className="mb-8">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Report Quality Log — Research Dataset</div>
            <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
              <div className="grid grid-cols-5 gap-2 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase">
                <div className="col-span-2">Report</div>
                <div className="text-center">Quality</div>
                <div className="text-center">CI Width</div>
                <div className="text-center">Runs</div>
              </div>
              {reports.map(r => (
                <div key={r.id} className="grid grid-cols-5 gap-2 px-4 py-3 border-b border-gray-800 text-xs hover:bg-gray-800">
                  <div className="col-span-2 text-gray-200 line-clamp-1">{r.title}</div>
                  <div className="text-center">
                    <span className={`font-bold ${r.quality_score >= 8 ? 'text-green-400' : r.quality_score >= 6 ? 'text-yellow-400' : r.quality_score > 0 ? 'text-red-400' : 'text-gray-600'}`}>
                      {r.quality_score > 0 ? r.quality_score.toFixed(1) : 'N/A'}
                    </span>
                  </div>
                  <div className="text-center text-blue-400 font-mono">
                    {r.confidence_interval_width > 0 ? r.confidence_interval_width.toFixed(3) : '—'}
                  </div>
                  <div className="text-center text-gray-400">{r.analysis_runs || 1}</div>
                </div>
              ))}
            </div>
            <div className="mt-2 text-xs text-gray-600 leading-relaxed">
              Quality score requires 3 independent pipeline runs for CI analysis (t-distribution, n=3). Single-run reports show N/A until re-analysed.
            </div>
          </section>
        )}

        {/* Free tier proof */}
        <section>
          <div className="bg-green-950 border border-green-800 rounded-xl p-5">
            <div className="text-sm font-bold text-green-300 mb-3">&#x1F4B0; $0.00/month — Free Tier Architecture</div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs text-center">
              {[
                { service: 'Groq', detail: '100K tokens/day', cost: '$0' },
                { service: 'Supabase', detail: '500MB PostgreSQL', cost: '$0' },
                { service: 'Vercel', detail: 'Next.js hosting', cost: '$0' },
                { service: 'GitHub', detail: 'Actions + repo', cost: '$0' },
              ].map(s => (
                <div key={s.service} className="bg-green-900 rounded-lg p-3">
                  <div className="font-bold text-green-300 text-sm">{s.cost}</div>
                  <div className="text-green-400 font-bold">{s.service}</div>
                  <div className="text-gray-400">{s.detail}</div>
                </div>
              ))}
            </div>
          </div>
        </section>
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
          GNI Autonomous | Research Data | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}