'use client'

export default function MethodologyPage() {
  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <a href="/researcher" className="inline-flex items-center gap-1.5 bg-green-900 hover:bg-green-700 border border-green-700 text-green-200 rounded-lg px-3 py-1.5 text-xs font-bold transition-colors shrink-0">← Pattern Intelligence</a>
          <div className="flex items-center justify-between mt-2">
          <div>
            <h1 className="text-2xl font-bold text-white">&#x1F4D0; Methodology</h1>
            <p className="text-sm text-gray-400">How GNI_Autonomous works — full technical methodology</p>
          </div>
          <a href="/" className="text-sm text-blue-400 hover:text-blue-300">&larr; Dashboard</a>
        
          {/* Cross-Navigation -- 4 main pages (GNI-R-140) */}
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
            <a href="/reports" className="flex items-center gap-1.5 bg-amber-900 hover:bg-amber-700 border border-amber-700 rounded-lg px-3 py-1.5 text-xs font-bold text-amber-200 transition-colors">
              🎯 Feedback Loop
            </a>
          </div>
</div>
          </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-8">

        {/* Pipeline Overview */}
        <section>
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Pipeline Architecture</div>
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
            <div className="text-sm text-gray-300 leading-relaxed mb-4">
              GNI_Autonomous runs 4 autonomous pipelines via GitHub Actions cron jobs. No human intervention required.
              Every day it collects global news, analyzes it with AI, produces sentiment reports with 95% confidence intervals,
              runs a 4-agent multi-perspective debate, and publishes everything to this live web app.
            </div>
            <div className="space-y-3">
              {[
                { pipeline: 'gni_pipeline', cron: '02:00 + 10:00 UTC', tokens: '~6,175/run', desc: 'RSS collection → intelligence funnel → AI analysis → CI → pillar reports → save → verify' },
                { pipeline: 'gni_mad', cron: '02:30 + 10:30 UTC', tokens: '~12,393/run', desc: '4-agent debate (Bull/Bear/Black Swan/Ostrich) → 3 rounds → Arbitrator → verdict → predictions' },
                { pipeline: 'gni_heartbeat', cron: 'Every 30 min', tokens: '0 (zero)', desc: 'Monitor escalation delta → trigger adaptive → NYSE alerts → divergence detection' },
                { pipeline: 'gni_adaptive', cron: 'On trigger', tokens: '0–12,393', desc: 'Fresh analysis when escalation spikes — CRITICAL=0 Groq, HIGH=4 calls, LOW=19 calls' },
              ].map(p => (
                <div key={p.pipeline} className="bg-gray-800 rounded-lg p-4">
                  <div className="flex items-center justify-between mb-1">
                    <span className="font-mono font-bold text-blue-400 text-sm">{p.pipeline}</span>
                    <div className="flex gap-3 text-xs">
                      <span className="text-gray-500">{p.cron}</span>
                      <span className="text-orange-400">{p.tokens}</span>
                    </div>
                  </div>
                  <div className="text-xs text-gray-400">{p.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Stage by stage */}
        <section>
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Pipeline Stages — Step by Step</div>
          <div className="space-y-3">
            {[
              { stage: 'Step 0', title: 'Quota Guard Pre-flight', desc: 'Reads groq_daily_usage → sums today\'s tokens → checks against 85K safe ceiling. If insufficient headroom: EXIT with Telegram alert. Sacred runs (02:00+10:00 UTC) always permitted.' },
              { stage: 'Stage 1a', title: 'RSS Collection', desc: 'Fetches up to 20 articles per RSS source from 25+ global news feeds. Target: 400+ raw articles per run. All saved to pipeline_articles table.' },
              { stage: 'Stage 1b', title: 'Injection Detection', desc: '66 prompt injection patterns scanned across 7 layers: Unicode norm, source credibility, context boundary, NER, Groq hardened JSON, output sanitization, audit trail. Flagged articles written to audit_trail table.' },
              { stage: 'Stage 2', title: 'Deduplication', desc: 'MD5 hash of first 6 title words. Articles with same hash within 6 hours are deduplicated. Prevents duplicate reporting on same event.' },
              { stage: 'Stage 3', title: 'Intelligence Funnel', desc: 'Each article scored on geopolitical significance (0-20). Top N articles selected with source diversity enforced (max 3 per source). Pillar routing: geo/tech/fin tags assigned.' },
              { stage: 'Stage 4a', title: 'Primary Analysis + CI', desc: 'Groq llama-3.3-70b-versatile analyzes top articles. 3 independent runs at temperatures 0.1, 0.3, 0.7 generate 95% confidence intervals using t-distribution (t=4.303 for n=3).' },
              { stage: 'Stage 4b', title: 'Three Pillar Reports', desc: 'Three separate AI analyses for Geopolitical, Technology, Financial domains. Same top articles, domain-specific prompts. Runs after 120s rate limit reset.' },
              { stage: 'Stage 5', title: 'Save + Telegram', desc: 'Report saved to Supabase reports table with SHA-256 audit chain. Telegram notification sent with escalation level, sentiment, and MAD verdict.' },
              { stage: 'Stage 6', title: 'GPVS Verify', desc: 'After verify_date passes, actual SPY market movement compared to prediction direction. Accuracy logged. Source weights updated via EMA: correct=weight×1.1, wrong=weight×0.9.' },
            ].map((s, i) => (
              <div key={s.stage} className={`border rounded-xl p-4 ${i % 2 === 0 ? 'border-gray-700 bg-gray-900' : 'border-gray-800 bg-gray-900'}`}>
                <div className="flex items-start gap-4">
                  <div className="text-xs font-mono font-bold text-blue-400 w-20 shrink-0 mt-0.5">{s.stage}</div>
                  <div>
                    <div className="text-sm font-bold text-white mb-1">{s.title}</div>
                    <div className="text-xs text-gray-400 leading-relaxed">{s.desc}</div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        </section>

        {/* MAD Protocol detail */}
        <section>
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Quadratic MAD Protocol — Novel Contribution #1</div>
          <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
            <div className="text-xs text-gray-400 leading-relaxed mb-4">
              The MAD (Multi-Agent Debate) protocol applies the Johari Window framework to geopolitical intelligence.
              Four agents represent four quadrants: Bull (Known Positives), Bear (Known Negatives),
              Black Swan (Unknown Negatives), Ostrich (Ignored Realities).
              After 3 rounds of debate with Arbitrator coaching, a BULLISH/BEARISH/NEUTRAL verdict is reached with confidence score.
            </div>
            <div className="grid grid-cols-2 gap-3">
              {[
                { agent: '&#x1F402; Bull', quad: 'Known + Proactive', desc: 'Identifies opportunity costs of inaction. What positive outcomes are being missed?', color: 'bg-green-950 border-green-800 text-green-400' },
                { agent: '&#x1F43B; Bear', quad: 'Known + Ignored', desc: 'Finds systemic failures and fragile systems. What known risks are being dismissed?', color: 'bg-red-950 border-red-800 text-red-400' },
                { agent: '&#x1F9A2; Black Swan', quad: 'Unknown + Negative', desc: 'Uncovers hidden dangers from low-scoring articles. What could catch everyone off guard?', color: 'bg-blue-950 border-blue-800 text-blue-400' },
                { agent: '&#x1F9A6; Ostrich', quad: 'Unknown + Ignored', desc: 'Exposes what institutions are in denial about. What threat is everyone pretending does not exist?', color: 'bg-yellow-950 border-yellow-800 text-yellow-400' },
              ].map(a => (
                <div key={a.agent} className={`border rounded-lg p-3 ${a.color}`}>
                  <div className="text-sm font-bold mb-1" dangerouslySetInnerHTML={{ __html: a.agent }} />
                  <div className="text-xs opacity-75 mb-2">{a.quad}</div>
                  <div className="text-xs text-gray-300 leading-relaxed">{a.desc}</div>
                </div>
              ))}
            </div>
          </div>
        </section>

        {/* Tech stack */}
        <section>
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">Technology Stack</div>
          <div className="bg-gray-900 border border-gray-700 rounded-xl overflow-hidden">
            {[
              ['Python 3.10+', 'Pipeline scripts', 'main.py, mad_runner.py, monitoring_pipeline.py, adaptive_pipeline.py'],
              ['Next.js 14 + TypeScript', 'Web app + API routes', '33 pages live on Vercel'],
              ['Groq API', 'LLM inference', 'llama-3.3-70b-versatile — 100K tokens/day free'],
              ['Supabase', 'PostgreSQL database', '15 tables — reports, predictions, audit_trail, groq_daily_usage...'],
              ['GitHub Actions', 'Cron + CI/CD', '4 workflows — gni_pipeline, gni_mad, gni_heartbeat, gni_adaptive'],
              ['Telegram Bot API', 'Alert notifications', 'Sacred completion, CRITICAL escalation, NYSE alerts, divergence'],
              ['Vercel', 'Deployment + CDN', 'Auto-deploy on git push to main'],
            ].map(([tech, role, detail], i) => (
              <div key={tech} className={`grid grid-cols-3 gap-2 px-4 py-3 border-b border-gray-800 text-xs ${i % 2 === 0 ? '' : 'bg-gray-800 bg-opacity-50'}`}>
                <div className="font-bold text-blue-400 font-mono">{tech}</div>
                <div className="text-gray-300">{role}</div>
                <div className="text-gray-500">{detail}</div>
              </div>
            ))}
          </div>
        </section>

      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI Methodology | Team Geeks | Higher Diploma in Computer Science | Spring University Myanmar (SUM)
        </div>
      </footer>
    </div>
  )
}