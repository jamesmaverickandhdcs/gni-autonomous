with open('src/app/about/page.tsx', 'r', encoding='utf-8') as f:
    content = f.read()

NEW_CARDS = '''
        {/* 4 Perspective Sub-Pages */}
        <div className="bg-gray-900 border border-gray-700 rounded-xl p-5">
          <div className="text-xs text-gray-500 uppercase tracking-wider mb-4">Explore GNI From 4 Perspectives</div>
          <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
            <a href="/about/quantum" className="bg-blue-950 border border-blue-800 hover:border-blue-600 rounded-xl p-5 transition-colors group">
              <div className="text-lg font-bold text-blue-400 mb-1 group-hover:text-blue-300">Quantum Strategist</div>
              <div className="text-xs text-blue-600 uppercase tracking-wider mb-2">Outcomes + Verdicts</div>
              <p className="text-xs text-gray-400 leading-relaxed">What GNI decides and why. MAD Protocol outcomes, live threat verdicts, market implications, action recommendations, and blind spot warnings -- the full intelligence output explained.</p>
              <div className="mt-3 text-xs text-blue-500 font-bold">View Outcomes --&gt;</div>
            </a>
            <a href="/about/patterns" className="bg-green-950 border border-green-800 hover:border-green-600 rounded-xl p-5 transition-colors group">
              <div className="text-lg font-bold text-green-400 mb-1 group-hover:text-green-300">Pattern Intelligence</div>
              <div className="text-xs text-green-600 uppercase tracking-wider mb-2">Long-Term Research</div>
              <p className="text-xs text-gray-400 leading-relaxed">How GNI builds its evidence base over time. GPVS prediction accuracy, source weight evolution, pipeline run history, and the statistical methodology behind every intelligence claim.</p>
              <div className="mt-3 text-xs text-green-500 font-bold">View Research --&gt;</div>
            </a>
            <a href="/about/feedback" className="bg-amber-950 border border-amber-800 hover:border-amber-600 rounded-xl p-5 transition-colors group">
              <div className="text-lg font-bold text-amber-400 mb-1 group-hover:text-amber-300">Feedback Loop</div>
              <div className="text-xs text-amber-600 uppercase tracking-wider mb-2">Active/Passive SWOT</div>
              <p className="text-xs text-gray-400 leading-relaxed">The most honest assessment of GNI. Strengths, weaknesses, opportunities, and threats -- analyzed rigorously with live prediction verification data showing exactly where GNI stands.</p>
              <div className="mt-3 text-xs text-amber-500 font-bold">View SWOT --&gt;</div>
            </a>
            <a href="/about/devops" className="bg-purple-950 border border-purple-800 hover:border-purple-600 rounded-xl p-5 transition-colors group">
              <div className="text-lg font-bold text-purple-400 mb-1 group-hover:text-purple-300">Dev Console</div>
              <div className="text-xs text-purple-600 uppercase tracking-wider mb-2">Autonomous Architecture</div>
              <p className="text-xs text-gray-400 leading-relaxed">How GNI runs itself. All 4 GitHub Actions pipelines, the self-healing heartbeat, the 66-pattern security layer, and live token quota data proving .00/month L7 autonomous operation.</p>
              <div className="mt-3 text-xs text-purple-500 font-bold">View Architecture --&gt;</div>
            </a>
          </div>
        </div>
'''

# Insert before the disclaimer div
if 'DISCLAIMER' in content:
    content = content.replace(
        '\n      {/* DISCLAIMER */}',
        NEW_CARDS + '\n      {/* DISCLAIMER */}'
    )
    with open('src/app/about/page.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('FIXED: about/page.tsx -- added 4 perspective cards')
else:
    # Insert before footer
    content = content.replace(
        '\n      <div className="max-w-6xl mx-auto px-6 pb-2',
        NEW_CARDS + '\n      <div className="max-w-6xl mx-auto px-6 pb-2'
    )
    with open('src/app/about/page.tsx', 'w', encoding='utf-8') as f:
        f.write(content)
    print('FIXED: about/page.tsx -- added 4 perspective cards (before footer)')
print('Done')