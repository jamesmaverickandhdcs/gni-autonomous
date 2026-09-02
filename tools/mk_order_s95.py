#!/usr/bin/env python3
"""Build docs/GNI_TARGET_AND_ORDER_S95.md (generation 15) from generation 14
by BYTE COPY plus anchored patches (DECISION S92-5).

The GRAVEYARD travels inside the copy: not retyped, not re-read, not re-inserted.
Every anchor must match exactly once or the script refuses before writing.
"""
import os
import sys

SRC = "docs/GNI_TARGET_AND_ORDER_S94.md"
DST = "docs/GNI_TARGET_AND_ORDER_S95.md"

HEADER_OLD = ("**GENERATION 14 - 2026-09-02 (S94 close). SUPERSEDES generation 13 "
              "(`GNI_TARGET_AND_ORDER_S93.md`).**")
HEADER_NEW = ("**GENERATION 15 - 2026-09-03 (S95 close). SUPERSEDES generation 14 "
              "(`GNI_TARGET_AND_ORDER_S94.md`).**")

MISSION_FROM = "## NEXT SESSION'S MISSION (S95)"
MISSION_TO = "## TARGET (unchanged"
MISSION_NEW = """## NEXT SESSION'S MISSION (S96)

**Build the time-series macro map: X = session, Y = White Paper layer, Z = Vision ->
Executable. Measure the gap instead of estimating it.**

WHY THIS IS TOP. It is JAMES'S roadmap (DECISION S93-2) and the last row of it. S93
built the detector, S94 the world model, S95 moved law out of prose and into code.
S96 measures whether any of that closed distance.

**S95 handed it a real axis.** `docs/GNI_RULE_CHECKABILITY_S95.tsv` is machine-readable:
159 rules, 53 CHECKABLE, 106 not, one reason each. Z is no longer an estimate for the
rule layer - it is a ratio that can be recomputed at every close and diffed.

**Definition of done:** a generated artifact - not a hand-drawn one - that plots at
least one measured series per axis, names its source for every point, and states which
points are measured and which are absent. An absent point is shown as absent, never
interpolated. Read R-S95-4 before comparing any figure across generations: compare the
SET, not the integer.

**Scope, stated narrowly because this item invites sprawl:** ONE generated artifact.
Not a dashboard, not a new document type, not a metric framework. If the first honest
version has three points on it, ship three points.

**Discriminating cert (R-S90-1):** change one input figure and the artifact must move;
revert it and the artifact must return byte-identical. An artifact that renders the same
under both has measured nothing.

"""

CLOSED_ANCHOR = "**CLOSED AT S94 - `44a3cba`, certified on the live tree:**"
CLOSED_NEW = """**CLOSED AT S95 - `b70fc08` + the S95 docs commit, certified on CI:**
- **THE S95 MISSION.** All 159 registered rules classified CHECKABLE / NOT with a one-line
  reason each - 53 yes, 106 no - and FIVE shipped as executable checks in
  `tools/gni_rule_checks.py`, running as a second CI job. Markers and
  `docs/GNI_RULE_CHECKABILITY_S95.tsv` come from ONE dict, so prose and table cannot drift.
  Cert across three commits: `b639b54` rule_checks GREEN -> `66c105e` (one manifest row
  removed) rule_checks RED, ONE check failing, harnesses unmoved -> `a5e9c1e` GREEN again.
  `harnesses` failed in all three: that is the CONTROL, not noise.
- **`rule_checks` is the first CI square in GNI that is meant to be green, and is.**
  Job-level reading was required to see it - run-level `conclusion` is `failure` in every
  case because `harnesses` is correctly red (5.14). Never read this workflow at run level.
- **THE FOUR CI EXIT INTEGERS, answered.** S94's UNKNOWN asked whether they still read
  1/1/0/0. They do: `dryrun_false_neutral` 1, `dryrun_mad_redefinition` 1, `dryrun_nn5_gate`
  0, `dryrun_rate_governor` 0, two `ZeroDivisionError`s, signature identical to `33572158050`.
- **5.20 PARTIALLY DISCHARGED.** `tools/gni_rule_checks_fixture.py` is a self-asserting
  selftest over 11 fixture families and runs in CI as the control probe BEFORE the checks.
  `tools/gni_state.py` remains outside; the item stays open for that half only.
- **`R-S92-2` DEMOTED to NOT CHECKABLE, with evidence.** Three check designs died against
  measurement. `src/app/api/health/route.ts:39` carries `.order('run_at', {ascending:
  false}).limit(1000)` - the direct descendant of `limit(332)`. Position-decay lives in HOW
  the constant was derived, not in the call site, and `limit(1000)` and `limit(332)` are
  byte-identical in shape. C3's slot went to `R-S74-1` instead.

"""

