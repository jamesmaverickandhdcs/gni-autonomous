#!/usr/bin/env python3
"""S109 close assembler - the executable record of how every byte of the S109 close set moved.

Byte-copies the S108 set (DECISION S92-5), applies anchored patches (each anchor must occur exactly
once), strips and RE-BINDS every order item to the claims it serves (roadmap 3 row R3-4), writes the
S109 files into OUTDIR, and REFUSES to write anything when the order's two counting scans disagree
with each other, with the declared count or with the cap, when ROOT 5 exceeds its cap, when an item is
left unbound, when a binding no longer holds against the live verdict file, when a closed id is still
cited in the queue, or when the GRAVEYARD no longer hashes to its published value (R-S95-1). The
architecture is the S109 file already in the tree (written by the S109 product commits); this script
adds its S109 status block. The macro map is generated LAST from the committed bytes.
usage: python tools/mk_close_s109.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5_CAP, ORPHANS = 65, 70, 42, 47
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"
CLOSED = ("9.23", "9.20", "9.16")

# R3-4 binding, re-made at S109. 9.23 and 9.20 left the queue (bound); 9.16 left (ORPHAN); 9.5 now
# serves the two empty-state sentences on /alerts that its remainder carries.
BIND = {
    "9.19": ["CLM-170"], "9.5": ["CLM-692", "CLM-693"], "9.11": ["CLM-538"],
    "9.12": ["CLM-278"], "6.10": ["CLM-230", "CLM-242", "CLM-751"],
    "6.13": ["CLM-230", "CLM-242", "CLM-751"], "6.5": ["CLM-127", "CLM-144"], "6.3": ["CLM-278"],
    "6.4": ["CLM-745"], "5.30": ["CLM-227"], "5.32": ["CLM-621"], "7.1": ["CLM-226"],
    "7.2": ["CLM-226"], "7.3": ["CLM-226"], "7.4": ["CLM-226"], "2.4": ["CLM-220"],
    "3.1": ["CLM-224"], "4.6": ["CLM-621"],
}
PHRASE = {
    "CLM-170": "Pipeline success rate", "CLM-227": "3 rounds of debate", "CLM-538": "100K tokens/day",
    "CLM-278": "Live Token Quota", "CLM-230": "02:13", "CLM-242": "02:13",
    "CLM-751": "scheduled for 08:43 and 16:43 Myanmar time", "CLM-127": "immutable audit trail",
    "CLM-144": "immutable audit trail", "CLM-745": "Always on", "CLM-621": "MAD is split",
    "CLM-226": "Johari", "CLM-220": "Yahoo Finance", "CLM-224": "sentiment reports",
    "CLM-692": "Alerts fire via Telegram", "CLM-693": "This page archives all alerts",
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
    for ln in rd(root, "GNI_CLAIM_VERDICTS_S109.tsv").split("\n"):
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


MISSION = """## NEXT SESSION'S MISSION (S110)

**ROADMAP 3's AGENT TEST, THEN ITEM 9.5's REMAINDER.** DONE when: (a) James asks the session, verbatim,
*"why are we doing Smart Office?"*; the session answers from the repository's documents alone; James's
verdict is written as ONE line in `docs/GNI_ORIGIN.md` in the completion test's form
`AGENT-TEST <date> S110 PASS|FAIL -- <reason>`, and `grep -cE '^AGENT-TEST .* PASS ' docs/GNI_ORIGIN.md`
prints 1 or more on PASS; (b) on PASS, roadmap 3 is declared ACHIEVED at the S110 close with its
evidence and CONTRACT's PHASE TRANSITION runs before the order is regenerated - JAMES declares the next
target or roadmap together with its written completion test; on FAIL, the reason becomes roadmap 3's
next row, not a footnote; (c) with the time left, 9.5's F16 to F19 are measured and each is PAID, FIXED
or ruled.

