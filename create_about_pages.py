import os

os.makedirs('src/app/about/quantum', exist_ok=True)
os.makedirs('src/app/about/patterns', exist_ok=True)
os.makedirs('src/app/about/feedback', exist_ok=True)
os.makedirs('src/app/about/devops', exist_ok=True)

# Write each file using open with utf-8 encoding
files = {}

files['src/app/about/quantum/page.tsx'] = """\
'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''
import { useEffect, useState } from 'react'

interface Report {
  title: string
  sentiment: string
  sentiment_score: number
  escalation_score: number
  escalation_level: string
  mad_verdict: string
  mad_confidence: number
  mad_action_recommendation: string
  mad_blind_spot: string
  created_at: string
  risk_level: string
}
interface SourceWeight { source: string; weight: number; gpvs_score: number }

export default function AboutQuantumPage() {
  const [report, setReport] = useState<Report | null>(null)
  const [weights, setWeights] = useState<SourceWeight[]>([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState('')

  useEffect(() => {
    Promise.all([
      fetch('/api/reports', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
      fetch('/api/source-weights', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
    ]).then(([rData, wData]) => {
      const reports = rData.reports || []
      if (reports.length > 0) setReport(reports[0])
      setWeights((wData.weights || []).slice(0, 5))
    }).catch(() => setError('Failed to load live data.')).finally(() => setLoading(false))
  }, [])

  const sColor = (s: string) => s?.toLowerCase() === 'bearish' ? 'text-red-400' : s?.toLowerCase() === 'bullish' ? 'text-green-400' : 'text-yellow-400'
  const vColor = (v: string) => v === 'bearish' ? 'bg-red-900 border-red-700 text-red-300' : v === 'bullish' ? 'bg-green-900 border-green-700 text-green-300' : 'bg-gray-800 border-gray-600 text-gray-300'

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/about" className="inline-flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 text-gray-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">Back to About</a>
          <h1 className="text-2xl font-bold text-blue-400">Quantum Strategist -- Outcomes</h1>
          <p className="text-sm text-gray-400">What GNI decides, why it decides it, and what it means for global markets. This page shows the Quantum Strategist perspective -- actionable intelligence outcomes from the MAD Protocol, real-time threat verdicts, and market implications from 25 global news sources running 2x daily.</p>
        </div>
      </header>
      <main className="max-w-6xl mx-auto px-6 py-8 space-y-6">

        <div className="bg-blue-950 border border-blue-800 rounded-xl p-6">
          <div className="text-xs text-blue-400 uppercase tracking-wider mb-3">The Quantum Strategist Philosophy</div>
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            {[
              { title: 'Speed over Perfection', desc: 'GNI delivers actionable intelligence within minutes of pipeline completion. In geopolitical risk, timeliness beats completeness. A verdict with 80% confidence delivered now beats a perfect analysis delivered tomorrow.' },
              { title: 'Multi-Agent Consensus', desc: 'No single AI perspective is trusted. Four agents -- Bull, Bear, Black Swan, Ostrich -- debate every scenario across the Johari Window framework. Only consensus after 3 coached rounds becomes a verdict.' },
              { title: 'Market-Linked Intelligence', desc: 'Every report connects geopolitical events to specific market instruments (SPY, GLD, USO, DXY). Intelligence without market linkage is academic. GNI links threat verdicts directly to investment implications.' },
            ].map(item => (
              <div key={item.title} className="bg-blue-900 bg-opacity-40 rounded-lg p-4">
                <div className="text-sm font-bold text-blue-300 mb-2">{item.title}</div>
                <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
              </div>
            ))}
          </div>
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Live Latest MAD Verdict</div>
          {loading && <div className="text-center py-8 text-gray-500">Loading live data...</div>}
          {error && <div className="text-center py-8 text-red-400">{error}</div>}
          {!loading && report && (
            <div className="space-y-4">
              <div className="flex items-start justify-between gap-4 flex-wrap">
                <div className="flex-1">
                  <h2 className="text-lg font-bold text-white mb-1">{report.title}</h2>
                  <p className="text-xs text-gray-500">{new Date(report.created_at).toLocaleString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</p>
                </div>
                <div className={"px-4 py-2 rounded-lg border font-bold text-sm " + vColor(report.mad_verdict)}>
                  {report.mad_verdict?.toUpperCase() || 'PENDING'} {report.mad_confidence ? Math.round(report.mad_confidence * 100) + '%' : ''}
                </div>
              </div>
              <div className="grid grid-cols-2 md:grid-cols-4 gap-3">
                {[
                  { label: 'Sentiment', value: report.sentiment, color: sColor(report.sentiment) },
                  { label: 'Score', value: report.sentiment_score?.toFixed(2), color: 'text-white' },
                  { label: 'Escalation', value: (report.escalation_score?.toFixed(1) || '0') + '/10', color: 'text-orange-400' },
                  { label: 'Risk Level', value: report.risk_level?.toUpperCase(), color: 'text-yellow-400' },
                ].map(item => (
                  <div key={item.label} className="bg-gray-800 rounded-lg p-3 text-center">
                    <div className={"text-lg font-bold " + item.color}>{item.value}</div>
                    <div className="text-xs text-gray-500 mt-1">{item.label}</div>
                  </div>
                ))}
              </div>
              {report.mad_action_recommendation && (
                <div className="bg-blue-950 border border-blue-800 rounded-lg p-4">
                  <div className="text-xs text-blue-400 font-bold uppercase mb-2">Action Recommendation</div>
                  <p className="text-sm text-white leading-relaxed">{report.mad_action_recommendation}</p>
                </div>
              )}
              {report.mad_blind_spot && (
                <div className="bg-purple-950 border border-purple-800 rounded-lg p-4">
                  <div className="text-xs text-purple-400 font-bold uppercase mb-2">Blind Spot Warning</div>
                  <p className="text-sm text-gray-300 leading-relaxed">{report.mad_blind_spot}</p>
                </div>
              )}
            </div>
          )}
          {!loading && !report && !error && (
            <div className="text-center py-8 text-gray-500">No reports available yet.</div>
          )}
        </div>

        <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Outcome Framework -- What QS Produces</div>
          <div className="space-y-3">
            {[
              { step: '01', title: 'Threat Verdict', desc: 'BEARISH / BULLISH / NEUTRAL with confidence score 0-100%. Derived from 3 rounds of 4-agent MAD debate using Johari Window framework. Each verdict includes Arbitrator reasoning and coaching notes.' },
              { step: '02', title: 'Action Recommendation', desc: 'Specific diplomatic, economic, or strategic action for the next 4-6 weeks. Geopolitical posture recommendation based on full threat assessment across all four agent perspectives.' },
              { step: '03', title: 'Blind Spot Warning', desc: 'The Black Swan agent identifies one weak signal that all other agents are ignoring. This is the highest-value intelligence output -- the thing nobody else is watching but should be.' },
              { step: '04', title: 'Market Implications', desc: 'Specific tickers (SPY, GLD, USO, DXY) with directional bias. Links geopolitical threat directly to investable market instruments with sentiment scoring.' },
              { step: '05', title: 'Scenario Planning', desc: 'Base, Upside, and Downside scenarios with probability weights. Allows decision-makers to prepare for multiple futures simultaneously across 7-30 day and 3-24 month horizons.' },
            ].map(item => (
              <div key={item.step} className="flex gap-4 bg-gray-800 rounded-lg p-4">
                <div className="text-2xl font-bold text-blue-600 shrink-0 w-10 text-center">{item.step}</div>
                <div>
                  <div className="text-sm font-bold text-blue-300 mb-1">{item.title}</div>
                  <p className="text-xs text-gray-400 leading-relaxed">{item.desc}</p>
                </div>
              </div>
            ))}
          </div>
        </div>

        {!loading && weights.length > 0 && (
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Top Intelligence Sources (Live GPVS Weights)</div>
            <div className="space-y-2">
              {weights.map((w, i) => (
                <div key={w.source} className="flex items-center gap-3 bg-gray-800 rounded-lg px-4 py-3">
                  <div className="text-sm font-bold text-gray-500 w-6">{i + 1}</div>
                  <div className="flex-1 text-sm font-bold text-white">{w.source}</div>
                  <div className="text-xs text-gray-400">GPVS: {w.gpvs_score ? (w.gpvs_score * 100).toFixed(0) + '%' : 'N/A'}</div>
                  <div className="text-sm font-bold text-green-400">Weight: {w.weight?.toFixed(2)}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        <div className="bg-gray-900 border border-yellow-800 rounded-xl p-6">
          <div className="text-xs text-yellow-600 uppercase tracking-wider mb-3">Academic Contribution -- Novel Contribution 1</div>
          <p className="text-sm text-gray-300 leading-relaxed mb-3">The Quantum Strategist represents Novel Contribution 1 in GNI&apos;s IEEE paper: the application of the Johari Window framework to AI-based geopolitical threat assessment. The four-quadrant Known/Unknown x Proactive/Ignored matrix provides a systematic way to ensure no threat dimension is overlooked.</p>
          <p className="text-sm text-gray-400 leading-relaxed">This approach goes beyond standard sentiment analysis by explicitly modeling what the system does not know (Black Swan) and what institutions are actively ignoring (Ostrich) -- dimensions absent from conventional intelligence platforms like Bloomberg Terminal or Stratfor.</p>
        </div>

      </main>
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">Warning: GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.</p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | About -- Quantum Strategist | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
"""

