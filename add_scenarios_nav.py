"""
GNI Dashboard Nav -- Add Scenarios to Intelligence group
Scenarios fits Intelligence group alongside History, Debate, etc.
GNI-R-037: Full file read done this session
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_scenarios_nav.py
"""

import os
import py_compile

file_path = os.path.join("src", "app", "page.tsx")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Change Intelligence grid from 6-col to 7-col and add Scenarios
old = """            <div className="grid grid-cols-2 md:grid-cols-6 gap-2">
              <a href="/history" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-orange-700 border border-gray-700 hover:border-orange-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4cb</span><span>History</span>
              </a>
              <a href="/debate" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-red-800 border border-gray-700 hover:border-red-600 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f402\U0001f43b</span><span>Debate</span>
              </a>
              <a href="/stocks" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-green-700 border border-gray-700 hover:border-green-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4c8</span><span>Stocks</span>
              </a>
              <a href="/map" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-blue-700 border border-gray-700 hover:border-blue-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f5fa\ufe0f</span><span>Map</span>
              </a>
              <a href="/keywords" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-teal-700 border border-gray-700 hover:border-teal-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f524</span><span>Keywords</span>
              </a>
              <a href="/correlations" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-violet-700 border border-gray-700 hover:border-violet-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4ca</span><span>Correlations</span>
              </a>
            </div>"""

new = """            <div className="grid grid-cols-2 md:grid-cols-7 gap-2">
              <a href="/history" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-orange-700 border border-gray-700 hover:border-orange-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4cb</span><span>History</span>
              </a>
              <a href="/debate" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-red-800 border border-gray-700 hover:border-red-600 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f402\U0001f43b</span><span>Debate</span>
              </a>
              <a href="/stocks" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-green-700 border border-gray-700 hover:border-green-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4c8</span><span>Stocks</span>
              </a>
              <a href="/map" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-blue-700 border border-gray-700 hover:border-blue-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f5fa\ufe0f</span><span>Map</span>
              </a>
              <a href="/keywords" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-teal-700 border border-gray-700 hover:border-teal-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f524</span><span>Keywords</span>
              </a>
              <a href="/correlations" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-violet-700 border border-gray-700 hover:border-violet-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f4ca</span><span>Correlations</span>
              </a>
              <a href="/scenarios" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-indigo-700 border border-gray-700 hover:border-indigo-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f52e</span><span>Scenarios</span>
              </a>
            </div>"""

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"OK Updated: {file_path}")
    print("  Scenarios added to Intelligence group (7-col grid)")
else:
    print("ERROR: Target block not found -- file may have changed.")
    exit(1)

py_compile.compile(__file__, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
