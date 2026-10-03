#!/usr/bin/env python3
"""S108 close assembler - the executable record of how every byte of the S108 close set moved.

Byte-copies the S107 set (DECISION S92-5), applies anchored patches (each anchor must occur exactly
once), strips and RE-BINDS every order item to the claims it serves (roadmap 3 row R3-4), writes the
S108 files into OUTDIR, and REFUSES to write anything when the order's two counting scans disagree
with each other, with the declared count or with the cap, when ROOT 5 exceeds its cap, when an item is
left unbound, when a binding no longer holds against the live verdict file, when the printed ORPHAN
RATE differs from the bindings, or when the GRAVEYARD no longer hashes to its published value
(R-S95-1). The architecture is the S108 file already in the tree (written by the 9.23 commit); this
script adds its S108 status block. The macro map is generated LAST from the committed bytes.
usage: python tools/mk_close_s108.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5_CAP = 68, 70, 42
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"

# R3-4 binding, re-made at S108. 9.24 and 9.18 left the queue; 6.10 and 6.13 now serve CLM-751, the
# scheduled-time sentence that replaced CLM-492 on the home page.
BIND = {
    "9.23": ["CLM-440"], "9.19": ["CLM-170"], "9.20": ["CLM-227"], "9.11": ["CLM-538"],
    "9.12": ["CLM-278"], "6.10": ["CLM-230", "CLM-242", "CLM-751"],
    "6.13": ["CLM-230", "CLM-242", "CLM-751"], "6.5": ["CLM-127", "CLM-144"], "6.3": ["CLM-278"],
    "6.4": ["CLM-745"], "5.30": ["CLM-227"], "5.32": ["CLM-621"], "7.1": ["CLM-226"],
    "7.2": ["CLM-226"], "7.3": ["CLM-226"], "7.4": ["CLM-226"], "2.4": ["CLM-220"],
    "3.1": ["CLM-224"], "4.6": ["CLM-621"],
}
PHRASE = {
    "CLM-440": "escalation 0-10", "CLM-170": "Pipeline success rate", "CLM-227": "3 rounds of debate",
    "CLM-538": "100K tokens/day", "CLM-278": "Live Token Quota", "CLM-230": "02:13", "CLM-242": "02:13",
    "CLM-751": "scheduled for 08:43 and 16:43 Myanmar time", "CLM-127": "immutable audit trail",
    "CLM-144": "immutable audit trail", "CLM-745": "Always on", "CLM-621": "MAD is split",
    "CLM-226": "Johari", "CLM-220": "Yahoo Finance", "CLM-224": "sentiment reports",
}
TAG_RE = re.compile(r" \{(?:claims: [^}]*|ORPHAN)\}$")


def die(msg):
    print("REFUSED: " + msg); sys.exit(1)


def rd(root, name):
    with open(os.path.join(root, "docs", name), "rb") as fh:
        return fh.read().decode("utf-8").replace("\r\n", "\n")


def sub1(text, old, new, what):
    n = text.count(old)
    if n != 1:
        die("%s: anchor occurs %d times: %r" % (what, n, old[:80]))
    return text.replace(old, new)


def span(text, start, end, new, what):
    if text.count(start) != 1 or text.count(end) != 1:
        die("%s: span anchors not unique (%d, %d)" % (what, text.count(start), text.count(end)))
    i, j = text.index(start), text.index(end)
    if j <= i:
        die(what + ": span end precedes start")
    return text[:i] + new + text[j:]


def order_range(t):
    return t.split("\n## THE ORDER\n", 1)[1].split("\n## ARCHIVED", 1)[0]


def scans(t):
    r = order_range(t)
    bold = set(m[2:] for m in re.findall(r"\*\*[0-9]+\.[0-9]+", r))
    anyd = set(re.findall(r"[0-9]+\.[0-9]+", r))
    root5 = set(i for i in bold if i.split(".")[0] == "5")
    return bold, anyd, len(root5)


def graveyard_md5(t):
    lines, on, out = t.split("\n"), False, []
    for ln in lines:
        if not on and re.match(r"^## .*GRAVEYARD", ln):
            on = True
        if on:
            out.append(ln)
            if ln.startswith("<!-- GRAVEYARD-END -->"):
                break
    return hashlib.md5(("\n".join(out) + "\n").encode("utf-8")).hexdigest()


def claim_texts(root):
    out = {}
    for ln in rd(root, "GNI_CLAIM_VERDICTS_S108.tsv").split("\n"):
        p = ln.split("\t")
        if len(p) == 5 and p[1] == "CLAIM":
            out[p[3]] = p[4]
    return out


def strip_tags(text):
    head, rest = text.split("\n## THE ORDER\n", 1)
    body, tail = rest.split("\n## ARCHIVED", 1)
    out, n = [], 0
    for ln in body.split("\n"):
        if re.match(r"^\s*-\s+\*\*(\d+\.\d+)\*\*", ln) and TAG_RE.search(ln):
            ln, n = TAG_RE.sub("", ln), n + 1
        out.append(ln)
    return head + "\n## THE ORDER\n" + "\n".join(out) + "\n## ARCHIVED" + tail, n


def bind(text, claims):
    """Append the binding tag to each item's DEFINING line (the first `- **N.N**` line)."""
    head, rest = text.split("\n## THE ORDER\n", 1)
    body, tail = rest.split("\n## ARCHIVED", 1)
    seen, out, orphans = set(), [], 0
    for ln in body.split("\n"):
        m = re.match(r"^\s*-\s+\*\*(\d+\.\d+)\*\*", ln)
        if m and m.group(1) not in seen:
            iid = m.group(1)
            seen.add(iid)
            ids = BIND.get(iid)
            if ids:
                for c in ids:
                    if c not in claims or PHRASE[c] not in claims[c]:
                        die("binding %s -> %s does not hold against the verdict file" % (iid, c))
                ln = ln.rstrip() + " {claims: %s}" % ", ".join(ids)
            else:
                ln = ln.rstrip() + " {ORPHAN}"
                orphans += 1
        out.append(ln)
    missing = set(BIND) - seen
    if missing:
        die("bound ids not in the queue: %s" % sorted(missing))
    return head + "\n## THE ORDER\n" + "\n".join(out) + "\n## ARCHIVED" + tail, orphans, len(seen)


