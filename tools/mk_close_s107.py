#!/usr/bin/env python3
"""S107 close assembler - the executable record of how every byte of the S107 close set moved.

Byte-copies the S106 set (DECISION S92-5), applies anchored patches (each anchor must occur exactly
once), BINDS every order item to the claims it serves (roadmap 3 row R3-4), writes the S107 files
into OUTDIR, and REFUSES to write anything when the order's two counting scans disagree with each
other, with the declared count or with the cap, when ROOT 5 exceeds its cap, when an item is left
unbound, when the printed ORPHAN RATE differs from the bindings, or when the GRAVEYARD no longer
hashes to its published value (R-S95-1). The architecture and glossary are S107 files already in the
tree; the macro map is generated LAST from the committed bytes by tools/gni_macro_map.py.
usage: python tools/mk_close_s107.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5_CAP = 70, 70, 42
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"

# R3-4 binding. Each id lists the claims it serves, verified below against the live verdict file
# by a phrase that must occur in the claim's own text. Every other id is ORPHAN.
BIND = {
    "9.24": ["CLM-222", "CLM-272", "CLM-276", "CLM-384", "CLM-451", "CLM-492", "CLM-537", "CLM-655"],
    "9.23": ["CLM-440"], "9.19": ["CLM-170"], "9.20": ["CLM-227"], "9.11": ["CLM-538"],
    "9.12": ["CLM-278"], "6.10": ["CLM-230", "CLM-242", "CLM-492"],
    "6.13": ["CLM-230", "CLM-242", "CLM-492"], "6.5": ["CLM-127", "CLM-144"], "6.3": ["CLM-278"],
    "6.4": ["CLM-745"], "5.30": ["CLM-227"], "5.32": ["CLM-621"], "7.1": ["CLM-226"],
    "7.2": ["CLM-226"], "7.3": ["CLM-226"], "7.4": ["CLM-226"], "2.4": ["CLM-220"],
    "3.1": ["CLM-224"], "4.6": ["CLM-621"],
}
PHRASE = {
    "CLM-440": "escalation 0-10", "CLM-170": "Pipeline success rate", "CLM-227": "3 rounds of debate",
    "CLM-538": "100K tokens/day", "CLM-278": "Live Token Quota", "CLM-230": "02:13", "CLM-242": "02:13",
    "CLM-492": "Myanmar time", "CLM-127": "immutable audit trail", "CLM-144": "immutable audit trail",
    "CLM-745": "Always on", "CLM-621": "MAD is split", "CLM-226": "Johari", "CLM-220": "Yahoo Finance",
    "CLM-224": "sentiment reports", "CLM-222": "8 autonomous GitHub Actions workflows",
    "CLM-272": "8 workflows", "CLM-276": "8 GitHub Actions workflows",
    "CLM-384": "70 injection patterns", "CLM-451": "8 GitHub Actions workflows",
    "CLM-537": "8 autonomous GitHub Actions workflows", "CLM-655": "70 prompt injection patterns",
}


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
    return bold, len(anyd), len(root5)


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
    for ln in rd(root, "GNI_CLAIM_VERDICTS_S107.tsv").split("\n"):
        p = ln.split("\t")
        if len(p) == 5 and p[1] == "CLAIM":
            out[p[3]] = p[4]
    return out


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


MISSION = """## NEXT SESSION'S MISSION (S108)

**ITEM 9.24 - THE EIGHT DEFEATED CLAIMS, MADE TRUE.** DONE when the check labelled `claim status
derived` prints **0 DEFEATED** on the committed tree and every corrected page has been read LIVE on
the new build, proved by a rendered literal grepped in the minified bundle (R-S105-2).

WHY THIS. It is the top of ROOT 9, and it is the first finding roadmap 3 produced about the PRODUCT
rather than about the record: `tools/gni_fitness.py` measured eight public statements against the
tree they describe and found them false - "70 injection patterns" on `/security` and the Dev Console
hub (the list holds 81; 70 is the count of the detector S69 found dead), "8 GitHub Actions workflows"
in five places (there are 9), and "09:00 and 17:00 Myanmar time" on the home page (the cron is 08:43
and 16:43). The claims are listed with their ids in item 9.24 and in `docs/GNI_CLAIMS_S107.md`.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. The detector holds SIXTEEN checks and the
fixture SIXTY-SEVEN families; name a check by its LABEL (R-S105-1). A page edit moves claim lines:
regenerate the claims document (`python tools/gni_claims.py --write 108`) after ANY page change, or
`claims resolve` and `claim status derived` go red on the shift; a NEW sentence needs a verdict row
first, and a new claim a binding row. Prefer a sentence that names no number over one that hard-codes
it; a number that stays must be one a fitness function measures. The container's HEAD must equal
James's HEAD before any generator runs (R-S107-1).

