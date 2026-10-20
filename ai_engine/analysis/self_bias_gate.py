# ============================================================
# GNI Self-Bias Gate -- PHI-003 self-audit
# "An anti-pretense instrument that is never itself audited
#  becomes the purest form of pretense." -- S39 fourth analyst
#
# GNI audits its sources (NN-PHI-5/6), its inputs (injection),
# its absences (NN-PHI-5). Nothing audited GNI's OWN OUTPUT for
# internal contradiction -- until the escalation latch broadcast
# manufactured fear for days while sentiment said calm.
#
# This gate reads GNI's recent reports and flags where the system
# contradicts itself or violates an NN-PHI. Findings are written to
# the tamper-evident audit_trail chain (SELF_BIAS_FLAG) so the audit
# of GNI cannot itself be quietly rewritten.
# ============================================================
import ast
import os
import re
import sys
from datetime import datetime, timezone, timedelta
from functools import lru_cache

# S115: the Freedom-from-Fear measures below are stdlib only, and tools/gni_fitness.py imports
# this module in CI's rule_checks job, which installs nothing. The daily gate still loads .env.
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def _get_client():
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_SERVICE_KEY", "")
        if not url or not key:
            return None
        return create_client(url, key)
    except Exception:
        return None


def _fetch_recent_reports(hours: int = 24) -> list[dict]:
    """Pull reports written in the last `hours` for coherence auditing."""
    client = _get_client()
    if not client:
        return []
    cutoff = (datetime.now(timezone.utc) - timedelta(hours=hours)).isoformat()
    try:
        result = client.table("reports") \
            .select("id, title, created_at, escalation_score, escalation_level, "
                    "sentiment, sentiment_score, risk_level, combo_bonus, "
                    "summary, fff_what_is_happening, fff_honest_analysis, fff_human_path") \
            .gte("created_at", cutoff) \
            .order("created_at", desc=True) \
            .execute()
        return result.data or []
    except Exception as e:
        # combo_bonus may not be a stored column -- retry without it
        try:
            result = client.table("reports") \
                .select("id, title, created_at, escalation_score, escalation_level, "
                        "sentiment, sentiment_score, risk_level, summary, "
                        "fff_what_is_happening, fff_honest_analysis, fff_human_path") \
                .gte("created_at", cutoff) \
                .order("created_at", desc=True) \
                .execute()
            return result.data or []
        except Exception as e2:
            print(f"  Warning: Could not fetch reports: {str(e2)[:80]}")
            return []


# ---- Check 1: escalation must agree with honest sentiment/risk (NN-PHI-1) ----
def _check_escalation_sentiment(r: dict) -> dict | None:
    """
    Flag a report where escalation screams CRITICAL/HIGH while GNI's own
    LLM read says calm (Bullish/Neutral + Low/Medium). This is the bug the
    PHI-003 escalation gate fixed -- this check is its permanent regression
    guard. A flag here means either the gate regressed or was bypassed.
    """
    level = (r.get("escalation_level") or "").upper()
    sentiment = (r.get("sentiment") or "").strip().lower()
    risk = (r.get("risk_level") or "").strip().lower()

    if level not in ("CRITICAL", "HIGH"):
        return None
    calm_sentiment = sentiment in ("bullish", "neutral")
    calm_risk = risk in ("low", "medium")
    if not (calm_sentiment and calm_risk):
        return None

    # Ostrich guard: a genuine critical combo legitimately overrides a calm
    # read. If combo_bonus is stored and >= 3, this is NOT a contradiction.
    combo = r.get("combo_bonus")
    if combo is not None and combo >= 3:
        return None

    return {
        "check": "escalation_sentiment",
        "nn_phi": "NN-PHI-1",
        "report_id": r.get("id"),
        "title": (r.get("title") or "")[:80],
        "detail": (f"escalation={level} but sentiment={r.get('sentiment')} "
                   f"risk={r.get('risk_level')} -- manufactured fear (no critical combo)"),
        "escalation_score": r.get("escalation_score"),
    }


