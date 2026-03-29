export default function AboutPage() {
  const infra = [
    { name: 'Groq API (Llama 3)', role: 'Cloud AI — free tier, 100K tokens/day', cost: '$0.00' },
    { name: 'Groq API', role: 'Cloud AI fallback — free tier (public repo)', cost: '$0.00' },
    { name: 'Supabase', role: 'Database — free tier (500MB)', cost: '$0.00' },
    { name: 'Vercel', role: 'Web hosting — free tier (100GB bandwidth)', cost: '$0.00' },
    { name: 'GitHub Actions', role: 'CI/CD pipeline — unlimited free (public repo)', cost: '$0.00' },
    { name: 'Telegram Bot API', role: 'CRITICAL alerts — free', cost: '$0.00' },
  ]

  const timeline = [
    { level: 'L4', day: 'Day 7',  label: 'Diploma baseline',  desc: '5 RSS sources · 92 articles · basic AI report · map · stocks · transparency' },
    { level: 'L5', day: 'Day 10', label: 'GPVS + Quality',    desc: 'Prediction validation · quality scoring · source weights · escalation · 13 RSS sources · 242 articles' },
    { level: 'L6', day: 'Day 13', label: 'Self-improving',    desc: 'Prompt A/B testing · source credibility learning · historical correlation · weekly digest' },
    { level: 'L7', day: 'Day 17', label: 'Fully autonomous',  desc: 'MAD Protocol · deception detection · frequency controller · health agent · audit trail · self-healing' },
  ]

  const stats = [
    { label: 'Pipeline runs',     value: '30+' },
    { label: 'Articles analysed', value: '7,000+' },
    { label: 'Reports generated', value: '30+' },
    { label: 'GPVS accuracy',     value: '100%' },
    { label: 'Injection patterns',value: '66' },
    { label: 'Sprint days',       value: '17' },
  ]

  const comparisons = [
    { name: 'Bloomberg Terminal',    cost: '$31,980/yr', note: 'Single seat — 2026 verified price' },
    { name: 'Stratfor Worldview',    cost: '$199/yr',    note: 'Individual subscription' },
    { name: 'Oxford Analytica',      cost: 'On Request', note: 'Enterprise custom quote — no public price' },
    { name: 'Human Analyst',         cost: '$82,429–$104,177/yr', note: 'Geopolitical intelligence analyst — US average 2026' },
    { name: 'GNI_Autonomous',        cost: '$0.00/yr',  note: 'Open. Free. Always.' },
  ]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-6xl mx-auto px-6 py-4">
          <div>
            <h1 className="text-2xl font-bold text-white">🌐 About GNI</h1>
            <p className="text-sm text-gray-400">Global Nexus Insights (Autonomous) — The $0.00/month intelligence platform</p>
          </div>
          
        
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
              🔄 Feedback Loop
            </a>
          </div>
</div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8 space-y-8">

        {/* $0 Hero */}
        <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 text-center">
          <div className="text-8xl font-bold text-green-400 mb-2">$0.00</div>
          <div className="text-xl text-gray-300 mb-1">per month</div>
          <div className="text-sm text-gray-500">Production-grade autonomous AI intelligence. Forever free.</div>
        </div>

        {/* Intelligence cost comparison */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Intelligence Cost Comparison</div>
          <div className="space-y-2">
            {comparisons.map(item => (
              <div key={item.name} className={`flex items-center justify-between rounded-lg px-4 py-3 ${item.name === 'GNI_Autonomous' ? 'bg-green-950 border border-green-800' : 'bg-gray-800'}`}>
                <div>
                  <div className="text-sm font-bold text-white">{item.name}</div>
                  <div className="text-xs text-gray-500">{item.note}</div>
                </div>
                <div className={`text-lg font-bold ${item.name === 'GNI_Autonomous' ? 'text-green-400' : 'text-red-400'}`}>
                  {item.cost}
                </div>
              </div>
            ))}
          </div>
          <div className="mt-3 text-xs text-gray-600 text-center">
            Bloomberg Terminal has grown 60% since 2010 ($20,000 → $31,980). The cost barrier widens every year.
          </div>
        </div>

        {/* Infrastructure cost table */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Infrastructure Cost Breakdown</div>
          <div className="space-y-2">
            {infra.map(item => (
              <div key={item.name} className="flex items-center justify-between bg-gray-800 rounded-lg px-4 py-3">
                <div>
                  <div className="text-sm font-bold text-white">{item.name}</div>
                  <div className="text-xs text-gray-500">{item.role}</div>
                </div>
                <div className="text-lg font-bold text-green-400">{item.cost}</div>
              </div>
            ))}
            <div className="flex items-center justify-between bg-green-950 border border-green-800 rounded-lg px-4 py-3">
              <div className="text-sm font-bold text-green-300">Total monthly cost</div>
              <div className="text-2xl font-bold text-green-400">$0.00</div>
            </div>
          </div>
          <div className="mt-3 text-xs text-gray-600 text-center">
            GitHub Actions: unlimited free minutes for public repositories. Myanmar internet penetration: 61.1% (DataReportal 2025).
          </div>
        </div>

        {/* Sprint Stats */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Sprint Statistics</div>
          <div className="grid grid-cols-3 md:grid-cols-6 gap-3">
            {stats.map(s => (
              <div key={s.label} className="bg-gray-800 rounded-lg p-3 text-center">
                <div className="text-2xl font-bold text-white">{s.value}</div>
                <div className="text-xs text-gray-500 mt-1">{s.label}</div>
              </div>
            ))}
          </div>
        </div>

        {/* L4 to L7 Journey */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">
            The Journey — L4 → L7 in 17 Days
          </div>
          <div className="space-y-3">
            {timeline.map(item => (
              <div key={item.level} className="flex items-start gap-4 bg-gray-800 rounded-lg p-4">
                <div className="bg-blue-900 border border-blue-700 rounded-lg px-3 py-2 text-center shrink-0">
                  <div className="text-lg font-bold text-blue-400">{item.level}</div>
                  <div className="text-xs text-gray-500">{item.day}</div>
                </div>
                <div>
                  <div className="text-sm font-bold text-white mb-1">{item.label}</div>
                  <div className="text-xs text-gray-400">{item.desc}</div>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* The Dream */}
        <div className="bg-gray-900 border border-yellow-800 rounded-2xl p-6">
          <div className="text-xs text-yellow-600 uppercase tracking-wider mb-3">🌟 The Dream</div>
          <p className="text-gray-300 text-sm leading-relaxed mb-3">
            Intelligence should not be a privilege. It should be a right.
          </p>
          <p className="text-gray-400 text-sm leading-relaxed mb-3">
            GNI_Autonomous was built to prove that industrial-grade AI intelligence can run for $0.00 per month,
            accessible to anyone in the world — including people in Myanmar
            where 61.1% of the population now has internet access (DataReportal 2025) but where even a
            $199/year subscription would represent 18% of average annual income.
          </p>
          <p className="text-gray-400 text-sm leading-relaxed mb-4">
            Built as a Higher Diploma final project at Spring University Myanmar (SUM).
            The goal was never just to pass an exam. The goal was to build something real,
            something that keeps running after the exam is over, something that serves people.
          </p>
          <div className="grid grid-cols-3 gap-3 mt-4">
            <div className="bg-gray-800 rounded-lg p-3 text-center">
              <div className="text-sm font-bold text-yellow-400">Always Free</div>
              <div className="text-xs text-gray-500">$0.00/month forever</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3 text-center">
              <div className="text-sm font-bold text-yellow-400">Always On</div>
              <div className="text-xs text-gray-500">Self-healing 24/7</div>
            </div>
            <div className="bg-gray-800 rounded-lg p-3 text-center">
              <div className="text-sm font-bold text-yellow-400">For Everyone</div>
              <div className="text-xs text-gray-500">No login required</div>
            </div>
          </div>
        </div>

        {/* Built by — anonymous per project policy */}
        <div className="bg-gray-900 border border-gray-800 rounded-xl p-5 text-center">
          <div className="text-xs text-gray-500 mb-2">Built by</div>
          <div className="text-lg font-bold text-white">Team Geeks</div>
          <div className="text-sm text-gray-400">Higher Diploma in Computer Science</div>
          <div className="text-sm text-gray-500">Spring University Myanmar (SUM) · 2026</div>
          <div className="mt-3 text-xs text-gray-600">
            Pipeline runs autonomously via GitHub Actions (public repo — unlimited free minutes) · gni-autonomous.vercel.app
          </div>
        </div>

      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-6xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights (Autonomous) | Higher Diploma in Computer Science | Spring University Myanmar (SUM) | © 2026
        </div>
      </footer>
    </div>
  )
}
