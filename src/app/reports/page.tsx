'use client'
import { useEffect, useState } from 'react'

interface Prediction {
  id: string
  direction: string
  confidence: number
  verify_date: string
  accuracy_score: number | null
  agent_name: string
  created_at: string
}

export default function ReportsHub() {
  const [predictions, setPredictions] = useState<Prediction[]>([])

  useEffect(() => {
    fetch('/api/predictions-list')
      .then(r => r.json())
      .then(data => setPredictions(data.predictions || []))
      .catch(() => {})
  }, [])

  const pending = predictions.filter(p => p.accuracy_score === null)
  const verified = predictions.filter(p => p.accuracy_score !== null)
  const nextVerify = pending.length > 0
    ? pending.sort((a, b) => new Date(a.verify_date).getTime() - new Date(b.verify_date).getTime())[0]
    : null
  const daysToNext = nextVerify
    ? Math.max(0, Math.ceil((new Date(nextVerify.verify_date).getTime() - Date.now()) / 86400000))
    : null

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-amber-300">🎯 Feedback Loop</h1>
              <p className="text-xs text-gray-400">What did reality confirm or surprise, and what does GNI do next?</p>
            </div>
            
          </div>
          <div className="flex flex-wrap gap-2">
            <a href="/" className="flex items-center gap-1.5 bg-blue-900 hover:bg-blue-700 border border-blue-700 rounded-lg px-3 py-1.5 text-xs font-bold text-blue-200 transition-colors">
              🎯 Quantum Strategist
            </a>
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Researcher
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Dev Console
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {/* Intro */}
        <div className="bg-amber-950 border border-amber-700 border-l-4 border-l-amber-400 rounded-xl p-5 mb-6">
          <p className="text-sm text-gray-100 leading-relaxed">
            Feedback Loop is GNI&apos;s reality validation hub -- the place where predictions meet outcomes and where GNI learns from what actually happened in the world.
            Every MAD debate produces directional predictions (BULLISH or BEARISH) with a specific verify date, allowing GNI to score its own accuracy objectively using the GPVS standard.
            The GPVS (GNI Prediction Validation Standard) tracks each agent&apos;s directional accuracy across three time horizons: 7-day, 30-day, and 180-day predictions.
            As predictions verify over time, source trust weights are automatically adjusted -- sources whose articles led to accurate predictions gain higher weight in future pipeline runs.
            This self-correcting feedback mechanism is what elevates GNI beyond a static intelligence system into a continuously learning autonomous platform.
          </p>
        </div>
        {/* GPVS Status */}
        <div className="grid grid-cols-3 gap-4 mb-8">
          <div className="bg-amber-950 border border-amber-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-amber-300">{predictions.length}</div>
            <div className="text-xs text-gray-500 mt-1">Total Predictions</div>
          </div>
          <div className="bg-amber-950 border border-amber-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-amber-300">{pending.length}</div>
            <div className="text-xs text-gray-500 mt-1">Pending Verification</div>
          </div>
          <div className="bg-amber-950 border border-amber-700 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-amber-300">{verified.length}</div>
            <div className="text-xs text-gray-500 mt-1">Verified by GPVS</div>
          </div>
        </div>

        {/* Next Verification Countdown */}
        {nextVerify && (
          <div className="bg-amber-950 border border-amber-700 rounded-xl p-4 mb-6">
            <div className="text-xs text-amber-400 font-bold uppercase tracking-wider mb-2">⏰ Next Verification</div>
            <div className="flex items-center gap-4">
              <div className="text-3xl font-bold text-white">{daysToNext}d</div>
              <div>
                <div className="text-sm text-gray-300">
                  {nextVerify.direction?.toUpperCase()} prediction by {nextVerify.agent_name || 'MAD Agent'}
                </div>
                <div className="text-xs text-gray-500">
                  Verify date: {new Date(nextVerify.verify_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' })}
                </div>
              </div>
            </div>
          </div>
        )}

        {/* Predictions Page Link */}
        <div className="text-xs text-amber-400 uppercase tracking-wider mb-4 font-bold">Active Reports</div>
       <a href="/predictions" className="block bg-amber-950 border border-amber-700 hover:border-amber-500 hover:bg-amber-900 rounded-xl p-5 mb-4 transition-colors">
          <div className="flex items-center gap-3 mb-2">
            <span className="text-xs font-bold text-amber-400 bg-amber-950 border border-amber-700 rounded-full w-6 h-6 flex items-center justify-center shrink-0">01</span>
            <span className="text-xl">🎯</span>
            <div className="text-sm font-bold text-white">Predictions</div>
            <span className="text-xs bg-amber-900 text-amber-300 px-2 py-0.5 rounded-full ml-auto">LIVE</span>
          </div>
          <p className="text-xs text-gray-300 leading-relaxed mb-3">All MAD agent predictions with verify dates, confidence levels, and GPVS accuracy scores -- the complete prediction ledger. Each prediction is tagged with the agent that made it (Bull, Bear, Black Swan, or Ostrich) and the specific time horizon for verification. Active insights are surfaced automatically when predictions reach their verify date and reality confirms or contradicts GNI&apos;s forecast.</p>
          <div className="flex items-center justify-between">
            <div className="flex gap-4 text-xs">
              <span className="text-amber-400">{pending.length} pending</span>
              <span className="text-green-400">{verified.length} verified</span>
              <span className="text-gray-500">Earliest: April 10, 2026</span>
            </div>
            <span className="text-xs font-bold text-amber-200 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 transition-colors">View Predictions →</span>
          </div>
        </a>

        {/* Future Pages */}
        <div className="text-xs text-amber-400 uppercase tracking-wider mb-4 font-bold">Passive Reports -- Coming as GPVS Accumulates</div>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <a href="/validation-log" className="bg-gray-900 border border-amber-900 hover:border-amber-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold text-amber-400 bg-amber-950 border border-amber-800 rounded-full w-6 h-6 flex items-center justify-center shrink-0">02</span>
              <span className="text-base">📋</span>
              <div className="text-sm font-bold text-amber-200">Validation Log</div>
              <span className="text-xs bg-gray-800 text-gray-500 px-2 py-0.5 rounded-full ml-auto">FUTURE</span>
            </div>
            <div className="text-xs text-amber-600 mb-2">Available: April 10, 2026+</div>
            <p className="text-xs text-gray-500 leading-relaxed">When predictions verify accurately -- which agent was right, which was wrong, and what patterns emerge in their accuracy over time. The GPVS scorecard in full detail.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-amber-300 bg-amber-950 border border-amber-800 rounded-lg px-3 py-1.5">Preview →</span>
            </div>
          </a>
          <a href="/model-learning" className="bg-gray-900 border border-amber-900 hover:border-amber-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold text-amber-400 bg-amber-950 border border-amber-800 rounded-full w-6 h-6 flex items-center justify-center shrink-0">03</span>
              <span className="text-base">🧠</span>
              <div className="text-sm font-bold text-amber-200">Model Learning</div>
              <span className="text-xs bg-gray-800 text-gray-500 px-2 py-0.5 rounded-full ml-auto">FUTURE</span>
            </div>
            <div className="text-xs text-amber-600 mb-2">Available: Q3 2026</div>
            <p className="text-xs text-gray-500 leading-relaxed">Surprise outcomes, model recalibration events, and source bias corrections. Tracks how GNI improves its prediction accuracy over time through autonomous self-correction.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-amber-300 bg-amber-950 border border-amber-800 rounded-lg px-3 py-1.5">Preview →</span>
            </div>
          </a>
          <a href="/pattern-library" className="bg-gray-900 border border-amber-900 hover:border-amber-600 rounded-xl p-4 transition-colors">
            <div className="flex items-center gap-2 mb-2">
              <span className="text-xs font-bold text-amber-400 bg-amber-950 border border-amber-800 rounded-full w-6 h-6 flex items-center justify-center shrink-0">04</span>
              <span className="text-base">📚</span>
              <div className="text-sm font-bold text-amber-200">Pattern Library</div>
              <span className="text-xs bg-gray-800 text-gray-500 px-2 py-0.5 rounded-full ml-auto">FUTURE</span>
            </div>
            <div className="text-xs text-amber-600 mb-2">Available: Q4 2026</div>
            <p className="text-xs text-gray-500 leading-relaxed">When current escalation matches historical validated sequences, GNI predicts what comes next. The most advanced predictive capability in the GNI roadmap.</p>
            <div className="flex justify-end mt-3">
              <span className="text-xs font-bold text-amber-300 bg-amber-950 border border-amber-800 rounded-lg px-3 py-1.5">Preview →</span>
            </div>
          </a>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Feedback Loop Hub | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
