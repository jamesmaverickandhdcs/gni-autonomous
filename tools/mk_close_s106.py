#!/usr/bin/env python3
"""S106 close assembler - the executable record of how every byte of the S106 close set moved.

Byte-copies the S105 set (DECISION S92-5), applies anchored patches (each anchor must occur exactly
once), writes the S106 files into OUTDIR, and REFUSES to write anything when the order's two counting
scans disagree with each other, with the declared count or with the cap, or when the GRAVEYARD no
longer hashes to its published value (R-S95-1). The architecture and glossary are S106 files already
in the tree (R3-1 and D2 shipped them); this script patches them in place in OUTDIR. The macro map is
NOT written here: it is generated LAST, from the committed bytes, by tools/gni_macro_map.py.
usage: python tools/mk_close_s106.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5_CAP = 70, 70, 42
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"
HERE = os.path.dirname(os.path.abspath(__file__))


def die(msg):
    print("REFUSED: " + msg); sys.exit(1)


def rd(root, name):
    with open(os.path.join(root, "docs", name), "rb") as fh:
        return fh.read().decode("utf-8").replace("\r\n", "\n")


def side(name):
    p = os.path.join(HERE, name)
    if not os.path.exists(p):
        die(name + " must sit beside this script when it runs")
    return open(p, "rb").read().decode("utf-8").replace("\r\n", "\n")


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


MISSION = """## NEXT SESSION'S MISSION (S107)

**ROADMAP 3, ROW R3-2 - THE CLAIMS HARVEST, BUILT TO THE ROW'S OWN DONE COMMANDS.** The row, its
commands and the roadmap's completion test are in `GNI_ARCHITECTURE_S106.md`, section ROADMAP 3.

WHY THIS. DECISION S105-6 placed R3-2 at S107, after R3-1, which closed at S106. It is the first row
that touches the PRODUCT: `tools/gni_claims.py` harvests every claim the public pages and the white
paper make, verbatim with `file:line`, one `CLM-###` id each (the id family enters the glossary's
NAMESPACES the day it is minted), and a check labelled `claims resolve` proves each quoted text is
still where the file says it is.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. The detector holds ELEVEN checks and the
fixture FORTY families; name a check by its LABEL (R-S105-1). The check labelled `glossary` scans
every live document and ORIGIN, so a new all-capitals token in any close document must be defined in
the glossary before the close commit, or the detector goes red on paperwork. Two files are the only
homes of public numbers: `src/lib/escalation.ts` (every escalation score, with its raw magnitude;
check `escalation magnitude`) and `src/lib/freshness.ts` (the bound and the dated runtime figures).
A live read waits for deployment `success` and proves the NEW build with a rendered literal grepped
in the minified bundle (R-S105-2, further instance). A limited query's length is never a count
(R-S106-3).

SEEDS FOR THE HARVEST, measured at S106 and deliberately NOT fixed under the cap:
`/autonomy` shows "Run Interval 30 min" and "AI decides run frequency autonomously" while the
pipeline runs on its cron twice a day and adaptive runs about seven times a day; `/autonomy` says the
final score "has been at the cap on every measured run" - true of the 67 runs that carry a raw value,
false of the 263 that carry a score; `/developer` documents `/api/adaptive-log` as a "self-healing
log"; `src/components/ResetBanner.tsx` says "Always on" and is imported by nothing (R3-3's dead
symbols, not R3-2's). The white paper is still unlocated (OWED).

"""

TARGET_ROADMAPS = """**ROADMAP 2 IS FOUR OF FOUR - ACHIEVED AT S104 AND ARCHIVED** (evidence in `GNI_ARCHITECTURE`).

**ROADMAP 3 - CLAIMS - ROW 1 OF 4 DONE AT S106.** Declared at S105 (DECISION S105-1, delegated).
R3-1 shipped at `f86febb` (CI `37069679116` green at job level): `docs/GNI_ORIGIN.md`, the
glossary, and the checks labelled `glossary` and `origin citations`; its fourth DONE line is met by
this close's handoff. The row's own text said a citation may resolve "to a session record or a
commit"; DECISION S106-2 narrowed that to sessions, because ORIGIN is never regenerated and the
declared history rewrite changes every hash. Rows, completion test and OWED list in
`GNI_ARCHITECTURE_S106.md`.

