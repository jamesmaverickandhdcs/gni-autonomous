"use client"

export default function ModelLearningPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/reports" className="inline-flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Feedback Loop</a>
          <div className="flex items-center justify-between mt-2">
            <div>
              <h1 className="text-xl font-bold text-amber-300">🧠 Model Learning</h1>
              <p className="text-xs text-gray-400">How GNI recalibrates from surprise outcomes</p>
            </div>
            <span className="text-xs bg-amber-900 text-amber-300 border border-amber-700 px-3 py-1.5 rounded-lg font-bold">Available: Q3 2026</span>
          </div>
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
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-6">

        {/* Coming Soon Banner */}
        <div className="bg-amber-950 border border-amber-700 rounded-xl p-6 mb-6 text-center">
          <div className="text-5xl mb-4">🧠</div>
          <h2 className="text-xl font-bold text-amber-300 mb-2">Model Learning</h2>
          <p className="text-sm text-gray-300 max-w-2xl mx-auto leading-relaxed mb-4">
            Model Learning tracks every event where reality surprised GNI&apos;s predictions -- and how the system responded. When a Black Swan event occurs, source weights are recalibrated, prompt templates are adjusted in the A/B system, and the adaptive pipeline modifies its escalation thresholds. This page will document GNI&apos;s learning trajectory, showing measurable improvement in prediction accuracy over time.
          </p>
          <div className="inline-flex items-center gap-2 bg-amber-900 border border-amber-700 rounded-lg px-4 py-2">
            <span className="text-xs text-amber-300">⏰ Available: <span className="font-bold text-white">Q3 2026</span></span>
          </div>
        </div>

        {/* What to Expect */}
        <div className="bg-gray-900 border border-amber-800 rounded-xl p-5 mb-6">
          <div className="text-xs text-amber-400 font-bold uppercase tracking-wider mb-4">What This Page Will Show</div>
          <ul className="space-y-2">
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Surprise outcome registry -- events that defied all 4 agents</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Source bias corrections triggered by systematic errors</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>A/B prompt template evolution history</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Escalation threshold recalibration log</li>
              <li className="flex items-start gap-2 text-xs text-gray-400"><span className="text-amber-400 mt-0.5">•</span>Accuracy improvement trend across pipeline generations</li>
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
              <div className="text-xl font-bold text-amber-300">Q3 2026</div>
              <div className="text-xs text-gray-500">Page Available</div>
            </div>
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Model Learning | Higher Diploma in Computer Science | SUM
        </div>
      </footer>
    </div>
  )
}
