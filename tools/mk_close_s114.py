#!/usr/bin/env python3
"""S114 close assembler - the executable record of how every byte of the S114 close set moved.

S114 IS NOT A PHASE TRANSITION (Protocol Part C step 4a): roadmap 5 stands at ONE ROW OF FOUR - R5-1 DONE
at `ae0b0b1`, the sample `docs/gni_output_sample_S114.json`. So the order is regenerated from generation 33
by anchored patches (each anchor must occur exactly once), every binding tag is stripped and RE-MADE against
the live claims, and nothing is re-classified.

The count HOLDS at 58 by DECISION S114-11 (delegated): WAIT-10 folded into 9.5 as tail (g) and was paid at
`3ed06f5`; WAIT-9 folded into 9.5 as tail (h), open; the residuals of S114's security read WIDEN 6.16
instead of opening an item. One S114 finding waits outside the range as WAIT-11. The file is REFUSED when
the two counting scans disagree with each other, with the declared count or with the cap, when ROOT 5 moves
from 34, when an item is left unbound, when a binding names a claim the live claims document no longer
carries or whose text no longer holds its phrase, when a decimal number lands inside the order range, or
when the GRAVEYARD no longer hashes to its published value (R-S95-1).

CONTRACT goes to v12 (DECISION S114-7, the review cadence for archived roadmaps) and PROTOCOL to v22 (the
step that runs it, and Part A's stale "it is private"). The register gains four rules and two amendments.
The architecture, glossary and roadmap 5 specification are born as S114. Section five, the claims document
and the macro map are regenerated after this script, the map LAST.
usage: python tools/mk_close_s114.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5, ORPHANS = 58, 70, 34, 41
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"

# R3-4 binding, re-made at S114 against the live claims. Unchanged from S113: CLM-852 left the claims at
# 3ed06f5 and served no item (only WAIT-10 cited it).
BIND = {
    "9.19": ["CLM-170"], "9.5": ["CLM-757"], "6.10": ["CLM-230", "CLM-242", "CLM-751"],
    "6.13": ["CLM-230", "CLM-242", "CLM-751"], "6.3": ["CLM-391"],
    "5.30": ["CLM-235"], "5.32": ["CLM-391"], "7.1": ["CLM-226"], "7.2": ["CLM-226"],
    "7.3": ["CLM-226"], "7.4": ["CLM-226"], "2.4": ["CLM-1007"], "3.1": ["CLM-293"],
    "4.6": ["CLM-391"],
    "9.25": ["CLM-1079", "CLM-1080", "CLM-814", "CLM-531"], "9.26": ["CLM-739", "CLM-1065", "CLM-798"],
    "9.27": ["CLM-185", "CLM-1133"],
}
PHRASE = {
    "CLM-170": "Pipeline success rate", "CLM-757": "PENDING", "CLM-230": "02:13", "CLM-242": "02:13",
    "CLM-751": "scheduled for 08:43 and 16:43 Myanmar time", "CLM-391": "per-account usage",
    "CLM-235": "3 rounds", "CLM-226": "Johari", "CLM-1007": "Yahoo Finance chart data",
    "CLM-293": "verdict with confidence score",
    "CLM-1079": "GPVS v1.2", "CLM-1080": "shows skill only if", "CLM-814": "trust weight",
    "CLM-531": "trust weights", "CLM-739": "a fall of 2% or more", "CLM-1065": "48 hours",
    "CLM-798": "0.7 x old",
    "CLM-185": "logged and explained", "CLM-1133": "Log every upgrad",
    # minted at 3ed06f5 (DECISION S114-5); cited by the CHANGED section
    "CLM-1138": "admitted by its Origin or Referer header", "CLM-1139": "Neither check is a lock",
}
MINTED_S114 = ("CLM-1138", "CLM-1139")
RETIRED_S114 = ("CLM-852",)
TAG_RE = re.compile(r" \{(?:claims: [^}]*|ORPHAN)\}$")
CLAIMS_DOC = "GNI_CLAIMS_S113.md"            # the live claims document when this script runs
VERDICTS = "GNI_CLAIM_VERDICTS_S113.tsv"


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


def after1(text, anchor, add, what):
    return sub1(text, anchor, anchor + add, what)


def span(text, start, end, new, what):
    if text.count(start) != 1 or text.count(end) != 1:
        die("%s: span anchors not unique (%d, %d)" % (what, text.count(start), text.count(end)))
    i, j = text.index(start), text.index(end)
    if j <= i:
        die(what + ": span end precedes start")
    return text[:i] + new + text[j:]


def order_range(t):
    return t.split("\n## THE ORDER\n", 1)[1].split("\n## ARCHIVED", 1)[0]


def published_range(t):
    """What the published sed command reads: from `## THE ORDER` THROUGH the `## ARCHIVED` heading line."""
    i = t.index("\n## THE ORDER\n") + 1
    j = t.index("\n## ARCHIVED", i) + 1
    k = t.index("\n", j)
    return t[i:k + 1]


def scans(t):
    r = published_range(t)
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
    for ln in rd(root, VERDICTS).split("\n"):
        p = ln.split("\t")
        if len(p) == 5 and p[1] == "CLAIM":
            out[p[3]] = p[4]
    return out


def live_claim_ids(root):
    return set(re.findall(r"^\| (CLM-[0-9]+) \|", rd(root, CLAIMS_DOC), re.M))


def check_claim(c, claims, live, what):
    if c not in claims or PHRASE[c] not in claims[c]:
        die("%s -> %s does not hold against the verdict file" % (what, c))
    if c not in live:
        die("%s -> %s names a claim the live claims document no longer carries" % (what, c))


def strip_tags(text):
    head, rest = text.split("\n## THE ORDER\n", 1)
    body, tail = rest.split("\n## ARCHIVED", 1)
    out, n = [], 0
    for ln in body.split("\n"):
        if re.match(r"^\s*-\s+\*\*(\d+\.\d+)\*\*", ln) and TAG_RE.search(ln):
            ln, n = TAG_RE.sub("", ln), n + 1
        out.append(ln)
    return head + "\n## THE ORDER\n" + "\n".join(out) + "\n## ARCHIVED" + tail, n


def bind(text, claims, live):
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
                    check_claim(c, claims, live, "binding " + iid)
                ln = ln.rstrip() + " {claims: %s}" % ", ".join(ids)
            else:
                ln = ln.rstrip() + " {ORPHAN}"
                orphans += 1
        out.append(ln)
    missing = set(BIND) - seen
    if missing:
        die("bound ids not in the queue: %s" % sorted(missing))
    return head + "\n## THE ORDER\n" + "\n".join(out) + "\n## ARCHIVED" + tail, orphans, len(seen)


# ------------------------------------------------------------------ ORDER, generation 34
HEADER_OLD = ("**GENERATION 33 - 2026-10-13 (S113 close, a PHASE TRANSITION). SUPERSEDES generation 32\n"
              "(`GNI_TARGET_AND_ORDER_S112.md`).**")
HEADER_NEW = ("**GENERATION 34 - 2026-10-18 (S114 close). SUPERSEDES generation 33\n"
              "(`GNI_TARGET_AND_ORDER_S113.md`).**")

MISSION = """## NEXT SESSION'S MISSION (S115)