MISSION = """## NEXT SESSION'S MISSION (S109)

**ITEM 9.23 FINISHED.** DONE when all four hold on the committed tree: (a) part 2 is CERTIFIED - the
SQL below shows the first main-pipeline `frequency_log` row written after `2026-10-03 16:51:27+00`
with a non-NULL `escalation_score_raw` and every row before it NULL; (b) `adaptive_pipeline.py` prints
its logged line only when `save_pipeline_run` returned an id, and says it failed otherwise, proved by
the fake-client pattern of S108 (one success, one forced failure); (c) the escalation block on `/alerts`
is either removed or fed by a column that exists - it reads `alert.escalation_score`, which
`health_alerts` does not have; (d) the `historical_correlations` question is put to James as a lettered
ruling with `LINEAGE:` lines - its `avg_escalation_score` averages CAPPED scores, and a raw average
could cover only the reports written since S90.

```sql
select kind, run_at, val,
       case when run_at > timestamptz '2026-10-03 16:51:27+00' then 'AFTER' else 'before' end as side
from (
  select 'adaptive' as kind, run_at, coalesce(mode, 'NULL') as val
  from pipeline_runs where pipeline_type = 'adaptive' and run_at > now() - interval '30 hours'
  union all
  select 'freq', run_at, coalesce(escalation_score_raw::text, 'NULL')
  from frequency_log where run_at > now() - interval '40 hours'
) t
order by kind, run_at desc;
```

WHY THIS. It is the top of ROOT 9 now that 9.24 is closed, and half of it is already shipped and
certified: the run row records its mode (`440b205`, run `37139455249`). What remains is small, and
two of its four parts are false statements the system makes to its operator - a logged line printed
whatever the write did, and a page block that can never render.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. `health_alerts` never stores the escalation:
the spike alert in `health_agent.py` is returned, not passed to `_save_alert`. Only the main pipeline
writes `frequency_log` (`main.py`, Step 3d), from the scorer's `score_breakdown['raw_score']`. Any
`.py` edit stales section 5: run `python tools/gni_blocks.py --session 109` and then
`python tools/gni_macro_map.py --session 109` before the commit (protocol 9a, v16). The container's
HEAD must equal James's before any generator runs (R-S107-1).

ROADMAP 3, ROW R3-4: DECISION S107-8's prediction held at S108 (68 items). The S109 close prints
`python tools/gni_lambda.py --window S108:S109` beside its count.
"""

