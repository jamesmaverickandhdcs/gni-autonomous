#!/usr/bin/env python3
"""S105 close assembler - the executable record of how every byte of the S105 close set moved.

Byte-copies the S104 set (DECISION S92-5), applies anchored patches (each anchor must occur exactly
once), writes the S105 files into OUTDIR, and REFUSES to write anything when the order's two
counting scans disagree with each other, with the declared count or with the cap, or when the
GRAVEYARD no longer hashes to its published value (R-S95-1). The macro map is NOT written here: it
is generated LAST, from the committed bytes, by tools/gni_macro_map.py --session 105.
usage: python tools/mk_close_s105.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5_CAP = 70, 70, 42
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"

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
    """Replace from `start` (inclusive) up to `end` (exclusive); each must occur once."""
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
    return len(bold), len(anyd), len(root5)

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

# ------------------------------------------------------------------ ORDER, generation 25
MISSION = """## NEXT SESSION'S MISSION (S106)

**ROADMAP 3, ROW R3-1 - GLOSSARY + ORIGIN, BUILT TO THE ROW'S OWN DONE COMMANDS.** The row, its
commands and the roadmap's completion test are in `GNI_ARCHITECTURE_S105.md`, section ROADMAP 3.

WHY THIS AND NOT THE TOP OF THE QUEUE. Roadmap 3 was DECLARED at S105 (DECISION S105-1, delegated)
and DECISION S105-2 placed R3-1 at S106, after the identity separation that was its precondition:
the specification's glossary listed a rule namespace that has since been renumbered. DECISION
S105-6 gives R3-1 ONE session. R3-2 - the claims harvest, which reads the public pages and the white
paper and is the first row that touches the PRODUCT - follows at S107. A roadmap of institutional
rows only would repeat what S105 measured across S96-S104: fifty items opened against sixteen
closed, forty-two of the fifty in ROOT 5.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. The detector holds EIGHT checks; `C7` also
requires `src/lib/freshness.ts` to mirror the SLO-CFG lines since S105. The fixture holds
TWENTY-SEVEN families. Name a check by its LABEL, never by a number not yet registered (R-S105-1).
A public-page claim is verified on the LIVE build only after the deployment reports `success`, and
against the bytes of the read taken before the change (R-S105-2), counting visible markup only
(R-S105-3). A local pre-commit guard blocks any commit that would reintroduce the identity terms;
its deny list lives off-repo by design, so a blocked commit is reported by the hook, never here.

"""

TARGET_ROADMAPS = """**ROADMAP 2 IS FOUR OF FOUR - ACHIEVED AT S104 AND ARCHIVED** (evidence in `GNI_ARCHITECTURE`).

**ROADMAP 3 - CLAIMS - IS DECLARED (S105, DECISION S105-1, delegated by James: "your call").** Every
promise GNI makes about itself gets a source, a status the machine derives, and a check that goes
red when the promise breaks. Its four rows and its completion test, each with the command that
answers it, are in `GNI_ARCHITECTURE_S105.md`. Its OWED list names three debts payable before the
row that needs them; the first - the lambda baseline has no recorded command - blocks row four's
falsifiable prediction until it is paid.

"""

DOD = """**DEFINITION OF DONE - RESTATED AT S105 (DECISION S105-9), each line with the command that answers it.**
S105 measured that two of the four lines could never be met: both sat on roots archived or blocked
while the lines stayed in the definition, so the target could not be declared achieved by
construction (R-S105-6). Each line is now stated in a form the work can reach and mapped to the
guideline it implements - ICD 203's analytic standards, EU AI Act Art. 50(4), and section ten's SLO.

| # | line | status at this regeneration |
|---|---|---|
| D1 | the arbitrator reads what it claims to read | DONE - certified S96, archived; no re-run owed |
| D2 | no public page shows the capped escalation score without its uncapped magnitude (ICD 203: express uncertainty, describe method) | OPEN - 15 of the 16 pages that render the score omit it; only `/autonomy` carries it |
| D3 | the grounding gate measures reading, not existence | BLOCKED on item 7.1 - a line with no command is named as such, not hidden |
| D4 | every public statement of cadence, count or provenance is derived from a measurement or labelled as a request, and AI-generated text is labelled at first exposure | PARTLY - the freshness item closed and the disclosure shipped at S105; item 9.22 open |

