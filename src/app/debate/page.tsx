'use client'

import { useEffect, useState } from 'react'

interface RoundPositions {
  bull: string
  bear: string
  black_swan: string
  ostrich: string
}

interface ArbFeedbacks {
  round1: { bull: string; bear: string; black_swan: string; ostrich: string }
  round2: { bull: string; bear: string; black_swan: string; ostrich: string }
}

interface Report {
  id: string
  title: string
  summary: string
  sentiment: string
  mad_verdict: string
  mad_confidence: number
  mad_bull_case: string
  mad_bear_case: string
  mad_black_swan_case: string
  mad_ostrich_case: string
  mad_historian_case: string
  mad_risk_case: string
  mad_reasoning: string
  mad_blind_spot: string
  mad_action_recommendation: string
  short_focus_threats: string
  long_shoot_threats: string
  short_verify_days: number
  long_verify_days: number
  mad_round1_positions: RoundPositions | null
  mad_round2_positions: RoundPositions | null
  mad_round3_positions: RoundPositions | null
  mad_arb_feedbacks: ArbFeedbacks | null
  escalation_score: number
  risk_level: string
  location_name: string
  created_at: string
  tickers_affected: string[]
}

function verdictColor(verdict: string) {
  switch (verdict?.toLowerCase()) {
    case 'bullish': return 'bg-green-900 border-green-600 text-green-300'
    case 'bearish': return 'bg-red-900 border-red-600 text-red-300'
    default: return 'bg-gray-800 border-gray-600 text-gray-300'
  }
}

function confidenceBar(confidence: number) {
  const pct = Math.round((confidence || 0) * 100)
  const color = pct >= 80 ? 'bg-green-500' : pct >= 60 ? 'bg-yellow-500' : 'bg-red-500'
  return { pct, color }
}

const AGENTS = [
  { key: 'bull',       label: 'Bull',        emoji: '🐂', color: 'text-green-400', bg: 'bg-green-950', border: 'border-green-800', desc: 'Known Positives — Opportunity Cost' },
  { key: 'bear',       label: 'Bear',        emoji: '🐻', color: 'text-red-400',   bg: 'bg-red-950',   border: 'border-red-800',   desc: 'Known Negatives — Systemic Failure' },
  { key: 'black_swan', label: 'Black Swan',  emoji: '🦢', color: 'text-blue-400',  bg: 'bg-blue-950',  border: 'border-blue-800',  desc: 'Unknown Negatives — Antifragility' },
  { key: 'ostrich',    label: 'Ostrich',     emoji: '🦦', color: 'text-yellow-400',bg: 'bg-yellow-950',border: 'border-yellow-800',desc: 'Ignored Realities — Inertia' },
]

function getRoundPosition(positions: RoundPositions | null | undefined, key: string): string {
  if (!positions) return ''
  return (positions as unknown as Record<string, string>)[key] || ''
}

function getArbFeedback(feedbacks: ArbFeedbacks | null | undefined, round: 'round1' | 'round2', key: string): string {
  if (!feedbacks) return ''
  return (feedbacks[round] as unknown as Record<string, string>)[key] || ''
}

function AgentCard({ agent, text, coaching, round }: {
  agent: typeof AGENTS[0], text: string, coaching?: string, round: number
}) {
  return (
    <div className={`${agent.bg} ${agent.border} border rounded-xl p-4`}>
      <div className="flex items-center gap-2 mb-2">
        <span className="text-xl">{agent.emoji}</span>
        <div>
          <div className={`text-sm font-bold ${agent.color}`}>{agent.label}</div>
          <div className="text-xs text-gray-500">{agent.desc}</div>
        </div>
        <span className="ml-auto text-xs text-gray-600 font-mono">R{round}</span>
      </div>
      <p className="text-sm text-gray-300 leading-relaxed">{text || <span className="italic text-gray-600">No position recorded</span>}</p>
      {coaching && (
        <div className="mt-3 pt-3 border-t border-gray-700">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">⚖️ Arbitrator feedback</div>
          <p className="text-xs text-gray-400 italic leading-relaxed">{coaching}</p>
        </div>
      )}
    </div>
  )
}

