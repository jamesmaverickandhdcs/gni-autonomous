"""
GNI Comparison Page -- Add 7/15/30 day trend tracking
Pure frontend -- computes from existing reports array
No new API needed
GNI-R-037: Full file read done
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_comparison_trends.py
"""

import os
import py_compile

file_path = os.path.join("src", "app", "comparison", "page.tsx")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: Add trend computation to the component logic
old1 = "  const filtered = filter === 'disagree'\n    ? reports.filter(r => isDisagree(r.sentiment, r.mad_verdict))\n    : reports"

new1 = """  const filtered = filter === 'disagree'
    ? reports.filter(r => isDisagree(r.sentiment, r.mad_verdict))
    : reports

  const now = new Date()
  const daysAgo = (d: number) => new Date(now.getTime() - d * 24 * 60 * 60 * 1000)

  const inWindow = (r: Report, days: number) =>
    new Date(r.created_at) >= daysAgo(days)

  const trend7  = reports.filter(r => inWindow(r, 7))
  const trend15 = reports.filter(r => inWindow(r, 15))
  const trend30 = reports.filter(r => inWindow(r, 30))

  const disagree7  = trend7.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length
  const disagree15 = trend15.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length
  const disagree30 = trend30.filter(r => isDisagree(r.sentiment, r.mad_verdict)).length

  const disagreeRate = (d: number, t: number) =>
    t === 0 ? 0 : Math.round((d / t) * 100)"""

if old1 in content:
    content = content.replace(old1, new1)
    fixes += 1
    print("OK Fix 1: Added 7/15/30 day trend computation")

# Fix 2: Add trend section after header stats grid
old2 = """        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">"""

new2 = """          {reports.length > 0 && (
            <div className="mt-4 bg-gray-800 border border-gray-700 rounded-xl p-4">
              <div className="text-xs text-gray-500 uppercase tracking-wider mb-3">&#x26A0;&#xFE0F; DISAGREE Signal Trend</div>
              <div className="grid grid-cols-3 gap-4">
                {[
                  { label: '7 Days', total: trend7.length, disagree: disagree7 },
                  { label: '15 Days', total: trend15.length, disagree: disagree15 },
                  { label: '30 Days', total: trend30.length, disagree: disagree30 },
                ].map(({ label, total, disagree }) => {
                  const rate = disagreeRate(disagree, total)
                  const barColor = rate >= 30 ? 'bg-red-500' : rate >= 15 ? 'bg-yellow-500' : 'bg-green-500'
                  return (
                    <div key={label}>
                      <div className="flex justify-between text-xs mb-1">
                        <span className="text-gray-400">{label}</span>
                        <span className={`font-bold ${rate >= 30 ? 'text-red-400' : rate >= 15 ? 'text-yellow-400' : 'text-green-400'}`}>
                          {disagree}/{total} runs ({rate}%)
                        </span>
                      </div>
                      <div className="h-2 bg-gray-700 rounded-full">
                        <div className={`h-2 rounded-full ${barColor}`} style={{ width: `${rate}%` }} />
                      </div>
                      <div className="text-xs text-gray-600 mt-1">
                        {rate >= 30 ? 'High divergence' : rate >= 15 ? 'Moderate divergence' : 'Low divergence'}
                      </div>
                    </div>
                  )
                })}
              </div>
              <div className="mt-3 text-xs text-gray-600">
                Divergence rate above 30% = systematic disagreement between report AI and MAD debate. Investigate prompt quality or source bias.
              </div>
            </div>
          )}
        </div>
      </header>

      <main className="max-w-6xl mx-auto px-6 py-8">"""

if old2 in content:
    content = content.replace(old2, new2)
    fixes += 1
    print("OK Fix 2: Added 7/15/30 day trend bars to header")

if fixes == 0:
    print("ERROR: No target blocks found -- file may have changed.")
    exit(1)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"OK Updated: {file_path} ({fixes} fixes applied)")

# GNI-R-062
py_compile.compile(__file__, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