TARGET_R3 = """**ROADMAP 3 - CLAIMS - ROWS 1 TO 3 DONE, ROW 4 BOUND; ITS PREDICTION HELD AT THE FIRST JUDGING
CLOSE.** Declared at S105 (DECISION S105-1, delegated). R3-1 at S106. R3-2 at `cf1742c`. R3-3 at
`d0612e0`, `203e048`, `4b2b391`. R3-4 bound at S107; DECISION S107-8 judges it on the queue over S108
and S109, and at S108 the count is 68, below 70 - two departures, no arrival. Rows, completion test
and the S108 status in `GNI_ARCHITECTURE_S108.md`.

"""

D2_OLD = ("Residual, itemised: three tables carry no raw column, so their rows point to the report instead "
          "(item 9.23) |")
D2_NEW = ("Residual, itemised (9.23): `frequency_log` carries the raw value from S108, its cert pending; "
          "`health_alerts` never stores the escalation; `historical_correlations` averages capped scores |")
D4_OLD = ("| NOT MET - the claims harvest (R3-2) answered whether the set was complete, and it was not: eight "
          "count and cadence claims are DEFEATED by the tree they describe (check `claim status derived`), "
          "item 9.24 |")
D4_NEW = ("| BOUND HALF MET AT S108 - `claim status derived` prints 0 DEFEATED from `7cfc1d2` (9.24, nine "
          "claims made true). NOT DECLARABLE: 724 of 745 claims are UNMEASURED, and the check speaks only for "
          "what is bound |")

HEAD_OLD = ("Generation 26 held 70.\nThis close CLOSED one item and opened one, so the cap held with no "
            "exception.")
HEAD_NEW = ("Generation 27 held 70.\nThis close CLOSED two items and opened none, so the count FELL to 68.")

ORPHAN_OLD = """**ORPHAN RATE: 50/70**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{claims: CLM-###, ...}` - the public claims it serves, ids from `docs/GNI_CLAIMS_S107.md` - or
`{ORPHAN}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close; the rate is derived.
"""
ORPHAN_NEW = """**ORPHAN RATE: {orph}/{total}**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{{claims: CLM-###, ...}}` - the public claims it serves, ids from `docs/GNI_CLAIMS_S108.md` - or
`{{ORPHAN}}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close and re-made at S108:
6.10 and 6.13 now serve CLM-751, the sentence that replaced CLM-492; the rate is derived.
"""

ITEM_923 = """- **9.23** NEW (S106) [PART 1 CERTIFIED S108; PART 2 SHIPPED, CERT PENDING] - COR - **THE CAPPED
  SCORE PINS EVERY CONSUMER OF THE LEVEL, AND THE TABLES THAT STORE IT COULD NOT SHOW WHAT THE CAP
  HIDES.** Measured at S106: 262 of 263 reports sit at the cap, so the level read from the score has
  been CRITICAL on every run since 2026-06-23, and adaptive runs its no-analysis mode at CRITICAL
  (GNI-R-115). SHIPPED S108 at `440b205`, the two columns added by SQL first: `pipeline_runs.mode`
  records which branch ran - CERTIFIED by run `37139455249`, whose 17:09Z row reads `lightweight` while
  the 15:12Z row before the commit reads NULL; `frequency_log.escalation_score_raw` carries the
  uncapped value from `main.py`, passed through `/api/health`, `/autonomy` and `/health` - CERT
  PENDING on the first main-pipeline row after the commit. REMAINS: (a) `adaptive_pipeline.py` prints
  `OK Adaptive run logged` whatever `save_pipeline_run` returned, because that function swallows its
  own exception and returns None; (b) the S106 text named an `alerts` table and none exists:
  `health_alerts` never stores the escalation, so the escalation block on `/alerts` can never render;
  (c) `historical_correlations.avg_escalation_score` averages CAPPED scores, and a raw average would
  cover only the reports written since S90 - a new statistic over a biased subset, James's ruling, not
  a mechanical carry. NOT a recalibration - the GRAVEYARD rules that out. Whether ROOT 8 returns from
  the archive on this measurement is James's.
"""

