import os

# Create the debate page directory
os.makedirs('src/app/debate', exist_ok=True)

content = """\
'use client'

import { useEffect, useState } from 'react'

interface Report {
  id: string
  title: string
  summary: string
  sentiment: string
  mad_verdict: string
  mad_confidence: number
  mad_bull_case: string
  mad_bear_case: string
  mad_reasoning: string
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

export default function DebatePage() {
  const [reports, setReports] = useState<Report[]>([])
  const [selected, setSelected] = useState<Report | null>(null)
  const [loading, setLoading] = useState(true)

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

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">

      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">\U0001f402\U0001f43b MAD Protocol</h1>
              <p className="text-sm text-gray-400">Multi-Agent Debate \u2014 Bull vs Bear vs Arbitrator</p>
              <p className="text-xs text-gray-500 mt-1 max-w-2xl">
                Three independent AI agents analyse every report from opposing perspectives.
                The Bull Agent argues for market opportunity. The Bear Agent argues for risk and decline.
                The Arbitrator weighs both cases and delivers a final verdict with confidence score.
              </p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300 shrink-0 mt-1">
              \u2190 Dashboard
            </a>
          </div>

          {/* Verdict summary bar */}
          {reports.length > 0 && (
            <div className="grid grid-cols-3 gap-3 mt-4">
              <div className="bg-green-950 border border-green-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-green-400">{verdictCounts.bullish}</div>
                <div className="text-xs text-green-600">\U0001f402 Bullish verdicts</div>
              </div>
              <div className="bg-red-950 border border-red-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-red-400">{verdictCounts.bearish}</div>
                <div className="text-xs text-red-600">\U0001f43b Bearish verdicts</div>
              </div>
              <div className="bg-gray-800 border border-gray-700 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-gray-400">{reports.length}</div>
                <div className="text-xs text-gray-500">Total debates run</div>
              </div>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">

        {loading && (
          <div className="text-center py-20 text-gray-400">Loading debates...</div>
        )}

        {!loading && reports.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">\U0001f402\U0001f43b</div>
            <p>No MAD debates yet. Pipeline will generate debates on next run.</p>
          </div>
        )}

        {!loading && reports.length > 0 && (
          <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">

            {/* Sidebar — debate list */}
            <div className="lg:col-span-1">
              <div className="bg-gray-900 border border-gray-700 rounded-xl p-4">
                <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">
                  Debates ({reports.length})
                </div>
                <div className="space-y-2 max-h-[600px] overflow-y-auto">
                  {reports.map(r => {
                    const { pct, color } = confidenceBar(r.mad_confidence)
                    return (
                      <button
                        key={r.id}
                        onClick={() => setSelected(r)}
                        className={`w-full text-left p-3 rounded-lg text-xs transition-colors ${
                          selected?.id === r.id
                            ? 'bg-blue-600 text-white'
                            : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                        }`}
                      >
                        <div className="font-bold mb-1 line-clamp-2">{r.title}</div>
                        <div className="flex items-center justify-between">
                          <span className={`px-1.5 py-0.5 rounded text-xs font-bold ${
                            r.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300' :
                            r.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300' :
                            'bg-gray-700 text-gray-300'
                          }`}>
                            {r.mad_verdict?.toUpperCase()}
                          </span>
                          <span className="text-gray-500">{pct}%</span>
                        </div>
                        <div className="mt-1.5 bg-gray-700 rounded-full h-1">
                          <div className={`${color} h-1 rounded-full`} style={{ width: pct + '%' }} />
                        </div>
                        <div className="text-gray-600 mt-1">
                          {new Date(r.created_at).toLocaleDateString('en-US', {
                            month: 'short', day: 'numeric', hour: '2-digit', minute: '2-digit'
                          })}
                        </div>
                      </button>
                    )
                  })}
                </div>
              </div>
            </div>

            {/* Main — selected debate */}
            {selected && (
              <div className="lg:col-span-3 space-y-4">

                {/* Report context */}
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                  <div className="flex items-start justify-between gap-4 mb-3">
                    <h2 className="text-lg font-bold text-white">{selected.title}</h2>
                    <div className="flex items-center gap-2 shrink-0">
                      <span className={`text-xs font-bold px-2 py-1 rounded-full ${
                        selected.risk_level?.toLowerCase() === 'critical' ? 'bg-red-600 text-white' :
                        selected.risk_level?.toLowerCase() === 'high' ? 'bg-orange-500 text-white' :
                        'bg-gray-600 text-white'
                      }`}>
                        {selected.risk_level?.toUpperCase()}
                      </span>
                      {selected.escalation_score > 0 && (
                        <span className="text-xs font-bold px-2 py-1 rounded-full bg-red-900 border border-red-700 text-red-200">
                          \u26a1 {selected.escalation_score.toFixed(1)}/10
                        </span>
                      )}
                    </div>
                  </div>
                  <p className="text-gray-400 text-sm">{selected.summary}</p>
                  <div className="flex items-center gap-4 mt-3 text-xs text-gray-500">
                    <span>\U0001f4cd {selected.location_name || 'Global'}</span>
                    <span>{new Date(selected.created_at).toLocaleString()}</span>
                    {selected.tickers_affected?.slice(0, 3).map(t => (
                      <span key={t} className="font-mono text-blue-400">{t}</span>
                    ))}
                  </div>
                </div>

                {/* Verdict banner */}
                <div className={`border rounded-xl p-5 ${verdictColor(selected.mad_verdict)}`}>
                  <div className="flex items-center justify-between mb-3">
                    <div className="flex items-center gap-3">
                      <span className="text-3xl">
                        {selected.mad_verdict === 'bullish' ? '\U0001f402' : selected.mad_verdict === 'bearish' ? '\U0001f43b' : '\u2696\ufe0f'}
                      </span>
                      <div>
                        <div className="text-xl font-bold">
                          ARBITRATOR VERDICT: {selected.mad_verdict?.toUpperCase()}
                        </div>
                        <div className="text-sm opacity-75">
                          Confidence: {Math.round((selected.mad_confidence || 0) * 100)}%
                        </div>
                      </div>
                    </div>
                  </div>
                  {/* Confidence bar */}
                  <div className="bg-black bg-opacity-30 rounded-full h-3 mb-3">
                    <div
                      className={`h-3 rounded-full ${confidenceBar(selected.mad_confidence).color}`}
                      style={{ width: confidenceBar(selected.mad_confidence).pct + '%' }}
                    />
                  </div>
                  {selected.mad_reasoning && (
                    <div>
                      <div className="text-xs uppercase tracking-wider opacity-60 mb-1">
                        Arbitrator Reasoning
                      </div>
                      <p className="text-sm leading-relaxed opacity-90">{selected.mad_reasoning}</p>
                    </div>
                  )}
                </div>

                {/* Bull vs Bear */}
                <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                  <div className="bg-green-950 border border-green-800 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-2xl">\U0001f402</span>
                      <div>
                        <div className="text-sm font-bold text-green-400">Bull Agent</div>
                        <div className="text-xs text-green-700">Argues for opportunity</div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_bull_case}</p>
                  </div>

                  <div className="bg-red-950 border border-red-800 rounded-xl p-5">
                    <div className="flex items-center gap-2 mb-3">
                      <span className="text-2xl">\U0001f43b</span>
                      <div>
                        <div className="text-sm font-bold text-red-400">Bear Agent</div>
                        <div className="text-xs text-red-700">Argues for risk</div>
                      </div>
                    </div>
                    <p className="text-sm text-gray-300 leading-relaxed">{selected.mad_bear_case}</p>
                  </div>
                </div>

                {/* How MAD works */}
                <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                  <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">
                    How the MAD Protocol Works
                  </div>
                  <div className="grid grid-cols-1 md:grid-cols-3 gap-4 text-xs">
                    <div className="bg-gray-800 rounded-lg p-3">
                      <div className="text-green-400 font-bold mb-1">\U0001f402 Step 1: Bull Agent</div>
                      <p className="text-gray-400">Analyses the report and constructs the strongest possible bullish case. Identifies buying opportunities, positive catalysts, and upside scenarios.</p>
                    </div>
                    <div className="bg-gray-800 rounded-lg p-3">
                      <div className="text-red-400 font-bold mb-1">\U0001f43b Step 2: Bear Agent</div>
                      <p className="text-gray-400">Constructs the strongest possible bearish case. Identifies risks, negative catalysts, and downside scenarios independently of the Bull Agent.</p>
                    </div>
                    <div className="bg-gray-800 rounded-lg p-3">
                      <div className="text-blue-400 font-bold mb-1">\u2696\ufe0f Step 3: Arbitrator</div>
                      <p className="text-gray-400">Reads both cases without knowing which agent wrote which. Weighs the evidence and delivers a final verdict with confidence score.</p>
                    </div>
                  </div>
                </div>

              </div>
            )}
          </div>
        )}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI \u2014 Global Nexus Insights (Autonomous) | MAD Protocol \u2014 Multi-Agent Debate | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
"""

# Post-process emoji escapes
content = (content
    .replace('\\U0001f402\\U0001f43b', '\U0001f402\U0001f43b')
    .replace('\\U0001f402', '\U0001f402')
    .replace('\\U0001f43b', '\U0001f43b')
    .replace('\\u2014', '\u2014')
    .replace('\\u2190', '\u2190')
    .replace('\\u26a1', '\u26a1')
    .replace('\\U0001f4cd', '\U0001f4cd')
    .replace('\\u2696\\ufe0f', '\u2696\ufe0f')
    .replace('\\u2014', '\u2014')
)

with open('src/app/debate/page.tsx', 'w', encoding='utf-8', newline='\n') as f:
    f.write(content)

# Verify
c = open('src/app/debate/page.tsx', encoding='utf-8').read()
print('Debate page created:', len(c), 'chars')
print('Bull emoji:', '\U0001f402' in c)
print('Bear emoji:', '\U0001f43b' in c)
print('MAD Protocol title:', 'MAD Protocol' in c)
print('Arbitrator section:', 'Arbitrator' in c)
print('How MAD works:', 'How the MAD Protocol Works' in c)
