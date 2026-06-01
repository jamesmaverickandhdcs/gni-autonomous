# ============================================================
# GNI Multi-Entity Extractor -- B3 Phase 1 foundation
#
# Two outputs per article:
#   entities : the FULL SET of entities in title+summary
#              -> co-occurrence material for the B3 graph
#   salient  : the subset central to the article's "aboutness"
#              -> entities GNI's OWN title/summary judged worth mentioning
#
# WHY salience by summary-worthiness (not "first in a list", not raw
# frequency): graded-entity-salience research (GUM-SAGE 2025, Google NLP)
# finds summary-worthiness aligns with human "aboutness" far better than
# frequency/position proxies. GNI already generates an LLM summary -- that
# summary IS the salience oracle, free. An entity in the title/summary is
# what GNI itself decided the article is about. This REPLACES the broken
# "first match in a hardcoded priority list" logic of _extract_location
# (which picks by list position, not article focus).
#
# ADDITIVE: does NOT modify _extract_location (correct for map pins, stays).
# STANDALONE: nothing calls this yet. Run it to prove it works.
# ============================================================
import re

# alias -> canonical. Extends supabase_saver._extract_location's 26 locations
# with blocs/orgs (the relational signal it ignored).
_GAZETTEER = {
    "Israel": ["israel", "israeli"],
    "Iran": ["iran", "iranian", "tehran"],
    "Ukraine": ["ukraine", "ukrainian", "kyiv", "kiev"],
    "Russia": ["russia", "russian", "moscow", "kremlin"],
    "China": ["china", "chinese", "beijing"],
    "Taiwan": ["taiwan", "taiwanese", "taipei"],
    "Gaza": ["gaza"],
    "Lebanon": ["lebanon", "lebanese", "beirut"],
    "Syria": ["syria", "syrian", "damascus"],
    "Iraq": ["iraq", "iraqi", "baghdad"],
    "Saudi Arabia": ["saudi arabia", "saudi", "riyadh"],
    "Yemen": ["yemen", "yemeni", "houthi", "houthis"],
    "North Korea": ["north korea", "north korean", "pyongyang", "dprk"],
    "South Korea": ["south korea", "south korean", "seoul"],
    "Japan": ["japan", "japanese", "tokyo"],
    "India": ["india", "indian", "new delhi"],
    "Pakistan": ["pakistan", "pakistani", "islamabad"],
    "United States": ["united states", "u.s.", "washington", "white house", "pentagon"],
    "Europe": ["europe", "european", "brussels"],
    "Middle East": ["middle east"],
    "Sudan": ["sudan", "sudanese", "khartoum"],
    "Ethiopia": ["ethiopia", "ethiopian", "addis ababa"],
    "Somalia": ["somalia", "somali", "mogadishu"],
    "Myanmar": ["myanmar", "burma", "burmese", "naypyidaw"],
    "Afghanistan": ["afghanistan", "afghan", "kabul", "taliban"],
    "NATO": ["nato"],
    "United Nations": ["united nations", "u.n.", "unsc"],
    "Hezbollah": ["hezbollah", "hizbollah"],
    "Hamas": ["hamas"],
}

# Build alias->canonical map and a single pre-compiled word-boundary regex
# (compiled ONCE at import, not per-call -- runs on ~525 articles/run).
_ALIAS_TO_CANON = {}
for _canon, _aliases in _GAZETTEER.items():
    for _a in _aliases:
        _ALIAS_TO_CANON[_a] = _canon
_ALIASES_SORTED = sorted(_ALIAS_TO_CANON.keys(), key=len, reverse=True)
_PATTERN = re.compile(
    r"\b(" + "|".join(re.escape(a) for a in _ALIASES_SORTED) + r")\b",
    re.IGNORECASE,
)

_SUMMARY_SCAN_CHARS = 300


def _entities_in(text: str) -> set:
    """Canonical entities found in a text span (word-boundary, alias-resolved)."""
    found = set()
    if not text:
        return found
    for m in _PATTERN.findall(text):
        canon = _ALIAS_TO_CANON.get(m.lower())
        if canon:
            found.add(canon)
    return found


