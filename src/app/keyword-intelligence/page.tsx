'use client'
import { useEffect, useState } from 'react'

interface SecurityLog {
  id: string
  keyword_raw: string
  keyword_clean: string
  sources: string[]
  layer1_passed: boolean
  layer1_reason: string
  layer2_passed: boolean
  layer2_reason: string
  layer3_applied: boolean
  layer4_passed: boolean
  layer4_signature: Record<string, unknown> | null
  layer5_passed: boolean
  layer6_passed: boolean
  security_veto: boolean
  agent_analyst_vote: string
  agent_analyst_confidence: number
  agent_analyst_reason: string
  agent_auditor_vote: string
  agent_auditor_confidence: number
  agent_auditor_attack_prob: number
  agent_auditor_reason: string
  agent_advocate_vote: string
  agent_advocate_confidence: number
  agent_advocate_reason: string
  vote_result: string
  final_decision: string
  attack_type: string
  created_at: string
}

interface Keyword {
  id: string
  keyword: string
  status: string
  pillar_suggestion: string
  frequency_count: number
  source_count: number
  groq_definition: string
  created_at: string
}

interface Stats {
  total_processed: number
  layer1_blocked: number
  layer2_blocked: number
  layer4_blocked: number
  layer6_blocked: number
  security_veto: number
  auto_rejected: number
  recommended: number
  vote_3_0: number
  vote_2_1: number
  vote_1_2: number
  vote_0_3: number
}

const voteColor = (r: string) => {
  if (r === '3-0') return 'bg-green-900 border-green-600 text-green-300'
  if (r === '2-1') return 'bg-yellow-900 border-yellow-600 text-yellow-300'
  if (r === '1-2') return 'bg-orange-900 border-orange-600 text-orange-300'
  if (r === '0-3') return 'bg-red-900 border-red-600 text-red-300'
  if (r === 'SECURITY_VETO') return 'bg-red-950 border-red-500 text-red-200'
  return 'bg-gray-800 border-gray-600 text-gray-300'
}
const decisionColor = (d: string) => d === 'RECOMMEND' ? 'text-green-400' : d === 'AUTO_REJECT' ? 'text-red-400' : 'text-gray-400'
const statusColor = (s: string) => s === 'approved' ? 'bg-green-700 text-white' : s === 'candidate' ? 'bg-blue-700 text-white' : s === 'watching' ? 'bg-yellow-700 text-white' : 'bg-gray-700 text-gray-300'
const pillarColor = (p: string) => p === 'geo' ? 'text-red-400' : p === 'tech' ? 'text-blue-400' : p === 'fin' ? 'text-green-400' : 'text-gray-400'

function LayerBadge({ passed, label }: { passed: boolean; label: string }) {
  return (
    <span className={`text-xs px-2 py-0.5 rounded font-mono ${passed ? 'bg-green-900 text-green-400' : 'bg-red-900 text-red-400'}`}>
      {passed ? '✓' : '✗'} {label}
    </span>
  )
}

function AgentBadge({ vote, confidence, name }: { vote: string; confidence: number; name: string }) {
  const ok = vote === 'approve'
  return (
    <div className={`text-xs px-2 py-1 rounded border ${ok ? 'bg-green-950 border-green-700 text-green-300' : 'bg-red-950 border-red-700 text-red-300'}`}>
      <div className='font-bold'>{name}</div>
      <div>{ok ? '✅' : '❌'} {vote?.toUpperCase()} {Math.round(confidence * 100)}%</div>
    </div>
  )
}

