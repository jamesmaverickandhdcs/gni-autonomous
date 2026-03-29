import os
import re

pages_with_footer_issues = [
    "comparison","scenarios","map","alerts","history","correlations",
    "weekly-digest","transparency","health","source-health","adaptive-log",
    "quota","predictions"
]

for page in pages_with_footer_issues:
    path = f"src/app/{page}/page.tsx"
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    # Find footer content
    footer_idx = content.find("<footer")
    if footer_idx != -1:
        footer_content = content[footer_idx:footer_idx+400]
        print(f"=== {page} ===")
        print(repr(footer_content[:250]))
        print()