LIFECYCLE_ANCHOR = "### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away"
NEW_ITEMS = """- **5.22** **NEW (S95) [MEASURED] — `tools/*.py` ARE FRAGILE TO THE OPERATOR'S CONSOLE AND
  TO STRAY BYTES.** Two defects, one subject. (a) `gni_state.py --stdout` dies with
  `UnicodeEncodeError` on `\\u2192` because Windows `print` encodes cp1252; the file-writing
  path is unaffected, so only `--stdout` is broken, and Linux CI would never show it.
  (b) `code_consumers()` splits `git grep` output with `splitlines()`, which also breaks on a
  lone `\\r`, yielding a colon-less fragment and `IndexError`. Both are `R-S87-5` / `R-S94-3`
  kin: the environment translates without being asked. Fix shape: `sys.stdout.reconfigure(
  encoding="utf-8")` and `split("\\n")` with a colon-count guard that exits 2.
- **5.23** **NEW (S95) — C5'S BLIND SPOT IS WHERE THE ERRORS LIVE.** `tools/gni_rule_checks.py`
  lints itself for hand-written integers, but patch scripts live in `/tmp` and are never
  committed, so nothing lints them. FIVE of this session's SEVEN instrument errors happened
  there. The rule that would have caught them (`R-S81-5`) is shipped as a check that cannot
  see them.
- **5.24** **NEW (S95) [MEASURED] — 22 FILES IN `docs/` CARRY NO SESSION NUMBER.** Of 117
  markdown files, 84 are session-numbered generations of the six live families (78 superseded,
  6 live), 11 belong to one-off numbered families, and **22 have no number at all** -
  including `SUBPAGE_CERTIFICATION.md` and `SUBPAGE_IC_CENSUS.md`. A numbered file can at
  least say "something higher exists, so I am dead". An unnumbered file can never be
  superseded and can never declare itself live. This is D4's mechanism in its general form:
  D4 said no live document points at the deliverable; the bytes say there is no MECHANISM by
  which one could.
- **5.25** **NEW (S95) [MEASURED from §7.2] — TWO SECRETS WHOSE WIRING CONTRADICTS THEIR
  CONSUMERS.** `ALPHA_VANTAGE_API_KEY` is stored and bound to an env alias in
  `gni_pipeline.yml` with **zero** code consumers, while `ai_engine/collectors/alpha_vantage.py`
  reads `TWELVE_DATA_API_KEY`. `GROQ_MAD_EVENING` is referenced by `gni_mad.yml` with **no env
  alias and zero** consumers. Neither is a deletion instruction (S93 ruling); both are
  unexplained, unlike the four `none` rows §7.2 explains. Not chased at S95: out of mission scope.
- **6.11** **NEW (S95) [MEASURED] — ONE UNORDERED `limit(N>1)` IN `ai_engine/`.**
  `ai_engine/mad_runner.py:104` calls `.limit(50)` with no `.order()` in the same chain, so
  which 50 rows Postgres returns is not defined by the query. Found by an AST probe over
  `ai_engine/` (26 `limit(1)` singletons, 7 ordered `limit(N>1)`, this one). Not a run-time
  failure and not measured against `frequency_log` / `reports`; an UNKNOWN, not a defect.
- **9.18** **NEW (S95) — THE TYPESCRIPT HALF OF THE POSITION-SELECT SURFACE IS UNMEASURABLE.**
  35 `.limit()` sites live in `src/app/api/*.ts`, including the `limit(1000)` descendant of
  `limit(332)`. No TypeScript parser is available to a stdlib-only tool, so every AST-based
  measurement this session made covers `ai_engine/` only. Any claim about GNI's
  position-select surface that does not say "Python only" is overstated.

"""

