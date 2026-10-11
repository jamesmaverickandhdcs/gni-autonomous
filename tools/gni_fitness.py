#!/usr/bin/env python3
"""tools/gni_fitness.py - S107, roadmap 3 row R3-3 (DECISION S107-5).

The FITNESS FUNCTIONS a claim can be bound to. Vocabulary from Ford, Parsons
and Kua, *Building Evolutionary Architectures*: a fitness function is any
mechanism performing an objective integrity assessment of some characteristic.
Status vocabulary from OMG SACM's AssertionDeclaration (needsSupport, defeated).

Each entry MEASURES the tree and PARSES the claim. A binding row names only the
claim, the fitness id and a verbatim fragment of the claim's own text; the
fitness function reads the claimed value out of that fragment with its own
parser. So neither the claimed value nor the status is ever typed by a human
(spec section 2: "no status may be typed by a human").

  SUPPORTED  - the measurement bears out the value the fragment states
               (equality for a count; a schedule holds when every named time
               is scheduled - see _scheduled)
  DEFEATED   - it does not (SACM `defeated`: invalidated by counter-evidence)
  UNMEASURED - declared in the binding file; no fitness function yet
               (SACM `needsSupport`)

LIMIT, written down: every function here measures the REPOSITORY. A claim
about what happens at runtime (cadence achieved, accuracy, cost, uptime) needs
the database or the run log, which CI cannot reach without secrets; those
claims stay UNMEASURED with reason RUNTIME until a fitness function can read a
committed snapshot of that data.

stdlib only (item 6.9). Measurements are lazy: only a bound function runs.
"""
import ast
import glob
import os
import re


class FitnessError(Exception):
    """The measurement could not be taken - an instrument error, never a status."""


INT_RE = re.compile(r"\d+")
HHMM_RE = re.compile(r"\b(\d{1,2}):(\d{2})\b")
CRON_RE = re.compile(r"cron:\s*['\"](\d+)\s+(\d+)\s")


def _first_int(fragment):
    m = INT_RE.search(fragment)
    if not m:
        raise FitnessError("no number in fragment %r" % fragment)
    return int(m.group(0))


def _ast_list_len(root, rel, name):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            if isinstance(node.value, (ast.List, ast.Tuple)):
                return len(node.value.elts)
    raise FitnessError("no top-level list %s in %s" % (name, rel))


def _count(root, pattern):
    return len(glob.glob(os.path.join(root, pattern), recursive=True))


# Myanmar Standard Time is UTC+06:30. Named here because a page states the
# schedule in it, and the parser must convert rather than guess.
TZ_OFFSET_MIN = (("UTC", 0), ("Myanmar", 390))


