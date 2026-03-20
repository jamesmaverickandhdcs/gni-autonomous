f = open("src/app/page.tsx", "r", encoding="utf-8")
c = f.read()
f.close()

# Fix 1: Add MAD fields to Report interface
old_interface = '  llm_source: string\n  created_at: string\n}'
new_interface = '  llm_source: string\n  created_at: string\n  mad_bull_case: string\n  mad_bear_case: string\n  mad_verdict: string\n  mad_confidence: number\n}'
c = c.replace(old_interface, new_interface)

# Fix 2: Add MAD widget before Disclaimer
old_disclaimer = '                {/* Disclaimer */}'
new_disclaimer = '''                {/* MAD Protocol Widget */}
                {(latest.mad_verdict) && (
                  <div className="bg-gray-800 rounded-lg p-4 mb-4">
                    <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">
                      🐂🐻 MAD Protocol — Multi-Agent Debate
                    </div>
                    <div className="flex items-center gap-3 mb-3">
                      <span className={`text-sm font-bold px-3 py-1 rounded-full ${latest.mad_verdict === 'bullish' ? 'bg-green-900 text-green-300' : latest.mad_verdict === 'bearish' ? 'bg-red-900 text-red-300' : 'bg-gray-700 text-gray-300'}`}>
                        {latest.mad_verdict === 'bullish' ? '🐂' : latest.mad_verdict === 'bearish' ? '🐻' : '◆'} {latest.mad_verdict?.toUpperCase()}
                      </span>
                      <span className="text-xs text-gray-400">
                        Confidence: {latest.mad_confidence ? Math.round(latest.mad_confidence * 100) + '%' : 'N/A'}
                      </span>
                    </div>
                    <div className="grid grid-cols-1 md:grid-cols-2 gap-3">
                      <div className="bg-green-950 border border-green-800 rounded-lg p-3">
                        <div className="text-xs text-green-400 font-bold mb-1">🐂 Bull Case</div>
                        <p className="text-xs text-gray-300 leading-relaxed">{latest.mad_bull_case}</p>
                      </div>
                      <div className="bg-red-950 border border-red-800 rounded-lg p-3">
                        <div className="text-xs text-red-400 font-bold mb-1">🐻 Bear Case</div>
                        <p className="text-xs text-gray-300 leading-relaxed">{latest.mad_bear_case}</p>
                      </div>
                    </div>
                  </div>
                )}

                {/* Disclaimer */}'''
c = c.replace(old_disclaimer, new_disclaimer)

f = open("src/app/page.tsx", "w", encoding="utf-8")
f.write(c)
f.close()
print("Done")