NOTE_920_ANCHOR = ("  amendment describes; they look alike in a run list and are different doors. Do not conflate.\n")
NOTE_920 = NOTE_920_ANCHOR + """  NOTE (S108) [MEASURED]: the same manual path reports a second false status. Check 2 of
  `mad_preflight.py` filters `pipeline_type = 'gni_pipeline'`; no row carries it (SQL: 265 `main`, 933
  `adaptive`, nothing else), so every preflight prints that the run table is empty. The instrument saw
  data, so the zero indicts the filter (R-S81-1). Folded here, not opened, by DECISION S108-5.
"""

LINE_918 = "- **9.18** OPEN (S95) - COR. Carried unchanged.\n"

ARCHIVED_HEAD_OLD = "## ARCHIVED - ONE ITEM CLOSES INTO IT THIS GENERATION"
ARCHIVED_HEAD_NEW = "## ARCHIVED - TWO ITEMS CLOSE INTO IT THIS GENERATION"
ARCHIVED_ROWS = (
    "| **9.24** the eight public claims the tree defeated | CLOSED S108 at `7cfc1d2`, the session's "
    "mission. They were nine: CLM-498 stated two counts and was bound to the true one, so it was bound "
    "FIRST and the check went red (9 DEFEATED) before it went green (0). Workflow copy made count-free - "
    "the ninth workflow file is a CI harness run on push, so \"9\" would have been false (R-S108-2); "
    "injection copy now says 81, bound to F-INJ; the home page's time now says scheduled. Read LIVE after "
    "Vercel `success`: six pages by HTML hits 0 to 1, the home page by the deployed client chunk (new 1 "
    "and 1, old 0 and 0), because its sentences sit in a client branch a fetch never receives. |\n"
    "| **9.18** the TypeScript half of the position-select surface is unmeasurable | CLOSED S108 BY THE "
    "RETIRE CLAUSE, as accepted. Opened S95 with a real measurement (35 `.limit()` sites under "
    "`src/app/api/`, no TypeScript parser in a stdlib tool), then carried as a bare \"Carried unchanged\" "
    "for eleven regenerations - no measurement, no ruling, no claim served. The public half it worried "
    "about was closed at S106 by reading, not parsing: 9.22(b) moved every count to an exact count and "
    "R-S106-3 forbids a limited length shown as a count. The limit stays true and is accepted. |\n")

CHANGED = """## CHANGED THIS REGENERATION

- **DECISION S108-1 (delegated).** 9.24 by binding CLM-498's hidden value first and rewriting copy to
  its referent: workflow sentences count-free, injection count 81 bound to F-INJ, the home page's time
  labelled as scheduled. Over copying the instrument's numbers (green check, five false pages) and over
  narrowing F-WF so "8" could stay (an instrument changed to pass a claim, wider than the mission).
- **DECISION S108-2 (James).** After the mission: continue to 9.23 and read the two unread MAD runs.
- **DECISION S108-3 (James).** Design and build 9.23 in this session rather than close first.
- **DECISION S108-4 (delegated).** 9.23 option B: the run row's mode plus the raw value on
  `frequency_log`, columns by SQL before code. Over mode alone (half the item) and over adding a raw
  average to `historical_correlations` (a new statistic over a biased subset - parked for James).
- **DECISION S108-5 (close judgement, not delegated; James may overrule).** No item opened. The
  `mad_preflight` filter joins 9.20, the same manual path's false status; the `/alerts` dead block and
  the unconditional logged line join 9.23, the same table and the same writer; F-WF's scope is noted
  here and not itemised, because no live claim is bound to F-WF since 9.24 closed; the masked model id
  goes to the handoff's UNKNOWNS with its new route. Over opening four items under a full cap.
- **DECISION S108-6 (close judgement, not delegated).** 9.18 closed by the retire clause - eleven
  regenerations as a bare line, ORPHAN, its public half closed at S106 by 9.22(b) and R-S106-3.
- CLOSED 9.24 (mission) and 9.18 (retire clause) - OPENED none - count 68, ROOT 5 at 41, ORPHAN 49/68.
  DECISION S107-8's prediction holds at its first judging close. The fall is two departures and no
  arrival; under the cap that is the only way the count can fall (R-S107-3).
- **NOT ACTED, NAMED: 5.25's retire clause is due again.** DECISION S92-2 paused its class's clocks,
  so retiring it is James's.
- **9.23 REWRITTEN** with what S108 measured: part 1 certified, part 2 pending, the table name
  corrected, two residuals added. **9.20** gains the preflight note.
- **SHIPPED**: `7cfc1d2` (9.24) and `440b205` (9.23), both CI-green at job level and Vercel `success`;
  two nullable columns added by SQL before the code; one manual adaptive dispatch for the cert.
- **MEASURED**: claims 745 at 798 locations, COVERAGE 21/745, 0 DEFEATED - coverage fell from 25
  because nine measured claims were retired with the copy and four of their successors are count-free.
  `pipeline_runs`: 265 main, 933 adaptive. The adaptive gap between runs is three to six hours, because
  the heartbeat dispatches it on an escalation delta; the half-hour CRITICAL interval is a floor.
- **L2 MAD**: three runs since the S107 handoff, split at job level - two debates, one watch. Read by
  id: the evening debate (depth=0, 39 of 39 arrived, verdict neutral) and the watch (seven days: 151
  consultant and 117 arbitrator hits over 14 runs). The morning debate was not read.
- **FOUND IN THE TOOLS THIS SESSION**: any `.py` edit stales section 5 at the MISSION commit, so the
  9.23 runner regenerates it and the macro map before staging (protocol 9a, v16 - caught in a dry run,
  not by CI); a glossary NAMESPACES pattern may not end in an asterisk, because the cell reader strips
  asterisks as bold markup (caught by the check labelled `glossary` during this close).
- CONTRACT UNCHANGED (v11). PROTOCOL UNCHANGED (v20). Three rules and two further instances are in
  `GNI_RULES_S108.md`.

"""

