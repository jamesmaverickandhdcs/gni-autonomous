'use client'
import { useState } from 'react'

const ENDPOINTS = [
  { method: 'GET', path: '/api/reports', desc: 'Latest intelligence reports + historical baseline', group: 'Core' },
  { method: 'GET', path: '/api/latest', desc: 'Single call = complete GNI state (report + MAD + pillars + quota)', group: 'Core' },
  { method: 'GET', path: '/api/status', desc: 'Pipeline health check for external monitoring', group: 'Core' },
  { method: 'GET', path: '/api/pillar-reports', desc: 'GEO / TECH / FIN pillar intelligence reports', group: 'Core' },
  { method: 'GET', path: '/api/quota', desc: 'Live token usage vs 85K safe ceiling vs 100K limit', group: 'System' },
  { method: 'GET', path: '/api/health', desc: 'Pipeline status + quality scores per run', group: 'System' },
  { method: 'GET', path: '/api/source-health', desc: '25 RSS sources: healthy / degraded / down', group: 'System' },
  { method: 'GET', path: '/api/alerts', desc: 'Alert archive: CRITICAL / NYSE / ADAPTIVE / SOURCE_DOWN', group: 'System' },
  { method: 'GET', path: '/api/adaptive-log', desc: 'Self-healing log: when triggered, why, tokens used', group: 'System' },
  { method: 'GET', path: '/api/predictions-list', desc: 'All MAD predictions + verify dates + accuracy scores', group: 'Intelligence' },
  { method: 'GET', path: '/api/correlations', desc: '3-horizon CFA (7d/30d/180d) + per-agent accuracy', group: 'Intelligence' },
  { method: 'GET', path: '/api/stocks', desc: 'Yahoo Finance data: price + day change + chart data', group: 'Intelligence' },
  { method: 'GET', path: '/api/article-events', desc: 'Geo-tagged articles for map view', group: 'Intelligence' },
  { method: 'GET', path: '/api/pipeline-runs', desc: 'Pipeline run history + funnel stats', group: 'Pipeline' },
  { method: 'GET', path: '/api/pipeline-articles', desc: 'Articles per run with stage scores', group: 'Pipeline' },
  { method: 'GET', path: '/api/source-weights', desc: 'Dynamic source trust weights (GPVS-adjusted)', group: 'Pipeline' },
  { method: 'GET', path: '/api/prediction-outcomes', desc: 'GPVS scorecard: accuracy % per horizon', group: 'Pipeline' },
  { method: 'GET', path: '/api/export/reports?format=csv&days=30', desc: 'Download reports as CSV (IEEE paper replication)', group: 'Export' },
  { method: 'GET', path: '/api/export/predictions?format=csv', desc: 'Download all MAD predictions as CSV', group: 'Export' },
  { method: 'GET', path: '/api/export/articles?format=csv', desc: 'Download pipeline articles as CSV', group: 'Export' },
  { method: 'GET', path: '/api/audit-trail', desc: 'Security injection detection audit log', group: 'Security' },
]

const SCHEMA = [
  { table: 'reports', desc: 'Core intelligence reports', cols: 'id, title, summary, sentiment, sentiment_score, sentiment_score_lower, sentiment_score_upper, confidence_interval_width, analysis_runs, risk_level, escalation_score, escalation_level, mad_verdict, mad_confidence, mad_action_recommendation, mad_bull_case, mad_bear_case, mad_blind_spot, tickers_affected, location_name, lat, lng, llm_source, plain_narrative, deception_level, created_at' },
  { table: 'debate_predictions', desc: 'MAD agent predictions + GPVS verification', cols: 'id, report_id, agent_name, direction, confidence, verify_date, accuracy_score, created_at' },
  { table: 'pillar_reports', desc: 'GEO / TECH / FIN domain reports', cols: 'id, pillar, title, summary, sentiment, sentiment_score, risk_level, tickers_affected, market_impact, weakness_identified, quality_score, created_at' },
  { table: 'groq_daily_usage', desc: 'Token usage per pipeline run', cols: 'id, pipeline_type, tokens_used, model_used, created_at' },
  { table: 'pipeline_articles', desc: 'Articles processed per run with stage scores', cols: 'id, run_id, source, title, url, summary, stage3_score, stage4_rank, stage4_selected, created_at' },
  { table: 'source_health', desc: 'RSS source reliability tracking', cols: 'id, source, status, last_checked, articles_fetched, created_at' },
  { table: 'source_weights', desc: 'Dynamic trust weights (GPVS-adjusted)', cols: 'id, source, weight, gpvs_contribution, last_updated' },
]

