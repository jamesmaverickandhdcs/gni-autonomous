import re
import hashlib
import sys
import os
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.source_weights import get_source_weights

# ============================================================
# GNI Intelligence Funnel v3 â€” Day 6
# Now returns full article trace for Explainable AI
# Each article carries pass/fail + reason at every stage
# ============================================================

# Stage 1: Relevance keywords
GEOPOLITICAL_KEYWORDS = [
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
]

IRRELEVANT_KEYWORDS = [
    'celebrity', 'entertainment', 'movie', 'music', 'sport', 'football',
    'basketball', 'tennis', 'golf', 'oscars', 'grammy', 'fashion',
    'recipe', 'cooking', 'lifestyle', 'travel', 'tourism', 'wedding',
    'divorce', 'dating', 'viral', 'meme', 'tiktok', 'instagram',
]

# Stage 1b: Injection patterns
INJECTION_PATTERNS = [
    # Category 1: Direct instruction overrides
    r'ignore\s+(previous|prior|above|all)\s+instructions?',
    r'disregard\s+(previous|prior|above|all)\s+instructions?',
    r'forget\s+(previous|prior|above|all)\s+instructions?',
    r'override\s+(previous|prior|above|all)\s+instructions?',
    r'new\s+instructions?\s*:',
    r'updated\s+instructions?\s*:',
    r'system\s*:\s*you\s+are',
    r'you\s+are\s+now\s+(a\s+)?(?:different|new|another)',
    r'act\s+as\s+(a|an)\s+\w+',
    r'pretend\s+(you\s+are|to\s+be)',
    r'roleplay\s+as',
    r'from\s+now\s+on\s+(you|act|behave)',
    r'your\s+new\s+(role|persona|identity|task)\s+is',
    # Category 2: Score manipulation
    r'rate\s+this\s+article\s+[0-9]+\s*/\s*[0-9]+',
    r'score\s*[=:]\s*[0-9]+',
    r'set\s+(score|rating|priority)\s+to',
    r'give\s+(this|all)\s+(article|story)\s+a\s+(score|rating)',
    r'mark\s+(all|this)\s+(others?|article)',
    r'rank\s+(this|all)\s+(article|story)\s+(as|at)\s+(top|highest|first)',
    # Category 3: Bias manipulation
    r'(system|admin|root)\s*:\s*(override|bypass|ignore)',
    r'always\s+(rate|score|rank)\s+(israel|iran|us|china|russia)\s+as',
    r'ignore\s+(all\s+)?(article|news)\s+(from|about)',
    r'filter\s+out\s+(all\s+)?(article|news)\s+(from|about)',
    r'never\s+(report|include|select)\s+(news|article)\s+(about|from)',
    # Category 4: Prompt boundary attacks
    r'```\s*(system|assistant|user)\s*```',
    r'<\s*system\s*>',
    r'\[INST\]',
    r'\[\/INST\]',
    r'<<SYS>>',
    r'<</SYS>>',
    r'human\s*:\s*ignore',
    r'assistant\s*:\s*sure',
    r'<\|system\|>',
    r'<\|user\|>',
    r'<\|assistant\|>',
    r'\[SYSTEM\]',
    r'\[USER\]',
    r'\[ASSISTANT\]',
    # Category 5: Encoded attacks
    r'aWdub3Jl',
    r'aW5zdHJ1Y3Rpb24',
    r'base64\s*:\s*[A-Za-z0-9+/=]{20,}',
    r'&#x[0-9a-fA-F]{2};.*ignore',
    # Category 6: Multilingual injections
    r'ignorez\s+les\s+instructions',
    r'ignorar\s+las\s+instrucciones',
    r'ignorieren\s+sie\s+die\s+anweisungen',
    r'ignora\s+(le\s+)?istruzioni',
    # Category 7: Role confusion and jailbreak
    r'(unlock|enable|activate)\s+(developer|god|admin|root|jailbreak)\s+mode',
    r'DAN\s+(mode|protocol|is\s+now)',
    r'jailbreak(ed|\s+mode|\s+prompt)?',
    r'(bypass|circumvent|override)\s+(safety|filter|restriction|guideline)',
    r'(forget|ignore)\s+(that\s+)?(you\s+are\s+an?\s+)?(ai|assistant|bot)',
    # Category 8: Context overflow
    r'\[\s*IGNORE\s*EVERYTHING\s*ABOVE\s*\]',
    r'###\s*(end|stop|ignore)\s*(above|previous|all)',
    r'-{10,}\s*(new\s+instruction|system\s+prompt)',
    # Category 9: Nested injections
    r'the\s+article\s+says\s+(to\s+)?(ignore|override|disregard)',
    r'urgent\s*:\s*(ignore|override|disregard)\s+(all\s+)?instructions?',
    # Category 10: Code execution and data exfiltration
    r'print\s*\(',
    r'exec\s*\(',
    r'eval\s*\(',
    r'__import__',
    r'send\s+(all|this)\s+(data|article|information)\s+to',
    r'forward\s+(all|this)\s+(data|article|information)\s+to',
    r'exfiltrate\s+(data|information|results)',
    r'http[s]?://(?!www\.(aljazeera|cnn|foxnews|bbc|dw|reuters|bloomberg|nikkei|wired|technologyreview|france24|usni|straitstimes|rcinet)\.(com|org|net|co))',
]


