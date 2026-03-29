with open("src/app/about/page.tsx", "r", encoding="utf-8") as f:
    content = f.read()

# Find the stats section
idx = content.find("Pipeline runs")
print(repr(content[idx-50:idx+300]))