MAINTAINED_OLD = ("`tools/mk_close_s107.py`, which refuses on any disagreement, on an unbound item, and on an ORPHAN\n"
                  "RATE that differs from the bindings it just wrote.")
MAINTAINED_NEW = ("`tools/mk_close_s108.py`, which refuses on any disagreement, on an unbound item, on a binding\n"
                  "that no longer holds against the verdict file, and on an ORPHAN RATE that differs from the\n"
                  "bindings it just wrote.")

RULES_BLOCK = """
## S108 ADDITIONS (2026-10-03)

- R-S108-1 - "0 DEFEATED" DISCRIMINATES ONLY WHEN EVERY MEASURABLE VALUE IN A BOUND CLAIM HAS ITS OWN
  BINDING. CLM-498 stated two counts - 42 RSS sources and 70 injection patterns - and was bound to the
  first alone, so it read SUPPORTED while its second half was false; fixing the eight DEFEATED claims
  would have printed 0 with "70" still on the home page. Before a claim set is declared clean, census
  every bound claim for a measurable value no binding covers, and bind the missing one FIRST, so the
  check goes red before it goes green.
  **CHECKABLE: yes** - a census over the verdict and binding files finds a fitness-shaped value with no row.

- R-S108-2 - A FITNESS FUNCTION'S MEASURED SET MUST BE THE CLAIM'S REFERENT BEFORE ITS VERDICT IS ACTED
  ON. F-WF counts every workflow file; the pages said eight autonomous workflows and named exactly
  eight; the ninth file is a CI harness run on push. Copying "9" would have turned the check green and
  five pages false. When a DEFEATED claim and its instrument disagree about WHAT is counted, correct the
  sentence to what is true of its referent and record the instrument's scope as a finding - never copy
  the instrument's number into the copy.
  **CHECKABLE: no** - deciding a claim's referent is a reading, not a parse.

- R-S108-3 - A SUCCESS LINE PRINTED AFTER A CALL THAT SWALLOWS ITS OWN FAILURE CERTIFIES NOTHING.
  `save_pipeline_run` catches its exception and returns None; `adaptive_pipeline.py` prints that the
  run was logged either way, and S108's own cert script grepped that line. A write is certified by
  reading the written row, split at the commit time into before and after, never by the writer's
  message about itself.
  **CHECKABLE: no** - it constrains how a certification is designed.

## FURTHER INSTANCE of R-S105-3 (a phrase counted in a rendered page counts its rendering path)
S108 predicted one hit on the home page for a corrected sentence. The page is a client component; the
sentence sits in a toggle closed by default, inside a branch that needs articles loaded, so the HTML a
fetch receives never holds it and the read printed 0 on a good build. The home claims were proved from
the deployed client chunk instead. Read the component boundary and every condition around a line
BEFORE predicting its count - S108 did that for the empty-state line and not for its neighbour.
**CHECKABLE: no** - it constrains how a prediction is made.

## FURTHER INSTANCE of R-S105-2 (a live read proves it read the NEW build)
S108's runner required each page's bytes to change after the deploy. Two edits replaced "70" with
"81": same length, same byte count, a correct build - the hit count moving from 0 to 1 discriminated,
the byte count could not. And a local chunk hash is not the deployed build's identity: the two differed
(build-time environment inlining is the likely cause, unmeasured). A proof is content only the new
source can produce, read against a control taken before the push.
**CHECKABLE: no** - it constrains how a verification is designed.
"""

