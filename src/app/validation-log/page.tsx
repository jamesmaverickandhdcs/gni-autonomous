"use client"

export default function ValidationLogPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/reports" className="inline-flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Feedback Loop</a>
          <div className="flex items-center justify-between mt-2">
            <div>
              <h1 className="text-xl font-bold text-amber-300">📋 Validation Log</h1>
              <p className="text-xs text-gray-400">Agent accuracy revealed as predictions verify</p>
            </div>
            <span className="text-xs bg-amber-900 text-amber-300 border border-amber-700 px-3 py-1.5 rounded-lg font-bold">Available: April 10, 2026+</span>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6">

        {/* Coming Soon Banner */}
        <div className="bg-amber-950 border border-amber-700 rounded-xl p-6 mb-6 text-center">
          <div className="text-5xl mb-4">📋</div>
          <h2 className="text-xl font-bold text-amber-300 mb-2">Validation Log</h2>
          <p className="text-sm text-gray-300 max-w-2xl mx-auto leading-relaxed mb-4">
            When MAD predictions reach their verify date, GNI automatically scores each agent&apos;s directional accuracy against real-world outcomes. The Validation Log will surface which agents (Bull, Bear, Black Swan, Ostrich) were right, which were wrong, and what patterns emerge in their accuracy over time. This is the foundation of the GPVS feedback loop -- transforming past predictions into future intelligence improvements.
          </p>
          <div className="inline-flex items-center gap-2 bg-amber-900 border border-amber-700 rounded-lg px-4 py-2">
            <span className="text-xs text-amber-300">⏰ Available: <span className="font-bold text-white">April 10, 2026+</span></span>
          </div>
        </div>

        {/* What to Expect */}
        <div className="bg-gray-900 border border-amber-800 rounded-xl p-5 mb-6">
          <div className="text-xs text-amber-400 font-bold uppercase tracking-wider mb-4">What This Page Will Show</div>
          <ul className="space-y-2">
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Per-agent accuracy scores across all verified predictions</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Directional accuracy by time horizon (7d / 30d / 180d)</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Source weight adjustments triggered by prediction outcomes</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Surprise outcome detection -- when reality defied all agents</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>GPVS scorecard exportable for IEEE paper evidence</li>
          </ul>
        </div>

        {/* GPVS Dependency */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 mb-6">
          <div className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-2">Why This Requires GPVS Accumulation</div>
          <p className="text-xs text-gray-400 leading-relaxed">
            This page requires verified prediction data from the GPVS system. The earliest MAD predictions were made in March 2026 with verify dates starting April 10, 2026. As predictions verify over time, this page will automatically populate with real accuracy data. No manual intervention is needed -- GNI&apos;s autonomous pipeline handles verification and scoring automatically.
          </p>
        </div>

        {/* Current GPVS Status */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
          <div className="text-xs text-gray-500 font-bold uppercase tracking-wider mb-3">Current GPVS Status</div>
          <div className="grid grid-cols-3 gap-4 text-center">
            <div>
              <div className="text-xl font-bold text-amber-300">0</div>
              <div className="text-xs text-gray-500">Verified Predictions</div>
            </div>
            <div>
              <div className="text-xl font-bold text-amber-300">Apr 10</div>
              <div className="text-xs text-gray-500">First Verification</div>
            </div>
            <div>
              <div className="text-xl font-bold text-amber-300">April 10, 2026+</div>
              <div className="text-xs text-gray-500">Page Available</div>
            </div>
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Validation Log | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
