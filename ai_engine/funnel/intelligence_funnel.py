import re
import hashlib
import sys
import os
import html
import unicodedata
from datetime import datetime
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.source_weights import get_source_weights
from matching import kw_match, matched_keywords, any_match

# S66 KEY-MAP: every keyword test below is word-boundary matched via kw_match,
# NOT raw substring. Substring matching fired 'eu' inside 'europe', 'war' inside
# 'warsaw', 'oil' inside 'turmoil', 'sport' inside 'transport'. A trailing '*'
# marks a DELIBERATE stem ('sanction*' -> sanctions, sanctions-hit). Default
# policy: star every pluralizable head noun; exact matching is the exception and
# carries an inline reason. Irregular plurals (-y/-ies, -is/-es) stay exact --
# kw_match does not stem them and substring never caught them either.

# ============================================================
# GNI Intelligence Funnel v3 â€” Day 6
# Now returns full article trace for Explainable AI
# Each article carries pass/fail + reason at every stage
# ============================================================

# PHI-003 "Freedom From Fear" keyword set (§5, S44): mass mobilization /
# crackdowns under authoritarian regimes are leading indicators of geopolitical
# rupture (UN human-security pillar; civil-resistance scholarship). Folded into
# GEO relevance below (NOT a 4th pillar). All lowercase for substring matching.
# Bare ambiguous acronyms from the brief (PDF, CDM, NUG, FBK) use full forms,
# and bare "Memorial" is omitted, to avoid substring false positives
# (e.g. "pdf" files, "nugget", "memorial day").
PHI003_FREEDOM_FROM_FEAR = [
    # Universal — repression / civil-resistance signals
    'political prisoner*', 'prisoner of conscience', 'arbitrary detention*',
    'enforced disappearance*', 'civil disobedience', 'nonviolent resistance',
    'pro-democracy protest*', 'crackdown*', 'internet shutdown*', 'censorship',
    'dissident*', 'exile*', 'defector*', 'junta*', 'martial law',
    'magnitsky', 'targeted sanctions',
    # 'prisoner of conscience' stays exact: the plural inflects mid-phrase
    # ("prisonerS of conscience"), which a trailing stem cannot reach.
    # Myanmar
    'spring revolution', 'national unity government', "people's defence force",
    'civil disobedience movement', 'tatmadaw',
    # China
    'white paper protest*', 'a4 revolution', 'uyghur*', 'xinjiang', 'tibet*',
    'hong kong', '709 crackdown',
    # Iran
    'woman life freedom', 'mahsa amini', 'hijab protest*', 'irgc', 'evin prison',
    # Russia
    'navalny', 'anti-corruption foundation', 'foreign agent law',
    'mobilization protest*',
    # North Korea
    'kwanliso', 'political prison camp*', 'forced labor', 'forced labour',
    # Belarus
    'tsikhanouskaya', 'viasna', 'bialiatski', '2020 protests',
]

# Stage 1: Relevance keywords
GEOPOLITICAL_KEYWORDS = [
    # Tier 4 — Strategic chokepoints and maritime (GNI unique angle)
    'red sea', 'south china sea', 'strait*', 'hormuz', 'malacca',
    'suez', 'persian gulf', 'bosphorus', 'panama canal', 'arctic',
    'chokepoint*', 'blockade*',
    # Tier 5 — New economy conflicts (fastest growing)
    'ai chips', 'semiconductor*', 'critical minerals', 'rare earth*',
    'lithium', 'cobalt', 'export control*', 'debt trap*', 'belt and road',
    # Tier 1 — Major powers and flashpoints
    # Demonym stems (S66 census): 'iran*' catches Iranian, 'russia*' Russian,
    # 'israel*' Israeli, 'taiwan*' Taiwanese, 'europe*' European -- all real GEO
    # signal that exact matching would drop. 'china'/'ukraine' are NOT stemmable
    # (Chinese/Ukrainian do not extend the country string) and substring never
    # caught them either, so they are unchanged.
    'china', 'russia*', 'iran*', 'israel*', 'ukraine', 'taiwan*',
    'north korea', 'middle east', 'europe*', 'usa',
    # Tier 2 — Conflict and military
    # 'war' is EXACT BY DESIGN: 'war*' would re-admit 'warsaw' -- the very bug
    # this sweep exists to kill. Cost: the plural 'wars' is not matched here.
    'war', 'conflict*', 'military', 'attack*', 'invasion*', 'strike*',
    'missile*', 'nuclear', 'troops', 'weapon*', 'bomb*', 'ceasefire*',
    'sanction*', 'embargo*', 'terrorism', 'extremis*', 'coup*', 'crisis', 'threat*',
    # Tier 3 — Economics and markets
    # 'economy'/'commodity'/'currency' stay exact: -y/-ies is not a stem kw_match
    # can reach, and substring never caught those plurals either.
    'economy', 'trade', 'oil', 'energy', 'inflation', 'tariff*',
    'gdp', 'recession*', 'gas', 'commodity', 'dollar*', 'currency',
    'interest rate*', 'federal reserve', 'export*', 'import*', 'opec',
    # Tier 6 — Diplomacy and governance
    'election*', 'government*', 'president*', 'prime minister*',
    'diplomacy', 'ambassador*', 'alliance*', 'nato', 'eu',
    'united nations', 'security council*', 'geopolit*',
    'protest*', 'revolution*', 'riot*', 'supply chain*',
    # Tier 7 — Humanitarian and global issues
    'refugee*', 'humanitarian', 'famine*', 'drought*', 'climate',
    'pandemic*', 'vaccine*', 'who', 'tension*', 'pacific',
    # Tier 8 — PHI-003 Freedom From Fear (§5): authoritarian crackdown /
    #   civil-resistance early-warning. Folded into GEO, not a 4th pillar.
    *PHI003_FREEDOM_FROM_FEAR,
]

# This list KILLS articles at Stage 1, so a false match is a silent suppression
# -- the opposite risk polarity from the scoring lists. Under substring matching
# 'sport' killed every article containing 'transport', and 'dating' killed
# 'updating' / 'mandating' / 'validating'. Word-boundary matching ends both.
# EXACT BY DESIGN (no star): 'music', 'travel', 'dating', 'cooking', 'viral',
# 'golf', 'fashion', 'entertainment', 'tourism' -- their embedded-match victims
# (musical, travelling, updating, virally, golfing, fashioned) were the bug, not
# a plural we need to keep catching. 'celebrity' stays exact (-y/-ies).
IRRELEVANT_KEYWORDS = [
    'celebrity', 'entertainment', 'movie*', 'music', 'sport*', 'football',
    'basketball', 'tennis', 'golf', 'oscars', 'grammy', 'fashion',
    'recipe*', 'cooking', 'lifestyle*', 'travel', 'tourism', 'wedding*',
    'divorce*', 'dating', 'viral', 'meme*', 'tiktok', 'instagram',
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
    r'you\s+are\s+now\s+a\s+\w+\s+\w+',
    r'disregard\s+\w+\s+(previous|all|above)\s+instructions?',
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
    # Category 10b: exfiltration = verb + data-object + URL, close together.
    # NOT blocking external URLs -- legit articles cite sources constantly.
    # Tightened S44 (arc 6): the old `(send|forward|post|submit|exfiltrate).{0,50}url`
    #   wiped 100% of full-content feeds (WoR/Breaking Defense/Bellingcat/Amnesty/
    #   DFRLab) because "post"/"submit"/"forward"/"send" sit near a link in any HTML
    #   body. Genuine "send all data to X" is still caught by the precise patterns above.
    r'(send|forward|upload|exfiltrate|leak)\b[^\n]{0,30}\b(data|information|results|credentials|content|article)s?\b[^\n]{0,30}https?://',
    # Category 11: PHI-003 manipulation techniques (GNI S35)
    # Peer pressure — consensus without evidence
    r'everyone\s+(agrees|knows|understands|accepts)',
    r'any\s+reasonable\s+(person|analyst|observer)',
    r'no\s+serious\s+(analyst|expert|observer|person)',
    r'obviously\s+(this|the|it|we)',
    r'it\s+is\s+obvious\s+that',
    r'common\s+sense\s+(tells|shows|dictates)',
    # Passive extreme normalization — making extreme acts seem inevitable
    r'(was|is|seems?|appears?)\s+(necessary|inevitable|understandable|justified)\s+(given|considering|in light of)',
    r'what\s+(other\s+)?choice\s+(did|do|does)\s+(they|he|she|it)\s+have',
    r'forced\s+(them|him|her|the)\s+to\s+(attack|strike|retaliate|respond)',
    r'left\s+(with\s+)?no\s+(other\s+)?choice\s+but\s+to',
    # Butterfly Effect — worst-case chain without probability
    r'this\s+could\s+(easily\s+)?lead\s+to\s+.{5,50}(collapse|war|catastrophe|crisis)',
    r'if\s+.{5,50}then\s+.{5,50}(will|must|shall)\s+(collapse|fail|fall|end)',
    r'(domino|cascade|spiral|chain)\s+(effect|reaction|of\s+events)',
    r'(trigger|spark|ignite)\s+(a\s+)?(global|regional|wider|full)',

    r'https?://[^\s]{5,}.{0,30}(api.key|password|token|secret)',
]