CHANGED_FROM = "## CHANGED THIS REGENERATION"
CHANGED_TO = "## HOW THIS FILE IS MAINTAINED"
CHANGED_NEW = """## CHANGED THIS REGENERATION

**S95 (generation 15). Produced by BYTE COPY of generation 14 plus anchored patches
(DECISION S92-5), with the GRAVEYARD carried inside that copy rather than re-inserted.
The whole of this section is replaced, never appended to.**
- MISSION replaced: S95's rule-to-check pass (done) -> S96's macro map, the last row of
  DECISION S93-2's roadmap.
- THE ORDER: a CLOSED AT S95 block added at the top; the S94, S93 and S92 blocks below keep
  their own session labels.
- **`R-S92-2` demoted from CHECKABLE to NOT CHECKABLE.** The reason is written beside the
  rule and in the CLOSED block. It was `yes` for most of the session and three designs died
  proving otherwise; recording the correction is the point (R-S84-3).
- GRAVEYARD: unchanged at SEVEN rows, carried by byte copy - not retyped, not re-read.
- **RULINGS THIS SESSION: NONE.** James set no new direction; S95 executed DECISION S93-2's
  assignment. There is no DECISION S95-n line and the absence is stated, not inferred.
- Judgements made without a ruling, recorded as mine: (a) the manifest ratchet is NOT added
  to CONTRACT, because C1 enforces it mechanically and adding prose law beside a working
  check is exactly the direction ARCHITECTURE 8.3 argues against; (b) the CRLF repair was
  committed rather than history-rewritten.
- ARCHITECTURE: section 7 REGENERATED at S95 from `tools/gni_state.py`; the ROADMAP table's
  S95 row carries its commit. Sections 5 and 6 remain EMPTY and that is the correct state.
- RULES -> five earned, `R-S95-1` .. `R-S95-5`, each carrying a CHECKABLE marker. The
  register now holds 159 ids and PART 0 gains an UNREGISTERED ID MANIFEST of eight rows,
  which `tools/gni_rule_checks.py` reads as C1's escape source.
- CONTRACT: UNCHANGED at v9, byte-identical, md5 `d7e68e815a17eaffbaedc5d6b4494bde`
  (DECISION S89-6). Protocol: UNCHANGED at v11. Nothing about the rules of engagement
  changed; the law-vs-state test says that is the healthy outcome.

**CLOSED:** the S95 MISSION (classification + five executable checks, cert across three
commits) · 5.20's fixture half · one S94 UNKNOWN (the four CI exit integers, measured
1/1/0/0) · `R-S92-2`'s checkability question, answered NO with evidence.

**NEW ITEMS: SIX. rho = 6/1 = 6.00 this generation, and it is not being hidden.**
**5.22** (tools fragile to console encoding and stray CR) · **5.23** (C5 cannot see the
`/tmp` scripts where 5 of 7 instrument errors lived) · **5.24** (22 unnumbered docs cannot
be superseded) · **5.25** (two secrets whose wiring contradicts their consumers) · **6.11**
(one unordered `limit(50)`) · **9.18** (the TypeScript half is unmeasurable).
**Findings routed OUT of this file this session: NONE.**

**ITEMS CONSIDERED AND DELIBERATELY NOT MINTED:** the `\\r\\r\\n` corruption (repaired within
the session, and its lesson is `R-S95-5`, not a queue row) and `gni_state.py`'s control probe
printing `7/7 pass` after a traceback (the same subject as 5.22 - the probe checks the
instrument's LOGIC, not its robustness, and that sentence belongs beside 5.22, not in a new
number).

"""


