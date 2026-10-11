#!/usr/bin/env python3
"""S110 close assembler - the executable record of how every byte of the S110 close set moved.

S110 is a PHASE TRANSITION close (Protocol PART C step 4a): roadmap 3 is declared ACHIEVED and archived,
roadmap 4 is declared with its written completion test (DECISION S110-12, delegated by James), and the
order is regenerated with every surviving item re-read against the target. Byte-copies the S109 set
(DECISION S92-5), applies anchored patches (each anchor must occur exactly once), strips and RE-BINDS
every order item to the claims it serves, writes the S110 files into OUTDIR, appends two lines to
docs/GNI_ORIGIN.md (append-only; refuses if either line is already there), and REFUSES to write
anything when the order's two counting scans disagree with each other, with the declared count or with
the cap, when ROOT 5 exceeds its cap, when an item is left unbound, when a binding names a claim the
LIVE claims document no longer carries (stricter than S109: a retired claim keeps its verdict row), when
a closed id is still cited in the queue, or when the GRAVEYARD no longer hashes to its published value
(R-S95-1). The architecture is born here as S110 from the S109 file in the tree. The macro map is
generated LAST from the committed bytes, after sections five and seven are regenerated.
usage: python tools/mk_close_s110.py <repo-root> <outdir>"""
import hashlib, os, re, sys

COUNT, CAP, ROOT5_CAP, ORPHANS = 62, 70, 42, 47
GRAVEYARD_MD5 = "3e8ac222c6ef212261676c02d7d56f6f"
CLOSED = ("9.11", "9.12", "6.5")