def _check_relevance(article: dict) -> tuple[bool, str]:
    """Stage 1: Check if article is geopolitically relevant."""
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    # Check irrelevant first
    for kw in IRRELEVANT_KEYWORDS:
        if kw in text:
            return False, f"Irrelevant topic: '{kw}'"

    # Check relevant
    matched = [kw for kw in GEOPOLITICAL_KEYWORDS if kw in text]
    if matched:
        return True, f"Matched keywords: {', '.join(matched[:3])}"

    return False, "No geopolitical keywords found"


def _check_injection(article: dict) -> tuple[bool, str]:
    """Stage 1b: Check for prompt injection attacks."""
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return False, f"Injection pattern detected: {pattern[:40]}"
    return True, "Clean â€” no injection patterns"


def _get_dedup_key(article: dict) -> str:
    """Generate deduplication key from title."""
    title = article.get('title', '').lower().strip()
    title = re.sub(r'[^a-z0-9\s]', '', title)
    words = title.split()[:6]
    return hashlib.md5(' '.join(words).encode()).hexdigest()


def _score_article(article: dict) -> tuple[float, str]:
    """Stage 3: Score article by significance."""
    score = 0.0
    reasons = []

    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    # High-impact keywords (+3 each, max 15) — Tier 4 + Tier 5 (GNI unique angle)
    high_impact = [
        'red sea', 'hormuz', 'malacca', 'suez', 'chokepoint',
        'blockade', 'persian gulf', 'south china sea', 'arctic',
        'ai chips', 'critical minerals', 'semiconductor', 'rare earth',
        'lithium', 'cobalt', 'debt trap', 'belt and road', 'export control',
    ]
    hi_matches = [kw for kw in high_impact if kw in text]
    hi_score = min(len(hi_matches) * 3, 15)
    score += hi_score
    if hi_matches:
        reasons.append(f"High-impact terms ({hi_score}pts): {', '.join(hi_matches[:3])}")

    # Medium-impact keywords (+1 each, max 10) — Tier 1 + Tier 2
    med_impact = [
        'war', 'nuclear', 'invasion', 'attack', 'crisis',
        'sanction', 'ceasefire', 'coup', 'collapse', 'embargo',
        'china', 'russia', 'iran', 'israel', 'ukraine', 'taiwan', 'north korea',
        'military', 'troops', 'missile', 'tension',
    ]
    med_matches = [kw for kw in med_impact if kw in text]
    med_score = min(len(med_matches), 10)
    score += med_score
    if med_matches:
        reasons.append(f"Medium-impact terms ({med_score}pts): {', '.join(med_matches[:3])}")

    # Major country/region bonus (+5)
    major_regions = [
        'middle east', 'europe', 'usa', 'pacific',
        'economy', 'oil', 'trade', 'inflation', 'election',
    ]
    region_matches = [r for r in major_regions if r in text]
    if region_matches:
        score += 5
        reasons.append(f"Major region (+5pts): {region_matches[0]}")

    # Dynamic source weight bonus (replaces hardcoded credibility)
    weights = get_source_weights()
    source_key = article.get('source', '').lower()
    weight = weights.get(source_key, 1.0)
    weight_bonus = round((weight - 1.0) * 10, 2)  # 1.3 weight = +3pts, 0.9 = -1pt
    if weight_bonus != 0:
        score += weight_bonus
        reasons.append(f"Source weight ({weight:.2f} = {weight_bonus:+.1f}pts): {article.get('source')}")

    reason_str = " | ".join(reasons) if reasons else "Base score only"
    return round(score, 2), reason_str