def extract_entities(article: dict) -> dict:
    """
    Returns:
      {
        "entities": set   -- ALL entities in title+summary (graph co-occurrence)
        "salient":  set   -- entities GNI's title/summary judged 'about' (aboutness)
        "primary":  str|None -- single most-salient (title beats summary), or None
      }

    Salience = summary-worthiness (field-validated > frequency/position).
    Primary = title entity first (the focus), else any salient, else None --
    NOT 'first in a hardcoded list' (the _extract_location flaw).
    """
    title = article.get("title", "") or ""
    summary = (article.get("summary", "") or "")[:_SUMMARY_SCAN_CHARS]

    title_ents = _entities_in(title)
    summary_ents = _entities_in(summary)

    entities = title_ents | summary_ents          # full set -> graph edges
    salient = title_ents | summary_ents            # both title & summary = aboutness
    # primary: earliest-mentioned entity in the highest-priority text that
    # has one (title focus first, else summary focus). NEVER alphabetical /
    # list-position -- that is the _extract_location flaw we are replacing.
    def _earliest(ents, text):
        low = text.lower()
        return min(ents, key=lambda e: min(
            (low.find(a) for a in _GAZETTEER[e] if a in low), default=10**9))

    primary = None
    if title_ents:
        primary = _earliest(title_ents, title)
    elif summary_ents:
        primary = _earliest(summary_ents, summary)

    return {"entities": entities, "salient": salient, "primary": primary}


if __name__ == "__main__":
    # SELF-PROVING BLOCK. Each case asserts expected set + primary.
    # Includes fairness (non-Western) and the exact flaw this fixes
    # ("first-in-list" would mispick primary; salience picks by focus).
    cases = [
        # title, summary, expect_entities, expect_primary, proves
        ("Israel seizes Beaufort Castle in Lebanon", "",
         {"Israel", "Lebanon"}, "Israel",
         "multi-entity + primary by title-focus (Israel first)"),
        ("Ukraine strikes deep inside Russia", "",
         {"Ukraine", "Russia"}, "Ukraine",
         "FLAW FIX: primary=Ukraine (the actor/first-in-title), NOT list-order"),
        ("Russia retaliates against Ukraine after strike", "",
         {"Russia", "Ukraine"}, "Russia",
         "FLAW FIX: flip the focus -> primary flips to Russia (list can't do this)"),
        ("Tehran restores gas production at South Pars", "",
         {"Iran"}, "Iran",
         "alias resolution Tehran->Iran"),
        ("Croatian inflation expected to ease, ECB says", "",
         set(), None,
         "no-entity -> empty set, primary None (no false hit)"),
        ("Myanmar junta clashes intensify near Naypyidaw", "",
         {"Myanmar"}, "Myanmar",
         "FAIRNESS: non-Western entity + alias caught"),
        ("Iranian and Saudi officials meet in Beijing", "",
         {"Iran", "Saudi Arabia", "China"}, "Iran",
         "three-entity hub (graph gold), primary by title focus"),
        ("Markets steady", "Tensions in Lebanon ease as Hezbollah withdraws",
         {"Lebanon", "Hezbollah"}, "Lebanon",
         "entities from SUMMARY when title has none (aboutness from summary)"),
        # REAL headlines (Dawn + Breaking Defense live feeds), APOSTROPHES KEPT.
        # S40 logged a "possessive bug" -- it was a TEST ARTIFACT: that session
        # hand-stripped the apostrophe (Lebanon's->Lebanons) for heredoc safety,
        # turning a working possessive into a failing glued-plural. Verified S41:
        # ASCII ', typographic U+2019, and HTML &apos;/&#039; ALL extract correctly;
        # sanitize swaps words only; no ascii-coercion in the live collect->funnel
        # path. The possessive was never broken. These cases lock that in.
        ("Israel captures Lebanon\u2019s medieval Beaufort Castle in deepest incursion", "",
         {"Israel", "Lebanon"}, "Israel",
         "REAL possessive (typographic apostrophe): both entities extract"),
        ("Japan\u2019s defense minister rebuffs militarism allegation", "",
         {"Japan"}, "Japan",
         "REAL possessive (typographic apostrophe): single entity, no false-hit"),
    ]

    print("=== entity_extractor self-test ===")
    passed = 0
    for title, summary, exp_ents, exp_prim, proves in cases:
        r = extract_entities({"title": title, "summary": summary})
        ok = (r["entities"] == exp_ents) and (r["primary"] == exp_prim)
        passed += ok
        print(f"  [{'PASS' if ok else 'FAIL'}] {proves}")
        if not ok:
            print(f"         title:    {title}")
            print(f"         expected: ents={sorted(exp_ents)} primary={exp_prim}")
            print(f"         got:      ents={sorted(r['entities'])} primary={r['primary']}")
    print(f"=== {passed}/{len(cases)} passed ===")
