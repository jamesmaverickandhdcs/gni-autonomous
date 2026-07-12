# ============================================================
# GNI MAD Grounding Gate (Layer-1) -- S61 SHADOW BUILD
# ------------------------------------------------------------
# Deterministic, model-independent entity/geography/quantity
# fabrication detector for the consultant->agent->arbitrator
# laundering channel (4/4 confirmed specimens, S55-S60).
#
# SHADOW MODE: this module only DETECTS and returns hits. It never
# blocks, never edits text, never changes a verdict. Zero LLM calls,
# zero new dependencies (pure stdlib: re, collections). Because it is
# a pure string check it survives the Aug-16 Groq model cliff.
#
# Rules in force: R-S60-2 (structure != grounding), R-S60-3 (never
# pipe an ungrounded layer into grounded layers unchecked), GNI-R-076
# (basket field names verified against real pipeline_articles schema:
# title / summary / entities -- there is NO `keywords` column; the
# closest analogue is the jsonb `entities` list, so we ground against
# title + summary + entities, plus `keywords` defensively if present).
# ============================================================

import re
from collections import OrderedDict

# ---- Skip vocab: never flag these (agent roles, verdict words, in-scope tickers) ----
ROLE_NAMES = {
    'bull', 'bear', 'swan', 'black swan', 'ostrich', 'arbitrator', 'arbiter',
}
VERDICT_VOCAB = {
    'bullish', 'bearish', 'neutral', 'confidence', 'escalation', 'de escalation',
    'verdict', 'blind spot', 'blind spot quadrant',
}
TICKERS = {'spy', 'gld', 'uso'}
# Single common capitalized words (sentence starters / connectives / MAD scaffolding).
COMMON_SKIP = {
    'the', 'a', 'an', 'this', 'that', 'these', 'those', 'it', 'its', 'their',
    'his', 'her', 'our', 'your', 'in', 'on', 'at', 'for', 'and', 'but', 'or',
    'if', 'when', 'while', 'after', 'before', 'during', 'because', 'however',
    'round', 'final', 'opening', 'position', 'positions', 'future', 'threats',
    'threat', 'report', 'risk', 'summary', 'current', 'intelligence', 'debate',
    'history', 'coach', 'push', 'deeper', 'harder', 'maximum', 'name', 'names',
    'i', 'we', 'you', 'they', 'he', 'she', 'no', 'yes', 'not', 'all', 'one',
    'two', 'three', 'jurisdiction', 'grounding', 'tier', 'absolute', 'mission',
    'vision', 'foundation', 'lens', 'quadrant', 'senior', 'analyst',
}
_SKIP_PHRASES = ROLE_NAMES | VERDICT_VOCAB | TICKERS

# ---- Dialect allowlist (GT-1, S67) ----
# MAD prompt vocabulary + contentless filler. These spans carry zero attribution
# content, so they are NOT fabrication: they are reported as kind='dialect' hits
# for observability but never count toward hit_count and never flip `grounded`.
# Normalized forms (lowercase, punctuation stripped) -- compare against _norm().
DIALECT_PREFIXES = (
    'hidden pattern', 'second order', 'third order', 'invisible link',
    'silo gap', 'far reaching',
)
# Reachable today only via Title-Case (_CAP_RE): these are lowercase unhyphenated
# bigrams, which no current extractor pass emits as a candidate span. Becomes fully
# reachable when the G-GAP-1 lowercase-phrase pass lands (GT-3). Kept deliberately.
DIALECT_EXACT = {
    'invisible broker', 'cascading effects', 'knock on effects',
}
# Single abstract nouns from arbitrator list-style output (digest-proven).
ARB_LIST_NOUNS = {
    'cascading', 'contagion', 'erosion', 'emergence', 'diversification',
    'disruption', 'cooperation', 'potential', 'establishment',
}


def _is_dialect(norm: str) -> bool:
    return (norm in DIALECT_EXACT
            or norm in ARB_LIST_NOUNS
            or norm.startswith(DIALECT_PREFIXES))


