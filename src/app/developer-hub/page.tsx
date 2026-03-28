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
              📊 Pattern Intelligence
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

        {/* Intro */}
        <div className="bg-purple-950 border border-purple-700 border-l-4 border-l-purple-400 rounded-xl p-5 mb-6">
          <p className="text-sm text-gray-100 leading-relaxed">
            Dev Console is GNI&apos;s technical transparency hub, designed for developers, system architects, and anyone who wants to understand how GNI works under the hood.
            Every component of the autonomous pipeline is observable here -- from the 66-pattern injection security filter to the A/B prompt quality system and the self-healing adaptive engine.
            The API reference documents all 21 endpoints with method, path, and description, making it straightforward to integrate GNI intelligence into external systems.
            Source health monitoring tracks all 25 RSS feeds in real time, showing which sources are healthy, degraded, or down and how their trust weights are adjusted dynamically.
            The quota monitor ensures GNI never exceeds its free-tier token budget, with a safe ceiling at 85K tokens and a hard limit at 100K per day -- the foundation of the /bin/sh.00/month architecture.
          </p>
        </div>
        {/* System Status Row */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-purple-950 border border-purple-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-purple-300">{reportCount}</div>
            <div className="text-xs text-gray-500 mt-1">Reports Generated</div>
          </div>
          <div className="bg-purple-950 border border-purple-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-purple-300">
              {sourceCount ? `${sourceCount.healthy}/${sourceCount.total}` : '--'}
            </div>
            <div className="text-xs text-gray-500 mt-1">Sources Healthy</div>
          </div>
          <div className="bg-purple-950 border border-purple-700 rounded-xl p-4 text-center">
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
        <div className="text-xs text-purple-400 uppercase tracking-wider mb-4 font-bold">Developer Pages</div>
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4 mb-6">

          {[
            { href: '/transparency', emoji: '📜', num: '01', label: 'Transparency', desc: 'Full AI funnel trace showing how each article was selected stage by stage. View the complete pipeline from 150 raw articles down to the final 3 selected for analysis. Essential for understanding GNI’s editorial decision-making process.', status: 'LIVE' },
            { href: '/autonomy',     emoji: '🧠', num: '02', label: 'Autonomy',     desc: 'The frequency controller, A/B prompt quality system, and L3.5 self-healing design that give GNI its autonomous capabilities. Shows how GNI adjusts its own behavior based on escalation levels and quota constraints. This is the architecture behind GNI’s L7 autonomy rating.', status: 'LIVE' },
            { href: '/health',       emoji: '🏥', num: '03', label: 'Health',       desc: 'Real-time pipeline status with quality scores per run across 5 dimensions: relevance, depth, actionability, source diversity, and novelty. Includes A/B prompt test current state and historical quality trend. Use this to verify GNI is operating within expected quality parameters.', status: 'LIVE' },
            { href: '/security',     emoji: '🛡️', num: '04', label: 'Security', desc: '66 injection patterns actively blocked at Stage 1b of the pipeline with SHA-256 audit chain for tamper detection. Full pentest results and security audit trail available. GNI’s security layer ensures all 25 RSS sources are validated before any content reaches the AI analysis stage.', status: 'LIVE' },
            { href: '/source-health',emoji: '📡', num: '05', label: 'Source Health',desc: 'Live status of all 25 RSS sources: healthy, degraded, or down. Dynamic trust weights adjusted by GPVS prediction accuracy are shown per source. Mini sparkline charts reveal each source’s reliability trend over the last 7 days.', status: 'LIVE' },
            { href: '/adaptive-log', emoji: '⚡',     num: '06', label: 'Adaptive Log', desc: 'The self-healing log showing every time GNI’s heartbeat triggered the adaptive pipeline -- including the reason (escalation delta), tokens consumed, and analysis result. This is GNI’s L3.5 self-healing evidence, demonstrating autonomous response to geopolitical threat changes.', status: 'LIVE' },
            { href: '/quota',        emoji: '💰', num: '07', label: 'Quota',        desc: 'Live Groq token budget showing usage per pipeline type vs the 85K safe ceiling vs the 100K hard limit. Historical usage trends and per-pipeline breakdown available. This page is the proof behind GNI’s /bin/sh.00/month architecture claim for the IEEE paper.', status: 'LIVE' },
          ].map(({ href, emoji, num, label, desc, status }) => (
            <a key={href} href={href} className="bg-gray-900 border border-gray-700 hover:border-purple-500 hover:bg-purple-950 rounded-xl p-4 transition-colors group">
              <div className="flex items-center gap-3 mb-2">
                <span className="text-xs font-bold text-purple-400 bg-purple-950 border border-purple-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">{num}</span>
                <span className="text-lg">{emoji}</span>
                <div className="text-sm font-bold text-white">{label}</div>
                <span className="text-xs bg-purple-900 text-purple-300 px-2 py-0.5 rounded-full ml-auto">{status}</span>
              </div>
              <p className="text-xs text-gray-400 leading-relaxed">{desc}</p>
              <div className="flex justify-end mt-3">
                <span className="text-xs font-bold text-purple-200 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 transition-colors">View {label} →</span>
              </div>
            </a>
          ))}

          {/* Dataset Export API */}
          <a href="/developer" className="bg-gray-900 border border-gray-700 hover:border-purple-500 hover:bg-purple-950 rounded-xl p-4 transition-colors group">
            <div className="flex items-center gap-3 mb-2">
              <span className="text-xs font-bold text-purple-400 bg-purple-950 border border-purple-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">08</span>
              <span className="text-lg">📥</span>
              <div className="text-sm font-bold text-white">Dataset Export API</div>
              <span className="text-xs bg-purple-900 text-purple-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
            </div>
            <p className="text-xs text-gray-400 leading-relaxed">Three REST endpoints allow programmatic access to GNI&apos;s complete dataset: reports, predictions, and pipeline articles -- all exportable as CSV or JSON. No authentication required -- all data is publicly accessible. Essential for IEEE paper replication, external analysis, and building applications on top of GNI intelligence.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-purple-200 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 transition-colors">View Export API →</span>
            </div>
          </a>

        </div>

        {/* API Endpoints */}
        <div className="text-xs text-purple-400 uppercase tracking-wider mb-4 font-bold">API Endpoints</div>
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

        {/* API Status */}
        <div className="bg-gray-900 border border-purple-800 rounded-xl p-4">
          <div className="text-xs text-purple-400 uppercase tracking-wider mb-3 font-bold">Additional Endpoints</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
            <div className="bg-purple-950 border border-purple-800 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <div className="font-mono text-xs text-purple-300">/api/latest</div>
                <span className="text-xs bg-green-900 text-green-300 px-1.5 py-0.5 rounded-full ml-auto">LIVE</span>
              </div>
              <div className="text-xs text-gray-500">Single call = complete GNI state</div>
            </div>
            <div className="bg-purple-950 border border-purple-800 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <div className="font-mono text-xs text-purple-300">/api/status</div>
                <span className="text-xs bg-green-900 text-green-300 px-1.5 py-0.5 rounded-full ml-auto">LIVE</span>
              </div>
              <div className="text-xs text-gray-500">Pipeline health for external monitoring</div>
            </div>
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
              <div className="flex items-center gap-2 mb-1">
                <div className="font-mono text-xs text-yellow-400">/api/webhooks</div>
                <span className="text-xs bg-yellow-900 text-yellow-300 px-1.5 py-0.5 rounded-full ml-auto">SOON</span>
              </div>
              <div className="text-xs text-gray-500">Subscribe to NEW_REPORT / CRITICAL events</div>
            </div>
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
