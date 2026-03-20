export default function AboutPage() {
  const infra = [
    { name: 'Ollama (Llama 3)', role: 'Local AI — runs on James laptop', cost: '$0.00' },
    { name: 'Groq API', role: 'Cloud AI fallback — free tier', cost: '$0.00' },
    { name: 'Supabase', role: 'Database — free tier', cost: '$0.00' },
    { name: 'Vercel', role: 'Web hosting — free tier', cost: '$0.00' },
    { name: 'GitHub Actions', role: 'CI/CD pipeline — free tier', cost: '$0.00' },
    { name: 'Telegram Bot API', role: 'CRITICAL alerts — free', cost: '$0.00' },
  ]

  const timeline = [
    { level: 'L4', day: 'Day 7', label: 'Diploma baseline', desc: '5 RSS sources · 92 articles · basic AI report · map · stocks · transparency' },
    { level: 'L5', day: 'Day 10', label: 'GPVS + Quality', desc: 'Prediction validation · quality scoring · source weights · escalation · 13 RSS sources · 242 articles' },
    { level: 'L6', day: 'Day 13', label: 'Self-improving', desc: 'Prompt A/B testing · source credibility learning · historical correlation · weekly digest' },
    { level: 'L7', day: 'Day 17', label: 'Fully autonomous', desc: 'MAD Protocol · deception detection · frequency controller · health agent · audit trail · self-healing' },
  ]

  const stats = [
    { label: 'Pipeline runs', value: '30+' },
    { label: 'Articles analysed', value: '7,000+' },
    { label: 'Reports generated', value: '30+' },
    { label: 'GPVS accuracy', value: '100%' },
    { label: 'Injection patterns', value: '66' },
    { label: 'Sprint days', value: '17' },
  ]

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100">
      <header className="border-b border-gray-800 bg-gray-900">
        <div className="max-w-5xl mx-auto px-6 py-4 flex items-center justify-between">
          <div>
            <h1 className="text-2xl font-bold text-white">🌐 About GNI</h1>
            <p className="text-sm text-gray-400">Global Nexus Insights (Autonomous) — The $0.00/month intelligence platform</p>
          </div>
          <a href="/" className="text-sm text-blue-400 hover:text-blue-300">← Dashboard</a>
        </div>
      </header>

      <main className="max-w-5xl mx-auto px-6 py-8 space-y-8">

        {/* $0 Hero */}
        <div className="bg-gray-900 border border-gray-700 rounded-2xl p-8 text-center">
          <div className="text-8xl font-bold text-green-400 mb-2">$0.00</div>
          <div className="text-xl text-gray-300 mb-1">per month</div>
          <div className="text-sm text-gray-500">Production-grade autonomous AI intelligence. Forever free.</div>
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
            accessible to anyone in the world — including people in remote regions like Myanmar
            where access to quality global news analysis is limited.
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

        {/* Built by */}
      </main>

      <footer className="border-t border-gray-800 mt-12">
        <div className="max-w-5xl mx-auto px-6 py-4 text-center text-xs text-gray-600">
          GNI — Global Nexus Insights (Autonomous) | Higher Diploma in Computer Science | Spring University Myanmar (SUM) | © 2026
        </div>
      </footer>
    </div>
  )
}