"""

DOD_D2_OLD = "| D2 | no public page shows the capped escalation score without its uncapped magnitude (ICD 203: express uncertainty, describe method) | OPEN - 15 of the 16 pages that render the score omit it; only `/autonomy` carries it |"
DOD_D2_NEW = "| D2 | no public page shows the capped escalation score without its uncapped magnitude (ICD 203: express uncertainty, describe method) | MET AT S106 - every page formats the score through `src/lib/escalation.ts`, which prints the raw value beside it; the check labelled `escalation magnitude` refuses a page that formats it itself; read LIVE. Residual, itemised: three tables carry no raw column, so their rows point to the report instead (item 9.23) |"
DOD_D4_OLD = "| D4 | every public statement of cadence, count or provenance is derived from a measurement or labelled as a request, and AI-generated text is labelled at first exposure | PARTLY - the freshness item closed and the disclosure shipped at S105; item 9.22 open |"
DOD_D4_NEW = "| D4 | every public statement of cadence, count or provenance is derived from a measurement or labelled as a request, and AI-generated text is labelled at first exposure | MET FOR THE KNOWN SET at S106 - the public-claims item closed, every claim it named read LIVE; whether the set is COMPLETE is what the claims harvest (R3-2) exists to say |"
DOD_CMD_OLD = """# D2 - DONE when this prints nothing (S105: prints 15; positive control: src/app/autonomy/page.tsx)
for f in $(git grep -l escalation_score -- 'src/app/**/*.tsx'); do grep -q -E 'escalation_score_raw|Raw Magnitude' "$f" || echo "$f"; done"""
DOD_CMD_NEW = """# D2 - prints 1. RESTATED AT S106: the S105 command counted FILES, could not see src/app/page.tsx
# (the pathspec needs a directory after src/app/), and listed pages that only declare the field.
python tools/gni_rule_checks.py | grep -cE '^\\[PASS\\] C[0-9]+ +\\S+ +(escalation magnitude)'"""

ORDER_HEAD_OLD_1 = """and ROOT 5 may not exceed 42, unless James rules an exception in writing. Generation 24 held 70.
This close CLOSED one item, MERGED one into its twin and opened two, so the cap held with no
exception."""
ORDER_HEAD_NEW_1 = """and ROOT 5 may not exceed 42, unless James rules an exception in writing. Generation 25 held 70.
This close CLOSED one item and opened one, so the cap held with no exception."""

ITEM_923 = """- **9.23** NEW (S106) [MEASURED] - COR - **THE CAPPED SCORE PINS EVERY CONSUMER OF THE LEVEL, AND
  THREE TABLES CANNOT SHOW WHAT THE CAP HIDES.** 262 of 263 reports sit at the cap (SQL, S106), so the
  level read from the score has been CRITICAL on every run since 2026-06-23. The one exception,
  2026-06-22 15:34 UTC, scored exactly 5 - the reader's own fallback value, so whether it was a real
  reading is UNKNOWN. Adaptive runs its no-analysis mode at CRITICAL (GNI-R-115): its activity log's
  last entry is one minute after that report, and it wrote 0 reports in 930 runs. The frequency
  controller recommends 30 min while the pipeline keeps its cron. `frequency_log`, `alerts` and
  `historical_correlations` carry no raw column, and adaptive's run rows record no mode, so all of
  this is visible only by inference. FIX SHAPE: record the mode on the run row (read every consumer
  of `llm_source` first); carry the raw value where the level is stored. NOT a recalibration - the
  GRAVEYARD rules that out. Whether ROOT 8 returns from the archive on this measurement is James's.
"""

ARCHIVED_ROW = """| **9.22** the public surface's unmeasured claims and query-limit counts | CLOSED S106 in all three parts, each read LIVE on the new build after the deployment reported `success`, each proved with a rendered literal grepped in the minified bundle. (c) DoD D2 at `7403921` + `cd27f88`: one lib, one check, home rank and trend moved to the raw value because capped ties had made every run "top 0%". (b) at `591f218` + `a52bba0`: counts from the run table, exact; the correction commit exists because the fix itself printed a limited length as a count (R-S106-3). (a) at `ac284a2`: dated section-6 constants replace "twice daily", "24/7", "Always On", "Real-time" and "may fire 2-3 hours late" (measured: median 260 min, max 727 min). "The system fixes itself", listed by the S105 text, had already been removed at S105. |
"""

CHANGED = """## CHANGED THIS REGENERATION