export default function KeywordIntelligencePage() {
  const [logs, setLogs] = useState<SecurityLog[]>([])
  const [keywords, setKeywords] = useState<Keyword[]>([])
  const [stats, setStats] = useState<Stats | null>(null)
  const [loading, setLoading] = useState(true)
  const [tab, setTab] = useState<'journey' | 'pending' | 'approved' | 'explainer'>('journey')
  const [expanded, setExpanded] = useState<string | null>(null)

  useEffect(() => {
    fetch('/api/keyword-intelligence')
      .then(r => r.json())
      .then(d => { setLogs(d.logs || []); setKeywords(d.keywords || []); setStats(d.stats || null) })
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const pending  = keywords.filter(k => k.status === 'candidate')
  const approved = keywords.filter(k => k.status === 'approved')

  return (
    <div className='min-h-screen bg-gray-950 text-gray-100'>
      <header className='border-b border-gray-800 bg-gray-900'>
        <div className='max-w-7xl mx-auto px-6 py-4'>
          <div className='flex items-start justify-between gap-4'>
            <div>
              <h1 className='text-2xl font-bold text-white'>🔐 Keyword Intelligence Engine</h1>
              <p className='text-sm text-gray-400'>How GNI detects and validates emerging intelligence vocabulary</p>
              <p className='text-xs text-gray-600 mt-1'>7 security layers + 3-agent MAD voting + human final approval</p>
            </div>
            <a href='/' className='text-sm text-blue-400 hover:text-blue-300 shrink-0 mt-1'>← Dashboard</a>
          </div>
          {stats && (
            <div className='grid grid-cols-4 gap-3 mt-4'>
              <div className='bg-gray-800 border border-gray-700 rounded-lg p-3 text-center'>
                <div className='text-2xl font-bold text-white'>{stats.total_processed}</div>
                <div className='text-xs text-gray-500'>Total Processed</div>
              </div>
              <div className='bg-red-950 border border-red-800 rounded-lg p-3 text-center'>
                <div className='text-2xl font-bold text-red-400'>{stats.auto_rejected}</div>
                <div className='text-xs text-red-600'>❌ Auto-Rejected</div>
              </div>
              <div className='bg-green-950 border border-green-800 rounded-lg p-3 text-center'>
                <div className='text-2xl font-bold text-green-400'>{stats.recommended}</div>
                <div className='text-xs text-green-600'>✅ Recommended</div>
              </div>
              <div className='bg-orange-950 border border-orange-800 rounded-lg p-3 text-center'>
                <div className='text-2xl font-bold text-orange-400'>{stats.security_veto}</div>
                <div className='text-xs text-orange-600'>🛡 Security Veto</div>
              </div>
            </div>
          )}
        </div>
      </header>

      <main className='max-w-7xl mx-auto px-6 py-8'>
        {loading && <div className='text-center py-20 text-gray-400'><div className='text-4xl mb-4'>⌛</div><p>Loading...</p></div>}
        {!loading && (
          <>
            <div className='flex gap-2 mb-6 flex-wrap'>
              {([
                { key: 'journey',   label: '🧭 Journey',  count: logs.length },
                { key: 'pending',   label: '⌛ Pending', count: pending.length },
                { key: 'approved',  label: '✅ Approved',   count: approved.length },
                { key: 'explainer', label: '💡 How It Works', count: 0 },
              ] as const).map(({ key, label, count }) => (
                <button key={key} onClick={() => setTab(key)}
                  className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${tab === key ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'}`}>
                  {label} {count > 0 && <span className='ml-1 bg-gray-700 px-1.5 py-0.5 rounded-full text-xs'>{count}</span>}
                </button>
              ))}
            </div>

            {tab === 'journey' && (
              <section>
                {stats && (
                  <div className='bg-gray-900 border border-gray-700 rounded-xl p-5 mb-6'>
                    <div className='text-xs text-gray-500 uppercase tracking-wider mb-3'>🛡 Security Layer Stats</div>
                    <div className='grid grid-cols-2 md:grid-cols-4 gap-3 mb-4'>
                      {[
                        { label: 'L1 Unicode', count: stats.layer1_blocked, color: 'text-purple-400' },
                        { label: 'L2 Sources', count: stats.layer2_blocked, color: 'text-blue-400' },
                        { label: 'L4 NER', count: stats.layer4_blocked, color: 'text-yellow-400' },
                        { label: 'L6 Output', count: stats.layer6_blocked, color: 'text-orange-400' },
                      ].map(({ label, count, color }) => (
                        <div key={label} className='bg-gray-800 rounded-lg p-3 text-center'>
                          <div className={`text-xl font-bold ${color}`}>{count}</div>
                          <div className='text-xs text-gray-500 mt-1'>{label}</div>
                        </div>
                      ))}
                    </div>
                    <div className='text-xs text-gray-500 uppercase tracking-wider mb-3'>🗳 Agent Votes</div>
                    <div className='grid grid-cols-4 gap-3'>
                      {[
                        { label: '3-0 Unanimous', count: stats.vote_3_0, color: 'text-green-400' },
                        { label: '2-1 Majority',  count: stats.vote_2_1, color: 'text-yellow-400' },
                        { label: '1-2 Minority',  count: stats.vote_1_2, color: 'text-orange-400' },
                        { label: '0-3 Rejected',  count: stats.vote_0_3, color: 'text-red-400' },
                      ].map(({ label, count, color }) => (
                        <div key={label} className='bg-gray-800 rounded-lg p-3 text-center'>
                          <div className={`text-xl font-bold ${color}`}>{count}</div>
                          <div className='text-xs text-gray-500 mt-1'>{label}</div>
                        </div>
                      ))}
                    </div>
                  </div>
                )}
                {logs.length === 0 && (
                  <div className='text-center py-20 text-gray-500'>
                    <div className='text-4xl mb-4'>🔐</div>
                    <p>No keyword processing logs yet. Logs appear after next pipeline run.</p>
                  </div>
                )}
                <div className='space-y-3'>
                  {logs.map(log => (
                    <div key={log.id} className={`bg-gray-900 border rounded-xl overflow-hidden ${log.security_veto ? 'border-red-600' : log.final_decision === 'RECOMMEND' ? 'border-green-700' : 'border-gray-700'}`}>
                      <button onClick={() => setExpanded(expanded === log.id ? null : log.id)}
                        className='w-full text-left px-5 py-3 hover:bg-gray-800 transition-colors'>
                        <div className='flex items-center justify-between gap-4'>
                          <div className='flex items-center gap-3 flex-wrap'>
                            <span className='font-mono text-sm font-bold text-white'>{log.keyword_clean || log.keyword_raw || 'unknown'}</span>
                            {log.vote_result && <span className={`text-xs px-2 py-0.5 rounded-full border font-bold ${voteColor(log.vote_result)}`}>{log.vote_result}</span>}
                            <span className={`text-xs font-bold ${decisionColor(log.final_decision)}`}>{log.final_decision === 'RECOMMEND' ? '✅ RECOMMEND' : log.final_decision === 'AUTO_REJECT' ? '❌ AUTO-REJECT' : log.final_decision}</span>
                            {log.security_veto && <span className='text-xs bg-red-900 text-red-300 px-2 py-0.5 rounded-full border border-red-600 font-bold'>🛡 VETO</span>}
                          </div>
                          <span className='text-gray-600 text-xs'>{expanded === log.id ? '▲' : '▼'}</span>
                        </div>
                        <div className='flex gap-1.5 mt-2 flex-wrap'>
                          <LayerBadge passed={log.layer1_passed} label='L1' />
                          <LayerBadge passed={log.layer2_passed} label='L2' />
                          <LayerBadge passed={log.layer3_applied} label='L3' />
                          <LayerBadge passed={log.layer4_passed} label='L4' />
                          <LayerBadge passed={log.layer5_passed} label='L5' />
                          <LayerBadge passed={log.layer6_passed} label='L6' />
                          <LayerBadge passed={!log.security_veto} label='Veto' />
                        </div>
                      </button>
                      {expanded === log.id && (
                        <div className='border-t border-gray-800 px-5 py-4 space-y-4'>
                          <div className='space-y-1.5 text-xs'>
                            {[
                              { label: 'L1 Unicode Normalization', passed: log.layer1_passed, reason: log.layer1_reason },
                              { label: 'L2 Source Credibility', passed: log.layer2_passed, reason: log.layer2_reason },
                              { label: 'L3 Context Boundary', passed: log.layer3_applied, reason: 'Applied per-article' },
                              { label: 'L4 NER Event Signature', passed: log.layer4_passed, reason: log.layer4_signature ? JSON.stringify(log.layer4_signature).slice(0,80) : 'No Actor+Action or Location+Action' },
                              { label: 'L5 Groq Hardened', passed: log.layer5_passed, reason: 'Definition generated' },
                              { label: 'L6 Output Sanitization', passed: log.layer6_passed, reason: 'Final blocklist check' },
                            ].map(({ label, passed, reason }) => (
                              <div key={label} className='flex items-start gap-2'>
                                <span className={`font-bold shrink-0 ${passed ? 'text-green-400' : 'text-red-400'}`}>{passed ? '✓' : '✗'}</span>
                                <span className={passed ? 'text-gray-300' : 'text-red-300'}>{label}</span>
                                {reason && <span className='text-gray-600 ml-auto text-right max-w-xs'>{reason}</span>}
                              </div>
                            ))}
                          </div>
                          {log.vote_result && (
                            <div>
                              <div className='text-xs text-gray-500 uppercase tracking-wider mb-2'>🗳 Agent Votes ({log.vote_result})</div>
                              <div className='grid grid-cols-3 gap-3'>
                                <AgentBadge vote={log.agent_analyst_vote}  confidence={log.agent_analyst_confidence}  name='🧐 Analyst' />
                                <AgentBadge vote={log.agent_auditor_vote}  confidence={log.agent_auditor_confidence}  name='🛡 Auditor' />
                                <AgentBadge vote={log.agent_advocate_vote} confidence={log.agent_advocate_confidence} name='⚖️ Advocate' />
                              </div>
                              <div className='mt-2 space-y-1 text-xs text-gray-500'>
                                {log.agent_analyst_reason  && <div>🧐 {log.agent_analyst_reason}</div>}
                                {log.agent_auditor_reason  && <div>🛡 {log.agent_auditor_reason} (atk: {Math.round(log.agent_auditor_attack_prob * 100)}%)</div>}
                                {log.agent_advocate_reason && <div>⚖️ {log.agent_advocate_reason}</div>}
                              </div>
                            </div>
                          )}
                          {log.sources?.length > 0 && (
                            <div>
                              <div className='text-xs text-gray-500 uppercase tracking-wider mb-1'>📡 Sources ({log.sources.length})</div>
                              <div className='flex flex-wrap gap-1'>
                                {log.sources.map((s: string) => <span key={s} className='text-xs bg-gray-800 text-gray-400 px-2 py-0.5 rounded'>{s}</span>)}
                              </div>
                            </div>
                          )}
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              </section>
            )}

            {tab === 'pending' && (
              <section>
                <div className='text-xs text-gray-500 uppercase tracking-wider mb-4'>Keywords recommended by agents -- your final approval via Telegram</div>
                {pending.length === 0 && <div className='text-center py-20 text-gray-500'><div className='text-4xl mb-4'>⌛</div><p>No keywords pending review.</p></div>}
                <div className='space-y-3'>
                  {pending.map(kw => (
                    <div key={kw.id} className='bg-gray-900 border border-yellow-700 rounded-xl p-5'>
                      <div className='flex items-start justify-between gap-4 mb-2'>
                        <div>
                          <span className='font-mono font-bold text-white text-lg'>{kw.keyword}</span>
                          <span className={`ml-3 text-xs font-bold ${pillarColor(kw.pillar_suggestion)}`}>{kw.pillar_suggestion?.toUpperCase()}</span>
                        </div>
                        <span className={`text-xs font-bold px-2 py-1 rounded-full ${statusColor(kw.status)}`}>{kw.status?.toUpperCase()}</span>
                      </div>
                      {kw.groq_definition && <p className='text-sm text-gray-400 mb-3'>{kw.groq_definition}</p>}
                      <div className='flex gap-4 text-xs text-gray-500'>
                        <span>Frequency: <span className='text-white font-bold'>{kw.frequency_count}</span></span>
                        <span>Sources: <span className='text-white font-bold'>{kw.source_count}</span></span>
                        <span>{new Date(kw.created_at).toLocaleDateString('en-US', { month: 'short', day: 'numeric' })}</span>
                      </div>
                      <div className='mt-2 text-xs text-yellow-600'>⚠️ Approve or reject via Telegram.</div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {tab === 'approved' && (
              <section>
                <div className='text-xs text-gray-500 uppercase tracking-wider mb-4'>Keywords approved and active in the intelligence funnel</div>
                {approved.length === 0 && <div className='text-center py-20 text-gray-500'><div className='text-4xl mb-4'>✅</div><p>No approved keywords yet.</p></div>}
                <div className='grid grid-cols-1 md:grid-cols-2 gap-3'>
                  {approved.map(kw => (
                    <div key={kw.id} className='bg-gray-900 border border-green-800 rounded-xl p-4'>
                      <div className='flex items-center justify-between mb-2'>
                        <span className='font-mono font-bold text-green-300'>{kw.keyword}</span>
                        <span className={`text-xs font-bold ${pillarColor(kw.pillar_suggestion)}`}>{kw.pillar_suggestion?.toUpperCase()}</span>
                      </div>
                      {kw.groq_definition && <p className='text-xs text-gray-500 mb-2'>{kw.groq_definition}</p>}
                      <div className='flex gap-3 text-xs text-gray-600'>
                        <span>Freq: {kw.frequency_count}</span>
                        <span>Sources: {kw.source_count}</span>
                      </div>
                    </div>
                  ))}
                </div>
              </section>
            )}

            {tab === 'explainer' && (
              <section className='space-y-6'>
                <div className='bg-gray-900 border border-gray-700 rounded-xl p-6'>
                  <div className='text-xs text-gray-500 uppercase tracking-wider mb-4'>💡 7 Security Layers</div>
                  <div className='space-y-3'>
                    {[
                      { step: 'Layer 1 — Unicode Normalization', desc: 'Homoglyph mapping, invisible character removal, HTML entity decode. Kills spoofing attacks.', color: 'border-purple-600' },
                      { step: 'Layer 2 — Source Credibility Gate', desc: 'Requires 2+ trusted sources. Blocks single-source floods. Kills manipulation attacks.', color: 'border-blue-600' },
                      { step: 'Layer 3 — Context Boundary', desc: 'Title max 120 chars, summary max 200 chars. Cuts at injection markers.', color: 'border-cyan-600' },
                      { step: 'Layer 4 — NER Event Signature', desc: 'GDELT-inspired: requires Actor+Action or Location+Action. Deterministic dictionaries only. Eliminates generic words.', color: 'border-yellow-600' },
                      { step: 'Layer 5 — Groq Hardened Call', desc: 'System prompt enforces JSON-only output. No raw article text reaches Groq.', color: 'border-orange-600' },
                      { step: 'Layer 6 — Output Sanitization', desc: 'Final blocklist, 1-3 word limit, NER signature required. Last line of defense.', color: 'border-red-600' },
                      { step: 'Layer 7 — Audit Trail', desc: 'All processing logged to keyword_security_log. Every decision recorded with full reasoning.', color: 'border-gray-500' },
                    ].map(({ step, desc, color }) => (
                      <div key={step} className={`border-l-4 ${color} pl-4`}>
                        <div className='text-sm font-bold text-white'>{step}</div>
                        <div className='text-xs text-gray-400 mt-0.5'>{desc}</div>
                      </div>
                    ))}
                  </div>
                </div>
                <div className='bg-gray-900 border border-gray-700 rounded-xl p-6'>
                  <div className='text-xs text-gray-500 uppercase tracking-wider mb-4'>🗳 3-Agent MAD Voting</div>
                  <div className='grid grid-cols-1 md:grid-cols-3 gap-4 mb-4'>
                    {[
                      { name: '🧐 Intelligence Analyst', role: 'Relevance scorer', q: 'Is this a genuine intelligence signal?', ok: 'Conflict/sanctions/tech warfare signal', no: 'Generic word, no intelligence value' },
                      { name: '🛡 Security Auditor',     role: 'Attack detector (VETO)', q: 'Could this be a manipulation attempt?', ok: 'Organic rise, diverse trusted sources', no: 'Sudden spike, low source diversity' },
                      { name: '⚖️ Devils Advocate',      role: 'Novelty validator', q: 'Is this truly new or just noise?', ok: 'Not in 90-day history, 5x+ spike', no: 'Fades in 48hrs, single news cycle' },
                    ].map(({ name, role, q, ok, no }) => (
                      <div key={name} className='bg-gray-800 rounded-xl p-4'>
                        <div className='font-bold text-white mb-1'>{name}</div>
                        <div className='text-xs text-gray-500 mb-2'>{role}</div>
                        <div className='text-xs text-gray-400 italic mb-3'>&ldquo;{q}&rdquo;</div>
                        <div className='text-xs text-green-400 mb-1'>✓ {ok}</div>
                        <div className='text-xs text-red-400'>✗ {no}</div>
                      </div>
                    ))}
                  </div>
                  <div className='grid grid-cols-4 gap-3 text-xs mb-3'>
                    {[
                      { label: '3-0', sub: 'Unanimous', desc: 'Recommend (prominent)', c: 'border-green-700 bg-green-950 text-green-300' },
                      { label: '2-1', sub: 'Majority',  desc: 'Recommend + dissent',   c: 'border-yellow-700 bg-yellow-950 text-yellow-300' },
                      { label: '1-2', sub: 'Minority',  desc: 'Auto-rejected, logged', c: 'border-orange-700 bg-orange-950 text-orange-300' },
                      { label: '0-3', sub: 'Rejected',  desc: 'Auto-rejected + flag',  c: 'border-red-700 bg-red-950 text-red-300' },
                    ].map(({ label, sub, desc, c }) => (
                      <div key={label} className={`border rounded-lg p-3 text-center ${c}`}>
                        <div className='font-bold text-lg'>{label}</div>
                        <div className='text-xs opacity-70'>{sub}</div>
                        <div className='text-gray-400 mt-1 text-xs'>{desc}</div>
                      </div>
                    ))}
                  </div>
                  <div className='text-xs text-red-400 bg-red-950 border border-red-800 rounded-lg p-3'>🛡 Security Veto: If Auditor detects attack probability &gt; 70%, auto-rejected regardless of other votes. (GNI-R-103)</div>
                </div>
              </section>
            )}
          </>
        )}
      </main>
      <footer className='border-t border-gray-800 mt-12'>
        <div className='max-w-7xl mx-auto px-6 py-4 text-center text-xs text-gray-600'>
          GNI — Global Nexus Insights | Keyword Intelligence Engine v3 | Team Geeks | SUM
        </div>
      </footer>
    </div>
  )
}
