'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Prediction {
  id: string
  report_id: string
  horizon: string
  prediction_text: string
  direction: string
  confidence: number
  verify_date: string
  accuracy_score: number | null
  verified: boolean
  created_at: string
}

export default function PredictionsPage() {
  const [predictions, setPredictions] = useState<Prediction[]>([])
  const [loading, setLoading] = useState(true)
  const [filter, setFilter] = useState<'all' | 'pending' | 'verified'>('all')

  useEffect(() => {
    fetch('/api/predictions-list', { headers: { 'X-GNI-Key': GNI_KEY } })
      .then(r => r.json())
      .then(data => setPredictions(data.predictions || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const filtered = predictions.filter(p => {
    if (filter === 'pending') return !p.verified
    if (filter === 'verified') return p.verified
    return true
  })

  const pending = predictions.filter(p => !p.verified).length
  const verified = predictions.filter(p => p.verified).length
  const correct = predictions.filter(p => p.verified && p.accuracy_score && p.accuracy_score >= 70).length

  const directionColor = (d: string) => {
    if (d?.toLowerCase() === 'bearish') return 'text-red-400'
    if (d?.toLowerCase() === 'bullish') return 'text-green-400'
    return 'text-gray-400'
  }

  const horizonColor = (h: string) => {
    if (h === 'short') return 'bg-blue-900 text-blue-300'
    if (h === 'medium') return 'bg-yellow-900 text-yellow-300'
    return 'bg-purple-900 text-purple-300'
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/reports" className="inline-flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Feedback Loop</a>
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-white">GPVS Predictions</h1>
              <p className="text-sm text-gray-400">GNI Prediction Validation Standard — all predictions with verify dates</p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300">&larr; Dashboard</a>
          </div>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-white">{predictions.length}</div>
              <div className="text-xs text-gray-500">Total Predictions</div>
            </div>
            <div className="bg-yellow-950 border border-yellow-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-yellow-400">{pending}</div>
              <div className="text-xs text-yellow-600">Pending Verification</div>
            </div>
            <div className="bg-green-950 border border-green-800 rounded-lg p-3 text-center">
              <div className="text-2xl font-bold text-green-400">{verified}</div>
              <div className="text-xs text-green-600">Verified ({correct} correct)</div>
            </div>
          </div>
        
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
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">
        {loading && <div className="text-center py-20 text-gray-400">Loading predictions...</div>}

        {!loading && (
          <>
            <div className="flex gap-2 mb-6">
              {(['all', 'pending', 'verified'] as const).map(f => (
                <button key={f} onClick={() => setFilter(f)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors capitalize ${
                    filter === f ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                  }`}>
                  {f} ({f === 'all' ? predictions.length : f === 'pending' ? pending : verified})
                </button>
              ))}
            </div>

            {predictions.length === 0 && (
              <div className="text-center py-20 text-gray-400">
                <div className="text-4xl mb-4">&#x1F3AF;</div>
                <p>No predictions yet. MAD pipeline generates predictions with each debate run.</p>
              </div>
            )}

            <div className="space-y-3">
              {filtered.map(p => (
                <div key={p.id} className={`bg-gray-900 border rounded-xl p-4 ${p.verified ? 'border-green-800' : 'border-gray-700'}`}>
                  <div className="flex items-start justify-between gap-4 mb-2">
                    <p className="text-sm text-gray-200 leading-relaxed flex-1">{p.prediction_text}</p>
                    <div className="flex flex-col items-end gap-1 shrink-0">
                      <span className={`text-xs px-2 py-0.5 rounded-full font-bold ${horizonColor(p.horizon)}`}>
                        {p.horizon}
                      </span>
                      <span className={`text-sm font-bold ${directionColor(p.direction)}`}>
                        {p.direction?.toUpperCase()}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-4 text-xs text-gray-500 mt-2">
                    <span>Confidence: <span className="text-white font-bold">{p.confidence ? Math.round(p.confidence * 100) + '%' : 'N/A'}</span></span>
                    <span>Verify by: <span className="text-yellow-400">{p.verify_date ? new Date(p.verify_date).toLocaleDateString('en-US', { month: 'short', day: 'numeric', year: 'numeric' }) : 'TBD'}</span></span>
                    {p.verified && p.accuracy_score !== null && (
                      <span className={`font-bold ${p.accuracy_score >= 70 ? 'text-green-400' : 'text-red-400'}`}>
                        Score: {p.accuracy_score}%
                      </span>
                    )}
                    {!p.verified && (
                      <span className="text-yellow-600 font-bold">PENDING</span>
                    )}
                  </div>
                </div>
              ))}
            </div>

            <div className="mt-6 bg-gray-900 border border-gray-700 rounded-xl p-4 text-xs text-gray-400">
              <span className="text-white font-bold">How GPVS works: </span>
              Every MAD debate generates short (7d), medium (30d), and long (180d) horizon predictions.
              After the verify date passes, actual SPY market movement is compared to the prediction direction.
              Correct predictions increase source trust weights. Wrong predictions reduce them.
              Earliest verification: April 10, 2026.
            </div>
          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI GPVS Predictions | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}