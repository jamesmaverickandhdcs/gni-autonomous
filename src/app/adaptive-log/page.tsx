'use client'
import { useEffect, useState } from 'react'

interface AdaptiveRun {
  id: string
  pipeline: string
  tokens_used: number
  requests_used: number
  run_id: string
  created_at: string
}

interface AdaptiveReport {
  id: string
  title: string
  escalation_score: number
  escalation_level: string
  created_at: string
}

export default function AdaptiveLogPage() {
  const [runs, setRuns] = useState<AdaptiveRun[]>([])
  const [reports, setReports] = useState<AdaptiveReport[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/adaptive-log')
      .then(r => r.json())
      .then(data => {
        setRuns(data.runs || [])
        setReports(data.reports || [])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const totalTokens = runs.reduce((s, r) => s + (r.tokens_used || 0), 0)

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-4xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">&#x26A1; Adaptive Pipeline Log</h1>
              <p className="text-sm text-gray-400">Self-healing intelligence — every adaptive trigger with reason and tokens</p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300">&larr; Dashboard</a>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-blue-950 border border-blue-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-blue-400">{runs.length}</div>
              <div className="text-xs text-blue-600">Adaptive Runs</div>
            </div>
            <div className="bg-orange-950 border border-orange-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-orange-400">{totalTokens.toLocaleString()}</div>
              <div className="text-xs text-orange-600">Total Tokens</div>
            </div>
            <div className="bg-green-950 border border-green-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-green-400">{reports.length}</div>
              <div className="text-xs text-green-600">Reports Generated</div>
            </div>
          </div>
        </div>
      </header>

      <main className="max-w-4xl mx-auto px-6 py-8">
        {loading && <div className="text-center py-20 text-gray-400">Loading adaptive log...</div>}

        {!loading && runs.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">&#x26A1;</div>
            <p className="text-lg font-bold mb-2">No adaptive runs logged yet</p>
            <p className="text-sm max-w-md mx-auto">
              The adaptive pipeline fires when escalation delta &gt;= 2.0 or CRITICAL level detected.
              Each run is logged to groq_daily_usage with tokens consumed.
            </p>
            <div className="mt-6 bg-gray-900 border border-gray-700 rounded-xl p-5 text-left max-w-md mx-auto">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">How Self-Healing Works</div>
              <div className="space-y-3 text-xs text-gray-400">
                <div className="flex gap-3">
                  <span className="text-blue-400 font-bold shrink-0">1.</span>
                  <span>Heartbeat runs every 30 min — zero Groq calls (GNI-R-114)</span>
                </div>
                <div className="flex gap-3">
                  <span className="text-blue-400 font-bold shrink-0">2.</span>
                  <span>Detects escalation delta &gt;= 2.0 or CRITICAL level</span>
                </div>
                <div className="flex gap-3">
                  <span className="text-blue-400 font-bold shrink-0">3.</span>
                  <span>Triggers gni_adaptive.yml via GitHub Actions API</span>
                </div>
                <div className="flex gap-3">
                  <span className="text-blue-400 font-bold shrink-0">4.</span>
                  <span>Adaptive runs fresh analysis — 0 to 19 Groq calls based on level</span>
                </div>
                <div className="flex gap-3">
                  <span className="text-blue-400 font-bold shrink-0">5.</span>
                  <span>Sends Telegram alert with trigger reason and result</span>
                </div>
              </div>
            </div>
          </div>
        )}

        {!loading && runs.length > 0 && (
          <>
            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Adaptive Run Log</div>
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="grid grid-cols-4 gap-2 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase">
                  <div>Run</div>
                  <div className="text-right">Tokens</div>
                  <div className="text-right">Requests</div>
                  <div className="text-right">Time</div>
                </div>
                {runs.map((run, i) => (
                  <div key={run.id} className="grid grid-cols-4 gap-2 px-4 py-3 border-b border-gray-800 text-sm hover:bg-gray-800">
                    <div className="text-blue-400 font-bold text-xs">#{runs.length - i}</div>
                    <div className="text-right text-orange-400 font-bold text-xs">{(run.tokens_used || 0).toLocaleString()}</div>
                    <div className="text-right text-gray-400 text-xs">{run.requests_used || 0}</div>
                    <div className="text-right text-gray-500 text-xs">
                      {new Date(run.created_at).toLocaleDateString('en-US', {
                        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                      })}
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {reports.length > 0 && (
              <section>
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Reports Generated by Adaptive</div>
                <div className="space-y-3">
                  {reports.map(r => (
                    <div key={r.id} className="bg-gray-900 border border-blue-900 rounded-xl p-4">
                      <div className="flex items-center justify-between">
                        <div className="flex-1">
                          <div className="text-sm font-bold text-white">{r.title}</div>
                          <div className="text-xs text-gray-500 mt-1">
                            {new Date(r.created_at).toLocaleDateString('en-US', {
                              month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                            })}
                          </div>
                        </div>
                        <div className="text-right">
                          <div className={`text-sm font-bold ${(r.escalation_score || 0) >= 8 ? 'text-red-400' : (r.escalation_score || 0) >= 5 ? 'text-orange-400' : 'text-gray-400'}`}>
                            {(r.escalation_score || 0).toFixed(1)}/10
                          </div>
                          <div className="text-xs text-gray-500">{r.escalation_level}</div>
                        </div>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}
          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-4xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Adaptive Pipeline Log | Self-healing L3.5 | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}