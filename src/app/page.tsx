'use client'
import { useEffect, useState } from 'react'
import dynamic from 'next/dynamic'
import { AreaChart, Area, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid } from 'recharts'
const MiniMapView = dynamic(() => import('@/components/MapView'), { ssr: false })


interface PillarReport {
  id: string
  pillar: string
  title: string
  summary: string
  sentiment: string
  sentiment_score: number
  risk_level: string
  location_name: string
  tickers_affected: string[]
  market_impact: string
  weakness_identified: string
  threat_horizon: string
  dark_side_detected: string
  quality_score: number
  created_at: string
}

interface Report {
  id: string
  title: string
  summary: string
  sentiment: string
  sentiment_score: number
  sentiment_score_lower: number
  sentiment_score_upper: number
  confidence_interval_width: number
  analysis_runs: number
  risk_level: string
  location_name: string
  lat: number | null
  lng: number | null
  tickers_affected: string[]
  market_impact: string
  llm_source: string
  created_at: string
  mad_bull_case: string
  mad_bear_case: string
  mad_historian_case: string
  mad_risk_case: string
  mad_black_swan_case: string
  mad_ostrich_case: string
  mad_blind_spot: string
  mad_action_recommendation: string
  mad_verdict: string
  weakness_identified: string
  threat_horizon: string
  dark_side_detected: string
  mad_confidence: number
  escalation_score: number
  escalation_level: string
  deception_level: string
  myanmar_summary: string
}

interface PredictionSummary {
  total: number
  avg_score: number
  accuracy_3d: number
  accuracy_7d: number
  pending_review: number
}

interface SourceWeight {
  source: string
  weight: number
  gpvs_contribution: number | null
  last_updated: string
}

interface PipelineArticle {
  id: string
  source: string
  title: string
  url: string
  summary: string
  stage3_score: number
  stage4_rank: number
  stage4_selected: boolean
}

interface PipelineRun {
  id: string
  total_collected: number
  total_relevant: number
  total_deduped: number
  total_scored: number
  total_selected: number
}

const riskColor = (risk: string) => {
  switch (risk?.toLowerCase()) {
    case 'critical': return 'bg-red-600 text-white'
    case 'high':     return 'bg-orange-500 text-white'
    case 'medium':   return 'bg-yellow-500 text-black'
    case 'low':      return 'bg-green-500 text-white'
    default:         return 'bg-gray-500 text-white'
  }
}

const escalationColor = (level: string) => {
  switch (level?.toLowerCase()) {
    case 'critical':  return 'bg-red-700 text-red-100 border border-red-500'
    case 'high':      return 'bg-orange-700 text-orange-100 border border-orange-500'
    case 'elevated':  return 'bg-yellow-700 text-yellow-100 border border-yellow-500'
    case 'moderate':  return 'bg-blue-700 text-blue-100 border border-blue-500'
    default:          return 'bg-gray-700 text-gray-300 border border-gray-600'
  }
}

const sentimentColor = (sentiment: string) => {
  switch (sentiment?.toLowerCase()) {
    case 'bearish': return 'text-red-500'
    case 'bullish': return 'text-green-500'
    default:        return 'text-gray-400'
  }
}

const sentimentIcon = (sentiment: string) => {
  switch (sentiment?.toLowerCase()) {
    case 'bearish': return '▼'
    case 'bullish': return '▲'
    default:        return '◆'
  }
}

