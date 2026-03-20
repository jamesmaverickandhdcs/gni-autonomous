f = open("analysis/nexus_analyzer.py", "r", encoding="utf-8")
c = f.read()
f.close()

old = 'market_impact": "2-3 sentence analysis of potential market impact"'
new = 'market_impact": "3-4 sentences explaining WHY this affects markets. Use causal language: because, therefore, as a result, driven by, consequently, leading to, due to. Explain the chain of causation from event to market outcome in detail."'

c = c.replace(old, new)

f = open("analysis/nexus_analyzer.py", "w", encoding="utf-8")
f.write(c)
f.close()
print("Done")