def _check_relevance(article: dict) -> tuple[bool, str]:
    """Stage 1: Check if article is geopolitically relevant."""
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    # Check irrelevant first
    for kw in IRRELEVANT_KEYWORDS:
        if kw_match(kw, text):
            return False, f"Irrelevant topic: '{kw}'"

    # Check relevant
    matched = matched_keywords(GEOPOLITICAL_KEYWORDS, text)
    if matched:
        # Item 2 S38: store match count in article for Stage 3 density bonus
        article["stage1_match_count"] = len(matched)
        return True, f"Matched keywords: {', '.join(matched[:3])}"

    return False, "No geopolitical keywords found"


# Stage 1b extension: PHI-002 bias attacks (GNI S29 — from Lens protection upgrade)
_PHI002_PATTERNS = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in [
    r'(ethnic|religious|cultural)\s+(traditions?|identity)\s+must\s+(supersede|override|come\s+before)\s+(individual|human)\s+rights',
    r'(group|collective|national|ethnic)\s+rights\s+(outweigh|are\s+more\s+important\s+than|supersede)\s+individual',
    r'(sovereignty|stability|order|security)\s+(requires|demands|necessitates)\s+(limiting|restricting|suspending)\s+(rights|freedoms|democracy)',
    r'democracy\s+(is|was)\s+(a|the)\s+western\s+(invention|concept|imposition|idea)',
    r'(human\s+rights|individual\s+rights)\s+(are|is)\s+(a|the)\s+(western|colonial|imperialist)\s+(concept|invention|tool)',
]]

_SECTARIAN_PATTERNS = [re.compile(p, re.IGNORECASE | re.DOTALL) for p in [
    r'(unnamed|anonymous|unverified|secret)\s+sources?\s+(say|report|claim|allege)\s+(that\s+)?(muslims?|christians?|buddhists?|hindus?|jews?)',
    r'(sources?|insiders?|informants?)\s+(confirm|reveal|expose)\s+(ethnic|religious|minority)\s+(plot|plan|attack|conspiracy)',
    r'(the|this)\s+(ethnic|religious|minority|indigenous)\s+group\s+(is|are)\s+(planning|behind|responsible\s+for)',
    r'(foreign|outside|external)\s+(agents?|forces?|powers?)\s+(are\s+)?(using|funding|arming)\s+(ethnic|religious|minority)',
    r'(ethnic|religious|cultural|sectarian)\s+(cleansing|war|conflict|tension)\s+(is|has)\s+(begun|started|erupted|inevitable)',
]]

# 'shell company' stays exact (-y/-ies). 'sanctions' is already plural and is
# left verbatim -- starring it would broaden the stuffing FLAG, which is a
# detection threshold, not a scoring signal.
_STUFFING_KW = [
    "sanctions", "dark money", "shell company", "money laundering",
    "oligarch*", "corruption", "energy security", "critical minerals",
    "food security", "military alliance*", "coup*", "sovereignty",
    "debt trap*", "financial warfare", "cyber attack*", "surveillance",
    "disinformation", "propaganda", "sectarian", "ethnic cleansing",
]


# ============================================================
# LAYER 1: Unicode normalization for the injection scan (S52 7-layer step 1).
# Lifted (copied) from keyword_sensor._normalize_text -- the dormant module is
# NOT imported. NFC -> NFKC here so compatibility forms (full-width, etc.) fold
# to ASCII and cannot be used to evade the 81-pattern scan. DETECTION-ONLY:
# _check_injection normalizes a LOCAL scan copy; the article's title/summary are
# never mutated (non-English content reaches MAD/readers untouched).
# ============================================================
_HOMOGLYPHS = {
    'а': 'a', 'е': 'e', 'о': 'o', 'р': 'p',
    'с': 'c', 'ѕ': 's', 'і': 'i', 'ј': 'j',
    'ɡ': 'g', 'ʜ': 'h', 'ĸ': 'k', 'ʟ': 'l',
    'ɴ': 'n', 'ᴛ': 't', 'ᴜ': 'u', 'ᴠ': 'v',
    'ᴡ': 'w', 'ʏ': 'y', 'Α': 'A', 'Β': 'B',
    'Ε': 'E', 'Ζ': 'Z', 'Η': 'H', 'Ι': 'I',
    'Κ': 'K', 'Μ': 'M', 'Ν': 'N', 'Ο': 'O',
    'Ρ': 'P', 'Τ': 'T', 'Υ': 'Y', 'Χ': 'X',
}

_INVISIBLE_CHARS = {
    '​', '‌', '‍', '⁠', '﻿', '­',
}


def _normalize_text_funnel(text: str) -> str:
    """Fold homoglyph/invisible/entity/full-width evasions to plain ASCII so the
    injection patterns scan the real payload. Pure (stdlib only), no side effects."""
    text = unicodedata.normalize('NFKC', text)
    text = ''.join(ch for ch in text if ch not in _INVISIBLE_CHARS)
    text = ''.join(_HOMOGLYPHS.get(ch, ch) for ch in text)
    text = html.unescape(text)
    text = ''.join(
        ch for ch in text
        if (ch.isascii() and (ch.isprintable() or ch == ' '))
    )
    return text.strip()


def _check_injection(article: dict) -> tuple[str, str]:
    """Stage 1b: Check for adversarial content.

    Returns (action, reason):
      REMOVE — direct prompt injection → drop article entirely
      FLAG   — Lens-style bias/sectarian attack → include with warning tag
      PASS   — clean article
    GNI S29: upgraded from (bool, str) to (str, str) for FLAG support.
    """
    # LAYER 1 (S52): normalize a LOCAL scan copy only -- never mutate the article.
    raw = f"{article.get('title', '')} {article.get('summary', '')}"
    text = _normalize_text_funnel(raw).lower()

    # Check direct injection patterns (REMOVE)
    for pattern in INJECTION_PATTERNS:
        if re.search(pattern, text, re.IGNORECASE):
            return "REMOVE", f"Injection pattern: {pattern[:40]}"

    # Check PHI-002 bias attacks (FLAG — attack is intelligence signal)
    for pattern in _PHI002_PATTERNS:
        if pattern.search(text):
            return "FLAG", "PHI-002 bias attack detected — included with warning"

    # Check sectarian trap content (FLAG — manufactured division is signal)
    for pattern in _SECTARIAN_PATTERNS:
        if pattern.search(text):
            return "FLAG", "Sectarian trap content — unsourced ethnic/religious claim"

    # Check indicator stuffing (short article, too many indicator keywords)
    word_count = len(text.split())
    if word_count < 150:
        hits = sum(1 for kw in _STUFFING_KW if kw_match(kw, text))
        if hits >= 8:
            return "FLAG", f"Indicator stuffing: {hits} keywords in {word_count}-word article"

    return "PASS", "Clean — no injection patterns"