# ---- Check 2: every threat must have a path (NN-PHI-4) ----
def _check_threat_has_path(r: dict) -> dict | None:
    """
    Flag a High/Critical-risk report whose fff_human_path is empty or
    dismissive. NN-PHI-4: 'Every threat must have a path.' A threat with
    no path violates the core mission -- fear without agency.
    """
    risk = (r.get("risk_level") or "").strip().lower()
    if risk not in ("high", "critical"):
        return None

    path = (r.get("fff_human_path") or "").strip()
    if len(path) >= 40:  # a real path is a sentence or more
        return None

    return {
        "check": "threat_has_path",
        "nn_phi": "NN-PHI-4",
        "report_id": r.get("id"),
        "title": (r.get("title") or "")[:80],
        "detail": (f"risk={r.get('risk_level')} but fff_human_path is "
                   f"{'empty' if not path else 'too thin (' + str(len(path)) + ' chars)'} "
                   f"-- threat without a path"),
        "escalation_score": r.get("escalation_score"),
    }


# ---- Check 3: required output fields must not be silently empty (NN-PHI-1) ----
# Conservative whitelist -- only fields that are ALWAYS required on a real
# report. A blank here means GNI published incomplete intelligence as if
# complete -- a small pretense (PHI-001) and a Freedom-from-Fear failure if
# the missing field is the human path (PHI-003). Sibling-class of the
# published_at/url silent-empty bugs found by the S40 silent-fail sweep.
_REQUIRED_NONEMPTY = ("title", "sentiment", "risk_level")

def _check_required_field_empty(r: dict) -> dict | None:
    missing = [f for f in _REQUIRED_NONEMPTY if not (r.get(f) or "").strip()]
    if not missing:
        return None
    return {
        "check": "required_field_empty",
        "nn_phi": "NN-PHI-1",
        "report_id": r.get("id"),
        "title": (r.get("title") or "")[:80],
        "detail": ("required field(s) silently empty: " + ", ".join(missing) +
                   " -- incomplete intelligence presented as complete"),
        "escalation_score": r.get("escalation_score"),
    }


# ============================================================
# S115 - roadmap 5 row R5-2: the Teenager Standard read on GNI's OWN TEXT.
# Each measure below is a PROXY for a human judgement (spec section 6): it finds what it
# names and nothing else, and R5-3 checks it against people before it may grade anything
# beyond this gate. One implementation: the daily audit calls these through CHECKS, and
# tools/gni_fitness.py imports this module and runs the same functions over the committed
# output sample (docs/gni_output_sample_S<N>.json).
#
# THRESHOLDS WERE RULED BEFORE ANY MEASURE RAN OVER THE SAMPLE (DECISIONS S115-1 to S115-4,
# delegated by the operator, carried in the commit that set them):
#   S115-1 T1 readability: Flesch-Kincaid grade of fff_what_is_happening at most 10 - the
#          "smart 16-year-old" GNI wrote down at S38 (da5ead8) is a US grade 10-11 reader.
#   S115-2 T1 jargon: no term of a CLOSED list in fff_what_is_happening; the list comes from
#          sources named below, never from the sample.
#   S115-3 T3: fff_human_path carries none of the generic forms the S38 teenager prompt bans;
#          NN-PHI-4: the existing path-present check, unchanged.
#   S115-4 T4: the intensity and certainty entries of the funnel's SANITIZE_VOCAB; T5: the
#          funnel's sectarian and PHI-002 patterns; NN-PHI-3: its PHI-003 rhetoric patterns.
#   Budget: where the founding text says every / never / reject outright (NN-PHI-4, T5,
#   NN-PHI-3) no output may be flagged; where the measure is a proxy for a judgement (T1, T3,
#   T4) at most 10% of outputs may be - the p90 shape SLO-2 uses (ARCHITECTURE 10.3).
# ============================================================
FK_GRADE_MAX = 10
PROXY_BUDGET = 0.10
ABSOLUTE_BUDGET = 0.0

