'use client'
import { useEffect, useState } from 'react'

interface QuotaData {
  used_today: number
  hard_limit: number
  safe_ceiling: number
}

export default function DeveloperHub() {
  const [quota, setQuota] = useState<QuotaData | null>(null)
  const [sourceCount, setSourceCount] = useState<{healthy: number, total: number} | null>(null)
  const [reportCount, setReportCount] = useState(0)

  useEffect(() => {
    fetch('/api/quota')
      .then(r => r.json())
      .then(data => {
        if (data.used_today !== undefined) {
          setQuota({ used_today: data.used_today, hard_limit: data.hard_limit || 100000, safe_ceiling: data.safe_ceiling || 85000 })
        }
      })
      .catch(() => {})

    fetch('/api/source-health')
      .then(r => r.json())
      .then(data => {
        const sources = data.sources || []
        const healthy = sources.filter((s: {status: string}) => s.status === 'healthy').length
        setSourceCount({ healthy, total: sources.length })
      })
      .catch(() => {})

    fetch('/api/reports')
      .then(r => r.json())
      .then(data => setReportCount((data.reports || []).length))
      .catch(() => {})
  }, [])

  const quotaPct = quota ? Math.round((quota.used_today / quota.hard_limit) * 100) : 0

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-purple-300">🧠 Dev Console</h1>
              <p className="text-xs text-gray-400">How does GNI work and how do I build on top of it?</p>
            </div>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Researcher
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        
          {/* Cross-Navigation -- 4 main pages (GNI-R-140) */}
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* System Status Row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-gray-900 border border-purple-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-purple-300">{reportCount}</div>
            <div className="text-xs text-gray-500 mt-1">Reports Generated</div>
          </div>
          <div className="bg-gray-900 border border-purple-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-purple-300">
              {sourceCount ? `${sourceCount.healthy}/${sourceCount.total}` : '--'}
            </div>
            <div className="text-xs text-gray-500 mt-1">Sources Healthy</div>
          </div>
          <div className="bg-gray-900 border border-purple-800 rounded-xl p-4 text-center">
            <div className={`text-2xl font-bold ${quotaPct > 70 ? 'text-orange-400' : 'text-purple-300'}`}>
              {quota ? `${quotaPct}%` : '--'}
            </div>
            <div className="text-xs text-gray-500 mt-1">Quota Used Today</div>
            {quota && (
              <div className="mt-2 bg-gray-800 rounded-full h-1.5">
                <div className={`h-1.5 rounded-full ${quotaPct > 70 ? 'bg-orange-500' : 'bg-purple-500'}`}
                  style={{ width: `${Math.min(quotaPct, 100)}%` }} />
              </div>
            )}
          </div>
        </div>

        {/* Sub-page Grid */}
        <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Developer Pages</div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">

          {[
            { href: '/transparency', emoji: '📜', label: 'Transparency', desc: 'Full AI funnel trace. How each article was selected stage by stage.', status: 'LIVE' },
            { href: '/autonomy',     emoji: '🧠', label: 'Autonomy',     desc: 'Frequency controller + A/B prompt system + L3.5 self-healing design.', status: 'LIVE' },
            { href: '/health',       emoji: '🏥', label: 'Health',       desc: 'Pipeline status + quality scores per run + A/B test current state.', status: 'LIVE' },
            { href: '/security',     emoji: '🛡️', label: 'Security', desc: '66 injection patterns + SHA-256 audit chain + pentest results.', status: 'LIVE' },
            { href: '/source-health',emoji: '📡', label: 'Source Health',desc: '25 RSS sources: healthy/degraded/down. Mini chart per source.', status: 'LIVE' },
            { href: '/adaptive-log', emoji: '⚡',     label: 'Adaptive Log', desc: 'Self-healing log. When triggered, why, tokens used, result.', status: 'LIVE' },
            { href: '/quota',        emoji: '💰', label: 'Quota',        desc: 'Live token budget per pipeline vs 85K safe ceiling vs 100K limit.', status: 'LIVE' },
          ].map(({ href, emoji, label, desc, status }) => (
            <a key={href} href={href} className="bg-gray-900 border border-gray-700 hover:border-purple-600 rounded-xl p-4 transition-colors">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-lg">{emoji}</span>
                <div className="text-sm font-bold text-white">{label}</div>
                <span className="text-xs bg-purple-900 text-purple-300 px-2 py-0.5 rounded-full ml-auto">{status}</span>
              </div>
              <p className="text-xs text-gray-400">{desc}</p>
            </a>
          ))}

        </div>

        {/* API Endpoints */}
        <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">API Endpoints</div>
        <div className="bg-gray-900 border border-purple-800 rounded-xl p-5 mb-6">
          <div className="space-y-3">
            {[
              { method: 'GET', path: '/api/reports', desc: 'Latest intelligence reports + baseline' },
              { method: 'GET', path: '/api/pillar-reports', desc: 'GEO / TECH / FIN pillar reports' },
              { method: 'GET', path: '/api/quota', desc: 'Token usage vs 85K ceiling' },
              { method: 'GET', path: '/api/source-health', desc: 'All 25 RSS source statuses' },
              { method: 'GET', path: '/api/alerts', desc: 'Alert archive with escalation deltas' },
              { method: 'GET', path: '/api/predictions-list', desc: 'All MAD predictions + verify dates' },
              { method: 'GET', path: '/api/health', desc: 'Pipeline health + quality scores' },
            ].map(({ method, path, desc }) => (
              <div key={path} className="flex items-center gap-3">
                <span className="text-xs font-bold bg-green-900 text-green-300 px-2 py-0.5 rounded font-mono shrink-0">{method}</span>
                <span className="font-mono text-xs text-purple-300 shrink-0">{path}</span>
                <span className="text-xs text-gray-500">{desc}</span>
              </div>
            ))}
          </div>
        </div>

        {/* Coming Soon */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Coming Soon</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            {[
              { path: '/api/latest', desc: 'Single call = complete GNI state' },
              { path: '/api/status', desc: 'Pipeline health for external monitoring' },
              { path: '/api/webhooks', desc: 'Subscribe to NEW_REPORT / CRITICAL events' },
            ].map(({ path, desc }) => (
              <div key={path} className="bg-gray-800 rounded-lg p-3">
                <div className="font-mono text-xs text-yellow-400 mb-1">{path}</div>
                <div className="text-xs text-gray-500">{desc}</div>
              </div>
            ))}
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Dev Console Hub | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