# ---- Alias groups (GT-2, S67) ----
# All 10 groups verified live against the 513-article 24h corpus (S67 Supabase
# check, R-S66-2 satisfied). Normalized forms. Expansion is CONDITIONAL: see
# _expand_aliases -- a group only becomes grounded vocabulary when the basket
# already contains one of its members.
ALIAS_GROUPS = [
    {'federal reserve', 'the fed', 'us federal reserve', 'fed'},
    {'treasury', 'us treasury', 'us treasury department', 'treasury department'},
    {'european union', 'eu'},
    {'united states', 'us', 'usa', 'u s'},
    {'us iran conflict', 'us iran', 'conflict between the us and iran', 'us iran war'},
    {'iran', 'iranian', 'iranians'},
    {'russia', 'russian', 'russians'},
    {'israel', 'israeli', 'israelis'},
    {'taiwan', 'taiwanese'},
    {'europe', 'european', 'europeans'},
]


def _expand_aliases(basket_norm: str) -> str:
    """Conditionally widen the grounded corpus with alias variants (GT-2).

    If ANY member of a group is present in the basket as a whole token/phrase,
    every member of that group is appended. CONDITIONAL BY DESIGN: a Fed span
    checked against a Fed-free basket must STILL fire, so we never expand
    unconditionally. Quantities are unaffected (they ground against basket_raw).
    """
    padded = ' ' + basket_norm + ' '
    extra = []
    for group in ALIAS_GROUPS:
        if any((' ' + member + ' ') in padded for member in group):
            extra.extend(sorted(group))
    if not extra:
        return basket_norm
    return basket_norm + ' ' + ' '.join(extra)


# ---- Extraction patterns ----
# 1. Proper-noun sequences: one or more consecutive Capitalized words.
_CAP_RE = re.compile(r'[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*')
# 2. Hyphenated / compound noun phrases: a hyphen-joined token, optionally
#    followed by ONE lowercase head noun ("dollar-depegging", "rare-earth broker").
_COMPOUND_RE = re.compile(r'[A-Za-z]+(?:-[A-Za-z]+)+(?:\s+[a-z]+)?')
# Function words wrongly captured as that optional head noun ("silo-gap between"):
# strip them off the span before normalization (GT-2 item 3).
STOP_HEADS = {'between', 'and', 'of', 'with', 'to', 'in', 'on', 'for',
              'that', 'which'}
# 3a. Quantity: number (+/- currency) followed by a unit/scale token.
_QTY_RE = re.compile(
    r'\$?\s?\d[\d,]*(?:\.\d+)?\s*'
    # `%` carries no trailing \b (it is a non-word char); word units keep \b.
    r'(?:%|(?:percent|percentage points|bps|basis points|billion|billions|'
    r'million|millions|trillion|trillions|thousand|thousands|bn|mn|tn)\b)',
    re.I,
)
# 3b. Scale-of phrases with no digits ("trillions of dollars").
_SCALE_RE = re.compile(
    r'\b(?:trillions|billions|millions|hundreds|thousands|dozens|scores)'
    r'\s+of\s+[a-z]+\b',
    re.I,
)
_DIGIT_RE = re.compile(r'\d[\d.,]*')


def _norm(s: str) -> str:
    """Lowercase, strip punctuation/hyphens to spaces, collapse whitespace."""
    s = s.lower()
    s = re.sub(r'[^a-z0-9\s]', ' ', s)
    return re.sub(r'\s+', ' ', s).strip()


def _basket_corpus(basket, whitelist_extra):
    """Concatenate all groundable text into (normalized, raw-lower) corpora.

    Real pipeline_articles fields (GNI-R-076 verified): title, summary,
    entities (jsonb list). `keywords` is included defensively for forward
    compatibility even though the current schema has no such column.
    """
    parts = []
    for art in (basket or []):
        if not isinstance(art, dict):
            continue
        for field in ('title', 'summary', 'stage3_reason'):
            val = art.get(field)
            if isinstance(val, str):
                parts.append(val)
        for field in ('entities', 'keywords'):
            val = art.get(field)
            if isinstance(val, list):
                parts.extend(str(x) for x in val)
            elif isinstance(val, str):
                parts.append(val)
    for extra in (whitelist_extra or []):
        if isinstance(extra, str):
            parts.append(extra)
    raw = ' '.join(parts).lower()
    return _norm(raw), raw