WHY THIS, NOT THE TOP ITEM. The top of ROOT 9 is 9.19, which waits on evidence no session can force (a
run at `ctx-trim@0`). R3-4 is DONE - DECISION S107-8's prediction held at both judging closes, 68 and
then 65, with zero arrivals - and the completion test's replay is recorded in the architecture since
S107. The agent test is the only line left between roadmap 3 and ACHIEVED, and it needs exactly what
S110 is: a fresh session holding only the repository. DECISION S109-9, a close judgement James may
overrule.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. The S69 registry in
`docs/SUBPAGE_CERTIFICATION.md` has been frozen since S70; 9.5's text is the live census. F16 to F19
are the `/researcher` trend chart, the `/research` confidence width at three runs, the two populations
on `/correlations`, and the correct-count beside the percentage on `/predictions`. Read each page's
code AND its data map before predicting a count (R-S105-3, R-S109-1). A copy change mints claim units:
add verdict and binding rows to the S110 `.tsv` files before `python tools/gni_claims.py --write 110`.
Runners carry a `--ship` mode, so the run box stays three lines.
"""

TARGET_R3 = """**ROADMAP 3 - CLAIMS - FOUR ROWS DONE; THE AGENT TEST IS ALL THAT STANDS BETWEEN IT AND ACHIEVED.**
Declared at S105 (DECISION S105-1, delegated). R3-1 at S106. R3-2 at `cf1742c`. R3-3 at `d0612e0`,
`203e048`, `4b2b391`. R3-4 bound at S107; DECISION S107-8 judged it on the queue over S108 and S109:
68, then 65 - five departures and no arrival - so the prediction HELD at both closes. Rows, completion
test and the S109 status in `GNI_ARCHITECTURE_S109.md`. ROADMAP CHECK (Part C step 4a): roadmap 3,
rows four of four; ACHIEVED waits on Test 2 alone.

