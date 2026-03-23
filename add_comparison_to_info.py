"""
GNI Dashboard Nav -- Add Comparison to INFO group
Adds Report vs Debate Comparison link alongside Transparency and About
GNI-R-037: Full file read done earlier this session
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_comparison_to_info.py
"""

import os
import py_compile

file_path = os.path.join("src", "app", "page.tsx")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

old = """          {/* Info group */}
          <div>
            <div className="text-xs text-gray-600 uppercase tracking-widest mb-1.5 px-1">Info</div>
            <div className="grid grid-cols-2 gap-2">
              <a href="/transparency" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-purple-700 border border-gray-700 hover:border-purple-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f50d</span><span>Transparency</span>
              </a>
              <a href="/about" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-yellow-700 border border-gray-700 hover:border-yellow-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f31f</span><span>About</span>
              </a>
            </div>
          </div>"""

new = """          {/* Info group */}
          <div>
            <div className="text-xs text-gray-600 uppercase tracking-widest mb-1.5 px-1">Info</div>
            <div className="grid grid-cols-3 gap-2">
              <a href="/transparency" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-purple-700 border border-gray-700 hover:border-purple-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f50d</span><span>Transparency</span>
              </a>
              <a href="/about" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-yellow-700 border border-gray-700 hover:border-yellow-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f31f</span><span>About</span>
              </a>
              <a href="/comparison" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-amber-700 border border-gray-700 hover:border-amber-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f50d</span><span>Comparison</span>
              </a>
            </div>
          </div>"""

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"OK Updated: {file_path}")
    print("  Comparison link added to INFO group (3-col grid)")
else:
    print("ERROR: Target block not found -- file may have changed.")
    exit(1)

# GNI-R-062: py_compile check
py_compile.compile(__file__, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