export default function DebatePage() {
  const [reports, setReports] = useState<Report[]>([])
  const [selected, setSelected] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'transcript' | 'verdict' | 'predictions'>('verdict')

  useEffect(() => {
    fetch('/api/reports')
      .then(r => r.json())
      .then(data => {
        const rpts = (data.reports || []).filter((r: Report) => r.mad_verdict)
        setReports(rpts)
        if (rpts.length > 0) setSelected(rpts[0])
      })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const verdictCounts = {
    bullish: reports.filter(r => r.mad_verdict === 'bullish').length,
    bearish: reports.filter(r => r.mad_verdict === 'bearish').length,
    neutral: reports.filter(r => r.mad_verdict === 'neutral').length,
  }

  const isQuadratic = (r: Report | null) => !!(r?.mad_round1_positions)

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-7xl mx-auto px-6 py-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">🐂🐻🦢🦦 Quadratic MAD Protocol</h1>
              <p className="text-sm text-gray-400">Bull → Bear → Black Swan → Ostrich → Arbitrator — 3 Live Rounds on Future Threats</p>
              <p className="text-xs text-gray-500 mt-1 max-w-3xl">
                Four agents debate future threats across two axes: Known/Unknown × Proactive/Ignored.
                Arbitrator coaches each agent after every round. Based on all relevant intelligence articles.
                Short Focus (7-30 days) and Long Shoots (3-24 months) tracked for real-world validation.
              </p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300 shrink-0 mt-1">← Dashboard</a>
          </div>
          {reports.length > 0 && (
            <div className="grid grid-cols-4 gap-3 mt-4">
              <div className="bg-green-950 border border-green-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-green-400">{verdictCounts.bullish}</div>
                <div className="text-xs text-green-600">🐂 Bullish</div>
              </div>
              <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-red-400">{verdictCounts.bearish}</div>
                <div className="text-xs text-red-600">🐻 Bearish</div>
              </div>
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-gray-400">{verdictCounts.neutral}</div>
                <div className="text-xs text-gray-500">◆ Neutral</div>
              </div>
              <div className="bg-blue-950 border border-blue-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-blue-400">{reports.length}</div>
                <div className="text-xs text-blue-600">Total Debates</div>
              </div>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-7xl mx-auto px-6 py-8">
        {loading && <div className="text-center py-20 text-gray-400">Loading debates...</div>}

        {!loading && reports.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">🐂🐻🦢🦦</div>
            <p>No Quadratic debates yet. Pipeline will generate debates on next run.</p>
          </div>
        )}

        {!loading && reports.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-5 gap-6">

            {/* Sidebar */}
            <div className="lg:col-span-1">
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Debates ({reports.length})</div>
                <div className="space-y-2 max-h-[700px] overflow-y-auto">
                  {reports.map(r => {
                    const { pct, color } = confidenceBar(r.mad_confidence)
                    return (
                      <button key={r.id} onClick={() => { setSelected(r); setActiveTab('verdict') }}
                        className={`w-full text-left p-3 rounded-lg text-xs transition-colors ${
                          selected?.id === r.id ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                        }`}>
                        <div className="font-bold mb-1 line-clamp-2">{r.title}</div>
                        <div className="flex items-center justify-between">
                          <span className={`px-1.5 py-0.5 rounded text-xs font-bold ${
                            r.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300' :
                            r.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300' : 'bg-gray-700 text-gray-300'
                          }`}>{r.mad_verdict?.toUpperCase()}</span>
                          <span className="text-gray-500">{pct}%</span>
                        </div>
                        <div className="mt-1.5 bg-gray-700 rounded-full h-1">
                          <div className={`${color} h-1 rounded-full`} style={{ width: pct + '%' }} />
                        </div>
                        {isQuadratic(r) && <div className="text-blue-400 text-xs mt-1">★ Quadratic</div>}
                        <div className="text-gray-600 mt-1">{new Date(r.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit' })}</div>
                      </button>
                    )
                  })}
                </div>
              </div>

              {/* Quadrant map */}
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-4 mt-4">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Quadrant Map</div>
                <div className="grid grid-cols-2 gap-1 text-xs">
                  <div className="bg-green-950 border border-green-800 rounded p-2 text-center">
                    <div>🐂 Bull</div>
                    <div className="text-gray-500">Known +</div>
                  </div>
                  <div className="bg-blue-950 border border-blue-800 rounded p-2 text-center">
                    <div>🦢 Swan</div>
                    <div className="text-gray-500">Unknown -</div>
                  </div>
                  <div className="bg-red-950 border border-red-800 rounded p-2 text-center">
                    <div>🐻 Bear</div>
                    <div className="text-gray-500">Known -</div>
                  </div>
                  <div className="bg-yellow-950 border border-yellow-800 rounded p-2 text-center">
                    <div>🦦 Ostrich</div>
                    <div className="text-gray-500">Ignored</div>
                  </div>
                </div>
              </div>
            </div>

            {/* Main content */}
            {selected && (
              <div className="lg:col-span-4 space-y-4">

                {/* Report context */}
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <h2 className="text-lg font-bold text-white">{selected.title}</h2>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                        selected.risk_level?.toLowerCase() === 'critical' ? 'bg-red-600 text-white' :
                        selected.risk_level?.toLowerCase() === 'high' ? 'bg-orange-500 text-white' : 'bg-gray-600 text-white'
                      }`}>{selected.risk_level?.toUpperCase()}</span>
                      {selected.escalation_score > 0 && (
                        <span className="text-xs font-bold px-2 py-1 rounded-full bg-red-900 border border-red-700 text-red-200">
                          ⚡ {selected.escalation_score.toFixed(1)}/10
                        </span>
                      )}
                      {isQuadratic(selected) && (
                        <span className="text-xs font-bold px-2 py-1 rounded-full bg-blue-900 border border-blue-700 text-blue-200">
                          ★ Quadratic
                        </span>
                      )}
                    </div>
                  </div>
                  <p className="text-gray-400 text-sm">{selected.summary}</p>
                  <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                    <span>📍 {selected.location_name || 'Global'}</span>
                    <span>{new Date(selected.created_at).toLocaleString()}</span>
                    {selected.tickers_affected?.slice(0, 4).map(t => (
                      <span key={t} className="font-mono text-blue-400">{t}</span>
                    ))}
                  </div>
                </div>

                {/* Tabs */}
                <div className="flex gap-2">
                  {(['verdict', 'transcript', 'predictions'] as const).map(tab => (
                    <button key={tab} onClick={() => setActiveTab(tab)}
                      className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                        activeTab === tab ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                      }`}>
                      {tab === 'transcript' ? '📜 Debate Transcript' :
                       tab === 'verdict' ? '⚖️ Verdict & Synthesis' : '🔮 Predictions'}
                    </button>
                  ))}
                </div>

                {/* TRANSCRIPT TAB */}
                {activeTab === 'transcript' && (
                  <div className="space-y-6">
                    {isQuadratic(selected) ? (
                      <>
                        {/* Round 1 */}
                        <div>
                          <div className="flex items-center gap-3 mb-3">
                            <div className="bg-gray-700 text-white text-xs font-bold px-3 py-1 rounded-full">ROUND 1</div>
                            <div className="text-sm text-gray-400">Opening positions on future threats</div>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {AGENTS.map(agent => (
                              <AgentCard key={agent.key} agent={agent} round={1}
                                text={getRoundPosition(selected.mad_round1_positions, agent.key) || ''}
                                coaching={getArbFeedback(selected.mad_arb_feedbacks, 'round1', agent.key)} />
                            ))}
                          </div>
                          <div className="mt-3 bg-gray-900 border border-gray-700 rounded-xl p-4">
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-lg">⚖️</span>
                              <div className="text-sm font-bold text-blue-400">Arbitrator Coaching — After Round 1</div>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                              {AGENTS.map(agent => (
                                <div key={agent.key} className="bg-gray-800 rounded-lg p-2">
                                  <div className={`font-bold mb-1 ${agent.color}`}>{agent.emoji} To {agent.label}</div>
                                  <p className="text-gray-400 italic">{getArbFeedback(selected.mad_arb_feedbacks, 'round1', agent.key) || 'No coaching recorded'}</p>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>

                        {/* Round 2 */}
                        <div>
                          <div className="flex items-center gap-3 mb-3">
                            <div className="bg-blue-900 text-blue-200 text-xs font-bold px-3 py-1 rounded-full">ROUND 2</div>
                            <div className="text-sm text-gray-400">Refined positions after Arbitrator coaching</div>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {AGENTS.map(agent => (
                              <AgentCard key={agent.key} agent={agent} round={2}
                                text={getRoundPosition(selected.mad_round2_positions, agent.key) || ''}
                                coaching={getArbFeedback(selected.mad_arb_feedbacks, 'round2', agent.key)} />
                            ))}
                          </div>
                          <div className="mt-3 bg-gray-900 border border-gray-700 rounded-xl p-4">
                            <div className="flex items-center gap-2 mb-2">
                              <span className="text-lg">⚖️</span>
                              <div className="text-sm font-bold text-blue-400">Arbitrator Coaching — After Round 2</div>
                            </div>
                            <div className="grid grid-cols-2 md:grid-cols-4 gap-3 text-xs">
                              {AGENTS.map(agent => (
                                <div key={agent.key} className="bg-gray-800 rounded-lg p-2">
                                  <div className={`font-bold mb-1 ${agent.color}`}>{agent.emoji} To {agent.label}</div>
                                  <p className="text-gray-400 italic">{getArbFeedback(selected.mad_arb_feedbacks, 'round2', agent.key) || 'No coaching recorded'}</p>
                                </div>
                              ))}
                            </div>
                          </div>
                        </div>

                        {/* Round 3 */}
                        <div>
                          <div className="flex items-center gap-3 mb-3">
                            <div className="bg-purple-900 text-purple-200 text-xs font-bold px-3 py-1 rounded-full">ROUND 3</div>
                            <div className="text-sm text-gray-400">Final positions — sharpest analysis</div>
                          </div>
                          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {AGENTS.map(agent => (
                              <AgentCard key={agent.key} agent={agent} round={3}
                                text={getRoundPosition(selected.mad_round3_positions, agent.key) || ''} />
                            ))}
                          </div>
                        </div>
                      </>
                    ) : (
                      /* Old format fallback */
                      <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                        <div className="bg-green-950 border border-green-800 rounded-xl p-5">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-2xl">🐂</span>
                            <div>
                              <div className="text-sm font-bold text-green-400">Bull Agent</div>
                              <div className="text-xs text-green-700">Argues for opportunity</div>
                            </div>
                          </div>
                          <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_bull_case}</p>
                        </div>
                        <div className="bg-red-950 border border-red-800 rounded-xl p-5">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-2xl">🐻</span>
                            <div>
                              <div className="text-sm font-bold text-red-400">Bear Agent</div>
                              <div className="text-xs text-red-700">Argues for risk</div>
                            </div>
                          </div>
                          <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_bear_case}</p>
                        </div>
                        <div className="bg-amber-950 border border-amber-800 rounded-xl p-5">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-2xl">📜</span>
                            <div>
                              <div className="text-sm font-bold text-amber-400">Historian Agent</div>
                              <div className="text-xs text-amber-700">Historical precedents</div>
                            </div>
                          </div>
                          <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_historian_case || 'Not available for this report.'}</p>
                        </div>
                        <div className="bg-purple-950 border border-purple-800 rounded-xl p-5">
                          <div className="flex items-center gap-2 mb-3">
                            <span className="text-2xl">🚨</span>
                            <div>
                              <div className="text-sm font-bold text-purple-400">Risk Manager</div>
                              <div className="text-xs text-purple-700">Tail risk</div>
                            </div>
                          </div>
                          <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_risk_case || 'Not available for this report.'}</p>
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* VERDICT TAB */}
                {activeTab === 'verdict' && (
                  <div className="space-y-4">
                    <div className={`border rounded-xl p-5 ${verdictColor(selected.mad_verdict)}`}>
                      <div className="flex items-center gap-3 mb-3">
                        <span className="text-3xl">
                          {selected.mad_verdict === 'bullish' ? '🐂' : selected.mad_verdict === 'bearish' ? '🐻' : '⚖️'}
                        </span>
                        <div>
                          <div className="text-xl font-bold">ARBITRATOR VERDICT: {selected.mad_verdict?.toUpperCase()}</div>
                          <div className="text-sm opacity-75">Confidence: {Math.round((selected.mad_confidence || 0) * 100)}%</div>
                        </div>
                      </div>
                      <div className="bg-black bg-opacity-30 rounded-full h-3 mb-4">
                        <div className={`h-3 rounded-full ${confidenceBar(selected.mad_confidence).color}`}
                          style={{ width: confidenceBar(selected.mad_confidence).pct + '%' }} />
                      </div>
                      {selected.mad_reasoning && (
                        <div>
                          <div className="text-xs uppercase tracking-wider opacity-60 mb-1">Arbitrator Reasoning</div>
                          <p className="text-sm leading-relaxed opacity-90">{selected.mad_reasoning}</p>
                        </div>
                      )}
                    </div>

                    {selected.mad_blind_spot && (
                      <div className="bg-orange-950 border border-orange-800 rounded-xl p-5">
                        <div className="text-xs text-orange-400 font-bold uppercase tracking-wider mb-2">🔍 Blind Spot Quadrant</div>
                        <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_blind_spot}</p>
                      </div>
                    )}

                    {selected.mad_action_recommendation && (
                      <div className="bg-green-950 border border-green-800 rounded-xl p-5">
                        <div className="text-xs text-green-400 font-bold uppercase tracking-wider mb-2">⚡ Action Recommendation</div>
                        <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_action_recommendation}</p>
                      </div>
                    )}

                    {/* Final positions summary */}
                    {isQuadratic(selected) && (
                      <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                        <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Final Positions — Round 3</div>
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                          {AGENTS.map(agent => (
                            <div key={agent.key} className={`${agent.bg} ${agent.border} border rounded-lg p-3`}>
                              <div className={`text-xs font-bold ${agent.color} mb-1`}>{agent.emoji} {agent.label}</div>
                              <p className="text-xs text-gray-300 leading-relaxed line-clamp-3">
                                {getRoundPosition(selected.mad_round3_positions, agent.key) || selected[`mad_${agent.key === 'black_swan' ? 'black_swan' : agent.key}_case` as keyof Report] as string || 'No position'}
                              </p>
                            </div>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                )}

                {/* PREDICTIONS TAB */}
                {activeTab === 'predictions' && (
                  <div className="space-y-4">
                    <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                      <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">🔮 Short Focus — {selected.short_verify_days || 14} Days</div>
                      {selected.short_focus_threats ? (
                        <p className="text-sm text-gray-300 leading-relaxed">{selected.short_focus_threats}</p>
                      ) : (
                        <p className="text-sm text-gray-600 italic">Available for Quadratic MAD reports only.</p>
                      )}
                    </div>
                    <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                      <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">🎯 Long Shoots — {selected.long_verify_days || 180} Days</div>
                      {selected.long_shoot_threats ? (
                        <p className="text-sm text-gray-300 leading-relaxed">{selected.long_shoot_threats}</p>
                      ) : (
                        <p className="text-sm text-gray-600 italic">Available for Quadratic MAD reports only.</p>
                      )}
                    </div>
                    <div className="bg-blue-950 border border-blue-800 rounded-xl p-4">
                      <div className="text-xs text-blue-400 font-bold mb-2">How Prediction Validation Works</div>
                      <p className="text-xs text-gray-400 leading-relaxed">
                        Short Focus predictions are verified after {selected.short_verify_days || 14} days.
                        Long Shoot predictions are verified after {selected.long_verify_days || 180} days.
                        When real world events occur, each prediction is marked accurate or missed.
                        Over time this builds a track record of which agent sees furthest ahead.
                      </p>
                    </div>
                  </div>
                )}

              </div>
            )}
          </div>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-7xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights (Autonomous) | Quadratic MAD Protocol — Future Threat Intelligence | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
