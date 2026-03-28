'use client'
import { useEffect, useState } from 'react'

interface Alert {
  id: string
  alert_type: string
  message: string
  escalation_score: number
  created_at: string
}

interface Usage {
  id: string
  pipeline: string
  tokens_used: number
  created_at: string
}

export default function AlertsPage() {
  const [alerts, setAlerts] = useState<Alert[]>([])
  const [usage, setUsage] = useState<Usage[]>([])
  const [loading, setLoading] = useState(true)

  useEffect(() => {
    fetch('/api/alerts')
      .then(r => r.json())
      .then(data => {
        setAlerts(data.alerts || [])
        setUsage(data.usage || [])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const alertTypeColor = (type: string) => {
    switch (type?.toUpperCase()) {
      case 'CRITICAL': return 'bg-red-950 border-red-700 text-red-300'
      case 'NYSE_OPEN': return 'bg-green-950 border-green-700 text-green-300'
      case 'NYSE_CLOSE': return 'bg-orange-950 border-orange-700 text-orange-300'
      case 'ADAPTIVE_TRIGGER': return 'bg-blue-950 border-blue-700 text-blue-300'
      case 'SOURCE_DOWN': return 'bg-yellow-950 border-yellow-700 text-yellow-300'
      default: return 'bg-gray-900 border-gray-700 text-gray-300'
    }
  }

  const recentTriggers = usage.filter(u => u.pipeline === 'gni_adaptive')

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/" className="inline-flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Quantum Strategist</a>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">&#x1F6A8; Alert History</h1>
              <p className="text-sm text-gray-400">Heartbeat + Adaptive + System alerts — full web archive</p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300">&larr; Dashboard</a>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-white">{alerts.length}</div>
              <div className="text-xs text-gray-500">Total Alerts</div>
            </div>
            <div className="bg-blue-950 border border-blue-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-blue-400">{recentTriggers.length}</div>
              <div className="text-xs text-blue-600">Adaptive Triggers</div>
            </div>
            <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-red-400">
                {alerts.filter(a => a.alert_type?.toUpperCase() === 'CRITICAL').length}
              </div>
              <div className="text-xs text-red-600">Critical Alerts</div>
            </div>
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
        {loading && <div className="text-center py-20 text-gray-400">Loading alerts...</div>}

        {!loading && alerts.length === 0 && usage.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">&#x1F6A8;</div>
            <p className="text-lg font-bold mb-2">No alerts yet</p>
            <p className="text-sm max-w-md mx-auto">
              Alerts fire via Telegram when escalation spikes, NYSE opens/closes, or adaptive pipeline triggers.
              This page archives all alerts for web review. Data populates automatically.
            </p>
            <div className="mt-6 bg-gray-900 border border-gray-700 rounded-xl p-4 text-left max-w-md mx-auto">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Alert Types</div>
              {[
                { type: 'CRITICAL', desc: 'Escalation score 9+/10 — immediate attention', color: 'text-red-400' },
                { type: 'NYSE_OPEN', desc: 'US markets opened — heightened monitoring', color: 'text-green-400' },
                { type: 'NYSE_CLOSE', desc: 'US markets closed — after-hours watch', color: 'text-orange-400' },
                { type: 'ADAPTIVE_TRIGGER', desc: 'Escalation delta fired adaptive pipeline', color: 'text-blue-400' },
                { type: 'SOURCE_DOWN', desc: 'RSS source health degraded', color: 'text-yellow-400' },
              ].map(a => (
                <div key={a.type} className="flex items-center gap-3 py-2 border-b border-gray-800">
                  <span className={`text-xs font-bold font-mono w-36 shrink-0 ${a.color}`}>{a.type}</span>
                  <span className="text-xs text-gray-400">{a.desc}</span>
                </div>
              ))}
            </div>
          </div>
        )}

        {!loading && alerts.length > 0 && (
          <section className="mb-8">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Alert Log</div>
            <div className="space-y-3">
              {alerts.map(alert => (
                <div key={alert.id} className={`border rounded-xl p-4 ${alertTypeColor(alert.alert_type)}`}>
                  <div className="flex items-center justify-between mb-2">
                    <span className="text-xs font-bold font-mono">{alert.alert_type?.toUpperCase()}</span>
                    <span className="text-xs text-gray-500">
                      {new Date(alert.created_at).toLocaleDateString('en-US', {
                        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                      })}
                    </span>
                  </div>
                  <p className="text-sm leading-relaxed">{alert.message}</p>
                  {alert.escalation_score > 0 && (
                    <div className="mt-2 text-xs text-gray-400">
                      Escalation: <span className="font-bold text-red-400">{alert.escalation_score}/10</span>
                    </div>
                  )}
                </div>
              ))}
            </div>
          </section>
        )}

        {!loading && recentTriggers.length > 0 && (
          <section>
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Recent Adaptive Triggers (from quota log)</div>
            <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
              {recentTriggers.slice(0, 10).map((u, i) => (
                <div key={u.id} className="flex items-center justify-between px-4 py-3 border-b border-gray-800 text-sm">
                  <div className="flex items-center gap-3">
                    <span className="text-blue-400 font-bold text-xs">#{i + 1}</span>
                    <span className="text-gray-300 font-mono text-xs">{u.pipeline}</span>
                  </div>
                  <div className="flex items-center gap-4 text-xs">
                    <span className="text-orange-400 font-bold">{(u.tokens_used || 0).toLocaleString()} tokens</span>
                    <span className="text-gray-500">
                      {new Date(u.created_at).toLocaleDateString('en-US', {
                        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                      })}
                    </span>
                  </div>
                </div>
              ))}
            </div>
          </section>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Alert History | Heartbeat + Adaptive | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}