ROADMAP 3, ROW R3-4: binding landed at this close. Its prediction (DECISION S107-8) is judged at the
S108 and S109 closes: the item count must fall below 70. Each of those closes prints
`python tools/gni_lambda.py --window S108:S109` beside it.
"""

TARGET_R3 = """**ROADMAP 3 - CLAIMS - ROWS 1 TO 3 DONE, ROW 4 BOUND AT S107.** Declared at S105 (DECISION
S105-1, delegated). R3-1 at S106. R3-2 at `cf1742c`: 745 claims at 798 locations from the pages and
the White Paper, located at S107 and frozen in `docs/`. R3-3 at `d0612e0`, `203e048`, `4b2b391`:
statuses derived by fitness functions, every unreferenced module in a bucket, every declared layer
mapped to code. R3-4: every item below is bound; the ORPHAN RATE is printed where the queue starts.
Its outcome is measured over the next two closes (DECISION S107-8). Rows, completion test and the
S107 status in `GNI_ARCHITECTURE_S107.md`.

"""

D4_OLD = ("| MET FOR THE KNOWN SET at S106 - the public-claims item closed, every claim it named read LIVE; "
          "whether the set is COMPLETE is what the claims harvest (R3-2) exists to say |")
D4_NEW = ("| NOT MET - the claims harvest (R3-2) answered whether the set was complete, and it was not: eight "
          "count and cadence claims are DEFEATED by the tree they describe (check `claim status derived`), "
          "item 9.24 |")

HEAD_OLD = ("Generation 25 held 70.\nThis close CLOSED one item and opened one, so the cap held with no "
            "exception.")
HEAD_NEW = ("Generation 26 held 70.\nThis close CLOSED one item and opened one, so the cap held with no "
            "exception.")

ORPHAN_ANCHOR = "unchanged: this close's assembler is a different stand-in, not the probe.\n"
ORPHAN_BLOCK = ORPHAN_ANCHOR + """
**ORPHAN RATE: {orph}/{total}**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{{claims: CLM-###, ...}}` - the public claims it serves, ids from `docs/GNI_CLAIMS_S107.md` - or
`{{ORPHAN}}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close; the rate is derived.
"""

ITEM_924 = """- **9.24** NEW (S107) [MEASURED] - COR - **EIGHT PUBLIC CLAIMS ARE DEFEATED BY THE TREE THEY
  DESCRIBE.** Measured by `tools/gni_fitness.py` and published by the check labelled `claim status
  derived`: "70 injection patterns" on `/security` and in the Dev Console hub, where the funnel's list
  holds 81 and 70 is the length of the list in the detector S69 found dead; "8 GitHub Actions
  workflows" in five places, where the tree holds 9; "09:00 and 17:00 Myanmar time" on the home page,
  where the pipeline's cron runs at 08:43 and 16:43 Myanmar time. Done when the check prints 0
  DEFEATED and each page is read LIVE. Prefer count-free prose; a number that stays is one a fitness
  function measures.
"""

LINE_524 = "- **5.24** OPEN (S95) - PER. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**\n"

ARCHIVED_ROW = ("| **5.24** twenty-two files in `docs/` with no session number | CLOSED S107 BY THE RETIRE "
                "CLAUSE, as accepted. Opened S95 and carried unchanged from generation 15 to 26 - twelve "
                "regenerations without a measurement or a ruling. The files are fossils the protocol "
                "already names as non-sources; numbering them buys nothing a reader needs. Its slot "
                "admits 9.24 under the cap. |\n")

CHANGED = """## CHANGED THIS REGENERATION

- **DECISION S107-1 (delegated).** Claims are found by deterministic extraction plus a recorded
  verdict per sentence, keyed by the hash of its text; an unclassified sentence fails the check. Over
  a keyword filter (blind to what it does not list) and over taking every literal (noise).
- **DECISION S107-2 (delegated).** The White Paper enters the tree as frozen verbatim text, one
  paragraph per line, extracted from the .docx; the .pdf is a render of it (20 s later, seven fused
  hyphenations, no other difference).
- **DECISION S107-3 (delegated).** Verdicts are tiered: a fragment of code is DATA by rule, a sentence
  under four words with no lexicon word is UI by rule, everything else is judged. The lexicon's blind
  spot is a fixture family, not a footnote.
- **DECISION S107-4 (delegated).** The harvest unit is the sentence: 61 of the paper's 200 paragraph
  lines hold more than one, and a paragraph that is half true cannot carry one status.
- **DECISION S107-5 (delegated).** Status by measurement binding: a binding names a fitness function
  and a verbatim fragment; the function parses the claimed value and measures the tree. SUPPORTED,
  DEFEATED, or UNMEASURED declared with a reason (OMG SACM's needsSupport). A DEFEATED claim is
  published, not failed; a blank one fails.
- **DECISION S107-6 (James: "pick the complete and reliable one").** Declared layers are found in
  the page text itself and mapped layer by layer to code; the replay judges an old tree by today's
  map. Over folding layers into claim statuses, which cannot gate and cannot read an old tree.
- **DECISION S107-7 (delegated).** lambda redefined by a command, `tools/gni_lambda.py`, over the
  order's own published id scan. The "~6.5" most likely averaged the hand-written NEW lines of
  S98-S101, S100's being a stale copy of S99's - an inference, recorded as one.
- **DECISION S107-8 (delegated).** R3-4's prediction is judged on the queue: under the cap arrivals
  equal departures, so lambda measures closing, not pressure. Hypothesis: the item count falls below
  70 over S108-S109. lambda is still reported, baseline 1.50 per close (S105:S106).
- CLOSED 5.24 (retire clause, accepted) - OPENED 9.24 - count 70, cap held, ROOT 5 at 41.
- **NOT ACTED, NAMED: 5.25's retire clause is due again.** It concerns two secrets whose wiring
  contradicts their consumers; DECISION S92-2 paused that class's clocks, so retiring it is James's.
- **R3-2 DONE** (`fd84f3b`, `cf1742c`), **R3-3 DONE** (`d0612e0`, `203e048`, `4b2b391`), **R3-4 BOUND**
  here; lambda's command `fbf9c06`. Every commit CI-green at job level; `3e09ec3` was red (section 5
  stale: the gating run preceded `git add`) and `5235776` fixed it.
- **MEASURED**: 2597 candidate sentences, 1389 verdicts, 745 claims at 798 locations; COVERAGE 25/745,
  17 SUPPORTED, 8 DEFEATED; 43 unreferenced modules, 1 WIRE (5.32), 2 DELETE (`keyword_sensor.py`,
  `self_healing_runner.py`); 2 live layer declarations, 8 layers, all wired; ORPHAN RATE 50/70.
- **TEST 1 REPLAYED**: S68 reads FAIL on `dead symbols` (the 70-pattern detector) and `declared layers
  wired` (layers four and six of seven); S91 reads FAIL on `order bound to claims`.
- **FOUND IN THE TOOLS THIS SESSION**: Test 1's command could not run as written (a full run halts on
  an old tree); the extractor read a CRLF White Paper's body marker as absent (fixed before any Windows
  clone met it); any `.md` under `docs/` widens the glossary check's English corpus - the paper hid six
  plain words, nothing more, and the claims document hid none.
- **NOTED, NOT ITEMISED UNDER THE CAP**: the claims surfaced six internal contradictions - 70 vs 81
  patterns, two EMA formulas, first verification 10 vs 14 April, three horizon sets, two schedules,
  and a page describing a planned capability in the present tense; the eight measurable ones are 9.24.
- **L2 MAD**: no run between the S106 close and the S107 open; S107 did not re-read MAD.
- CONTRACT UNCHANGED (v11). PROTOCOL v20: Part C step 9a gains the claims document and the HEAD rule.
  Three rules and one further instance are in `GNI_RULES_S107.md`.

"""

MAINTAINED_OLD = "`tools/mk_close_s106.py`, which refuses on any disagreement."
MAINTAINED_NEW = ("`tools/mk_close_s107.py`, which refuses on any disagreement, on an unbound item, and on an ORPHAN\n"
                  "RATE that differs from the bindings it just wrote.")

RULES_BLOCK = """
- R-S107-1 - THE CONTAINER'S HEAD EQUALS THE OPERATOR'S HEAD BEFORE ANY GENERATOR RUNS. Section five
  stamps HEAD; at S107 the container still sat one commit behind James, and the architecture it
  regenerated would have failed his byte check. Before a generator writes a document that will be
  verified on the operator's side, `git rev-parse --short HEAD` on both sides prints the same hash,
  and the operator's script refuses on any other.
  **CHECKABLE: yes** - the commit scripts assert HEAD before regenerating.

- R-S107-2 - A REPLAY RUNS ONLY THE CHECKS IT NAMES. Roadmap 3's Test 1 ran the full detector on the
  S68 tree and grepped two labels; a full run halts on an old tree before any check, so the grep read
  nothing - and nothing reads like "not two of three FAIL". A historical replay uses `--only`, which
  skips the live-document preconditions, and a replay that prints no verdict line is an instrument
  error, never a result.
  **CHECKABLE: yes** - `--only` exits 2 when no label matches.

- R-S107-3 - UNDER A WIP CAP, AN ARRIVAL RATE MEASURES THE CLOSING RATE. A full order admits an item
  only when one leaves, so arrivals equal departures and lambda fell from about eight to one and a
  half without any pressure falling. Before a prediction rests on a rate, state the cap that bounds
  it; under a binding cap, judge the hypothesis on what the cap does not bound - here, the queue
  shrinking below it.
  **CHECKABLE: no** - it constrains how a prediction is written.

## FURTHER INSTANCE of R-S100-2 (stage a new or changed tool before regenerating anything)
S107's first product commit added two tools, ran the detector BEFORE `git add`, saw it green, and CI
went red: section five inventories the INDEX, and an untracked tool is invisible to it. The rule
already said to stage first; the session read the trap in the handoff and did not apply it. The
detector run that gates a commit is a regeneration too - it runs on the staged state, or it has
verified a tree that will not be committed.
**CHECKABLE: yes** - every S107 commit script verified after `git add`.
"""

PROTO_TITLE_OLD = "# GNI SESSION TRANSFER PROTOCOL v19"
PROTO_TITLE_NEW = "# GNI SESSION TRANSFER PROTOCOL v20"
PROTO_9A_OLD = ("      `python tools/gni_state.py  --session {N} --src docs/GNI_ARCHITECTURE_S{N}.md`\n"
                "      `python tools/gni_macro_map.py --session {N}`\n")
PROTO_9A_NEW = ("      `python tools/gni_state.py  --session {N} --src docs/GNI_ARCHITECTURE_S{N}.md`\n"
                "      `python tools/gni_claims.py --write {N}`   (v20: whenever a page, the verdicts,\n"
                "                                                  the bindings or the White Paper moved)\n"
                "      `python tools/gni_macro_map.py --session {N}`\n")
PROTO_9A_HEAD_OLD = "    STAGE A NEW OR CHANGED TOOL BEFORE REGENERATING ANYTHING (v15, R-S100-2). The\n"
PROTO_9A_HEAD_NEW = ("    THE CONTAINER'S HEAD EQUALS THE OPERATOR'S HEAD BEFORE ANY GENERATOR RUNS (v20,\n"
                     "    R-S107-1): section five stamps HEAD, so a container one commit behind writes a\n"
                     "    document the operator's byte check refuses.\n\n"
                     "    STAGE A NEW OR CHANGED TOOL BEFORE REGENERATING ANYTHING (v15, R-S100-2). The\n")
PROTO_LOG_OLD = "## VERSION LOG\n\n"
PROTO_LOG_NEW = ("## VERSION LOG\n\n"
                 "- **v20 - S107 (2026-10-03).** PART C step 9a only. It gains the claims document among the\n"
                 "  artifacts a close regenerates - a page edit moves claim lines, and two checks read them - and\n"
                 "  the HEAD rule (R-S107-1), because section five stamps HEAD and the container had sat one commit\n"
                 "  behind the operator. PART A, B and D unchanged.\n")


def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s107.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    handoff = os.path.join(out, "HANDOFF_S107.md")
    if not os.path.exists(handoff):
        die("HANDOFF_S107.md must already be in OUTDIR (written from the Part B template)")
    os.makedirs(out, exist_ok=True)
    res = {}
    claims = claim_texts(root)

    o = rd(root, "GNI_TARGET_AND_ORDER_S106.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S106 order does not hash to its published value")
    o = sub1(o, "**GENERATION 26 - 2026-10-03 (S106 close). SUPERSEDES generation 25\n(`GNI_TARGET_AND_ORDER_S105.md`).**",
             "**GENERATION 27 - 2026-10-03 (S107 close). SUPERSEDES generation 26\n(`GNI_TARGET_AND_ORDER_S106.md`).**", "header")
    o = span(o, "## NEXT SESSION'S MISSION (S107)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = span(o, "**ROADMAP 3 - CLAIMS - ROW 1 OF 4 DONE AT S106.**", "**DEFINITION OF DONE - RESTATED AT S105",
             TARGET_R3, "target roadmap")
    o = sub1(o, D4_OLD, D4_NEW, "dod d4")
    o = sub1(o, HEAD_OLD, HEAD_NEW, "order head")
    o = o.replace("docs/GNI_TARGET_AND_ORDER_S106.md \\\n", "docs/GNI_TARGET_AND_ORDER_S107.md \\\n")
    o = sub1(o, "`tools/mk_close_s106.py`, which refuses to write when they disagree",
             "`tools/mk_close_s107.py`, which refuses to write when they disagree", "head tool")
    o = sub1(o, "- **9.23** NEW (S106) [MEASURED]", ITEM_924 + "- **9.23** NEW (S106) [MEASURED]", "9.24 in")
    o = sub1(o, LINE_524, "", "5.24 out")
    o = sub1(o, "| what | why archived |\n|---|---|\n", "| what | why archived |\n|---|---|\n" + ARCHIVED_ROW, "archived")
    o = span(o, "## CHANGED THIS REGENERATION", "## HOW THIS FILE IS MAINTAINED", CHANGED, "changed")
    o = sub1(o, MAINTAINED_OLD, MAINTAINED_NEW, "maintained")
    o, orphans, total = bind(o, claims)
    o = sub1(o, ORPHAN_ANCHOR, ORPHAN_BLOCK.format(orph=orphans, total=total), "orphan rate")
    if "5.24" in order_range(o):
        die("a closed id is still cited inside the queue")
    bold, anyd, r5 = scans(o)
    print("order scans: bold=%d any=%d root5=%d orphan=%d/%d (want %d/%d/<=%d)"
          % (len(bold), anyd, r5, orphans, total, COUNT, COUNT, ROOT5_CAP))
    if not (len(bold) == anyd == total == COUNT <= CAP and r5 <= ROOT5_CAP):
        die("order counts disagree, exceed the cap, or an id has no defining line")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD changed during assembly")
    res["GNI_TARGET_AND_ORDER_S107.md"] = o

    rl = rd(root, "GNI_RULES_S106.md")
    res["GNI_RULES_S107.md"] = rl.rstrip("\n") + "\n" + RULES_BLOCK

    pr = rd(root, "GNI_Session_Transfer_Protocol_S106.md")
    pr = sub1(pr, PROTO_TITLE_OLD, PROTO_TITLE_NEW, "protocol title")
    pr = sub1(pr, PROTO_9A_OLD, PROTO_9A_NEW, "protocol 9a list")
    pr = sub1(pr, PROTO_9A_HEAD_OLD, PROTO_9A_HEAD_NEW, "protocol 9a head")
    pr = sub1(pr, PROTO_LOG_OLD, PROTO_LOG_NEW, "protocol log")
    res["GNI_Session_Transfer_Protocol_S107.md"] = pr

    res["CONTRACT_S107.md"] = rd(root, "CONTRACT_S106.md")

    for name, text in sorted(res.items()):
        data = text.encode("utf-8")
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(data)
        print("%-40s %7d bytes  md5 %s (EOL-normalised)" % (name, len(data), hashlib.md5(data).hexdigest()))
    print("WROTE %d files beside HANDOFF_S107.md. The macro map is generated LAST." % len(res))


if __name__ == "__main__":
    main()