"""

D2_OLD = ("Residual, itemised (9.23): `frequency_log` carries the raw value from S108, its cert pending; "
          "`health_alerts` never stores the escalation; `historical_correlations` averages capped scores |")
D2_NEW = ("Residual CLOSED S109: `frequency_log` carries the raw value, certified (18.4, 21.5); "
          "`health_alerts` never stored the escalation and the block that read it is gone; "
          "`historical_correlations` keeps a capped average labelled as capped (DECISION S109-2) |")
D4_OLD = "BOUND HALF MET AT S108 - `claim status derived` prints 0 DEFEATED from `7cfc1d2`"
D4_NEW = "BOUND HALF MET AT S108, HELD AT S109 - `claim status derived` prints 0 DEFEATED from `7cfc1d2` through `c78c288`"
D4B_OLD = "NOT DECLARABLE: 724 of 745 claims are UNMEASURED"
D4B_NEW = "NOT DECLARABLE: 727 of 748 claims are UNMEASURED"

HEAD_OLD = ("Generation 27 held 70.\nThis close CLOSED two items and opened none, so the count FELL to 68.")
HEAD_NEW = ("Generation 28 held 68.\nThis close CLOSED three items and opened none, so the count FELL to 65.")

ORPHAN_NEW = """**ORPHAN RATE: {orph}/{total}**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{{claims: CLM-###, ...}}` - the public claims it serves, ids from `docs/GNI_CLAIMS_S109.md` - or
`{{ORPHAN}}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close and re-made at S109: 9.5
now serves CLM-692 and CLM-693, the two empty-state sentences its remainder carries; the rate is derived.

"""

ITEM_95 = """- **9.5** OPEN - COR - **THE S69 CENSUS, RE-READ AGAINST THE S109 TREE.** The open registry in
  `docs/SUBPAGE_CERTIFICATION.md` had been frozen since S70. PAID by the tree, no action: F1 (no
  "70-pattern" left), F3 ("seven states" is TRUE - the status map, the legend and the route all hold
  seven; R-S109-1), F15 (relabelled "Last 10 Runs"), F5's copy. FIXED at S109: F12 and its class
  (`d87f57a` - four `pipeline_runs` readers now filter `main`; R-S109-2), F13 (`848b256`), and F14 with
  three sibling pages (`c78c288` - one rule in `src/lib/verdict.ts`; R-S109-3). REMAINS: (a) F16 to F19,
  unmeasured - browser and database; (b) the empty-state copy on `/alerts` says Telegram alerts are
  archived there and none are - it renders only when the table is empty; (c) a detector check, kin of
  the one labelled `escalation magnitude`, that refuses a page comparing `mad_verdict` itself, shipped
  with its fixture family; (d) the run-count governor (`get_pipeline_run_count`, unfiltered) is
  DORMANT - one active prompt variant, and health ran on 6 of 60 mains under either count (DECISION
  S109-8) - REOPEN the moment a second variant is activated; (e) the PENDING banner is proved in the
  deployed chunk, not yet on real data. LEAD, not itemised: a TypeScript route defaults to a retired
  model id (the note on **5.31**).
"""

NOTE_919_ANCHOR = "Next move: find a run at `ctx-trim@0`."
NOTE_919 = NOTE_919_ANCHOR + ("\n  S109 read two more debates (`37190098951`, `37110117798`): `ctx-trim@5121` and `@4930` -"
                              " characters\n  of context kept, never zero.")

NOTE_610_ANCHOR = "- **6.5** OPEN - COR - **THERE IS NO BACKUP.**"
NOTE_610 = """  NOTE (S109) [MEASURED]: the main pipeline started at 08:05Z and 14:43Z on Oct 3, and at 08:26Z and
  15:22Z on Oct 4, against a cron of 02:13 and 10:13 UTC - about six hours late every time. The adaptive
  protection and blackout windows (GNI-R-118, GNI-R-122) are keyed to the cron times, so they no longer
  bracket the runs they were written to protect. A lead folded here, not opened (DECISION S109-9).
""" + NOTE_610_ANCHOR

NOTE_616_ANCHOR = "  broken; the reproducible install path is.\n"
NOTE_616 = NOTE_616_ANCHOR + "  NOTE (S109): still true at `c78c288` - `npm ci` refused with the same `EUSAGE` in the S109 container.\n"

NOTE_531_ANCHOR = "- **5.31** OPEN (S98) [MEASURED] - PRE. Model resolution has no floor; resolved at module import.\n"
NOTE_531 = NOTE_531_ANCHOR + """  NOTE (S109): a TypeScript sibling - `src/app/api/stock-context/route.ts` falls back to a retired Llama
  model id when its environment variable is unset. Found by the S69 census re-read, folded here.
"""

ARCHIVED_HEAD_OLD = "## ARCHIVED - TWO ITEMS CLOSE INTO IT THIS GENERATION"
ARCHIVED_HEAD_NEW = "## ARCHIVED - THREE ITEMS CLOSE INTO IT THIS GENERATION"
ARCHIVED_ROWS = (
    "| **9.23** the capped score's consumers, and tables that could not show what the cap hides | CLOSED S109, "
    "the session's mission. (a) `frequency_log.escalation_score_raw` CERTIFIED: the first main rows after "
    "`440b205` read 18.4 and 21.5, every row before NULL; (b) the adaptive run's logged line reports the written "
    "row (`720e374`; run `37201358890` printed id `0de95f4e`, the row's own id); (c) the `/alerts` block that read "
    "a column `health_alerts` lacks is removed (DECISION S109-1); (d) `historical_correlations` keeps its capped "
    "average, labelled as capped (DECISION S109-2). |\n"
    "| **9.20** two false statuses on the manual MAD path | CLOSED S109. `mad_preflight.py` check 2 filtered the "
    "QUOTA pipeline name; it filters `main` (`ea74cc9`; live preflight: \"table empty\" before, \"Gap since "
    "Intelligence: 251 min\" after). The four `return True` exits of `mad_runner.py` stay: over 60 runs, 40 of 40 "
    "`run-mad success` jobs carried `ARB-FIT`, so no job count was ever wrong; PROTOCOL v21 Part D step 4 now "
    "confirms a debate by `ARB-FIT` (DECISION S109-3). |\n"
    "| **9.16** a workflow record taken from one side only | CLOSED S109 BY MEASUREMENT (DECISION S109-4). Both "
    "sides read: 8 of 9 workflows run `actions/setup-python` at 3.11; `gni_selfcheck.yml` runs the runner's own "
    "`python3`, unpinned. No live document repeats the S93 sentence. The unpinned interpreter is a lead, not "
    "itemised. |\n"
)

CHANGED = """## CHANGED THIS REGENERATION

- **DECISION S109-1 (delegated).** The `/alerts` escalation block removed - over adding capped and raw
  columns to `health_alerts` and saving the spike alert: a new writer, a new schema and a cert that waits
  on a spike while every score sits at the cap.
- **DECISION S109-2 (delegated).** `historical_correlations` keeps the capped average, labelled - over a
  raw average of the S90-onward subset beside it, two populations side by side. Weakness named: near the
  cap the figure carries little information.
- **DECISION S109-3 (delegated).** No runner change for the four clean exits; Part D step 4 confirms a
  debate by `ARB-FIT` - over a non-zero exit (red runs for an event never observed) and over a step output.
- **DECISION S109-4 (delegated).** 9.16 closed by measurement from both sides.
- **DECISION S109-5 (delegated).** The four readers that mean "the pipeline run" filter `main`; the
  run-count governor is left for simulation - over filtering all five at once and over the alert and the
  card alone.
- **DECISION S109-6 (delegated).** F13 option B: the two tiles and the dead block removed, a link to
  `/adaptive-log` - over counting adaptive runs on `/alerts`, a second copy of a count that drifts.
- **DECISION S109-7 (delegated).** F14 option A: one rule in `src/lib/verdict.ts` for four pages - over
  `/comparison` alone (the home page would still contradict it) and over shipping the detector check now
  (carried in 9.5 with its fixture family).
- **DECISION S109-8 (delegated).** The governor stays dormant with a trigger: one active variant, health
  6 against 6 over 60 mains.
- **DECISION S109-9 (close judgement, not delegated; James may overrule).** No item opened: the cron-drift
  lead joins 6.10, the TypeScript model default joins 5.31, the unpinned selfcheck interpreter is named
  in 9.16's archive row, the empty-state copy and the verdict check join 9.5 - over four new items under a
  cap. And S110's mission is roadmap 3's agent test rather than the top item, for the reason written in it.
- **DECISION S109-10 (James).** Continue after the mission, twice.
- CLOSED 9.23 (mission), 9.20 and 9.16 - OPENED none - count 65, ROOT 5 at 41, ORPHAN 47/65. DECISION
  S107-8's prediction HELD at its second judging close; `python tools/gni_lambda.py --window S108:S109`
  prints no arrival over the two closes.
- **NOT ACTED, NAMED: 5.25's retire clause is due again** (DECISION S92-2 makes it James's). The
  retire-clause audit was NOT re-run item by item at this close.
- **9.5 REWRITTEN** as the live census. **9.19** gains two more runs; **6.10**, **6.16**, **5.31** gain notes.
- **SHIPPED**: `720e374`, `ea74cc9`, `d87f57a`, `848b256`, `c78c288` - each CI-green at job level, Vercel
  `success`, and live-read against a control taken before its push. One manual adaptive dispatch.
- **MEASURED**: claims 748 at 801 locations, COVERAGE 21/748, 0 DEFEATED - CLM-691 retired, CLM-755 to
  CLM-758 minted. `health_alerts`: 13 rows ever, 10 of them `avg 0` alerts since June, written over
  adaptive rows. `reports.mad_verdict`: 153 neutral, 100 bearish, 8 bullish, 5 left `pending` for good;
  14 arbitrator failures, all stored as neutral. The Oct 3 and Oct 4 main runs started about six hours
  after cron.
- **L2 MAD**: 40 of 40 debate jobs carried `ARB-FIT` (Sep 14 - Oct 4). Two debates read by id.
- **FOUND IN THE TOOLS**: a copy change mints claim units, and `gni_claims.py --write` refuses until each
  has a verdict row AND a binding row; `npm ci` still refuses on the lockfile (6.16); the container's
  GitHub API calls are rate-limited.
- CONTRACT UNCHANGED (v11). PROTOCOL v21 - Part D step 4 only. Three rules and one further instance are
  in `GNI_RULES_S109.md`.

"""

MAINTAINED_OLD = "`tools/mk_close_s108.py`, which refuses on any disagreement, on an unbound item, on a binding\n"
MAINTAINED_NEW = "`tools/mk_close_s109.py`, which refuses on any disagreement, on an unbound item, on a binding\n"

RULES_BLOCK = """
## S109 ADDITIONS (2026-10-04)

- R-S109-1 - A COMMENT IS A CLAIM ABOUT THE CODE, NOT THE CODE. S109 called CLM-365's "seven states" a
  hidden false half because a comment above the status map said "5-state taxonomy"; the map holds seven,
  the legend renders seven from its order list, and the route emits seven. Before stating what code does
  - in a finding, a prediction or a fix - read the data structure or the condition itself. A comment is
  evidence of an intent at the time it was written.
  **CHECKABLE: no** - it constrains how a reading is done.

- R-S109-2 - A TABLE THAT HOLDS TWO POPULATIONS NAMES ITS POPULATION IN EVERY READ. `pipeline_runs`
  holds main rows and adaptive rows (265 and 933 at S108), and adaptive rows carry `total_collected = 0`.
  Five readers that meant "the pipeline run" read both: the preflight's check 2, the health agent's
  RUN_GAP and LOW_COLLECTION checks (3 of 3 alerts in 30 days false), `should_run_now`, and the public
  "Last Pipeline Run" card, which showed 0 articles. The graph job had fixed the same class in June by
  switching tables, and no sibling sweep followed (R-S55-1). When a writer starts putting a second
  population into a shared table, grep every reader of that table in the same commit and give each one
  its filter.
  **CHECKABLE: yes** - a grep for `pipeline_runs` reads with no `pipeline_type` filter, against a named
  allowlist of readers meant to see both populations.

- R-S109-3 - A WRITER'S PLACEHOLDER IS A STATE THAT EVERY READER MUST NAME. `main.py` writes
  `mad_verdict = 'pending'` at insert, and a failed arbitrator stores a default `'neutral'`. The
  `/comparison` rule knew only real verdicts and `'neutral'`, so `'pending'` rendered as a DISAGREEMENT
  - "trust the divergence signal" - about a debate that had not run, and five reports stayed pending for
  good; the home page called every neutral debate DIVERGING. When a column carries a placeholder or a
  failure default, the rule that reads it lives in one place (`src/lib/verdict.ts`, as the escalation
  wording lives in `src/lib/escalation.ts`) and names the placeholder explicitly.
  **CHECKABLE: yes** - a check of the `escalation magnitude` kind could refuse a page that compares
  `mad_verdict` itself; item 9.5 carries it.

## FURTHER INSTANCE of R-S105-3 (read every condition around a line before predicting its count)
S109 predicted a LOW_COLLECTION alert at the Oct 4 main run from the contents of the window the check
reads, and was right about the window and wrong about the alert: the health checks run only when the
row count is a multiple of ten (`main.py`, six lines above the call). The wrong prediction is what found
the run-count governor. Read the gate before the body.
**CHECKABLE: no** - it constrains how a prediction is made.
"""

PROTO_TITLE_OLD = "# GNI SESSION TRANSFER PROTOCOL v20"
PROTO_TITLE_NEW = "# GNI SESSION TRANSFER PROTOCOL v21"
PROTO_STEP4_ANCHOR = "   computes a negative (R-S84-4, amended S99).\n"
PROTO_STEP4_NEW = PROTO_STEP4_ANCHOR + """   AMENDED S109: job level SEPARATES the debate from the watch; it does not prove a debate RAN.
   `mad_runner.py` has four exits that return True - no fresh report, a handshake skip, a quota block -
   and each one reads `run-mad success`. A debate is CONFIRMED by `ARB-FIT` in its log. S109 read 60
   runs: 40 of 40 `run-mad success` jobs carried it, so the job count had held - the confirmation is
   what makes it a measurement (DECISION S109-3).
"""
PROTO_LOG_ANCHOR = "## VERSION LOG\n\n"
PROTO_LOG_NEW = PROTO_LOG_ANCHOR + """- **v21 - S109 (2026-10-04).** PART D step 4 only. Job level separates a debate from a watch but
  cannot prove that a debate ran: four clean exits of `mad_runner.py` also read `run-mad success`. A
  debate is now confirmed by `ARB-FIT`; measured 40 of 40 over 60 runs, so no past count was wrong
  (DECISION S109-3). PART A, B and C unchanged.
"""

ARCH_ANCHOR = ("the \"autonomous workflows\" the pages meant (R-S108-2). No live claim is bound to it.\n"
               "- **AGENT TEST**: not yet run.\n")
ARCH_BLOCK = ARCH_ANCHOR + """
### STATUS AT THE S109 CLOSE - R3-4 DONE: ITS PREDICTION HELD AT BOTH JUDGING CLOSES

- Generation 29 holds **65** items against a cap of 70: 9.23 (the mission), 9.20 and 9.16 closed; none
  opened. DECISION S107-8's hypothesis - the count falls below 70 over S108-S109 - HELD at both closes
  (68, then 65). Five departures and zero arrivals: `python tools/gni_lambda.py --window S108:S109`
  reports no arrival. R3-4's row is DONE.
- The claims document reads 748 claims at 801 locations, COVERAGE 21/748, **0 DEFEATED**. CLM-691
  retired with its copy; CLM-755 to CLM-758 minted for the copy that replaced it on `/alerts` and
  `/comparison`, UNMEASURED and UNREVIEWED.
- **ACHIEVED is NOT declared.** Four rows DONE and the replay recorded at S107; Test 2, the agent test,
  has never run. It is S110's mission (DECISION S109-9).
- **AGENT TEST**: not yet run.
"""

GLOSS_OLD = "# GNI GLOSSARY - S108"
GLOSS_NEW = "# GNI GLOSSARY - S109"
# Rows the S109 documents need (the check labelled `glossary` named exactly this one on the assembled set;
# it also named UNAVAILABLE, which only a container without `gh` writes into section seven).
GLOSS_ROWS = [
    ("| SQL | the query language of the Supabase database |",
     "| ASCII | the 7-bit character set; every patch anchor is kept inside it |\n", "glossary ASCII"),
]


def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s109.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    if not os.path.exists(os.path.join(out, "HANDOFF_S109.md")):
        die("HANDOFF_S109.md must already be in OUTDIR (written from the Part B template)")
    res = {}
    claims = claim_texts(root)

    o = rd(root, "GNI_TARGET_AND_ORDER_S108.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S108 order does not hash to its published value")
    o = sub1(o, "**GENERATION 28 - 2026-10-03 (S108 close). SUPERSEDES generation 27\n(`GNI_TARGET_AND_ORDER_S107.md`).**",
             "**GENERATION 29 - 2026-10-04 (S109 close). SUPERSEDES generation 28\n(`GNI_TARGET_AND_ORDER_S108.md`).**", "header")
    o = span(o, "## NEXT SESSION'S MISSION (S109)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = span(o, "**ROADMAP 3 - CLAIMS - ROWS 1 TO 3 DONE, ROW 4 BOUND; ITS PREDICTION HELD AT THE FIRST JUDGING",
             "**DEFINITION OF DONE - RESTATED AT S105", TARGET_R3, "target roadmap")
    o = sub1(o, D2_OLD, D2_NEW, "dod d2")
    o = sub1(o, D4_OLD, D4_NEW, "dod d4")
    o = sub1(o, D4B_OLD, D4B_NEW, "dod d4 count")
    o = sub1(o, "**EXPECTED ITEM COUNT: 68 distinct numbered items", "**EXPECTED ITEM COUNT: 65 distinct numbered items",
             "expected count")
    o = sub1(o, HEAD_OLD, HEAD_NEW, "order head")
    if o.count("docs/GNI_TARGET_AND_ORDER_S108.md \\\n") != 2:
        die("the two published scan commands are not both present")
    o = o.replace("docs/GNI_TARGET_AND_ORDER_S108.md \\\n", "docs/GNI_TARGET_AND_ORDER_S109.md \\\n")
    o = sub1(o, "Both must print **68**.", "Both must print **65**.", "both print")
    o = sub1(o, "`tools/mk_close_s108.py`, which refuses to write when they disagree",
             "`tools/mk_close_s109.py`, which refuses to write when they disagree", "head tool")
    o, ntags = strip_tags(o)
    if ntags != 68:
        die("expected 68 binding tags in generation 28, stripped %d" % ntags)
    o = span(o, "**ORPHAN RATE: 49/68**", "### ROOT 9 - PUBLIC COPY", "@@ORPHAN@@\n", "orphan block")
    o = span(o, "- **9.23** NEW (S106)", "- **9.19** OPEN (S96)", "", "9.23 out")
    o = span(o, "- **9.20** OPEN (S98)", "- **9.5** OPEN - COR.", "", "9.20 and 9.16 out")
    o = sub1(o, "- **9.5** OPEN - COR. Eight unresolved S69 census flags; F14 renders BEARISH over a stale basis.\n",
             ITEM_95, "9.5 rewritten")
    o = sub1(o, NOTE_919_ANCHOR, NOTE_919, "9.19 note")
    o = sub1(o, NOTE_610_ANCHOR, NOTE_610, "6.10 note")
    o = sub1(o, NOTE_616_ANCHOR, NOTE_616, "6.16 note")
    o = sub1(o, NOTE_531_ANCHOR, NOTE_531, "5.31 note")
    o = sub1(o, ARCHIVED_HEAD_OLD, ARCHIVED_HEAD_NEW, "archived head")
    o = sub1(o, "| what | why archived |\n|---|---|\n", "| what | why archived |\n|---|---|\n" + ARCHIVED_ROWS, "archived")
    o = span(o, "## CHANGED THIS REGENERATION", "## HOW THIS FILE IS MAINTAINED", CHANGED, "changed")
    o = sub1(o, MAINTAINED_OLD, MAINTAINED_NEW, "maintained")
    o, orphans, total = bind(o, claims)
    o = sub1(o, "@@ORPHAN@@\n", ORPHAN_NEW.format(orph=orphans, total=total), "orphan rate")
    q = order_range(o)
    for gone in CLOSED:
        if re.search(r"(?<![0-9.])" + re.escape(gone) + r"(?![0-9])", q):
            die("closed id %s is still cited inside the queue" % gone)
    bold, anyd, r5 = scans(o)
    print("order scans: bold=%d any=%d root5=%d orphan=%d/%d (want %d/%d/<=%d, orphan %d)"
          % (len(bold), len(anyd), r5, orphans, total, COUNT, COUNT, ROOT5_CAP, ORPHANS))
    if anyd - bold:
        die("the any-digits scan sees non-item numbers in the queue: %s" % sorted(anyd - bold))
    if not (len(bold) == len(anyd) == total == COUNT <= CAP and r5 <= ROOT5_CAP and orphans == ORPHANS):
        die("order counts disagree, exceed the cap, or the orphan rate is not the declared one")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD changed during assembly")
    res["GNI_TARGET_AND_ORDER_S109.md"] = o

    rl = rd(root, "GNI_RULES_S108.md")
    if "R-S109-" in rl:
        die("the S108 register already holds an R-S109 id")
    res["GNI_RULES_S109.md"] = rl.rstrip("\n") + "\n" + RULES_BLOCK

    p = rd(root, "GNI_Session_Transfer_Protocol_S108.md")
    p = sub1(p, PROTO_TITLE_OLD, PROTO_TITLE_NEW, "protocol title")
    p = sub1(p, PROTO_STEP4_ANCHOR, PROTO_STEP4_NEW, "protocol step 4")
    p = sub1(p, PROTO_LOG_ANCHOR, PROTO_LOG_NEW, "protocol log")
    res["GNI_Session_Transfer_Protocol_S109.md"] = p
    res["CONTRACT_S109.md"] = rd(root, "CONTRACT_S108.md")
    g = sub1(rd(root, "GNI_GLOSSARY_S108.md"), GLOSS_OLD, GLOSS_NEW, "glossary title")
    for anchor, row, what in GLOSS_ROWS:
        g = sub1(g, anchor, row + anchor, what)
    res["GNI_GLOSSARY_S109.md"] = g
    ar = rd(root, "GNI_ARCHITECTURE_S109.md")
    res["GNI_ARCHITECTURE_S109.md"] = sub1(ar, ARCH_ANCHOR, ARCH_BLOCK, "architecture status")

    for name, text in sorted(res.items()):
        data = text.encode("utf-8")
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(data)
        print("%-40s %7d bytes  md5 %s (EOL-normalised)" % (name, len(data), hashlib.md5(data).hexdigest()))
    print("WROTE %d files beside HANDOFF_S109.md. The macro map is generated LAST." % len(res))


if __name__ == "__main__":
    main()