def _sentence_starts(text: str) -> set:
    """Char indices that begin a sentence (start of text or after . ! ?)."""
    starts = {0}
    for m in re.finditer(r'[.!?]\s+', text):
        starts.add(m.end())
    return starts


def _mask(text: str, spans) -> str:
    """Replace already-claimed spans with spaces (length-preserving)."""
    chars = list(text)
    for start, end in spans:
        for i in range(start, end):
            chars[i] = ' '
    return ''.join(chars)


def _qty_grounded(span: str, basket_norm: str, basket_raw: str) -> bool:
    m = _DIGIT_RE.search(span)
    if m:
        key = m.group(0).rstrip('.,').replace(',', '')
        return bool(key) and key in basket_raw
    scale = re.search(r'(trillion|billion|million|hundred|thousand|dozen|score)',
                      span.lower())
    key = scale.group(1) if scale else _norm(span)
    return bool(key) and key in basket_norm


def check_grounding(text, basket, whitelist_extra=None, location=''):
    """Deterministic Layer-1 grounding check (SHADOW: detect + report only).

    Args:
        text: the checked reply (a consultant or arbitrator output).
        basket: list of article dicts (pipeline_articles rows).
        whitelist_extra: list of extra grounded strings (report title/summary/
            location, Swan FALLOUT headers) supplied by the caller.
        location: optional label stamped onto each hit (e.g. "c1_bull").

    Returns:
        {"hits": [{"span","kind","location"}], "hit_count", "checked_spans",
         "grounded"}  (grounded == hit_count == 0)

    kind=='dialect' hits (GT-1 allowlist) are reported in `hits` but excluded
    from `hit_count` and `grounded` -- they are prompt vocabulary/filler, not
    fabrication. `checked_spans` still counts them.
    """
    result = {'hits': [], 'hit_count': 0, 'checked_spans': 0, 'grounded': True}
    if not text or not isinstance(text, str) or text.startswith('[Agent error'):
        return result

    basket_norm, basket_raw = _basket_corpus(basket, whitelist_extra)
    basket_norm = _expand_aliases(basket_norm)
    sent_starts = _sentence_starts(text)

    # candidates: OrderedDict norm_span -> (raw_span, kind)  (dedup, keep first)
    candidates = OrderedDict()

    # -- pass 1: hyphenated / compound noun phrases (mask so caps/qty don't re-claim) --
    compound_spans = []
    for m in _COMPOUND_RE.finditer(text):
        raw = m.group(0).strip()
        words = raw.split()
        if len(words) > 1 and words[-1].lower() in STOP_HEADS:
            raw = ' '.join(words[:-1])
        norm = _norm(raw)
        if not norm or norm in _SKIP_PHRASES:
            continue
        compound_spans.append((m.start(), m.end()))
        candidates.setdefault(norm, (raw, 'entity'))
    masked = _mask(text, compound_spans)

    # -- pass 2: quantities --
    qty_spans = []
    for rgx in (_QTY_RE, _SCALE_RE):
        for m in rgx.finditer(masked):
            raw = m.group(0).strip()
            norm = _norm(raw)
            if not norm:
                continue
            qty_spans.append((m.start(), m.end()))
            candidates.setdefault('#qty:' + norm, (raw, 'quantity'))
    masked = _mask(masked, qty_spans)

    # -- pass 3: capitalized proper-noun sequences --
    for m in _CAP_RE.finditer(masked):
        words = m.group(0).split()
        stripped_lead = False
        # strip leading/trailing common scaffolding words ("The Bull" -> "Bull")
        while words and words[0].lower() in COMMON_SKIP:
            words.pop(0)
            stripped_lead = True
        while words and words[-1].lower() in COMMON_SKIP:
            words.pop()
        if not words:
            continue
        raw = ' '.join(words)
        norm = _norm(raw)
        if not norm or len(norm) < 3:
            continue
        if norm in _SKIP_PHRASES:
            continue
        single = ' ' not in norm
        if single and norm in COMMON_SKIP:
            continue
        # skip a lone capitalized word at the START of a sentence (only when we
        # did not strip a leading scaffolding word to reach it)
        if single and not stripped_lead and m.start() in sent_starts:
            continue
        candidates.setdefault(norm, (raw, 'entity'))

    # -- grounding test --
    for key, (raw, kind) in candidates.items():
        result['checked_spans'] += 1
        if kind == 'entity' and _is_dialect(_norm(raw)):
            result['hits'].append(
                {'span': raw, 'kind': 'dialect', 'location': location})
            continue
        if kind == 'quantity':
            grounded = _qty_grounded(raw, basket_norm, basket_raw)
        else:
            grounded = _norm(raw) in basket_norm
        if not grounded:
            result['hits'].append({'span': raw, 'kind': kind, 'location': location})

    # GT-1: dialect hits are reported but never counted / never flip `grounded`.
    result['hit_count'] = sum(1 for h in result['hits'] if h['kind'] != 'dialect')
    result['grounded'] = result['hit_count'] == 0
    return result


