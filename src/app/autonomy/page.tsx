'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''

import { useEffect, useState } from 'react'

interface FrequencyEntry {
  id: string
  run_at: string
  escalation_score: number
  recommended_interval_hours: number
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

// Derive level label from escalation_score (FT-11: no escalation_level column in DB)
function scoreToLevel(score: number): string {
  if (score >= 8) return 'CRITICAL'
  if (score >= 6) return 'HIGH'
  if (score >= 4) return 'ELEVATED'
  if (score >= 2) return 'MODERATE'
  return 'LOW'
}

export default function AutonomyPage() {
  const [health, setHealth] = useState<HealthData | null>(null)
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/health', { headers: { 'X-GNI-Key': GNI_KEY } })
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

  const levels = [
    { level: 'CRITICAL', score: '8–10', interval: '30 min', color: 'text-red-400 border-red-700' },
    { level: 'HIGH',     score: '6–8',  interval: '2h',     color: 'text-orange-400 border-orange-700' },
    { level: 'ELEVATED', score: '4–6',  interval: '4h',     color: 'text-yellow-400 border-yellow-700' },
    { level: 'MODERATE', score: '2–4',  interval: '6h',     color: 'text-blue-400 border-blue-700' },
    { level: 'LOW',      score: '0–2',  interval: '12h',    color: 'text-green-400 border-green-700' },
  ]

  const latest = health?.frequency_log?.[0]
  const latestLevel = latest ? scoreToLevel(latest.escalation_score) : null

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
                      {intervalMap[latestLevel] || `${latest.recommended_interval_hours}h`}
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
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Escalation Evidence -- Score Breakdown (GNI-R-117)</div>
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
                      {health.latest_escalation.escalation_score_lower?.toFixed(1) ?? '--'}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Lower Bound</div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-2xl font-bold text-orange-400">
                      {health.latest_escalation.escalation_score_upper?.toFixed(1) ?? '--'}
                    </div>
                    <div className="text-xs text-gray-500 mt-1">Upper Bound</div>
                  </div>
                </div>
                <div className="text-xs text-gray-600 text-center">
                  Score breakdown and signal evidence stored in pipeline -- visible in Transparency page
                </div>
              </div>
            )}

            {/* Frequency Log History */}
            {health.frequency_log.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Recent Frequency Log</div>
                <div className="space-y-2">
                  {health.frequency_log.map(entry => {
                    const entryLevel = scoreToLevel(entry.escalation_score)
                    return (
                      <div key={entry.id} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                        <span className="text-xs text-gray-500">{new Date(entry.run_at).toLocaleString()}</span>
                        <span className={`font-bold ${levelColor[entryLevel]?.split(' ')[0] || 'text-gray-400'}`}>
                          {entryLevel}
                        </span>
                        <span className="text-white">{entry.escalation_score.toFixed(1)}/10</span>
                        <span className="text-blue-400">{intervalMap[entryLevel]}</span>
                      </div>
                    )
                  })}
                </div>
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

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights (Autonomous) | Autonomy Engine | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
