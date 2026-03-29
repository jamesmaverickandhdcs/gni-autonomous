'use client'
const GNI_KEY = process.env.NEXT_PUBLIC_GNI_API_KEY || ''

import { useEffect, useState } from 'react'

interface PipelineRun {
  id: string
  run_at: string
  total_collected: number
  total_after_relevance: number
  total_after_funnel: number
  llm_source: string
  status: string
  duration_seconds: number
  report_id: string
}

interface Report {
  id: string
  title: string
  summary: string
  sentiment: string
  sentiment_score: number
  risk_level: string
  location_name: string
  tickers_affected: string[]
  market_impact: string
  llm_source: string
  created_at: string
  quality_score: number
  quality_breakdown: QualityBreakdown
  mad_verdict: string
  mad_confidence: number
  escalation_score: number
  escalation_level: string
  weakness_identified: string
  threat_horizon: string
  dark_side_detected: string
  mad_blind_spot: string
  mad_action_recommendation: string
  short_focus_threats: string
  long_shoot_threats: string
}

interface Article {
  id: string
  source: string
  title: string
  url: string
  summary: string
  stage3_score: number
  stage4_rank: number
  stage4_selected: boolean
}

interface PredictionOutcome {
  accuracy_score: number
  spy_change_3d: number
  spy_change_7d: number
  spy_change_30d: number
  direction_correct_3d: boolean
  direction_correct_7d: boolean
  direction_correct_30d: boolean
  black_swan_flag: boolean
  human_review_needed: boolean
  measured_at: string
}

interface QualityBreakdown {
  specificity: number
  market_linkage: number
  source_consensus: number
  analytical_novelty: number
  prediction_specificity: number
}

interface GpvsTimelineEntry {
  date: string
  accuracy_score: number
  sentiment: string
  black_swan: boolean
}

