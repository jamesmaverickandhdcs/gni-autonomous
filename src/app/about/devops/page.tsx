'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface QuotaData {
  today_tokens: number
  daily_limit: number
  today_cost: number
}

export default function AboutDevopsPage() {
  const [quota, setQuota] = useState<QuotaData | null>(null)
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/quota', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setQuota(data))
      .catch(() => setError('Failed to load live data.'))
      .finally(() => setLoading(false))
  }, [])

  const pct = quota && quota.daily_limit ? Math.round(quota.today_tokens / quota.daily_limit * 100) : 0

  const pipelines = [
    { name: 'gni_pipeline', schedule: '02:00 + 10:00 UTC', tokens: '~6,175/run', color: 'blue', desc: 'Core intelligence pipeline. RSS collection from 25 sources -- injection detection across 66 patterns -- MD5 deduplication -- geopolitical funnel scoring -- 3-temperature AI analysis with confidence intervals -- Three Pillar domain reports -- Supabase persistence -- Telegram notification. The sacred run that never fails.' },
    { name: 'gni_mad', schedule: '02:30 + 10:30 UTC', tokens: '~12,393/run', color: 'purple', desc: 'Quadratic MAD Protocol. Four AI agents (Bull, Bear, Black Swan, Ostrich) debate the latest report across 3 rounds with Arbitrator coaching after each round. Produces BULLISH/BEARISH/NEUTRAL verdict with confidence score, action recommendation, blind spot warning, and GPVS prediction.' },
    { name: 'gni_heartbeat', schedule: 'Every 30 min', tokens: '0 tokens', color: 'green', desc: 'Escalation monitoring and NYSE alert system. Reads latest escalation score, compares to previous pipeline run, detects signal divergence between Pipeline and MAD, fires NYSE open/close alerts, triggers adaptive pipeline when escalation delta exceeds threshold.' },
    { name: 'gni_adaptive', schedule: 'On trigger', tokens: '0 to 12,393', color: 'amber', desc: 'Emergency fresh analysis when world escalation spikes. CRITICAL level = 0 Groq calls (cached data only). HIGH = 4 calls. LOW = 19 calls. Frequency controller adjusts run interval autonomously: CRITICAL=30min, HIGH=2h, ELEVATED=4h, MODERATE=6h, LOW=12h.' },
  ]

  const architecture = [
    { layer: 'L1 Data', title: 'RSS Ingestion + Deduplication', desc: '25 global news sources, up to 20 articles each, 400-500 raw articles per run. MD5 deduplication prevents duplicate event reporting within 6-hour rolling windows.' },
    { layer: 'L2 Security', title: '66-Pattern Injection Detection', desc: 'Every article scanned across 7 security layers: Unicode normalization, source credibility scoring, context boundary detection, Named Entity Recognition, Groq hardened JSON output, output sanitization, SHA-256 audit chain for every intelligence item.' },
    { layer: 'L3 Intelligence', title: 'Funnel Scoring + AI Analysis', desc: 'Geopolitical significance scoring (0-20 points), top-N selection with source diversity enforcement, 3 independent AI runs at temperatures 0.1/0.3/0.7, t-distribution confidence interval (t=4.303, n=3, alpha=0.05) for every sentiment score.' },
    { layer: 'L4 Validation', title: 'GPVS Prediction Scoring', desc: 'After verify_date passes, actual SPY movement measured against prediction direction. Correct predictions: source weight x1.1 via EMA. Wrong predictions: weight x0.9. Weights bounded 0.5 to 2.0. Creates compounding accuracy advantage.' },
    { layer: 'L5 Autonomy', title: 'Self-Healing + Mission Control', desc: 'Heartbeat monitors escalation delta every 30 minutes. Mission Control checks Supabase connection, report freshness, quota ceiling, source health, pipeline recency. Telegram CRITICAL/WARNING alerts with specific action recommendations.' },
  ]

  const colorMap: Record<string, string> = {
    blue: 'bg-blue-950 border-blue-800',
    purple: 'bg-purple-950 border-purple-800',
    green: 'bg-green-950 border-green-800',
    amber: 'bg-amber-950 border-amber-800',
  }
  const textMap: Record<string, string> = {
    blue: 'text-blue-400',
    purple: 'text-purple-400',
    green: 'text-green-400',
    amber: 'text-amber-400',
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/about" className="inline-flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">Back to About</a>
          <h1 className="text-2xl font-bold text-purple-400">Dev Console -- Autonomous Architecture</h1>
          <p className="text-sm text-gray-400">How GNI runs itself. The Dev Console perspective reveals every autonomous process -- from the 4 GitHub Actions pipelines to the self-healing heartbeat to the 66-pattern injection security layer. This page proves L7 autonomy: zero human intervention required for daily operation, with live token quota data as the .00/month evidence.</p>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        <div className="bg-purple-950 border border-purple-800 rounded-xl p-6">
          <div className="text-xs text-purple-400 uppercase tracking-wider mb-3">The Autonomy Philosophy</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title: '.00/Month Forever', desc: 'Every component uses free tiers: Groq (100K tokens/day), Supabase (500MB), Vercel (100GB bandwidth), GitHub Actions (unlimited public repo minutes). Zero vendor lock-in. Zero credit card required. Zero maintenance cost.' },
              { title: 'Zero Human Intervention', desc: 'Once deployed, GNI runs 2x daily without any human action. The frequency controller adjusts run intervals based on world escalation score. The adaptive pipeline responds to breaking threats automatically without any trigger from a human.' },
              { title: 'Self-Healing by Design', desc: 'Mission Control monitors 6 health dimensions every 30 minutes. Telegram alerts fire before failures cascade. The heartbeat detects anomalies and triggers corrective pipelines autonomously. The system fixes itself.' },
            ].map(item => (
              <div key={item.title} className="bg-purple-900 bg-opacity-30 rounded-lg p-4">
                <div className="text-sm font-bold text-purple-300 mb-2">{item.title}</div>
                <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {loading && <div className="text-center py-8 text-gray-500">Loading live quota data...</div>}
        {error && <div className="text-center py-8 text-red-400">{error}</div>}

        {!loading && quota && (
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Live Token Quota -- .00/Month Proof</div>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
              {[
                { label: 'Tokens Used Today', value: quota.today_tokens?.toLocaleString() || '0', color: 'text-white' },
                { label: 'Daily Limit', value: quota.daily_limit?.toLocaleString() || '100,000', color: 'text-gray-400' },
                { label: 'Usage', value: String(pct) + '%', color: pct > 85 ? 'text-red-400' : pct > 70 ? 'text-yellow-400' : 'text-green-400' },
                { label: 'Cost Today', value: '.00', color: 'text-green-400' },
              ].map(item => (
                <div key={item.label} className="bg-gray-800 rounded-lg p-4 text-center">
                  <div className={"text-2xl font-bold mb-1 " + item.color}>{item.value}</div>
                  <div className="text-xs text-gray-500">{item.label}</div>
                </div>
              ))}
            </div>
            <div className="bg-gray-800 rounded-full h-3 overflow-hidden">
              <div className={"h-3 rounded-full " + (pct > 85 ? 'bg-red-500' : pct > 70 ? 'bg-yellow-500' : 'bg-green-500')} style={{width: Math.min(pct, 100) + '%'}}></div>
            </div>
            <div className="flex justify-between text-xs text-gray-500 mt-1">
              <span>0</span><span className="text-yellow-600">85K safe ceiling</span><span>100K limit</span>
            </div>
          </div>
        )}

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">The 4 Autonomous Pipelines</div>
          <div className="space-y-4">
            {pipelines.map(p => (
              <div key={p.name} className={"border rounded-xl p-5 " + colorMap[p.color]}>
                <div className="flex items-center gap-3 mb-2 flex-wrap">
                  <span className={"text-sm font-bold font-mono " + textMap[p.color]}>{p.name}</span>
                  <span className="text-xs text-gray-500 bg-gray-800 px-2 py-0.5 rounded">{p.schedule}</span>
                  <span className={"text-xs font-bold px-2 py-0.5 rounded " + textMap[p.color]}>{p.tokens}</span>
                </div>
                <p className="text-xs text-gray-400 leading-relaxed">{p.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Architecture Layers -- L1 to L5</div>
          <div className="space-y-3">
            {architecture.map(item => (
              <div key={item.layer} className="flex gap-4 bg-gray-800 rounded-lg p-4">
                <div className="bg-purple-900 border border-purple-700 rounded-lg px-3 py-2 shrink-0 text-center min-w-16">
                  <div className="text-xs font-bold text-purple-400">{item.layer}</div>
                </div>
                <div>
                  <div className="text-sm font-bold text-purple-300 mb-1">{item.title}</div>
                  <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-yellow-800 rounded-xl p-6">
          <div className="text-xs text-yellow-600 uppercase tracking-wider mb-3">Academic Contribution -- L7 Autonomy Proof</div>
          <p className="text-sm text-gray-300 leading-relaxed mb-3">The Dev Console perspective provides the technical evidence for GNI&apos;s most significant engineering claim: a production-grade autonomous AI intelligence system running at .00/month. This is not a prototype or a demo -- it is a live system processing real news, making real predictions, and verifying them against real market outcomes.</p>
          <p className="text-sm text-gray-400 leading-relaxed">The 4-pipeline architecture, the self-healing heartbeat, and the Mission Control monitoring layer collectively demonstrate L7 autonomy: the system manages itself, responds to world events, and maintains quality -- all without human intervention after initial deployment.</p>
        </div>

      </main>
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">Warning: GNI data is for informational purposes only. Not financial advice.</p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | About -- Dev Console | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