def _get_dedup_key(article: dict) -> str:
    """Generate deduplication key from title."""
    title = article.get('title', '').lower().strip()
    title = re.sub(r'[^a-z0-9\s]', '', title)
    words = title.split()[:6]
    return hashlib.md5(' '.join(words).encode()).hexdigest()


# ── Source Tier System (from LENS experience) ────────────────────────────────
# Tier-based baseline bonus independent of GPVS EMA weights.
# EMA weights take months to become reliable (~100+ observations).
# Tiers give correct relative trust from day one.
# STATE: wire services (highest factual accuracy, institutional trust)
# TIER1: deep editorial standards, specialist expertise
# TIER2: solid reporting, regional or thematic strength
# TIER3: specialist/niche — valuable content, lower editorial baseline
SOURCE_TIERS = {
    # STATE — Wire services
    'NPR World News': 'TIER2',  # replaced Reuters (RSS dead)
    'AP News via Google News': 'STATE',
    # TIER1 — Highest credibility
    'BBC': 'TIER1',
    'The Economist': 'TIER1',
    'Human Rights Watch': 'TIER1',
    'Bellingcat': 'TIER1',
    'EFF Deeplinks': 'TIER1',
    'Foreign Policy': 'TIER1',
    'The Diplomat': 'TIER1',
    'DW News': 'TIER1',
    'France 24': 'TIER1',
    'The Conversation': 'TIER1',
    # TIER2 — Solid credibility
    'Project Syndicate': 'TIER2',
    'Financial Times': 'TIER2',
    'Al Jazeera': 'TIER2',
    'MIT Technology Review': 'TIER2',
    'Krebs on Security': 'TIER2',
    'Rest of World': 'TIER2',
    'Washington Post': 'TIER2',   # reserve source
    'AllAfrica': 'TIER2',          # reserve source
    'Mail and Guardian': 'TIER2',  # reserve source
    'The Independent': 'TIER2',    # reserve source
    'Radio Free Europe': 'TIER2',  # reserve source
    'New York Times': 'TIER2',     # reserve source
    # TIER3 — Specialist / regional (good content, lower editorial baseline)
    # All unlisted sources default to TIER3 (0 pts)
}
TIER_BONUS = {'STATE': 5, 'TIER1': 3, 'TIER2': 1, 'TIER3': 0}