# S115-2. (i) The tickers the live report prompt lists for tickers_affected (PROMPT_V1 in
# prompt_manager.py), matched case-sensitively as whole words so 'coin' and 'hack' pass.
# (ii) Terms the SEC's Plain English Handbook (1998) replaces or explains: equities, capital
# appreciation, debt securities, call option, undervalued, REIT ('income' and 'distribution'
# are left out - they are ordinary words outside the handbook's context). (iii) The market-
# call labels the prompt itself asks for. Incomplete by construction: a term passes until named.
JARGON_TOKENS = ("SPY", "AAPL", "JPM", "XOM", "GLD", "USO", "LMT", "TLT", "EWT", "EWJ", "FXI",
                 "DXY", "SOXX", "HACK", "VIX", "EWG", "EWY", "HYG", "EMB", "UNG", "WEAT", "GDX",
                 "BTC-USD", "ETH-USD", "COIN", "REIT")
JARGON_TERMS = ("equities", "capital appreciation", "debt securities", "call option",
                "undervalued", "bullish", "bearish", "sentiment")

# S115-3. The S38 teenager prompt (nexus_analyzer.py, da5ead8) says of the path: not "advocate
# for diplomacy", not "stay informed", "not investing advice (they have no money yet)". Those
# three, in their own words with their inflections - a paraphrase passes (spec section 6).
GENERIC_PATH_PATTERNS = tuple(re.compile(p, re.IGNORECASE) for p in (
    r"\badvocat\w*\s+for\s+diplomac\w*",
    r"\bstay\w*\s+informed\b",
    r"\binvest(?:s|ed|ing|or|ors|ment|ments)?\b",
))

# S115-4. SANITIZE_VOCAB holds two kinds of entry: intensity or certainty ('catastrophic',
# 'imminent threat', 'guaranteed to') and political labels ('regime', 'invasion'). Fear without
# understanding (T4) is the first kind; a label can be the accurate word, so the second is left out.
FEAR_EXCLUDED_LABELS = ("puppet government", "regime", "invasion", "occupation", "terror attack",
                        "terrorist", "aggressor", "war criminal", "western aggression",
                        "nato aggression", "us imperialism", "imperialist", "puppet state",
                        "proxy war", "hegemon", "hegemony")

TEXT_FIELDS = ("title", "summary", "fff_what_is_happening", "fff_honest_analysis", "fff_human_path")

_FUNNEL = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),
                       "funnel", "intelligence_funnel.py")


