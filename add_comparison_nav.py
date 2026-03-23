"""
GNI Dashboard Nav Update
Adds Comparison page link to src/app/page.tsx
Inserts as a special highlighted row between Intelligence and System groups
GNI-R-037: Read full file first -- already done, file in context
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_comparison_nav.py
"""

import os
import py_compile

file_path = os.path.join("src", "app", "page.tsx")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# The exact block to find -- end of Intelligence group
old = """              <a href="/correlations" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-violet-700 border border-gray-700 hover:border-violet-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4ca</span><span>Correlations</span>
              </a>
            </div>
          </div>
          {/* System group */}"""

new = """              <a href="/correlations" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-violet-700 border border-gray-700 hover:border-violet-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4ca</span><span>Correlations</span>
              </a>
            </div>
          </div>
          {/* Comparison -- special signal page */}
          <div className="mb-2">
            <div className="text-xs text-gray-600 uppercase tracking-widest mb-1.5 px-1">Signal Analysis</div>
            <a href="/comparison" className="flex items-center justify-center gap-2 bg-amber-950 hover:bg-amber-900 border border-amber-800 hover:border-amber-600 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors w-full">
              <span>\U0001f50d</span>
              <span className="text-amber-300">Report vs Debate Comparison</span>
              <span className="ml-auto text-xs bg-amber-800 text-amber-200 px-2 py-0.5 rounded-full font-bold">DISAGREE = \u26a0\ufe0f Signal</span>
            </a>
          </div>
          {/* System group */}"""

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"OK Updated: {file_path}")
else:
    print("ERROR: Target block not found -- file may have changed. Do not proceed.")
    exit(1)

# GNI-R-062: py_compile check
py_compile.compile(__file__, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