def _score_article(article: dict) -> tuple[float, str]:
    """Stage 3: Score article by significance."""
    score = 0.0
    reasons = []

    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()

    # High-impact keywords (+3 each, max 15) — Tier 4 + Tier 5 (GNI unique angle)
    high_impact = [
        'red sea', 'hormuz', 'malacca', 'suez', 'chokepoint*',
        'blockade*', 'persian gulf', 'south china sea', 'arctic',
        'ai chips', 'critical minerals', 'semiconductor*', 'rare earth*',
        'lithium', 'cobalt', 'debt trap*', 'belt and road', 'export control*',
    ]
    hi_matches = matched_keywords(high_impact, text)
    hi_score = min(len(hi_matches) * 3, 15)
    score += hi_score
    if hi_matches:
        reasons.append(f"High-impact terms ({hi_score}pts): {', '.join(hi_matches[:3])}")

    # Medium-impact keywords (+1 each, max 10) — Tier 1 + Tier 2
    med_impact = [
        # 'war' exact by design (see GEOPOLITICAL_KEYWORDS: 'war*' re-admits 'warsaw').
        # 'crisis' exact: -is/-es plural is not a stem kw_match can reach.
        # Demonym stems mirror GEOPOLITICAL_KEYWORDS (Iranian/Russian/Israeli/Taiwanese).
        'war', 'nuclear', 'invasion*', 'attack*', 'crisis',
        'sanction*', 'ceasefire*', 'coup*', 'collapse*', 'embargo*',
        'china', 'russia*', 'iran*', 'israel*', 'ukraine', 'taiwan*', 'north korea',
        'military', 'troops', 'missile*', 'tension*',
    ]
    med_matches = matched_keywords(med_impact, text)
    med_score = min(len(med_matches), 10)
    score += med_score
    if med_matches:
        reasons.append(f"Medium-impact terms ({med_score}pts): {', '.join(med_matches[:3])}")

    # Major country/region bonus (+5)
    major_regions = [
        # 'europe*' mirrors GEOPOLITICAL_KEYWORDS/med_impact -- same demonym class,
        # same left-boundary safety. The lists must agree on European.
        'middle east', 'europe*', 'usa', 'pacific',
        'economy', 'oil', 'trade', 'inflation', 'election*',
    ]
    region_matches = matched_keywords(major_regions, text)
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

    # Source tier bonus (independent of EMA — active from day one)
    source_name = article.get('source', '')
    tier = SOURCE_TIERS.get(source_name, 'TIER3')
    tier_pts = TIER_BONUS.get(tier, 0)
    if tier_pts > 0:
        score += tier_pts
        reasons.append(f"Source tier {tier} (+{tier_pts}pts): {source_name}")

    # ── THREAT keywords (+4 each, max 20) ─────────────────────────────
    # Direct aggression, attacks, hostile actions -- global perspective
    WT_THREAT_KEYWORDS = [
        # Geo threats -- 'mass atrocity' exact (-y/-ies).
        'war crime*', 'genocide', 'ethnic cleansing', 'civilian massacre*',
        'chemical weapon*', 'biological weapon*', 'nuclear threat*',
        'proxy war*', 'false flag*', 'covert operation*',
        'assassination*', 'targeted killing*', 'extrajudicial killing*',
        'ethnic persecution', 'political prisoner*', 'forced labour',
        'child soldier*', 'mass detention*', 'enforced disappearance*',
        'torture', 'sexual violence', 'mass atrocity',
        # Financial threats
        'financial contagion', 'bank run*', 'currency attack*',
        'economic coercion', 'financial warfare', 'swift exclusion',
        'sovereign default*', 'speculative attack*', 'asset freeze*',
        'economic blockade*', 'financial isolation', 'economic weapon*',
        # Tech threats
        'infrastructure cyberattack*', 'power grid attack*', 'hospital ransomware',
        'election interference', 'state sponsored hacking', 'zero day exploit*',
        'autonomous weapon*', 'deepfake propaganda', 'satellite attack*',
        'information warfare', 'influence operation*', 'disinformation campaign*',
    ]
    threat_matches = matched_keywords(WT_THREAT_KEYWORDS, text)
    threat_score = min(len(threat_matches) * 4, 20)
    score += threat_score
    if threat_matches:
        reasons.append("THREAT signal (" + str(threat_score) + "pts): " + ", ".join(threat_matches[:3]))

    # ── WEAKNESS keywords (+3 each, max 15) ───────────────────────────
    # Vulnerabilities, failures, fragilities -- global perspective
    WT_WEAKNESS_KEYWORDS = [
        # Geo weakness -- '...crisis' entries exact (-is/-es).
        'state collapse', 'failed state*', 'governance failure*',
        'democratic backsliding', 'authoritarian crackdown*',
        'institutional breakdown*', 'alliance fracture*', 'diplomatic breakdown*',
        'peace deal collapse', 'ceasefire violation*', 'power vacuum*',
        'press suppression', 'judicial independence', 'corruption crisis',
        # Financial weakness
        'food insecurity', 'supply chain collapse', 'hyperinflation',
        'foreign reserve depletion', 'fiscal crisis', 'currency devaluation*',
        'commodity shock*', 'harvest failure*', 'poverty trap*',
        'inequality crisis', 'wage suppression', 'remittance cut*',
        'energy poverty', 'import dependency',
        # Tech weakness -- '...vulnerability'/'tech monopoly' exact (-y/-ies).
        'critical infrastructure vulnerability', 'chip dependency',
        'internet fragmentation', 'digital divide', 'single point of failure',
        'data sovereignty', 'legacy system*', 'cyber vulnerability',
        'platform dependency', 'tech monopoly', 'algorithmic discrimination',
    ]
    weakness_matches = matched_keywords(WT_WEAKNESS_KEYWORDS, text)
    weakness_score = min(len(weakness_matches) * 3, 15)
    score += weakness_score
    if weakness_matches:
        reasons.append("WEAKNESS signal (" + str(weakness_score) + "pts): " + ", ".join(weakness_matches[:3]))

    # ── DARK SIDE keywords (+4 each, max 20) ──────────────────────────
    # Good systems created for benefit, weaponised for harm
    # Responsible civic intelligence -- surface dual-use harm
    WT_DARK_SIDE_KEYWORDS = [
        # Geo dark side -- humanitarian and diplomatic systems weaponised
        # 'shell company'/'kleptocracy' exact (-y/-ies). 'food as weapon' and
        # 'water as weapon' exact: fixed idioms, never pluralised in print.
        'debt trap diplomacy', 'energy blackmail', 'food as weapon',
        'water as weapon', 'refugee weaponisation', 'migration weapon*',
        'sanctions evasion', 'money laundering', 'human trafficking',
        'golden passport*', 'citizenship scheme*', 'shell company',
        'aid conditionality', 'cultural suppression',
        # Financial dark side -- finance created for growth, used for harm
        'crypto terrorism', 'ransomware payment*', 'dark money',
        'illicit finance', 'predatory lending', 'development aid corruption',
        'infrastructure debt trap*', 'offshore tax evasion',
        'financial crime*', 'kleptocracy', 'oligarch wealth',
        # Tech dark side -- technology created for good, weaponised
        'mass surveillance', 'facial recognition abuse', 'social credit',
        'internet shutdown*', 'digital authoritarianism', 'spyware abuse',
        'pegasus', 'stalker software', 'surveillance state*',
        'social media manipulation', 'algorithmic suppression',
        'biometric persecution', 'drone surveillance abuse',
        'predictive policing abuse', 'vpn ban*', 'encrypted communication ban*',
        'deepfake abuse', 'ai generated propaganda',
    ]
    dark_matches = matched_keywords(WT_DARK_SIDE_KEYWORDS, text)
    dark_score = min(len(dark_matches) * 4, 20)
    score += dark_score
    if dark_matches:
        reasons.append("DARK SIDE signal (" + str(dark_score) + "pts): " + ", ".join(dark_matches[:3]))


    # ── OPPORTUNITY/STRENGTH keywords (+3 each, max 15) — PHI-003 B ──────
    # Positive-signal content — PHI-003 all-directions principle
    # Rewards balanced reporting, not just threat detection
    WT_OPPORTUNITY_KEYWORDS = [
        # Diplomatic breakthroughs
        # Verb-final entries ('sanctions lifted', 'treaty signed') stay exact --
        # the head is a participle, not a pluralisable noun.
        'peace agreement*', 'peace deal signed', 'ceasefire agreement*',
        'diplomatic breakthrough*', 'diplomatic progress', 'peace talks progress',
        'alliance strengthened', 'alliance formed', 'treaty signed',
        'sanctions lifted', 'sanctions removed', 'embargo lifted',
        'normalisation', 'normalization', 'diplomatic ties restored',
        # Trade and economic progress
        'trade agreement*', 'trade deal*', 'trade framework*',
        'tariff reduction*', 'tariff cut*', 'tariff eliminated',
        'debt relief', 'debt forgiven', 'aid delivered',
        'investment agreement*', 'economic partnership*',
        # Humanitarian progress
        'humanitarian corridor*', 'aid corridor opened',
        'food security improved', 'famine averted',
        'refugee return*', 'displaced persons return',
        'reconstruction begins', 'rebuilding begins',
        # Technology and governance advances
        'technology transfer*', 'technology cooperation',
        'digital rights protected', 'press freedom restored',
        'democratic election*', 'election certified',
        'accountability established', 'justice served',
        'renewable energy', 'clean energy agreement*',
    ]
    opp_matches = matched_keywords(WT_OPPORTUNITY_KEYWORDS, text)
    opp_score = min(len(opp_matches) * 3, 15)
    score += opp_score
    if opp_matches:
        reasons.append("OPPORTUNITY signal (" + str(opp_score) + "pts): " + ", ".join(opp_matches[:3]))


    # ── HUMAN SECURITY keywords (+3 each, max 12) — PHI-003 NN-PHI-1 ──
    # Item 1 S38: PHI-003 says GNI serves humans not markets
    # Human rights/security content now visible in scoring formula
    WT_HUMAN_SECURITY_KEYWORDS = [
        # Civilian impact
        'civilian casualties', 'civilian deaths', 'civilian harm',
        'civilian population*', 'civilian infrastructure',
        # Humanitarian -- 'crisis'/'emergency' exact (-is/-es, -y/-ies).
        'humanitarian crisis', 'humanitarian aid', 'humanitarian corridor*',
        'humanitarian access', 'humanitarian emergency',
        # Rights and freedoms
        'human rights violation*', 'arbitrary detention*',
        'political prisoner*', 'freedom of press', 'internet shutdown*',
        # 'enforced disappearance*' is the canonical UN term and already lives in
        # PHI003_FREEDOM_FROM_FEAR and WT_THREAT -- the lists must agree. Substring
        # matching only ever caught it here by accident ('forced' inside 'enforced').
        'censorship', 'forced disappearance*', 'enforced disappearance*',
        # Displacement
        'refugee crisis', 'internally displaced', 'displacement crisis',
        # Protection
        'war crime*', 'ethnic cleansing', 'genocide',
        'hospital attack*', 'school attack*', 'medical access blocked',
        # Health and basic needs
        'disease outbreak*', 'famine', 'food insecurity',
        'clean water access', 'medical humanitarian',
    ]
    hs_matches = matched_keywords(WT_HUMAN_SECURITY_KEYWORDS, text)
    hs_score = min(len(hs_matches) * 3, 12)
    score += hs_score
    if hs_matches:
        reasons.append("HUMAN SECURITY signal (" + str(hs_score) + "pts): " + ", ".join(hs_matches[:3]))

    # ── STAGE 1 DENSITY BONUS (+0.3 per match, max 8) — Item 2 S38 ──
    # Use match count stored by _check_relevance
    # Article with 20 keyword matches is more significant than one with 2
    s1_count = article.get('stage1_match_count', 0)
    if s1_count > 0:
        density_bonus = round(min(s1_count * 0.3, 8), 1)
        score += density_bonus
        reasons.append(f"Stage1 density ({density_bonus}pts): {s1_count} keyword matches")

    # ── PHI-003 BALANCE SIGNAL (+3) — Change A ───────────────────────
    # Rewards articles covering BOTH positive AND negative dimensions
    # Encodes PHI-003 all-directions principle: balanced > pure fear
    has_threat_signal = (threat_score > 0 or weakness_score > 0 or dark_score > 0)
    has_opportunity_signal = (opp_score > 0)
    if has_threat_signal and has_opportunity_signal:
        score += 3
        reasons.append("PHI-003 balance signal (+3pts): covers both threat and opportunity")


    # ── CONTRADICTION DETECTION (+3) — PHI-003 contested stories ────
    # Stories with contested claims need honest analysis more than settled ones
    # Directly aligned with MAD protocol — perfect debate input
    import re as _re_c
    CONTRADICTION_PATTERNS = [
        r'\b(denied|denies|deny)\b',
        r'\b(rejected|rejects|reject)\b',
        r'\b(disputed|disputes|dispute)\b',
        r'\b(contradicts|contradicted|contradiction)\b',
        r'\b(accused|accuses|accuse)\b.{0,50}\b(denied|denies)\b',
        r'\bsays.{0,80}(but|however|while|whereas).{0,80}(says|claims|insists)\b',
        r'\b(claims?|alleged?|reportedly).{0,50}\b(denied?|rejected?|disputed?)\b',
        r'\bcontrovers(y|ial)\b',
        r'\bdisagreement\b',
        r'\bconflicting (reports?|accounts?|claims?)\b',
    ]
    contradiction_hits = sum(1 for p in CONTRADICTION_PATTERNS
                            if _re_c.search(p, text, _re_c.IGNORECASE))
    if contradiction_hits >= 2:
        score += 3
        reasons.append(f"Contradiction signal (+3pts): {contradiction_hits} contested claim patterns")

    # ── PILLAR-SPECIFIC BONUS SCORING (+2 each, max 10) ──────────────
    # Boosts articles that are highly relevant to their assigned pillar
    # so quota selection picks the best-fit article per pillar
    pillar = article.get("pillar", "").lower()

    if pillar == "geo":
        GEO_BONUS = [
            "ceasefire*", "peace deal*", "peace talks", "diplomatic",
            "ambassador*", "state actor*", "proxy war*", "occupation*",
            "territorial", "sovereignty", "humanitarian crisis",
            "civilian*", "refugee*", "displacement", "airstrike*",
            "ground offensive*", "siege*", "blockade*", "military operation*",
            "nato", "alliance*", "security council", "united nations",
            "coup*", "revolution*", "protest*", "uprising*", "civil war*",
        ]
        geo_matches = matched_keywords(GEO_BONUS, text)
        geo_score = min(len(geo_matches) * 2, 10)
        score += geo_score
        if geo_matches:
            reasons.append(f"GEO pillar bonus ({geo_score}pts): {', '.join(geo_matches[:3])}")

    elif pillar == "tech":
        TECH_BONUS = [
            # 'chip' is EXACT BY DESIGN -- stem decision deferred to G-TUNE.
            # 'vulnerability'/'platform monopoly' exact (-y/-ies).
            "artificial intelligence", "machine learning", "deep learning",
            "large language model*", "generative ai", "ai regulation*",
            "semiconductor*", "chip", "nvidia", "tsmc", "intel",
            "export control*", "chip ban*", "advanced chips",
            "cyberattack*", "ransomware", "zero day", "vulnerability",
            "cyber espionage", "state sponsored hacking", "critical infrastructure",
            "digital sovereignty", "internet shutdown*", "surveillance",
            "facial recognition", "quantum computing", "5g", "6g",
            "tech regulation*", "data privacy", "platform monopoly",
        ]
        tech_matches = matched_keywords(TECH_BONUS, text)
        tech_score = min(len(tech_matches) * 2, 10)
        score += tech_score
        if tech_matches:
            reasons.append(f"TECH pillar bonus ({tech_score}pts): {', '.join(tech_matches[:3])}")

    elif pillar == "fin":
        FIN_BONUS = [
            # 'equity'/'monetary policy'/'import duty'/'currency'/'commodity'
            # exact (-y/-ies). 'euro' exact: under substring it fired inside
            # 'europe' -- a FIN bonus on a pure GEO story.
            "stock market*", "equity", "bond*", "yield*", "interest rate*",
            "federal reserve", "central bank*", "monetary policy",
            "inflation", "deflation", "recession*", "gdp growth",
            "tariff*", "trade war*", "trade deal*", "import duty",
            "sanction*", "asset freeze*", "swift", "currency",
            "dollar*", "yuan", "euro", "exchange rate*",
            "oil price*", "energy market*", "opec", "crude",
            "capital flow*", "foreign investment*", "fdi",
            "sovereign debt", "bond yield*", "credit rating*",
            "commodity", "gold", "copper", "lithium price*",
        ]
        fin_matches = matched_keywords(FIN_BONUS, text)
        fin_score = min(len(fin_matches) * 2, 10)
        score += fin_score
        if fin_matches:
            reasons.append(f"FIN pillar bonus ({fin_score}pts): {', '.join(fin_matches[:3])}")



    # -- BM25 RELEVANCE SCORING (+2 each, max 10) -- Commit 3
    # Dynamic relevance vs geopolitical reference corpus
    # Scores higher when article terms match reference query
    # significantly more than other articles in today's pool
    try:
        from rank_bm25 import BM25Okapi as _BM25
        _bm25_query = [
            'geopolitical', 'conflict', 'trade', 'sanction', 'military',
            'diplomatic', 'nuclear', 'economic', 'security', 'intelligence',
            'semiconductor', 'energy', 'alliance', 'crisis', 'escalation',
        ]
        _bm25_doc = text.split()
        _bm25_corpus = [_bm25_doc, _bm25_query]
        _bm25 = _BM25(_bm25_corpus)
        _bm25_scores = _bm25.get_scores(_bm25_query)
        _bm25_val = float(_bm25_scores[0]) if len(_bm25_scores) > 0 else 0.0
        _bm25_pts = min(int(_bm25_val / 2), 10)
        if _bm25_pts > 0:
            score += _bm25_pts
            reasons.append('BM25 relevance (+' + str(_bm25_pts) + 'pts): score=' + str(round(_bm25_val, 2)))
    except ImportError:
        pass

    # -- YAKE KEYWORD EXTRACTION (+2 each, max 10) -- Commit 2
    # Unsupervised extraction -- catches terms static lists miss
    try:
        import yake as _yake
        _yake_ext = _yake.KeywordExtractor(lan='en', n=2, dedupLim=0.7, top=10, features=None)
        _yake_kws = [kw.lower() for kw, sc in _yake_ext.extract_keywords(
            article.get('title','') + ' ' + article.get('summary',''))]
        _geo_domain = [
            'united states', 'european union', 'middle east', 'south china',
            'north korea', 'iran nuclear', 'ukraine war', 'trade war',
            'supply chain', 'interest rate', 'federal reserve', 'oil price',
            'cyber attack', 'artificial intelligence', 'semiconductor chip',
            'climate change', 'human rights', 'united nations', 'nato alliance',
        ]
        _yake_hits = sum(1 for kw in _yake_kws if any(d in kw for d in _geo_domain))
        _yake_score = min(_yake_hits * 2, 10)
        if _yake_score > 0:
            score += _yake_score
            reasons.append('YAKE signal (' + str(_yake_score) + 'pts): ' + str(_yake_kws[:3]))
    except ImportError:
        pass

    # ── Recency bonus (W-15 fix GNI S29) ─────────────────────────────────
    # published_at is set by rss_collector for every article
    # Breaking news (<6h) gets +5pts. Older than 48h gets nothing.
    # Additive (not multiplier) — avoids compounding with trending multiplier
    published_at = article.get('published_at', '')
    if published_at:
        try:
            from datetime import timezone as _tz
            from datetime import datetime as _dt
            pub = _dt.fromisoformat(published_at.replace('Z', '+00:00'))
            hours_old = (_dt.now(_tz.utc) - pub).total_seconds() / 3600
            if hours_old < 6:
                rec_bonus = 5
            elif hours_old < 12:
                rec_bonus = 4
            elif hours_old < 24:
                rec_bonus = 3
            elif hours_old < 36:
                rec_bonus = 2
            elif hours_old < 48:
                rec_bonus = 1
            else:
                rec_bonus = 0
            # Item 14 S38: context-sensitive recency
            # CRITICAL/HIGH escalation: fresh articles matter much more
            # Normal: mild recency bonus only
            _escalation_level = article.get('escalation_level', '')
            _is_critical = 'CRITICAL' in str(_escalation_level).upper() or 'HIGH' in str(_escalation_level).upper()
            # Change C: cap recency bonus for thin content (PHI-003 depth over speed)
            content_score = hi_score + med_score + threat_score + weakness_score + dark_score + opp_score
            # Item 14 S38: escalation-aware cap
            # CRITICAL/HIGH: no cap -- fresh breaking news always valued
            # Normal: cap recency at +2 for thin content (PHI-003 depth over speed)
            if content_score < 5 and rec_bonus > 2 and not _is_critical:
                rec_bonus = 2
            if rec_bonus > 0:
                score += rec_bonus
                reasons.append(f"Recency (+{rec_bonus}pts): {round(hours_old, 1)}h old")

            # Velocity bonus: breaking story signal (fresh + high impact)
            # rec_bonus >= 4 = <12h old | hi_score >= 6 = 2+ high-impact matches
            if rec_bonus >= 4 and hi_score >= 6:
                vel_bonus = 2
                score += vel_bonus
                reasons.append(f"Velocity (+{vel_bonus}pts): breaking story signal")

        except Exception as _rec_e:
            # never let recency calc break scoring -- but never silently either
            print('  [RECENCY-WARN] bonus skipped: ' + str(_rec_e)[:80])

    reason_str = " | ".join(reasons) if reasons else "Base score only"
    return round(score, 2), reason_str