# R3-4 binding, re-made at S110. 9.11, 9.12 and 6.5 left the queue (all bound). 9.5's remainder (e)
# waits to see the PENDING heading on real data, so it serves CLM-757; CLM-692/693 were retired at S110.
BIND = {
    "9.19": ["CLM-170"], "9.5": ["CLM-757"], "6.10": ["CLM-230", "CLM-242", "CLM-751"],
    "6.13": ["CLM-230", "CLM-242", "CLM-751"], "6.3": ["CLM-278"], "6.4": ["CLM-745"],
    "5.30": ["CLM-227"], "5.32": ["CLM-621"], "7.1": ["CLM-226"], "7.2": ["CLM-226"],
    "7.3": ["CLM-226"], "7.4": ["CLM-226"], "2.4": ["CLM-220"], "3.1": ["CLM-224"],
    "4.6": ["CLM-621"],
}
PHRASE = {
    "CLM-170": "Pipeline success rate", "CLM-757": "PENDING", "CLM-230": "02:13", "CLM-242": "02:13",
    "CLM-751": "scheduled for 08:43 and 16:43 Myanmar time", "CLM-278": "Live Token Quota",
    "CLM-745": "Always on", "CLM-227": "3 rounds of debate", "CLM-621": "MAD is split",
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
    for ln in rd(root, "GNI_CLAIM_VERDICTS_S110.tsv").split("\n"):
        p = ln.split("\t")
        if len(p) == 5 and p[1] == "CLAIM":
            out[p[3]] = p[4]
    return out


def live_claim_ids(root):
    return set(re.findall(r"^\| (CLM-[0-9]+) \|", rd(root, "GNI_CLAIMS_S110.md"), re.M))


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
                    if c not in live:
                        die("binding %s -> %s names a claim the live claims document no longer carries" % (iid, c))
                ln = ln.rstrip() + " {claims: %s}" % ", ".join(ids)
            else:
                ln = ln.rstrip() + " {ORPHAN}"
                orphans += 1
        out.append(ln)
    missing = set(BIND) - seen
    if missing:
        die("bound ids not in the queue: %s" % sorted(missing))
    return head + "\n## THE ORDER\n" + "\n".join(out) + "\n## ARCHIVED" + tail, orphans, len(seen)


# ------------------------------------------------------------------ ORDER, generation 30
HEADER_OLD = ("**GENERATION 29 - 2026-10-04 (S109 close). SUPERSEDES generation 28\n"
              "(`GNI_TARGET_AND_ORDER_S108.md`).**")
HEADER_NEW = ("**GENERATION 30 - 2026-10-11 (S110 close, a PHASE TRANSITION). SUPERSEDES generation 29\n"
              "(`GNI_TARGET_AND_ORDER_S109.md`).**")

MISSION = """## NEXT SESSION'S MISSION (S111)

**ROADMAP 4, ROW R4-1 - THE UNREVIEWED RATCHET, THEN THE FIRST PAGE REVIEWED.** DONE when: (a) the
claims document's STATUS line prints, derived by the tool beside COVERAGE, two counts: claims still
UNREVIEWED (415 at S110), and number-bearing statements on the public pages that no fitness function
supports and no HISTORICAL or PROVENANCE reason excuses (139 at S110); (b) a check labelled
`unreviewed ratchet` fails when either printed count differs from the one the tree derives, or rises
above the count the previous claims generation printed - shipped with fixture families that make it go
RED both ways and one in which a count falls and it stays green, CI green at job level (R-S90-1); (c) with the time left, the claims of ONE page are reviewed -
`/about/devops` first, the page carrying the most UNREVIEWED claims (46 at S110) - each given a fitness
function, a written reason from `UNMEASURED_REASONS`, or its copy retired, and the ratchet falls by
that page's count.

WHY THIS, NOT THE TOP ITEM. Roadmap 3 was declared ACHIEVED at the S110 close and roadmap 4 was
declared in the same close (DECISION S110-12, delegated). Roadmap 4 is ROOT 9's own work: the top of
ROOT 9 is 9.19, which waits on a run no session can force, and 9.5's remainder is a dormant trigger and
a cert that needs a narrow morning window. R4-1 comes first for the reason R3-4's baseline came first:
a count the machine derives before the work is the only way the work can later be shown to have moved
it. The rows, their commands, the completion test and the OWED list are in `GNI_ARCHITECTURE_S110.md`,
section ROADMAP 4.

WHAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED. 752 claims at 805 locations; COVERAGE 32/752,
0 DEFEATED; 720 UNMEASURED - 415 UNREVIEWED, 204 PROMISE, 61 HISTORICAL, 36 PROVENANCE, 4 QUALITATIVE,
counted as unique ids from the claims document's evidence column. The binding file holds 427
UNREVIEWED rows because a retired claim keeps its rows: count claims from the claims document, never
rows from the binding file. A copy change mints claim units that need a verdict row and a binding row
before `python tools/gni_claims.py --write 111`. `RUNTIME` is defined in the docstring of
`tools/gni_fitness.py` (a claim about runtime waits for a fitness function that reads a committed
snapshot); `EXTERNAL`, `PROVENANCE` and `QUALITATIVE` are accepted and defined nowhere - roadmap 4's OWED
list asks for them before row R4-2 uses them. S105 measured the queue turning inward (ROOT 5 from 11 to
42 items while ROOT 9 stood still): R4-1 is roadmap 4's only instrument row, and a session that ships
the instrument without moving the count has repeated that.
"""

TARGET_R = """**ROADMAP 3 - CLAIMS - DECLARED ACHIEVED AT THE S110 CLOSE, AND ARCHIVED.** Four rows DONE by S109; the
historical replay read FAIL on all three lines at S107; the agent test PASSED at S110 and stands as one
line in `docs/GNI_ORIGIN.md`, with the roadmap's ACHIEVED line beneath it. The agent test's verdict was
delegated by James to the session that answered, so the test graded itself - said in the line, in
R-S110-3, and the reason roadmap 4's human test may not be delegated.

**ROADMAP 4 - CLAIMS REVIEWED - DECLARED AT THE S110 CLOSE (DECISION S110-12, delegated by James: "your
call").** Every claim GNI makes about itself is looked at - measured by a fitness function, given the
written reason it cannot be, or retired with its copy - and every promise has a state a reader can
count: built, partly built, not built or withdrawn. Four rows, a completion test and an OWED list, each
row with the command that answers it, in `GNI_ARCHITECTURE_S110.md`. ROADMAP CHECK (Part C step 4a):
roadmap 4, rows zero of four - declared this close.

"""

D2_OLD = "`historical_correlations` keeps a capped average labelled as capped (DECISION S109-2) |"
D2_NEW = ("`historical_correlations` keeps a capped average labelled as capped (DECISION S109-2). S110: the "
          "`/researcher` trend moved to the raw magnitude through one helper, and the check now also refuses "
          "the capped score divided by the cap |")
D4_OLD = "BOUND HALF MET AT S108, HELD AT S109 - `claim status derived` prints 0 DEFEATED from `7cfc1d2` through `c78c288`"
D4_NEW = "BOUND HALF MET AT S108, HELD AT S109 AND S110 - `claim status derived` prints 0 DEFEATED from `7cfc1d2` through `980e876`"
D4B_OLD = "NOT DECLARABLE: 727 of 748 claims are UNMEASURED, and the check speaks only for what is bound"
D4B_NEW = ("NOT DECLARABLE: 720 of 752 claims are UNMEASURED, 415 of them never reviewed, and the check speaks "
           "only for what is bound. Roadmap 4 rows R4-2 and R4-3 are this line's other half")

HEAD_OLD = ("Generation 28 held 68.\nThis close CLOSED three items and opened none, so the count FELL to 65.")
HEAD_NEW = ("Generation 29 held 65.\nThis close CLOSED three items and opened none, so the count FELL to 62.")

ORPHAN_NEW = """**ORPHAN RATE: @ORPH@/@TOTAL@**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{claims: CLM-###, ...}` - the public claims it serves, ids from `docs/GNI_CLAIMS_S110.md` - or
`{ORPHAN}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close and re-made at S110: the
item about the S69 census now serves CLM-757, the PENDING heading its remainder waits to see on real
data, because the two sentences it served were retired with their copy; the rate is derived.

**PHASE TRANSITION (S110) - EVERY ITEM RE-READ AGAINST THE TARGET, NOTHING INHERITED.** Roadmap 3 is
archived, so no item below keeps a place because it served that roadmap. Each item's defining line was
read at this close against TRUTHFULNESS OF OUTPUT and against roadmap 4. The result is stated rather
than implied: no class changed and the order of the roots stands. ROOT 9 stays TOP because roadmap 4
is its work; ROOT 6 stays second, with the backup gone from it; ROOT 5 keeps its S104 standing note,
which already says what this paragraph says. What is carried is carried because it is still true.

"""

ITEM_95 = """- **9.5** OPEN - COR - **THE S69 CENSUS - TWO TAILS LEFT.** F16 to F19 were measured at S110. F16 FIXED
  (`4b58cf3`: the `/researcher` trend goes through `trendSeries()`); F17 PAID by the tree (the S72 fix is
  still there - `/research` shows a confidence width only for multi-run rows); F18 FIXED (`0c57334`: the
  newest refresh only); F19 FIXED (`c3e5652`: exact counts). (b) FIXED (`fc68ff7`), and the `/comparison`
  panel that still decided agreement by itself FIXED (`ddbb439`). (c) SHIPPED (`b82a982`: the check
  labelled `escalation magnitude` now sees the capped score divided by the cap, and the check labelled
  `verdict in lib` is new). REMAINS: (d) the run-count governor is DORMANT (DECISION S109-8) - REOPEN
  the moment a second prompt variant is activated; (e) the PENDING heading is proved in the deployed
  chunk and not yet on real data - it can show only between a main run and its debate, a morning
  window. LEADS folded here, not itemised: `/predictions` counts its tabs from the list and its tiles
  from the table, and labels the list "Latest 1000 Of"; the `/researcher` chart's scale. Claim-shaped
  leads - the medium and long columns no writer fills (CLM-554), `/developer`'s "All MAD predictions"
  (CLM-342) - belong to roadmap 4's review, not here.

"""

ITEM_35_OLD = "Two limitations, both written into section 6.5\n"
ITEM_35_NEW = "Two limitations, both written into section six\n"
ITEM_36_OLD = "Kin of **6.5** and of the Partner B"
ITEM_36_NEW = "Kin of the backup item archived at S110 and of the Partner B"

NOTE_31_ANCHOR = "- **3.1** WIDENED (S86) - COR. A constant confidence value on two dates.\n"
NOTE_31 = NOTE_31_ANCHOR + ("  NOTE (S110): the same constant appeared again in the S110 reads of the public pages. A lead,\n"
                            "  not re-measured as an item.\n")

LIFE_OLD = "**CLOCKS REMAIN PAUSED (DECISION S92-2).** 22 secrets stored."
LIFE_NEW = ("**CLOCKS REMAIN PAUSED (DECISION S92-2).** 24 secrets stored - two added at S110 for the backup\n"
            "(`SUPABASE_BACKUP_DB_URL`, `BACKUP_PASSPHRASE`; the passphrase is also held outside GitHub).")

ARCHIVED_HEAD_OLD = "## ARCHIVED - THREE ITEMS CLOSE INTO IT THIS GENERATION"
ARCHIVED_HEAD_NEW = "## ARCHIVED - THREE ITEMS AND ONE ROADMAP CLOSE INTO IT THIS GENERATION"
ARCHIVED_ROWS = (
    "| **ROADMAP 3 - CLAIMS** | **DECLARED ACHIEVED at the S110 close.** R3-1 at `f86febb`; R3-2 at `cf1742c`; "
    "R3-3 at `d0612e0`, `203e048`, `4b2b391`; R3-4 bound at S107, its prediction held at S108 and S109 (68, then 65, "
    "no arrival by `tools/gni_lambda.py`). Test 1, the replay, read FAIL on all three lines at S107 - the S68 tree "
    "on both status lines, the S91 tree on the binding line. Test 2, the agent test, PASSED on 2026-10-10: the "
    "answer was read from `docs/` alone and carried all five steps and both points left unresolved at S106. "
    "**Weakness, named:** James delegated the verdict and the answering session gave it, so the test graded "
    "itself (R-S110-3). A gap the answer found: the S92 records name only the Smart Desk; the name Smart Office first appears at "
    "the S96 close as roadmap 2's title, while the glossary credited it to DECISION S92-3 (its source column is "
    "corrected at this close). **The third roadmap this project has run to completion** - roadmap 1 at S96, "
    "roadmap 2 at S104; roadmap 2's archive row below calls itself the first, which the S96 record contradicts. Roadmap 4 was declared in the same close with its own completion test (DECISION S110-12). |\n"
    "| **6.5** there is no backup | CLOSED S110, open since S84. `.github/workflows/gni_backup.yml` at `57a5e83`, "
    "`462c3e9`, `980e876` (DECISIONS S110-10, S110-11): daily at 20:07 UTC, `pg_dump` of the public schema "
    "through a read-only role with BYPASSRLS, AES-256 under a passphrase also held outside GitHub, decrypted "
    "again and RESTORED into an empty Postgres 17 on every run, which must match the tables, every row count "
    "between the counts taken before and after the dump, the policies and the RLS tables. Run `38104487145`: "
    "RESTORE TEST PASS, 33 tables, 135672 rows, 18 policies; the artifact is kept 30 days. The offsite path was "
    "proven the same day: James downloaded the artifact, its sha256 matched, and HIS copy of the passphrase "
    "decrypted it to a 30546179-byte Postgres dump. Two red runs on the way, each a dump dependency the restore "
    "had not read (R-S110-2), and one false cert (R-S110-1). Left as they are: `public.profiles` holds 0 rows "
    "and references `auth.users` - the restore test fails red the day it holds a value, and dropping the "
    "table is a future ruling; the offsite copy is monthly and manual, prompted on Telegram. |\n"
    "| **9.11** the Groq daily-token figure | CLOSED S110 at `4d88eb2` (DECISION S110-8). Seven lines on seven "
    "pages stated 100K tokens a day as the provider's limit, which GNI never measured. Each now says it is "
    "GNI's planning limit, `TPD_HARD_LIMIT` in `quota_guard.py`, and the fitness function F-TPD reads that "
    "constant by AST, so the nine claims go DEFEATED the day it moves without them. The provider's per-model "
    "limit stays unmeasured and is claimed nowhere. The Supabase and Vercel provider figures on the same "
    "pages are left to roadmap 4. |\n"
    "| **9.12** the `/about/devops` quota gauge | CLOSED S110 BY MEASUREMENT at `21e03e4` (DECISION S110-9). The "
    "premise - a three-account SUM against a per-account ceiling - had been false since S55: the bar uses the "
    "worst account. Two real defects on the same gauge were fixed instead: 'Cost Today' had rendered '.00' "
    "since May (a shell ate the '$0'), and the 85K label sat in the middle of a bar whose 85K mark is at 85%. "
    "Both scale labels are derived: CLM-771 by F-TPD-SAFE, CLM-772 by F-TPD. |\n"
)

CHANGED = """## CHANGED THIS REGENERATION

- **PHASE TRANSITION (Part C step 4a).** ROADMAP 3 DECLARED ACHIEVED with its evidence, dated in
  ORIGIN and archived above; ROADMAP 4 declared with its written completion test in
  `GNI_ARCHITECTURE_S110.md`; every surviving item re-read against the target before this file was
  assembled (the note above ROOT 9).
- **DECISION S110-1 (James, delegated to the session).** The agent test's verdict was given by the
  session that answered: PASS. Weakness named in the ORIGIN line itself and in R-S110-3.
- **DECISION S110-2 (delegated).** F18: `/api/correlations` keeps the newest refresh only and names its
  population - over summing every snapshot (422 against 271 outcomes) and over showing two populations.
- **DECISION S110-3 (delegated).** F19: the route returns exact counts and the tiles say what "correct"
  meant - over relabelling a limited length.
- **DECISION S110-4 (delegated).** F16: one helper, `trendSeries()`, for both trend charts - over fixing
  `/researcher` by itself (R-S73-1, R-S55-1).
- **DECISION S110-5 (delegated).** 9.5(b): the `/alerts` empty state names what `health_alerts` holds.
- **DECISION S110-6 (delegated).** The `/comparison` panel reads the relation from the lib.
- **DECISION S110-7 (delegated).** 9.5(c): the escalation check widened and the verdict check added,
  each certified on three real commits.
- **DECISION S110-8 (delegated).** 9.11: the figure is labelled as GNI's planning limit and derived -
  over measuring the provider's limit, which only a forced 429 could do.
- **DECISION S110-9 (delegated).** 9.12 closed by measurement; the two real defects fixed.
- **DECISION S110-10 (delegated).** 6.5, design A: a dedicated read-only role and new secrets rather
  than the service key in `.env` (James asked for that), daily, 30-day artifacts, a monthly offsite
  download prompted on Telegram, and a restore test in every run.
- **DECISION S110-11 (delegated).** 6.5's foreign key, option A: an empty stub read from the dump's own
  DDL, and a red run if the referencing column ever holds a value - over carrying the auth schema in the
  backup and over dropping the empty `profiles` table, which stays a future ruling.
- **DECISION S110-12 (delegated - "your call").** Roadmap 4 is CLAIMS REVIEWED - over B, the free tier's
  cadence guarantees (ROOT 6), and C, the grounding gate (D3, ROOT 7). A was the lean. **That proposal
  carried no `LINEAGE:` line** - a WRONG entry, counted in the handoff.
- **DECISION S110-13 (James).** Continue after the mission: 9.11 and 9.12, then ROOT 6 for 6.5.
- **DECISION S110-14 (close judgement, not delegated; James may overrule).** No item opened. The
  public-page leads join 9.5; the claim-shaped leads go to roadmap 4's review; 3.1 gains a note.
- CLOSED 9.11, 9.12 and 6.5; 9.5 narrowed to two tails - OPENED none - count 62, ROOT 5 at 41,
  ORPHAN 47/62.
- **NOT ACTED, NAMED: 5.25's retire clause is due again** (DECISION S92-2 makes it James's).
- **SHIPPED** (eleven commits, each CI-green at job level and Vercel `success`, each product page
  live-read against a control): `0c57334` F18, `c3e5652` F19, `4b58cf3` F16, `fc68ff7` 9.5(b),
  `ddbb439` the `/comparison` panel, `b82a982` 9.5(c), `4d88eb2` 9.11, `21e03e4` 9.12, `57a5e83`,
  `462c3e9` and `980e876` 6.5 - the last two after red backup runs.
- **MEASURED**: claims 752 at 805 locations, COVERAGE 32/752, 0 DEFEATED, 415 never reviewed.
  `historical_correlations` holds every refresh since 2026-03-27 (84 rows; the newest, 2026-10-05, 260
  outcomes). `debate_predictions` held 1299 non-fossil rows on 2026-10-10. The backup: 33 tables,
  135672 rows, 18 policies, a 30546179-byte dump; one foreign key leaves the public schema.
- **FOUND IN THE TOOLS**: GitHub echoes a step's script into its log, so a grep of the log matched the
  source and certified a red run (R-S110-1). The S109 trap said the container's GitHub API calls were
  rate-limited; S110 found them access-limited.
- **COUNTER-CHECK OF ROADMAP 4 AGAINST THE PAST RECORDS, at James's request before the commit.** The
  roadmap 3 specification, the S96, S102 and S105 records and the fitness module were re-read. Four
  corrections, all folded in before this file was written: (1) R4-3 first read "no claim carries reason
  RUNTIME", which a review that never used the reason would pass - it now counts number-bearing page
  claims, 139 at S110; (2) `RUNTIME` IS defined, in `tools/gni_fitness.py`'s docstring - the OWED row
  now names the three reasons that are not; (3) a WITHDRAWN promise needs a DECISION of James's; (4)
  roadmap 3 is the THIRD roadmap completed, not the second - roadmap 1 was declared ACHIEVED at S96.
  Kept as written after the re-read: option A itself, which answers the question James asked at S102
  (where Smart Office stands, what remains) and the open half of D4. Added from S105: roadmap 4 has one
  instrument row and three reading rows, and from S112 every session moves a count.
- CONTRACT UNCHANGED (v11). PROTOCOL UNCHANGED (v21). Three rules and one further instance are in
  `GNI_RULES_S110.md`.

"""

MAINTAINED_OLD = "`tools/mk_close_s109.py`, which refuses on any disagreement, on an unbound item, on a binding\n"
MAINTAINED_NEW = "`tools/mk_close_s110.py`, which refuses on any disagreement, on an unbound item, on a binding\n"

# ------------------------------------------------------------------ RULES
RULES_BLOCK = """
## S110 ADDITIONS (2026-10-11)

- R-S110-1 - A CERT THAT READS A CI LOG MATCHES WHAT THE STEP PRINTED, NEVER WHAT IT RAN. GitHub
  writes a step's script into the step's log before its output. The first backup runner grepped the log
  for `RESTORE TEST PASS`, matched the `echo` line of the script itself, and printed BACKUP CERT PASS
  over a run whose job had failed. A cert requires the job's conclusion AND an output line anchored on
  the timestamp GitHub puts before printed text (`Z == RESTORE TEST PASS:`), and says which it read.
  **CHECKABLE: no** - it constrains how a runner reads a log.

- R-S110-2 - A LIST DERIVED FROM A GRAMMAR READS EVERY PLACE THE GRAMMAR CAN NAME THE THING. The
  backup's restore test read the roles a dump names after `TO` and `FROM`; the dump also names them
  after `FOR ROLE` (default privileges) and `SESSION AUTHORIZATION`, and names other schemas through a
  foreign key's `REFERENCES`. Each omission cost a red run against the real database - `auth`, then
  `supabase_admin` - while every local test passed, because the local source held only the forms the
  author had thought of. Before the first real run, list every production that can carry the name and
  read the live system for each one (S110 did it for policies, triggers, indexes and foreign keys only
  after the second red run).
  **CHECKABLE: no** - it constrains how a derivation is designed.

- R-S110-3 - A HUMAN-JUDGED TEST NAMES ITS JUDGE, AND THE JUDGE IS NOT THE SESSION UNDER TEST.
  Roadmap 3's agent test asked for James's verdict; James delegated it, and the session that answered
  wrote PASS about its own answer. The ORIGIN line says so, which keeps it honest, but the test graded
  itself. A completion test that rests on a human verdict states who gives it and that it may not be
  delegated to the session that answered; roadmap 4's Test 2 is written that way.
  **CHECKABLE: no** - it constrains how a completion test is written.

## FURTHER INSTANCE of R-S109-1 (read the structure, not a description of it)
9.12, written at S90 as [PROPOSED] with its render path never read, said the `/about/devops` bar
compared a three-account SUM; the bar had used the worst account since S55. S110 began F18 the same
way - assuming the route summed every row - and the route already deduplicated. Both were settled by
reading the code first. A queue item is a description too.
**CHECKABLE: no** - it constrains how a reading is done.
"""

# ------------------------------------------------------------------ ARCHITECTURE (born S110)
ARCH_TAIL_ANCHOR = ("- **ACHIEVED is NOT declared.** Four rows DONE and the replay recorded at S107; Test 2, the agent test,\n"
                    "  has never run. It is S110's mission (DECISION S109-9).\n"
                    "- **AGENT TEST**: not yet run.\n")
ARCH_TAIL = ARCH_TAIL_ANCHOR + r"""
### STATUS AT THE S110 CLOSE - ROADMAP 3 ACHIEVED

- **AGENT TEST: PASS**, 2026-10-10, one line in `docs/GNI_ORIGIN.md`;
  `grep -cE '^AGENT-TEST .* PASS ' docs/GNI_ORIGIN.md` prints 1. James delegated the verdict to the
  session that answered, so the test graded itself; the line says so (R-S110-3).
- **ACHIEVED, declared with its evidence** against the definition above - four rows DONE, the replay
  at least two of three FAIL, one AGENT-TEST PASS line: rows at S106 to S109, the replay three of three
  FAIL at S107, the agent test at S110. Dated in ORIGIN on the line below the agent test, and archived
  in generation 30 of the order.
- The claims document reads 752 claims at 805 locations, COVERAGE 32/752, **0 DEFEATED**; 415 claims
  have never been reviewed, and 139 number-bearing statements on the public pages are not derived. Those
  two counts are where roadmap 4 begins.
- Generation 30 holds **62** items: 9.11, 9.12 and 6.5 closed; none opened.

## ROADMAP 4 - CLAIMS REVIEWED (S111-), declared at S110 (DELEGATED)

**Status:** DECLARED at the S110 close, **DELEGATED** by James ("your call"), recorded as delegated per
CONTRACT's phase-transition clause (DECISION S110-12). Three options were put to him: A, claims
reviewed; B, the free tier's cadence guarantees (ROOT 6); C, the grounding gate (D3, ROOT 7). A was the
lean, and the proposal carried no `LINEAGE:` line, which the S110 handoff counts as WRONG. The lineage
was read after the choice, at James's request and before the close commit - the roadmap 3
specification, the S96, S102 and S105 records, the fitness module - and four corrections were made to
the rows below (listed in the order's CHANGED THIS REGENERATION).

**Target, unchanged:** TRUTHFULNESS OF OUTPUT. **Roadmap 4 in one line:** every claim GNI makes about
itself has been looked at - measured, given the written reason it cannot be, or retired with its copy -
and every promise has a state a reader can count.

**Why this one, from guidelines found before the analysis.** ISO/IEC/IEEE 15026-2:2022 builds an
assurance case from claims supported by argument and evidence; the claims document is that case's claim
layer, and 415 of its claims have never been examined for evidence at all. The NIST AI Risk Management
Framework's MEASURE function asks that trustworthiness be evaluated and that the effectiveness of the
measurement itself be evaluated and documented (MEASURE 2.13) - which a count the machine derives does
and a status typed by hand cannot. Roadmap 4 is also the half of definition-of-done line D4 that has
stood NOT DECLARABLE since S105, and it answers the question ORIGIN recorded as unresolved at S106: how
complete GNI is against what it set out to be.

### THE FOUR ROWS

Each row is answered by bytes, with the `passes` helper defined in ROADMAP 3 above.

| row | build | DONE when, from bytes |
|---|---|---|
| **R4-1** RATCHET | `tools/gni_claims.py` prints two derived counts on the claims document's STATUS line - claims UNREVIEWED, and NUMBERS UNDERIVED: STATE or MIXED claims with a location under `src/`, a digit in their text, not SUPPORTED, and no HISTORICAL or PROVENANCE reason; a check labelled `unreviewed ratchet` fails when either printed count differs from the derived one, or exceeds the count the previous claims generation printed | `passes 'unreviewed ratchet'` prints **1**; fixture families: one adds an UNREVIEWED binding (RED), one prints a count the tree does not derive (RED), one lowers a count (green) |
| **R4-2** REVIEW | each UNREVIEWED claim gets a fitness function in `tools/gni_fitness.py`, a reason from `UNMEASURED_REASONS`, or its copy retired | `grep -E '^\| CLM-[0-9]+ \| [A-Z]+ \| UNMEASURED \| UNREVIEWED \|' <live claims document> \| cut -d'\|' -f2 \| sort -u \| wc -l` prints **0** (415 at S110) |
| **R4-3** NUMBERS DERIVED (D4) | every number-bearing statement on a public page is SUPPORTED by a fitness function - one that reads a committed snapshot when the number is a runtime one (the RUNTIME limit in `tools/gni_fitness.py`'s docstring) - or its copy is relabelled as a plan or a request, or made count-free, as S108 did | the STATUS line prints NUMBERS UNDERIVED **0** (139 at S110) and `0 DEFEATED`; D4 then becomes declarable. Written this way, not as "no claim carries reason RUNTIME", because that form would pass on a review that simply never used the reason |
| **R4-4** PROMISE LEDGER | `docs/GNI_PROMISE_LEDGER_S<N>.tsv`: one row per PROMISE claim (204 at S110), state BUILT, PARTIAL, NOT BUILT or WITHDRAWN, with a path or a claim id as its evidence - and a WITHDRAWN row names the DECISION of James's that withdrew it, because a session may not retire a promise GNI made; a check labelled `promise ledger` fails on a PROMISE id with no row, a row with no evidence, or a BUILT row whose path is absent | `passes 'promise ledger'` prints **1**; the ledger's summary line equals its rows counted by state |

### COMPLETION TEST - for the roadmap

**Test 1 - the count moved.** The R4-2 command prints **415** on the S110 close tree, named by its commit
message so a history rewrite does not break it (`git log -1 --format=%H --grep='^S110 close'`), and
**0** on the tree that declares ACHIEVED. A roadmap whose count never moved cannot be declared by
relabelling.

**Test 2 - the completeness question, judged by James in person.** A fresh session given only the repo's
documents is asked verbatim *"how much of what GNI set out to be is built?"* - the question James asked at S102 in his own words:
where Smart Office stands and what remains. The answer must quote the
ledger's counts by state and name three NOT BUILT promises by claim id. JAMES gives the verdict himself;
it may not be delegated to the session that answered (R-S110-3). One line in ORIGIN:
`LEDGER-TEST <date> S<n> PASS|FAIL -- <reason>`. DONE: `grep -cE '^LEDGER-TEST .* PASS ' docs/GNI_ORIGIN.md`
prints **1 or more**.

**ACHIEVED** = four rows DONE + Test 1 + Test 2 PASS, declared with its evidence and dated in ORIGIN. If
not achieved, the reason is written down.

### OWED BEFORE THE ROW THAT NEEDS IT

| owed | needed by | why |
|---|---|---|
| `EXTERNAL`, `PROVENANCE` and `QUALITATIVE` defined in writing | R4-2 | the fitness module accepts all three and no comment says what any of them means (`RUNTIME` and `HISTORICAL` are defined there, `UNREVIEWED` too); a reason without a definition is a status typed by hand, and R4-3 lets HISTORICAL and PROVENANCE excuse a number, so those two must be exact |
| a snapshot a runtime fitness function may read | R4-3 | section six's runtime snapshot is the precedent; a fitness function that queried the live database would put a network call inside the deterministic detector, which S104 refused for the secret list |
| what "the previous claims generation" means | R4-1 | claims documents are session-numbered (S107 to S110); the next-lower number is the candidate, and a session that writes no claims document must not reset the ratchet |

### SEQUENCING AND SIZE

R4-1 at S111: the count first, as R3-4's baseline came first. R4-2 page by page, the densest first -
`/about/devops` 46, `/methodology` 42, `/developer` 33, `/developer-hub` 32 UNREVIEWED at S110. At forty
to eighty claims a session that is six to ten sessions; the estimate is a guess, to be replaced by the
ratchet's own slope after two sessions. R4-3 and R4-4 follow once R4-2's first pages show what the
reasons hold. **One instrument row, three reading rows, on purpose.** S105 measured the queue turning
inward - ROOT 5 grew from 11 to 42 items across S84-S104 while ROOT 9, the public copy, stood still for
eight generations. From S112 every roadmap 4 session moves one of the two counts or says why it did not.
"""

# Rows the S110 documents need: the check labelled `glossary` named exactly these on the assembled set.
GLOSS_SQL = "| SQL | the query language of the Supabase database |"
GLOSS_ROWS_DEFINED = (
    "| AES-256 | the Advanced Encryption Standard with a 256-bit key; the cipher the backup artifact is encrypted with, by gpg | `.github/workflows/gni_backup.yml` |\n"
    "| BYPASSRLS | the Postgres role attribute that lets a role read past row-level security; the backup role carries it and nothing beyond SELECT | `.github/workflows/gni_backup.yml` |\n"
    "| DDL | data definition language: the CREATE, ALTER and GRANT statements a dump carries; the restore test reads from them the roles and schemas it needs | `.github/workflows/gni_backup.yml` |\n"
    "| PGDMP | the five bytes that open every Postgres custom-format dump; the S110 offsite proof read them from the decrypted artifact | HANDOFF S110 |\n"
    "| RLS | row-level security: Postgres policies that decide which rows a role may read; the backup role reads past them with BYPASSRLS | `.github/workflows/gni_backup.yml`; ORDER |\n"
    "| NUMBERS UNDERIVED | the count printed beside UNREVIEWED from S111: STATE or MIXED claims with a location under `src/`, a digit in their text, not SUPPORTED and with no HISTORICAL or PROVENANCE reason; 139 at S110 | ARCHITECTURE, ROADMAP 4 row R4-1 |\n"
    "| NIST | the United States National Institute of Standards and Technology; its AI Risk Management Framework and SP 800-53 are cited by roadmap 4 and by the backup policy | ARCHITECTURE, ROADMAP 4; `.github/workflows/gni_backup.yml` |\n"
)
GLOSS_SO_OLD = "| Smart Office | the direction GNI took at S92: make the system's state visible from outside instead of rewriting the code | DECISION S92-3; `docs/GNI_ORIGIN.md` |"
GLOSS_SO_NEW = "| Smart Office | the direction GNI took at S92: make the system's state visible from outside instead of rewriting the code. S92 named it the Smart Desk (ARCHITECTURE section 4); the name Smart Office first appears at the S96 close, as roadmap 2's title | ARCHITECTURE, ROADMAP 2; `docs/GNI_ORIGIN.md` |"
GLOSS_SMART = "| SMART | first word of Smart Office, defined above |\n"
GLOSS_UNDERIVED = "| UNDERIVED | second word of NUMBERS UNDERIVED, defined above |\n"
GLOSS_R3 = "| `R3-\\d+` | a row of roadmap 3 (ARCHITECTURE, ROADMAP 3) |\n"
GLOSS_R4 = "| `R4-\\d+` | a row of roadmap 4 (ARCHITECTURE, ROADMAP 4) |\n"

ORIGIN_ANCHOR = ("Roadmap 3's agent test is recorded here as one line,\n"
                 "`AGENT-TEST <date> S<n> PASS|FAIL -- <reason>`, appended below this heading.\n")
ORIGIN_LINES = (
    "\nAGENT-TEST 2026-10-10 S110 PASS -- the answer was read from docs/ alone and carried all five steps "
    "and both points left unresolved at S106, matching the account James gave at S102; James delegated "
    "the verdict and the answering session made it, so the work graded itself. Gap found: the S92 records "
    "name only the Smart Desk; the name Smart Office first appears at the S96 close as roadmap 2's title, and "
    "the glossary credited it to DECISION S92-3, which does not name it.\n"
    "\nROADMAP-3 ACHIEVED 2026-10-11 S110 -- declared at the S110 close: its four rows were done by S109, "
    "the historical replay had read FAIL on all three lines at S107, and the agent test above had passed. "
    "Roadmap 4, claims reviewed, was declared in the same close.\n"
)


def main():
    if len(sys.argv) != 3:
        die("usage: mk_close_s110.py <repo-root> <outdir>")
    root, out = sys.argv[1], sys.argv[2]
    if not os.path.exists(os.path.join(out, "HANDOFF_S110.md")):
        die("HANDOFF_S110.md must already be in OUTDIR (written from the Part B template)")
    res = {}
    claims, live = claim_texts(root), live_claim_ids(root)

    o = rd(root, "GNI_TARGET_AND_ORDER_S109.md")
    if graveyard_md5(o) != GRAVEYARD_MD5:
        die("GRAVEYARD in the S109 order does not hash to its published value")
    o = sub1(o, HEADER_OLD, HEADER_NEW, "header")
    o = span(o, "## NEXT SESSION'S MISSION (S110)", "## TARGET - UNCHANGED", MISSION, "mission")
    o = span(o, "**ROADMAP 3 - CLAIMS - FOUR ROWS DONE; THE AGENT TEST IS ALL THAT STANDS BETWEEN IT AND ACHIEVED.**",
             "**DEFINITION OF DONE - RESTATED AT S105", TARGET_R, "target roadmap")
    o = sub1(o, D2_OLD, D2_NEW, "dod d2")
    o = sub1(o, D4_OLD, D4_NEW, "dod d4")
    o = sub1(o, D4B_OLD, D4B_NEW, "dod d4 count")
    o = sub1(o, "**EXPECTED ITEM COUNT: 65 distinct numbered items", "**EXPECTED ITEM COUNT: 62 distinct numbered items",
             "expected count")
    o = sub1(o, HEAD_OLD, HEAD_NEW, "order head")
    if o.count("docs/GNI_TARGET_AND_ORDER_S109.md \\\n") != 2:
        die("the two published scan commands are not both present")
    o = o.replace("docs/GNI_TARGET_AND_ORDER_S109.md \\\n", "docs/GNI_TARGET_AND_ORDER_S110.md \\\n")
    o = sub1(o, "Both must print **65**.", "Both must print **62**.", "both print")
    o = sub1(o, "`tools/mk_close_s109.py`, which refuses to write when they disagree",
             "`tools/mk_close_s110.py`, which refuses to write when they disagree", "head tool")
    o, ntags = strip_tags(o)
    if ntags != 65:
        die("expected 65 binding tags in generation 29, stripped %d" % ntags)
    o = span(o, "**ORPHAN RATE: 47/65**", "### ROOT 9 - PUBLIC COPY", "@@ORPHAN@@\n", "orphan block")
    o = span(o, "- **9.5** OPEN - COR - **THE S69 CENSUS, RE-READ AGAINST THE S109 TREE.**",
             "### ROOT 6 - FREE-TIER", ITEM_95, "9.5 rewritten, 9.11 and 9.12 out")
    o = span(o, "- **6.5** OPEN - COR - **THERE IS NO BACKUP.**", "- **6.3** RE-SPECIFIED (S89)", "", "6.5 out")
    o = sub1(o, ITEM_35_OLD, ITEM_35_NEW, "5.35 section citation")
    o = sub1(o, ITEM_36_OLD, ITEM_36_NEW, "5.36 kin")
    o = sub1(o, NOTE_31_ANCHOR, NOTE_31, "3.1 note")
    o = sub1(o, LIFE_OLD, LIFE_NEW, "lifecycle secrets")
    o = sub1(o, ARCHIVED_HEAD_OLD, ARCHIVED_HEAD_NEW, "archived head")
    o = sub1(o, "| what | why archived |\n|---|---|\n", "| what | why archived |\n|---|---|\n" + ARCHIVED_ROWS, "archived")
    o = span(o, "## CHANGED THIS REGENERATION", "## HOW THIS FILE IS MAINTAINED", CHANGED, "changed")
    o = sub1(o, MAINTAINED_OLD, MAINTAINED_NEW, "maintained")
    o, orphans, total = bind(o, claims, live)
    o = sub1(o, "@@ORPHAN@@\n", ORPHAN_NEW.replace("@ORPH@", str(orphans)).replace("@TOTAL@", str(total)), "orphan rate")
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
    res["GNI_TARGET_AND_ORDER_S110.md"] = o

    rl = rd(root, "GNI_RULES_S109.md")
    if "R-S110-" in rl:
        die("the S109 register already holds an R-S110 id")
    res["GNI_RULES_S110.md"] = rl.rstrip("\n") + "\n" + RULES_BLOCK
    res["GNI_Session_Transfer_Protocol_S110.md"] = rd(root, "GNI_Session_Transfer_Protocol_S109.md")
    res["CONTRACT_S110.md"] = rd(root, "CONTRACT_S109.md")
    ar = rd(root, "GNI_ARCHITECTURE_S109.md")
    if not ar.endswith(ARCH_TAIL_ANCHOR):
        die("the S109 architecture no longer ends with the S109 status block")
    res["GNI_ARCHITECTURE_S110.md"] = sub1(ar, ARCH_TAIL_ANCHOR, ARCH_TAIL, "architecture status")

    g = rd(root, "GNI_GLOSSARY_S110.md")
    if "| AES-256 |" in g or "`R4-" in g:
        die("the S110 glossary already carries the S110 close rows")
    g = sub1(g, GLOSS_SQL, GLOSS_ROWS_DEFINED + GLOSS_SQL, "glossary defined rows")
    g = sub1(g, GLOSS_R3, GLOSS_R3 + GLOSS_R4, "glossary roadmap 4 namespace")
    g = sub1(g, GLOSS_SO_OLD, GLOSS_SO_NEW, "glossary Smart Office source")
    g = sub1(g, GLOSS_SMART, GLOSS_UNDERIVED + GLOSS_SMART, "glossary not-an-abbreviation row")
    res["GNI_GLOSSARY_S110.md"] = g

    og = rd(root, "GNI_ORIGIN.md")
    if "AGENT-TEST 2026-10-10 S110" in og or "ROADMAP-3 ACHIEVED" in og:
        die("ORIGIN already carries the S110 lines - append-only, never twice")
    if not og.endswith(ORIGIN_ANCHOR):
        die("ORIGIN no longer ends at its APPENDED LINES heading text")
    res["GNI_ORIGIN.md"] = og + ORIGIN_LINES

    for name, text in sorted(res.items()):
        data = text.encode("utf-8")
        with open(os.path.join(out, name), "wb") as fh:
            fh.write(data)
        print("%-40s %7d bytes  md5 %s (EOL-normalised)" % (name, len(data), hashlib.md5(data).hexdigest()))
    print("WROTE %d files beside HANDOFF_S110.md. Sections five and seven, then the macro map, are regenerated next." % len(res))


if __name__ == "__main__":
    main()
