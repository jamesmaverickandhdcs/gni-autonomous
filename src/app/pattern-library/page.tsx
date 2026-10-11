"use client"

export default function PatternLibraryPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/reports" className="inline-flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Feedback Loop</a>
          <div className="flex items-center justify-between mt-2">
            <div>
              <h1 className="text-xl font-bold text-amber-300">📚 Pattern Library</h1>
              <p className="text-xs text-gray-400">Pattern Library will look for current escalation sequences that match validated patterns in GNI&apos;s prediction archive, and surface the historical outcome as a signal for what may come next. Nothing in the engine matches sequences yet; this page holds the plan.</p>
            </div>
            <span className="text-xs bg-amber-900 text-amber-300 border border-amber-700 px-3 py-1.5 rounded-lg font-bold">In development</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6">

        {/* Coming Soon Banner */}
        <div className="bg-amber-950 border border-amber-700 rounded-xl p-6 mb-6 text-center">
          <div className="text-5xl mb-4">📚</div>
          <h2 className="text-xl font-bold text-amber-300 mb-2">Pattern Library</h2>
          <p className="text-sm text-gray-300 max-w-2xl mx-auto leading-relaxed mb-4">
            The Pattern Library is GNI&apos;s most advanced future capability — a database of validated escalation sequences that have historically preceded specific geopolitical outcomes. When current escalation scores match a historical validated sequence, GNI will proactively predict what comes next based on prior evidence. This transforms GNI from a reactive intelligence system into a predictive pattern-matching platform.
          </p>
          <div className="inline-flex items-center gap-2 bg-amber-900 border border-amber-700 rounded-lg px-4 py-2">
            <span className="text-xs text-amber-300">⏰ Status: <span className="font-bold text-white">In development</span></span>
          </div>
        </div>

        {/* What to Expect */}
        <div className="bg-gray-900 border border-amber-800 rounded-xl p-5 mb-6">
          <div className="text-xs text-amber-400 font-bold uppercase tracking-wider mb-4">What This Page Will Show</div>
          <ul className="space-y-2">
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Validated escalation sequences with historical outcome records</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Pattern match alerts when current data resembles past sequences</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Sequence similarity scoring using confidence intervals</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Cross-pillar pattern detection (GEO + TECH + FIN convergence)</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Pattern library exportable for academic research</li>
          </ul>
        </div>

        {/* GPVS Dependency */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 mb-6">
          <div className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-2">Why This Requires GPVS Accumulation</div>
          <p className="text-xs text-gray-400 leading-relaxed">
            This page requires verified prediction data from the GPVS system. Read from the database on 11 October 2026, the earliest stored debate prediction was made on 24 May 2026, with a verify-by date of 7 June 2026. As predictions verify over time, this page will automatically populate with real accuracy data. No manual intervention is needed — GNI&apos;s autonomous pipeline handles verification and scoring automatically.
          </p>
        </div>

        {/* Current GPVS Status */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
          <div className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-3">Current GPVS Status</div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <a href="/predictions" className="text-xl font-bold text-amber-300 hover:text-amber-200">Live count &rarr;</a>
              <div className="text-xs text-gray-500">Verified Predictions</div>
            </div>
            <div>
              <div className="text-xl font-bold text-amber-300">Jun 7</div>
              <div className="text-xs text-gray-500">First Stored Verify-By</div>
            </div>
            <div>
              <div className="text-xl font-bold text-amber-300">In development</div>
              <div className="text-xs text-gray-500">Page Status</div>
            </div>
          </div>
        </div>

      </main>

      
      {/* DISCLAIMER */}
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">
            ⚠️ <strong>Disclaimer:</strong> GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.
          </p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Pattern Library | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
