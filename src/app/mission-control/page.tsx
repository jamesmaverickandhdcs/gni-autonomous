'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface CheckResult {
  status: string
  message: string
  auto_healed?: boolean
}

interface SelfCheckData {
  overall_status: string
  issues_found: number
  auto_healed: number
  telegram_sent: boolean
  duration_ms: number
  checked_at: string
  checks: Record<string, CheckResult>
}

interface HistoryRow {
  id: string
  checked_at: string
  overall_status: string
  issues_found: number
  auto_healed: number
  telegram_sent: boolean
}

const statusColor = (s: string) => {
  switch (s) {
    case 'OK': case 'HEALTHY': return 'text-green-400'
    case 'WARNING': return 'text-yellow-400'
    case 'CRITICAL': return 'text-red-400'
    default: return 'text-gray-400'
  }
}

const statusBg = (s: string) => {
  switch (s) {
    case 'OK': case 'HEALTHY': return 'bg-green-900 border-green-700 text-green-300'
    case 'WARNING': return 'bg-yellow-900 border-yellow-700 text-yellow-300'
    case 'CRITICAL': return 'bg-red-900 border-red-700 text-red-300'
    default: return 'bg-gray-800 border-gray-600 text-gray-300'
  }
}

const CHECK_LABELS: Record<string, string> = {
  supabase_connection: 'Supabase Connection',
  latest_report: 'Latest Report Age',
  groq_quota: 'Groq Token Quota',
  source_health: 'RSS Source Health',
  pipeline_recent: 'Pipeline Recent Run',
  mad_recent: 'MAD Debate Recent',
}

export default function SelfCheckPage() {
  const [data, setData] = useState<SelfCheckData | null>(null)
  const [history, setHistory] = useState<HistoryRow[]>([])
  const [loading, setLoading] = useState(false)
  const [histLoading, setHistLoading] = useState(true)
  const [lastRun, setLastRun] = useState<string | null>(null)

  const loadHistory = async () => {
    try {
      const res = await fetch('/api/mission-control-history', { headers: { 'X-GNI-Key': GNI_KEY } })
      const json = await res.json()
      setHistory(json.history || [])
    } catch (e) { console.error(e) }
    finally { setHistLoading(false) }
  }

  const runCheck = async () => {
    setLoading(true)
    try {
      // Public call -- returns last cached result from DB (no new check triggered)
      const res = await fetch('/api/mission-control', { headers: { 'X-GNI-Key': GNI_KEY } })
      const json = await res.json()
      setData(json)
      setLastRun(new Date().toLocaleTimeString())
      loadHistory()
    } catch (e) { console.error(e) }
    finally { setLoading(false) }
  }

  useEffect(() => {
    loadHistory()
    runCheck()
    const interval = setInterval(runCheck, 5 * 60 * 1000)
    return () => clearInterval(interval)
  }, []) // eslint-disable-line react-hooks/exhaustive-deps

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/developer-hub" className="inline-flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Dev Console</a>
          <div className="flex items-center justify-between mt-2">
            <div>
              <h1 className="text-xl font-bold text-purple-300">🛡️ Mission Control System</h1>
              <p className="text-xs text-gray-400">GNI Operations Monitor | Aggregates all system health | Admin Telegram alerts</p>
            </div>
            <div className="flex items-center gap-3">
              {lastRun && <span className="text-xs text-gray-500">Last run: {lastRun}</span>}
              <button onClick={runCheck} disabled={loading}
                className="text-xs font-bold bg-purple-700 hover:bg-purple-600 text-white rounded-lg px-4 py-2 transition-colors disabled:opacity-50">
                {loading ? 'Checking...' : '▶ Run Check Now'}
              </button>
            </div>
          </div>
          <div className="flex flex-wrap gap-2 mt-3">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">🎯 Quantum Strategist</a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">📊 Pattern Intelligence</a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">🎯 Feedback Loop</a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">🌟 About</a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6">

        {data && (
          <div className={`border rounded-xl p-5 mb-6 ${statusBg(data.overall_status)}`}>
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-4">
                <div className="text-3xl">
                  {data.overall_status === 'HEALTHY' ? '✅' : data.overall_status === 'WARNING' ? '⚠️' : '🚨'}
                </div>
                <div>
                  <div className="text-xl font-bold">{data.overall_status}</div>
                  <div className="text-xs opacity-80">
                    {data.overall_status === 'HEALTHY' ? 'All systems operational' : `${data.issues_found} issue${data.issues_found > 1 ? 's' : ''} detected`}
                    {data.telegram_sent && ' | Telegram alert sent'}
                  </div>
                </div>
              </div>
              <div className="text-right text-xs opacity-70">
                <div>Checked: {new Date(data.checked_at).toLocaleString()}</div>
                <div>Duration: {data.duration_ms}ms</div>
              </div>
            </div>
          </div>
        )}

        {loading && !data && (
          <div className="text-center py-12 text-gray-400">
            <div className="text-4xl mb-4">⏳</div>
            <p>Running system checks...</p>
          </div>
        )}

        {data && (
          <section className="mb-6">
            <div className="text-xs text-purple-400 font-bold uppercase tracking-wider mb-3">System Checks</div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {Object.entries(data.checks).map(([key, check]) => (
                <div key={key} className="bg-gray-900 border border-gray-700 rounded-xl p-4">
                  <div className="flex items-center justify-between mb-1">
                    <div className="text-sm font-bold text-white">{CHECK_LABELS[key] || key}</div>
                    <span className={`text-xs font-bold px-2 py-0.5 rounded-full border ${statusBg(check.status)}`}>
                      {check.status}
                    </span>
                  </div>
                  <p className="text-xs text-gray-400">{check.message}</p>
                </div>
              ))}
            </div>
          </section>
        )}

        <section className="mb-6">
          <div className="text-xs text-purple-400 font-bold uppercase tracking-wider mb-3">Check History</div>
          {histLoading && <div className="text-gray-400 text-xs">Loading history...</div>}
          <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
            <div className="grid grid-cols-5 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase tracking-wider">
              <div className="col-span-2">Time</div>
              <div>Status</div>
              <div>Issues</div>
              <div>Telegram</div>
            </div>
            {history.slice(0, 20).map(row => (
              <div key={row.id} className="grid grid-cols-5 px-4 py-2 border-b border-gray-800 hover:bg-gray-800 text-xs">
                <div className="col-span-2 text-gray-400">{new Date(row.checked_at).toLocaleString()}</div>
                <div className={`font-bold ${statusColor(row.overall_status)}`}>{row.overall_status}</div>
                <div className="text-gray-400">{row.issues_found}</div>
                <div className={row.telegram_sent ? 'text-green-400' : 'text-gray-600'}>
                  {row.telegram_sent ? 'Sent' : '--'}
                </div>
              </div>
            ))}
            {history.length === 0 && !histLoading && (
              <div className="px-4 py-4 text-xs text-gray-600">No history yet -- run first check above</div>
            )}
          </div>
        </section>

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
          <div className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-2">How This Works</div>
          <p className="text-xs text-gray-400 leading-relaxed">
            Auto-runs every 30 minutes. Checks: Supabase connection, latest report age, Groq quota, source health, pipeline recency, MAD debate recency.
            CRITICAL or WARNING issues trigger automatic Telegram alert to admin. All results saved to mission_control_log table.
            This is GNI&apos;s web-layer self-monitoring -- part of the L8 autonomy roadmap.
          </p>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Mission Control System | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