@lru_cache(maxsize=None)
def _funnel_lists():
    """The funnel's pattern lists, READ from its source by AST rather than imported: importing
    the funnel pulls the database client, which neither this gate's workflow nor CI installs.
    The strings and the re flags are the funnel's own, so the two cannot drift."""
    with open(_FUNNEL, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    out = {}
    for node in tree.body:
        if not isinstance(node, ast.Assign) or not isinstance(node.targets[0], ast.Name):
            continue
        name = node.targets[0].id
        if name == "SANITIZE_VOCAB":
            out[name] = ast.literal_eval(node.value)
        elif name in ("_PHI003_RHETORIC_PATTERNS", "_PHI002_PATTERNS", "_SECTARIAN_PATTERNS"):
            comp = node.value
            call = comp.elt
            flags = 0
            for part in ast.walk(call.args[1]):
                if isinstance(part, ast.Attribute):
                    flags |= getattr(re, part.attr)
            out[name] = tuple(re.compile(p, flags) for p in ast.literal_eval(comp.generators[0].iter))
    missing = {"SANITIZE_VOCAB", "_PHI003_RHETORIC_PATTERNS", "_PHI002_PATTERNS",
               "_SECTARIAN_PATTERNS"} - set(out)
    if missing or not all(out.values()):
        raise RuntimeError("intelligence_funnel.py: missing or empty %s" % sorted(missing or out))
    return out


_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['\u2019\-\u2010\u2011][A-Za-z0-9]+)*")
_ABBREV_RE = re.compile(r"\b(?:[A-Z]\.){2,}")
_SENT_END_RE = re.compile(r"[.!?]+(?=\s|$)")


def _syllables(word):
    """Vowel groups, less a silent final e/es/ed - a heuristic; tools differ (spec section 2,
    Redish's first reason), and a token holding a digit counts as one syllable."""
    w = word.lower()
    if any(c.isdigit() for c in w):
        return 1
    w = re.sub(r"[^a-z]", "", w)
    if len(w) <= 3:
        return 1
    n = len(re.findall(r"[aeiouy]+", w))
    if w.endswith("e") and not w.endswith(("le", "ee", "ye")):
        n -= 1                                   # silent e: make, state
    elif (w.endswith("ed") and w[-3] not in "aeiouy"
          and not w.endswith(("ted", "ded"))):
        n -= 1                                   # silent -ed: fired, struck (not agreed, not started)
    elif (w.endswith("es") and w[-3] not in "aeiouy"
          and not w.endswith(("ses", "xes", "zes", "ches", "shes", "ces", "ges"))):
        n -= 1                                   # silent -es: makes, strikes (not countries, not taxes)
    return max(1, n)


def fk_grade(text):
    """Flesch-Kincaid grade level (Kincaid, Fishburne, Rogers and Chissom, 1975, Navy Research
    Branch Report 8-75): 0.39 words/sentence + 11.8 syllables/word - 15.59. The report says such
    formulas are accurate to about one grade level. None for a text with no words."""
    t = _ABBREV_RE.sub(lambda m: m.group(0).replace(".", ""), text or "")
    words = _WORD_RE.findall(t)
    if not words:
        return None
    sentences = max(1, len(_SENT_END_RE.findall(t.strip())))
    syl = sum(_syllables(w) for w in words)
    return round(0.39 * len(words) / sentences + 11.8 * syl / len(words) - 15.59, 1)


def _finding(r, check, nn, detail):
    return {"check": check, "nn_phi": nn, "report_id": r.get("id"),
            "title": (r.get("title") or "")[:80], "detail": detail,
            "escalation_score": r.get("escalation_score")}


def _reader_text(r):
    return "\n".join(r.get(f) or "" for f in TEXT_FIELDS)


# ---- Check 4: T1 - can a teenager understand what is happening (CLM-1109) ----
def _check_readability(r):
    g = fk_grade(r.get("fff_what_is_happening"))
    if g is None or g <= FK_GRADE_MAX:
        return None
    return _finding(r, "readability", "T1", "fff_what_is_happening reads at Flesch-Kincaid "
                    "grade %s, above %d (proxy, unvalidated until R5-3)" % (g, FK_GRADE_MAX))


def _jargon_found(text):
    found = [t for t in JARGON_TOKENS if re.search(r"(?<![\w-])%s(?![\w-])" % re.escape(t), text)]
    found += [t for t in JARGON_TERMS if re.search(r"\b%s\b" % re.escape(t), text, re.IGNORECASE)]
    return found


# ---- Check 5: T1 - market jargon in what is happening (CLM-1109) ----
def _check_jargon(r):
    found = _jargon_found(r.get("fff_what_is_happening") or "")
    if not found:
        return None
    return _finding(r, "jargon", "T1", "fff_what_is_happening uses " + ", ".join(found))


# ---- Check 6: T3 - a path is not one of the forms the S38 prompt bans (CLM-1111) ----
def _check_path_generic(r):
    path = r.get("fff_human_path") or ""
    hits = [m.group(0) for p in GENERIC_PATH_PATTERNS for m in [p.search(path)] if m]
    if not hits:
        return None
    return _finding(r, "path_generic", "T3", "fff_human_path uses a banned generic form: "
                    + ", ".join(hits))


# ---- Check 7: T4 - fear without understanding, by GNI's own amplifier list (CLM-1112) ----
def _check_fear_vocabulary(r):
    text = _reader_text(r)
    found = [loaded for loaded, _ in _funnel_lists()["SANITIZE_VOCAB"]
             if loaded not in FEAR_EXCLUDED_LABELS
             and re.search(re.escape(loaded), text, re.IGNORECASE)]
    if not found:
        return None
    return _finding(r, "fear_vocabulary", "T4", "amplifier terms in GNI's own text: " + ", ".join(found))


def _patterns_hit(names, text):
    lists = _funnel_lists()
    return [m.group(0)[:60] for n in names for p in lists[n] for m in [p.search(text)] if m]


# ---- Check 8: T5 - identity division in GNI's own text (CLM-1113) ----
def _check_sectarian(r):
    hits = _patterns_hit(("_SECTARIAN_PATTERNS", "_PHI002_PATTERNS"), _reader_text(r))
    if not hits:
        return None
    return _finding(r, "sectarian", "T5", "sectarian or PHI-002 pattern in GNI's own text: "
                    + "; ".join(hits))


# ---- Check 9: NN-PHI-3 - no manipulation technique in GNI's own text (CLM-1124) ----
def _check_manipulation(r):
    hits = _patterns_hit(("_PHI003_RHETORIC_PATTERNS",), _reader_text(r))
    if not hits:
        return None
    return _finding(r, "manipulation", "NN-PHI-3", "PHI-003 rhetoric pattern in GNI's own text: "
                    + "; ".join(hits))


CHECKS = [
    _check_escalation_sentiment,
    _check_threat_has_path,
    _check_required_field_empty,
    _check_readability,
    _check_jargon,
    _check_path_generic,
    _check_fear_vocabulary,
    _check_sectarian,
    _check_manipulation,
]

# The measures tools/gni_fitness.py runs over the output sample, each with the share of
# outputs it may flag before the claim it is bound to reads DEFEATED.
FFF_MEASURES = {
    "readability": (_check_readability, PROXY_BUDGET),
    "jargon": (_check_jargon, PROXY_BUDGET),
    "path_generic": (_check_path_generic, PROXY_BUDGET),
    "fear_vocabulary": (_check_fear_vocabulary, PROXY_BUDGET),
    "threat_has_path": (_check_threat_has_path, ABSOLUTE_BUDGET),
    "sectarian": (_check_sectarian, ABSOLUTE_BUDGET),
    "manipulation": (_check_manipulation, ABSOLUTE_BUDGET),
}


def _check_flatline(reports: list[dict]) -> list[dict]:
    """
    Set-level check (NN-PHI-1 + NN-PHI-3): a numeric field frozen bit-identical
    across many consecutive reports is the latch signature -- the escalation
    bug that broadcast CRITICAL 10.0 for days while the world changed. Genuine
    analysis always has some jitter; perfect constancy across N+ distinct runs
    is manufactured constancy, a pretense. Conservative: needs >= 4 reports and
    EXACT equality (mild stability does not trip it).
    """
    findings = []
    if len(reports) < 4:
        return findings
    for field in ("escalation_score", "sentiment_score"):
        vals = [r.get(field) for r in reports]
        if any(v is None for v in vals):
            continue
        if len(set(vals)) == 1:  # bit-identical across every report
            findings.append({
                "check": "flatline",
                "nn_phi": "NN-PHI-1/3",
                "report_id": reports[0].get("id"),
                "title": (reports[0].get("title") or "")[:80],
                "detail": (f"{field} frozen at {vals[0]} across {len(vals)} consecutive "
                           f"reports -- possible latch (manufactured constancy)"),
                "escalation_score": reports[0].get("escalation_score"),
            })
    return findings


def _fetch_latest_selected() -> list[dict]:
    """Pull stage4-selected articles from the most recent pipeline run."""
    client = _get_client()
    if not client:
        return []
    try:
        # newest run_id first
        latest = client.table("pipeline_articles") \
            .select("run_id, created_at") \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()
        if not latest.data:
            return []
        run_id = latest.data[0].get("run_id")
        if not run_id:
            return []
        sel = client.table("pipeline_articles") \
            .select("source, pillar, stage4_selected, run_id") \
            .eq("run_id", run_id) \
            .eq("stage4_selected", True) \
            .execute()
        return sel.data or []
    except Exception as e:
        print(f"  Warning: source-dominance fetch failed: {str(e)[:80]}")
        return []


def _check_source_dominance(min_selected: int = 10, threshold: float = 0.35) -> list[dict]:
    """
    Set-level check (NN-PHI-2 + NN-PHI-6): no single source should dominate
    GNI's own selection. PHI-002 turned inward -- if one voice supplies a
    disproportionate share of the selected set, GNI's output is being captured
    by that source's framing, the exact risk Partner B found in RT (OP-033). This
    audits GNI's selection the way GNI audits its sources. Conservative: needs
    >= min_selected articles before judging (a tiny run won't false-flag).
    """
    selected = _fetch_latest_selected()
    findings = []
    total = len(selected)
    if total < min_selected:
        return findings  # too few to judge -- not enough signal

    counts = {}
    for a in selected:
        src = (a.get("source") or "Unknown").strip()
        counts[src] = counts.get(src, 0) + 1

    for src, n in counts.items():
        share = n / total
        if share > threshold:
            findings.append({
                "check": "source_dominance",
                "nn_phi": "NN-PHI-2/6",
                "report_id": None,
                "title": f"selection capture: {src}",
                "detail": (f"{src} supplied {n}/{total} selected articles "
                           f"({share:.0%}) -- single-source dominance over "
                           f"{threshold:.0%} threshold (selection framing risk)"),
                "escalation_score": None,
            })
    return findings


def run_self_bias_audit(hours: int = 24) -> dict:
    """
    Main entry point. Reads recent reports, runs every coherence check,
    writes findings (or a clean record) to the tamper-evident audit_trail.

    Returns dict: {findings: [...], reports_audited: N, clean: bool}
    """
    print("  SELF-BIAS GATE: auditing GNI's own recent output...")
    reports = _fetch_recent_reports(hours)
    findings = []
    for r in reports:
        for check in CHECKS:
            f = check(r)
            if f:
                findings.append(f)

    # Set-level checks (compare across reports, not per-row)
    findings.extend(_check_flatline(reports))
    findings.extend(_check_source_dominance())

    # Write to the tamper-evident chain -- the audit of GNI cannot be rewritten
    try:
        from analysis.audit_trail import log_audit_event
    except Exception:
        try:
            from audit_trail import log_audit_event
        except Exception:
            log_audit_event = None

    if log_audit_event:
        if findings:
            log_audit_event("SELF_BIAS_FLAG", {
                "reports_audited": len(reports),
                "finding_count": len(findings),
                "findings": findings,
            })
        else:
            # Absence of findings is itself recorded -- proves the gate ran
            log_audit_event("SELF_BIAS_AUDIT_CLEAN", {
                "reports_audited": len(reports),
                "window_hours": hours,
            })

    if findings:
        print(f"  SELF-BIAS GATE: {len(findings)} contradiction(s) in {len(reports)} reports")
        for f in findings:
            print(f"    [{f['nn_phi']}] {f['check']}: {f['detail']}")
    else:
        print(f"  SELF-BIAS GATE: clean -- {len(reports)} reports audited, no contradictions")

    return {
        "findings": findings,
        "reports_audited": len(reports),
        "clean": len(findings) == 0,
    }


if __name__ == "__main__":
    result = run_self_bias_audit()
    print(f"\nSelf-bias audit complete: "
          f"{result['reports_audited']} audited, "
          f"{len(result['findings'])} flagged, "
          f"clean={result['clean']}")