if __name__ == '__main__':
    # ------------------------------------------------------------------
    # Specimen test block -- synthetic reproductions of the 4 confirmed
    # laundering specimens (S55-S60) against a basket that LACKS them.
    # Run: python ai_engine/analysis/mad_grounding_gate.py
    # ------------------------------------------------------------------
    basket = [{
        'title': 'US sanctions Iran after Hormuz tanker strikes',
        'summary': ('United States naval forces deployed near the Strait of Hormuz '
                    'as oil prices climbed following attacks on three vessels.'),
        'entities': ['Iran', 'Hormuz', 'United States', 'oil'],
        'stage3_score': 8.0,
    }]
    whitelist = ['Iran Threatens Hormuz', 'Iran moved forces to Hormuz.', 'Iran',
                 'Detection Failure', 'Escalation', 'Geopolitical Retaliation']

    failures = []

    def _expect_hit(label, text, needle):
        r = check_grounding(text, basket, whitelist, location='test')
        spans = [h['span'].lower() for h in r['hits']]
        ok = any(needle.lower() in s or s in needle.lower() for s in spans)
        print(f'[{"PASS" if ok else "FAIL"}] specimen {label!r} -> hits={spans}')
        if not ok:
            failures.append(label)

    # Specimen 1 (S55): fabricated "Iranian rare earths / invisible broker"
    _expect_hit('Iranian rare earths',
                'The senior read is that Iranian rare-earth supply is quietly '
                'controlled by an unnamed broker.', 'rare-earth')
    # Specimen 2 (S60): fabricated "Caucasus region" laundered to arbitrator action
    _expect_hit('Caucasus region',
                'A separatist cell operating from the Caucasus region will strike '
                'the pipeline within weeks.', 'caucasus')
    # Specimen 3 (S60): fabricated cryptocurrency angle in blind spot + action
    _expect_hit('cryptocurrency',
                'Contagion then spreads through cryptocurrency-driven bank runs '
                'across the region.', 'cryptocurrency-driven')
    # Specimen 4 (S60): lowercase compound "dollar-depegging" published as Long Shoot
    _expect_hit('dollar-depegging',
                'The tail scenario is a dollar-depegging spiral that drains reserves.',
                'dollar-depegging')

    # Quantity fabrications (benign tier, same channel): unsourced figures
    rq = check_grounding('This wipes out 10% of EU GDP and trillions of dollars.',
                         basket, whitelist, location='test')
    qty_hits = [h['span'] for h in rq['hits'] if h['kind'] == 'quantity']
    qok = len(qty_hits) >= 2
    print(f'[{"PASS" if qok else "FAIL"}] quantity fabrications -> {qty_hits}')
    if not qok:
        failures.append('quantity')

    # Zero-false-positive: agent role names + verdict vocab + GROUNDED entities.
    rn = check_grounding(
        'The Bull and Bear reached a bearish verdict with high confidence after '
        'escalation. Iran and Hormuz over the Strait of Hormuz remain the focus.',
        basket, whitelist, location='test')
    fp_ok = rn['hit_count'] == 0
    print(f'[{"PASS" if fp_ok else "FAIL"}] no false positive on roles/verdict/'
          f'grounded -> hits={[h["span"] for h in rn["hits"]]}')
    if not fp_ok:
        failures.append('false-positive')

    # Dialect allowlist (GT-1): MAD prompt vocab / filler is REPORTED but never
    # counted -- hit_count stays 0 and grounded stays True.
    rd = check_grounding(
        'The hidden-pattern connection implies second-order effects via an '
        'invisible broker.',
        basket, whitelist, location='test')
    dialect_hits = [h['span'] for h in rd['hits'] if h['kind'] == 'dialect']
    # >=2, not >=3: "invisible broker" is a lowercase unhyphenated bigram, so no
    # current extractor pass emits it as a candidate (see DIALECT_EXACT note).
    dok = (len(rd['hits']) >= 2
           and all(h['kind'] == 'dialect' for h in rd['hits'])
           and rd['hit_count'] == 0
           and rd['grounded'] is True)
    print(f'[{"PASS" if dok else "FAIL"}] dialect allowlist -> dialect={dialect_hits} '
          f'all_hits={[(h["span"], h["kind"]) for h in rd["hits"]]} '
          f'hit_count={rd["hit_count"]} grounded={rd["grounded"]}')
    if not dok:
        failures.append('dialect')

    # ---- GT-2 (S67): conditional alias expansion + compound head-noun fix ----

    # (a) Superstring: a Fed-bearing basket grounds the "US Federal Reserve" alias.
    fed_basket = [{
        'title': 'Federal Reserve holds rates steady',
        'summary': 'The Federal Reserve left policy unchanged at its meeting.',
        'entities': ['Federal Reserve'],
    }]
    ra = check_grounding('The US Federal Reserve signalled a pause.',
                         fed_basket, [], location='test')
    aok = ra['hit_count'] == 0
    print(f'[{"PASS" if aok else "FAIL"}] alias superstring (Fed basket) -> '
          f'hits={[(h["span"], h["kind"]) for h in ra["hits"]]} '
          f'hit_count={ra["hit_count"]}')
    if not aok:
        failures.append('alias-superstring')

    # (b) Negative control: Fed-free basket -> the alias group must NOT expand,
    #     so a Federal Reserve span still fires as an entity hit.
    rb = check_grounding('The Federal Reserve will hike rates.',
                         basket, whitelist, location='test')
    bok = any(h['kind'] == 'entity' and 'federal reserve' in h['span'].lower()
              for h in rb['hits'])
    print(f'[{"PASS" if bok else "FAIL"}] alias negative control (Fed-free basket) -> '
          f'hits={[(h["span"], h["kind"]) for h in rb["hits"]]} '
          f'hit_count={rb["hit_count"]}')
    if not bok:
        failures.append('alias-negative-control')

    # (c) Head-noun fix: the trailing function word is stripped, so the span
    #     normalizes to 'silo gap' (GT-1 dialect) and not 'silo gap between'.
    rc = check_grounding('The silo-gap between the agencies persists.',
                         basket, whitelist, location='test')
    cok = (any(_norm(h['span']) == 'silo gap' and h['kind'] == 'dialect'
               for h in rc['hits'])
           and rc['hit_count'] == 0)
    print(f'[{"PASS" if cok else "FAIL"}] compound head-noun fix -> '
          f'hits={[(h["span"], h["kind"]) for h in rc["hits"]]} '
          f'hit_count={rc["hit_count"]}')
    if not cok:
        failures.append('head-noun-fix')

    print('\n' + ('ALL SPECIMEN TESTS PASSED' if not failures
                  else 'FAILURES: ' + ', '.join(failures)))