- **DECISION S106-1 (delegated: "your call").** The glossary check's candidate class: an all-capitals
  token none of whose parts is a lowercase word in `docs/` prose; the glossary must define it, list
  it as NOT an abbreviation, or match it with a NAMESPACES pattern. Chosen over author markup (it
  checks only what authors mark) and a bare stoplist (about five hundred entries). The length rule
  first drafted was dropped as a hand-written threshold. Its leak classes are in its docstring.
- **DECISION S106-2 (delegated).** ORIGIN cites sessions only, resolved against a file under `docs/`
  or a CHAT-ONLY glossary row; a commit hash is refused (R-S106-2). Over allowing hashes with a full
  clone in CI, and over a generated commit index - both break at the declared history rewrite.
- **DECISION S106-3 (delegated).** D2 through one shared lib and a check, over a fifteen-file render
  patch (drift returns with the next page) and a schema change (scope beyond the line).
- **DECISION S106-4 (delegated).** The adaptive counts were fixed from the run table without touching
  the pipeline; recording the mode on the run row is itemised (9.23), because it changes a production
  write path whose readers were not yet read.
- **DECISION S106-5 (James: "B").** The last public-claims part was finished in-session rather than
  deferred to the claims harvest, closing the item whole.
- CLOSED 9.22 - OPENED 9.23 - count 70, cap held.
- **R3-1 DONE** at `f86febb`, CI `37069679116`. S52 and S53 located as CHAT-ONLY, each with a URL and
  a query in the glossary (James asked that the next agent find S53 at once). The specification's
  "seven-layer defence designed at S53" was wrong: designed at the end of S52, built in S52 and S53.
  S69's "three layers only on paper" conflicts with S52/S53's "built" for two of them - not settled,
  passed to the harvest.
- **PRODUCT, READ LIVE**: `7403921`, `cd27f88`, `591f218`, `a52bba0`, `ac284a2` (see ARCHIVED).
- **MEASURED** (SQL, S106): 262 of 263 reports at the cap since 2026-05-24; the 67 with a raw value
  run from 10.0 to 26.5, median 19.6; 930 adaptive runs and 263 main runs, 263 reports - adaptive wrote
  none; the adaptive activity log holds 85 rows, the last on 2026-06-23.
- **NOTED, NOT ITEMISED UNDER THE CAP**: the letters D and L each name two series (the glossary says
  so); the geopolitical pillar of the 2026-10-02 report dated its events "early October 2024" - ROOT
  2's fabrication surface, model output the harvest does not read; the `escalation magnitude` detail
  prints a native path separator on Windows; activity rows before June carry a constant 6,175 tokens.
- **FOUND IN THE TOOL ITSELF**: `tools/gni_rule_checks.py`'s header named C3 as a rule no check
  implements, omitted C8 and counted "seven"; corrected at `f86febb`.
- **L2 MAD**: three runs since the S105 handoff, every job `success`.
- CONTRACT and PROTOCOL UNCHANGED (v11, v19): no rule of engagement moved; six rules and one further
  instance are in `GNI_RULES_S106.md`.

"""

MAINTAINED_OLD = "`tools/mk_close_s105.py`, which refuses on any disagreement."
MAINTAINED_NEW = "`tools/mk_close_s106.py`, which refuses on any disagreement."

ARCH_STATUS = """
### STATUS AT THE S106 CLOSE - ROW 1 OF 4

- **R3-1 DONE.** `f86febb`, CI `37069679116` green at job level. `passes 'glossary|origin citations'`
  prints 2; the fixture ends `0 mismatches` with four families for `glossary` and five for `origin
  citations`; the live handoff's LOAD CHECK names ORIGIN and the glossary on two lines. AMENDED IN
  THE BUILD (DECISION S106-2): a citation resolves to a session record, never to a commit hash.
- **R3-2 NEXT** (S107). Seeds measured at S106 are listed in the order's mission.
- **OWED, updated.** The lambda baseline still has no command. S106 adds: **mu**, listed by the
  specification's glossary plan, is defined and used nowhere in `docs/` (the glossary's OWED section).