**ROADMAP 5, ROW R5-2 - THE MACHINE MEASURES, THEIR THRESHOLDS RULED BEFORE ANYTHING IS MEASURED.** The
second row of the working roadmap. DONE when:
(a) the guidelines are found and read at their sources BEFORE anything is proposed: what a readability
measure of `fff_what_is_happening` can and cannot say, and what plain-language guidance sets as a level -
ISO 24495-1:2023 gives principles and no number (DECISION S114-2) - plus a market-jargon list and the
generic-path phrases the report prompt already bans. Then the operator rules the readability threshold
and the jargon list, recorded as a DECISION and carried in the next commit message (R-S112-1), BEFORE any
measure is computed over `docs/gni_output_sample_S114.json`: a threshold typed after the measurement is a
status typed by hand (the specification's section 5).
(b) R5-2's DONE line holds from bytes (`docs/GNI_ROADMAP5_SPEC_S114.md` section 3): the checks are added
to the CHECKS list of `ai_engine/analysis/self_bias_gate.py`, not a module beside it; fitness functions
run the same checks over the sample; CLM-1109, 1111, 1112, 1113, 1124 and 1125 are each bound to one, and
each has a failure test on a copy (a sample with one failing output turns its claim DEFEATED). Detector
and fixture green; CI green at job level.
(c) the first block reads what ran while nobody watched: the seventh scheduled backup (the trap expires at
seven green; six of six at S114) and whether `gni_market` runs on a Saturday. Every log a runner fetches
has its exit code and size checked before it is read (R-S81-1, amended at S114).
(d) the operator rules on WAIT-11 (section FINDINGS AWAITING A SLOT). The count is 58 and may not grow
without an exception in writing.

WHY THIS ORDER. R5-1 is done, and every later row reads R5-2's functions: R5-3 compares people's ratings
with them, R5-4 calls them inline. The thresholds are the operator's because the sample is already in the
tree, and a number chosen after looking at it would grade the sample by its own distribution. (c) is one
runner. (d) is one ruling.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. The sample: 88 reports, every report created in
[2026-08-31 09:02:39Z, 2026-10-14 00:00Z) - the lower bound is `fd43129`, the last change to the
report-writing code - 0 empty fields, 0 model-fallback events, `query_md5`
`0f3dd05e3401603479394e81604a0b69`. Claims 841 at 902 locations; COVERAGE 162/841; 0 DEFEATED; UNREVIEWED
0; NUMBERS UNDERIVED 0. The promise ledger: 238 rows, BUILT 63, PARTIAL 105, NOT BUILT 70, WITHDRAWN 0.
Detector 20 checks, fixture 112 families. Every scheduled main run since `1adf922` installed the pinned
versions and printed no `Quality feedback:` line (S114 C7, read from the job logs).
"""

R5_OLD = "`docs/GNI_ROADMAP5_SPEC_S113.md` (corrected at `50022aa`). ROADMAP CHECK: **zero rows of four.**"
R5_NEW = ("`docs/GNI_ROADMAP5_SPEC_S114.md` (corrected at `50022aa`; S114 records R5-1 and the rulings).\n"
          "ROADMAP CHECK: **one row of four** - R5-1 DONE at `ae0b0b1` (S114): `docs/gni_output_sample_S114.json`\n"
          "holds every report of the DECISION S114-1 window, its `query_md5` matching the query in the tree, and\n"
          "its writer refuses a copy whose rows or per-report md5 disagree. R5-4's ruling is given\n"
          "(annotate-and-alert, DECISION S114-4); R5-2's and R5-3's are carried to their rows' starts.")

COUNT_OLD1 = "unless James rules an exception in writing. Generation 32 held 58.\n"
COUNT_NEW1 = "unless James rules an exception in writing. Generation 33 held 58.\n"
COUNT_OLD2 = ("By DECISION S113-1 this close opened one item and closed one by the retire clause, so the count\n"
              "HOLDS at 58; two S113 findings wait outside the range for the operator's ruling.")
COUNT_NEW2 = ("By DECISION S114-11 this close opened nothing and closed nothing: WAIT-9 and WAIT-10 folded into\n"
              "9.5 as tails (h) and (g), and the S114 security read's residuals widen 6.16, so the count HOLDS at\n"
              "58; one S114 finding waits outside the range for the operator's ruling.")
EXPECT_LINE = "**EXPECTED ITEM COUNT: 58 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**"
PRINT_LINE = "Both must print **58**. BOTH WERE RUN ON THE ASSEMBLED BYTES BEFORE THIS FILE WAS WRITTEN, by"

ORPHAN_START = "**ORPHAN RATE: 41/58**"
ORPHAN_END = "### ROOT 9 - PUBLIC COPY"
ORPHAN_BLOCK = """**ORPHAN RATE: @ORPH@/@TOTAL@**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{claims: CLM-###, ...}` - the public claims it serves, ids from the live claims document - or
`{ORPHAN}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close and re-made at every close
since. At S114 every bound sentence was re-read in the claims by the assembler. The one claim retired at
`3ed06f5` served no item - only the waiting finding WAIT-10 cited it, and that finding is folded into
9.5 - so no binding moved. The rate is derived.

**NOT A PHASE TRANSITION (S114).** Roadmap 5 stands at one row of four, so this generation is patched
from generation 33 and no item is re-classified. The S114 security read (OWASP Top 10:2025, OWASP API
Security Top 10 2023, OWASP Top 10 for LLM Applications 2025, GitHub's Actions secure-use guide) found
no SILENT LIVE FAILURE in the DISCOVERY POLICY's sense: what it could fix inside the session shipped by
the operator's rulings (DECISION S114-8, S114-9), and what is left widens 6.16 rather than opening an
item. Notes are added to 9.5, 9.19, 9.26, 9.27, 6.10, 6.16, 5.29, 5.40 and 3.1; 3.1 is marked
MEASURED.

"""

N95_ANCHOR = "  text, so a removed article's audit trail is incomplete (was WAIT-8's lead).\n"
N95_ADD = """  NOTE (S114, DECISION S114-5 and S114-6): tail (g), was WAIT-10, PAID at `3ed06f5` - `/developer-hub`
  stopped saying that a request without the key is refused, and says what `src/lib/auth.ts` does: the
  site's pages are admitted by Origin or Referer, any other caller needs the key, and neither check is a
  lock (OWASP API Security Top 10 2023, API2). The sentence's claim retired; CLM-1138 and CLM-1139 were
  minted, each read against its page (R-S113-2). Tail (h), was WAIT-9, OPEN: widen the claims harvest to
  the text a page renders from `src/lib/`. The pending-row branch of `e9c6ca9` was SEEN on the live site
  on 2026-10-14 at 15:15Z - `/api/latest` sent a pending row's confidence as null while the raw
  `/api/reports` control sent the insert placeholder - so tail (f) is paid on real data. Left: (d),
  dormant; (h). LEAD added at S114: `pillar_reports` store the three Freedom from Fear sections and no
  page renders them, so R5-1 did not sample them.
"""
N919_ANCHOR = "  of context kept, never zero.\n"
N919_ADD = """  NOTE (S114) [MEASURED]: every debate whose `ARB-ARRIVAL` S114 read - nine, 2026-10-14 to 2026-10-17 -
  had every assembled article arrived and none truncated or dropped; `ARB-FIT` estimated
  4741 to 4948 of its 5000 budget with the same steps. Still not the zero-article case; on 2026-10-16
  the margin was 52 tokens.
"""
N926_ANCHOR = "  unbound for this reason. Each needs the guideline it implements, or a written reason it has none.\n"
N926_ADD = """  NOTE (S114): the claims that state the confidence interval's method read SUPPORTED - F-CI-T and
  F-CI-TEMPS find the copy's t value, sample size and temperatures in the code - and SUPPORTED there
  says that the copy matches the code, not that the method is valid. The method's defect is carried
  here, not by the claims status.
"""
N927_ANCHOR = "  day - then design the entry; logging every weight write may be the wrong grain.\n"
N927_ADD = """  NOTE (S114) [MEASURED, run logs]: the volume. An evening run writes about sixteen weight rows per
  verified report - 16 for one report; 31, 32 and 31 for two (S114 C2, C5, C7) - and the morning run
  wrote them too, through the quality channel, until `e3b81a1`. The writes are upserts, so the table
  keeps no history and a past weight cannot be read back. Lean for the design: one audit entry per run,
  naming the reports verified and each weight before and after, not one entry per write.
"""
N610_ANCHOR = "  bracket the runs they were written to protect. A lead folded here, not opened (DECISION S109-9).\n"
N610_ADD = """  NOTE (S114) [MEASURED]: still true. The main pipeline started between about six and ten hours after
  its cron on every day S114 read, and `gni_market` about four hours after its slots; every run
  completed - S114 C6 read 72 runs across ten workflows after 2026-10-15 16:28Z, 0 failed.
"""
N616_ANCHOR = "  this a new finding to the operator - WRONG, this item has held it since S105 (R-S89-1).\n"
N616_ADD = """  NOTE (S114, DECISION S114-11) - WIDENED to the residuals of S114's security read, rather than an
  item opened under the cap. (a) is the item as opened: the lock and the manifest disagree. (b) The web
  app runs Next on its 14 line, past its end of life (2025-10-26): about 22 advisories are fixed only on
  the 15 line. Its two criticals need Windows hosting
  or the image optimizer, and GNI uses neither; two are reachable - a denial of service through server
  components (high) and cache poisoning (moderate). The fix is the migration. (c) The shadcn command-line
  chain sits in `dependencies`. Dependabot opened eight pull requests on 2026-10-13 (#1 to #8), all
  transitive or development packages; none is merged. The lean is one change - shadcn to
  `devDependencies`, then `npm audit fix` - made together with (a). (d) `/api/about-stats` returns the
  exception's text to its caller (A10). (e) Nothing alerts on abuse of the API (A09). (f) The pip
  constraints pin versions, not hashes, so a package outside the list still floats (A03). (g) The
  `anon` role holds every table privilege on the public tables and RLS alone refuses its writes
  (S114_Q2); revoking the grants is defence in depth (A01). PAID inside S114, not carried: least-privilege
  tokens and SHA-pinned actions (`c91e2de`), one constraints file (`1adf922`), the CSP cut to what the
  pages load (`2a34427`), and three repository settings - the default token read-only, Dependabot alerts
  and security updates on, and a ruleset that refuses deletion and force-push on main.
"""
N529_ANCHOR = "  the generator's parser. Appends since S99 have used the dominant shape without regularising.\n"
N529_ADD = """  NOTE (S114) [MEASURED]: five rules from S111 to S113 carry `**CHECKABLE: partly**`, a seventh shape
  the macro map's yes-or-no pattern does not read, so R-S113-1 and R-S113-2 are absent from its X axis.
  The S114 rules carry yes or no; the five are not rewritten, because a marker changed after the fact
  would change what those sessions said.
"""
N540_ANCHOR = "  `OPENCAGE_API_KEY`, GNI-L-002's class), written in the promise ledger's CLM-073 note.\n"
N540_ADD = """  NOTE (S114): `update_mad_confidence` in `prompt_manager.py` - which rolls a prompt variant back after
  three debates under 40% confidence - is imported by `main.py` and called nowhere, so that rollback
  cannot fire. A lonely symbol for this triage; not deleted.
"""
N31_DEF_OLD = "- **3.1** WIDENED (S86) - COR. A constant confidence value on two dates."
N31_DEF_NEW = "- **3.1** WIDENED (S86) [MEASURED AT S114] - COR. A constant confidence value on two dates."
N31_ANCHOR = "  BEARISH. Unruled. Roadmap 5 bears on it: a confidence that barely moves is output a reader sees.\n"
N31_ADD = """  NOTE (S114) [MEASURED, the database and run logs]: S114_Q1 read the debate confidences stored for the
  R5-1 window - 53% is the mode, at 59% of 87. The ten debates read in S114's run logs gave, in order,
  53, 53, 73, 73, 53, 53, 57, 53, 48 and 77 per cent. S114 predicted that more than half of the last four
  would read 53% and was WRONG: one of four did. The mode holds and the spread is wider than the S111 to
  S113 screens showed. Still unruled; the hypothesis (history injection, a prompt asking for a moderate
  confidence) is untested.
"""

ARCH_HEAD_OLD = "## ARCHIVED - ROADMAP 4 IS ACHIEVED, AND ONE ITEM CLOSES BY THE RETIRE CLAUSE, THIS GENERATION"
ARCH_HEAD_NEW = "## ARCHIVED - NOTHING ENTERS OR LEAVES THIS GENERATION"

AWAIT_START = "## FINDINGS AWAITING A SLOT (S113) - OUTSIDE THE COUNT, FOR THE OPERATOR'S RULING AT S114"
AWAIT_HEAD = """## FINDINGS AWAITING A SLOT (S114) - OUTSIDE THE COUNT, FOR THE OPERATOR'S RULING AT S115

S113's two findings left this section at S114: WAIT-10 folded into 9.5 as tail (g) and was paid at
`3ed06f5` (DECISION S114-5); WAIT-9 folded into 9.5 as tail (h), open (DECISION S114-6). Their
generation-33 text stays in `GNI_TARGET_AND_ORDER_S113.md`. S114 found one more, numbered WAIT-11 so that
no id is reused. The count is 58 and may not grow across a regeneration (CONTRACT v11), so an item that
enters needs one that leaves or the operator's exception in writing.

"""
WAIT_NEW = """- **WAIT-11 - PRE - QUALITATIVE IS A TERMINAL STATE.** 298 claims in the live claims document carry the
  reason QUALITATIVE: no fitness function reads them, so none can ever turn DEFEATED, and nothing
  schedules a second look. Roadmap 4's review gave each one once; S113 found seven on one page that its
  own page contradicted (R-S113-2), and S114's open re-check of the archived roadmaps found another
  overstated one (the API's "refused", paid as 9.5(g)). CONTRACT v12's review cadence re-runs completion
  tests, which count QUALITATIVE as reviewed, so it does not reach them either. Options for the ruling:
  re-read a stated sample of them against their pages at each cadence review; or give QUALITATIVE an
  expiry after which a claim is UNREVIEWED again; or accept the state and write the reason.
"""

CHANGED = """## CHANGED THIS REGENERATION

- **NOT A PHASE TRANSITION (Part C step 4a).** Roadmap 5: one row of four - R5-1 DONE at `ae0b0b1`; R5-2,
  R5-3 and R5-4 not started. The order is patched from generation 33; no item is re-classified.
- **MISSION (S113's declaration for S114): YES.** (a) The four owed rulings were asked together and
  delegated: DECISION S114-1 ruled the window and size, S114-4 ruled R5-4, S114-2 and S114-3 carried
  R5-2's and R5-3's to their rows by name (`e51cdc2`'s message). (b) R5-1's DONE line holds from bytes:
  `tools/gni_output_sample.sql` was written and reviewed before it ran, and `docs/gni_output_sample_S114.json`
  holds 88 reports, `query_md5` matching (`ae0b0b1`); the writer refused the operator's first copy, a
  Markdown export that had lost one backslash (`677bc62`). (c) The R3 live read saw the pending-row branch
  on the live site on 2026-10-14 at 15:15Z, against the raw route as control: PASS. (d) WAIT-9 and WAIT-10
  ruled (S114-5, S114-6).
- **DECISIONS S114-1 to S114-7 (delegated - "your call", 2026-10-14), carried in `e51cdc2`'s message.**
  S114-1: the window is `created_at` in [2026-08-31 09:02:39Z, 2026-10-14 00:00Z), every report in it, a
  census - its start is `fd43129`, the last change to the report-writing code, so the window is one code
  regime (DECISION S90-3); weakness named: a change of the model secret is invisible to git. S114-2: the
  readability threshold and jargon list CARRIED to R5-2's start - ISO 24495-1:2023 gives no number.
  S114-3: the outside reader CARRIED to R5-3's start. S114-4: annotate-and-alert over hold-for-review -
  holding conflicts with NN-1 and NN-PHI-2. S114-5: WAIT-10 into 9.5 as tail (g), paid. S114-6: WAIT-9
  into 9.5 as tail (h). S114-7: a review cadence for archived roadmaps, ruled at this close as CONTRACT v12
  - every close whose session number is a multiple of ten, and every phase transition; the first is due
  at the S120 close (NIST AI RMF GOVERN 1.5: the frequency of periodic review is decided in advance).
- **DECISION S114-8 (delegated - "your call", option A, after the security read).** Harden what the read
  found in the build and the repository: least-privilege tokens and SHA-pinned actions in every workflow
  (`c91e2de`), one constraints file for every pip install (`1adf922`), and three settings read back - the
  default token read-only, Dependabot alerts and security updates on, a ruleset refusing deletion and
  force-push on main. Over B (write the findings, fix nothing) and C (migrate Next first): A was small,
  reversible and certified on 30 and more scheduled runs with 0 failures; C is the largest change and
  has no reachable critical behind it.
- **DECISION S114-9 (the operator: "2", from the list of light tasks).** The CSP stops allowing six origins
  no page loads in the browser (`2a34427`); four pages read in the operator's browser console after the
  deploy.
- **DECISION S114-10 (delegated - "your call").** A over B: close now, with the seventh backup and the
  Saturday market read carried to the S115 open, rather than wait about five hours for one reading.
- **DECISION S114-11 (delegated, at this close).** The count holds at 58 with no exception: the security
  residuals widen 6.16 instead of opening an item, because they share its subject (what the web app is
  built from and exposes) and its owner; the eight Dependabot pull requests are not merged one by one -
  they are handled as 6.16(c). WAIT-11 is written outside the range.
- MERGED none - OPENED none - CLOSED none - FOLDED two findings (WAIT-9, WAIT-10) - count 58, ROOT 5 at 34,
  ORPHAN 41/58. One S114 finding waits as WAIT-11.
- **SHIPPED** (eight product commits, each CI-green at job level, Vercel `success` where a page moved):
  `e51cdc2` the sample query and its writer; `3ed06f5` `/developer-hub`'s key sentence; `bed11b6` two
  generators stop printing hand-written state; `677bc62` the writer accepts the JSON export; `ae0b0b1`
  the sample; `c91e2de` tokens and pins; `1adf922` constraints; `2a34427` the CSP.
- **MEASURED**: claims 841 at 902 locations, COVERAGE 162/841, 0 DEFEATED, UNREVIEWED 0, NUMBERS UNDERIVED
  0; the sample, 88 reports; 3.1 from the database and ten logs; 9.27's volume; nine debates with every
  article arrived; 72 runs after 2026-10-15 16:28Z, 0 failed; six of six scheduled backups green.
- **FOUND IN THE TOOLS**: two generators printed hand-written state into the sections they generate
  (R-S114-2, paid at `bed11b6`); a runner checked a commit hash where only the tree survives `git am`
  (R-S114-1); a watcher took an in-progress run as already seen (R-S114-3); a cache kept a failed log fetch
  as a log, the case R-S81-1's S84 amendment already named (amended again); a Markdown export lost a
  byte the row count could not see (R-S111-3, amended); two security leads reported before their code
  path was read (R-S114-4).
- CONTRACT v12 (the review cadence). PROTOCOL v22 (step 4b runs it; Part A's "it is private" corrected).
  Four rules and two amendments are in `GNI_RULES_S114.md`. Architecture S114 (roadmap 5 at one of four,
  two stale prose lines corrected, the security posture written in section 11); glossary S114; roadmap
  5 specification S114.

"""

MAINTAINED_OLD = "`tools/mk_close_s113.py`, which refuses on any disagreement, on an unbound item, on a binding\n"
MAINTAINED_NEW = "`tools/mk_close_s114.py`, which refuses on any disagreement, on an unbound item, on a binding\n"

# ------------------------------------------------------------------ RULES
RULES_BLOCK = """
## S114 ADDITIONS (2026-10-18)

- R-S114-1 - A PATCH DELIVERED THROUGH `git am` KEEPS ITS TREE, NOT ITS HASH; A RUNNER CHECKS THE TREE.
  S114 built each commit in the container, shipped it with `git format-patch`, and the operator's runner
  applied it with `git am --committer-date-is-author-date`. The trees matched; the commit hashes did not,
  because the committer differs. S114_R1b refused a correct commit on its hash and was replaced by R1c,
  which compares `git rev-parse HEAD^{tree}` with the tree gated in the container. A session never
  promises the operator a hash it computed itself.
  **CHECKABLE: yes** - a runner that applies a patch and then compares `rev-parse HEAD` with a literal can be grepped.

- R-S114-2 - A GENERATED DOCUMENT PRINTS NO HAND-WRITTEN STATE. `tools/gni_blocks.py` printed into
  ARCHITECTURE section 5.5 that 36 assertions had never run in CI, six sessions after the CI harness began
  running them, and `tools/gni_macro_map.py` printed "Five checks exist" beside a detector of twenty. A
  generated section is trusted because a tool wrote it, so a sentence typed into the tool is published
  as if measured, and C5, which forbids a hand-written integer inside a check, never reads a generator's
  prose. Paid at `bed11b6` by printing where the answer is read, not a new number (PROTOCOL v18).
  **CHECKABLE: no** - a count inside a generator's string is found by reading it; C5's lint sees integers, not prose.

- R-S114-3 - A WATCHER DECIDES WHAT IT HAS SEEN BY THE NEWEST COMPLETED RUN. S114_W1 took a run still in
  progress as already seen, so the window it was written to catch opened and closed while it waited, and
  its twelve-hour limit then ended it. S114_W2 keys "seen" on the newest run whose status is `completed`;
  an in-progress run is neither seen nor missed.
  **CHECKABLE: no** - the property belongs to a watcher's loop, which lives outside the repository.

- R-S114-4 - A VULNERABILITY IS A LEAD UNTIL ITS CODE PATH IS READ END TO END. S114's security read
  reported two that were not there: anonymous writes to `mission_control_log` (the route writes with the
  service key, and its writes land by design) and an unbounded `article-events` read (the route already
  limits its rows). Both came from a probe's response or a grep, before the route was read. A finding
  about access or resource use is reported after the code that serves the request is read, with the line
  that decides it.
  **CHECKABLE: no** - whether a path was read before a finding was written is a property of the session.

- R-S81-1 (AMENDED 2026-10-18): the S84 amendment says a redirected failure produces a corpus, and `wc -l`
  comes before any grep on a cached or redirected artifact. Amended: a CACHE turns that corpus permanent.
  S114's runners fetched each run log with `gh run view --log > file 2>&1` and reused any file that was
  non-empty; on 2026-10-17 GitHub's log service failed for three of four runs, each file held one 286-byte
  error line, and C6 read "Quality feedback 0, Traceback 0" off them as clean runs. The rule was in the
  register and the session did not apply it. A fetch is cached only when its exit code is 0 and its size
  is plausible; a failed fetch is printed as a failure and retried, never counted.

- R-S111-3 (AMENDED 2026-10-18): an export carries its own row count and the reader asserts it. Amended:
  it also carries a content hash computed AT THE SOURCE for each row. The SQL Editor's Markdown export of
  the R5-1 cell had the right row count and had lost one backslash in 406690 bytes; only the md5 Postgres
  computed over each report's texts showed the copy was not the data, and the writer refused it.
"""

# ------------------------------------------------------------------ CONTRACT v12
CONTRACT_ANCHOR = "\"Is this arc finished?\" must be answerable from the repo by a named command.\n"
CONTRACT_CADENCE = ("- REVIEW CADENCE FOR ARCHIVED ROADMAPS (v12, S114, DECISION S114-7, delegated). An archived roadmap's "
                    "written completion test is RE-RUN from bytes at every close whose session number is a multiple of ten "
                    "and at every PHASE TRANSITION. Each archived roadmap gets one line in CHANGED THIS REGENERATION - HOLDS, "
                    "or DRIFTED with its evidence - and a drift is a finding under the DISCOVERY POLICY, never a silent "
                    "re-open of the roadmap. The first review is due at the S120 close. WHY: NIST AI RMF GOVERN 1.5 asks that "
                    "periodic review be planned and its frequency decided in advance; the S114 open re-checked roadmaps 1 to "
                    "4 by hand, unasked by any step, and found drift every check had passed - a generated section publishing "
                    "a false sentence, a public sentence overstating what the API refuses.\n")
CONTRACT_LOG_ANCHOR = ("  other line is byte-identical to `CONTRACT_S104.md` as it stands at `5fc6936`.\n")
CONTRACT_LOG_ADD = ("- v12 - S114 (2026-10-18): REVIEW CADENCE added under TARGET AND ORDER, delegated by James (DECISION\n"
                    "  S114-7). A rule of engagement, not a lesson: it changes what a close must do with an ARCHIVED roadmap,\n"
                    "  which until now no close re-read. PROTOCOL swept the same close (R-S82-4) to v22. Recorded with it, and\n"
                    "  changing no rule: v6's reason \"it is private and the container is empty\" no longer holds - the\n"
                    "  repository is public (since S104) and a session container may clone it - and v6's rule stands on its\n"
                    "  other ground, that a numbered file never copied is visibly absent. Every other line is byte-identical\n"
                    "  to `CONTRACT_S113.md`.\n")

# ------------------------------------------------------------------ PROTOCOL v22
P_HEAD_OLD = "# GNI SESSION TRANSFER PROTOCOL v21\n"
P_HEAD_NEW = "# GNI SESSION TRANSFER PROTOCOL v22\n"
P_PRIV_OLD = ("  But NO SESSION READS THE REPO. It is private, the container is empty, and every file reaches\n"
              "  a session because James ATTACHES it. v3 protected a read that never happens, and charged a\n"
              "  filename negotiation at every close for the privilege.\n")
P_PRIV_NEW = ("  But NO SESSION READS THE REPO. It is private, the container is empty, and every file reaches\n"
              "  a session because James ATTACHES it. v3 protected a read that never happens, and charged a\n"
              "  filename negotiation at every close for the privilege. (v22: the repo has been PUBLIC since\n"
              "  S104 and a container may clone it to verify the attachments - Part D step 0 - so this reason\n"
              "  is history; the rule stands on the next one.)\n")
P_STEP4A_ANCHOR = ("   write \"roadmap N of M\" in one line and move on. SILENCE IS NOT AN ANSWER: an unwritten\n"
                   "   check cannot be audited, and the arc that dies is the one no close ever asked about (D4).\n")
P_STEP4B = ("\n4b. REVIEW CADENCE (v22, CONTRACT v12). If {N} is a multiple of ten, or step 4a found a roadmap\n"
            "   complete, re-run EVERY ARCHIVED roadmap's written completion test from bytes, by the commands\n"
            "   beside it in ARCHITECTURE, and write one line per roadmap in CHANGED THIS REGENERATION: HOLDS, or\n"
            "   DRIFTED with the evidence. A drift is a finding (step 2), not a re-opened roadmap. If neither\n"
            "   holds, write \"review cadence: not due\" in one line. The first review is due at S120.\n")
P_LOG_ANCHOR = "## VERSION LOG\n\n"
P_LOG_ADD = ("- **v22 - S114 (2026-10-18).** PART C gains step 4b, which runs the REVIEW CADENCE that CONTRACT v12 added (DECISION\n"
             "  S114-7): archived roadmaps are re-read at every tenth close and at every phase transition, because\n"
             "  until now nothing re-read them and the S114 open found drift by doing so unasked. Steps were NOT\n"
             "  renumbered (DECISION S96-4's constraint). PART A's v4 rationale \"It is private\" is marked as\n"
             "  history - Part D step 0 has said PUBLIC since v19, so the file contradicted itself (R-S82-4's sibling\n"
             "  sweep). PART B and PART D unchanged.\n")

# ------------------------------------------------------------------ ARCHITECTURE (born S114)
A_PRIV_OLD = ("| Repo is PRIVATE; chat sessions run with an empty container | chat cannot read the repo — every file "
              "arrives as an attachment (CONTRACT v6). **Does not apply to a local agent.** |\n")
A_PRIV_NEW = ("| Repo is PUBLIC (since S104); a chat session's container may clone it read-only and never pushes | every "
              "close file still reaches a session as an attachment (CONTRACT v6) and is verified by bytes against a "
              "clone (PROTOCOL Part D step 0); the operator runs every commit and push |\n")
A_RULES_OLD = ("GNI holds 134 engineering rules. All 134 are prose; all 134 require an LLM to read\n"
               "and apply; **none is executable.** Yet many are mechanically checkable —\n")
A_RULES_NEW = ("At S92 GNI held 134 engineering rules, all prose, all needing an LLM to read and\n"
               "apply; **none was executable.** Since S95 `tools/gni_rule_checks.py` executes some of\n"
               "them; how many is state, and the macro map's Z axis prints it. Many more are mechanically checkable —\n")
A_SEC_ANCHOR = ("hours. Both fixed by selecting on a RELATION, not a position.\n")
A_SEC_ADD = """
**SECURITY POSTURE, READ AT S114** (OWASP Top 10:2025; OWASP API Security Top 10 2023; OWASP Top 10
for LLM Applications 2025; GitHub's Actions secure-use guide). What the system IS after the read, not a
queue - the residuals are the order's item 6.16.
- *Build and repository (A03, A08).* Every workflow declares `permissions: contents: read` (the heartbeat
  adds `actions: write`, the one dispatch the code makes); every action is pinned to a commit SHA; every
  pip install reads `.github/constraints/python-3.11.txt`; the repository's default token is read-only,
  Dependabot alerts and security updates are on, and a ruleset refuses deletion and force-push on main.
  Versions are pinned, hashes are not.
- *Web app (A02, A05, API2).* The CSP allows scripts and connections from the site's own origin only; it
  keeps `'unsafe-inline'` and `'unsafe-eval'`, which only a nonce-based policy removes. The API admits
  the site's pages by Origin or Referer and any other caller by a key that every browser receives, so
  it limits casual use and protects nothing secret - the data is public by design. The Telegram webhook
  refuses a request without its secret token. The framework is past its end of life (item 6.16).
- *Database (A01).* RLS is on for every public table and no write policy exists for `anon`, so the anon
  key the browser holds can read and cannot write; the grants themselves are wider than the policies.
- *Model output (LLM01, LLM05).* Reports are written by the model from harvested articles; the funnel
  screens inputs for injection patterns (F-INJ) and nothing executes model output. Roadmap 5 measures
  what the output says to a reader.
"""
A_R5_OLD = ("**WORKING FROM S114 (S113 close, the phase transition).** Roadmap 4 was declared ACHIEVED, so this\n"
            "roadmap is the working one. ROADMAP CHECK: **zero rows of four.** R5-1 is first; it needs one of the\n"
            "operator's four owed rulings (the sample window and its size), and each later row needs its own.\n")
A_R5_NEW = A_R5_OLD + """
### STATUS AT THE S114 CLOSE - ONE ROW OF FOUR

- **R5-1 DONE** at `ae0b0b1`: `docs/gni_output_sample_S114.json` holds the operator's cell of
  `tools/gni_output_sample.sql`, kept unaltered - 88 reports, every one created in [2026-08-31 09:02:39Z,
  2026-10-14 00:00Z) (DECISION S114-1; the start is `fd43129`, the last change to the report-writing code),
  0 empty fields, 0 model-fallback events, `query_md5` `0f3dd05e3401603479394e81604a0b69` matching the
  query in the tree. `tools/gni_output_sample.py` refuses a copy whose rows, order, window or per-report
  md5 disagree; it refused the first copy, a Markdown export that had lost one backslash.
- **R5-4 ruled** annotate-and-alert (DECISION S114-4). **R5-2 and R5-3** wait on their rulings, carried by
  name (S114-2, S114-3). The specification moves to `docs/GNI_ROADMAP5_SPEC_S114.md`.
- Claims 841 at 902 locations, COVERAGE 162/841, 0 DEFEATED. Detector 20 checks, fixture 112 families.
  Order generation 34: 58 items.
"""
A_SPEC_OLD = "**The specification is a separate document**, `docs/GNI_ROADMAP5_SPEC_S113.md`, and it is not copied\n"
A_SPEC_NEW = "**The specification is a separate document**, `docs/GNI_ROADMAP5_SPEC_S114.md`, and it is not copied\n"

# ------------------------------------------------------------------ GLOSSARY (born S114)
G_HEAD_OLD = "# GNI GLOSSARY - S113\n"
G_HEAD_NEW = "# GNI GLOSSARY - S114\n"
G_FIX = [
    ("| `R5-\\d+` | a row of roadmap 5 (`docs/GNI_ROADMAP5_SPEC_S112.md`) |",
     "| `R5-\\d+` | a row of roadmap 5 (`docs/GNI_ROADMAP5_SPEC_S<N>.md`, the highest number is live) |"),
    ("| `NN-\\d+` | a non-negotiable of the S32 philosophy, NN-1 to NN-8 (`docs/GNI_PHILOSOPHY_S112.md`) |",
     "| `NN-\\d+` | a non-negotiable of the S32 philosophy, NN-1 to NN-8 (`docs/GNI_PHILOSOPHY_S<N>.md`) |"),
    ("| `NP-\\d+` | a principle of the S32 philosophy, NP-1 to NP-5 (`docs/GNI_PHILOSOPHY_S112.md`) |",
     "| `NP-\\d+` | a principle of the S32 philosophy, NP-1 to NP-5 (`docs/GNI_PHILOSOPHY_S<N>.md`) |"),
    ("`docs/GNI_PHILOSOPHY_S112.md`; WAIT-7 |", "`docs/GNI_PHILOSOPHY_S113.md`; roadmap 6, a candidate (was WAIT-7) |"),
    ("`docs/GNI_PHILOSOPHY_S112.md`; WAIT-6 |", "`docs/GNI_PHILOSOPHY_S113.md`; order item 9.27 (was WAIT-6) |"),
    ("S35 record; WAIT-7 |", "S35 record; roadmap 6, a candidate (was WAIT-7) |"),
]
G_NS_ANCHOR = "| `S\\d+` | a session number |\n"
G_NS_ADD = ("| `A\\d\\d` | a category of the OWASP Top 10:2025, A01 Broken Access Control to A10 Mishandling of Exceptional "
            "Conditions, cited by S114's security read |\n"
            "| `API\\d+` | a risk of the OWASP API Security Top 10 2023; API2 is Broken Authentication |\n"
            "| `LLM\\d\\d` | a risk of the OWASP Top 10 for LLM Applications 2025; LLM01 is Prompt Injection, LLM05 Improper "
            "Output Handling |\n")
G_DEFINED_ANCHOR = "\n## NOT ABBREVIATIONS\n"
G_DEFINED_ADD = [
    ("OWASP", "the Open Worldwide Application Security Project, whose Top 10 lists (web 2025, API 2023, LLM "
              "applications 2025) S114's security read followed", "S114 security read"),
    ("CSP", "Content-Security-Policy, the response header that names the origins a page may load scripts, "
            "styles, images and connections from", "`next.config.mjs`; S114 R8"),
]


# ------------------------------------------------------------------ ROADMAP 5 SPECIFICATION (born S114)
S_HEAD_OLD = "# ROADMAP 5 - FREEDOM FROM FEAR, MEASURED - SPECIFICATION (S113)\n"
S_HEAD_NEW = "# ROADMAP 5 - FREEDOM FROM FEAR, MEASURED - SPECIFICATION (S114)\n"
S_STATUS_ANCHOR = "Freedom from Fear can mean when measured. `docs/GNI_ROADMAP5_SPEC_S112.md` stays as it was.\n"
S_STATUS_ADD = ("\n**S114: R5-1 DONE at `ae0b0b1`; the four owed rulings asked together (section 5).** The sample is\n"
                "`docs/gni_output_sample_S114.json`. Nothing else in this specification changed;\n"
                "`docs/GNI_ROADMAP5_SPEC_S113.md` stays as it was.\n")
S_OWED_OLD = """| owed | needed by | why |
|---|---|---|
| the sample window and its size | R5-1 | a dated window keeps the sample from going stale (DECISION S90-3, S112-4) |
| the readability threshold and the jargon list | R5-2 | a threshold typed after the measurement is a status typed by hand |
| who the outside reader is | R5-3 | the builder grading its own proxies is the self-grading roadmap 4 refused |
| annotate-and-alert, or hold-for-review | R5-4 | blocking conflicts with NN-1 and NN-PHI-2; this spec leans to annotate-and-alert |
"""
S_OWED_NEW = """| owed | needed by | why | ruled (S114, delegated) |
|---|---|---|---|
| the sample window and its size | R5-1 | a dated window keeps the sample from going stale (DECISION S90-3, S112-4) | DECISION S114-1: every report created in [2026-08-31 09:02:39Z, 2026-10-14 00:00Z), a census of 88; the start is `fd43129`, the last change to the report-writing code |
| the readability threshold and the jargon list | R5-2 | a threshold typed after the measurement is a status typed by hand | CARRIED to R5-2's start (DECISION S114-2): ISO 24495-1:2023 gives principles and no number; the sample is in the tree, so the threshold is ruled before any measure is computed over it |
| who the outside reader is | R5-3 | the builder grading its own proxies is the self-grading roadmap 4 refused | CARRIED to R5-3's start (DECISION S114-3) |
| annotate-and-alert, or hold-for-review | R5-4 | blocking conflicts with NN-1 and NN-PHI-2; this spec leans to annotate-and-alert | DECISION S114-4: annotate-and-alert |
"""
S_SEQ_OLD = ("Roadmap 4's Test 2 first (S113 open): the ledger now holds the founding philosophy, so the answer to\n"
             "\"how much of what GNI set out to be is built?\" can quote values, not only features. Then R5-1, whose\n"
             "query is written and reviewed before it is run.\n")
S_SEQ_NEW = S_SEQ_OLD + ("S114: R5-1 done. Next R5-2, whose thresholds are ruled before any measure runs over the sample;\n"
                         "then R5-3 and R5-4, each after its ruling.\n")


def glossary_rows(rows):
    return "".join("| %s | %s | %s |\n" % r for r in rows)


def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s114.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    if not os.path.exists(os.path.join(out, "HANDOFF_S114.md")):
        die("HANDOFF_S114.md must already be in OUTDIR (written from the Part B template)")
    claims, live = claim_texts(root), live_claim_ids(root)
    for c in MINTED_S114:
        check_claim(c, claims, live, "minted at S114")
    for c in RETIRED_S114:
        if c in live:
            die("%s should be retired from the live claims document" % c)

    o = rd(root, "GNI_TARGET_AND_ORDER_S113.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S113 order does not hash to its published value")
    o = sub1(o, HEADER_OLD, HEADER_NEW, "header")
    o = span(o, "## NEXT SESSION'S MISSION (S114)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = sub1(o, R5_OLD, R5_NEW, "roadmap 5 status")
    o = sub1(o, COUNT_OLD1, COUNT_NEW1, "count note 1")
    o = sub1(o, COUNT_OLD2, COUNT_NEW2, "count note 2")
    if o.count("docs/GNI_TARGET_AND_ORDER_S113.md \\\n") != 2:
        die("the two published scan commands are not both present")
    o = o.replace("docs/GNI_TARGET_AND_ORDER_S113.md \\\n", "docs/GNI_TARGET_AND_ORDER_S114.md \\\n")
    o = sub1(o, "`tools/mk_close_s113.py`, which refuses to write when they disagree",
             "`tools/mk_close_s114.py`, which refuses to write when they disagree", "head tool")
    for line in (EXPECT_LINE, PRINT_LINE):
        if o.count(line) != 1:
            die("count line missing or doubled: %r" % line[:60])
    o, ntags = strip_tags(o)
    if ntags != COUNT:
        die("expected %d binding tags in generation 33, stripped %d" % (COUNT, ntags))
    o = span(o, ORPHAN_START, ORPHAN_END, "@@ORPHAN@@\n", "orphan block")
    o = after1(o, N95_ANCHOR, N95_ADD, "9.5 note")
    o = after1(o, N919_ANCHOR, N919_ADD, "9.19 note")
    o = after1(o, N926_ANCHOR, N926_ADD, "9.26 note")
    o = after1(o, N927_ANCHOR, N927_ADD, "9.27 note")
    o = after1(o, N610_ANCHOR, N610_ADD, "6.10 note")
    o = after1(o, N616_ANCHOR, N616_ADD, "6.16 note")
    o = after1(o, N529_ANCHOR, N529_ADD, "5.29 note")
    o = after1(o, N540_ANCHOR, N540_ADD, "5.40 note")
    o = sub1(o, N31_DEF_OLD, N31_DEF_NEW, "3.1 defining line")
    o = after1(o, N31_ANCHOR, N31_ADD, "3.1 note")
    o = sub1(o, ARCH_HEAD_OLD, ARCH_HEAD_NEW, "archive head")
    o = span(o, AWAIT_START, "## HOW THIS FILE IS MAINTAINED", AWAIT_HEAD + WAIT_NEW + "\n" + CHANGED,
             "awaiting + changed")
    o = sub1(o, MAINTAINED_OLD, MAINTAINED_NEW, "maintained")
    o, orphans, total = bind(o, claims, live)
    o = sub1(o, "@@ORPHAN@@\n", ORPHAN_BLOCK.replace("@ORPH@", str(orphans)).replace("@TOTAL@", str(total)),
             "orphan rate")
    bold, anyd, r5 = scans(o)
    print("order scans: bold=%d any=%d root5=%d orphan=%d/%d (want %d/%d/%d, orphan %d)"
          % (len(bold), len(anyd), r5, orphans, total, COUNT, COUNT, ROOT5, ORPHANS))
    if anyd - bold:
        die("the any-digits scan sees non-item numbers in the queue: %s" % sorted(anyd - bold))
    if not (len(bold) == len(anyd) == total == COUNT) or COUNT > CAP:
        die("count disagreement: bold %d, any %d, items %d, declared %d, cap %d"
            % (len(bold), len(anyd), total, COUNT, CAP))
    if r5 != ROOT5:
        die("ROOT 5 holds %d items, declared %d" % (r5, ROOT5))
    if orphans != ORPHANS:
        die("orphan count %d, declared %d" % (orphans, ORPHANS))
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD changed during assembly")
    if "- **WAIT-" in order_range(o):
        die("a waiting finding landed inside the order range")
    for w in (9, 10):
        if "- **WAIT-%d - " % w in o:
            die("WAIT-%d is still defined; DECISION S114-5/6 ruled it" % w)
    if o.count("- **WAIT-11 - ") != 1:
        die("WAIT-11 is defined %d times" % o.count("- **WAIT-11 - "))
    if "## NEXT SESSION'S MISSION (S114)" in o or "PHASE TRANSITION (S113) - EVERY ITEM" in o:
        die("the S114 mission or the S113 transition note survived the regeneration")
    for c in RETIRED_S114:
        if c in o:
            die("the order cites the retired claim " + c)
    files = {"GNI_TARGET_AND_ORDER_S114.md": o}

    r = rd(root, "GNI_RULES_S113.md")
    if "R-S114-" in r:
        die("the S113 register already carries an S114 rule")
    for rid in ("R-S81-1 (AMENDED 2026-10-13)", "- R-S111-3 - AN EXPORT CARRIES ITS OWN ROW COUNT"):
        if r.count(rid) != 1:
            die("the rule being amended is not in the register exactly once: " + rid)
    files["GNI_RULES_S114.md"] = r.rstrip("\n") + "\n" + RULES_BLOCK

    c = rd(root, "CONTRACT_S113.md")
    c = after1(c, CONTRACT_ANCHOR, CONTRACT_CADENCE, "contract cadence")
    c = after1(c, CONTRACT_LOG_ANCHOR, CONTRACT_LOG_ADD, "contract log")
    files["CONTRACT_S114.md"] = c

    p = rd(root, "GNI_Session_Transfer_Protocol_S113.md")
    p = sub1(p, P_HEAD_OLD, P_HEAD_NEW, "protocol head")
    p = sub1(p, P_PRIV_OLD, P_PRIV_NEW, "protocol part A")
    p = after1(p, P_STEP4A_ANCHOR, P_STEP4B, "protocol step 4b")
    p = after1(p, P_LOG_ANCHOR, P_LOG_ADD, "protocol log")
    files["GNI_Session_Transfer_Protocol_S114.md"] = p

    a = rd(root, "GNI_ARCHITECTURE_S113.md")
    if "STATUS AT THE S114 CLOSE" in a:
        die("the S113 architecture already carries the S114 status")
    a = sub1(a, A_PRIV_OLD, A_PRIV_NEW, "architecture constraint")
    a = sub1(a, A_RULES_OLD, A_RULES_NEW, "architecture 8.3")
    a = after1(a, A_SEC_ANCHOR, A_SEC_ADD, "architecture security posture")
    a = sub1(a, A_R5_OLD, A_R5_NEW, "architecture roadmap 5 status")
    a = sub1(a, A_SPEC_OLD, A_SPEC_NEW, "architecture spec pointer")
    files["GNI_ARCHITECTURE_S114.md"] = a

    g = rd(root, "GNI_GLOSSARY_S113.md")
    g = sub1(g, G_HEAD_OLD, G_HEAD_NEW, "glossary head")
    for old, new in G_FIX:
        g = sub1(g, old, new, "glossary pointer")
    g = after1(g, G_NS_ANCHOR, G_NS_ADD, "glossary namespaces")
    for term, _, _ in G_DEFINED_ADD:
        if re.search(r"^\| %s \|" % re.escape(term), g, re.M):
            die("glossary already defines " + term)
    defined, rest = g.split(G_DEFINED_ANCHOR, 1)
    g = defined.rstrip("\n") + "\n" + glossary_rows(G_DEFINED_ADD) + G_DEFINED_ANCHOR + rest
    files["GNI_GLOSSARY_S114.md"] = g

    s = rd(root, "GNI_ROADMAP5_SPEC_S113.md")
    s = sub1(s, S_HEAD_OLD, S_HEAD_NEW, "spec head")
    s = after1(s, S_STATUS_ANCHOR, S_STATUS_ADD, "spec status")
    s = sub1(s, S_OWED_OLD, S_OWED_NEW, "spec owed table")
    s = sub1(s, S_SEQ_OLD, S_SEQ_NEW, "spec sequencing")
    files["GNI_ROADMAP5_SPEC_S114.md"] = s

    for name, text in files.items():
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(text.encode("utf-8"))
        print("wrote %-42s %7d bytes  md5 %s" % (name, len(text.encode("utf-8")),
                                                  hashlib.md5(text.encode("utf-8")).hexdigest()))


if __name__ == "__main__":
    main()
