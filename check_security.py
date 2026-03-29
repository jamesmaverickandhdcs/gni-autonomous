with open("src/app/stocks/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

import re
# Find sk- occurrences
matches = re.finditer(r'sk-[^\s\'"]{5,}', content)
for m in matches:
    idx = m.start()
    print(f"Found at {idx}:")
    print(repr(content[idx-50:idx+100]))
    print()

# Also check about page stale numbers
print("=== ABOUT stale numbers ===")
with open("src/app/about/page.tsx", "r", encoding="utf-8") as f:
    about = f.read()
for num in ["30+", "7,000+", "7000"]:
    idx = about.find(num)
    if idx != -1:
        print(f"Found {num} at {idx}:")
        print(repr(about[idx-100:idx+100]))
        print()