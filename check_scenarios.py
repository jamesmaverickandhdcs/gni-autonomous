with open("src/app/scenarios/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

import re
matches = re.finditer(r'100\+', content)
for m in matches:
    idx = m.start()
    print(f"Found 100+ at {idx}:")
    print(repr(content[idx-100:idx+100]))
    print()