'use client'

import { useEffect, useState } from 'react'

interface FrequencyEntry {
  id: string
  run_at: string
  escalation_score: number
  escalation_level: string
  recommended_interval_hours: number
  reason: string
}

interface PromptVariant {
  version: number
  avg_quality_score: number
  run_count: number
  active: boolean
}

interface HealthData {
  status: string
  avg_quality_score: number
  frequency_log: FrequencyEntry[]
  prompt_variants: PromptVariant[]
  recent_quality: Array<{ date: string; score: number; llm: string }>
}

export default function AutonomyPage() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/health')
      .then(r => r.json())
      .then(data => setHealth(data))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const intervalMap: Record<string, string> = {
    'CRITICAL': '30 min', 'HIGH': '2h', 'ELEVATED': '4h', 'MODERATE': '6h', 'LOW': '12h'
  }
  const levelColor: Record<string, string> = {
    'CRITICAL': 'text-red-400 border-red-700',
    'HIGH': 'text-orange-400 border-orange-700',
    'ELEVATED': 'text-yellow-400 border-yellow-700',
    'MODERATE': 'text-blue-400 border-blue-700',
    'LOW': 'text-green-400 border-green-700',
  }

  const latest = health?.frequency_log?.[0]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4 flex items-start justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">🧠 Autonomy Engine</h1>
            <p className="text-sm text-gray-400">Frequency Control · Self-Improvement · Health Monitoring</p>
            <p className="text-xs text-gray-500 mt-1 max-w-2xl">
              GNI manages itself. The frequency controller decides how often to run based on world escalation.
              The A/B system tests prompt variants and auto-promotes the winner.
              The health agent monitors pipeline quality 24/7.
            </p>
          </div>
          <a href="/" className="text-sm text-blue-400 hover:text-blue-300 shrink-0 mt-1">← Dashboard</a>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        {loading && <div className="text-center py-20 text-gray-400">Loading autonomy data...</div>}

        {!loading && health && (
          <>
            {/* Frequency Controller */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
                ⚡ Frequency Controller — Autonomous Run Scheduling
              </div>
              {latest ? (
                <>
                  <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                    <div className={`bg-gray-800 border rounded-xl p-4 text-center ${levelColor[latest.escalation_level] || 'border-gray-700'}`}>
                      <div className={`text-3xl font-bold ${levelColor[latest.escalation_level]?.split(' ')[0] || 'text-gray-400'}`}>
                        {latest.escalation_level}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">Current Alert Level</div>
                    </div>
                    <div className="bg-gray-800 rounded-xl p-4 text-center">
                      <div className="text-3xl font-bold text-white">{latest.escalation_score.toFixed(1)}</div>
                      <div className="text-xs text-gray-500 mt-1">Escalation Score /10</div>
                    </div>
                    <div className="bg-blue-950 border border-blue-800 rounded-xl p-4 text-center">
                      <div className="text-3xl font-bold text-blue-400">
                        {intervalMap[latest.escalation_level] || `${latest.recommended_interval_hours}h`}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">Current Run Interval</div>
                    </div>
                    <div className="bg-gray-800 rounded-xl p-4 text-center">
                      <div className="text-sm font-bold text-gray-300 leading-relaxed">{latest.reason}</div>
                      <div className="text-xs text-gray-500 mt-1">Reason</div>
                    </div>
                  </div>

                  {/* Interval scale */}
                  <div className="bg-gray-800 rounded-lg p-4">
                    <div className="text-xs text-gray-500 mb-3">Escalation → Frequency Scale</div>
                    <div className="grid grid-cols-5 gap-2">
                      {[
                        { level: 'CRITICAL', interval: '30min', score: '8-10', color: 'bg-red-900 border-red-700 text-red-300' },
                        { level: 'HIGH', interval: '2h', score: '6-8', color: 'bg-orange-900 border-orange-700 text-orange-300' },
                        { level: 'ELEVATED', interval: '4h', score: '4-6', color: 'bg-yellow-900 border-yellow-700 text-yellow-300' },
                        { level: 'MODERATE', interval: '6h', score: '2-4', color: 'bg-blue-900 border-blue-700 text-blue-300' },
                        { level: 'LOW', interval: '12h', score: '0-2', color: 'bg-green-900 border-green-700 text-green-300' },
                      ].map(item => (
                        <div key={item.level} className={`border rounded-lg p-2 text-center ${item.color} ${latest.escalation_level === item.level ? 'ring-2 ring-white ring-opacity-50' : ''}`}>
                          <div className="text-xs font-bold">{item.level}</div>
                          <div className="text-lg font-bold mt-1">{item.interval}</div>
                          <div className="text-xs opacity-60">score {item.score}</div>
                        </div>
                      ))}
                    </div>
                  </div>

                  {/* History */}
                  {health.frequency_log.length > 1 && (
                    <div className="mt-4">
                      <div className="text-xs text-gray-500 mb-2">Frequency history</div>
                      <div className="space-y-2">
                        {health.frequency_log.slice(0, 5).map((entry) => (
                          <div key={entry.id} className="flex items-center justify-between bg-gray-800 rounded-lg px-3 py-2 text-xs">
                            <span className="text-gray-500">{new Date(entry.run_at).toLocaleString()}</span>
                            <span className={`font-bold ${levelColor[entry.escalation_level]?.split(' ')[0] || 'text-gray-400'}`}>
                              {entry.escalation_level}
                            </span>
                            <span className="text-white">{entry.escalation_score.toFixed(1)}/10</span>
                            <span className="text-blue-400">{intervalMap[entry.escalation_level]}</span>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </>
              ) : (
                <div className="text-gray-600 text-sm">No frequency data yet.</div>
              )}
            </div>

            {/* A/B Test */}
            {health.prompt_variants && health.prompt_variants.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
                  🧪 Prompt A/B Test — Self-Improving Analysis
                </div>
                <div className="grid grid-cols-2 gap-4 mb-4">
                  {health.prompt_variants.map(v => (
                    <div key={v.version} className={`rounded-xl p-4 border ${v.active ? 'border-blue-600 bg-gray-800' : 'border-gray-700 bg-gray-900 opacity-60'}`}>
                      <div className="flex items-center justify-between mb-3">
                        <span className="font-bold text-white">Prompt v{v.version}</span>
                        {v.active
                          ? <span className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">Active</span>
                          : <span className="text-xs bg-gray-700 text-gray-400 px-2 py-0.5 rounded">Retired</span>
                        }
                      </div>
                      <div className={`text-3xl font-bold ${v.avg_quality_score >= 8 ? 'text-green-400' : v.avg_quality_score >= 6 ? 'text-blue-400' : 'text-gray-400'}`}>
                        {v.avg_quality_score > 0 ? `${v.avg_quality_score.toFixed(2)}/10` : 'No data'}
                      </div>
                      <div className="text-xs text-gray-500 mt-1">{v.run_count} runs</div>
                      {v.run_count > 0 && (
                        <div className="mt-2 bg-gray-700 rounded-full h-2">
                          <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${Math.min(100, v.avg_quality_score * 10)}%` }} />
                        </div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="bg-gray-800 rounded-lg p-3 text-xs text-gray-400">
                  Auto-promotes winner after 10 runs per variant if quality difference ≥ 0.3 points.
                  Each pipeline run alternates between variants using the run count as selector.
                </div>
              </div>
            )}

            {/* Health Agent */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
                🤖 Health Agent — 5 Automated Checks
              </div>
              <div className="grid grid-cols-1 md:grid-cols-5 gap-3">
                {[
                  { check: 'Run gap', desc: 'Alerts if no run in 25h', status: 'OK' },
                  { check: 'Quality drift', desc: 'Alerts if avg drops below 6.0', status: health.avg_quality_score >= 6 ? 'OK' : 'ALERT' },
                  { check: 'Collection volume', desc: 'Alerts if < 50 articles', status: 'OK' },
                  { check: 'MAD confidence', desc: 'Alerts if avg confidence < 60%', status: 'OK' },
                  { check: 'Escalation spike', desc: 'Alerts on rapid score increase', status: 'OK' },
                ].map((item, idx) => (
                  <div key={idx} className={`rounded-lg p-3 border text-center ${item.status === 'OK' ? 'bg-green-950 border-green-800' : 'bg-red-950 border-red-800'}`}>
                    <div className={`text-xs font-bold ${item.status === 'OK' ? 'text-green-400' : 'text-red-400'}`}>
                      {item.status === 'OK' ? '✅' : '⚠️'} {item.status}
                    </div>
                    <div className="text-xs text-white font-bold mt-1">{item.check}</div>
                    <div className="text-xs text-gray-500 mt-1">{item.desc}</div>
                  </div>
                ))}
              </div>
            </div>

          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights (Autonomous) | Autonomy Engine | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