def splice(text, frm, to, new, label):
    if text.count(frm) != 1:
        sys.exit("REFUSE: %s start anchor matched %d times" % (label, text.count(frm)))
    if text.count(to) != 1:
        sys.exit("REFUSE: %s end anchor matched %d times" % (label, text.count(to)))
    a, b = text.index(frm), text.index(to)
    if not a < b:
        sys.exit("REFUSE: %s anchors out of order" % label)
    return text[:a] + new + text[b:]


def main():
    if not os.path.isfile(SRC):
        sys.exit("REFUSE: %s not found" % SRC)
    if os.path.exists(DST):
        sys.exit("REFUSE: %s already exists" % DST)
    with open(SRC, "rb") as fh:
        raw = fh.read()
    nl = "\r\n" if raw.count(b"\r\n") > raw.count(b"\n") - raw.count(b"\r\n") else "\n"
    text = "\n".join(raw.decode("utf-8-sig").splitlines())

    for anchor, label in ((HEADER_OLD, "header"), (CLOSED_ANCHOR, "closed"),
                          (LIFECYCLE_ANCHOR, "lifecycle")):
        if text.count(anchor) != 1:
            sys.exit("REFUSE: %s anchor matched %d times" % (label, text.count(anchor)))

    graves_before = text.count("| ")
    out = text.replace(HEADER_OLD, HEADER_NEW, 1)
    out = splice(out, MISSION_FROM, MISSION_TO, MISSION_NEW, "mission")
    out = out.replace(CLOSED_ANCHOR, CLOSED_NEW + CLOSED_ANCHOR, 1)
    out = out.replace(LIFECYCLE_ANCHOR, NEW_ITEMS + LIFECYCLE_ANCHOR, 1)
    out = splice(out, CHANGED_FROM, CHANGED_TO, CHANGED_NEW, "changed")

    # --- verification BEFORE the write (R-S95-1) ---
    if out.count("| ") != graves_before:
        sys.exit("REFUSE: table-row count changed %d -> %d; the GRAVEYARD must be untouched"
                 % (graves_before, out.count("| ")))
    if "GENERATION 14" in out:
        sys.exit("REFUSE: generation 14 header survived")
    # Each new id is DEFINED once in THE ORDER and NAMED once in the NEW ITEMS
    # line. Expecting one occurrence was wrong and the guard caught it before a
    # byte was written - which is R-S95-1 doing its job on its own author.
    for rid in ("5.22", "5.23", "5.24", "5.25", "6.11", "9.18"):
        defs = out.count("- **%s** **NEW (S95)" % rid)
        if defs != 1:
            sys.exit("REFUSE: item %s defined %d times, expected 1" % (rid, defs))
        if out.count("**%s**" % rid) != 2:
            sys.exit("REFUSE: item %s appears %d times, expected 2 (definition + summary)"
                     % (rid, out.count("**%s**" % rid)))
    body = (nl.join(out.splitlines()) + nl).encode("utf-8")
    if b"\r\r" in body:
        sys.exit("REFUSE: \\r\\r produced")

    print("newline      : %r" % nl)
    print("table rows   : %d (unchanged - GRAVEYARD carried by bytes)" % graves_before)
    print("new items    : 5.22 5.23 5.24 5.25 6.11 9.18")
    print("bytes        : %d -> %d" % (len(raw), len(body)))

    with open(DST, "wb") as fh:
        fh.write(body)
    print("WROTE        : %s" % DST)


if __name__ == "__main__":
    main()