_STOP_WORDS = {
    "a","an","the","and","or","but","in","on","at","to","for","of","with",
    "by","from","is","are","was","were","be","been","has","have","had",
    "will","would","could","should","this","that","these","those","it",
    "its","as","up","out","into","about","over","after","says","said",
    "also","more","than","which","when","where","after","while","their",
    "during","since","before","between","news","report","reuters","press",
}

def _event_deduplicate(articles: list) -> list:
    """Deduplicate events within a pillar and apply trending multiplier.

    Two articles = same event if they share 4+ significant words (5+ chars).
    Keeps highest-scored article per cluster (deduplication).
    Boosts winner score based on how many sources covered the same event (trending).

    trending_multiplier = min(2.0, 1.0 + 0.15 * peer_count)
    Example: Iran covered by 4 sources -> winner score x1.45
    GNI S29: dedup + trending working together correctly.
    """
    # Pass 1: cluster all articles by event
    clusters = []  # each: {kws, best_art, peer_count}
    for art in articles:
        text = f"{art.get('title','')} {art.get('summary','')}".lower()
        words = {w for w in re.findall(r'[a-z]{5,}', text) if w not in _STOP_WORDS}
        matched = None
        for cluster in clusters:
            if len(words & cluster['kws']) >= 4:
                matched = cluster
                break
        if matched is None:
            clusters.append({'kws': words, 'best_art': art, 'peer_count': 1})
        else:
            matched['peer_count'] += 1
            matched['kws'] |= words
            if art.get('stage3_score', 0) > matched['best_art'].get('stage3_score', 0):
                matched['best_art'] = art

    # Pass 2: apply trending multiplier to each cluster winner
    unique = []
    for cluster in clusters:
        art = cluster['best_art']
        peers = cluster['peer_count']
        if peers > 1:
            mult = min(2.0, 1.0 + 0.15 * (peers - 1))
            orig = art.get('stage3_score', 0)
            art['stage3_score'] = round(orig * mult, 2)
            art['trending_peer_count'] = peers
            art['trending_multiplier'] = round(mult, 2)
            art['trending_original_score'] = orig
        unique.append(art)

    unique.sort(key=lambda a: a.get('stage3_score', 0), reverse=True)
    return unique