ARCH_ANCHOR = ("  S99's; an inference, not a measurement). The real claim count is 745. The White Paper is in the tree.\n"
               "- **AGENT TEST**: not yet run.\n")
ARCH_BLOCK = ARCH_ANCHOR + """
### STATUS AT THE S108 CLOSE - R3-4'S PREDICTION HELD AT THE FIRST OF ITS TWO JUDGING CLOSES

- Generation 28 holds **68** items against a cap of 70: 9.24 closed by its mission (`7cfc1d2`) and 9.18
  by the retire clause; none opened. DECISION S107-8's hypothesis - the count falls below 70 over
  S108-S109 - holds at S108 and is judged again at S109. The fall is two departures with no arrival,
  the only way a capped count can fall (R-S107-3). `python tools/gni_lambda.py --window S108:S108`
  reports the arrival side by the baseline's own command.
- The claims document reads 745 claims at 798 locations, COVERAGE 21/745, **0 DEFEATED**. COVERAGE
  FELL from 25: nine measured claims were retired with their copy, five successors are measured, and
  four are count-free and declared QUALITATIVE (DECISION S108-1). A falling coverage figure is the cost
  of preferring a sentence with no number, and it is published, not hidden.
- One instrument finding, recorded and not itemised: F-WF counts every workflow file, a wider set than
  the "autonomous workflows" the pages meant (R-S108-2). No live claim is bound to it.
- **AGENT TEST**: not yet run.
"""

GLOSS_OLD = "# GNI GLOSSARY - S107"
GLOSS_NEW = "# GNI GLOSSARY - S108"
# Rows the S108 documents need (the check labelled `glossary` named exactly these four).
GLOSS_ROWS = [
    ("| SQL | the query language of the Supabase database |",
     "| OK | the success word a script prints about its own action; it certifies nothing unless the "
     "action's result was checked first (R-S108-3) | HANDOFF S108; `ai_engine/adaptive_pipeline.py` |\n"
     "| RSS | Really Simple Syndication: the feed format of the sources the collector reads | "
     "`ai_engine/collectors/rss_collector.py`; GNI_RULES |\n", "glossary OK, RSS"),
    ("| EXTENT | emphasis |", "| DECLARABLE | emphasis |\n", "glossary DECLARABLE"),
    ("| `D\\d+` | TWO SERIES:",
     "| `F-[A-Z]+(?:-[A-Z]+){0,3}` | a fitness function in `tools/gni_fitness.py` (F-INJ, F-WF, F-CRON-PIPE); "
     "a binding row names one beside a verbatim fragment of its claim |\n", "glossary F- namespace"),
]


