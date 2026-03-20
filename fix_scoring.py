import re
content = open('ai_engine/funnel/intelligence_funnel.py', encoding='utf-8').read()
old = """    # High-impact keywords (+3 each, max 15)
    high_impact = [
        'war', 'nuclear', 'invasion', 'attack', 'crisis',
        'sanction', 'ceasefire', 'coup', 'collapse', 'embargo'
    ]"""
new = """    # High-impact keywords (+3 each, max 15) — Tier 4 + Tier 5 (GNI unique angle)
    high_impact = [
        'red sea', 'hormuz', 'malacca', 'suez', 'chokepoint',
        'blockade', 'persian gulf', 'south china sea', 'arctic',
        'ai chips', 'critical minerals', 'semiconductor', 'rare earth',
        'lithium', 'cobalt', 'debt trap', 'belt and road', 'export control',
    ]"""
result = content.replace(old, new)
old2 = """    # Medium-impact keywords (+1 each, max 10)
    med_impact = [
        'military', 'troops', 'missile', 'economy', 'inflation',
        'oil', 'trade', 'tariff', 'election', 'protest', 'tension'
    ]"""
new2 = """    # Medium-impact keywords (+1 each, max 10) — Tier 1 + Tier 2
    med_impact = [
        'war', 'nuclear', 'invasion', 'attack', 'crisis',
        'sanction', 'ceasefire', 'coup', 'collapse', 'embargo',
        'china', 'russia', 'iran', 'israel', 'ukraine', 'taiwan', 'north korea',
        'military', 'troops', 'missile', 'tension',
    ]"""
result = result.replace(old2, new2)
old3 = """    major_regions = [
        'china', 'russia', 'ukraine', 'iran', 'israel',
        'taiwan', 'north korea', 'middle east', 'usa', 'europe'
    ]"""
new3 = """    major_regions = [
        'middle east', 'europe', 'usa', 'pacific',
        'economy', 'oil', 'trade', 'inflation', 'election',
    ]"""
result = result.replace(old3, new3)
open('ai_engine/funnel/intelligence_funnel.py', 'w', encoding='utf-8').write(result)
print('high replacements:', content.count(old))
print('med replacements:', content.count(old2))
print('region replacements:', content.count(old3))