# ============================================================
# Stage 1b Extension: Language Sanitization (NN-6 / Gap 2)
# Strips emotionally loaded vocabulary before articles reach MAD.
# Replaced phrases logged as sanitization evidence on each article.
# ============================================================
SANITIZE_VOCAB = [
    ('catastrophic', 'significant'), ('catastrophically', 'significantly'),
    ('devastating', 'damaging'), ('devastation', 'damage'),
    ('apocalyptic', 'severe'), ('existential threat', 'serious risk'),
    ('unprecedented crisis', 'major crisis'), ('unprecedented', 'notable'),
    ('shocking', 'notable'), ('alarming', 'concerning'),
    ('terrifying', 'serious'), ('horrifying', 'serious'),
    ('explosive growth', 'rapid growth'), ('explosive', 'rapid'),
    ('skyrocketing', 'rising sharply'), ('plummeting', 'falling sharply'),
    ('crashing', 'declining'), ('collapsing', 'declining sharply'),
    ('breaking news', 'recent report'), ('breaking:', 'report:'),
    ('urgent:', 'update:'), ('emergency alert', 'alert'),
    ('imminent threat', 'potential threat'), ('imminent danger', 'potential risk'),
    ('time is running out', 'deadline approaches'),
    ('act now', 'action needed'), ('must act immediately', 'action advised'),
    ('puppet government', 'allied government'), ('regime', 'government'),
    ('invasion', 'military operation'), ('occupation', 'military presence'),
    ('terror attack', 'attack'), ('terrorist', 'armed group'),
    ('aggressor', 'initiating party'), ('war criminal', 'accused official'),
    ('western aggression', 'western action'), ('nato aggression', 'nato action'),
    ('us imperialism', 'us policy'), ('imperialist', 'foreign'),
    ('puppet state', 'allied state'), ('proxy war', 'indirect conflict'),
    ('hegemon', 'dominant power'), ('hegemony', 'dominance'),
    ('definitely will', 'may'), ('certainly will', 'may'),
    ('guaranteed to', 'likely to'), ('inevitable', 'probable'),
    ('without doubt', 'likely'), ('undeniably', 'arguably'),
    ('everyone knows', 'it is reported'), ('clearly shows', 'suggests'),
]


def _sanitize_article(art: dict) -> dict:
    """Strip emotionally loaded vocabulary from title + summary.
    Replaced terms logged in art['sanitized_terms'] as injection evidence.
    Never removes articles. Silent on failure. NN-6 / Gap 2.
    """
    try:
        import re as _re
        replaced = []
        for field in ['title', 'summary']:
            text = art.get(field, '')
            if not text:
                continue
            for loaded, neutral in SANITIZE_VOCAB:
                text, n = _re.subn(_re.escape(loaded), neutral, text, flags=_re.IGNORECASE)
                if n > 0:
                    replaced.append(loaded)
            art[field] = text
        art['sanitized_terms'] = replaced
        art['sanitization_flag'] = len(replaced) > 0
        if replaced:
            existing = art.get('stage1b_reason', '')
            art['stage1b_reason'] = existing + f' | Sanitized: {replaced[:3]}'
    except Exception:
        art['sanitized_terms'] = []
        art['sanitization_flag'] = False
    return art



