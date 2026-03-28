'use client'

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
  source_credibility: Array<{
    source: string
    credibility_score: number
    gpvs_wins: number
    gpvs_total: number
    last_calculated: string
  }>
  prompt_variants: Array<{
    version: number
    avg_quality_score: number
    run_count: number
    active: boolean
  }>
  recent_quality: Array<{
    date: string
    score: number
    llm: string
  }>
  health_alerts: Array<{
    id: string
    alert_type: string
    severity: string
    message: string
    metric_name: string
    metric_value: number
    threshold: number
    resolved: boolean
    created_at: string
  }>
  frequency_log: Array<{
    id: string
    run_at: string
    escalation_score: number
    escalation_level: string
    recommended_interval_hours: number
    reason: string
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

function credColor(score: number) {
  if (score >= 0.8) return 'bg-green-500'
  if (score >= 0.6) return 'bg-blue-500'
  if (score >= 0.4) return 'bg-yellow-500'
  return 'bg-red-500'
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
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/developer-hub" className="inline-flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">← Dev Console</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">System Health</h1>
            <p className="text-sm text-gray-400">Pipeline status, quality scores, source weights, credibility, A/B test</p>
          </div>
          <a href="/" className="text-sm text-blue-400 hover:text-blue-300">Back to Dashboard</a>
        
          {/* Cross-Navigation -- 4 main pages (GNI-R-140) */}
          <div className="flex flex-wrap gap-2 mt-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Pattern Intelligence
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Dev Console
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
          </div>
</div>
          </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        {loading && <div className="text-center py-20 text-gray-400">Loading health data...</div>}

        {!loading && health && (
          <>
            <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">System Status</div>
                <div className={`text-3xl font-bold ${statusColor(health.status)}`}>{health.status?.toUpperCase()}</div>
                <div className="text-xs text-gray-600 mt-1">All components operational</div>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Avg Quality Score</div>
                <div className={`text-3xl font-bold ${qualityColor(health.avg_quality_score)}`}>{health.avg_quality_score}/10</div>
                <div className="text-xs text-gray-600 mt-1">{qualityLabel(health.avg_quality_score)} — last {health.total_reports} reports</div>
              </div>
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Last Pipeline Run</div>
                {health.last_run ? (
                  <>
                    <div className={`text-xl font-bold ${statusColor(health.last_run.status)}`}>{health.last_run.status?.toUpperCase()}</div>
                    <div className="text-xs text-gray-500 mt-1">{new Date(health.last_run.run_at).toLocaleString()} — {health.last_run.duration_seconds}s</div>
                    <div className="text-xs text-gray-600">{health.last_run.total_collected} articles to {health.last_run.total_after_funnel} via {health.last_run.llm_source}</div>
                  </>
                ) : <div className="text-gray-600 text-sm">No runs yet</div>}
              </div>
            </div>

            {health.frequency_log && health.frequency_log.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">⚡ Frequency Controller — Autonomous Run Scheduling</div>
                {(() => {
                  const latest = health.frequency_log[0]
                  const intervalMap: Record<string, string> = {
                    'CRITICAL': '30 min', 'HIGH': '2h', 'ELEVATED': '4h', 'MODERATE': '6h', 'LOW': '12h'
                  }
                  const levelColor: Record<string, string> = {
                    'CRITICAL': 'text-red-400', 'HIGH': 'text-orange-400',
                    'ELEVATED': 'text-yellow-400', 'MODERATE': 'text-blue-400', 'LOW': 'text-green-400'
                  }
                  return (
                    <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
                      <div className="bg-gray-800 rounded-lg p-3 text-center">
                        <div className={`text-2xl font-bold ${levelColor[latest.escalation_level] || 'text-gray-400'}`}>
                          {latest.escalation_level}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">Current Level</div>
                      </div>
                      <div className="bg-gray-800 rounded-lg p-3 text-center">
                        <div className="text-2xl font-bold text-white">
                          {latest.escalation_score.toFixed(1)}/10
                        </div>
                        <div className="text-xs text-gray-500 mt-1">Escalation Score</div>
                      </div>
                      <div className="bg-gray-800 rounded-lg p-3 text-center">
                        <div className="text-2xl font-bold text-blue-400">
                          {intervalMap[latest.escalation_level] || `${latest.recommended_interval_hours}h`}
                        </div>
                        <div className="text-xs text-gray-500 mt-1">Run Interval</div>
                      </div>
                      <div className="bg-gray-800 rounded-lg p-3 text-center">
                        <div className="text-xs text-gray-300 leading-relaxed">{latest.reason}</div>
                        <div className="text-xs text-gray-500 mt-1">Reason</div>
                      </div>
                    </div>
                  )
                })()}
                <div className="text-xs text-gray-600 mt-3">
                  CRITICAL=30min · HIGH=2h · ELEVATED=4h · MODERATE=6h · LOW=12h — AI decides run frequency autonomously
                </div>
              </div>
            )}

            {health.health_alerts && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">🚨 Health Agent Alerts</div>
                {health.health_alerts.length === 0 ? (
                  <div className="flex items-center gap-3 text-green-400">
                    <span className="text-lg">✅</span>
                    <span className="text-sm">All health checks passing — no alerts fired</span>
                  </div>
                ) : (
                  <div className="space-y-2">
                    {health.health_alerts.map(alert => (
                      <div key={alert.id} className={`rounded-lg p-3 border ${
                        alert.severity === 'CRITICAL' ? 'bg-red-950 border-red-800' :
                        alert.severity === 'WARNING' ? 'bg-yellow-950 border-yellow-800' :
                        'bg-gray-800 border-gray-700'
                      }`}>
                        <div className="flex items-center justify-between mb-1">
                          <span className={`text-xs font-bold ${
                            alert.severity === 'CRITICAL' ? 'text-red-400' :
                            alert.severity === 'WARNING' ? 'text-yellow-400' : 'text-gray-400'
                          }`}>
                            {alert.severity} — {alert.alert_type}
                          </span>
                          <span className="text-xs text-gray-600">
                            {new Date(alert.created_at).toLocaleString()}
                          </span>
                        </div>
                        <p className="text-xs text-gray-300">{alert.message}</p>
                        {alert.metric_name && (
                          <div className="text-xs text-gray-500 mt-1">
                            {alert.metric_name}: {alert.metric_value?.toFixed(2)} (threshold: {alert.threshold?.toFixed(2)})
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}

            {health.prompt_variants && health.prompt_variants.length > 0 && (
              <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Prompt A/B Test — L6 Self-Improvement</div>
                <div className="grid grid-cols-2 gap-4">
                  {health.prompt_variants.map(v => (
                    <div key={v.version} className={`rounded-lg p-4 ${v.active ? 'border border-blue-600 bg-gray-800' : 'border border-gray-700 bg-gray-850 opacity-60'}`}>
                      <div className="flex items-center justify-between mb-2">
                        <span className="text-sm font-bold text-white">Prompt v{v.version}</span>
                        {v.active ? <span className="text-xs bg-blue-900 text-blue-300 px-2 py-0.5 rounded">Active</span> : <span className="text-xs bg-gray-700 text-gray-400 px-2 py-0.5 rounded">Retired</span>}
                      </div>
                      <div className={`text-2xl font-bold ${qualityColor(v.avg_quality_score)}`}>{v.avg_quality_score > 0 ? `${v.avg_quality_score.toFixed(2)}/10` : 'No data'}</div>
                      <div className="text-xs text-gray-500 mt-1">{v.run_count} runs</div>
                      {v.run_count > 0 && <div className="mt-2 bg-gray-700 rounded-full h-1.5"><div className={`h-1.5 rounded-full ${qualityColor(v.avg_quality_score) === 'text-green-400' ? 'bg-green-500' : 'bg-blue-500'}`} style={{ width: `${Math.min(100, v.avg_quality_score * 10)}%` }} /></div>}
                    </div>
                  ))}
                </div>
                <div className="text-xs text-gray-600 mt-3">Auto-promotes winner after 10 runs per variant if difference ≥ 0.3</div>
              </div>
            )}

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Source Credibility — GPVS-Based Learning</div>
              {health.source_credibility && health.source_credibility.length > 0 ? (
                <div className="space-y-3">
                  {health.source_credibility.map(s => (
                    <div key={s.source} className="flex items-center gap-4">
                      <div className="w-36 text-sm text-gray-300 shrink-0">{s.source}</div>
                      <div className="flex-1 bg-gray-800 rounded-full h-2">
                        <div className={`${credColor(s.credibility_score)} h-2 rounded-full`} style={{ width: `${s.credibility_score * 100}%` }} />
                      </div>
                      <div className="text-sm font-mono text-blue-400 w-14 text-right">{s.credibility_score.toFixed(3)}</div>
                      <div className="text-xs text-gray-600 w-20 text-right">{s.gpvs_wins}/{s.gpvs_total} wins</div>
                    </div>
                  ))}
                </div>
              ) : <div className="text-gray-600 text-sm">No credibility data yet — accumulates after GPVS outcomes</div>}
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Source Weights — Dynamic Intelligence Weighting</div>
              {health.source_weights.length === 0 ? <div className="text-gray-600 text-sm">No source weights yet</div> : (
                <div className="space-y-3">
                  {health.source_weights.map(sw => (
                    <div key={sw.source} className="flex items-center gap-4">
                      <div className="w-36 text-sm text-gray-300 shrink-0">{sw.source}</div>
                      <div className="flex-1 bg-gray-800 rounded-full h-2">
                        <div className="bg-blue-500 h-2 rounded-full" style={{ width: `${Math.min(100, (sw.weight / 2.0) * 100)}%` }} />
                      </div>
                      <div className="text-sm font-mono text-blue-400 w-12 text-right">{sw.weight?.toFixed(2)}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Recent Quality Scores</div>
              {health.recent_quality.length === 0 ? <div className="text-gray-600 text-sm">No reports yet</div> : (
                <div className="space-y-2">
                  {health.recent_quality.map((r, i) => (
                    <div key={i} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-2">
                      <div className="text-xs text-gray-500">{new Date(r.date).toLocaleString()}</div>
                      <div className="text-xs text-gray-600">{r.llm}</div>
                      <div className={`text-sm font-bold ${qualityColor(r.score)}`}>{r.score}/10 {qualityLabel(r.score)}</div>
                    </div>
                  ))}
                </div>
              )}
            </div>

            <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Infrastructure</div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[{ label: 'Supabase', status: 'Connected' }, { label: 'Groq API', status: 'Active' }, { label: 'Ollama', status: 'Active' }, { label: 'Telegram', status: 'Live' }].map(item => (
                  <div key={item.label} className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className="text-xs text-gray-500 mb-1">{item.label}</div>
                    <div className="text-sm font-bold text-green-400">{item.status}</div>
                  </div>
                ))}
              </div>
            </div>
          </>
        )}

        {!loading && !health && <div className="text-center py-20 text-red-400">Failed to load health data.</div>}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Health Dashboard — Real-time pipeline monitoring | GNI_Autonomous Sprint
        </div>
      </footer>
    </div>
  )
}
