content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()
new_keywords = """GEOPOLITICAL_KEYWORDS = [
    # Tier 4 — Strategic chokepoints and maritime (GNI unique angle)
    'red sea', 'south china sea', 'strait', 'hormuz', 'malacca',
    'suez', 'persian gulf', 'bosphorus', 'panama canal', 'arctic',
    'chokepoint', 'blockade',
    # Tier 5 — New economy conflicts (fastest growing)
    'ai chips', 'semiconductor', 'critical minerals', 'rare earth',
    'lithium', 'cobalt', 'export control', 'debt trap', 'belt and road',
    # Tier 1 — Major powers and flashpoints
    'china', 'russia', 'iran', 'israel', 'ukraine', 'taiwan',
    'north korea', 'middle east', 'europe', 'usa',
    # Tier 2 — Conflict and military
    'war', 'conflict', 'military', 'attack', 'invasion', 'strike',
    'missile', 'nuclear', 'troops', 'weapon', 'bomb', 'ceasefire',
    'sanction', 'embargo', 'terrorism', 'extremis', 'coup', 'crisis', 'threat',
    # Tier 3 — Economics and markets
    'economy', 'trade', 'oil', 'energy', 'inflation', 'tariff',
    'gdp', 'recession', 'gas', 'commodity', 'dollar', 'currency',
    'interest rate', 'federal reserve', 'export', 'import', 'opec',
    # Tier 6 — Diplomacy and governance
    'election', 'government', 'president', 'prime minister',
    'diplomacy', 'ambassador', 'alliance', 'nato', 'eu',
    'united nations', 'security council', 'geopolit',
    'protest', 'revolution', 'riot', 'supply chain',
    # Tier 7 — Humanitarian and global issues
    'refugee', 'humanitarian', 'famine', 'drought', 'climate',
    'pandemic', 'vaccine', 'who', 'tension', 'pacific',
]"""
import re
result = re.sub(r'GEOPOLITICAL_KEYWORDS = \[.*?\]', new_keywords, content, flags=re.DOTALL)
open('ai_engine/funnel/intelligence_funnel.py', 'w', encoding='utf-8').write(result)
print('Done')
