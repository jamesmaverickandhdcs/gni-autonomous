with open("src/app/about/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

import re

# Find 2025 occurrences
for m in re.finditer(r"2025", content):
    print(f"2025 at {m.start()}:")
    print(repr(content[m.start()-80:m.start()+80]))
    print()

# Find Sprint days
idx = content.find("Sprint days")
if idx != -1:
    print(f"Sprint days at {idx}:")
    print(repr(content[idx-80:idx+120]))