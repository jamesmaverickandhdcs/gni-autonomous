# ============================================================
# GNI Escalation Scorer — Day 10
# Counts concurrent high-relevance events across all three
# GNI pillars: Technology, Geopolitical, Financial
# Score: 1-10 where 10 = maximum systemic risk
# ============================================================

# Pillar 1 — Technology / New Economy signals
TECH_SIGNALS = [
    'ai chips', 'semiconductor', 'chip ban', 'export control',
    'critical minerals', 'rare earth', 'lithium', 'cobalt',
    'debt trap', 'belt and road', 'cyber', 'hack', 'ransomware',
    'tech war', 'huawei', 'nvidia', 'tsmc',
    'artificial intelligence', 'quantum computing', 'drone', 'satellite',
    'biotech', 'electric vehicle', 'battery', 'data center',
]

# Pillar 2 — Geopolitical / Maritime signals
GEO_SIGNALS = [
    'war', 'invasion', 'attack', 'missile', 'nuclear', 'coup',
    'sanction', 'embargo', 'blockade', 'chokepoint',
    'red sea', 'hormuz', 'malacca', 'south china sea', 'arctic',
    'strait', 'naval', 'military', 'troops', 'ceasefire',
    'iran', 'russia', 'china', 'north korea', 'israel',
    'taiwan', 'ukraine',
]

# Pillar 3 — Financial / Market signals
FIN_SIGNALS = [
    'oil price', 'energy crisis', 'inflation', 'recession',
    'federal reserve', 'interest rate', 'market crash', 'currency',
    'dollar', 'gold', 'crude', 'opec', 'supply chain disruption',
    'trade war', 'tariff', 'gdp', 'economic crisis',
    'bank run', 'banking crisis', 'credit crunch', 'debt default',
    'currency collapse', 'hyperinflation', 'devaluation', 'capital flight',
    'commodity shock', 'wheat', 'food crisis', 'natural gas',
    'bond yield', 'yield curve', 'treasury', 'debt ceiling',
    'crypto crash', 'bitcoin', 'stablecoin', 'liquidity crisis',
]

# Critical escalation combinations — when these co-occur, score jumps
CRITICAL_COMBOS = [
    (['hormuz', 'iran'], 3),
    (['taiwan', 'china', 'military'], 3),
    (['nuclear', 'north korea'], 3),
    (['red sea', 'attack'], 2),
    (['semiconductor', 'export control', 'china'], 2),
    (['oil', 'sanction', 'russia'], 2),
    (['malacca', 'blockade'], 2),
    (['bank run', 'banking crisis'], 3),
    (['currency collapse', 'dollar'], 2),
    (['commodity shock', 'food crisis'], 2),
    (['debt default', 'recession'], 2),
]


def score_escalation(articles: list[dict]) -> dict:
    """
    Score systemic escalation risk from selected articles.

    Args:
        articles: top selected articles from intelligence funnel

    Returns:
        dict with escalation_score (1-10), level, pillar_scores, signals_found
    """
    combined_text = ' '.join([
        f"{a.get('title', '')} {a.get('summary', '')}".lower()
        for a in articles
    ]).lower()

    # Score each pillar
    tech_hits = [s for s in TECH_SIGNALS if s in combined_text]
    geo_hits  = [s for s in GEO_SIGNALS if s in combined_text]
    fin_hits  = [s for s in FIN_SIGNALS if s in combined_text]

    # Base score — weighted by pillar importance
    tech_score = min(len(tech_hits) * 1.5, 5)
    geo_score  = min(len(geo_hits)  * 1.0, 5)
    fin_score  = min(len(fin_hits)  * 0.8, 4)

    base_score = tech_score + geo_score + fin_score

    # Pillar diversity bonus — all three pillars active = convergence
    active_pillars = sum([
        1 if tech_hits else 0,
        1 if geo_hits  else 0,
        1 if fin_hits  else 0,
    ])
    diversity_bonus = (active_pillars - 1) * 1.5 if active_pillars > 1 else 0

    # Critical combination bonus
    combo_bonus = 0
    for keywords, bonus in CRITICAL_COMBOS:
        if all(kw in combined_text for kw in keywords):
            combo_bonus += bonus

    # Final score — capped at 10
    raw_score = base_score + diversity_bonus + combo_bonus
    final_score = round(min(raw_score, 10.0), 1)
    final_score = max(final_score, 1.0)

    # Escalation level
    if final_score >= 9:
        level = 'CRITICAL'
    elif final_score >= 7:
        level = 'HIGH'
    elif final_score >= 5:
        level = 'ELEVATED'
    elif final_score >= 3:
        level = 'MODERATE'
    else:
        level = 'LOW'

    # GNI-R-117: Return full evidence object -- never discard reasoning
    score_breakdown = {
        'tech_base':       round(tech_score, 1),
        'geo_base':        round(geo_score, 1),
        'fin_base':        round(fin_score, 1),
        'base_total':      round(base_score, 1),
        'diversity_bonus': round(diversity_bonus, 1),
        'combo_bonus':     round(combo_bonus, 1),
        'raw_score':       round(raw_score, 1),
        'final_score':     final_score,
    }
    factors = []
    if tech_hits:
        factors.append('Tech signals: ' + ', '.join(tech_hits[:3]))
    if geo_hits:
        factors.append('Geo signals: ' + ', '.join(geo_hits[:3]))
    if fin_hits:
        factors.append('Fin signals: ' + ', '.join(fin_hits[:3]))
    if diversity_bonus > 0:
        factors.append('Multi-pillar convergence: +' + str(round(diversity_bonus, 1)))
    if combo_bonus > 0:
        factors.append('Critical combination detected: +' + str(combo_bonus))

    return {
        'escalation_score': final_score,
        'escalation_level': level,
        'pillar_scores': {
            'technology': round(tech_score, 1),
            'geopolitical': round(geo_score, 1),
            'financial': round(fin_score, 1),
        },
        'active_pillars': active_pillars,
        'signals_found': {
            'technology': tech_hits[:5],
            'geopolitical': geo_hits[:5],
            'financial': fin_hits[:5],
        },
        'combo_bonus':     combo_bonus,
        'score_breakdown': score_breakdown,
        'factors':         factors,
    }


if __name__ == '__main__':
    # Quick test
    test_articles = [
        {'title': 'Iran threatens to close Strait of Hormuz amid US sanctions',
         'summary': 'Iran military moves near Hormuz chokepoint as oil prices spike'},
        {'title': 'China semiconductor export controls target AI chips',
         'summary': 'Beijing restricts rare earth exports critical minerals supply chain'},
        {'title': 'Federal Reserve signals interest rate hike amid inflation',
         'summary': 'Market crash fears as dollar strengthens and gold surges'},
    ]
    result = score_escalation(test_articles)
    print(f"Escalation Score: {result['escalation_score']}/10 [{result['escalation_level']}]")
    print(f"Active Pillars: {result['active_pillars']}/3")
    print(f"Pillar Scores: {result['pillar_scores']}")
    print(f"Combo Bonus: {result['combo_bonus']}")
    print(f"Tech Signals: {result['signals_found']['technology']}")
    print(f"Geo Signals:  {result['signals_found']['geopolitical']}")
    print(f"Fin Signals:  {result['signals_found']['financial']}")