def _times_utc(fragment):
    offset = None
    for name, off in TZ_OFFSET_MIN:
        if name in fragment:
            offset = off
            break
    if offset is None:
        raise FitnessError("no known timezone in fragment %r" % fragment)
    out = set()
    for h, m in HHMM_RE.findall(fragment):
        t = (int(h) * 60 + int(m) - offset) % 1440
        out.add("%02d:%02d" % (t // 60, t % 60))
    if not out:
        raise FitnessError("no HH:MM in fragment %r" % fragment)
    return sorted(out)


def _cron(root, workflow):
    path = os.path.join(root, ".github", "workflows", workflow)
    if not os.path.isfile(path):
        raise FitnessError(".github/workflows/%s not found" % workflow)
    with open(path, "rb") as fh:
        crons = CRON_RE.findall(fh.read().decode("utf-8"))
    if not crons:
        raise FitnessError("no fixed-time cron line in %s" % workflow)
    return sorted("%02d:%02d" % (int(h), int(m)) for m, h in crons)


def _int_k(fragment):
    """'100K' -> 100000. A figure written in thousands is compared in units."""
    m = re.search(r"(\d+)\s*K\b", fragment)
    if not m:
        raise FitnessError("no <n>K figure in fragment %r" % fragment)
    return int(m.group(1)) * 1000


def _ast_int_const(root, rel, name):
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == name for t in node.targets):
            if isinstance(node.value, ast.Constant) and isinstance(node.value.value, int):
                return node.value.value
    raise FitnessError("no top-level integer %s in %s" % (name, rel))


LEVELS = ("CRITICAL", "HIGH", "ELEVATED", "MODERATE", "LOW")
GAP_RE = re.compile(r"\b(%s)\s+(\d+(?:\.\d+)?)\s*(min|h)\b" % "|".join(LEVELS))


def _hours(value):
    return ("%g" % value) + "h"


def _gap_claim(fragment):
    """'CRITICAL 30 min, HIGH 2 h' -> ['CRITICAL=0.5h', 'HIGH=2h']."""
    out = [lv + "=" + _hours(float(n) / 60 if unit == "min" else float(n))
           for lv, n, unit in GAP_RE.findall(fragment)]
    if not out:
        raise FitnessError("no LEVEL <n> min|h pair in fragment %r" % fragment)
    return out


def _adaptive_gaps(root):
    """The minimum gap the adaptive run enforces per level: interval_h in
    ESCALATION_MODES, adaptive_pipeline.py (AST). This table, not the frequency
    controller's, is what run_adaptive_pipeline compares hours_since against."""
    rel = "ai_engine/adaptive_pipeline.py"
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    for node in tree.body:
        if isinstance(node, ast.Assign) and any(getattr(t, "id", "") == "ESCALATION_MODES"
                                                for t in node.targets):
            out = []
            for k, v in zip(node.value.keys, node.value.values):
                gap = [vv.value for kk, vv in zip(v.keys, v.values)
                       if getattr(kk, "value", None) == "interval_h"]
                if not gap:
                    raise FitnessError("ESCALATION_MODES[%r] has no interval_h" % k.value)
                out.append(k.value + "=" + _hours(float(gap[0])))
            return out
    raise FitnessError("no top-level ESCALATION_MODES in %s" % rel)


def _groq_refs(root):
    """Groq references in the heartbeat module (AST): imports of the groq
    package and calls to a name Groq. LIMIT, written down: imports are not
    followed - section 5 shows monitoring_pipeline imports no internal module,
    so at S111 there is nothing to follow; a new internal import moves that."""
    rel = "ai_engine/monitoring_pipeline.py"
    path = os.path.join(root, rel)
    if not os.path.isfile(path):
        raise FitnessError("%s not found" % rel)
    with open(path, "rb") as fh:
        tree = ast.parse(fh.read().decode("utf-8-sig"))
    n = 0
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            n += sum(a.name.split(".")[0] == "groq" for a in node.names)
        elif isinstance(node, ast.ImportFrom) and (node.module or "").split(".")[0] == "groq":
            n += 1
        elif isinstance(node, ast.Call) and getattr(node.func, "id", "") == "Groq":
            n += 1
    return n


def _equal(claimed, measured):
    return claimed == measured


def _scheduled(claimed, measured):
    """A schedule claim names times at which runs happen. It holds when every
    named time is a scheduled time; a workflow may schedule more runs than a
    page names (gni_mad.yml adds an 11:13 watch beside its two debates)."""
    return set(claimed) <= set(measured)


# id: (what it measures, parser of the claim's fragment, measurement, comparison)
FITNESS = {
    "F-INJ": ("injection patterns in the funnel's INJECTION_PATTERNS list (AST)",
              _first_int,
              lambda r: _ast_list_len(r, "ai_engine/funnel/intelligence_funnel.py",
                                      "INJECTION_PATTERNS"), _equal),
    "F-RSS": ("RSS sources in the collector's SOURCES list (AST)",
              _first_int,
              lambda r: _ast_list_len(r, "ai_engine/collectors/rss_collector.py", "SOURCES"),
              _equal),
    "F-WF": ("workflow files under .github/workflows",
             _first_int, lambda r: _count(r, ".github/workflows/*.yml"), _equal),
    "F-PAGES": ("page.tsx files under src/app",
                _first_int, lambda r: _count(r, "src/app/**/page.tsx"), _equal),
    "F-ROUTES": ("route.ts files under src/app/api",
                 _first_int, lambda r: _count(r, "src/app/api/**/route.ts"), _equal),
    "F-CRON-PIPE": ("main pipeline schedule, UTC, from gni_pipeline.yml cron lines",
                    _times_utc, lambda r: _cron(r, "gni_pipeline.yml"), _scheduled),
    "F-CRON-MAD": ("MAD schedule, UTC, from gni_mad.yml cron lines",
                   _times_utc, lambda r: _cron(r, "gni_mad.yml"), _scheduled),
    # S110 (item 9.11): the per-account daily token limit GNI PLANS against. Not the provider's
    # limit - GNI has never measured that - which is why the page labels it as GNI's.
    "F-TPD": ("per-account daily Groq token limit GNI plans against: TPD_HARD_LIMIT in quota_guard.py (AST)",
              _int_k, lambda r: _ast_int_const(r, "ai_engine/quota_guard.py", "TPD_HARD_LIMIT"), _equal),
    "F-TPD-SAFE": ("per-account daily safe ceiling GNI plans against: TPD_SAFE_CEILING in quota_guard.py (AST)",
                   _int_k, lambda r: _ast_int_const(r, "ai_engine/quota_guard.py", "TPD_SAFE_CEILING"), _equal),
    # S111 (roadmap 4 row R4-2, /about/devops).
    "F-ADAPT-GAP": ("minimum gap per escalation level the adaptive run enforces: interval_h in "
                    "ESCALATION_MODES, adaptive_pipeline.py (AST)",
                    _gap_claim, _adaptive_gaps, _scheduled),
    "F-HB-GROQ": ("Groq imports and Groq() calls in the heartbeat module, monitoring_pipeline.py (AST)",
                  _first_int, _groq_refs, _equal),
}

# Why a claim has no fitness function. Written down at S111 for the three that
# were accepted and defined nowhere (roadmap 4's OWED list); a reason without a
# definition is a status typed by hand.
# UNREVIEWED: nobody has yet looked for a fitness function for the claim - it
# says nothing about the claim, and it is the reason most claims carry at S107.
# RUNTIME: see the module docstring - the claim is about what happens when GNI
# runs, and waits for a fitness function that reads a committed snapshot.
# PROMISE: the claim states an intention, not a state (its kind is PROMISE).
# HISTORICAL: the claim states a past state of the system (the frozen March 2026
# White Paper's "current" figures); measuring today's tree against it would
# defeat a claim that was true when made.
# PROVENANCE: the claim states who made GNI, where, or in which programme - an
# authorship or credit line. It describes GNI's origin, not its behaviour.
# EXTERNAL: the claim states a fact about a party GNI does not control - a
# provider's free-tier terms, limits or billing, or an outside statistic. Only
# that party's published terms can bear it out (ARCHITECTURE section 4, SLM).
# QUALITATIVE: the claim describes GNI's design or behaviour with no count, rate,
# time or date in it, so no fitness function can bear it out or defeat it. The
# review that gives this reason has READ THE CODE the sentence describes and
# judged it true; the reviewing commit names the files read. A sentence judged
# false gets no reason: its copy is retired. WEAKNESS: this is a person's
# judgement and leaves no trace beyond that commit message.
# HISTORICAL and PROVENANCE excuse a number on the public pages (gni_claims
# REVIEW_EXEMPT, roadmap 4 row R4-3); the other reasons do not.
UNMEASURED_REASONS = ("UNREVIEWED", "RUNTIME", "PROMISE", "HISTORICAL", "QUALITATIVE",
                      "EXTERNAL", "PROVENANCE")


def derive(root, fid, fragment, cache):
    """(status, claimed, measured). Raises FitnessError on an instrument fault."""
    if fid not in FITNESS:
        raise FitnessError("unknown fitness function %s" % fid)
    _, parse, measure, holds = FITNESS[fid]
    claimed = parse(fragment)
    if fid not in cache:
        cache[fid] = measure(root)
    measured = cache[fid]
    return ("SUPPORTED" if holds(claimed, measured) else "DEFEATED"), claimed, measured