def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s108.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    if not os.path.exists(os.path.join(out, "HANDOFF_S108.md")):
        die("HANDOFF_S108.md must already be in OUTDIR (written from the Part B template)")
    res = {}
    claims = claim_texts(root)

    o = rd(root, "GNI_TARGET_AND_ORDER_S107.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S107 order does not hash to its published value")
    o = sub1(o, "**GENERATION 27 - 2026-10-03 (S107 close). SUPERSEDES generation 26\n(`GNI_TARGET_AND_ORDER_S106.md`).**",
             "**GENERATION 28 - 2026-10-03 (S108 close). SUPERSEDES generation 27\n(`GNI_TARGET_AND_ORDER_S107.md`).**", "header")
    o = span(o, "## NEXT SESSION'S MISSION (S108)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = span(o, "**ROADMAP 3 - CLAIMS - ROWS 1 TO 3 DONE, ROW 4 BOUND AT S107.**",
             "**DEFINITION OF DONE - RESTATED AT S105", TARGET_R3, "target roadmap")
    o = sub1(o, D2_OLD, D2_NEW, "dod d2")
    o = sub1(o, D4_OLD, D4_NEW, "dod d4")
    o = sub1(o, "**EXPECTED ITEM COUNT: 70 distinct numbered items", "**EXPECTED ITEM COUNT: 68 distinct numbered items",
             "expected count")
    o = sub1(o, HEAD_OLD, HEAD_NEW, "order head")
    o = o.replace("docs/GNI_TARGET_AND_ORDER_S107.md \\\n", "docs/GNI_TARGET_AND_ORDER_S108.md \\\n")
    o = sub1(o, "Both must print **70**.", "Both must print **68**.", "both print")
    o = sub1(o, "`tools/mk_close_s107.py`, which refuses to write when they disagree",
             "`tools/mk_close_s108.py`, which refuses to write when they disagree", "head tool")
    o, ntags = strip_tags(o)
    if ntags != 70:
        die("expected 70 binding tags in generation 27, stripped %d" % ntags)
    o = span(o, "- **9.24** NEW (S107) [MEASURED]", "- **9.23** NEW (S106) [MEASURED]", "", "9.24 out")
    o = span(o, "- **9.23** NEW (S106) [MEASURED]", "- **9.19** OPEN (S96)", ITEM_923, "9.23 rewritten")
    o = sub1(o, NOTE_920_ANCHOR, NOTE_920, "9.20 note")
    o = sub1(o, LINE_918, "", "9.18 out")
    o = sub1(o, ARCHIVED_HEAD_OLD, ARCHIVED_HEAD_NEW, "archived head")
    o = sub1(o, "| what | why archived |\n|---|---|\n", "| what | why archived |\n|---|---|\n" + ARCHIVED_ROWS, "archived")
    o = span(o, "## CHANGED THIS REGENERATION", "## HOW THIS FILE IS MAINTAINED", CHANGED, "changed")
    o = sub1(o, MAINTAINED_OLD, MAINTAINED_NEW, "maintained")
    o, orphans, total = bind(o, claims)
    o = sub1(o, ORPHAN_OLD, ORPHAN_NEW.format(orph=orphans, total=total), "orphan rate")
    for gone in ("9.24", "9.18"):
        if gone in order_range(o):
            die("closed id %s is still cited inside the queue" % gone)
    bold, anyd, r5 = scans(o)
    print("order scans: bold=%d any=%d root5=%d orphan=%d/%d (want %d/%d/<=%d)"
          % (len(bold), len(anyd), r5, orphans, total, COUNT, COUNT, ROOT5_CAP))
    if anyd - bold:
        die("the any-digits scan sees non-item numbers in the queue: %s" % sorted(anyd - bold))
    if not (len(bold) == len(anyd) == total == COUNT <= CAP and r5 <= ROOT5_CAP):
        die("order counts disagree, exceed the cap, or an id has no defining line")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD changed during assembly")
    res["GNI_TARGET_AND_ORDER_S108.md"] = o

    rl = rd(root, "GNI_RULES_S107.md")
    if "R-S108-" in rl:
        die("the S107 register already holds an R-S108 id")
    res["GNI_RULES_S108.md"] = rl.rstrip("\n") + "\n" + RULES_BLOCK

    res["GNI_Session_Transfer_Protocol_S108.md"] = rd(root, "GNI_Session_Transfer_Protocol_S107.md")
    res["CONTRACT_S108.md"] = rd(root, "CONTRACT_S107.md")
    g = sub1(rd(root, "GNI_GLOSSARY_S107.md"), GLOSS_OLD, GLOSS_NEW, "glossary title")
    for anchor, row, what in GLOSS_ROWS:
        g = sub1(g, anchor, row + anchor, what)
    res["GNI_GLOSSARY_S108.md"] = g
    ar = rd(root, "GNI_ARCHITECTURE_S108.md")
    res["GNI_ARCHITECTURE_S108.md"] = sub1(ar, ARCH_ANCHOR, ARCH_BLOCK, "architecture status")

    for name, text in sorted(res.items()):
        data = text.encode("utf-8")
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(data)
        print("%-40s %7d bytes  md5 %s (EOL-normalised)" % (name, len(data), hashlib.md5(data).hexdigest()))
    print("WROTE %d files beside HANDOFF_S108.md. The macro map is generated LAST." % len(res))


if __name__ == "__main__":
    main()