const GROUPS = ['Core', 'System', 'Intelligence', 'Pipeline', 'Export', 'Security']
const GROUP_COLORS: Record<string, string> = {
  Core: 'bg-blue-900 text-blue-300 border-blue-700',
  System: 'bg-purple-900 text-purple-300 border-purple-700',
  Intelligence: 'bg-green-900 text-green-300 border-green-700',
  Pipeline: 'bg-amber-900 text-amber-300 border-amber-700',
  Export: 'bg-teal-900 text-teal-300 border-teal-700',
  Security: 'bg-red-900 text-red-300 border-red-700',
}

export default function DeveloperPage() {
  const [activeGroup, setActiveGroup] = useState('Core')
  const [activeTab, setActiveTab] = useState<'endpoints'|'schema'|'examples'|'fork'>('endpoints')

  const filtered = ENDPOINTS.filter(e => e.group === activeGroup)

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/developer-hub" className="inline-flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors mb-3">← Dev Console</a>
          <div className="flex items-center justify-between mb-3">
            <div>
              <h1 className="text-xl font-bold text-white">🧠 Developer Portal</h1>
              <p className="text-xs text-gray-400">GNI_Autonomous API Reference | Build on top of GNI | Fork guide | $0.00/month architecture</p>
            </div>
            <a href="/" className="text-xs text-blue-400 border border-blue-800 hover:border-blue-500 rounded px-3 py-1 transition-colors">
              ← Quantum Strategist
            </a>
          </div>
          <div className="flex flex-wrap gap-2">
            <a href="/researcher" className="flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 rounded-lg px-3 py-1.5 text-xs font-bold text-green-200 transition-colors">
              📊 Pattern Intelligence
            </a>
            <a href="/developer-hub" className="flex items-center gap-1.5 bg-purple-900 hover:bg-purple-700 border border-purple-700 rounded-lg px-3 py-1.5 text-xs font-bold text-purple-200 transition-colors">
              🧠 Dev Console
            </a>
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
            <a href="/about" className="flex items-center gap-1.5 bg-gray-800 hover:bg-gray-700 border border-gray-600 rounded-lg px-3 py-1.5 text-xs font-bold text-gray-200 transition-colors">
              🌟 About
            </a>
          </div>
        </div>
      </header>

      <div className="max-w-6xl mx-auto px-6 py-6">

        {/* Cost + Autonomy Banner */}
        <div className="grid grid-cols-3 gap-4 mb-6">
          <div className="bg-green-950 border border-green-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-green-300">$0.00</div>
            <div className="text-xs text-gray-500 mt-1">Monthly Cost (forever)</div>
          </div>
          <div className="bg-blue-950 border border-blue-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-blue-300">L7</div>
            <div className="text-xs text-gray-500 mt-1">Autonomy Level</div>
          </div>
          <div className="bg-purple-950 border border-purple-800 rounded-xl p-4 text-center">
            <div className="text-2xl font-bold text-purple-300">21</div>
            <div className="text-xs text-gray-500 mt-1">API Endpoints</div>
          </div>
        </div>

        {/* Tab Navigation */}
        <div className="flex gap-2 mb-6 border-b border-gray-800 pb-3">
          {(['endpoints', 'schema', 'examples', 'fork'] as const).map(tab => (
            <button
              key={tab}
              onClick={() => setActiveTab(tab)}
              className={`px-4 py-2 rounded-lg text-xs font-bold transition-colors capitalize ${
                activeTab === tab ? 'bg-blue-700 text-white' : 'bg-gray-900 text-gray-400 hover:text-white'
              }`}
            >
              {tab === 'endpoints' ? '📡 Endpoints' : tab === 'schema' ? '🗄️ Schema' : tab === 'examples' ? '💻 Code Examples' : '🍴 Fork Guide'}
            </button>
          ))}
        </div>

        {/* ENDPOINTS TAB */}
        {activeTab === 'endpoints' && (
          <div>
            <div className="flex gap-2 mb-4 flex-wrap">
              {GROUPS.map(g => (
                <button
                  key={g}
                  onClick={() => setActiveGroup(g)}
                  className={`px-3 py-1.5 rounded-lg text-xs font-bold border transition-colors ${
                    activeGroup === g ? GROUP_COLORS[g] : 'bg-gray-900 border-gray-700 text-gray-400 hover:text-white'
                  }`}
                >
                  {g}
                </button>
              ))}
            </div>
            <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
              <div className="grid grid-cols-12 px-4 py-2 border-b border-gray-800 text-xs text-gray-500 uppercase tracking-wider">
                <div className="col-span-1">Method</div>
                <div className="col-span-5">Endpoint</div>
                <div className="col-span-6">Description</div>
              </div>
              {filtered.map(({ method, path, desc }) => (
                <div key={path} className="grid grid-cols-12 px-4 py-3 border-b border-gray-800 hover:bg-gray-800 transition-colors items-center">
                  <div className="col-span-1">
                    <span className="text-xs font-bold bg-green-900 text-green-300 px-2 py-0.5 rounded font-mono">{method}</span>
                  </div>
                  <div className="col-span-5">
                    <span className="font-mono text-xs text-blue-300 break-all">{path}</span>
                  </div>
                  <div className="col-span-6 text-xs text-gray-400">{desc}</div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* SCHEMA TAB */}
        {activeTab === 'schema' && (
          <div className="space-y-4">
            {SCHEMA.map(({ table, desc, cols }) => (
              <div key={table} className="bg-gray-900 border border-gray-700 rounded-xl p-4">
                <div className="flex items-center gap-3 mb-2">
                  <span className="font-mono text-sm font-bold text-purple-300">{table}</span>
                  <span className="text-xs text-gray-500">{desc}</span>
                </div>
                <div className="bg-gray-800 rounded-lg p-3 font-mono text-xs text-gray-400 leading-relaxed">
                  {cols}
                </div>
              </div>
            ))}
          </div>
        )}

        {/* CODE EXAMPLES TAB */}
        {activeTab === 'examples' && (
          <div className="space-y-6">
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
              <div className="text-sm font-bold text-white mb-3">🐍 Python -- Get Latest GNI State</div>
              <pre className="bg-gray-800 rounded-lg p-4 text-xs text-green-300 overflow-x-auto leading-relaxed">{`import requests

BASE = "https://gni-autonomous.vercel.app"

# Get complete GNI state in one call
state = requests.get(f"{BASE}/api/latest").json()
report = state["gni_state"]["report"]
print(f"Verdict: {report['mad_verdict']} ({report['mad_confidence']*100:.0f}%)")
print(f"Escalation: {report['escalation_level']} {report['escalation_score']}/10")
print(f"Action: {report['mad_action_recommendation']}")

# Check pipeline health
status = requests.get(f"{BASE}/api/status").json()
print(f"Sources healthy: {status['sources']['healthy']}/{status['sources']['total']}")
print(f"Quota used: {status['quota']['percent_used']}%")`}</pre>
            </div>

            <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
              <div className="text-sm font-bold text-white mb-3">💻 JavaScript -- Download Dataset</div>
              <pre className="bg-gray-800 rounded-lg p-4 text-xs text-blue-300 overflow-x-auto leading-relaxed">{`const BASE = "https://gni-autonomous.vercel.app";

// Download last 30 days of reports as CSV
const res = await fetch(\`\${BASE}/api/export/reports?format=csv&days=30\`);
const csv = await res.text();
console.log(csv.split("\n").length + " rows exported");

// Get all predictions as JSON
const preds = await fetch(\`\${BASE}/api/export/predictions\`).then(r => r.json());
console.log(\`\${preds.count} predictions total\`);

// Monitor GNI status
const status = await fetch(\`\${BASE}/api/status\`).then(r => r.json());
if (status.quota.status === "safe") {
  console.log("GNI is healthy, quota safe");
}`}</pre>
            </div>

            <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
              <div className="text-sm font-bold text-white mb-3">📊 Python -- IEEE Paper Data Export</div>
              <pre className="bg-gray-800 rounded-lg p-4 text-xs text-yellow-300 overflow-x-auto leading-relaxed">{`import requests, csv, io

BASE = "https://gni-autonomous.vercel.app"

# Export full dataset for replication study
reports_csv = requests.get(f"{BASE}/api/export/reports?format=csv&days=90").text
predictions_csv = requests.get(f"{BASE}/api/export/predictions?format=csv").text

# Parse and analyze
reader = csv.DictReader(io.StringIO(reports_csv))
reports = list(reader)
print(f"Exported {len(reports)} reports for IEEE paper analysis")

# Calculate mean escalation
scores = [float(r["escalation_score"]) for r in reports if r["escalation_score"]]
print(f"Mean escalation: {sum(scores)/len(scores):.2f}")`}</pre>
            </div>
          </div>
        )}

        {/* FORK GUIDE TAB */}
        {activeTab === 'fork' && (
          <div className="space-y-4">
            <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
              <div className="text-sm font-bold text-white mb-4">🍴 Fork GNI_Autonomous in 5 Steps</div>
              <div className="space-y-3">
                {[
                  { step: '1', title: 'Fork the repo', desc: 'github.com/jamesmaverickandhdcs/gni-autonomous -- click Fork. It is PUBLIC.' },
                  { step: '2', title: 'Create Supabase project', desc: 'Free tier. Create tables: reports, debate_predictions, pillar_reports, groq_daily_usage, pipeline_articles, source_health, source_weights. See /developer schema tab for columns.' },
                  { step: '3', title: 'Get a Groq API key', desc: 'console.groq.com -- free tier gives 100K tokens/day. Add as GROQ_API_KEY in GitHub repo secrets.' },
                  { step: '4', title: 'Add environment variables', desc: 'In GitHub repo Settings > Secrets: GROQ_API_KEY, SUPABASE_URL, SUPABASE_ANON_KEY, SUPABASE_SERVICE_ROLE_KEY, TELEGRAM_BOT_TOKEN (optional).' },
                  { step: '5', title: 'Deploy to Vercel', desc: 'Connect your forked repo to Vercel. Add same env vars in Vercel dashboard. Deploy. Done -- $0.00/month.' },
                ].map(({ step, title, desc }) => (
                  <div key={step} className="flex gap-4 bg-gray-800 rounded-lg p-4">
                    <div className="text-2xl font-bold text-blue-400 shrink-0 w-8">{step}</div>
                    <div>
                      <div className="text-sm font-bold text-white mb-1">{title}</div>
                      <div className="text-xs text-gray-400 leading-relaxed">{desc}</div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            <div className="bg-yellow-950 border border-yellow-800 rounded-xl p-4">
              <div className="text-xs text-yellow-400 font-bold mb-2">⚠️ Important Notes</div>
              <ul className="text-xs text-gray-400 space-y-1 leading-relaxed">
                <li>-- Use a SEPARATE Groq account if running multiple projects (quota isolation)</li>
                <li>-- Sacred crons (02:00+10:00 UTC) may fire 2-3 hours late on free tier -- this is normal</li>
                <li>-- requirements.txt is DELETED -- all pipelines use inline pip install</li>
                <li>-- Monthly cost is $0.00 using Groq free tier + Supabase free + Vercel free + GitHub free</li>
                <li>-- Author anonymous -- Team Geeks only. Do not add individual names to commits or code.</li>
              </ul>
            </div>
          </div>
        )}

      </div>

      <footer className="border-t border-gray-800 mt-8">
        <div className="max-w-6xl mx-auto px-4 py-4 text-center text-xs text-gray-600">
          GNI Autonomous | Developer Portal | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}