```bash
# D2 - DONE when this prints nothing (S105: prints 15; positive control: src/app/autonomy/page.tsx)
for f in $(git grep -l escalation_score -- 'src/app/**/*.tsx'); do grep -q -E 'escalation_score_raw|Raw Magnitude' "$f" || echo "$f"; done
# D4 - the bound half: prints 1
python tools/gni_rule_checks.py | grep -c '^.PASS. C7 '
```
"""

ORDER_HEAD = """**EXPECTED ITEM COUNT: 70 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**
**CAP: 70 (DECISION S105-5; CONTRACT v11, WIP CAP).** The count may not grow across a regeneration,
and ROOT 5 may not exceed 42, unless James rules an exception in writing. Generation 24 held 70.
This close CLOSED one item, MERGED one into its twin and opened two, so the cap held with no
exception. Closed and merged ids are not repeated here: a closed id cited in the queue counts as a
queue item. Every id is bolded so the published command is true of the file it sits in, and a
second differently-shaped scan is printed beside it to reconcile against (R-S98-6):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S105.md \\
  | grep -oE '\\*\\*[0-9]+\\.[0-9]+' | sort -u | wc -l
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S105.md \\
  | grep -oE '[0-9]+\\.[0-9]+' | sort -u | wc -l
```

Both must print **70**. BOTH WERE RUN ON THE ASSEMBLED BYTES BEFORE THIS FILE WAS WRITTEN, by
`tools/mk_close_s105.py`, which refuses to write when they disagree with each other, with the number
above, or with the cap (R-S95-1). Item **5.51** - a control probe for the order generator - is
unchanged: this close's assembler is a different stand-in, not the probe.
"""

ITEM_922 = """- **9.22** NEW (S105) [MEASURED] - COR - **THE PUBLIC SURFACE STILL CARRIES CLAIMS NO MEASUREMENT
  SUPPORTS, AND ONE PAGE PUBLISHES QUERY LIMITS AS COUNTS.** One item, deliberately, under the cap.
  (a) Kin of the closed freshness item: "twice daily" on four pages, "24/7" on two, "Real-time" in
  two page bodies, "The system fixes itself", and `/developer`'s "may fire 2-3 hours late" - the
  last must be read against section six's slot lateness before it is rewritten, or one unmeasured
  sentence replaces another. (b) `/adaptive-log`: "Adaptive Runs" and "Reports Generated" render the
  LENGTH of a limited query, the "by Adaptive" list is the newest reports of every pipeline with no
  filter, and the run log is a token log that stops in June while `gni_adaptive.yml` runs about four
  times a day, every run `success` (gh, S105). (c) DoD line D2: 15 of the 16 pages that render the
  escalation score show the capped value without the uncapped magnitude certified at S90; only
  `/autonomy` carries it. Fix shape: the S105 pattern - one shared constant or a filtered query, a
  check wherever a number can drift, and a live read on the NEW build.
"""

ITEM_616 = """- **6.16** NEW (S105) [MEASURED] - ADA - `package.json` and `package-lock.json` DISAGREE on the major
  version of `@types/node`, so `npm ci` refuses with `EUSAGE` in a clean checkout (S105 container).
  `npm install` and `tsc --noEmit` pass, and Vercel built every S105 push, so nothing deployed is
  broken; the reproducible install path is.

"""

ARCHIVED_ROWS = """| **9.21** the freshness promise on public pages | CLOSED S105 at `867ea5b`. Read LIVE on the new build after the deployment reported `success`: every predicted cell matched, twenty of twenty. The bound reaches the pages through ONE constant that `C7` compares with SLO-CFG, so a moved bound reddens the detector until the pages follow. The one statement the read could not see sits in an empty-state branch and is fixed in source. |
| **9.17** the S94 twin of the `setup-python` record item | MERGED S105 into its S93 original (DECISION S105-8): its own text said "same shape, one generation later". |
"""

CHANGED = """## CHANGED THIS REGENERATION

- **DECISION S105-1 (delegated).** ROADMAP 3 DECLARED from `GNI_ROADMAP3_SPEC_S104.md`, amended in
  the declaration itself: checks are named by function and found by label, because the spec had
  reserved an id that S104 had already taken; every row carries a command; the AGENT TEST verdict is
  recorded as a dated line; three debts are listed as OWED. Text in `GNI_ARCHITECTURE_S105.md`.
- **DECISION S105-2 (delegated).** S105's build work was the identity separation the owner ruled
  elsewhere; R3-1 moves to S106 because its glossary would otherwise have re-published a renumbered
  namespace. The brief and its key are held off-repo, by design.
- **DECISION S105-3 (delegated).** The lessons-learned ids were renumbered into a GNI-own namespace,
  `GNI-L-###`, with FRESH numbers that derive nothing from the old ones; the detector, the macro map
  generator and the fixture follow it. Four ids that only named another project's rules were
  dropped from the text rather than renumbered.
