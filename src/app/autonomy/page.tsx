'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''

import { useEffect, useState } from 'react'

interface FrequencyEntry {
  id: string
  run_at: string
  escalation_score: number
  recommended_interval_hours: number
  escalation_level: string
  reason: string
}

interface PromptVariant {
  version: number
  avg_quality_score: number
  run_count: number
  active: boolean
}

interface EscalationData {
  escalation_score: number
  escalation_score_raw: number | null
  escalation_score_lower: number | null
  escalation_score_upper: number | null
  title: string
  created_at: string
}

interface HealthData {
  status: string
  avg_quality_score: number
  frequency_log: FrequencyEntry[]
  prompt_variants: PromptVariant[]
  recent_quality: Array<{ date: string; score: number; llm: string }>
  latest_escalation: EscalationData | null
}

// No score->level ladder lives here. escalation_level is READ from frequency_log,
// written by frequency_controller.py:104. Item 9.10 (S90) - this was the last
// frontend copy of the 9/7/5/3 ladder. A blank level hides the card rather than
// publishing a derived guess; that is deliberate.

export default function AutonomyPage() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/health', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setHealth(data))
      .catch(() => setError('Failed to load data.'))
      .finally(() => setLoading(false))
  }, [])

  // The MEASURED interval, as frequency_controller.py:104 stored it. Sub-hour
  // values render as minutes so 0.5 reads '30 min'. intervalMap below is only a
  // fallback for a missing value - it is the SCHEDULER's band table, not a
  // measurement, and at 9.0-9.4 it says '30 min' where the stored value is 1h.
  const formatInterval = (h: number): string =>
    h < 1 ? `${Math.round(h * 60)} min` : `${h}h`

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

  const levels = [
    { level: 'CRITICAL', score: '9–10', interval: '30 min', color: 'text-red-400 border-red-700' },
    { level: 'HIGH',     score: '7–9',  interval: '2h',     color: 'text-orange-400 border-orange-700' },
    { level: 'ELEVATED', score: '5–7',  interval: '4h',     color: 'text-yellow-400 border-yellow-700' },
    { level: 'MODERATE', score: '3–5',  interval: '6h',     color: 'text-blue-400 border-blue-700' },
    { level: 'LOW',      score: '0–3',  interval: '12h',    color: 'text-green-400 border-green-700' },
  ]

  const latest = health?.frequency_log?.[0]
  const latestLevel = latest?.escalation_level || null

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/developer-hub" className="inline-flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">← Dev Console</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">🧠 Autonomy Engine</h1>
            <p className="text-sm text-gray-400">Frequency Control · Self-Improvement · Health Monitoring</p>
            <p className="text-xs text-gray-500 mt-1 max-w-6xl">
              GNI manages itself. The frequency controller decides how often to run based on world escalation.
              The A/B system tests prompt variants and auto-promotes the winner.
              The health agent monitors pipeline quality 24/7.
            </p>
          </div>