function decodeHtml(text: string): string {
  if (!text) return ''
  return text
    .replace(/&amp;/g, '&')
    .replace(/&lt;/g, '<')
    .replace(/&gt;/g, '>')
    .replace(/&quot;/g, '"')
    .replace(/&#039;/g, "'")
    .replace(/&#39;/g, "'")
    .replace(/&apos;/g, "'")
    .replace(/&nbsp;/g, ' ')
}

function riskColor(risk: string) {
  switch (risk?.toLowerCase()) {
    case 'critical': return 'bg-red-600 text-white'
    case 'high':     return 'bg-orange-500 text-white'
    case 'medium':   return 'bg-yellow-500 text-black'
    case 'low':      return 'bg-green-500 text-white'
    default:         return 'bg-gray-500 text-white'
  }
}

function sentimentColor(sentiment: string) {
  switch (sentiment?.toLowerCase()) {
    case 'bearish': return 'text-red-400'
    case 'bullish': return 'text-green-400'
    default:        return 'text-gray-400'
  }
}

function qualityBadge(score: number) {
  if (score >= 8) return { label: 'Excellent', color: 'bg-green-700 text-green-100' }
  if (score >= 6) return { label: 'Good', color: 'bg-blue-700 text-blue-100' }
  if (score >= 4) return { label: 'Fair', color: 'bg-yellow-700 text-yellow-100' }
  return { label: 'Poor', color: 'bg-red-900 text-red-200' }
}

function GpvsTimelineChart({ entries }: { entries: GpvsTimelineEntry[] }) {
  if (!entries || entries.length === 0) return null
  const max = 100
  return (
    <div className='bg-gray-900 border border-gray-700 rounded-xl p-5 mb-6'>
      <div className='text-xs text-gray-500 uppercase tracking-wider mb-3'>
        📈 GPVS Accuracy Timeline — {entries.length} verified predictions
      </div>
      <div className='flex items-end gap-1 h-24'>
        {entries.map((e, i) => {
          const h = Math.max(4, (e.accuracy_score / max) * 96)
          const col = e.black_swan
            ? 'bg-purple-500'
            : e.accuracy_score >= 75 ? 'bg-green-500'
            : e.accuracy_score >= 50 ? 'bg-yellow-500'
            : 'bg-red-500'
          return (
            <div key={i} className='flex-1 flex flex-col items-center gap-1 group relative'>
              <div className='absolute bottom-full mb-1 hidden group-hover:block bg-gray-800 text-xs text-white px-2 py-1 rounded whitespace-nowrap z-10'>
                {e.date}: {e.accuracy_score}% {e.sentiment} {e.black_swan ? '🚨' : ''}
              </div>
              <div className={`w-full rounded-t ${col}`} style={{ height: h + 'px' }} />
            </div>
          )
        })}
      </div>
      <div className='flex items-center gap-4 mt-3 text-xs text-gray-600'>
        <span className='flex items-center gap-1'><span className='w-2 h-2 bg-green-500 rounded inline-block'/> Correct</span>
        <span className='flex items-center gap-1'><span className='w-2 h-2 bg-yellow-500 rounded inline-block'/> Partial</span>
        <span className='flex items-center gap-1'><span className='w-2 h-2 bg-red-500 rounded inline-block'/> Wrong</span>
        <span className='flex items-center gap-1'><span className='w-2 h-2 bg-purple-500 rounded inline-block'/> Black Swan</span>
      </div>
    </div>
  )
}

function RunCard({ run, reports }: { run: PipelineRun, reports: Report[] }) {
  const [expanded, setExpanded] = useState(false)
  const [articles, setArticles] = useState<Article[]>([])
  const [loadingArticles, setLoadingArticles] = useState(false)
  const [outcome, setOutcome] = useState<PredictionOutcome | null>(null)

  const report = reports.find(r => r.id === run.report_id)

  const handleExpand = () => {
    if (expanded === false && articles.length === 0) {
      setLoadingArticles(true)
      fetch('/api/pipeline-articles?run_id=' + run.id, { headers: { 'X-GNI-Key': GNI_KEY } })
        .then(r => r.json())
        .then(data => {
          const selected = (data.articles || []).filter((a: Article) => a.stage4_selected === true)
          setArticles(selected)
        })
        .catch(() => {})
        .finally(() => setLoadingArticles(false))

      // Fetch GPVS outcome for this report
      if (run.report_id) {
        fetch('/api/prediction-outcomes', { headers: { 'X-GNI-Key': GNI_KEY } })
          .then(r => r.json())
          .then(data => {
            const match = (data.outcomes || []).find((o: PredictionOutcome & {report_id: string}) => o.report_id === run.report_id)
            if (match) setOutcome(match)
          })
          .catch(() => {})
      }
    }
    setExpanded(expanded === false)
  }

  return (
    <div className="bg-gray-900 border border-gray-800 rounded-xl overflow-hidden">
      <button
        onClick={handleExpand}
        className="w-full text-left px-6 py-4 hover:bg-gray-800 transition-colors"
      >
        <div className="flex items-start justify-between gap-4">
          <div className="flex-1">
            <div className="flex items-center gap-3 mb-2 flex-wrap">
              <span className="text-sm font-bold text-blue-400">
                {new Date(run.run_at).toLocaleDateString('en-US', {
                  weekday: 'short', month: 'short', day: 'numeric',
                  hour: '2-digit', minute: '2-digit'
                })}
              </span>
              <span className={`text-xs px-2 py-0.5 rounded ${
                run.status === 'success' ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'
              }`}>
                {run.status}
              </span>
              <span className="text-xs text-gray-600">
                {run.llm_source} - {run.duration_seconds}s - {run.total_collected} articles to {run.total_after_funnel} selected
              </span>
            </div>
            {report ? (
              <div className="flex items-center gap-3 flex-wrap">
                <h3 className="text-white font-semibold text-sm">{report.title}</h3>
                <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${riskColor(report.risk_level)}`}>
                  {report.risk_level?.toUpperCase()}
                </span>
                <span className={`text-xs font-bold ${sentimentColor(report.sentiment)}`}>
                  {report.sentiment}
                </span>
                {(report.quality_score > 0) && (() => { const b = qualityBadge(report.quality_score); return <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${b.color}`}>Q:{report.quality_score}/10 {b.label}</span> })()}
                {report.mad_verdict && (
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${report.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300' : report.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300' : 'bg-gray-700 text-gray-300'}`}>
                    {report.mad_verdict === 'bullish' ? '🐂' : '🐻'} {report.mad_verdict?.toUpperCase()} {report.mad_confidence ? Math.round(report.mad_confidence * 100) + '%' : ''}
                  </span>
                )}
                {report.escalation_level && (
                  <span className={`text-xs font-bold px-2 py-0.5 rounded-full ${report.escalation_level?.toLowerCase() === 'critical' ? 'bg-red-700 text-red-100' : report.escalation_level?.toLowerCase() === 'high' ? 'bg-orange-700 text-orange-100' : 'bg-gray-700 text-gray-300'}`}>
                    ⚡ {report.escalation_level?.toUpperCase()} {report.escalation_score ? report.escalation_score.toFixed(1) + '/10' : ''}
                  </span>
                )}
              </div>
            ) : (
              <div className="text-xs text-gray-600">No report linked to this run</div>
            )}
          </div>
          <span className="text-gray-600 text-xs shrink-0">
            {expanded ? 'Hide' : 'Show'}
          </span>
        </div>
      </button>

      {expanded && (
        <div className="border-t border-gray-800 px-6 py-4 space-y-4">

          {outcome && (
            <div className="bg-gray-900 border border-gray-700 rounded-lg p-4">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">
                🎯 GPVS Outcome — Prediction vs Reality
              </div>
              <div className="grid grid-cols-4 gap-3">
                <div className="text-center">
                  <div className={`text-xl font-bold ${outcome.accuracy_score >= 0.75 ? 'text-green-400' : outcome.accuracy_score >= 0.5 ? 'text-yellow-400' : 'text-red-400'}`}>
                    {Math.round(outcome.accuracy_score * 100)}%
                  </div>
                  <div className="text-xs text-gray-500">GPVS Score</div>
                </div>
                <div className="text-center">
                  <div className={`text-xl font-bold ${outcome.direction_correct_3d ? 'text-green-400' : 'text-red-400'}`}>
                    {outcome.spy_change_3d > 0 ? '+' : ''}{outcome.spy_change_3d?.toFixed(1)}%
                  </div>
                  <div className="text-xs text-gray-500">SPY 3-Day</div>
                </div>
                <div className="text-center">
                  <div className={`text-xl font-bold ${outcome.direction_correct_7d ? 'text-green-400' : 'text-red-400'}`}>
                    {outcome.spy_change_7d > 0 ? '+' : ''}{outcome.spy_change_7d?.toFixed(1)}%
                  </div>
                  <div className="text-xs text-gray-500">SPY 7-Day</div>
                </div>
              </div>
              {outcome.human_review_needed && (
                <div className="mt-2 text-xs text-yellow-400">⚠️ Human review recommended</div>
              )}
            </div>
          )}

          {report && (
            <div className="bg-gray-800 rounded-lg p-4">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">
                Consolidated Intelligence Report
              </div>
              <p className="text-gray-300 text-sm leading-relaxed mb-2">{decodeHtml(report.summary)}</p>
              {report.market_impact && (
                <p className="text-gray-400 text-xs leading-relaxed mb-2">
                  <span className="text-gray-500">Market Impact: </span>
                  {decodeHtml(report.market_impact)}
                </p>
              )}
              <div className="flex items-center gap-3 flex-wrap">
                <span className="text-xs text-gray-500">Location: {report.location_name}</span>
                {report.tickers_affected?.map(t => (
                  <span key={t} className="text-xs font-mono text-blue-400 bg-blue-900 px-2 py-0.5 rounded">
                    {t}
                  </span>
                ))}
              </div>
            </div>
          )}

          {/* SWOT Intelligence */}
          {report && (report.weakness_identified || report.threat_horizon || report.dark_side_detected) && (
            <div className="grid grid-cols-1 md:grid-cols-3 gap-3">
              {report.weakness_identified && (
              <div className="bg-orange-950 border border-orange-800 rounded-lg p-3">
                <div className="text-xs text-orange-400 font-bold mb-1">⚠️ Weakness</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.weakness_identified}</p>
              </div>
              )}
              {report.threat_horizon && (
              <div className="bg-red-950 border border-red-800 rounded-lg p-3">
                <div className="text-xs text-red-400 font-bold mb-1">⏱ Threat Horizon</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.threat_horizon}</p>
              </div>
              )}
              {report.dark_side_detected && report.dark_side_detected !== "None" && (
              <div className="bg-purple-950 border border-purple-800 rounded-lg p-3">
                <div className="text-xs text-purple-400 font-bold mb-1">🌑 Dark Side</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.dark_side_detected}</p>
              </div>
              )}
            </div>
          )}

          {/* Blind Spot + Action */}
          {report && (report.mad_blind_spot || report.mad_action_recommendation) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {report.mad_blind_spot && (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                <div className="text-xs text-orange-400 font-bold mb-1">🔍 Blind Spot</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.mad_blind_spot}</p>
              </div>
              )}
              {report.mad_action_recommendation && (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                <div className="text-xs text-green-400 font-bold mb-1">⚡ Action</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.mad_action_recommendation}</p>
              </div>
              )}
            </div>
          )}

          {/* Short/Long predictions */}
          {report && (report.short_focus_threats || report.long_shoot_threats) && (
            <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
              {report.short_focus_threats && (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                <div className="text-xs text-blue-400 font-bold mb-1">🔮 Short Focus (30d)</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.short_focus_threats}</p>
              </div>
              )}
              {report.long_shoot_threats && (
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3">
                <div className="text-xs text-blue-400 font-bold mb-1">🎯 Long Shoots (180d)</div>
                <p className="text-xs text-gray-300 leading-relaxed">{report.long_shoot_threats}</p>
              </div>
              )}
            </div>
          )}

          <div>
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-2">
              Top Articles Fed to AI ({articles.length})
            </div>

            {loadingArticles && (
              <div className="text-xs text-gray-500 py-2">Loading articles...</div>
            )}

            <div className="space-y-2">
              {articles.map((art, i) => (
                <div key={art.id} className="flex items-start gap-3 bg-gray-800 rounded-lg p-3">
                  <span className="text-xs font-bold text-blue-400 w-6 shrink-0">#{i + 1}</span>
                  <div className="flex-1 min-w-0">
                    <div className="flex items-center gap-2 mb-1">
                      <span className="text-xs text-gray-500 font-mono">{art.source}</span>
                      <span className="text-xs text-yellow-400">Score: {art.stage3_score}</span>
                    </div>
                    {art.url ? (
                      <a
                        href={art.url}
                        target="_blank"
                        rel="noopener noreferrer"
                        className="text-sm text-blue-300 hover:text-blue-200 leading-tight"
                      >
                        {decodeHtml(art.title)}
                      </a>
                    ) : (
                      <div className="text-sm text-white leading-tight">{decodeHtml(art.title)}</div>
                    )}
                    {art.summary && (
                      <p className="text-xs text-gray-500 mt-1 line-clamp-2">{decodeHtml(art.summary)}</p>
                    )}
                  </div>
                </div>
              ))}
            </div>
          </div>
        </div>
      )}
    </div>
  )
}

export default function HistoryPage() {
  const [runs, setRuns] = useState<PipelineRun[]>([])
  const [reports, setReports] = useState<Report[]>([])
  const [loading, setLoading] = useState(true)
  const [timeline, setTimeline] = useState<GpvsTimelineEntry[]>([])

  useEffect(() => {
    Promise.all([
      fetch('/api/pipeline-runs', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
      fetch('/api/reports', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
      fetch('/api/prediction-outcomes', { headers: { 'X-GNI-Key': GNI_KEY } }).then(r => r.json()),
    ]).then(([runsData, reportsData, outcomesData]) => {
      setRuns(runsData.runs || [])
      setReports(reportsData.reports || [])
      setTimeline(outcomesData.timeline || [])
    }).finally(() => setLoading(false))
  }, [])

  const grouped: Record<string, PipelineRun[]> = {}
  runs.forEach(run => {
    const date = new Date(run.run_at).toLocaleDateString('en-US', {
      weekday: 'long', year: 'numeric', month: 'long', day: 'numeric'
    })
    if (grouped[date] === undefined) grouped[date] = []
    grouped[date].push(run)
  })

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/researcher" className="inline-flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 text-green-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">← Pattern Intelligence</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">Intelligence History</h1>
            <p className="text-sm text-gray-400">Intelligence History archives every GNI pipeline run with its full context -- escalation score, sentiment, MAD verdict, confidence interval, and the top articles that drove the analysis. Scroll back through history to identify escalation trends, structural shifts, and turning points in geopolitical risk. Each run is a timestamped snapshot of the world as GNI saw it at that moment.</p>
          </div>
</div>
          </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {loading && (
          <div className="text-center py-20 text-gray-400">
            <p>Loading history...</p>
          </div>
        )}

        {loading === false && runs.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <p>No pipeline runs yet.</p>
          </div>
        )}

        {timeline.length > 0 && <GpvsTimelineChart entries={timeline} />}

        {loading === false && Object.entries(grouped).map(([date, dateRuns]) => (
          <div key={date} className="mb-8">
            <div className="text-xs text-gray-500 uppercase tracking-wider mb-3 flex items-center gap-3">
              <span>{date}</span>
              <span className="text-gray-700">({dateRuns.length} run{dateRuns.length !== 1 ? 's' : ''})</span>
            </div>
            <div className="space-y-3">
              {dateRuns.map(run => (
                <RunCard key={run.id} run={run} reports={reports} />
              ))}
            </div>
          </div>
        ))}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights (Autonomous) | Intelligence History | Pipeline runs 2x daily via GitHub Actions
        </div>
      </footer>
    </div>
  )
}