- **DECISION S105-4 (delegated).** Historical `.docx` records were edited in place, paragraph by
  paragraph, rather than deleted: deleting them now and rewriting history later would erase them.
- **DECISION S105-5 (delegated).** WIP CAP: the order may not grow across a regeneration and ROOT 5
  may not pass 42, without James's written exception. Measured grounds: S96-S104 opened fifty items
  and closed sixteen, forty-two of the fifty in ROOT 5 (Little's law has no steady state there).
- **DECISION S105-6 (delegated).** R3-1 gets ONE session; R3-2, the first product-facing row, is S107.
- **DECISION S105-7 (delegated, same-session fix bar clause c).** Two product fixes shipped
  mid-session and were verified LIVE: the freshness item at `867ea5b` and a visible AI-generation
  disclosure at `5fc6936` (one visible occurrence per page; the second count is the RSC payload).
- **DECISION S105-8 (Claude).** The S94 `setup-python` item merged into its S93 original, to hold
  the cap; its own text called it the same shape.
- **DECISION S105-9 (delegated).** The DEFINITION OF DONE restated, line by line, with commands.
- CLOSED 9.21 · MERGED 9.17 · OPENED 9.22 and 6.16 · count 70, cap held.
- **IDENTITY SEPARATION, the tree half, DONE**: `e205631` + `54615c7` (patch, then regenerated
  sections), cosmetic follow-up `04aebc8` + `df45b4c`; CI green at job level on each push; a fresh
  public clone scans clean under the published scan and under a stricter private one. History is
  untouched until one agreed boundary for both repositories. A fail-closed local pre-commit guard
  now runs the private scanner; it blocked its own probe on James's machine.
- **L2 MAD RE-MEASURED** (the S103 reading is retired): 45 debates and 22 watches across the 23 days
  since S104, every job `success`, no scheduled day missed.
- **THE CYCLE, MEASURED** (James asked at S105 whether the find-fix-find loop had stopped). It
  slowed and it MOVED: items opened per close fell from fifteen to three across S96-S104, two
  roadmaps finished, and defects are now caught by machines - but nearly all new work landed in
  ROOT 5, and two DoD lines sat on archived or blocked roots. S105 corrected one of its own claims
  inside that analysis: the escalation root was not abandoned at S96 - the S90 magnitude stopgap
  exists - but it reached one page of sixteen.
- GUIDELINES ADOPTED, found by search this session rather than quoted from memory: ICD 203 (sourcing,
  uncertainty, information versus judgment) as R3-2's claim rubric; EU AI Act Art. 50(4) as a check
  for AI-generated public-interest text (applicability is James's to rule; Claude is not a lawyer);
  Little's law for the cap; SRE's engineering-versus-overhead split for reading ROOT 5.
- NOT DONE, DECLARED: the history rewrite (both repositories, one boundary); section six not
  re-harvested (item **5.60**); the lambda baseline command (OWED, roadmap 3).
- CONTRACT RAISED TO **v11** (operator line de-identified; WIP CAP). PROTOCOL RAISED TO **v19**
  (the repo is public - the open may clone and verify; the WRONG ledger publishes its count).

"""

MAINTAINED = """## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped - this generation's copy was hashed with the
published command's boundary BEFORE the file was written. The item count carries two commands
beside it, and both - plus the CAP - are checked on the ASSEMBLED bytes before the write by
`tools/mk_close_s105.py`, which refuses on any disagreement. Item **5.51** still asks for a control
probe; this assembler is not one.
Freshness confers no priority: an item found today does not outrank an item found in June unless
a measurement says so. Under the cap it also cannot enter without something leaving.
"""

# ------------------------------------------------------------------ RULES appended
RULES_S105 = """
- R-S105-1 - A PLAN MUST NOT RESERVE AN ID IT DOES NOT OWN YET. The roadmap 3 specification, written
  at S102 when the detector held six checks, named its glossary check `C8`. S104 shipped a different
  `C8` before the row began, and a declaration copied verbatim would have minted a duplicate inside
  the instrument whose third check exists to refuse duplicates. Ids are allocated at birth by the
  registry that owns them; a plan names the FUNCTION and the completion command finds the check by
  its registered label. It is the hard-coded detector count of Protocol v16 and v18 again, written
  into a plan instead of a template.
  **CHECKABLE: yes** - assert every `C<n>` a live roadmap or specification names resolves to a
  registered check whose label matches the function the text gives it.

- R-S105-2 - A LIVE READ PROVES NOTHING UNTIL IT PROVES IT READ THE NEW BUILD. S105 read the public
  pages twice before the deployment carrying the change existed: once while the hosting status was
  `pending`, and once from a wait-loop that stopped on "not pending" and so accepted an EMPTY status
  for a commit that had not been pushed. Both reads returned byte counts identical to the read taken
  before the change - which is the evidence that should have stopped them. A verification of a
  deployed change waits for `success` and nothing else, stops loudly on `failure`, `error` or
  timeout, and compares bytes against the pre-change read before trusting a single row.
  It is kin of R-S104-2: the loop tested "is it still pending", which is adjacent to "is it built".
  **CHECKABLE: no** - it constrains how a verification is run, not what a file contains.

- R-S105-3 - A PHRASE COUNTED IN A RENDERED PAGE COUNTS ITS RENDERING PATH, NOT ITS VISIBILITY. One
  disclosure line placed in a SERVER component appeared twice in the HTML - once in markup and once
  in the hydration payload inside a script tag - and a predicted count of one read as two. A line
  in a CLIENT component appeared once; another appeared ZERO times because it lives in an
  empty-state branch that the data never takes. Before predicting a count, read the component's
  boundary and the condition around the line; when counting, count visible markup outside scripts.
  **CHECKABLE: no** - it constrains reading a rendered artefact.

- R-S105-4 - SELECT A RUN BY WHAT PRODUCED IT, NOT BY WHAT IT RAN ON. A verification took the first
  run listed for a commit and read a scheduled price fetch instead of the CI run: after a push,
  every cron runs on the new tip, so "the newest run on this commit" is a race. Filter by the
  workflow that the claim is about. R-S92-2's family: selecting by position into a collection that
  other writers append to.
  **CHECKABLE: yes** - assert every published CI-verification command filters by workflow.

- R-S105-5 - A TABLE CAPPED BY ITS FORMAT CANNOT CARRY A RATE. The handoff's WRONG ledger read six
  rows in fourteen of fifteen handoffs from S90 to S104, because the template capped it at six; the
  S104 diary says the session was wrong eight times. A saturated instrument cannot show improvement
  or decline, which is the escalation score's disease in the project's own self-measurement. The
  ledger publishes its COUNT first, then the rows that matter most.
  **CHECKABLE: yes** - assert the live handoff's WRONG section carries a count line.

- R-S105-6 - A ROOT ARCHIVED WHILE ITS LINE STAYS IN THE DEFINITION OF DONE MAKES THE TARGET
  UNREACHABLE. From S96 to S104 two of the four DoD lines rested on roots that were archived or
  blocked, and every regeneration printed "Unchanged" beside them. The target could not be declared
  achieved, by construction, and nothing said so because nothing got worse. Archiving a root is a
  ruling about WORK; it must be paired with a ruling about the LINE - restate it in a reachable form
  with a command, or remove it and say why.
  **CHECKABLE: yes** - assert every DoD line names an open root, a command, or a written exemption.

- R-S105-7 - A QUEUE WITHOUT A CAP ADMITS WORK FASTER THAN IT RETIRES IT. S96-S104 opened fifty items
  and closed sixteen; finding was free and leaving was not, so the order could only grow. Little's
  law holds only where arrivals equal departures. The CONTRACT carries the cap since v11; this rule
  carries the reason, so the cap is not read as tidiness and waived on the first busy close.
  **CHECKABLE: yes** - assert the order generator refuses a count above the published cap.
"""

# ------------------------------------------------------------------ CONTRACT
WIP_LAW = ("- WIP CAP (v11, S105): the WORKING ORDER's item count may not grow across a regeneration, "
           "and ROOT 5 may not grow past the size it had when the cap was set, unless James rules an "
           "exception in writing. A new item enters only when one leaves - closed, merged or retired. "
           "Little's law: a queue whose arrivals exceed its departures has no steady state (R-S105-7).\n")
CONTRACT_LOG = """- v11 - S105 (2026-10-02): two changes. (1) The operator line in ROLES was de-identified at the
  owner's ruling; the ruling and its brief are held off-repo by design, so this entry records that it
  happened and nothing of its content. (2) WIP CAP added, delegated by James (DECISION S105-5). Every
  other line is byte-identical to `CONTRACT_S104.md` as it stands at `5fc6936`.
"""

# ------------------------------------------------------------------ PROTOCOL
STEP0_OLD = "0. The S{N} close set is ATTACHED (container is empty; repo is private — never try to clone)."
STEP0_NEW = ("0. The S{N} close set is ATTACHED. The repo is PUBLIC (since S104): the container MAY clone it\n"
             "   read-only at depth one and verify the attachments byte-for-byte against the tree, as S105 did.\n"
             "   It never pushes; James runs every commit and push.")
WRONG_OLD = "## 5. WRONG THIS SESSION (<=6 lines) - claims that turned out false"
WRONG_NEW = "## 5. WRONG THIS SESSION - COUNT: N (every one, counted), then the <=6 rows that matter most"
PROTO_LOG = """- **v19 - S105 (2026-10-02).** PART D step 0 and the handoff's section five only. Step 0 said the
  repo was private and forbade a clone; it has been public since S104, and S105 cloned it and found
  all eight attachments byte-identical to the tree - a check no earlier open could make. The WRONG
  ledger's header capped it at six rows and fourteen of fifteen handoffs printed exactly six, so
  the ledger could not show a rate (R-S105-5); it now prints its COUNT first.
"""

def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s105.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    res = {}

    o = rd(root, "GNI_TARGET_AND_ORDER_S104.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S104 order does not hash to its published value")
    o = sub1(o, "**GENERATION 24 - 2026-09-10 (S104 close). SUPERSEDES generation 23\n(`GNI_TARGET_AND_ORDER_S103.md`).**",
             "**GENERATION 25 - 2026-10-02 (S105 close). SUPERSEDES generation 24\n(`GNI_TARGET_AND_ORDER_S104.md`).**", "order header")
    o = span(o, "## NEXT SESSION'S MISSION (S105)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = span(o, "**ROADMAP 2 IS FOUR OF FOUR - DECLARED ACHIEVED AT THE S104 CLOSE, AND ARCHIVED.**",
             "**DEFINITION OF DONE - status at this regeneration:**", TARGET_ROADMAPS, "target roadmaps")
    o = span(o, "**DEFINITION OF DONE - status at this regeneration:**", "## 🪦 GRAVEYARD", DOD + "\n", "dod")
    o = span(o, "**EXPECTED ITEM COUNT: 70 distinct numbered items", "### ROOT 9 - PUBLIC COPY", ORDER_HEAD + "\n", "order head")
    o = span(o, "- **9.21** OPEN (S101)", "- **9.19** OPEN (S96)", ITEM_922, "9.21 -> 9.22")
    o = sub1(o, "- **9.16** OPEN (S93) - COR. Records are from the `setup-python` side only.\n"
                "- **9.17** OPEN (S94) - COR. Same shape as **9.16**, one generation later.\n",
             "- **9.16** OPEN (S93) - COR. Records are from the `setup-python` side only. MERGED S105: the\n"
             "  S94 item of the same shape, one generation later, is folded in here (DECISION S105-8).\n", "merge")
    o = sub1(o, "\n### ROOT 5 - INSTITUTIONAL HARDENING", "\n" + ITEM_616 + "### ROOT 5 - INSTITUTIONAL HARDENING", "6.16")
    o = sub1(o, "## ARCHIVED - TWO ITEMS AND ONE ROADMAP CLOSE INTO IT THIS GENERATION",
             "## ARCHIVED - ONE ITEM CLOSES AND ONE MERGES INTO IT THIS GENERATION", "archived heading")
    o = sub1(o, "| what | why archived |\n|---|---|\n", "| what | why archived |\n|---|---|\n" + ARCHIVED_ROWS, "archived rows")
    o = span(o, "## CHANGED THIS REGENERATION", "## HOW THIS FILE IS MAINTAINED", CHANGED, "changed")
    i = o.index("## HOW THIS FILE IS MAINTAINED")
    o = o[:i] + MAINTAINED
    b, a, r5 = scans(o)
    print("order scans: bold=%d any=%d root5=%d (want %d/%d/<=%d)" % (b, a, r5, COUNT, COUNT, ROOT5_CAP))
    if not (b == a == COUNT <= CAP and r5 <= ROOT5_CAP):
        die("order counts disagree or exceed the cap")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD changed during assembly")
    res["GNI_TARGET_AND_ORDER_S105.md"] = o

    a_ = rd(root, "GNI_ARCHITECTURE_S104.md")
    a_ = sub1(a_, "the gap count before looking at the schedule.\n",
              "the gap count before looking at the schedule.\n\n**S105: THE PAGES CARRY THIS BOUND THROUGH ONE "
              "CONSTANT.** `src/lib/freshness.ts` mirrors\nBOUND_HOURS, EXCEEDANCE_MAX and the window; `C7` compares "
              "them with the SLO-CFG lines and goes red\nwhen they differ, so a moved bound cannot leave a page "
              "stating the old one (fixture families 26\nand 27). Read live on the new build at S105, every "
              "predicted cell matched.\n", "arch 10.x")
    decl = open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "ROADMAP3_DECLARATION_DRAFT_S105.md"),
                "rb").read().decode("utf-8") if os.path.exists(os.path.join(os.path.dirname(os.path.abspath(__file__)),
                "ROADMAP3_DECLARATION_DRAFT_S105.md")) else None
    if decl is None:
        die("ROADMAP3_DECLARATION_DRAFT_S105.md must sit beside this script when it runs")
    decl = sub1(decl, "# ROADMAP 3 - DECLARATION (DRAFT, S105, 2026-10-02)",
                "## ROADMAP 3 - CLAIMS (S106-), declared at S105 (DELEGATED)", "decl heading")
    decl = sub1(decl, "This draft is folded into the ROADMAP section of the S105 architecture\nat the close and then retired; "
                "`GNI_ROADMAP3_SPEC_S104.md` becomes history (its own section 7).",
                "The specification\n`GNI_ROADMAP3_SPEC_S104.md` is history from this close (its own section 7).", "decl status")
    decl = sub1(decl, "(the spec says 28; section 5 says **38** at `54615c7`, so the bucket count is read, never copied)",
                "(the spec says 28; section 5 said 38 at `54615c7` and 41 at `5fc6936` - it moves with every committed "
                "script, so the bucket count is read, never copied)", "decl r3-3")
    decl = decl.replace("\n## ", "\n### ")
    a_ = a_.rstrip("\n") + "\n\n" + decl.rstrip("\n") + "\n"
    res["GNI_ARCHITECTURE_S105.md"] = a_

    rl = rd(root, "GNI_RULES_S104.md")
    rl = rl.rstrip("\n") + "\n" + RULES_S105
    res["GNI_RULES_S105.md"] = rl

    c = rd(root, "CONTRACT_S104.md")
    m = re.search(r"^- SAME-SESSION FIX BAR:.*\n", c, re.M)
    if not m:
        die("contract anchor missing")
    c = c[:m.end()] + WIP_LAW + c[m.end():]
    c = c.rstrip("\n") + "\n" + CONTRACT_LOG
    res["CONTRACT_S105.md"] = c

    p = rd(root, "GNI_Session_Transfer_Protocol_S104.md")
    p = sub1(p, "# GNI SESSION TRANSFER PROTOCOL v18", "# GNI SESSION TRANSFER PROTOCOL v19", "proto header")
    p = sub1(p, STEP0_OLD, STEP0_NEW, "proto step 0")
    p = sub1(p, WRONG_OLD, WRONG_NEW, "proto wrong")
    p = sub1(p, "- **v18 - S104 (2026-09-10).**", PROTO_LOG + "- **v18 - S104 (2026-09-10).**", "proto log")
    res["GNI_Session_Transfer_Protocol_S105.md"] = p

    h = os.path.join(os.path.dirname(os.path.abspath(__file__)), "HANDOFF_S105.md")
    if not os.path.exists(h):
        die("HANDOFF_S105.md must sit beside this script when it runs")
    res["HANDOFF_S105.md"] = open(h, "rb").read().decode("utf-8").replace("\r\n", "\n")

    for name, text in sorted(res.items()):
        data = text.encode("utf-8")
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(data)
        print("%-40s %7d bytes  md5 %s (EOL-normalised)" % (name, len(data), hashlib.md5(data).hexdigest()))
    print("WROTE %d files. The macro map is generated LAST, from committed bytes." % len(res))

if __name__ == "__main__":
    main()