</div>
          </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-8">

        {loading && <div className="text-center py-20 text-gray-400">Loading autonomy data...</div>}


        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">&#9888;&#65039;</div>
            <p>{error}</p>
          </div>
        )}
        {health && (
          <>
            {/* Current Frequency Status */}
            {latest && latestLevel && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-6">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">⚡ Frequency Controller — Autonomous Run Scheduling</div>
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                  <div className={`bg-gray-800 border rounded-xl p-4 text-center ${levelColor[latestLevel] || 'border-gray-700'}`}>
                    <div className={`text-3xl font-bold ${levelColor[latestLevel]?.split(' ')[0] || 'text-gray-400'}`}>
                      {latestLevel}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Current Level</div>
                  </div>
                  <div className="bg-gray-800 border border-gray-700 rounded-xl p-4 text-center">
                    <div className="text-3xl font-bold text-white">{latest.escalation_score.toFixed(1)}</div>
                    <div className="text-xs text-gray-500 mt-1">Escalation Score</div>
                  </div>
                  <div className="bg-gray-800 border border-blue-800 rounded-xl p-4 text-center">
                    <div className="text-3xl font-bold text-blue-400">
                      {latest.recommended_interval_hours != null ? formatInterval(latest.recommended_interval_hours) : intervalMap[latestLevel]}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Run Interval</div>
                  </div>
                  <div className="bg-gray-800 border border-gray-700 rounded-xl p-4 text-center">
                    <div className="text-sm font-bold text-gray-300">{latestLevel} {latest.escalation_score.toFixed(1)}/10</div>
                    <div className="text-xs text-gray-500 mt-1">Reason</div>
                  </div>
                </div>
                <div className="mt-3 text-xs text-gray-600 text-center">
                  CRITICAL=30min · HIGH=2h · ELEVATED=4h · MODERATE=6h · LOW=12h — AI decides run frequency autonomously
                </div>
              </div>
            )}

            {/* Frequency Level Reference */}
            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Frequency Level Reference</div>
              <div className="grid grid-cols-5 gap-2">
                {levels.map(item => (
                  <div key={item.level} className={`border rounded-lg p-2 text-center ${item.color} ${latestLevel === item.level ? 'ring-2 ring-white ring-opacity-50' : ''}`}>
                    <div className="text-sm font-bold">{item.level}</div>
                    <div className="text-xs text-gray-500">{item.score}</div>
                    <div className="text-xs font-bold mt-1">{item.interval}</div>
                  </div>
                ))}
              </div>
            </div>

            {/* Escalation Evidence -- GNI-R-117 */}
            {health.latest_escalation && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Escalation Evidence — Score Breakdown (GNI-R-117)</div>
                <div className="mb-3">
                  <div className="text-xs text-gray-500 mb-1">Latest Report</div>
                  <div className="text-sm text-gray-300">{health.latest_escalation.title}</div>
                  <div className="text-xs text-gray-600 mt-1">{new Date(health.latest_escalation.created_at).toLocaleString()}</div>
                </div>
                <div className="grid grid-cols-3 gap-3 mb-4">
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-white">{health.latest_escalation.escalation_score?.toFixed(1)}</div>
                    <div className="text-xs text-gray-500 mt-1">Final Score</div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-blue-400">
                      {health.latest_escalation.escalation_score_raw?.toFixed(1) ?? '--'}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Raw Magnitude (uncapped)</div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-orange-400">
                      {health.latest_escalation.escalation_score_upper?.toFixed(1) ?? '--'}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Upper Bound</div>
                  </div>
                </div>
                <div className="text-xs text-gray-600 text-center">
                  Final score is capped at 10 and has been at the cap on every measured run. Raw magnitude is the uncapped signal.
                </div>
              </div>
            )}

            {/* Frequency Log History */}
            {health.frequency_log.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Recent Frequency Log</div>
                <div className="space-y-2">
                  {health.frequency_log.slice(0, 10).map(entry => {
                    const entryLevel = entry.escalation_level
                    return (
                      <div key={entry.id} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                        <span className="text-xs text-gray-500">{new Date(entry.run_at).toLocaleString()}</span>
                        <span className={`font-bold ${levelColor[entryLevel]?.split(' ')[0] || 'text-gray-400'}`}>
                          {entryLevel}
                        </span>
                        <span className="text-white">{entry.escalation_score.toFixed(1)}/10</span>
                        <span className="text-blue-400">{entry.recommended_interval_hours != null ? formatInterval(entry.recommended_interval_hours) : intervalMap[entryLevel]}</span>
                      </div>
                    )
                  })}
                </div>
              </div>
            )}

            {/* Divergent intervals: measured value differs from the published band.
                Selected by divergence, not position - an absolute window decays as the
                table grows. Uses intervalMap, the existing published table; no new ladder. */}
            {health.frequency_log.filter(e => e.recommended_interval_hours != null && formatInterval(e.recommended_interval_hours) !== intervalMap[e.escalation_level]).length > 0 && (
              <div className="bg-gray-900 border border-yellow-800 rounded-xl p-5">
                <div className="text-xs text-yellow-500 uppercase tracking-wider mb-4">Measured Interval Differs From Published Band</div>
                <div className="space-y-2">
                  {health.frequency_log.filter(e => e.recommended_interval_hours != null && formatInterval(e.recommended_interval_hours) !== intervalMap[e.escalation_level]).slice(0, 5).map(entry => (
                    <div key={entry.id} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                      <span className="text-xs text-gray-500">{new Date(entry.run_at).toLocaleString()}</span>
                      <span className={`font-bold ${levelColor[entry.escalation_level]?.split(' ')[0] || 'text-gray-400'}`}>{entry.escalation_level}</span>
                      <span className="text-white">{entry.escalation_score.toFixed(1)}/10</span>
                      <span className="text-blue-400">{formatInterval(entry.recommended_interval_hours)}</span>
                      <span className="text-xs text-gray-600">band says {intervalMap[entry.escalation_level]}</span>
                    </div>
                  ))}
                </div>
                <div className="mt-3 text-xs text-gray-600 text-center">Measured by the frequency controller and stored. The band table above is a summary; these runs are the measurement.</div>
              </div>
            )}
            {/* A/B Prompt Testing */}
            {health.prompt_variants.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Prompt A/B Test — L6 Self-Improvement</div>
                <div className="grid grid-cols-2 gap-4">
                  {health.prompt_variants.map(v => (
                    <div key={v.version} className={`rounded-xl p-4 border ${v.active ? 'border-blue-700 bg-gray-800' : 'border-gray-700 bg-gray-800'}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="font-bold text-white">Prompt v{v.version}</span>
                        {v.active && <span className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">Active</span>}
                      </div>
                      {v.run_count > 0 ? (
                        <>
                          <div className={`text-3xl font-bold ${v.avg_quality_score >= 8 ? 'text-green-400' : v.avg_quality_score >= 6 ? 'text-yellow-400' : 'text-red-400'}`}>
                            {v.avg_quality_score.toFixed(2)}/10
                          </div>
                          <div className="text-xs text-gray-500 mt-1">{v.run_count} runs</div>
                        </>
                      ) : (
                        <div className="text-red-400 font-bold">No data</div>
                      )}
                    </div>
                  ))}
                </div>
                <div className="mt-3 text-xs text-gray-600 text-center">
                  Auto-promotes winner after 10 runs per variant if difference ≥ 0.3
                </div>
              </div>
            )}

            {/* Recent Quality Scores */}
            {health.recent_quality.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Recent Quality Scores</div>
                <div className="space-y-2">
                  {health.recent_quality.map((r, i) => (
                    <div key={i} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                      <span className="text-xs text-gray-500">{new Date(r.date).toLocaleString()}</span>
                      <span className="text-xs text-gray-400">{r.llm}</span>
                      <span className={`font-bold ${r.score >= 8 ? 'text-green-400' : r.score >= 6 ? 'text-yellow-400' : r.score > 0 ? 'text-orange-400' : 'text-red-400'}`}>
                        {r.score > 0 ? `${r.score.toFixed(2)}/10 ${r.score >= 8 ? 'Excellent' : r.score >= 6 ? 'Good' : 'Poor'}` : '0/10 Poor'}
                      </span>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

      </main>

      
      {/* DISCLAIMER */}
      <div className="max-w-6xl mx-auto px-6 pb-2 text-center">
        <p className="text-xs text-gray-600">⚠️ GNI data is for informational purposes only. Not financial advice.</p>
      </div>
      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Autonomy Engine | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
