content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()
old = "    'china', 'russia', 'ukraine', 'iran', 'israel', 'taiwan',"
new = "    'china', 'russia', 'ukraine', 'iran', 'israel', 'taiwan',\n    'red sea', 'south china sea', 'arctic', 'strait', 'hormuz',\n    'malacca', 'bosphorus', 'suez', 'panama canal', 'persian gulf',\n    'chokepoint', 'blockade', 'debt trap', 'belt and road',\n    'critical minerals', 'rare earth', 'lithium', 'cobalt',\n    'ai chips', 'semiconductor', 'export control', 'supply chain',"
result = content.replace(old, new)
open('ai_engine/funnel/intelligence_funnel.py', 'w', encoding='utf-8').write(result)
print('Done - replacements:', content.count(old))
