"""
Add Keyword Intelligence link to dashboard nav
Replaces Keywords link with Keyword Intelligence in Intelligence group
GNI-R-037: Full file read done this session
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_keyword_intelligence_nav.py
"""

import os
import py_compile

file_path = os.path.join("src", "app", "page.tsx")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Add keyword-intelligence link after the existing keywords link
old = """              <a href="/keywords" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-teal-700 border border-gray-700 hover:border-teal-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f524</span><span>Keywords</span>
              </a>"""

new = """              <a href="/keywords" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-teal-700 border border-gray-700 hover:border-teal-500 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f524</span><span>Keywords</span>
              </a>
              <a href="/keyword-intelligence" className="flex items-center justify-center gap-2 bg-gray-800 hover:bg-red-800 border border-gray-700 hover:border-red-600 rounded-lg px-3 py-2.5 text-sm font-medium transition-colors">
                <span>\U0001f510</span><span>KW Intel</span>
              </a>"""

if old in content:
    # Also update grid from 7 to 8 cols
    content = content.replace(
        "className=\"grid grid-cols-2 md:grid-cols-7 gap-2\"",
        "className=\"grid grid-cols-2 md:grid-cols-8 gap-2\""
    )
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"OK Updated: {file_path}")
    print("  Keyword Intelligence added to Intelligence group (8-col grid)")
else:
    print("ERROR: Target block not found.")
    exit(1)

py_compile.compile(__file__, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