def run_funnel(
    articles: list[dict],
    top_n: int = 5,
    max_per_source: int = 3
) -> tuple[list[dict], list[dict]]:
    """
    Run the 4-stage Intelligence Funnel.
    
    Returns:
        (top_articles, article_trace)
        
        top_articles: final selected articles for AI analysis
        article_trace: ALL articles with full stage-by-stage trace
    """
    print("ðŸ”½ Intelligence Funnel Running...")
    trace = []
    seen_keys = set()

    # â”€â”€ Stage 1: Relevance â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    stage1_pass = []
    for art in articles:
        passed, reason = _check_relevance(art)
        art['stage1_passed'] = passed
        art['stage1_reason'] = reason
        # Default remaining stages
        art['stage1b_passed'] = True
        art['stage1b_reason'] = 'Not evaluated (failed Stage 1)'
        art['stage2_passed'] = True
        art['stage2_reason'] = 'Not evaluated (failed Stage 1)'
        art['stage3_score'] = 0.0
        art['stage3_reason'] = 'Not evaluated (failed Stage 1)'
        art['stage4_selected'] = False
        art['stage4_rank'] = None

        if passed:
            stage1_pass.append(art)
        else:
            trace.append(art)

    print(f"  Stage 1 (Relevance):       {len(articles)} â†’ {len(stage1_pass)} articles")

    # â”€â”€ Stage 1b: Injection Detection â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    stage1b_pass = []
    for art in stage1_pass:
        passed, reason = _check_injection(art)
        art['stage1b_passed'] = passed
        art['stage1b_reason'] = reason
        art['stage2_passed'] = True
        art['stage2_reason'] = 'Not evaluated (failed Stage 1b)'
        art['stage3_score'] = 0.0
        art['stage3_reason'] = 'Not evaluated (failed Stage 1b)'

        if passed:
            stage1b_pass.append(art)
        else:
            trace.append(art)

    flagged = len(stage1_pass) - len(stage1b_pass)
    print(f"  Stage 1b (Inj. Filter):    {len(stage1_pass)} â†’ {len(stage1b_pass)} articles ({flagged} flagged)")

    # â”€â”€ Stage 2: Deduplication â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    stage2_pass = []
    for art in stage1b_pass:
        key = _get_dedup_key(art)
        if key in seen_keys:
            art['stage2_passed'] = False
            art['stage2_reason'] = f"Duplicate of earlier article (key: {key[:8]}...)"
            art['stage3_score'] = 0.0
            art['stage3_reason'] = 'Not evaluated (duplicate)'
            trace.append(art)
        else:
            seen_keys.add(key)
            art['stage2_passed'] = True
            art['stage2_reason'] = "Unique article â€” no duplicate found"
            stage2_pass.append(art)

    dupes = len(stage1b_pass) - len(stage2_pass)
    print(f"  Stage 2 (Deduplication):   {len(stage1b_pass)} â†’ {len(stage2_pass)} articles ({dupes} dupes)")

    # â”€â”€ Stage 3: Significance Scoring â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    for art in stage2_pass:
        score, reason = _score_article(art)
        art['stage3_score'] = score
        art['stage3_reason'] = reason

    print(f"  Stage 3 (Significance):    Scored {len(stage2_pass)} articles")

    # â”€â”€ Stage 4: Diversity Ranking â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€â”€
    sorted_arts = sorted(stage2_pass, key=lambda x: x['stage3_score'], reverse=True)

    source_counts = {}
    selected = []
    for art in sorted_arts:
        source = art.get('source', 'Unknown')
        count = source_counts.get(source, 0)
        if count < max_per_source and len(selected) < top_n:
            source_counts[source] = count + 1
            art['stage4_selected'] = True
            art['stage4_rank'] = len(selected) + 1
            art['stage4_reason'] = f"Rank {len(selected)+1} â€” score {art['stage3_score']} â€” {source} ({count+1}/{max_per_source})"
            selected.append(art)
        else:
            if count >= max_per_source:
                art['stage4_selected'] = False
                art['stage4_reason'] = f"Source limit reached: {source} already has {count} articles"
            else:
                art['stage4_selected'] = False
                art['stage4_reason'] = f"Top {top_n} already selected"

    # Add all stage2_pass to trace
    trace.extend(stage2_pass)

    dist = {}
    for a in selected:
        dist[a['source']] = dist.get(a['source'], 0) + 1

    print(f"  Stage 4 (Ranking+Diversity): Top {len(selected)} selected")
    print(f"  Source distribution: {dist}")
    print(f"  âœ… Funnel complete â€” {len(selected)} articles ready for AI analysis")
    print(f"  ðŸ“Š Total trace: {len(trace)} articles documented")

    return selected, trace
