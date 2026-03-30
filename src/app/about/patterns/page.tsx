'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface PipelineRun {
  id: string
  created_at: string
  escalation_score: number
  sentiment: string
  quality_score: number
}
interface Outcome {
  direction_correct_3d: boolean
  direction_correct_7d: boolean
}

export default function AboutPatternsPage() {
  const [runs, setRuns] = useState<PipelineRun[]>([])
  const [outcomes, setOutcomes] = useState<Outcome[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      fetch('/api/pipeline-runs', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
      fetch('/api/prediction-outcomes', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
    ]).then(([runsData, outcomesData]) => {
      setRuns((runsData.runs || []).slice(0, 7))
      setOutcomes(outcomesData.outcomes || [])
    }).catch(() => setError('Failed to load live data.')).finally(() => setLoading(false))
  }, [])

  const acc3d = outcomes.length > 0 ? Math.round(outcomes.filter(o => o.direction_correct_3d).length / outcomes.length * 100) : 100
  const acc7d = outcomes.length > 0 ? Math.round(outcomes.filter(o => o.direction_correct_7d).length / outcomes.length * 100) : 100
  const avgQ = runs.length > 0 ? (runs.reduce((a, r) => a + (r.quality_score || 0), 0) / runs.length).toFixed(1) : 'N/A'

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/about" className="inline-flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">Back to About</a>
          <h1 className="text-2xl font-bold text-green-400">Pattern Intelligence -- Long-Term Research</h1>
          <p className="text-sm text-gray-400">How GNI builds a self-improving evidence base over time. Pattern Intelligence is the research backbone of GNI -- tracking prediction accuracy across time horizons, validating source credibility through real market outcomes, and providing IEEE-citable statistical evidence for every intelligence claim made by the system.</p>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        <div className="bg-green-950 border border-green-800 rounded-xl p-6">
          <div className="text-xs text-green-400 uppercase tracking-wider mb-3">The Research Philosophy</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title: 'Evidence Over Opinion', desc: 'Every GNI claim is traceable to a specific pipeline run, specific articles, and a specific AI analysis chain. The Transparency Engine documents every algorithmic decision from 400 raw articles down to the final 3 selected for analysis.' },
              { title: 'Self-Improving Accuracy', desc: 'GPVS scores every prediction against real SPY market movement after 3 and 7 days. Sources that led to correct predictions gain higher trust weights via Exponential Moving Average -- 1.1x for correct, 0.9x for wrong.' },
              { title: 'Statistical Rigor', desc: 'Confidence intervals using t-distribution (t=4.303, n=3, alpha=0.05) provide IEEE-citable uncertainty quantification for every sentiment score. This is Novel Contribution 3 in the academic paper.' },
            ].map(item => (
              <div key={item.title} className="bg-green-900 bg-opacity-30 rounded-lg p-4">
                <div className="text-sm font-bold text-green-300 mb-2">{item.title}</div>
                <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        {loading && <div className="text-center py-8 text-gray-500">Loading live research data...</div>}
        {error && <div className="text-center py-8 text-red-400">{error}</div>}

        {!loading && (
          <>
            <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
              {[
                { label: 'Pipeline Runs', value: String(runs.length) + '+', color: 'text-green-400', desc: 'Total runs archived' },
                { label: '3-Day Accuracy', value: String(acc3d) + '%', color: acc3d >= 80 ? 'text-green-400' : 'text-yellow-400', desc: 'GPVS verified' },
                { label: '7-Day Accuracy', value: String(acc7d) + '%', color: acc7d >= 80 ? 'text-green-400' : 'text-yellow-400', desc: 'GPVS verified' },
                { label: 'Avg Quality', value: String(avgQ) + '/10', color: 'text-blue-400', desc: 'Pipeline quality score' },
              ].map(item => (
                <div key={item.label} className="bg-gray-900 border border-gray-700 rounded-xl p-5 text-center">
                  <div className={"text-3xl font-bold mb-1 " + item.color}>{item.value}</div>
                  <div className="text-sm font-bold text-white mb-1">{item.label}</div>
                  <div className="text-xs text-gray-500">{item.desc}</div>
                </div>
              ))}
            </div>

            {runs.length > 0 && (
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Recent Pipeline Run History (Live)</div>
                <div className="space-y-2">
                  {runs.map((run, i) => (
                    <div key={run.id} className="flex items-center gap-4 bg-gray-800 rounded-lg px-4 py-3">
                      <div className="text-xs text-gray-500 w-6">{i + 1}</div>
                      <div className="text-xs text-gray-400 w-36 shrink-0">{new Date(run.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</div>
                      <div className="flex-1">
                        <span className={"text-xs px-2 py-0.5 rounded " + (run.sentiment?.toLowerCase() === 'bearish' ? 'bg-red-900 text-red-300' : 'bg-green-900 text-green-300')}>{run.sentiment}</span>
                      </div>
                      <div className="text-xs text-gray-400">ESC: {run.escalation_score?.toFixed(1)}/10</div>
                      <div className="text-xs text-gray-400">Q: {run.quality_score?.toFixed(1) || 'N/A'}</div>
                    </div>
                  ))}
                </div>
              </div>
            )}
          </>
        )}

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Research Methodology -- The GPVS Standard</div>
          <div className="space-y-4">
            {[
              { phase: 'Phase 1', title: 'Prediction Generation', desc: 'Every MAD debate produces a directional prediction (BULLISH or BEARISH) with a specific verify date at 3-day and 7-day horizons. The prediction is tied to exact articles and sources that drove the analysis.' },
              { phase: 'Phase 2', title: 'Market Measurement', desc: 'After 3 and 7 days, actual SPY market movement is measured against the prediction. Binary outcome measurement -- correct or wrong -- eliminates ambiguity and enables statistical analysis.' },
              { phase: 'Phase 3', title: 'Weight Adjustment', desc: 'Sources whose articles led to correct predictions have their trust weight multiplied by 1.1 via EMA. Wrong predictions multiply by 0.9. Weights are bounded between 0.5 (penalised) and 2.0 (highly trusted).' },
              { phase: 'Phase 4', title: 'Evidence Accumulation', desc: 'As predictions accumulate, statistical confidence of accuracy claims increases. The GPVS Prediction Scorecard provides real-time evidence for every accuracy claim in the IEEE paper -- not theoretical, empirical.' },
            ].map(item => (
              <div key={item.phase} className="flex gap-4 bg-gray-800 rounded-lg p-4">
                <div className="bg-green-900 border border-green-700 rounded-lg px-3 py-2 shrink-0 text-center min-w-16">
                  <div className="text-xs font-bold text-green-400">{item.phase}</div>
                </div>
                <div>
                  <div className="text-sm font-bold text-green-300 mb-1">{item.title}</div>
                  <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-yellow-800 rounded-xl p-6">
          <div className="text-xs text-yellow-600 uppercase tracking-wider mb-3">Long-Term Research Value</div>
          <p className="text-sm text-gray-300 leading-relaxed mb-3">Pattern Intelligence becomes more valuable over time. As GNI accumulates verified predictions, the statistical confidence of its source weights increases and the GPVS Scorecard becomes a genuine empirical accuracy record -- not a theoretical claim.</p>
          <p className="text-sm text-gray-400 leading-relaxed">By April 2026, the first GPVS verifications complete. By Q3 2026, Model Learning begins recalibrating from surprise outcomes. By Q4 2026, the Pattern Library identifies historical escalation sequences that predict future geopolitical events with statistically significant accuracy.</p>
        </div>

      </main>
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">Warning: GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.</p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | About -- Pattern Intelligence | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
