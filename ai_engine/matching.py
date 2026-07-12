"""Keyword matching for the GNI funnel and sensors (S66 KEY-MAP).

The funnel and the sensor Layer 4 historically matched keywords with a raw
substring test (`if kw in text`). That fires on any embedded run of characters:
'eu' inside 'europe', 'war' inside 'warsaw', 'oil' inside 'turmoil', 'who'
inside 'whole'. Every one of those is a false positive, and because
stage1_match_count feeds the S38 density bonus, they inflate the score of
articles that matched nothing real.

This module replaces the substring test with word-boundary matching, while
preserving the DELIBERATE stems already in the keyword lists ('extremis',
'geopolit', 'sanction', 'strait'). Blind boundary-wrapping would break those --
'extremis' would stop matching 'extremism'. So stems are opt-in and explicit:

    'extremis*'   stem  -- matches extremism, extremist, extremists
    'extremis'    exact -- matches the bare word 'extremis' and nothing else

Callers pass keywords in any case; matching is case-insensitive throughout.
"""

import re
from functools import lru_cache

# Boundaries are lookarounds, not \b. They agree with \b whenever the keyword
# starts and ends with a word character (every keyword in the funnel list does
# today), but they stay correct for keywords that do not -- e.g. a trailing '.'
# in 'u.s.', where a trailing \b would demand a word character AFTER the dot and
# silently never match. Lookarounds assert "not glued to more word characters",
# which is what we actually mean, for any keyword shape.
_LEFT = r'(?<!\w)'
_RIGHT = r'(?!\w)'


@lru_cache(maxsize=2048)
def _pattern(keyword: str) -> "re.Pattern | None":
    """Compile a keyword once per process. Hot path: the funnel calls kw_match
    ~14 sites x |keywords| x |articles| per run, so compilation must not repeat.
    """
    kw = keyword.strip().lower()
    if not kw:
        return None

    is_stem = kw.endswith('*')
    if is_stem:
        kw = kw[:-1].strip()
        if not kw:
            return None

    body = re.escape(kw)
    # Phrases are stored with single spaces but arrive in text with arbitrary
    # whitespace (newlines from RSS summaries, double spaces). Match any run.
    body = re.sub(r'(\\?\s)+', r'\\s+', body)

    if is_stem:
        # Stem: allow the word to continue ('sanction*' -> 'sanctions-hit').
        # No right boundary -- \w* consumes the rest of the word itself.
        pattern = _LEFT + body + r'\w*'
    else:
        pattern = _LEFT + body + _RIGHT

    return re.compile(pattern, re.IGNORECASE)


def kw_match(keyword: str, text: str) -> bool:
    """True if `keyword` occurs in `text` as a whole word or phrase.

    A keyword ending in '*' is a stem and may be followed by more word
    characters. Otherwise the match is exact on word boundaries. Both are
    case-insensitive. An empty keyword never matches.
    """
    if not keyword or not text:
        return False
    pat = _pattern(keyword)
    if pat is None:
        return False
    return pat.search(text) is not None


def any_match(keywords, text: str) -> bool:
    """True if any keyword matches. Convenience for the irrelevant-topic gate."""
    return any(kw_match(kw, text) for kw in keywords)


def matched_keywords(keywords, text: str) -> list:
    """Every keyword that matches, in list order. Convenience for the Stage 1
    relevance gate, whose match COUNT feeds the S38 density bonus."""
    return [kw for kw in keywords if kw_match(kw, text)]


if __name__ == "__main__":
    passed = 0

    def check(got, want, label):
        global passed
        assert got == want, f"FAIL {label}: got {got!r}, want {want!r}"
        passed += 1

    # --- The convicted substring bugs -------------------------------------
    check(kw_match('eu', 'europe'), False, "eu not in europe")
    check(kw_match('eu', 'the EU said'), True, "eu as a word")
    check(kw_match('war', 'warsaw'), False, "war not in warsaw")
    check(kw_match('war', 'the war in Ukraine'), True, "war as a word")
    check(kw_match('oil', 'turmoil'), False, "oil not in turmoil")
    check(kw_match('oil', 'oil prices fell'), True, "oil as a word")
    check(kw_match('who', 'the whole story'), False, "who not in whole")
    check(kw_match('who', 'WHO issued guidance'), True, "who as a word")
    check(kw_match('gas', 'Madagascar'), False, "gas not in Madagascar")
    check(kw_match('import', 'important'), False, "import not in important")
    check(kw_match('strike', 'strikes'), False, "exact kw does not stem")

    # --- Explicit stems ('*' suffix) --------------------------------------
    check(kw_match('extremis*', 'extremism'), True, "stem extremism")
    check(kw_match('extremis*', 'extremist'), True, "stem extremist")
    check(kw_match('extremis*', 'far-right extremists'), True, "stem extremists")
    check(kw_match('geopolit*', 'geopolitical'), True, "stem geopolitical")
    check(kw_match('geopolit*', 'geopolitics'), True, "stem geopolitics")
    check(kw_match('sanction*', 'sanctions-hit'), True, "stem sanctions-hit")
    check(kw_match('sanction*', 'new sanctions'), True, "stem sanctions")
    check(kw_match('strait*', 'the Straits of Hormuz'), True, "stem straits")
    check(kw_match('strait*', 'straightforward'), False, "stem is not substring")
    check(kw_match('extremis*', 'the extremis'), True, "stem matches bare root")

    # --- Real keyword SHAPES found in GEOPOLITICAL_KEYWORDS ---------------
    # multi-word phrase
    check(kw_match('south china sea', 'South China Sea tensions'), True, "phrase")
    check(kw_match('south china sea', 'the South  China\nSea'), True, "phrase, ragged whitespace")
    check(kw_match('red sea', 'Red Sea shipping'), True, "phrase 2-word")
    check(kw_match('belt and road', 'the Belt and Road Initiative'), True, "phrase with stopword")
    check(kw_match('interest rate', 'interest rates rose'), False, "phrase is exact, not stem")
    # hyphenated
    check(kw_match('pro-democracy protest', 'a pro-democracy protest in Yangon'), True, "hyphenated phrase")
    check(kw_match('anti-corruption foundation', "the Anti-Corruption Foundation"), True, "hyphenated phrase 2")
    # apostrophe
    check(kw_match("people's defence force", "People's Defence Force clashed"), True, "apostrophe phrase")
    # digit-leading / alphanumeric
    check(kw_match('709 crackdown', 'the 709 crackdown on lawyers'), True, "digit-leading phrase")
    check(kw_match('a4 revolution', 'the A4 Revolution spread'), True, "alphanumeric phrase")
    check(kw_match('2020 protests', 'the 2020 protests in Belarus'), True, "digit-leading phrase 2")
    check(kw_match('2020 protests', 'the 12020 protests'), False, "digit boundary holds")
    # single-token proper nouns / acronyms
    check(kw_match('irgc', 'IRGC commanders'), True, "acronym")
    check(kw_match('nato', 'NATO allies'), True, "acronym 2")
    check(kw_match('junta', "the junta's spokesman"), True, "word before apostrophe-s")
    check(kw_match('tibet', 'Tibetan plateau'), False, "tibet not in Tibetan")
    check(kw_match('tibet*', 'Tibetan plateau'), True, "stem tibetan")

    # --- Degenerate input --------------------------------------------------
    check(kw_match('', 'anything'), False, "empty keyword")
    check(kw_match('war', ''), False, "empty text")
    check(kw_match('*', 'anything'), False, "bare star is not a keyword")

    print(f"PASS {passed}/{passed} -- all kw_match assertions green")