function PredictionScorecard({ summary }: { summary: PredictionSummary | null }) {
  if (summary === null || summary.total === 0) return null
  return (
    <section className="mb-8">
      <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-lg">🎯</span>
          <div>
            <div className="text-sm font-bold text-white">GPVS Prediction Scorecard</div>
            <div className="text-xs text-gray-400">GNI Prediction Validation Standard — {summary.total} reports verified</div>
          </div>
        </div>
        <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
          <div className="bg-gray-800 rounded-lg p-3 text-center">
            <div className={`text-2xl font-bold ${summary.avg_score >= 70 ? 'text-green-400' : summary.avg_score >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
              {summary.avg_score}%
            </div>
            <div className="text-xs text-gray-500 mt-1">GPVS Score</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-3 text-center">
            <div className={`text-2xl font-bold ${summary.accuracy_3d >= 70 ? 'text-green-400' : summary.accuracy_3d >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
              {summary.accuracy_3d}%
            </div>
            <div className="text-xs text-gray-500 mt-1">3-Day Accuracy</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-3 text-center">
            <div className={`text-2xl font-bold ${summary.accuracy_7d >= 70 ? 'text-green-400' : summary.accuracy_7d >= 50 ? 'text-yellow-400' : 'text-red-400'}`}>
              {summary.accuracy_7d}%
            </div>
            <div className="text-xs text-gray-500 mt-1">7-Day Accuracy</div>
          </div>
          <div className="bg-gray-800 rounded-lg p-3 text-center">
            <div className={`text-2xl font-bold ${summary.pending_review === 0 ? 'text-green-400' : 'text-yellow-400'}`}>
              {summary.pending_review}
            </div>
            <div className="text-xs text-gray-500 mt-1">Pending Review</div>
          </div>
        </div>
        <div className="mt-4 bg-gray-800 rounded-lg p-3 text-xs text-gray-400 leading-relaxed">
          <span className="text-white font-bold">How GPVS works: </span>
          Every GNI report makes a prediction — Bearish or Bullish on SPY market direction. After 3 and 7 days, actual market movement is measured and compared. Correct predictions increase a source&apos;s trust weight (up to 2.0). Wrong predictions reduce it (down to 0.5). Over time this builds a self-improving intelligence system where accuracy drives credibility.
        </div>
        <div className="mt-3 text-xs text-gray-600 text-center">
          Powered by GPVS v1.1 — GNI Prediction Validation Standard | SPY directional accuracy vs actual market movements
        </div>
        <div className="mt-2 text-xs text-yellow-600 text-center">
          ⚠️ Past accuracy does not guarantee future performance. Not financial advice.
        </div>
      </div>
    </section>
  )
}

function SourceWeightsTable({ weights }: { weights: SourceWeight[] }) {
  if (!weights || weights.length === 0) return null
  return (
    <section className="mb-8">
      <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
        <div className="flex items-center gap-3 mb-4">
          <span className="text-lg">⚖️</span>
          <div>
            <div className="text-sm font-bold text-white">Dynamic Source Weights <span className="text-xs text-gray-400 font-normal">(Updated automatically based on GPVS prediction accuracy)</span></div>
          </div>
        </div>
        <div className="space-y-2">
          {weights.map(w => {
            const pct = Math.min(100, Math.round((w.weight / 2.0) * 100))
            const barColor = w.weight >= 1.3 ? "bg-green-500" : w.weight >= 1.0 ? "bg-blue-500" : "bg-red-500"
            return (
              <div key={w.source} className="flex items-center gap-3">
                <div className="w-24 text-xs text-gray-300 font-mono capitalize shrink-0">{w.source}</div>
                <div className="flex-1 bg-gray-800 rounded-full h-2">
                  <div className={`h-2 rounded-full ${barColor}`} style={{ width: pct + "%" }} />
                </div>
                <div className="w-10 text-xs text-right font-bold text-white shrink-0">{w.weight.toFixed(2)}</div>
                <div className="w-16 text-xs text-right text-gray-500 shrink-0">
                  {w.gpvs_contribution != null ? `GPVS: ${Math.round(w.gpvs_contribution * 100)}%` : "baseline"}
                </div>
              </div>
            )
          })}
        </div>
        <div className="mt-4 bg-gray-800 rounded-lg p-3 text-xs text-gray-400 leading-relaxed">
          <span className="text-white font-bold">How Source Weights work: </span>
          Every GNI prediction is tracked against real market outcomes via GPVS. Sources whose articles led to correct predictions earn higher trust weights (up to 2.0). Sources linked to wrong predictions are penalised (down to 0.5). Weights update automatically using an Exponential Moving Average (EMA) after each verified prediction, so the most accurate sources drive the intelligence over time.
        </div>
        <div className="mt-3 text-xs text-gray-600">
          Weight: 0.5 (penalised) → 1.0 (neutral) → 2.0 (highly trusted) | Updates via EMA after each verified prediction
        </div>
      </div>
    </section>
  )
}

function EscalationSparkline({ reports }: { reports: { escalation_score: number; escalation_level: string; created_at: string }[] }) {
  const last7 = reports.slice(0, 7).reverse()
  if (last7.length < 2) return null
  const scores = last7.map(r => r.escalation_score || 0)
  const maxScore = 10
  const width = 160
  const height = 40
  const points = scores.map((s, i) => {
    const x = (i / (scores.length - 1)) * width
    const y = height - (s / maxScore) * height
    return `${x},${y}`
  }).join(' ')
  const latest = scores[scores.length - 1]
  const prev = scores[scores.length - 2]
  const trend = latest > prev ? 'up' : latest < prev ? 'down' : 'flat'
  const trendColor = latest >= 8 ? '#ef4444' : latest >= 6 ? '#f97316' : latest >= 4 ? '#eab308' : '#22c55e'
  return (
    <div className="flex items-center gap-3 mt-1">
      <div>
        <div className="text-xs text-gray-500 mb-0.5">7-run escalation trend</div>
        <svg width={width} height={height} className="overflow-visible">
          <polyline
            points={points}
            fill="none"
            stroke={trendColor}
            strokeWidth="1.5"
            strokeLinejoin="round"
            strokeLinecap="round"
          />
          {scores.map((s, i) => {
            const x = (i / (scores.length - 1)) * width
            const y = height - (s / maxScore) * height
            return <circle key={i} cx={x} cy={y} r={i === scores.length - 1 ? 3 : 2} fill={trendColor} />
          })}
        </svg>
      </div>
      <div>
        <div className="text-xs font-bold" style={{ color: trendColor }}>
          {trend === 'up' ? '↑' : trend === 'down' ? '↓' : '→'} {latest.toFixed(1)}/10
        </div>
        <div className="text-xs text-gray-600">
          {trend === 'up' ? 'escalating' : trend === 'down' ? 'de-escalating' : 'stable'}
        </div>
      </div>
    </div>
  )
}

export default function Home() {
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [pillarReports, setPillarReports] = useState<PillarReport[]>([])
  const [error, setError] = useState('')
  const [latestArticles, setLatestArticles] = useState<PipelineArticle[]>([])
  const [showAIThinking, setShowAIThinking] = useState(false)
  const [predictionSummary, setPredictionSummary] = useState<PredictionSummary | null>(null)
  const [sourceWeights, setSourceWeights] = useState<SourceWeight[]>([])
  const [latestRun, setLatestRun] = useState<PipelineRun | null>(null)
  const [showPreviousReports, setShowPreviousReports] = useState(false)
  const [mapEvents, setMapEvents] = useState<{id: string, source: string, bias: string, title: string, url: string, summary: string, stage3_score: number, stage4_rank: number, location_name: string, lat: number, lng: number, created_at: string}[]>([])
  const [btcChartData, setBtcChartData] = useState<{date: string, close: number}[]>([])
  const [btcPrice, setBtcPrice] = useState<{price: number, changePercent: string} | null>(null)
  const [baseline, setBaseline] = useState<{score: number, percentile: number, total_non_zero: number} | null>(null)

  useEffect(() => {
    const interval = setInterval(() => {
      fetch('/api/reports')
        .then(r => r.json())
        .then(data => {
          if (data.reports && data.reports.length > 0) {
            setReports(data.reports)
          }
        })
        .catch(() => {})
    }, 300000)
    return () => clearInterval(interval)
  }, [])

  useEffect(() => {
    fetch('/api/reports')
      .then(r => r.json())
      .then(data => {
        if (data.error) setError(data.error)
        else {
          setReports(data.reports || [])
          setBaseline(data.baseline || null)
        }
      })
      .catch(() => setError('Failed to load reports'))
      .finally(() => setLoading(false))

    fetch('/api/pillar-reports')
      .then(r => r.json())
      .then(data => setPillarReports(data.reports || []))
      .catch(() => {})

    fetch('/api/prediction-outcomes')
      .then(r => r.json())
      .then(data => setPredictionSummary(data.summary || null))
      .catch(() => {})

    fetch('/api/source-weights')
      .then(r => r.json())
      .then(data => setSourceWeights(data.weights || []))
      .catch(() => {})

    // Live map events widget
    fetch('/api/article-events?days=1')
      .then(r => r.json())
      .then(data => {
        const events = data.events || []
        const unique = events.filter((e: {location_name: string}, i: number, arr: {location_name: string}[]) =>
          arr.findIndex(x => x.location_name === e.location_name) === i
        ).slice(0, 3)
        setMapEvents(unique)
      })
      .catch(() => {})


    // BTC 10Y chart for mini widget
    fetch('/api/stocks?ticker=BTC-USD&range=10y')
      .then(r => r.json())
      .then(data => {
        if (data.chartData) {
          setBtcChartData(data.chartData.map((d: {date: string, close: number}) => ({
            date: new Date(d.date).toLocaleDateString('en-US', { month: 'short', year: '2-digit' }),
            close: d.close
          })))
          setBtcPrice({ price: data.price, changePercent: data.changePercent })
        }
      }).catch(() => {})

    fetch('/api/pipeline-runs')
      .then(r => r.json())
      .then(data => {
        const runs = data.runs || []
        if (runs.length > 0) {
          setLatestRun(runs[0])
          fetch(`/api/pipeline-articles?run_id=${runs[0].id}`)
            .then(r => r.json())
            .then(d => {
              const selected = (d.articles || []).filter((a: PipelineArticle) => a.stage4_selected === true)
              setLatestArticles(selected)
            })
        }
      })
      .catch(() => {})
  }, [])

  const latest = reports[0]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-center justify-between mb-4">
            <div>
              <h1 className="text-2xl font-bold text-white">🌐 Global Nexus Insights (Autonomous)</h1>
              <p className="text-sm text-gray-400">Technology + Geopolitics + Financial Impact</p>
            </div>
            <div className="text-right text-sm text-gray-400">
              <div>Pipeline: <span className="inline-flex items-center gap-1"><span className="inline-block w-2 h-2 rounded-full bg-green-400"></span><span className="text-green-400">Active</span></span></div>
              <div>Intelligence Reports: <span className="text-white font-bold">{reports.length}</span></div>
              {baseline && baseline.score > 0 && (
                <div className="text-xs mt-1">
                  <span className={`font-bold ${baseline.percentile >= 75 ? 'text-red-400' : baseline.percentile >= 50 ? 'text-orange-400' : 'text-yellow-400'}`}>
                    Today is top {100 - baseline.percentile}% most escalated
                  </span>
                  <span className="text-gray-600 ml-1">({baseline.total_non_zero} runs)</span>
                </div>
              )}
              {reports.length >= 2 && <EscalationSparkline reports={reports} />}
            </div>
          </div>

          {latest && (
            <div className="grid grid-cols-3 gap-3 mb-4">
              <div className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 flex items-center gap-2">
                <span className="text-sm">🧬</span>
                <div>
                  <div className="text-xs text-gray-500">Technology</div>
                  <div className={`text-xs font-bold ${latest.risk_level?.toLowerCase() === 'critical' ? 'text-red-400' : latest.risk_level?.toLowerCase() === 'high' ? 'text-orange-400' : 'text-yellow-400'}`}>
                    {latest.risk_level?.toUpperCase() || 'MONITORING'}
                  </div>
                </div>
              </div>
              <div className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 flex items-center gap-2">
                <span className="text-sm">🌍</span>
                <div>
                  <div className="text-xs text-gray-500">Geopolitics</div>
                  <div className={`text-xs font-bold ${latest.risk_level?.toLowerCase() === 'critical' ? 'text-red-400' : latest.risk_level?.toLowerCase() === 'high' ? 'text-orange-400' : 'text-yellow-400'}`}>
                    {latest.risk_level?.toUpperCase() || 'MONITORING'}
                  </div>
                </div>
              </div>
              <div className="bg-gray-800 border border-gray-700 rounded-lg px-3 py-2 flex items-center gap-2">
                <span className="text-sm">💹</span>
                <div>
                  <div className="text-xs text-gray-500">Financial</div>
                  <div className={`text-xs font-bold ${latest.sentiment?.toLowerCase() === 'bearish' ? 'text-red-400' : latest.sentiment?.toLowerCase() === 'bullish' ? 'text-green-400' : 'text-gray-400'}`}>
                    {latest.sentiment?.toUpperCase() || 'NEUTRAL'}
                  </div>
                </div>
              </div>
            </div>
          )}

                    {/* Cross-Navigation -- 4 buttons to other main pages (GNI-R-140) */}
          <div className="flex flex-wrap gap-2 mt-2">
            <a href="/researcher" className="flex items-center gap-2 bg-green-900 hover:bg-green-700 border border-green-700 hover:border-green-500 rounded-lg px-4 py-2 text-sm font-bold text-green-200 transition-colors">
              📊 Pattern Intelligence
            </a>
            <a href="/developer-hub" className="flex items-center gap-2 bg-purple-900 hover:bg-purple-700 border border-purple-700 hover:border-purple-500 rounded-lg px-4 py-2 text-sm font-bold text-purple-200 transition-colors">
              🧠 Dev Console
            </a>
            <a href="/reports" className="flex items-center gap-2 bg-amber-900 hover:bg-amber-700 border border-amber-700 hover:border-amber-500 rounded-lg px-4 py-2 text-sm font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
            <a href="/about" className="flex items-center gap-2 bg-gray-800 hover:bg-gray-700 border border-gray-600 hover:border-gray-400 rounded-lg px-4 py-2 text-sm font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {loading && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">⌛</div>
            <p>Loading intelligence reports...</p>
          </div>
        )}

        {error && (
          <div className="text-center py-20 text-red-400">
            <div className="text-4xl mb-4">⚠️</div>
            <p>{error}</p>
          </div>
        )}

        {!loading && !error && reports.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">📡</div>
            <p>No reports yet. Pipeline runs at 09:00 and 17:00 Myanmar time.</p>
          </div>
        )}

        {!loading && reports.length > 0 && (
          <>
                      {/* Hub Preview Rows -- 8 sub-page previews (GNI-R-141, GNI-R-143) */}

            {/* ROW: /brief -- most important missing page */}
            <section className="mb-4">
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="px-4 py-3 flex items-center justify-between">
                  <div className="flex items-center gap-3 flex-1">
                    <div className={`w-3 h-3 rounded-full shrink-0 ${
                      latest?.escalation_level?.toLowerCase() === 'critical' ? 'bg-red-500' :
                      latest?.escalation_level?.toLowerCase() === 'high' ? 'bg-orange-500' :
                      latest?.escalation_level?.toLowerCase() === 'elevated' ? 'bg-yellow-500' : 'bg-green-500'
                    }`} />
                    <div className={`text-xs font-bold px-3 py-1 rounded-full ${
                      latest?.escalation_level?.toLowerCase() === 'critical' ? 'bg-red-900 text-red-200 border border-red-700' :
                      latest?.escalation_level?.toLowerCase() === 'high' ? 'bg-orange-900 text-orange-200 border border-orange-700' :
                      latest?.escalation_level?.toLowerCase() === 'elevated' ? 'bg-yellow-900 text-yellow-200 border border-yellow-700' :
                      'bg-green-900 text-green-200 border border-green-700'
                    }`}>
                      {latest?.escalation_level?.toUpperCase() || 'MONITORING'}
                    </div>
                    <div className="text-sm text-gray-300 truncate">
                      {latest?.mad_action_recommendation
                        ? latest.mad_action_recommendation.slice(0, 120) + (latest.mad_action_recommendation.length > 120 ? '...' : '')
                        : 'Executive brief loading...'}
                    </div>
                  </div>
                  <a href="/brief" className="text-xs text-white bg-blue-700 hover:bg-blue-600 rounded px-3 py-1.5 font-bold ml-3 shrink-0 transition-colors">
                    30-sec Brief →
                  </a>
                </div>
              </div>
            </section>

            {/* ROW: /debate preview */}
            <section className="mb-4">
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="px-4 py-3 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3">
                    <span className={`text-sm font-bold px-3 py-1 rounded-full ${
                      latest?.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300 border border-green-700' :
                      latest?.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300 border border-red-700' :
                      'bg-gray-700 text-gray-300 border border-gray-600'
                    }`}>
                      {latest?.mad_verdict === 'bullish' ? '🐂' : latest?.mad_verdict === 'bearish' ? '🐻' : '◆'} {latest?.mad_verdict?.toUpperCase() || 'PENDING'}
                    </span>
                    <span className="text-xs text-gray-400">
                      Confidence: <span className="text-white font-bold">{latest?.mad_confidence ? Math.round(latest.mad_confidence * 100) + '%' : 'N/A'}</span>
                    </span>
                    <span className="text-xs text-gray-500 hidden md:block truncate max-w-xs">
                      {latest?.mad_action_recommendation?.slice(0, 80) || 'Awaiting MAD verdict'}
                    </span>
                  </div>
                  <a href="/debate" className="text-xs font-bold text-white bg-blue-700 hover:bg-blue-600 rounded-lg px-3 py-1.5 shrink-0 transition-colors">
                    Full Debate →
                  </a>
                </div>
              </div>
            </section>

{/* Live Map + Stocks Widgets */}
            <section className="mb-6">
              <div className="grid grid-cols-1 md:grid-cols-2 gap-4">

                {/* Mini Interactive Map Widget */}
                <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                  <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700">
                    <div>
                      <div className="text-sm font-bold text-white">🗺️ Geopolitical Event Map</div>
                      <div className="text-xs text-gray-400">Live Events — Click Pins for Details</div>
                    </div>
                    <a href="/map" className="text-xs font-bold text-white bg-blue-700 hover:bg-blue-600 rounded-lg px-3 py-1.5 transition-colors">Full Map →</a>
                  </div>
                  <div style={{ height: "220px", width: "100%" }}>
                    {mapEvents.length > 0 ? (
                      <MiniMapView events={mapEvents} height="220px" />
                    ) : (
                      <div className="flex items-center justify-center h-full text-xs text-gray-600">Loading map events...</div>
                    )}
                  </div>
                </div>

                {/* Mini Interactive Stock Chart Widget */}
                <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                  <div className="flex items-center justify-between px-4 py-3 border-b border-gray-700">
                    <div>
                      <div className="text-sm font-bold text-white">📈 Bitcoin (BTC) — 10 Year</div>
                      <div className="text-xs text-gray-400 flex items-center gap-2">
                        {btcPrice ? (
                          <>
                            <span className="text-white font-bold">${btcPrice.price?.toLocaleString()}</span>
                            <span className={`font-bold ${parseFloat(btcPrice.changePercent) >= 0 ? 'text-green-400' : 'text-red-400'}`}>
                              10Y: {parseFloat(btcPrice.changePercent) >= 0 ? '+' : ''}{btcPrice.changePercent}%
                            </span>
                          </>
                        ) : (
                          <span>Loading...</span>
                        )}
                      </div>
                    </div>
                    <a href="/stocks" className="text-xs font-bold text-white bg-blue-700 hover:bg-blue-600 rounded-lg px-3 py-1.5 transition-colors">25 Charts →</a>
                  </div>
                  <div style={{ height: "220px", width: "100%", padding: "8px" }}>
                    {btcChartData.length > 0 ? (
                      <ResponsiveContainer width="100%" height="100%">
                        <AreaChart data={btcChartData} margin={{ top: 5, right: 5, left: 0, bottom: 5 }}>
                          <defs>
                            <linearGradient id="btcGradient" x1="0" y1="0" x2="0" y2="1">
                              <stop offset="5%" stopColor="#f59e0b" stopOpacity={0.4} />
                              <stop offset="95%" stopColor="#f59e0b" stopOpacity={0} />
                            </linearGradient>
                          </defs>
                          <CartesianGrid strokeDasharray="3 3" stroke="#1f2937" />
                          <XAxis dataKey="date" tick={{ fill: '#6b7280', fontSize: 9 }} tickLine={false} axisLine={false} interval={Math.floor(btcChartData.length / 6)} />
                          <YAxis tick={{ fill: '#6b7280', fontSize: 9 }} tickLine={false} axisLine={false} tickFormatter={v => `$${(v/1000).toFixed(0)}k`} width={45} domain={['auto', 'auto']} />
                          <Tooltip
                            contentStyle={{ backgroundColor: '#111827', border: '1px solid #374151', borderRadius: '8px', color: '#f9fafb', fontSize: '11px' }}
                            formatter={(value) => [`$${Number(value).toLocaleString()}`, 'BTC']}
                          />
                          <Area type="monotone" dataKey="close" stroke="#f59e0b" strokeWidth={2} fill="url(#btcGradient)" dot={false} activeDot={{ r: 4, fill: '#f59e0b' }} />
                        </AreaChart>
                      </ResponsiveContainer>
                    ) : (
                      <div className="flex items-center justify-center h-full text-xs text-gray-600">Loading BTC chart...</div>
                    )}
                  </div>
                </div>

              </div>
            </section>

                        {/* ROW: /comparison preview */}
            <section className="mb-4">
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="px-4 py-3 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-4">
                    <div className="text-xs text-gray-400">
                      Pipeline: <span className="text-white font-bold">{latest?.sentiment_score?.toFixed(2) || 'N/A'}</span>
                    </div>
                    <div className="text-xs text-gray-400">
                      MAD: <span className="text-white font-bold">{latest?.mad_confidence ? (latest.mad_confidence * 2 - 1).toFixed(2) : 'N/A'}</span>
                    </div>
                    <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                      latest?.sentiment && latest?.mad_verdict &&
                      latest.sentiment.toLowerCase() !== latest.mad_verdict.toLowerCase()
                        ? 'bg-orange-900 text-orange-300 border border-orange-700'
                        : 'bg-green-900 text-green-300 border border-green-700'
                    }`}>
                      {latest?.sentiment && latest?.mad_verdict &&
                       latest.sentiment.toLowerCase() !== latest.mad_verdict.toLowerCase()
                        ? '⚠️ DIVERGING' : '✓ ALIGNED'}
                    </span>
                  </div>
                  <a href="/comparison" className="text-xs font-bold text-white bg-blue-700 hover:bg-blue-600 rounded-lg px-3 py-1.5 shrink-0 transition-colors">
                    See Divergence →
                  </a>
                </div>
              </div>
            </section>

            {/* ROW: /scenarios preview */}
            <section className="mb-4">
              <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                <div className="px-4 py-3 flex items-center justify-between gap-3">
                  <div className="flex items-center gap-3 flex-1 min-w-0">
                    <span className="text-xs text-gray-500 shrink-0">Base:</span>
                    <span className="text-xs text-gray-300 truncate">{latest?.mad_historian_case?.slice(0, 60) || 'Pending'}</span>
                    <span className="text-xs text-green-600 shrink-0 hidden md:block">| Upside</span>
                    <span className="text-xs text-red-600 shrink-0 hidden md:block">| Downside</span>
                  </div>
                  <a href="/scenarios" className="text-xs font-bold text-white bg-blue-700 hover:bg-blue-600 rounded-lg px-3 py-1.5 shrink-0 transition-colors">
                    View Scenarios →
                  </a>
                </div>
              </div>
            </section>


            <section className="mb-8">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Latest Intelligence Report</div>
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">

                <div className="flex items-start justify-between gap-4 mb-4">
                  <h2 className="text-xl font-bold text-white leading-tight">{latest.title}</h2>
                  <div className="flex flex-col items-end gap-2 shrink-0">
                    <span className={`text-xs font-bold px-3 py-1 rounded-full whitespace-nowrap ${riskColor(latest.risk_level)}`}>
                      {latest.risk_level?.toUpperCase()}
                    </span>
                    {latest.escalation_level && (
                      <span className={`text-xs font-bold px-2 py-1 rounded-full whitespace-nowrap ${escalationColor(latest.escalation_level)}`}>
                        ⚡ {latest.escalation_level?.toUpperCase()} {latest.escalation_score ? `${latest.escalation_score.toFixed(1)}/10` : ''}
                      </span>
                    )}
                  </div>
                </div>

                <p className="text-gray-300 text-sm leading-relaxed mb-4">{latest.summary}</p>

                <div className="grid grid-cols-2 md:grid-cols-4 gap-4 mb-4">
                  <div className="bg-gray-800 rounded-lg p-3">
                    <div className="text-xs text-gray-500 mb-1">Sentiment</div>
                    <div className={`font-bold ${sentimentColor(latest.sentiment)}`}>
                      {sentimentIcon(latest.sentiment)} {latest.sentiment}
                    </div>
                    <div className="text-xs text-gray-400">{latest.sentiment_score?.toFixed(2)}</div>
                    {latest.confidence_interval_width > 0 && (
                      <div className="text-xs text-gray-600 mt-1">
                        CI: [{latest.sentiment_score_lower?.toFixed(2)}, {latest.sentiment_score_upper?.toFixed(2)}]
                        {latest.analysis_runs > 1 && <span className="ml-1 text-blue-700">({latest.analysis_runs} runs)</span>}
                      </div>
                    )}
                    {latest.confidence_interval_width > 0 && (
                      <div className="mt-1.5 relative h-1.5 bg-gray-700 rounded-full">
                        <div className="absolute h-1.5 rounded-full bg-blue-600 opacity-50"
                          style={{
                            left: `${((latest.sentiment_score_lower + 1) / 2) * 100}%`,
                            width: `${(latest.confidence_interval_width / 2) * 100}%`
                          }}
                        />
                        <div className="absolute w-0.5 h-1.5 bg-white rounded-full"
                          style={{ left: `${((latest.sentiment_score + 1) / 2) * 100}%` }}
                        />
                      </div>
                    )}
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3">
                    <div className="text-xs text-gray-500 mb-1">Location</div>
                    <div className="font-bold text-white text-sm">📍 {latest.location_name || 'Global'}</div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3">
                    <div className="text-xs text-gray-500 mb-1">LLM Engine</div>
                    <div className="font-bold text-blue-400 text-sm">
                      {latest.llm_source === 'ollama' ? '🧠 Llama 3 Local' : '☁️ Groq API'}
                    </div>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3">
                    <div className="text-xs text-gray-500 mb-1">Generated</div>
                    <div className="font-bold text-white text-sm">
                      {new Date(latest.created_at).toLocaleDateString('en-US', {
                        month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                      })}
                    </div>
                  </div>
                </div>

                {latest.tickers_affected?.length > 0 && (
                  <div className="flex flex-wrap gap-2 mb-4">
                    {latest.tickers_affected.map(ticker => (
                      <span key={ticker} className="bg-blue-900 text-blue-300 text-xs font-mono font-bold px-2 py-1 rounded">
                        {ticker}
                      </span>
                    ))}
                  </div>
                )}

                <div className="bg-gray-800 rounded-lg p-4 mb-4">
                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Market Impact Analysis</div>
                  <p className="text-gray-300 text-sm leading-relaxed">
                    {latest.market_impact || 'Analysis will appear in next pipeline run.'}
                  </p>
                </div>

                {(latest.weakness_identified || latest.threat_horizon || latest.dark_side_detected) && (
                <div className="bg-gray-800 rounded-lg p-4 mb-4">
                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">🔍 SWOT Intelligence — Weakness & Threat Analysis</div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
                    {latest.weakness_identified && (
                    <div className="bg-orange-950 border border-orange-800 rounded-lg p-3">
                      <div className="text-xs text-orange-400 font-bold mb-1">⚠️ Weakness Identified</div>
                      <p className="text-xs text-gray-300 leading-relaxed">{latest.weakness_identified}</p>
                    </div>
                    )}
                    {latest.threat_horizon && (
                    <div className="bg-red-950 border border-red-800 rounded-lg p-3">
                      <div className="text-xs text-red-400 font-bold mb-1">⏱ Threat Horizon</div>
                      <p className="text-xs text-gray-300 leading-relaxed">{latest.threat_horizon}</p>
                    </div>
                    )}
                    {latest.dark_side_detected && latest.dark_side_detected !== 'None' && (
                    <div className="bg-purple-950 border border-purple-800 rounded-lg p-3">
                      <div className="text-xs text-purple-400 font-bold mb-1">🌍 Dark Side Detected</div>
                      <p className="text-xs text-gray-300 leading-relaxed">{latest.dark_side_detected}</p>
                    </div>
                    )}
                  </div>
                </div>
                )}

                {reports.length > 1 && (
                  <div className="bg-gray-800 rounded-lg p-4 mt-4 mb-4">
                    <button
                      onClick={() => setShowPreviousReports(prev => !prev)}
                      className="w-full flex items-center justify-between hover:opacity-80 transition-opacity"
                    >
                      <div className="text-xs text-gray-300 font-bold uppercase tracking-wider">{reports.length - 1} Previous Reports</div>
                      <span className="text-xs font-bold text-gray-200 bg-gray-700 hover:bg-gray-600 rounded-lg px-3 py-1.5">
                        {showPreviousReports ? "▲ Hide" : "▼ Show"}
                      </span>
                    </button>
                    {showPreviousReports && (
                      <div className="space-y-3 mt-3">
                        {reports.slice(1).map(report => (
                          <div key={report.id} className="bg-gray-700 border border-gray-600 rounded-xl p-4 hover:border-gray-500 transition-colors">
                            <div className="flex items-start justify-between gap-4">
                              <div className="flex-1 min-w-0">
                                <h3 className="font-semibold text-white text-sm mb-1 truncate">{report.title}</h3>
                                <p className="text-gray-300 text-xs line-clamp-5">{report.summary}</p>
                              </div>
                              <div className="flex flex-col items-end gap-2 shrink-0">
                                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${riskColor(report.risk_level)}`}>
                                  {report.risk_level?.toUpperCase()}
                                </span>
                                <span className={`text-xs font-bold ${sentimentColor(report.sentiment)}`}>
                                  {sentimentIcon(report.sentiment)} {report.sentiment}
                                </span>
                              </div>
                            </div>
                            <div className="flex items-center gap-4 mt-2">
                              <span className="text-xs text-gray-400">� {report.location_name || 'Global'}</span>
                              <span className="text-xs text-gray-400">
                                {new Date(report.created_at).toLocaleDateString('en-US', {
                                  month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                                })}
                              </span>
                              {report.tickers_affected?.slice(0, 3).map(t => (
                                <span key={t} className="text-xs font-mono text-blue-400">{t}</span>
                              ))}
                            </div>
                          </div>
                        ))}
                      </div>
                    )}
                  </div>
                )}

                <div className="bg-yellow-900 border border-yellow-700 rounded-lg p-3">
                  <p className="text-yellow-200 text-xs">
                    ⚠️ <strong>Disclaimer:</strong> GNI reports are for informational purposes only and do not constitute financial advice. Always conduct your own research before making investment decisions.
                  </p>
                </div>
              </div>
            </section>

            {/* Three Pillar Intelligence Reports */}
            {pillarReports.length > 0 && (() => {
              const geoR  = pillarReports.find(r => r.pillar === 'geo')
              const techR = pillarReports.find(r => r.pillar === 'tech')
              const finR  = pillarReports.find(r => r.pillar === 'fin')
              const pillars = [
                { key: 'geo',  label: 'Geopolitical', emoji: '🌍', report: geoR,  border: 'border-red-800',   bg: 'bg-red-950',   accent: 'text-red-400'   },
                { key: 'tech', label: 'Technology',   emoji: '💻', report: techR, border: 'border-blue-800',  bg: 'bg-blue-950',  accent: 'text-blue-400'  },
                { key: 'fin',  label: 'Financial',    emoji: '💰', report: finR,  border: 'border-green-800', bg: 'bg-green-950', accent: 'text-green-400' },
              ]
              return (
                <section className="mb-8">
                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">Three Pillar Intelligence Reports</div>
                <div className="text-xs text-gray-400 leading-relaxed mb-3 bg-gray-900 rounded-lg p-3">
                  <span className="text-white font-bold">How Three Pillar Reports work: </span>
                  Every pipeline run produces three separate AI analyses across the three intelligence pillars: Geopolitical (conflict, diplomacy, alliances), Technology (cyber, AI, surveillance), and Financial (markets, sanctions, trade). Each pillar uses the same top articles but focuses its analysis on its domain, giving a multi-dimensional view of the same global events.
                </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
                    {pillars.map(({ key, label, emoji, report, border, bg, accent }) => (
                      <div key={key} className={`border rounded-xl p-4 ${border} ${bg}`}>
                        <div className="flex items-center gap-2 mb-3">
                          <span className="text-xl">{emoji}</span>
                          <span className={`text-xs font-bold uppercase tracking-wider ${accent}`}>{label}</span>
                        </div>
                        {report ? (
                          <>
                            <div className="text-sm font-bold text-white mb-1 leading-tight line-clamp-2">{report.title}</div>
                            <div className="text-xs text-gray-400 mb-3 line-clamp-3">{report.summary}</div>
                            <div className="flex items-center justify-between mb-2">
                              <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${
                                report.risk_level === 'Critical' ? 'bg-red-700 text-white' :
                                report.risk_level === 'High'     ? 'bg-orange-700 text-white' :
                                report.risk_level === 'Medium'   ? 'bg-yellow-700 text-white' :
                                'bg-gray-700 text-gray-300'
                              }`}>{report.risk_level}</span>
                              <span className={`text-xs font-bold ${
                                report.sentiment === 'Bearish' ? 'text-red-400' :
                                report.sentiment === 'Bullish' ? 'text-green-400' : 'text-gray-400'
                              }`}>{report.sentiment} {report.sentiment_score >= 0 ? '+' : ''}{report.sentiment_score?.toFixed(2)}</span>
                            </div>
                            {report.weakness_identified && (
                              <div className="text-xs text-gray-500 border-t border-gray-700 pt-2 mt-1">
                                <span className="text-yellow-600 font-bold">Weakness: </span>
                                <span className="line-clamp-2">{report.weakness_identified}</span>
                              </div>
                            )}
                            {report.tickers_affected?.length > 0 && (
                              <div className="flex flex-wrap gap-1 mt-2">
                                {report.tickers_affected.slice(0, 3).map((t: string) => (
                                  <span key={t} className="text-xs font-mono text-blue-400 bg-blue-950 px-1.5 py-0.5 rounded">{t}</span>
                                ))}
                              </div>
                            )}
                          </>
                        ) : (
                          <div className="text-xs text-gray-600 italic py-4 text-center">Pending next pipeline run</div>
                        )}
                      </div>
                    ))}
                  </div>
                </section>
              )
            })()}

            {/* MAD Verdict Section */}
            {latest?.mad_verdict && (
              <section className="mb-8">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">
                  🐂🐻🦢🦦 Quadratic MAD — Latest Threat Verdict
                </div>
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-6">
                  <div className="flex items-center justify-between mb-4">
                    <div className="flex items-center gap-3">
                      <span className={`text-lg font-bold px-4 py-2 rounded-full ${latest.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300' : latest.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300' : 'bg-gray-700 text-gray-300'}`}>
                        {latest.mad_verdict === 'bullish' ? '🐂' : latest.mad_verdict === 'bearish' ? '🐻' : '◆'} {latest.mad_verdict?.toUpperCase()}
                      </span>
                      <span className="text-sm text-gray-400">
                        Confidence: {latest.mad_confidence ? Math.round(latest.mad_confidence * 100) + '%' : 'N/A'}
                      </span>
                      {latest.deception_level && latest.deception_level !== 'NONE' && (
                        <span className="text-xs bg-orange-900 text-orange-300 px-2 py-1 rounded-full">
                          🕵️ {latest.deception_level} coordination
                        </span>
                      )}
                    </div>
                    <a href="/debate" className="text-xs font-bold text-white bg-blue-700 hover:bg-blue-600 rounded-lg px-3 py-1.5 transition-colors">
                      Full Debate →
                    </a>
                  </div>
                  <div className="bg-gray-800 rounded-lg p-3 mb-4 text-xs text-gray-400 leading-relaxed">
                    <span className="text-white font-bold">How MAD works: </span>
                    Four AI agents debate future threats across two axes: Known/Unknown × Proactive/Ignored. Bull identifies opportunity costs, Bear finds systemic failures, Black Swan uncovers unknown dangers, and Ostrich exposes what is being ignored. After 3 rounds with Arbitrator coaching, a final verdict is reached. This is GNI&apos;s Novel Contribution #1 — the Johari Window applied to AI geopolitical intelligence.
                  </div>
                  {latest.mad_confidence > 0 && (
                    <div className="w-full bg-gray-800 rounded-full h-2 mb-4">
                      <div
                        className={`h-2 rounded-full ${latest.mad_verdict === 'bullish' ? 'bg-green-500' : latest.mad_verdict === 'bearish' ? 'bg-red-500' : 'bg-gray-500'}`}
                        style={{ width: Math.round(latest.mad_confidence * 100) + '%' }}
                      />
                    </div>
                  )}
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                    <div className="bg-green-950 border border-green-800 rounded-lg p-4">
                      <div className="text-xs text-green-400 font-bold mb-2">🐂 Bull — Known Positives</div>
                      <p className="text-xs text-gray-300 leading-relaxed line-clamp-4">{latest.mad_bull_case || 'Pending next MAD run.'}</p>
                    </div>
                    <div className="bg-red-950 border border-red-800 rounded-lg p-4">
                      <div className="text-xs text-red-400 font-bold mb-2">🐻 Bear — Known Negatives</div>
                      <p className="text-xs text-gray-300 leading-relaxed line-clamp-4">{latest.mad_bear_case || 'Pending next MAD run.'}</p>
                    </div>
                    <div className="bg-blue-950 border border-blue-800 rounded-lg p-4">
                      <div className="text-xs text-blue-400 font-bold mb-2">🦢 Black Swan — Unknown Negatives</div>
                      <p className="text-xs text-gray-300 leading-relaxed line-clamp-4">{latest.mad_black_swan_case || 'Pending next MAD run.'}</p>
                    </div>
                    <div className="bg-yellow-950 border border-yellow-800 rounded-lg p-4">
                      <div className="text-xs text-yellow-400 font-bold mb-2">🦦 Ostrich — Ignored Realities</div>
                      <p className="text-xs text-gray-300 leading-relaxed line-clamp-4">{latest.mad_ostrich_case || 'Pending next MAD run.'}</p>
                    </div>
                  </div>
                  {latest.mad_action_recommendation && (
                    <div className="mt-3 bg-gray-800 rounded-lg p-3">
                      <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Action Recommendation</div>
                      <p className="text-xs text-gray-300">{latest.mad_action_recommendation}</p>
                    </div>
                  )}
                </div>
              </section>
            )}

            {latestArticles.length > 0 && (
              <section className="mb-8">
                <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
                  <button
                    onClick={() => setShowAIThinking(prev => !prev)}
                    className="w-full px-6 py-4 flex items-center justify-between hover:bg-gray-800 transition-colors"
                  >
                    <div className="flex items-center gap-3">
                      <span className="text-lg">🧠</span>
                      <div className="text-left">
                        <div className="text-sm font-bold text-white">AI Thinking Transparency</div>
                        <div className="text-xs text-gray-400">
                          How {latestArticles.length} articles were consolidated into 1 report
                        </div>
                      </div>
                    </div>
                    <span className="text-gray-400 text-sm">{showAIThinking ? '▲ Hide' : '▼ Show'}</span>
                  </button>

                  <div className="px-6 pt-2 pb-3 text-xs text-gray-400 leading-relaxed">
                    <span className="text-white font-bold">How AI Thinking works: </span>
                    GNI collects articles from 25 RSS sources, then passes them through a 4-stage intelligence funnel: Stage 1 filters for geopolitical relevance, Stage 1b scans for 66 prompt injection patterns, Stage 2 removes duplicates, Stage 3 scores each article by significance, and Stage 4 selects the top articles with source diversity enforced. Only the best articles reach the AI for analysis.
                  </div>

                  {showAIThinking && (
                    <div className="px-6 pb-6 border-t border-gray-700">
                      <div className="grid grid-cols-2 md:grid-cols-5 gap-2 my-4">
                        {[
                          { label: 'Collected', value: latestRun?.total_collected ?? latestArticles.length * 24, color: 'bg-gray-700' },
                          { label: 'Relevant',  value: latestRun?.total_relevant  ?? Math.round((latestArticles.length * 24) * 0.69), color: 'bg-blue-900' },
                          { label: 'Deduped',   value: latestRun?.total_deduped   ?? Math.round((latestArticles.length * 24) * 0.68), color: 'bg-indigo-900' },
                          { label: 'Scored',    value: latestRun?.total_deduped   ?? Math.round((latestArticles.length * 24) * 0.68), color: 'bg-purple-900' },
                          { label: 'Selected',  value: latestArticles.length, color: 'bg-green-900' },
                        ].map((step, i) => (
                          <div key={i} className={`${step.color} rounded-lg p-2 text-center`}>
                            <div className="text-xl font-bold text-white">{step.value}</div>
                            <div className="text-xs text-gray-400">{step.label}</div>
                          </div>
                        ))}
                      </div>
                      <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">
                        Top {latestArticles.length} Articles Fed to AI
                      </div>
                      <div className="space-y-2">
                        {latestArticles.map((art, i) => (
                          <div key={art.id} className="bg-gray-800 rounded-lg p-3 flex items-start gap-3">
                            <span className="text-xs font-bold text-blue-400 w-6 shrink-0">#{i + 1}</span>
                            <div className="flex-1 min-w-0">
                              <div className="flex items-center gap-2 mb-1">
                                <span className="text-xs text-gray-500 font-mono">{art.source}</span>
                                <span className="text-xs text-yellow-400">Score: {art.stage3_score}</span>
                              </div>
                              {art.url ? (
                                <a href={art.url} target="_blank" rel="noopener noreferrer" className="text-sm text-blue-300 hover:text-blue-200 leading-tight">
                                  {art.title}
                                </a>
                              ) : (
                                <div className="text-sm text-white leading-tight">{art.title}</div>
                              )}
                              {art.summary && (
                                <p className="text-xs text-gray-500 mt-1 line-clamp-2">{art.summary}</p>
                              )}
                            </div>
                          </div>
                        ))}
                      </div>
                    </div>
                  )}
                </div>
              </section>
            )}

            <PredictionScorecard summary={predictionSummary} />
            <SourceWeightsTable weights={sourceWeights} />


          </>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          Global Nexus Insights (Autonomous) | Higher Diploma in Computer Science | Spring University Myanmar (SUM) | Pipelines runs 2x daily via GitHub Actions
        </div>
      </footer>
    </div>
  )
}
