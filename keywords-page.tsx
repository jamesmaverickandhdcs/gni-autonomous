'use client'

import { useEffect, useState } from 'react'

interface EmergingKeyword {
  id: string
  keyword: string
  frequency_count: number
  source_count: number
  example_context: string
  groq_definition: string
  pillar_suggestion: string
  status: string
  watching_days: number
  reemergence_count: number
  first_seen: string
  last_seen: string
}

const STATUS_CONFIG: Record<string, { label: string; color: string; bg: string; emoji: string }> = {
  candidate: { label: 'Candidate',  color: 'text-blue-300',   bg: 'bg-blue-900',   emoji: '🆕' },
  watching:  { label: 'Watching',   color: 'text-yellow-300', bg: 'bg-yellow-900', emoji: '⏳' },
  approved:  { label: 'Approved',   color: 'text-green-300',  bg: 'bg-green-900',  emoji: '✅' },
  rejected:  { label: 'Rejected',   color: 'text-red-300',    bg: 'bg-red-900',    emoji: '❌' },
}

const PILLAR_CONFIG: Record<string, { label: string; color: string; emoji: string }> = {
  geo:  { label: 'Geopolitical', color: 'text-emerald-400', emoji: '🌍' },
  fin:  { label: 'Financial',    color: 'text-blue-400',    emoji: '💰' },
  tech: { label: 'Technology',   color: 'text-purple-400',  emoji: '💻' },
}