- **AGENT TEST**: not yet run.
"""

ARCH_S12_NOTE_OLD = "(SSOT); a second list here would drift from the one a check reads."


def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s106.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    os.makedirs(out, exist_ok=True)
    res = {}

    o = rd(root, "GNI_TARGET_AND_ORDER_S105.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S105 order does not hash to its published value")
    o = sub1(o, "**GENERATION 25 - 2026-10-02 (S105 close). SUPERSEDES generation 24\n(`GNI_TARGET_AND_ORDER_S104.md`).**",
             "**GENERATION 26 - 2026-10-03 (S106 close). SUPERSEDES generation 25\n(`GNI_TARGET_AND_ORDER_S105.md`).**", "order header")
    o = span(o, "## NEXT SESSION'S MISSION (S106)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = span(o, "**ROADMAP 2 IS FOUR OF FOUR - ACHIEVED AT S104 AND ARCHIVED**",
             "**DEFINITION OF DONE - RESTATED AT S105", TARGET_ROADMAPS, "target roadmaps")
    o = sub1(o, DOD_D2_OLD, DOD_D2_NEW, "dod d2")
    o = sub1(o, DOD_D4_OLD, DOD_D4_NEW, "dod d4")
    o = sub1(o, DOD_CMD_OLD, DOD_CMD_NEW, "dod cmd")
    o = sub1(o, ORDER_HEAD_OLD_1, ORDER_HEAD_NEW_1, "order head")
    o = o.replace("docs/GNI_TARGET_AND_ORDER_S105.md \\\n", "docs/GNI_TARGET_AND_ORDER_S106.md \\\n")
    o = sub1(o, "`tools/mk_close_s105.py`, which refuses to write when they disagree",
             "`tools/mk_close_s106.py`, which refuses to write when they disagree", "head tool")
    o = span(o, "- **9.22** NEW (S105)", "- **9.19** OPEN (S96)", ITEM_923, "9.22 -> 9.23")
    o = sub1(o, "## ARCHIVED - ONE ITEM CLOSES AND ONE MERGES INTO IT THIS GENERATION",
             "## ARCHIVED - ONE ITEM CLOSES INTO IT THIS GENERATION", "archived heading")
    o = sub1(o, "| what | why archived |\n|---|---|\n", "| what | why archived |\n|---|---|\n" + ARCHIVED_ROW, "archived row")
    o = span(o, "## CHANGED THIS REGENERATION", "## HOW THIS FILE IS MAINTAINED", CHANGED, "changed")
    o = sub1(o, MAINTAINED_OLD, MAINTAINED_NEW, "maintained")
    if "9.22" in order_range(o):
        die("a closed id is still cited inside the queue")
    b, a, r5 = scans(o)
    print("order scans: bold=%d any=%d root5=%d (want %d/%d/<=%d)" % (b, a, r5, COUNT, COUNT, ROOT5_CAP))
    if not (b == a == COUNT <= CAP and r5 <= ROOT5_CAP):
        die("order counts disagree or exceed the cap")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD changed during assembly")
    res["GNI_TARGET_AND_ORDER_S106.md"] = o

    a_ = rd(root, "GNI_ARCHITECTURE_S106.md")
    a_ = a_.rstrip("\n") + "\n" + ARCH_STATUS
    res["GNI_ARCHITECTURE_S106.md"] = a_

    rl = rd(root, "GNI_RULES_S105.md")
    rl = rl.rstrip("\n") + "\n" + side("RULES_S106_BLOCK.md")
    res["GNI_RULES_S106.md"] = rl

    res["CONTRACT_S106.md"] = rd(root, "CONTRACT_S105.md")
    res["GNI_Session_Transfer_Protocol_S106.md"] = rd(root, "GNI_Session_Transfer_Protocol_S105.md")
    res["HANDOFF_S106.md"] = side("HANDOFF_S106.md")

    for name, text in sorted(res.items()):
        data = text.encode("utf-8")
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(data)
        print("%-40s %7d bytes  md5 %s (EOL-normalised)" % (name, len(data), hashlib.md5(data).hexdigest()))
    print("WROTE %d files. The macro map is generated LAST, from committed bytes." % len(res))


if __name__ == "__main__":
    main()