# ============================================================
# Option F Content Type Classifier (GNI S35 — PHI-003 U-4)
# 4-layer hybrid classifier: source → URL → heuristic → LLM
# Output: news | news_with_review | review_only
# ============================================================

# Layer 1: Known review-only sources (state media / adversarial)
_REVIEW_ONLY_SOURCES = {
    'rt', 'russia today', 'cgtn', 'press tv', 'presstv',
    'al-mayadeen', 'al mayadeen', 'telesur', 'global times',
}

# Layer 2: URL patterns indicating opinion/analysis content
_REVIEW_URL_PATTERNS = [
    r'/opinion/', r'/opinions/', r'/commentary/', r'/comment/',
    r'/analysis/', r'/analyse/', r'/editorial/', r'/editorials/',
    r'/perspective/', r'/perspectives/', r'/column/', r'/columns/',
    r'/blog/', r'/blogs/', r'/letters/', r'/forum/',
    r'\?.*type=opinion', r'\?.*section=opinion',
]

# Layer 3: Structural heuristics — review/opinion language signals
_REVIEW_HEURISTIC_PATTERNS = [
    # First person authorial voice
    r'\bi\s+(think|believe|argue|contend|submit|hold|maintain)\b',
    r'\bin\s+my\s+(view|opinion|assessment|judgment)\b',
    r'\bmy\s+(argument|thesis|point|contention|view)\b',
    # Prescriptive/normative language
    r'\b(should|must|ought\s+to|needs?\s+to)\s+\w+\s+(its?|their|the|a)\b',
    r'\bwe\s+(should|must|need\s+to|ought\s+to)\b',
    r'\bthe\s+\w+\s+(must|should|needs?\s+to)\b',
    # Explicit opinion markers
    r'\b(in\s+my|from\s+my)\s+(view|perspective|experience|reading)\b',
    r'\bthe\s+author\s+(argues?|contends?|believes?|suggests?)\b',
    r'\bthis\s+(essay|column|commentary|analysis|piece)\s+(argues?|examines?|explores?)\b',
]

_REVIEW_URL_RE = [__import__("re").compile(p, __import__("re").IGNORECASE) for p in _REVIEW_URL_PATTERNS]
_REVIEW_HEU_RE = [__import__("re").compile(p, __import__("re").IGNORECASE) for p in _REVIEW_HEURISTIC_PATTERNS]


def _classify_content_type(article: dict) -> dict:
    """Option F: 4-layer content type classifier.
    Sets article['content_type'] to: news | news_with_review | review_only
    Sets article['content_type_signals'] with layer evidence.
    Layer 4 (LLM) fires only when Layers 1-3 disagree (ambiguous ~20-30%).
    """
    signals = []
    review_votes = 0

    # Layer 1: Source pre-classification
    source = article.get("source", "").lower().strip()
    source_ct = article.get("content_type", "news")  # from rss_collector
    if source_ct == "review_only" or source in _REVIEW_ONLY_SOURCES:
        review_votes += 1
        signals.append("L1:source=review_only")
    else:
        signals.append(f"L1:source=news({source_ct})")

    # Layer 2: URL pattern matching
    url = article.get("link", "").lower()
    url_review = any(p.search(url) for p in _REVIEW_URL_RE)
    if url_review:
        review_votes += 1
        signals.append("L2:url=review_signal")
    else:
        signals.append("L2:url=news")

    # Layer 3: Structural heuristics
    text = f"{article.get('title', '')} {article.get('summary', '')}".lower()
    heu_hits = sum(1 for p in _REVIEW_HEU_RE if p.search(text))
    if heu_hits >= 2:
        review_votes += 1
        signals.append(f"L3:heuristic=review({heu_hits} hits)")
    else:
        signals.append(f"L3:heuristic=news({heu_hits} hits)")

    # Decision: 2+ votes = review confirmed, skip Layer 4
    # 0-1 votes but ambiguous = Layer 4 (LLM) — stubbed for now
    if review_votes >= 2:
        ct = "review_only" if review_votes == 3 else "news_with_review"
        signals.append(f"L4:skipped(consensus={review_votes}/3)")
    elif review_votes == 1:
        # Layer 3b: Enhanced heuristics before LLM
        title_lower = article.get("title", "").lower()
        url_lower = article.get("link", "").lower()
        # S66 KEY-MAP C4 fix 1: this was `"by " + title_lower[:3] in title_lower`, a
        # precedence accident -- it concatenated FIRST, so a title beginning "The..."
        # was tested for the string "by the". It never detected a byline. The S64 GN
        # author-page class is a title that STARTS with one.
        # Fix 2: the opinion phrases are matched on word boundaries over the same
        # lowered title+summary the sibling Layer 3 check uses, not a re-derived copy.
        # They stay exact -- fixed idioms, nothing to stem.
        l3b_review = (
            title_lower.startswith(("opinion:", "analysis:", "commentary:", "column:", "perspective:"))
            or "/opinion/" in url_lower or "/analysis/" in url_lower
            or title_lower.startswith("by ")
            or any_match(["i think", "i believe", "in my view", "we must", "we should"], text)
        )
        if l3b_review:
            ct = "news_with_review"
            signals.append("L3b:enhanced_heuristic=review")
            signals.append("L4:skipped(L3b_resolved)")
        else:
            # Layer 4: LLM spot-check — hard cap 5 calls per run via module-level counter
            import os as _os
            _l4_used = int(_os.environ.get("_GNI_L4_CALLS", "0"))
            _l4_cap = 5
            if _l4_used < _l4_cap:
                try:
                    import requests as _req
                    _groq_key = _os.getenv("GROQ_API_KEY", "")
                    _groq_url = "https://api.groq.com/openai/v1/chat/completions"
                    _l4_prompt = (
                        f"Is this article primarily opinion/analysis/review, or factual news reporting?\n"
                        f"Title: {article.get('title','')}\n"
                        f"Summary: {article.get('summary','')[:200]}\n"
                        f"Answer with one word only: OPINION or NEWS"
                    )
                    _resp = _req.post(_groq_url,
                        headers={"Authorization": f"Bearer {_groq_key}", "Content-Type": "application/json"},
                        json={"model": "llama-3.1-8b-instant", "messages": [{"role": "user", "content": _l4_prompt}],
                              "max_tokens": 5, "temperature": 0},
                        timeout=10)
                    if _resp.status_code == 200:
                        _l4_ans = _resp.json()["choices"][0]["message"]["content"].strip().upper()
                        ct = "news_with_review" if "OPINION" in _l4_ans else "news"
                        _os.environ["_GNI_L4_CALLS"] = str(_l4_used + 1)
                        signals.append(f"L4:llm={_l4_ans}(call {_l4_used+1}/{_l4_cap})")
                    else:
                        ct = "news"
                        signals.append("L4:llm_error→news")
                except Exception:
                    ct = "news"
                    signals.append("L4:llm_exception→news")
            else:
                ct = "news"
                signals.append(f"L4:cap_reached({_l4_cap})→news")
    else:
        ct = "news"
        signals.append("L4:skipped(clear_news)")

    article["content_type"] = ct
    article["content_type_signals"] = " | ".join(signals)
    article["content_type_review_votes"] = review_votes
    return article

