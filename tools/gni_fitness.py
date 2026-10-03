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
}

# Why a claim has no fitness function. HISTORICAL: the claim states a past
# state of the system (the frozen March 2026 White Paper's "current" figures);
# measuring today's tree against it would defeat a claim that was true when made.
# UNREVIEWED: nobody has yet looked for a fitness function for the claim - it
# says nothing about the claim, and it is the reason most claims carry at S107.
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