export default function KeywordsPage() {
  const [keywords, setKeywords] = useState<EmergingKeyword[]>([])
  const [loading, setLoading] = useState(true)
  const [activeTab, setActiveTab] = useState<'trending' | 'approved' | 'watching'>('trending')
  const [pillarFilter, setPillarFilter] = useState<string>('all')

  useEffect(() => {
    fetch('/api/emerging-keywords')
      .then(r => r.json())
      .then(data => setKeywords(data.keywords || []))
      .catch(() => {})
      .finally(() => setLoading(false))
  }, [])

  const filtered = keywords.filter(kw => {
    if (activeTab === 'trending') return kw.status === 'candidate' || kw.status === 'watching'
    if (activeTab === 'approved') return kw.status === 'approved'
    if (activeTab === 'watching') return kw.status === 'watching'
    return true
  }).filter(kw => pillarFilter === 'all' || kw.pillar_suggestion === pillarFilter)
   .sort((a, b) => b.frequency_count - a.frequency_count)

  const counts = {
    candidate: keywords.filter(k => k.status === 'candidate').length,
    watching:  keywords.filter(k => k.status === 'watching').length,
    approved:  keywords.filter(k => k.status === 'approved').length,
    rejected:  keywords.filter(k => k.status === 'rejected').length,
  }

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-5xl mx-auto px-6 py-4">
          <div className="flex items-start justify-between gap-4">
            <div>
              <h1 className="text-2xl font-bold text-white">🔤 Emerging Intelligence Vocabulary</h1>
              <p className="text-sm text-gray-400">
                GNI continuously monitors {keywords.length} emerging terms across 25 intelligence sources.
              </p>
              <p className="text-xs text-gray-500 mt-1 max-w-2xl">
                New terms appearing frequently across multiple sources are flagged for review.
                Approved terms are added to GNI scoring keywords — strengthening future threat detection.
              </p>
            </div>
            <a href="/" className="text-sm text-blue-400 hover:text-blue-300 shrink-0">← Dashboard</a>
          </div>

          {/* Stats */}
          <div className="grid grid-cols-4 gap-3 mt-4">
            {[
              { label: 'Candidates', count: counts.candidate, color: 'bg-blue-950 border-blue-800 text-blue-400' },
              { label: 'Watching',   count: counts.watching,  color: 'bg-yellow-950 border-yellow-800 text-yellow-400' },
              { label: 'Approved',   count: counts.approved,  color: 'bg-green-950 border-green-800 text-green-400' },
              { label: 'Rejected',   count: counts.rejected,  color: 'bg-red-950 border-red-800 text-red-400' },
            ].map(s => (
              <div key={s.label} className={`border rounded-lg p-3 text-center ${s.color}`}>
                <div className="text-2xl font-bold">{s.count}</div>
                <div className="text-xs opacity-70">{s.label}</div>
              </div>
            ))}
          </div>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8">

        {/* Tabs + Pillar Filter */}
        <div className="flex items-center justify-between mb-6 flex-wrap gap-3">
          <div className="flex gap-2">
            {([
              { key: 'trending', label: '🆕 Trending', count: counts.candidate + counts.watching },
              { key: 'watching', label: '⏳ Watching', count: counts.watching },
              { key: 'approved', label: '✅ Approved', count: counts.approved },
            ] as const).map(tab => (
              <button key={tab.key} onClick={() => setActiveTab(tab.key)}
                className={`px-4 py-2 rounded-lg text-sm font-medium transition-colors ${
                  activeTab === tab.key ? 'bg-blue-600 text-white' : 'bg-gray-800 text-gray-400 hover:bg-gray-700'
                }`}>
                {tab.label} ({tab.count})
              </button>
            ))}
          </div>
          <div className="flex gap-2">
            {['all', 'geo', 'fin', 'tech'].map(p => (
              <button key={p} onClick={() => setPillarFilter(p)}
                className={`px-3 py-1.5 rounded-lg text-xs font-medium transition-colors ${
                  pillarFilter === p ? 'bg-gray-600 text-white' : 'bg-gray-800 text-gray-500 hover:bg-gray-700'
                }`}>
                {p === 'all' ? 'All Pillars' : PILLAR_CONFIG[p]?.emoji + ' ' + PILLAR_CONFIG[p]?.label}
              </button>
            ))}
          </div>
        </div>

        {loading && <div className="text-center py-20 text-gray-400">Loading keywords...</div>}

        {!loading && filtered.length === 0 && (
          <div className="text-center py-20 text-gray-400">
            <div className="text-4xl mb-4">🔤</div>
            <p>No keywords in this category yet.</p>
            <p className="text-xs mt-2">The sensor runs after every pipeline collection.</p>
          </div>
        )}

        <div className="space-y-4">
          {filtered.map(kw => {
            const status = STATUS_CONFIG[kw.status] || STATUS_CONFIG.candidate
            const pillar = PILLAR_CONFIG[kw.pillar_suggestion] || PILLAR_CONFIG.geo
            return (
              <div key={kw.id} className="bg-gray-900 border border-gray-700 rounded-xl p-5">
                <div className="flex items-start justify-between gap-4 mb-3">
                  <div className="flex items-center gap-3 flex-wrap">
                    <span className="text-lg font-bold text-white font-mono">"{kw.keyword}"</span>
                    <span className={`text-xs font-bold px-2 py-1 rounded-full ${status.bg} ${status.color}`}>
                      {status.emoji} {status.label}
                    </span>
                    <span className={`text-xs font-bold ${pillar.color}`}>
                      {pillar.emoji} {pillar.label}
                    </span>
                    {kw.reemergence_count > 0 && (
                      <span className="text-xs bg-orange-900 text-orange-300 px-2 py-1 rounded-full">
                        🔄 Re-emerged ×{kw.reemergence_count}
                      </span>
                    )}
                  </div>
                  <div className="flex items-center gap-3 shrink-0 text-xs text-gray-500">
                    <span>📊 {kw.frequency_count} articles</span>
                    <span>📡 {kw.source_count} sources</span>
                  </div>
                </div>

                {kw.status === 'watching' && kw.watching_days > 0 && (
                  <div className="mb-3 bg-yellow-950 border border-yellow-800 rounded-lg px-3 py-2">
                    <span className="text-xs text-yellow-400">
                      ⏳ Continuously trending for <strong>{kw.watching_days} days</strong> — pending admin decision
                    </span>
                  </div>
                )}

                {kw.groq_definition && (
                  <div className="mb-3">
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Definition</div>
                    <p className="text-sm text-gray-300 leading-relaxed">{kw.groq_definition}</p>
                  </div>
                )}

                {kw.example_context && (
                  <div className="mb-3">
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-1">Example Context</div>
                    <p className="text-xs text-gray-500 italic leading-relaxed line-clamp-2">{kw.example_context}</p>
                  </div>
                )}

                <div className="flex items-center gap-4 text-xs text-gray-600 mt-2">
                  <span>First seen: {new Date(kw.first_seen).toLocaleDateString()}</span>
                  <span>Last seen: {new Date(kw.last_seen).toLocaleDateString()}</span>
                </div>
              </div>
            )
          })}
        </div>

        {/* How it works */}
        <div className="mt-8 bg-gray-900 border border-gray-700 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">How Emerging Vocabulary Works</div>
          <div className="grid grid-cols-1 md:grid-cols-4 gap-4 text-xs">
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-blue-400 font-bold mb-1">1. Detection</div>
              <p className="text-gray-400">After every pipeline run, GNI scans all relevant articles for terms appearing 3+ times across 2+ sources that are not in the current keyword database.</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-purple-400 font-bold mb-1">2. Definition</div>
              <p className="text-gray-400">Groq AI explains what the new term means in real-world current usage, and suggests which intelligence pillar it belongs to.</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-yellow-400 font-bold mb-1">3. Admin Review</div>
              <p className="text-gray-400">Admin receives a Telegram alert with Approve / Watch / Reject buttons. Watching terms are monitored and re-alerted every 3 days.</p>
            </div>
            <div className="bg-gray-800 rounded-lg p-3">
              <div className="text-green-400 font-bold mb-1">4. Integration</div>
              <p className="text-gray-400">Approved terms are added to GNI scoring keywords — future articles containing these terms score higher in the intelligence funnel.</p>
            </div>
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-5xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights | Emerging Intelligence Vocabulary | Continuous learning from 25 sources
        </div>
      </footer>
    </div>
  )
}
