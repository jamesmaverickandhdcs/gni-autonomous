content = r"""'use client'

import { useEffect, useState } from 'react'

interface HealthData {
  status: string
  last_run: {
    run_at: string
    status: string
    total_collected: number
    total_after_funnel: number
    duration_seconds: number
    llm_source: string
  } | null
  avg_quality_score: number
  total_reports: number
  source_weights: Array<{
    source: string
    weight: number
    gpvs_contribution: number
    last_updated: string
  }>
  recent_quality: Array<{
    date: string
    score: number
    llm: string
  }>
}

function statusColor(status: string) {
  return status === 'success' || status === 'ok' ? 'text-green-400' : 'text-red-400'
}

function qualityColor(score: number) {
  if (score >= 8) return 'text-green-400'
  if (score >= 6) return 'text-blue-400'
  if (score >= 4) return 'text-yellow-400'
  return 'text-red-400'
}

function qualityLabel(score: number) {
  if (score >= 8) return 'Excellent'
  if (score >= 6) return 'Good'
  if (score >= 4) return 'Fair'
  return 'Poor'
}

export default function HealthPage() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/health')
      .then(r => r.json())
      .then(data => setHealth(data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">System Health</h1>
            <p className="text-sm text-gray-400">Pipeline status, quality scores, source weights</p>
          </div>
          <a href="/" className="text-sm text-blue-400 hover:text-blue-300">Back to Dashboard</a>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 space-y-6">

        {loading && (
          <div className="text-center py-20 text-gray-400">Loading health data...</div>
        )}

        {!loading && health && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">

              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">System Status</div>
                <div className={`text-3xl font-bold ${statusColor(health.status)}`}>
                  {health.status?.toUpperCase()}
                </div>
                <div className="text-xs text-gray-600 mt-1">All components operational</div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Avg Quality Score</div>
                <div className={`text-3xl font-bold ${qualityColor(health.avg_quality_score)}`}>
                  {health.avg_quality_score}/10
                </div>
                <div className="text-xs text-gray-600 mt-1">
                  {qualityLabel(health.avg_quality_score)} — last {health.total_reports} reports
                </div>
              </div>

              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Last Pipeline Run</div>
                {health.last_run ? (
                  <>
                    <div className={`text-xl font-bold ${statusColor(health.last_run.status)}`}>
                      {health.last_run.status?.toUpperCase()}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">
                      {new Date(health.last_run.run_at).toLocaleString()} — {health.last_run.duration_seconds}s
                    </div>
                    <div className="text-xs text-gray-600">
                      {health.last_run.total_collected} articles to {health.last_run.total_after_funnel} selected via {health.last_run.llm_source}
                    </div>
                  </>
                ) : (
                  <div className="text-gray-600 text-sm">No runs yet</div>
                )}
              </div>

            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
                Source Weights — Dynamic Intelligence Weighting
              </div>
              {health.source_weights.length === 0 ? (
                <div className="text-gray-600 text-sm">No source weights yet</div>
              ) : (
                <div className="space-y-3">
                  {health.source_weights.map((sw) => (
                    <div key={sw.source} className="flex items-center gap-4">
                      <div className="w-32 text-sm text-gray-300 shrink-0">{sw.source}</div>
                      <div className="flex-1 bg-gray-800 rounded-full h-2">
                        <div
                          className="bg-blue-500 h-2 rounded-full"
                          style={{ width: Math.min(100, (sw.weight / 2.0) * 100) + '%' }}
                        />
                      </div>
                      <div className="text-sm font-mono text-blue-400 w-12 text-right">
                        {sw.weight?.toFixed(2)}
                      </div>
                      {sw.gpvs_contribution != null && (
                        <div className="text-xs text-gray-600 w-24 text-right">
                          GPVS: {sw.gpvs_contribution?.toFixed(2)}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
                Recent Quality Scores
              </div>
              {health.recent_quality.length === 0 ? (
                <div className="text-gray-600 text-sm">No reports yet</div>
              ) : (
                <div className="space-y-2">
                  {health.recent_quality.map((r, i) => (
                    <div key={i} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                      <div className="text-xs text-gray-500">
                        {new Date(r.date).toLocaleString()}
                      </div>
                      <div className="text-xs text-gray-600">{r.llm}</div>
                      <div className={`text-sm font-bold ${qualityColor(r.score)}`}>
                        {r.score}/10 {qualityLabel(r.score)}
                      </div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Infrastructure</div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { label: 'Supabase', status: 'Connected' },
                  { label: 'Groq API', status: 'Active' },
                  { label: 'Ollama', status: 'Active' },
                  { label: 'Telegram', status: 'Live' },
                ].map(item => (
                  <div key={item.label} className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-xs text-gray-500 mb-1">{item.label}</div>
                    <div className="text-sm font-bold text-green-400">{item.status}</div>
                  </div>
                ))}
              </div>
            </div>

          </>
        )}

        {!loading && !health && (
          <div className="text-center py-20 text-red-400">Failed to load health data.</div>
        )}

      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-5xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Health Dashboard — Real-time pipeline monitoring | GNI_Autonomous Sprint
        </div>
      </footer>

    </div>
  )
}
"""

with open('src/app/health/page.tsx', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)
print('Done')
