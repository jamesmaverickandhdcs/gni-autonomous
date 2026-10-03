# GNI TARGET + WORKING ORDER
**GENERATION 26 - 2026-10-03 (S106 close). SUPERSEDES generation 25
(`GNI_TARGET_AND_ORDER_S105.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S107)

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

## TARGET - UNCHANGED

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**ROADMAP 2 IS FOUR OF FOUR - ACHIEVED AT S104 AND ARCHIVED** (evidence in `GNI_ARCHITECTURE`).

**ROADMAP 3 - CLAIMS - ROW 1 OF 4 DONE AT S106.** Declared at S105 (DECISION S105-1, delegated).
R3-1 shipped at `f86febb` (CI `37069679116` green at job level): `docs/GNI_ORIGIN.md`, the
glossary, and the checks labelled `glossary` and `origin citations`; its fourth DONE line is met by
this close's handoff. The row's own text said a citation may resolve "to a session record or a
commit"; DECISION S106-2 narrowed that to sessions, because ORIGIN is never regenerated and the
declared history rewrite changes every hash. Rows, completion test and OWED list in
`GNI_ARCHITECTURE_S106.md`.

**DEFINITION OF DONE - RESTATED AT S105 (DECISION S105-9), each line with the command that answers it.**
S105 measured that two of the four lines could never be met: both sat on roots archived or blocked
while the lines stayed in the definition, so the target could not be declared achieved by
construction (R-S105-6). Each line is now stated in a form the work can reach and mapped to the
guideline it implements - ICD 203's analytic standards, EU AI Act Art. 50(4), and section ten's SLO.

| # | line | status at this regeneration |
|---|---|---|
| D1 | the arbitrator reads what it claims to read | DONE - certified S96, archived; no re-run owed |
| D2 | no public page shows the capped escalation score without its uncapped magnitude (ICD 203: express uncertainty, describe method) | MET AT S106 - every page formats the score through `src/lib/escalation.ts`, which prints the raw value beside it; the check labelled `escalation magnitude` refuses a page that formats it itself; read LIVE. Residual, itemised: three tables carry no raw column, so their rows point to the report instead (item 9.23) |
| D3 | the grounding gate measures reading, not existence | BLOCKED on item 7.1 - a line with no command is named as such, not hidden |
| D4 | every public statement of cadence, count or provenance is derived from a measurement or labelled as a request, and AI-generated text is labelled at first exposure | MET FOR THE KNOWN SET at S106 - the public-claims item closed, every claim it named read LIVE; whether the set is COMPLETE is what the claims harvest (R3-2) exists to say |

```bash
# D2 - prints 1. RESTATED AT S106: the S105 command counted FILES, could not see src/app/page.tsx
# (the pathspec needs a directory after src/app/), and listed pages that only declare the field.
python tools/gni_rule_checks.py | grep -cE '^\[PASS\] C[0-9]+ +\S+ +(escalation magnitude)'
# D4 - the bound half: prints 1
python tools/gni_rule_checks.py | grep -c '^.PASS. C7 '
```

## 🪦 GRAVEYARD — RULED-OUT DIRECTIONS (DECISION S88-2)

**COPY THIS SECTION INTO EVERY REGENERATION, VERBATIM. Never rewrite it from memory, never
drop it.** Protocol v8 PART C step 5 carries the same instruction, so the template cannot
delete it either. It exists because a design falsified in three seconds at S87 was first
proposed on 2026-06-01 and survived five sessions inside prose that nobody re-read.

| direction | killed by | evidence |
|---|---|---|
| **RECALIBRATE THE ESCALATION LEVEL** (Jun-01 option B; Mar-24 "Fix 2"; actor-tier; rupture-tier) | DECISION S87-2 | replayed n=192: Fix-2 gives 192/192 CRITICAL identical to production, actor-tier changes 0 runs, rupture-tier still 187/192. `tools/design_bench.py` re-proves this on EVERY run. |
| **FIX POLARITY BY EDITING A WORD LIST** (drop `ceasefire` from `GEO_SIGNALS`) | DECISION S88-3, S88 measurement | replayed n=196: **0 runs changed**, raw range/median identical. GEO hits min 8 / median 14 / max 19 against cap 5 — the pillar is cap-saturated, so ~half the 27-word list is arithmetically inert. R-S88-5. |
| **ROUND-ROBIN / PER-PILLAR ALLOTMENTS for the arbitrator budget** | DECISION S83-1, DECISION S85-1 | arrival is a CONSTANT not a share; coverage falls 14.4%→8.4% as volume rises, and the share is already stable at 62–65% of built. Ordering cannot raise coverage. The lever is per-article COST — shipped as `depth=0` (`228634c`). |
| **PER-SPEAKER GROUNDING BASKETS** (7.2 option C) | 2.1's standing law | fail-open is law; per-speaker baskets make the gate STRICTER and gates starve. |
| **RAISE THE ARB max_tokens FLOOR** to cure 413s | S80/S81 | the floor guarded the ANSWER side only; the prompt side exceeded the 8K per-request ceiling. Fixed by clamping context, not by raising the floor. |
| **DELETE `stage4_selected=False` ROWS TO RECLAIM STORAGE** (S89 proposal, killed the same session) | DECISION S89-4 | those rows ARE the XAI audit trail the March-2026 design built them to be — "every rejected article is visible with reason", the basis of the published "glass box / more transparent than industry systems" claim. Eight consumers in `src/`, including `/transparency`, `/history` and two API routes. Measured runway is ~550 days at 0.7 MB/day, so there is no capacity reason either. |
| **SWAP A PUBLISHED FIGURE FOR A FRESHER ONE WITHOUT ITS WINDOW** (S89's `6,175 → 16,144`, and S90's own first repeat of it) | DECISION S90-3, S90 measurement | `groq_daily_usage` holds TWO regimes: Mar/Apr/May `gni_pipeline` = exactly `6175` every month (a reservation constant, not a measurement), Jun 6,502, Jul 15,980, Aug 17,780. `16,144` was an average across the boundary and is reproducible from no window. The published figure must carry the window that produced it. |

**Reading this table is not optional before proposing anything in ROOT 8 or ROOT 1.**
A proposal that lands in this table without new measurement is a LINEAGE-BEV failure.

---
---

<!-- GRAVEYARD-END -->

<!-- GRAVEYARD-END -->

**md5 OF THIS SECTION, WITH THE COMMAND THAT PRODUCES IT (R-S96-2, R-S98-3, item 5.28):**
```bash
sed -n '/^## .*GRAVEYARD/,/^<!-- GRAVEYARD-END -->/p' docs/GNI_TARGET_AND_ORDER_S100.md \
  | tr -d '\r' | md5sum
```
Expected: `3e8ac222c6ef212261676c02d7d56f6f` - the SAME value generations 16, 17 and 18
published, verified against generation 18's bytes BEFORE this file was written and again
from this file's own bytes after (R-S95-1). See item **5.45** on the doubled end sentinel.

## THE CROSS-ROOT DIAGNOSIS (carried from generation 7 - now with eight instances)

> **GNI repeatedly measures what it has already guaranteed itself, and publishes the result as
> a fact about the world.**

| instance | what is measured | what it actually is |
|---|---|---|
| ROOT 7 | "the span exists in the pool" | reported as "the agent read it" |
| ROOT 8 gate | `_high_escalation` True six of six | a crisis channel that cannot leave crisis mode |
| ROOT 8 bonus | `diversity_bonus` at ceiling in most runs | the S39 funnel quota guarantees all three pillars |
| ROOT 8 GEO | GEO pillar "active" in every run | GEO hits far exceed the cap - the pillar cannot be inactive |
| ROOT 8 PHI | the PHI gate "protecting" the score | it has never fired; its own mute condition fires with it |
| S101 SLO | a published bound COMPARED against the measurement | any bound large enough passes forever; only a bound DERIVED by the check can fail |
| S102 fixture | sixteen families green on the standdown branch | `_snap_text` emits no run inside a protection window, so the branch was never entered |
| S103 `C6` | a check that resolved its own input from a stamp naming that same input | the INPUT pattern was built from the register's path, so the architecture line could never match |

Its use is predictive - when a metric is nearly constant, ask WHO GUARANTEED IT before tuning it.
The seventh instance was added this close; no earlier row changed.

**S99 NOTE - the S98 form of this diagnosis held again, four times, and once in the reverse
direction.** Three S98 instruments reported clean results about themselves; S99 produced four
more (R-S98-6's amendment lists them). The reverse case is new and worth the line: a measure can
also be bounded by the thing it measures, so it reports its SMALLEST possible answer exactly
where the truth is largest - a 365-minute lag read as 5 minutes (R-S99-1). Ask not only "who
guaranteed this constant" but "what is the largest number this instrument could ever return".

**S101 NOTE - the sixth instance is about a THRESHOLD rather than a metric.** The first draft
of the freshness check compared the published bound against the measured exceedance. That
passes for any bound large enough: a bound of one day would have kept the check green forever
while measuring nothing at all. The shipped check DERIVES the smallest whole hour that fits
the budget and fails when the published number is not that hour, in either direction, and the
cert proves it by flipping the bound one hour each way. Ask of any threshold: was this number
derived from the evidence, or chosen and then compared against it?

**S102 NOTE - the seventh instance is about a CONTROL PROBE.** The detector's fixture had sixteen
families and every one of them passed the day the standdown was removed. It could not have failed:
the synthetic run history starts at two in the morning, so no run ever fell inside a protection
window, so the branch that suppresses runs was never entered by any family. A green control probe
that never visited the ground it certifies is the same guarantee-then-measure shape one level
further in than S101's, and it is the most expensive one, because it is the instrument the other
instruments are checked against. Ask of any passing family: which branch did it actually enter?

**S103 NOTE - the eighth instance is about DIRECTION, not coverage.** `C6` was believed to read one
of two inputs because it hard-coded a count. It did not: it built its INPUT pattern by interpolating
the map's own `GENERATED from` stamp, and that stamp names the register by construction. The check
was aimed at a path it already knew rather than at what the document declares, so no number of
INPUT lines could ever have made it look at the second one. Widening a count would have changed
nothing. Ask of any check: is it reading what the artefact SAYS, or confirming what its author
already expected to find?

---

## THE ORDER

Every line carries an ISO/IEC 14764 class (DECISION S92-4): **COR**rective (something is broken),
**ADA**ptive (the world moved), **PER**fective (it works, it could be better), **PRE**ventive
(nothing is broken yet).

**EXPECTED ITEM COUNT: 70 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**
**CAP: 70 (DECISION S105-5; CONTRACT v11, WIP CAP).** The count may not grow across a regeneration,
and ROOT 5 may not exceed 42, unless James rules an exception in writing. Generation 25 held 70.
This close CLOSED one item and opened one, so the cap held with no exception. Closed and merged ids are not repeated here: a closed id cited in the queue counts as a
queue item. Every id is bolded so the published command is true of the file it sits in, and a
second differently-shaped scan is printed beside it to reconcile against (R-S98-6):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S106.md \
  | grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S106.md \
  | grep -oE '[0-9]+\.[0-9]+' | sort -u | wc -l
```

Both must print **70**. BOTH WERE RUN ON THE ASSEMBLED BYTES BEFORE THIS FILE WAS WRITTEN, by
`tools/mk_close_s106.py`, which refuses to write when they disagree with each other, with the number
above, or with the cap (R-S95-1). Item **5.51** - a control probe for the order generator - is
unchanged: this close's assembler is a different stand-in, not the probe.

### ROOT 9 - PUBLIC COPY AND REPORTED STATUS DRIFT FROM WHAT WAS MEASURED - URGENT - **TOP**

- **9.23** NEW (S106) [MEASURED] - COR - **THE CAPPED SCORE PINS EVERY CONSUMER OF THE LEVEL, AND
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
- **9.19** OPEN (S96) [PARTLY MEASURED at S98] - COR - DEGRADE-SILENT. A run in which `ctx-trim`
  leaves ZERO articles still reports SUCCESS. First byte evidence at S98 (`ARB-FIT: ctx_depth=0
  est=4997/5000`); still not the zero-article case. Next move: find a run at `ctx-trim@0`.
- **9.20** OPEN (S98) [PROPOSED, UNMEASURED] - COR. `mad_runner.py` prints `MAD skipped cleanly`
  and returns True. NOTE (S99): this is NOT the GitHub job-level `skipped` that R-S84-4's
  amendment describes; they look alike in a run list and are different doors. Do not conflate.
- **9.16** OPEN (S93) - COR. Records are from the `setup-python` side only. MERGED S105: the
  S94 item of the same shape, one generation later, is folded in here (DECISION S105-8).
- **9.18** OPEN (S95) - COR. Carried unchanged.
- **9.5** OPEN - COR. Eight unresolved S69 census flags; F14 renders BEARISH over a stale basis.
- **9.11** OPEN - COR. `research/page.tsx` publishes a Groq daily-token figure against a May record.
- **9.12** OPEN [PROPOSED, not measured] - COR. `/about/devops` compares a three-account token SUM.

### ROOT 6 - FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM - **RE-RANKED UP (S99)**

**RE-RANK, with the reason generation 18 owes for it.** This root sat below ROOT 5 for four
generations as a storage-and-backup root. S99 measured that it also holds a LIVE CAPABILITY GAP:
the two 30-minute crons deliver about a third of their declared slots, and the guarantee GNI
publishes about its own detection latency rests on the cadence that is not happening. That is
target-bearing, not housekeeping.

- **6.10** **NEW (S99)** [MEASURED] - ADA - **THE FREE TIER GIVES NO DELIVERY GUARANTEE, NOT
  MERELY NO TIMING GUARANTEE - AND THAT WAS NEVER MEASURED.** The ARCHIVED row "the lateness
  band" was archived because "a free-tier scheduler gives no timing guarantee". That reason
  understates it: R-S87-6's "zero runs missed" was measured over crons firing 1-3 times a day
  (S87 n=133, S91 n=8 slots) and is FALSE for the two firing 48 times a day. The delivery ratio
  is a distinct property with a distinct instrument, and the instrument now exists
  (`tools/gni_runtime.py`, the delivery table in section six). Derived lateness band: **744 min**.
  Un-archives the lateness row by measurement, per the ARCHIVED section's own condition.
- **6.5** OPEN - COR - **THERE IS NO BACKUP.** Still the highest single-point loss in the system,
  now for NINE generations, and never the mission. Said plainly rather than re-ranked again.
- **6.3** RE-SPECIFIED (S89) - ADA. Meter against tables; the difference is unexplained.
- **6.4** OPEN - ADA. L5 exposure when Supabase 402s. Paired with **5.30**.
- **6.13** **NEW (S101)** [MEASURED] - COR - **EVERY CADENCE FIGURE SECTION SIX PUBLISHES SPANS A
  REGIME BOUNDARY.** The delivery ratio, the median lateness and the derived lateness band are all
  averaged across a step change the generator itself warns about in its own prose. Section ten
  refuses those figures and publishes per-regime numbers with their windows instead, so the
  document now disagrees with itself between two sections. `C7` catches this shape in section ten
  and nothing catches it in section six. Same class as the GRAVEYARD's ruling on a window average.
  NOTE (S104): `C8` does not reach this either. `C8` asks whether section six's declared
  fingerprint matches the snapshot it read; it cannot ask whether the FIGURES derived from that
  snapshot are honest. Freshness and truthfulness are different properties and this item is the
  second one. See **5.59**, which is the same distinction found from the other side.
- **6.15** **NEW (S102)** [MEASURED] - PRE - **THE POLICY IS NARROWER THAN THE PROBLEM CLASS IT
  SERVES.** Section ten's policy fires when the freshness error budget is exhausted, and its
  corrective clause ranks a cause that IS ours above the next mission. The detector defect opened
  in ROOT 5 is the same disease one level up - a published claim that is untrue about GNI itself -
  and the policy cannot reach it, because the budget is NOT exhausted and the truthfulness of an
  instrument is not the freshness of a bound. **RULED at S102: the policy is NOT widened.** A
  trigger that needs judgment is a ruling wearing a policy's uniform. Recorded so a future clause
  is EARNED by first building the instrument that could fire it.

- **6.16** NEW (S105) [MEASURED] - ADA - `package.json` and `package-lock.json` DISAGREE on the major
  version of `@types/node`, so `npm ci` refuses with `EUSAGE` in a clean checkout (S105 container).
  `npm install` and `tsc --noEmit` pass, and Vercel built every S105 push, so nothing deployed is
  broken; the reproducible install path is.

### ROOT 5 - INSTITUTIONAL HARDENING

**NOTE ON THIS ROOT'S STANDING (S104).** It was "the roadmap's own root" for six generations. The
roadmap it served is finished and archived. Every item below therefore stands on its own merit
against the TARGET from this close forward, and none of them inherits priority from an arc that no
longer exists - Protocol PART C step 4a, which forbids inheriting a queue across a phase
transition. Nothing is inherited here; what is carried is carried because it is still true.

- **5.58** **NEW (S104)** [MEASURED, DISCLOSED AT SHIP TIME] - PRE - **SECTION SEVEN'S SECRET LIST
  IS AN INPUT THAT NO FINGERPRINT COVERS.** `C8` compares section seven's declared manifest md5
  against the workflow bytes, and that manifest hashes workflow files ONLY. The section also
  renders a stored-secret table read from `gh secret list`, whose source lies outside the tree and
  is unreachable from a harness that carries no secrets by design. A secret added or removed
  leaves the section stale against its source with its published fingerprint still green. DECISION
  S104-1 ruled this DISCLOSED rather than closed inside the mission, on two grounds: it is a
  configuration-IDENTIFICATION gap rather than the configuration-AUDIT gap row four tests, which
  are two distinct functions in IEEE 828; and closing it would have put a network call inside a
  deterministic tree-only detector, which fails RED for reasons that are not the subject. The fix
  shape is a GENERATOR change first - publish a fingerprint over the secret NAMES, never values -
  and only then can anything check it. Not a fifth surface: an input to a named one.
- **5.59** **NEW (S104)** [MEASURED] - COR - **NOTHING CHECKS PROVENANCE: ONE DOCUMENT MAY CITE
  TWO SOURCES FOR ONE NUMBER AND EVERY CHECK STAYS GREEN.** Found by a wrong prediction at S104 and
  worth more than the prediction was. `C8` was expected to go RED at `8ce57fc` because the S102
  record says section six was rendered from a stale snapshot there. It did not: at that commit the
  stamp and the live snapshot were BOTH the older generation, so liveness held and content matched.
  What `d9ebebb` actually fixed was different - section ten's prose and its embedded probe cited one
  snapshot while section six read another, inside one document. `C8` cannot see that shape at all,
  and neither can `C6`: both ask whether a declared fingerprint matches its source, never whether
  two sections agree about WHICH source. Kin of **6.13**, which is the same distinction reached from
  the figures rather than from the citations. The archived snapshot-stamps item closed at S102 is
  the other half of the evidence: its own closure message states the defect this item is about.
- **5.60** **NEW (S104)** [MEASURED] - ADA - **SECTION SIX WAS NOT REGENERATED AT S104, AND THE
  RE-HARVEST THAT WOULD REGENERATE IT NEEDS A RULING FIRST.** `gni_runtime.py` refused at the close:
  no snapshot exists for this session and `--harvest` is a separate act. It is DECLARED rather than
  skipped, and `C8` reports section six FRESH on its own terms - the stamp names the live snapshot
  and matches its bytes - which is exactly the distinction **5.59** is about. The blocking question
  is the standing UNKNOWN: does the published bound hold on a MOVED window? Moving the window
  carries SLO-3's regime rule with it and changes a published SLO, so it is a deliberate act with a
  ruling in front of it, never a side effect of a close. Two harvests three days apart already agree
  digit for digit on the frozen window `08-27 to 09-03`, so a re-harvest of THAT window measures
  nothing new.
- **5.52** **NEW (S102)** [MEASURED; NARROWED AT S104] - COR - **THE PUBLISHED REGENERATION ORDER
  CANNOT HOLD.** `gni_blocks` and `gni_state` count the INDEX but stamp HEAD, so running them before
  the mission commit writes the index's file list under a HEAD that predates the work. Both splice
  into the live architecture, so the map must run AFTER them or its architecture stamp is stale on
  arrival. **WHAT CHANGED AT S104, measured rather than assumed:** the CONSEQUENCE is now detected.
  A stamp that disagrees with the committed tree makes `C8` go RED on the CI run of the push that
  carries it, and a map stamped before the architecture makes `C6` go RED the same way - fixture
  family `19-map-stale-arch-md5`. **WHAT DID NOT CHANGE:** the generators still skew, and a check
  that reports a skew is not a generator that has none. Closing this item would claim the second.
  **CLOSURE TEST, written now so the next session does not re-derive it:** either a generator stamps
  the tree it counted, or a ruling is written that the skew is acceptable and the two checks are its
  mitigation. One of those two, in writing. Not before.
- **5.42** **NEW (S100)** [MEASURED; RULED AT S104, NOT YET SHIPPED] - PER - **`HEAD` IN A
  GENERATED STAMP IS DECORATIVE AND GOES STALE AT THE COMMIT THAT SHIPS IT.** All three generators
  stamp the short HEAD. Two options stood: drop it, or keep it and say in the stamp that it names
  the commit at RENDER time. **DECISION S104-1 chose the second, and it was already this project's
  ruling** - `d9ebebb` at S102 wrote that the one-commit lag between harvest and commit is what
  harvest-then-commit means, not a defect. S104 measured the consequence precisely: at `8ce57fc`
  the stamp names its own parent and is exactly right; four commits later at `a923ad9` the same
  stamp names a commit four steps back. **What is written and what is not:** the limitation is now
  recorded in row four of the completion test, with the reason a working-tree check cannot settle
  it. The STAMP ITSELF still does not say it, and that is the whole of what remains here.
- **5.35** **NEW (S99)** [MEASURED, DISCLOSED AT SHIP TIME] - PER - **`gni_runtime.py`'s PAIRING
  ASSUMES FIFO AND REFUSES AT THE WINDOW EDGE.** Two limitations, both written into section 6.5
  rather than left to be found: (a) ordered matching assumes the scheduler delivers slots in
  order, and MAD's two morning slots are 30 minutes apart against a 12-hour band, so an
  out-of-order delivery would mis-pair silently; (b) against a synthetic uniform 12-hour lag the
  pairing REFUSES with "a run BEFORE its slot at the window edge" even though delivery was
  complete. The failure direction is safe - NOT MEASURABLE rather than a wrong number - but it is
  a false negative. Fix: widen run collection past the window end without letting the previous
  day's runs leak in.
- **5.36** **NEW (S99)** [MEASURED] - PRE - **THE SNAPSHOTS HAVE NO RETENTION.** One runtime
  snapshot lands per session that harvests, each around 180 kB, and section six is regenerated
  every close. That is deliberate - the snapshot IS the evidence and must be in the tree for the
  byte-identity test - but nothing says when an old one may go. Kin of **6.5** and of the Partner B
  retention lesson: a stock grows, a flow does not. NOTE (S104): two snapshots now sit in `docs/`
  and the RELATION rule picks the higher, which `C8` depends on. Decide the policy before there are
  twenty, and decide it knowing a check now reads the newest one by construction.
- **5.30** OPEN (S98) [MEASURED] - COR. `_fetch_relevant_articles` returns an empty pool from
  three places and `run_mad_protocol` divides by its size. Written fail-open, behaves fail-hard.
  The policy question IS the item: what should MAD publish when it has no articles?
- **5.31** OPEN (S98) [MEASURED] - PRE. Model resolution has no floor; resolved at module import.
- **5.32** OPEN (S98) [MEASURED] - PER. `dryrun_two_account_split.py` sits at the REPO ROOT,
  outside the CI glob, exits 1, never read.
- **5.28** OPEN (S96) - COR. An unverifiable checksum. Practice continued this generation.
- **5.29** OPEN (S96) - PER. The register has six entry shapes. Load-bearing: `C6` reads it through
  the generator's parser. Appends since S99 have used the dominant shape without regularising.
- **5.21** OPEN (S94) - PRE. No `.gitattributes`. Unchanged, and it cost time again at S104: `git
  add` printed six LF-will-be-replaced-by-CRLF warnings at the mission commit. Harmless because
  every published hash in this repo is EOL-normalised (R-S98-3), which is the only reason the
  Windows tree and the Linux runner agree on section five's manifest md5 - proven at S104 by `C8`
  passing in CI on the same bytes it passed on locally.
- **5.20** PARTIALLY DISCHARGED (S94/S95) - PRE. Fixture at **25** families as of S104, up from 21.
  What remains is the control probe's own evidence.
- **5.22** OPEN (S95) [INSTANCE RE-HIT AT S104] - PER. Console fragility of `tools/*.py` on
  Windows. The instance this item already names - `python tools/gni_state.py --stdout` dying with
  `UnicodeEncodeError` on an arrow under cp1252 - was hit AGAIN at S104 and cost a false
  certification: two truncated renders compared clean. The item was already measured and already
  written down; what failed was reading a trap that named a DIFFERENT tool in the same family
  (R-S104-4). The fix is one line at import, as `gni_runtime.py` already has.
- **5.23** OPEN (S95) - PER. `C5`'s blind spot. NOTE (S104): confirmed live. `C5` rejects an
  integer literal above one inside a check function but cannot see a number inside a STRING, so a
  hard-coded count in a PASS message would pass its own lint. `C8`'s message derives its number,
  checked by grep at this close - but nothing enforces that.
- **5.24** OPEN (S95) - PER. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**
- **5.25** OPEN (S95) - PRE. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**
- **5.15** OPEN (S93) - PER. Selftest coverage.
- **5.16** OPEN (S93) [ONE INSTANCE MEASURED at S98] - PER. `__main__` blocks outside `tests/`.
- **5.18** OPEN (S93) - PER. Unread wrongness ledgers. Discharged by hand three times now: once
  when a session record ruled the standdown out as the cadence collapse's cause, again at S101 when
  the records returned four rule ids the register had lost, and again at S104 when the queue itself
  turned out to hold one defect under two numbers. Still no instrument.
- **5.19** OPEN (S93) - PER. R-S91-4's disproven evidence.
- **5.5** OPEN - PER. **PROMOTED INTO 5.56.**
- **5.6** OPEN - PER. **PROMOTED INTO 5.56.**
- **5.7** OPEN - PER. **PROMOTED INTO 5.56.**
- **5.8** OPEN - PER. **PROMOTED INTO 5.56.**
- **5.11** OPEN - PER. **PROMOTED INTO 5.56.**
- **5.12** OPEN - PER. **PROMOTED INTO 5.56, TEXT STILL UNRECOVERED.**
- **5.38** **NEW (S100)** [MEASURED] - ADA - **THE TREE CREATES ITS OWN PATH ROOTS, SO A FILE
  ANSWERS TO SEVERAL NAMES.** Tracked modules call `sys.path.append` or `sys.path.insert` from
  many places, published in ARCHITECTURE section five's path-roots subsection. Consequence:
  `ai_engine/analysis/mad_protocol.py` is imported as `analysis.mad_protocol`, never by the
  `ai_engine.` prefix, and the same file also answers to a bare `mad_protocol`. This is not a
  style note - it is why the FIRST version of `gni_blocks.py` reported three internal edges and
  zero test coverage, both impossible, and it will break the next reader that assumes
  package-relative names. No fix is proposed here: consolidating the roots is a large refactor
  with a real regression surface, and the item exists to make the cost visible and RULED rather
  than rediscovered. A decision is wanted before any import is touched.
- **5.39** **NEW (S100)** [MEASURED] - PRE - **MOST NON-TEST MODULES ARE IMPORTED BY NO TEST
  MODULE, AND NEARLY HALF THE TESTS IMPORT ONLY `mad_protocol`.** ARCHITECTURE section five's
  test-import table. Coverage here means one thing only - a test names the module in an import -
  so the true figure is not better than this and may be worse. This compounds the standing item
  that the assertions under `ai_engine/tests/` have never been run in CI: a test that is neither
  run nor imports what it claims to test is two failures, not one.
- **5.40** **NEW (S100)** [MEASURED] - PER - **A STANDING TABLE OF MODULE-LEVEL SYMBOLS READ
  NOWHERE, AND MODULES IMPORTED BY NOTHING.** The two no-static-reference tables in ARCHITECTURE
  section five. This is the class that produced DET-DEAD and `_FORCE_PROVIDER` five months apart,
  both found by accident. It is NOT a deletion list - pytest finds `test_*` by name, and a module
  can be reached by a workflow entrypoint. The work is a TRIAGE: join the unreferenced-module table
  against section seven's entrypoint column, subtract pytest discovery from the lonely-symbol
  table, and rule on the remainder. Do not delete anything before that join exists in writing.
- **5.43** **NEW (S100)** [MEASURED] - PRE - **`gni_state.py` HOLDS A HAND-WRITTEN PROBE COUNT.**
  Its control probe prints a pass tally as a literal. It is CORRECT TODAY and that is the whole
  danger: it is right by coincidence and unprotected against the next probe added. This is the
  pattern `C5` and R-S81-5 forbid inside the detector, and `gni_runtime.py`'s own docstring records
  that this same literal was once wrong by one when counted. Fix shape: count the failures, as
  `gni_blocks.py` and `gni_runtime.py` both do. Still unfixed at S104, and now the only
  hand-written instrument count left in `tools/`.
- **5.44** **NEW (S100)** [MEASURED] - COR - **`gni_state.py` PROMISES EXIT CODES IT DOES NOT
  DELIVER ON TWO PATHS.** Its docstring lists three. `main()` calls `splice(src.read_text(...))`
  with no `is_file()` guard and no `except ValueError`, so a mistyped `--src` and a document
  missing the section-seven boundary both die with a traceback and exit 1. `gni_runtime.py` guards
  both. Same class as the standing item about an exit code absent from its own docstring, and kin
  of **5.22**, whose instance produces exactly such an unlisted exit.
- **5.45** **NEW (S100)** [MEASURED] - PRE - **THE GRAVEYARD CARRIES A DOUBLED END SENTINEL.**
  `<!-- GRAVEYARD-END -->` appears twice, and the rule above it appears twice. The published md5
  covers only through the FIRST sentinel, so the value is stable today; but any future copy that
  bounds the section differently silently produces a different hash for the same seven rows. Do NOT
  quietly delete the duplicate: five generations now publish the same value, and removing bytes
  inside the hashed region breaks a number those generations carried. The fix is a ruling on which
  boundary is canonical, then one deliberate re-baselining that says so. NOTE (S104): the assembler
  that wrote this generation implements the FIRST-sentinel boundary in code, so the ambiguity is
  now encoded in a tool as well as in prose. That raises the cost of ruling the other way.
- **5.47** **NEW (S101)** [MEASURED] - PRE - **ONE-SHOT PATCH SCRIPTS HAVE NO POLICY, AND THE TREE
  CURRENTLY SAYS BOTH THINGS.** Four S95 one-shot scripts are committed under `tools/`; S100's
  order generator was deleted after use, and S101 deleted four more. Whichever answer is right, the
  committed ones sit inside section five's module count and its dead-surface census forever, and
  the deleted ones cannot be re-run to reproduce their own output. NOTE (S104): this item has now
  produced a measured consequence rather than a hypothetical one. `patch_s103_row4.py`, committed
  at S103, is the single file that moved section five's manifest and made its stamp false; S104
  committed four more patch scripts. A ruling, then one sweep.
- **5.48** **NEW (S101)** [MEASURED] - PRE - **THE HARVEST CAP SPANS THE SLO WINDOW TODAY AND WILL
  NOT IF DELIVERY RECOVERS.** `gni_runtime.py` caps the harvest at three hundred runs. At the
  current rate that is about two months of heartbeat history; at the rate before the break it is
  about nine days, and a fortnight-long window would truncate silently. `C7` raises an instrument
  error rather than a pass when the snapshot cannot span the published window, so the failure is
  loud - but nothing PREVENTS it, and it appears only when things get BETTER.
- **5.49** **NEW (S101)** [MEASURED] - PRE - **"ROW FOUR" NAMES TWO DIFFERENT ROWS.** The roadmap
  table's fourth row is the session that ships the SLO; the completion test's fourth row is the one
  about staleness. The S100 handoff used both senses in a single sentence. NOTE (S104): the second
  sense is now CLOSED and the first is not, so the ambiguity is more dangerous rather than less -
  a reader who resolves "row four is done" to the wrong row concludes the SLO session shipped.
  Cheap to fix, and exactly the ambiguity that produces a wrong claim at a close.
- **5.51** **NEW (S102)** [RE-SPECIFIED AT S104] - PRE - **THE ORDER GENERATOR IS IN THE TREE FOR
  THE FIRST TIME, AND IT IS STILL A STAND-IN.** The S101 close credits `tools/mk_order_s101.py`
  with running both published counting commands on the assembled bytes before writing; that file
  never entered the repo, and generations 22 and 23 were assembled by scripts written at the close
  and thrown away. **What changed at S104:** `tools/mk_order_s104.py` is committed, so the next
  close reads a program rather than a description of one. **What did not:** it has no control probe.
  It verifies the graveyard md5, both counts and the closed-id rule, but nothing verifies that those
  verifications can FAIL - which is R-S93-1 applied to the tool that writes this file. Rebuilding it
  properly is still a session with a control probe, not a close-time chore, exactly as this item has
  said since S102.
- **5.53** **NEW (S102)** [PROPOSED, not measured] - PRE - **NO ONE KNOWS WHICH BRANCHES THE
  FIXTURE EXERCISES.** The sixteen families that existed before S102 never entered the window branch
  of the detector's gap calculation: the synthetic history starts at two in the morning, so no run
  ever fell inside a protection window. Two families fixed that ONE branch. Whether any other branch
  of any other check is equally unvisited has never been asked. NOTE (S104): four more families
  shipped, and the same question travels with them - each was written for a failure shape its author
  named, which is the same method that left the window branch unvisited for sixteen. A coverage read
  of the fixture against the detector is the measurement, and the answer decides whether this is one
  defect or a class.
- **5.55** **NEW (S103)** [MEASURED] - PRE - **NO CHECK WATCHES THE ORDER-ITEM NUMBERS THAT LIVE
  DOCUMENTS CITE.** `C1` verifies that every RULE id cited by a live document is registered, by four
  id schemes. Order item numbers are a fifth scheme and are checked by nothing. This is load-bearing:
  row four of the completion test inside `GNI_ARCHITECTURE` cites an order item by number, and if
  that number drifted the architecture would cite an item that does not exist while every check in
  the repo stayed green. NOTE (S104): row four now cites a SECOND item number, so the exposure
  doubled at the close that closed the row. The shape of the fix is `C1` generalised, which is also
  what the roadmap 3 specification proposes for abbreviations - one check, several id schemes, one
  register each.
- **5.56** **NEW (S103)** [MEASURED] - PER - **THE RETIRE-CLAUSE DEBT ON SIX ITEMS, PROMOTED INTO
  WORK RATHER THAN CARRIED AN EIGHTH TIME.** Generations 16 and 17 replaced the six items' text with
  the bare line "Carried unchanged from generation 15", so the live order has not stated what they
  ARE since. Generation 18 recorded the debt and named the remedy - read their full text out of
  `GNI_TARGET_AND_ORDER_S95.md` and close or promote each in writing - and assigned it to S100. Four
  closes carried it unpaid. S103 established why: **it is not a close-time chore.** It needs an old
  file opened, six items recovered, and six rulings made. Partial recovery at S103 from that file:
  **5.5** is `DEBT_REGISTER_S69.md` and its one reader in five months; **5.6** is PARTLY PAID at
  S90, the register's PART 1 and PART 2 restructure; **5.7** is BYTE-CONFIRMED at S88, `_lower` and
  `_upper` still rendering a placeholder on `/autonomy`, which is a PUBLIC page and therefore ROOT
  9's subject rather than this root's; **5.8** is unnumbered items being invisible to the uniqueness
  assert; **5.11** is the dead-symbol and unwired-module CI detector, which S91 converted and which
  that file says was NOT a retire candidate. **5.12 HAS NO TEXT IN `GNI_TARGET_AND_ORDER_S95.md` AT
  ALL** - not merely compressed, unrecovered, and the earlier generation that holds it has not been
  found. Closing any of the six from these fragments would be R-S98-1's disease, so none is closed.
- **5.57** **NEW (S103)** [MEASURED] - COR - **`C1` DID NOT SEE A DANGLING ID INSIDE THE REGISTER
  ITSELF.** `GNI-R-118` is cited as law by `ai_engine/monitoring_pipeline.py` and in the register's
  own prose in the S102 `GNI-R-122` amendment. It is defined nowhere and was in no manifest. `C1`
  went RED at the S103 close only when the HANDOFF and the order cited it too - one generation after
  the register began citing it. Either `C1` exempts the register from its own scan or the citation
  form differs; the cause is UNMEASURED and settling it is this item. Two consequences travel with
  it, and both are bigger than the id. The register is the document most likely to cite ids, so an
  exemption there is an exemption where it matters most. And `C1` reads live DOCUMENTS only -
  `ai_engine/` cites rule ids in comments and nothing verifies them, which is how this one sat
  unregistered for months while every check stayed green. Manifested as `DANGLING-LAW`.

### ROOT 7 - THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" - IMPORTANT

- **7.1** PARTLY PAID (S86) - COR. `checked_spans` computed and discarded at the print.
- **7.2** BLOCKED - COR. Fix shape undecided; per-speaker baskets are in the GRAVEYARD.
- **7.3** PARTLY DISCHARGED (S86) - PER. Unchanged.
- **7.4** OPEN (S93) [UNMEASURED] - COR. `GROUNDING SHADOW` counts disagree across instruments.

### ROOT 2 - LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE - IMPORTANT

- **2.1** HALF-RULED (S86) - COR. Clause two, LABELED coverage, unmeasured.
- **2.2** BLOCKED on **2.1** - PER.
- **2.3** NARROWED (S87) - PER.
- **2.4** ONE READ FINISHES IT - COR. `/stocks` may render frozen prices.

### ROOT 3 - FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE - IMPORTANT

- **3.1** WIDENED (S86) - COR. A constant confidence value on two dates.
- **3.2** OPEN - ADA. `data_era` column plus tagging.

### ROOT 4 - COST AND HEADROOM - IMPORTANT

- **4.1** OPEN - COR. C2 solver recalibration; **9.19** carries the first log line.
- **4.4** OPEN - PER. Measure chars per token PER POSITION.
- **4.6** OPEN (S90) - ADA. `gni_mad` monthly token draw rose through the summer.

### LIFECYCLE + SECURITY - target-independent, never ranked away

**CLOCKS REMAIN PAUSED (DECISION S92-2).** 22 secrets stored. Nothing is due, nothing is overdue,
and no session may raise an item here as "overdue" until James restarts the clocks.

---

## ARCHIVED - ONE ITEM CLOSES INTO IT THIS GENERATION

Archived is not closed and not solved: not worked under this target, not re-ranked each close,
not re-read at open. Anything here returns only by a new measurement and a ruling.

| what | why archived |
|---|---|
| **9.22** the public surface's unmeasured claims and query-limit counts | CLOSED S106 in all three parts, each read LIVE on the new build after the deployment reported `success`, each proved with a rendered literal grepped in the minified bundle. (c) DoD D2 at `7403921` + `cd27f88`: one lib, one check, home rank and trend moved to the raw value because capped ties had made every run "top 0%". (b) at `591f218` + `a52bba0`: counts from the run table, exact; the correction commit exists because the fix itself printed a limited length as a count (R-S106-3). (a) at `ac284a2`: dated section-6 constants replace "twice daily", "24/7", "Always On", "Real-time" and "may fire 2-3 hours late" (measured: median 260 min, max 727 min). "The system fixes itself", listed by the S105 text, had already been removed at S105. |
| **9.21** the freshness promise on public pages | CLOSED S105 at `867ea5b`. Read LIVE on the new build after the deployment reported `success`: every predicted cell matched, twenty of twenty. The bound reaches the pages through ONE constant that `C7` compares with SLO-CFG, so a moved bound reddens the detector until the pages follow. The one statement the read could not see sits in an empty-state branch and is fixed in source. |
| **9.17** the S94 twin of the `setup-python` record item | MERGED S105 into its S93 original (DECISION S105-8): its own text said "same shape, one generation later". |
| **ROADMAP 2 - INSTITUTIONAL HARDENING** | **DECLARED ACHIEVED at the S104 close, four of four.** The completion test in `GNI_ARCHITECTURE` holds on every row, each answerable from bytes by the command beside it. Row one: a no-code-change push reaches `success` on both jobs. Row two: each generated section regenerates byte-identically on an unchanged tree. Row three: section ten carries a written SLO with an error budget and measured values with their commands. Row four, the last and the only one that ever failed: `rule_checks` exits 0 on a clean tree and RED on all four surfaces it names. Evidence `693ac2b` and `bc88bd8`, CI `34423999423` green at JOB level, twenty-five fixture families with no mismatch. **This is the first arc this project has run to completion.** SUBPAGE-IC died by being renamed near its end and never declared; this one was declared, dated and measured. The next roadmap is James's to declare with its own completion test, at S105 (DECISION S103-2). |
| the staleness check for sections five and six | CLOSED S104 at `693ac2b` + `bc88bd8`, CI green at job level. Opened TWICE, at S100 and again at S103, in different words - the same defect under two numbers, and neither session searched the queue for what it already held. Both ids close here. `C8` resolves every `**GENERATED by ` + "`tools/`" + ` stamp the architecture declares to a fingerprint RULE keyed by the generator that wrote it, then recomputes that fingerprint from the live tree using the generator's OWN code (R-S96-3) - `gni_state.workflow_manifest` was lifted out of `main()` to make that possible, and section seven renders byte-identically before and after, certified from two worktrees of ONE commit because the generator names itself by `__file__` and a renamed copy is a different document (R-S104-3). No count of sections is written anywhere; `C5`'s own lint proves it. Fixture families `22-sec5-stale-manifest`, `23-sec6-snapshot-renamed` (liveness, no md5 in the message), `24-sec7-workflow-edited` (the DISCRIMINATOR against `C2`: bytes move, counts do not) and `25-arch-unknown-generator` (instrument error, so a fourth generated section must announce itself). CERTIFIED on two REAL commits with ONE instrument: `8ce57fc` exits 0, `a923ad9` exits 1 naming the live md5 against the stamped one - on a **byte-identical** section five stamp, md5 `e1c9488b9df1f5d61f0596a227cc602f`, so the verdicts came from the trees and not from the document. Measured across twenty-four commits: section five's declared value disagreed with its tree at ELEVEN of them, and the nine that agreed did so because no tracked module moved in those sessions. |
| **ROOT 1** | CERTIFIED for content and ordering (S96). |
| **ROOT 8** | discharged in part at S91; the rest waited five generations under a target it does not serve. |
| the published band table | wrong in two of five rows - real, measured, and no longer blocked by roadmap 2. |
| the dependency manifest | a roadmap-2 by-product. Note (S99): `GNI_ARCHITECTURE` section 7.3 cites an item in the six-range that this order does not carry - a dangling item citation, the order-file twin of what `C1` checks for rule ids. That number is therefore NOT reused. The exact id is in `GNI_ARCHITECTURE` section 7.3, deliberately not repeated here so the count commands stay true. |
| `mad_runner.py` unordered `limit(50)` | kin of R-S92-2, no consumer waiting. |
| **5.33** section 7's own clock | CLOSED S100 at `3268c14`. The stamp carries HEAD, the workflow file count and an EOL-normalised manifest md5; byte-identical on two renders two seconds apart, and the md5 MOVES when a workflow changes. S104 note: that last property is now a fixture family and a check, not only a claim. |
| **5.34** `--session` default | CLOSED S100 at `3268c14`. Now required; a bare invocation exits 2. |
| **5.37** two unregistered rule ids | CLOSED S101 at `3b3b54a`. Four March-2026 ids recovered VERBATIM from four independent session records and confirmed by their own id citations inside `ai_engine/monitoring_pipeline.py`, then registered in PART 0. |
| **5.50** `C6` read one of two inputs | CLOSED S103 at `6c05076` + `60af1a5`. `C6` loops over every `INPUT ... md5` line the map declares, resolves each to the LIVE file of its family and compares path AND content. The defect was never a hard-coded two: the INPUT pattern was interpolated from the map's own stamp, which names the register by construction. |
| **6.11** the promise and the cadence disagree | CLOSED S101 at `b7eaab4`. ANSWERED rather than fixed: GNI has two cadences and not one, both published per regime with their windows, and `C7` fails when the written number stops being true. |
| **6.8** heartbeat standdown | CLOSED S101 at `b7eaab4` WITH ITS ROOT CAUSE. |
| **6.12** the watcher that checks nothing | CLOSED S102 at `9e11f57`. The published bound FELL from 12 h to 8 h, derived by `C7`, and `C7` no longer assumes the standdown exists. Certified by families `17-standdown-absent` and `18-standdown-reinstated`, differing by one call and by nothing else. |
| **5.46** the roadmap's stale scoreboard | CLOSED S102. The completion test was re-run for the first time since S98 and rewritten from bytes. A scoreboard nobody re-runs is a claim, not a measurement - which is why it was closed by reading rather than by building, and why the roadmap it scores could finish two sessions later. |
| **6.14** the snapshot's three stamps | CLOSED S102 at `d9ebebb`. Section six generated from the S102 snapshot, harvested that session. The one-commit lag between harvest and commit is what harvest-then-commit means, not a defect - the ruling DECISION S104-1 cites rather than re-derives. Its closure message is also the evidence for item **5.59**. |

**LEFT THE ARCHIVE THIS CLOSE: nothing.** The band table's blocker is gone with roadmap 2, but a
removed blocker is not a new measurement and the ARCHIVED section's return condition is unchanged.

`docs/GNI_RULE_CHECKABILITY_S95.tsv` remains RETIRED (S96) - on disk, out of the queue.

## CHANGED THIS REGENERATION

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

## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped - this generation's copy was hashed with the
published command's boundary BEFORE the file was written. The item count carries two commands
beside it, and both - plus the CAP - are checked on the ASSEMBLED bytes before the write by
`tools/mk_close_s106.py`, which refuses on any disagreement. Item **5.51** still asks for a control
probe; this assembler is not one.
Freshness confers no priority: an item found today does not outrank an item found in June unless
a measurement says so. Under the cap it also cannot enter without something leaving.