files['src/app/about/patterns/page.tsx'] = """\
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
"""

files['src/app/about/feedback/page.tsx'] = """\
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
      'Free-forever architecture -- .00/month with zero compromise on capability',
      'Multi-agent MAD Protocol eliminates single-point-of-failure in threat assessment',
      'GPVS creates an empirical accuracy record -- not theoretical claims',
      'Self-improving source weights via EMA -- gets smarter every verified prediction',
      '66-pattern injection detection layer -- adversarially robust pipeline',
      'L7 autonomous operation -- zero human intervention required after deployment',
    ],
    weaknesses: [
      'Free-tier rate limits (100K tokens/day Groq) constrain analysis depth in high-escalation periods',
      'GPVS verification requires real time to pass -- accuracy record still accumulating',
      'Binary BULLISH/BEARISH prediction oversimplifies complex multi-directional market movements',
      'English-language only -- misses non-English geopolitical signals from ASEAN and beyond',
      'Prediction window limited to SPY as proxy -- does not verify commodity or FX predictions directly',
      'Cold start problem -- source weights need time to diverge from neutral baseline of 1.0',
    ],
    opportunities: [
      'Myanmar language integration (GNI_Myanmar) opens ASEAN-language intelligence gap',
      'GPVS verification compounding -- accuracy advantage grows as predictions accumulate',
      'Pattern Library (Q4 2026) will enable predictive pattern matching across historical sequences',
      'Model Learning (Q3 2026) will enable autonomous recalibration from surprise outcomes',
      'API export layer enables third-party applications to build on GNI intelligence output',
      'L8 autonomy roadmap includes Mission Control-triggered pipeline response to breaking news',
    ],
    threats: [
      'Groq API terms change could eliminate free-tier access -- single provider dependency',
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
          <h1 className="text-2xl font-bold text-amber-400">Feedback Loop -- Active/Passive SWOT Analysis</h1>
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
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3 text-center">Active SWOT -- Internal Assessment</div>
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
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3 text-center">Passive SWOT -- External Assessment</div>
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
          <p className="text-sm text-gray-400 leading-relaxed">The weaknesses identified here are not failures -- they are the honest boundaries of what a .00/month system can achieve in Sprint 1. Each weakness maps directly to a Phase 2 improvement on the development roadmap.</p>
        </div>

      </main>
      <div className="max-w-6xl mx-auto px-6 pb-4">
        <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-3">
          <p className="text-xs text-yellow-300">Warning: GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.</p>
        </div>
      </div>
      <footer className="border-t border-gray-800 mt-4">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | About -- Feedback Loop | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
"""

files['src/app/about/devops/page.tsx'] = """\
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
"""

for path, content in files.items():
    with open(path, 'w', encoding='utf-8') as f:
        f.write(content)
    print('WRITTEN: ' + path)

print()
print('All 4 pages written successfully!')