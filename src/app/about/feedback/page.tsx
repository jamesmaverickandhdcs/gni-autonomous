'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Prediction {
  id: string
  verify_date: string
  horizon: string
  direction: string
  verified: boolean
  correct: boolean | null
}

export default function AboutFeedbackPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    fetch('/api/predictions-list', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setPredictions(data.predictions || []))
      .catch(() => setError('Failed to load live data.'))
      .finally(() => setLoading(false))
  }, [])

  const pending = predictions.filter(p => !p.verified).length
  const verified = predictions.filter(p => p.verified).length
  const correct = predictions.filter(p => p.correct === true).length

  const swot = {
    strengths: [
      'Free-forever architecture — .00/month with zero compromise on capability',
      'Multi-agent MAD Protocol eliminates single-point-of-failure in threat assessment',
      'GPVS creates an empirical accuracy record — not theoretical claims',
      'Self-improving source weights via EMA — gets smarter every verified prediction',
      '66-pattern injection detection layer — adversarially robust pipeline',
      'L7 autonomous operation — zero human intervention required after deployment',
    ],
    weaknesses: [
      'Free-tier rate limits (100K tokens/day Groq) constrain analysis depth in high-escalation periods',
      'GPVS verification requires real time to pass — accuracy record still accumulating',
      'Binary BULLISH/BEARISH prediction oversimplifies complex multi-directional market movements',
      'English-language only — misses non-English geopolitical signals from ASEAN and beyond',
      'Prediction window limited to SPY as proxy — does not verify commodity or FX predictions directly',
      'Cold start problem — source weights need time to diverge from neutral baseline of 1.0',
    ],
    opportunities: [
      'Myanmar language integration (GNI_Myanmar) opens ASEAN-language intelligence gap',
      'GPVS verification compounding — accuracy advantage grows as predictions accumulate',
      'Pattern Library (Q4 2026) will enable predictive pattern matching across historical sequences',
      'Model Learning (Q3 2026) will enable autonomous recalibration from surprise outcomes',
      'API export layer enables third-party applications to build on GNI intelligence output',
      'L8 autonomy roadmap includes Mission Control-triggered pipeline response to breaking news',
    ],
    threats: [
      'Groq API terms change could eliminate free-tier access — single provider dependency',
      'Geopolitical escalation exceeding Groq quota ceiling could cause analysis gaps during crises',
      'RSS feed quality degradation if news sources change their feed structure or paywall content',
      'Market regime change could break GPVS calibration (prolonged low-volatility environment)',
      'Adversarial prompt injection evolving faster than the 66-pattern detection layer',
      'Vercel free-tier bandwidth limits under high-traffic scenarios',
    ]
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/about" className="inline-flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">Back to About</a>
          <h1 className="text-2xl font-bold text-amber-400">Feedback Loop — Active/Passive SWOT Analysis</h1>
          <p className="text-sm text-gray-400">A rigorous self-assessment of GNI through the Feedback Loop lens. Active SWOT examines internal capabilities and limitations. Passive SWOT maps external opportunities and threats. Combined with live prediction verification data, this provides the most honest and complete picture of where GNI stands and where it is going.</p>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        {loading && <div className="text-center py-8 text-gray-500">Loading live prediction data...</div>}
        {error && <div className="text-center py-8 text-red-400">{error}</div>}

        {!loading && (
          <div className="grid grid-cols-3 gap-4">
            {[
              { label: 'Total Predictions', value: String(predictions.length), color: 'text-amber-400' },
              { label: 'Pending Verification', value: String(pending), color: 'text-yellow-400' },
              { label: 'Verified Correct', value: String(correct) + '/' + String(verified), color: 'text-green-400' },
            ].map(item => (
              <div key={item.label} className="bg-gray-900 border border-gray-700 rounded-xl p-5 text-center">
                <div className={"text-3xl font-bold mb-1 " + item.color}>{item.value}</div>
                <div className="text-sm text-gray-400">{item.label}</div>
              </div>
            ))}
          </div>
        )}

        <div>
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3 text-center">Active SWOT — Internal Assessment</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-green-950 border border-green-800 rounded-xl p-5">
              <div className="text-sm font-bold text-green-400 mb-3">Strengths</div>
              <ul className="space-y-2">
                {swot.strengths.map((s, i) => (
                  <li key={i} className="flex gap-2 text-xs text-gray-300 leading-relaxed">
                    <span className="text-green-500 shrink-0 mt-0.5">+</span>{s}
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-red-950 border border-red-800 rounded-xl p-5">
              <div className="text-sm font-bold text-red-400 mb-3">Weaknesses</div>
              <ul className="space-y-2">
                {swot.weaknesses.map((w, i) => (
                  <li key={i} className="flex gap-2 text-xs text-gray-300 leading-relaxed">
                    <span className="text-red-500 shrink-0 mt-0.5">-</span>{w}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div>
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3 text-center">Passive SWOT — External Assessment</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <div className="bg-blue-950 border border-blue-800 rounded-xl p-5">
              <div className="text-sm font-bold text-blue-400 mb-3">Opportunities</div>
              <ul className="space-y-2">
                {swot.opportunities.map((o, i) => (
                  <li key={i} className="flex gap-2 text-xs text-gray-300 leading-relaxed">
                    <span className="text-blue-500 shrink-0 mt-0.5">+</span>{o}
                  </li>
                ))}
              </ul>
            </div>
            <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-5">
              <div className="text-sm font-bold text-yellow-400 mb-3">Threats</div>
              <ul className="space-y-2">
                {swot.threats.map((t, i) => (
                  <li key={i} className="flex gap-2 text-xs text-gray-300 leading-relaxed">
                    <span className="text-yellow-500 shrink-0 mt-0.5">!</span>{t}
                  </li>
                ))}
              </ul>
            </div>
          </div>
        </div>

        <div className="bg-gray-900 border border-amber-800 rounded-xl p-6">
          <div className="text-xs text-amber-600 uppercase tracking-wider mb-3">The Feedback Loop Conclusion</div>
          <p className="text-sm text-gray-300 leading-relaxed mb-3">GNI&apos;s greatest strength is also its greatest research contribution: the feedback loop itself. Most AI systems produce outputs and stop. GNI produces outputs, measures them against reality, and uses that measurement to improve future outputs. This self-correcting mechanism is what separates a static intelligence tool from a genuinely autonomous one.</p>
          <p className="text-sm text-gray-400 leading-relaxed">The weaknesses identified here are not failures — they are the honest boundaries of what a .00/month system can achieve in Sprint 1. Each weakness maps directly to a Phase 2 improvement on the development roadmap.</p>
        </div>

      </main>
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">Warning: GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.</p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | About — Feedback Loop | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