def run_funnel(
    articles: list[dict],
    top_n: int = 11,  # 5 geo + 3 tech + 3 fin
    max_per_source: int = 2,  # D1: reduced from 3 for source diversity (PHI-003)
    excluded_urls: set = None  # S39: cross-run URL dedup set from main.py
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
        action, reason = _check_injection(art)
        art['stage1b_action'] = action
        art['stage1b_reason'] = reason
        art['stage1b_passed'] = (action != 'REMOVE')  # backwards compat
        art['stage2_passed'] = True
        art['stage2_reason'] = 'Not evaluated (failed Stage 1b)'
        art['stage3_score'] = 0.0
        art['stage3_reason'] = 'Not evaluated (failed Stage 1b)'

        if action != 'REMOVE':
            stage1b_pass.append(art)
        else:
            trace.append(art)

    flagged = len(stage1_pass) - len(stage1b_pass)
    print(f"  Stage 1b (Inj. Filter):    {len(stage1_pass)} â†’ {len(stage1b_pass)} articles ({flagged} flagged)")

    # -- Token Limit: max 500 chars per article summary --
    for art in stage1b_pass:
        if len(art.get('title', '')) + len(art.get('summary', '')) > 500:
            art['summary'] = art['summary'][:400]
            art['token_truncated'] = True
        else:
            art['token_truncated'] = False

    # NN-6: Language sanitization -- strip emotional amplification before MAD
    sanitized_count = 0
    for art in stage1b_pass:
        _sanitize_article(art)
        if art.get('sanitization_flag'):
            sanitized_count += 1
    if sanitized_count > 0:
        print(f"  Stage 1b (Sanitize):       {sanitized_count}/{len(stage1b_pass)} articles had emotional language stripped")

    # -- Option F: Content Type Classification (U-4) --
    for art in stage1b_pass:
        _classify_content_type(art)
    review_arts = [a for a in stage1b_pass if a.get("content_type") in ("review_only", "news_with_review")]
    print(f"  Stage 1b (Classifier):     {len(stage1b_pass)} articles classified — {len(review_arts)} review-type detected")


    # -- U-5: Review Acceptance Gate (PHI-003) --
    # review_only / news_with_review must pass BOTH: cause+effect AND fff_path
    # Either missing -> reject (logged). news articles pass unconditionally.
    _CAUSE_EFFECT = re.compile(
        r"\b(because|therefore|as\s+a\s+result|which\s+leads?\s+to|"
        r"consequently|due\s+to|caused\s+by|resulting\s+in|"
        r"this\s+means|leading\s+to|driven\s+by)\b",
        re.IGNORECASE
    )
    _FFF_PATH = re.compile(
        r"\b(can|could|should|advocate|understand|protect|demand|"
        r"empower|transparency|accountability|rights|freedom|"
        r"awareness|action|reform|resist|challenge|hold\s+accountable)\b",
        re.IGNORECASE
    )
    review_gate_pass = []
    review_gate_reject = 0
    for art in stage1b_pass:
        ct = art.get("content_type", "news")
        if ct not in ("review_only", "news_with_review"):
            review_gate_pass.append(art)
            art["review_gate"] = "skipped(news)"
            continue
        text = (art.get("title", "") + " " + art.get("summary", "")).lower()
        has_cause = bool(_CAUSE_EFFECT.search(text))
        has_fff = bool(_FFF_PATH.search(text))
        if has_cause and has_fff:
            review_gate_pass.append(art)
            art["review_gate"] = "passed(cause+fff)"
        else:
            missing = []
            if not has_cause: missing.append("cause+effect")
            if not has_fff: missing.append("fff_path")
            art["review_gate"] = "rejected(missing: " + ", ".join(missing) + ")"
            art["stage1b_passed"] = False
            art["stage1b_reason"] = art.get("stage1b_reason", "") + " | Review gate: missing " + ", ".join(missing)
            review_gate_reject += 1
            trace.append(art)
    stage1b_pass = review_gate_pass
    if review_gate_reject > 0:
        print(f"  Stage 1b (Review Gate):    {review_gate_reject} review articles rejected")

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
        # -- Stage 4: Pillar Quota + Diversity Ranking -----------
    # Quota: 60% Geo (3) + 20% Tech (1) + 20% Fin (1) = 5
    # S39: Cross-run URL deduplication -- exclude URLs selected in last 24h
    if excluded_urls:
        _before_xrun = len(stage2_pass)
        stage2_pass = [a for a in stage2_pass if a.get("link", "") not in excluded_urls]
        _excluded = _before_xrun - len(stage2_pass)
        if _excluded > 0:
            print(f"  Cross-run dedup:           {_excluded} recently-selected URLs excluded ({len(stage2_pass)} remain)")

    PILLAR_QUOTA = {"geo": 14, "tech": 4, "fin": 4}  # Three Pillar Reports: 14/4/4 = 22 total

    sorted_arts = sorted(stage2_pass, key=lambda x: x["stage3_score"], reverse=True)

    # Group by pillar
    by_pillar = {"geo": [], "tech": [], "fin": []}
    unclassified = []
    for art in sorted_arts:
        pillar = art.get("pillar", "").lower()
        if pillar in by_pillar:
            by_pillar[pillar].append(art)
        else:
            unclassified.append(art)

    selected = []
    source_counts = {}

    # Fill quota per pillar -- highest score first, max_per_source respected
    # GNI S29 W-11: event deduplication applied per pillar before selection
    for pillar in by_pillar:
        by_pillar[pillar] = _event_deduplicate(by_pillar[pillar])

    for pillar, quota in PILLAR_QUOTA.items():
        filled = 0
        for art in by_pillar[pillar]:
            if filled >= quota:
                break
            source = art.get("source", "Unknown")
            count = source_counts.get(source, 0)
            if count < max_per_source:
                source_counts[source] = count + 1
                art["stage4_selected"] = True
                art["stage4_rank"] = len(selected) + 1
                art["stage4_reason"] = (
                    "Pillar quota " + pillar.upper() + " (" + str(filled+1) + "/" + str(quota) + ")"
                    " -- score " + str(art["stage3_score"])
                )
                selected.append(art)
                filled += 1
            else:
                art["stage4_selected"] = False
                art["stage4_reason"] = "Source limit: " + source + " already has " + str(count)

        # Mark unfilled pillar articles as not selected
        for art in by_pillar[pillar]:
            if not art.get("stage4_selected") and "stage4_reason" not in art:
                art["stage4_selected"] = False
                art["stage4_reason"] = "Pillar quota " + pillar.upper() + " already filled"

    # Fallback: if total < top_n, fill from highest-scoring remaining
    if len(selected) < top_n:
        remaining = [a for a in sorted_arts if not a.get("stage4_selected")]
        for art in remaining:
            if len(selected) >= top_n:
                break
            source = art.get("source", "Unknown")
            count = source_counts.get(source, 0)
            if count < max_per_source:
                source_counts[source] = count + 1
                art["stage4_selected"] = True
                art["stage4_rank"] = len(selected) + 1
                art["stage4_reason"] = "Fallback fill -- score " + str(art["stage3_score"])
                selected.append(art)

    # Mark all unclassified as not selected
    for art in unclassified:
        if not art.get("stage4_selected"):
            art["stage4_selected"] = False
            art["stage4_reason"] = "No pillar assigned"

    # Add all stage2_pass to trace
    trace.extend(stage2_pass)

    dist = {}
    pillar_dist = {"geo": 0, "tech": 0, "fin": 0}
    for a in selected:
        dist[a["source"]] = dist.get(a["source"], 0) + 1
        p = a.get("pillar", "unknown")
        if p in pillar_dist:
            pillar_dist[p] += 1

    print(f"  Stage 4 (Ranking+Diversity): Top {len(selected)} selected")
    print(f"  Pillar distribution: Geo={pillar_dist['geo']}/14 Tech={pillar_dist['tech']}/4 Fin={pillar_dist['fin']}/4 (Three Pillar Reports)")
    print(f"  Source distribution: {dist}")
    print(f"  âœ… Funnel complete â€” {len(selected)} articles ready for AI analysis")
    print(f"  ðŸ“Š Total trace: {len(trace)} articles documented")

    return selected, trace
