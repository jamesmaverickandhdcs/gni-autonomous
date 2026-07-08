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

# ---- Extraction patterns ----
# 1. Proper-noun sequences: one or more consecutive Capitalized words.
_CAP_RE = re.compile(r'[A-Z][A-Za-z]+(?:\s+[A-Z][A-Za-z]+)*')
# 2. Hyphenated / compound noun phrases: a hyphen-joined token, optionally
#    followed by ONE lowercase head noun ("dollar-depegging", "rare-earth broker").
_COMPOUND_RE = re.compile(r'[A-Za-z]+(?:-[A-Za-z]+)+(?:\s+[a-z]+)?')
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
    """
    result = {'hits': [], 'hit_count': 0, 'checked_spans': 0, 'grounded': True}
    if not text or not isinstance(text, str) or text.startswith('[Agent error'):
        return result

    basket_norm, basket_raw = _basket_corpus(basket, whitelist_extra)
    sent_starts = _sentence_starts(text)

    # candidates: OrderedDict norm_span -> (raw_span, kind)  (dedup, keep first)
    candidates = OrderedDict()

    # -- pass 1: hyphenated / compound noun phrases (mask so caps/qty don't re-claim) --
    compound_spans = []
    for m in _COMPOUND_RE.finditer(text):
        raw = m.group(0).strip()
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
        if kind == 'quantity':
            grounded = _qty_grounded(raw, basket_norm, basket_raw)
        else:
            grounded = _norm(raw) in basket_norm
        if not grounded:
            result['hits'].append({'span': raw, 'kind': kind, 'location': location})

    result['hit_count'] = len(result['hits'])
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

    print('\n' + ('ALL SPECIMEN TESTS PASSED' if not failures
                  else 'FAILURES: ' + ', '.join(failures)))
