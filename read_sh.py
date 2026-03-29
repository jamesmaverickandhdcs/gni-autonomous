with open("src/app/source-health/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

idx = content.find("Dashboard")
print(repr(content[idx-150:idx+150]))