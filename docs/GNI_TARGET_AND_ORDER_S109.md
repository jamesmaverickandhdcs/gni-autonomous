# GNI TARGET + WORKING ORDER
**GENERATION 29 - 2026-10-04 (S109 close). SUPERSEDES generation 28
(`GNI_TARGET_AND_ORDER_S108.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S110)

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
## TARGET - UNCHANGED

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**ROADMAP 2 IS FOUR OF FOUR - ACHIEVED AT S104 AND ARCHIVED** (evidence in `GNI_ARCHITECTURE`).

**ROADMAP 3 - CLAIMS - FOUR ROWS DONE; THE AGENT TEST IS ALL THAT STANDS BETWEEN IT AND ACHIEVED.**
Declared at S105 (DECISION S105-1, delegated). R3-1 at S106. R3-2 at `cf1742c`. R3-3 at `d0612e0`,
`203e048`, `4b2b391`. R3-4 bound at S107; DECISION S107-8 judged it on the queue over S108 and S109:
68, then 65 - five departures and no arrival - so the prediction HELD at both closes. Rows, completion
test and the S109 status in `GNI_ARCHITECTURE_S109.md`. ROADMAP CHECK (Part C step 4a): roadmap 3,
rows four of four; ACHIEVED waits on Test 2 alone.

**DEFINITION OF DONE - RESTATED AT S105 (DECISION S105-9), each line with the command that answers it.**
S105 measured that two of the four lines could never be met: both sat on roots archived or blocked
while the lines stayed in the definition, so the target could not be declared achieved by
construction (R-S105-6). Each line is now stated in a form the work can reach and mapped to the
guideline it implements - ICD 203's analytic standards, EU AI Act Art. 50(4), and section ten's SLO.

| # | line | status at this regeneration |
|---|---|---|
| D1 | the arbitrator reads what it claims to read | DONE - certified S96, archived; no re-run owed |
| D2 | no public page shows the capped escalation score without its uncapped magnitude (ICD 203: express uncertainty, describe method) | MET AT S106 - every page formats the score through `src/lib/escalation.ts`, which prints the raw value beside it; the check labelled `escalation magnitude` refuses a page that formats it itself; read LIVE. Residual CLOSED S109: `frequency_log` carries the raw value, certified (18.4, 21.5); `health_alerts` never stored the escalation and the block that read it is gone; `historical_correlations` keeps a capped average labelled as capped (DECISION S109-2) |
| D3 | the grounding gate measures reading, not existence | BLOCKED on item 7.1 - a line with no command is named as such, not hidden |
| D4 | every public statement of cadence, count or provenance is derived from a measurement or labelled as a request, and AI-generated text is labelled at first exposure | BOUND HALF MET AT S108, HELD AT S109 - `claim status derived` prints 0 DEFEATED from `7cfc1d2` through `c78c288` (9.24, nine claims made true). NOT DECLARABLE: 727 of 748 claims are UNMEASURED, and the check speaks only for what is bound |

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

**EXPECTED ITEM COUNT: 65 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**
**CAP: 70 (DECISION S105-5; CONTRACT v11, WIP CAP).** The count may not grow across a regeneration,
and ROOT 5 may not exceed 42, unless James rules an exception in writing. Generation 28 held 68.
This close CLOSED three items and opened none, so the count FELL to 65. Closed and merged ids are not repeated here: a closed id cited in the queue counts as a
queue item. Every id is bolded so the published command is true of the file it sits in, and a
second differently-shaped scan is printed beside it to reconcile against (R-S98-6):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S109.md \
  | grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S109.md \
  | grep -oE '[0-9]+\.[0-9]+' | sort -u | wc -l
```

Both must print **65**. BOTH WERE RUN ON THE ASSEMBLED BYTES BEFORE THIS FILE WAS WRITTEN, by
`tools/mk_close_s109.py`, which refuses to write when they disagree with each other, with the number
above, or with the cap (R-S95-1). Item **5.51** - a control probe for the order generator - is
unchanged: this close's assembler is a different stand-in, not the probe.

**ORPHAN RATE: 47/65**

BINDING (roadmap 3 row R3-4, from generation 27). Every item's defining line ends in
`{claims: CLM-###, ...}` - the public claims it serves, ids from `docs/GNI_CLAIMS_S109.md` - or
`{ORPHAN}`. The check labelled `order bound to claims` derives the rate above from those tags and
fails when the two disagree, when an item carries no tag, or when a tag names an id never minted. An
ORPHAN serves no claim the public surface or the White Paper makes; under the claims model it is the
first candidate to leave. The binding is a judgement made at the S107 close and re-made at S109: 9.5
now serves CLM-692 and CLM-693, the two empty-state sentences its remainder carries; the rate is derived.

### ROOT 9 - PUBLIC COPY AND REPORTED STATUS DRIFT FROM WHAT WAS MEASURED - URGENT - **TOP**

- **9.19** OPEN (S96) [PARTLY MEASURED at S98] - COR - DEGRADE-SILENT. A run in which `ctx-trim` {claims: CLM-170}
  leaves ZERO articles still reports SUCCESS. First byte evidence at S98 (`ARB-FIT: ctx_depth=0
  est=4997/5000`); still not the zero-article case. Next move: find a run at `ctx-trim@0`.
  S109 read two more debates (`37190098951`, `37110117798`): `ctx-trim@5121` and `@4930` - characters
  of context kept, never zero.
- **9.5** OPEN - COR - **THE S69 CENSUS, RE-READ AGAINST THE S109 TREE.** The open registry in {claims: CLM-692, CLM-693}
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
- **9.11** OPEN - COR. `research/page.tsx` publishes a Groq daily-token figure against a May record. {claims: CLM-538}
- **9.12** OPEN [PROPOSED, not measured] - COR. `/about/devops` compares a three-account token SUM. {claims: CLM-278}

### ROOT 6 - FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM - **RE-RANKED UP (S99)**

**RE-RANK, with the reason generation 18 owes for it.** This root sat below ROOT 5 for four
generations as a storage-and-backup root. S99 measured that it also holds a LIVE CAPABILITY GAP:
the two 30-minute crons deliver about a third of their declared slots, and the guarantee GNI
publishes about its own detection latency rests on the cadence that is not happening. That is
target-bearing, not housekeeping.

- **6.10** **NEW (S99)** [MEASURED] - ADA - **THE FREE TIER GIVES NO DELIVERY GUARANTEE, NOT {claims: CLM-230, CLM-242, CLM-751}
  MERELY NO TIMING GUARANTEE - AND THAT WAS NEVER MEASURED.** The ARCHIVED row "the lateness
  band" was archived because "a free-tier scheduler gives no timing guarantee". That reason
  understates it: R-S87-6's "zero runs missed" was measured over crons firing 1-3 times a day
  (S87 n=133, S91 n=8 slots) and is FALSE for the two firing 48 times a day. The delivery ratio
  is a distinct property with a distinct instrument, and the instrument now exists
  (`tools/gni_runtime.py`, the delivery table in section six). Derived lateness band: **744 min**.
  Un-archives the lateness row by measurement, per the ARCHIVED section's own condition.
  NOTE (S109) [MEASURED]: the main pipeline started at 08:05Z and 14:43Z on Oct 3, and at 08:26Z and
  15:22Z on Oct 4, against a cron of 02:13 and 10:13 UTC - about six hours late every time. The adaptive
  protection and blackout windows (GNI-R-118, GNI-R-122) are keyed to the cron times, so they no longer
  bracket the runs they were written to protect. A lead folded here, not opened (DECISION S109-9).
- **6.5** OPEN - COR - **THERE IS NO BACKUP.** Still the highest single-point loss in the system, {claims: CLM-127, CLM-144}
  now for NINE generations, and never the mission. Said plainly rather than re-ranked again.
- **6.3** RE-SPECIFIED (S89) - ADA. Meter against tables; the difference is unexplained. {claims: CLM-278}
- **6.4** OPEN - ADA. L5 exposure when Supabase 402s. Paired with **5.30**. {claims: CLM-745}
- **6.13** **NEW (S101)** [MEASURED] - COR - **EVERY CADENCE FIGURE SECTION SIX PUBLISHES SPANS A {claims: CLM-230, CLM-242, CLM-751}
  REGIME BOUNDARY.** The delivery ratio, the median lateness and the derived lateness band are all
  averaged across a step change the generator itself warns about in its own prose. Section ten
  refuses those figures and publishes per-regime numbers with their windows instead, so the
  document now disagrees with itself between two sections. `C7` catches this shape in section ten
  and nothing catches it in section six. Same class as the GRAVEYARD's ruling on a window average.
  NOTE (S104): `C8` does not reach this either. `C8` asks whether section six's declared
  fingerprint matches the snapshot it read; it cannot ask whether the FIGURES derived from that
  snapshot are honest. Freshness and truthfulness are different properties and this item is the
  second one. See **5.59**, which is the same distinction found from the other side.
- **6.15** **NEW (S102)** [MEASURED] - PRE - **THE POLICY IS NARROWER THAN THE PROBLEM CLASS IT {ORPHAN}
  SERVES.** Section ten's policy fires when the freshness error budget is exhausted, and its
  corrective clause ranks a cause that IS ours above the next mission. The detector defect opened
  in ROOT 5 is the same disease one level up - a published claim that is untrue about GNI itself -
  and the policy cannot reach it, because the budget is NOT exhausted and the truthfulness of an
  instrument is not the freshness of a bound. **RULED at S102: the policy is NOT widened.** A
  trigger that needs judgment is a ruling wearing a policy's uniform. Recorded so a future clause
  is EARNED by first building the instrument that could fire it.

- **6.16** NEW (S105) [MEASURED] - ADA - `package.json` and `package-lock.json` DISAGREE on the major {ORPHAN}
  version of `@types/node`, so `npm ci` refuses with `EUSAGE` in a clean checkout (S105 container).
  `npm install` and `tsc --noEmit` pass, and Vercel built every S105 push, so nothing deployed is
  broken; the reproducible install path is.
  NOTE (S109): still true at `c78c288` - `npm ci` refused with the same `EUSAGE` in the S109 container.

### ROOT 5 - INSTITUTIONAL HARDENING

**NOTE ON THIS ROOT'S STANDING (S104).** It was "the roadmap's own root" for six generations. The
roadmap it served is finished and archived. Every item below therefore stands on its own merit
against the TARGET from this close forward, and none of them inherits priority from an arc that no
longer exists - Protocol PART C step 4a, which forbids inheriting a queue across a phase
transition. Nothing is inherited here; what is carried is carried because it is still true.

- **5.58** **NEW (S104)** [MEASURED, DISCLOSED AT SHIP TIME] - PRE - **SECTION SEVEN'S SECRET LIST {ORPHAN}
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
- **5.59** **NEW (S104)** [MEASURED] - COR - **NOTHING CHECKS PROVENANCE: ONE DOCUMENT MAY CITE {ORPHAN}
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
- **5.60** **NEW (S104)** [MEASURED] - ADA - **SECTION SIX WAS NOT REGENERATED AT S104, AND THE {ORPHAN}
  RE-HARVEST THAT WOULD REGENERATE IT NEEDS A RULING FIRST.** `gni_runtime.py` refused at the close:
  no snapshot exists for this session and `--harvest` is a separate act. It is DECLARED rather than
  skipped, and `C8` reports section six FRESH on its own terms - the stamp names the live snapshot
  and matches its bytes - which is exactly the distinction **5.59** is about. The blocking question
  is the standing UNKNOWN: does the published bound hold on a MOVED window? Moving the window
  carries SLO-3's regime rule with it and changes a published SLO, so it is a deliberate act with a
  ruling in front of it, never a side effect of a close. Two harvests three days apart already agree
  digit for digit on the frozen window `08-27 to 09-03`, so a re-harvest of THAT window measures
  nothing new.
- **5.52** **NEW (S102)** [MEASURED; NARROWED AT S104] - COR - **THE PUBLISHED REGENERATION ORDER {ORPHAN}
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
- **5.42** **NEW (S100)** [MEASURED; RULED AT S104, NOT YET SHIPPED] - PER - **`HEAD` IN A {ORPHAN}
  GENERATED STAMP IS DECORATIVE AND GOES STALE AT THE COMMIT THAT SHIPS IT.** All three generators
  stamp the short HEAD. Two options stood: drop it, or keep it and say in the stamp that it names
  the commit at RENDER time. **DECISION S104-1 chose the second, and it was already this project's
  ruling** - `d9ebebb` at S102 wrote that the one-commit lag between harvest and commit is what
  harvest-then-commit means, not a defect. S104 measured the consequence precisely: at `8ce57fc`
  the stamp names its own parent and is exactly right; four commits later at `a923ad9` the same
  stamp names a commit four steps back. **What is written and what is not:** the limitation is now
  recorded in row four of the completion test, with the reason a working-tree check cannot settle
  it. The STAMP ITSELF still does not say it, and that is the whole of what remains here.
- **5.35** **NEW (S99)** [MEASURED, DISCLOSED AT SHIP TIME] - PER - **`gni_runtime.py`'s PAIRING {ORPHAN}
  ASSUMES FIFO AND REFUSES AT THE WINDOW EDGE.** Two limitations, both written into section 6.5
  rather than left to be found: (a) ordered matching assumes the scheduler delivers slots in
  order, and MAD's two morning slots are 30 minutes apart against a 12-hour band, so an
  out-of-order delivery would mis-pair silently; (b) against a synthetic uniform 12-hour lag the
  pairing REFUSES with "a run BEFORE its slot at the window edge" even though delivery was
  complete. The failure direction is safe - NOT MEASURABLE rather than a wrong number - but it is
  a false negative. Fix: widen run collection past the window end without letting the previous
  day's runs leak in.
- **5.36** **NEW (S99)** [MEASURED] - PRE - **THE SNAPSHOTS HAVE NO RETENTION.** One runtime {ORPHAN}
  snapshot lands per session that harvests, each around 180 kB, and section six is regenerated
  every close. That is deliberate - the snapshot IS the evidence and must be in the tree for the
  byte-identity test - but nothing says when an old one may go. Kin of **6.5** and of the Partner B
  retention lesson: a stock grows, a flow does not. NOTE (S104): two snapshots now sit in `docs/`
  and the RELATION rule picks the higher, which `C8` depends on. Decide the policy before there are
  twenty, and decide it knowing a check now reads the newest one by construction.
- **5.30** OPEN (S98) [MEASURED] - COR. `_fetch_relevant_articles` returns an empty pool from {claims: CLM-227}
  three places and `run_mad_protocol` divides by its size. Written fail-open, behaves fail-hard.
  The policy question IS the item: what should MAD publish when it has no articles?
- **5.31** OPEN (S98) [MEASURED] - PRE. Model resolution has no floor; resolved at module import. {ORPHAN}
  NOTE (S109): a TypeScript sibling - `src/app/api/stock-context/route.ts` falls back to a retired Llama
  model id when its environment variable is unset. Found by the S69 census re-read, folded here.
- **5.32** OPEN (S98) [MEASURED] - PER. `dryrun_two_account_split.py` sits at the REPO ROOT, {claims: CLM-621}
  outside the CI glob, exits 1, never read.
- **5.28** OPEN (S96) - COR. An unverifiable checksum. Practice continued this generation. {ORPHAN}
- **5.29** OPEN (S96) - PER. The register has six entry shapes. Load-bearing: `C6` reads it through {ORPHAN}
  the generator's parser. Appends since S99 have used the dominant shape without regularising.
- **5.21** OPEN (S94) - PRE. No `.gitattributes`. Unchanged, and it cost time again at S104: `git {ORPHAN}
  add` printed six LF-will-be-replaced-by-CRLF warnings at the mission commit. Harmless because
  every published hash in this repo is EOL-normalised (R-S98-3), which is the only reason the
  Windows tree and the Linux runner agree on section five's manifest md5 - proven at S104 by `C8`
  passing in CI on the same bytes it passed on locally.
- **5.20** PARTIALLY DISCHARGED (S94/S95) - PRE. Fixture at **25** families as of S104, up from 21. {ORPHAN}
  What remains is the control probe's own evidence.
- **5.22** OPEN (S95) [INSTANCE RE-HIT AT S104] - PER. Console fragility of `tools/*.py` on {ORPHAN}
  Windows. The instance this item already names - `python tools/gni_state.py --stdout` dying with
  `UnicodeEncodeError` on an arrow under cp1252 - was hit AGAIN at S104 and cost a false
  certification: two truncated renders compared clean. The item was already measured and already
  written down; what failed was reading a trap that named a DIFFERENT tool in the same family
  (R-S104-4). The fix is one line at import, as `gni_runtime.py` already has.
- **5.23** OPEN (S95) - PER. `C5`'s blind spot. NOTE (S104): confirmed live. `C5` rejects an {ORPHAN}
  integer literal above one inside a check function but cannot see a number inside a STRING, so a
  hard-coded count in a PASS message would pass its own lint. `C8`'s message derives its number,
  checked by grep at this close - but nothing enforces that.
- **5.25** OPEN (S95) - PRE. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.** {ORPHAN}
- **5.15** OPEN (S93) - PER. Selftest coverage. {ORPHAN}
- **5.16** OPEN (S93) [ONE INSTANCE MEASURED at S98] - PER. `__main__` blocks outside `tests/`. {ORPHAN}
- **5.18** OPEN (S93) - PER. Unread wrongness ledgers. Discharged by hand three times now: once {ORPHAN}
  when a session record ruled the standdown out as the cadence collapse's cause, again at S101 when
  the records returned four rule ids the register had lost, and again at S104 when the queue itself
  turned out to hold one defect under two numbers. Still no instrument.
- **5.19** OPEN (S93) - PER. R-S91-4's disproven evidence. {ORPHAN}
- **5.5** OPEN - PER. **PROMOTED INTO 5.56.** {ORPHAN}
- **5.6** OPEN - PER. **PROMOTED INTO 5.56.** {ORPHAN}
- **5.7** OPEN - PER. **PROMOTED INTO 5.56.** {ORPHAN}
- **5.8** OPEN - PER. **PROMOTED INTO 5.56.** {ORPHAN}
- **5.11** OPEN - PER. **PROMOTED INTO 5.56.** {ORPHAN}
- **5.12** OPEN - PER. **PROMOTED INTO 5.56, TEXT STILL UNRECOVERED.** {ORPHAN}
- **5.38** **NEW (S100)** [MEASURED] - ADA - **THE TREE CREATES ITS OWN PATH ROOTS, SO A FILE {ORPHAN}
  ANSWERS TO SEVERAL NAMES.** Tracked modules call `sys.path.append` or `sys.path.insert` from
  many places, published in ARCHITECTURE section five's path-roots subsection. Consequence:
  `ai_engine/analysis/mad_protocol.py` is imported as `analysis.mad_protocol`, never by the
  `ai_engine.` prefix, and the same file also answers to a bare `mad_protocol`. This is not a
  style note - it is why the FIRST version of `gni_blocks.py` reported three internal edges and
  zero test coverage, both impossible, and it will break the next reader that assumes
  package-relative names. No fix is proposed here: consolidating the roots is a large refactor
  with a real regression surface, and the item exists to make the cost visible and RULED rather
  than rediscovered. A decision is wanted before any import is touched.
- **5.39** **NEW (S100)** [MEASURED] - PRE - **MOST NON-TEST MODULES ARE IMPORTED BY NO TEST {ORPHAN}
  MODULE, AND NEARLY HALF THE TESTS IMPORT ONLY `mad_protocol`.** ARCHITECTURE section five's
  test-import table. Coverage here means one thing only - a test names the module in an import -
  so the true figure is not better than this and may be worse. This compounds the standing item
  that the assertions under `ai_engine/tests/` have never been run in CI: a test that is neither
  run nor imports what it claims to test is two failures, not one.
- **5.40** **NEW (S100)** [MEASURED] - PER - **A STANDING TABLE OF MODULE-LEVEL SYMBOLS READ {ORPHAN}
  NOWHERE, AND MODULES IMPORTED BY NOTHING.** The two no-static-reference tables in ARCHITECTURE
  section five. This is the class that produced DET-DEAD and `_FORCE_PROVIDER` five months apart,
  both found by accident. It is NOT a deletion list - pytest finds `test_*` by name, and a module
  can be reached by a workflow entrypoint. The work is a TRIAGE: join the unreferenced-module table
  against section seven's entrypoint column, subtract pytest discovery from the lonely-symbol
  table, and rule on the remainder. Do not delete anything before that join exists in writing.
- **5.43** **NEW (S100)** [MEASURED] - PRE - **`gni_state.py` HOLDS A HAND-WRITTEN PROBE COUNT.** {ORPHAN}
  Its control probe prints a pass tally as a literal. It is CORRECT TODAY and that is the whole
  danger: it is right by coincidence and unprotected against the next probe added. This is the
  pattern `C5` and R-S81-5 forbid inside the detector, and `gni_runtime.py`'s own docstring records
  that this same literal was once wrong by one when counted. Fix shape: count the failures, as
  `gni_blocks.py` and `gni_runtime.py` both do. Still unfixed at S104, and now the only
  hand-written instrument count left in `tools/`.
- **5.44** **NEW (S100)** [MEASURED] - COR - **`gni_state.py` PROMISES EXIT CODES IT DOES NOT {ORPHAN}
  DELIVER ON TWO PATHS.** Its docstring lists three. `main()` calls `splice(src.read_text(...))`
  with no `is_file()` guard and no `except ValueError`, so a mistyped `--src` and a document
  missing the section-seven boundary both die with a traceback and exit 1. `gni_runtime.py` guards
  both. Same class as the standing item about an exit code absent from its own docstring, and kin
  of **5.22**, whose instance produces exactly such an unlisted exit.
- **5.45** **NEW (S100)** [MEASURED] - PRE - **THE GRAVEYARD CARRIES A DOUBLED END SENTINEL.** {ORPHAN}
  `<!-- GRAVEYARD-END -->` appears twice, and the rule above it appears twice. The published md5
  covers only through the FIRST sentinel, so the value is stable today; but any future copy that
  bounds the section differently silently produces a different hash for the same seven rows. Do NOT
  quietly delete the duplicate: five generations now publish the same value, and removing bytes
  inside the hashed region breaks a number those generations carried. The fix is a ruling on which
  boundary is canonical, then one deliberate re-baselining that says so. NOTE (S104): the assembler
  that wrote this generation implements the FIRST-sentinel boundary in code, so the ambiguity is
  now encoded in a tool as well as in prose. That raises the cost of ruling the other way.
- **5.47** **NEW (S101)** [MEASURED] - PRE - **ONE-SHOT PATCH SCRIPTS HAVE NO POLICY, AND THE TREE {ORPHAN}
  CURRENTLY SAYS BOTH THINGS.** Four S95 one-shot scripts are committed under `tools/`; S100's
  order generator was deleted after use, and S101 deleted four more. Whichever answer is right, the
  committed ones sit inside section five's module count and its dead-surface census forever, and
  the deleted ones cannot be re-run to reproduce their own output. NOTE (S104): this item has now
  produced a measured consequence rather than a hypothetical one. `patch_s103_row4.py`, committed
  at S103, is the single file that moved section five's manifest and made its stamp false; S104
  committed four more patch scripts. A ruling, then one sweep.
- **5.48** **NEW (S101)** [MEASURED] - PRE - **THE HARVEST CAP SPANS THE SLO WINDOW TODAY AND WILL {ORPHAN}
  NOT IF DELIVERY RECOVERS.** `gni_runtime.py` caps the harvest at three hundred runs. At the
  current rate that is about two months of heartbeat history; at the rate before the break it is
  about nine days, and a fortnight-long window would truncate silently. `C7` raises an instrument
  error rather than a pass when the snapshot cannot span the published window, so the failure is
  loud - but nothing PREVENTS it, and it appears only when things get BETTER.
- **5.49** **NEW (S101)** [MEASURED] - PRE - **"ROW FOUR" NAMES TWO DIFFERENT ROWS.** The roadmap {ORPHAN}
  table's fourth row is the session that ships the SLO; the completion test's fourth row is the one
  about staleness. The S100 handoff used both senses in a single sentence. NOTE (S104): the second
  sense is now CLOSED and the first is not, so the ambiguity is more dangerous rather than less -
  a reader who resolves "row four is done" to the wrong row concludes the SLO session shipped.
  Cheap to fix, and exactly the ambiguity that produces a wrong claim at a close.
- **5.51** **NEW (S102)** [RE-SPECIFIED AT S104] - PRE - **THE ORDER GENERATOR IS IN THE TREE FOR {ORPHAN}
  THE FIRST TIME, AND IT IS STILL A STAND-IN.** The S101 close credits `tools/mk_order_s101.py`
  with running both published counting commands on the assembled bytes before writing; that file
  never entered the repo, and generations 22 and 23 were assembled by scripts written at the close
  and thrown away. **What changed at S104:** `tools/mk_order_s104.py` is committed, so the next
  close reads a program rather than a description of one. **What did not:** it has no control probe.
  It verifies the graveyard md5, both counts and the closed-id rule, but nothing verifies that those
  verifications can FAIL - which is R-S93-1 applied to the tool that writes this file. Rebuilding it
  properly is still a session with a control probe, not a close-time chore, exactly as this item has
  said since S102.
- **5.53** **NEW (S102)** [PROPOSED, not measured] - PRE - **NO ONE KNOWS WHICH BRANCHES THE {ORPHAN}
  FIXTURE EXERCISES.** The sixteen families that existed before S102 never entered the window branch
  of the detector's gap calculation: the synthetic history starts at two in the morning, so no run
  ever fell inside a protection window. Two families fixed that ONE branch. Whether any other branch
  of any other check is equally unvisited has never been asked. NOTE (S104): four more families
  shipped, and the same question travels with them - each was written for a failure shape its author
  named, which is the same method that left the window branch unvisited for sixteen. A coverage read
  of the fixture against the detector is the measurement, and the answer decides whether this is one
  defect or a class.
- **5.55** **NEW (S103)** [MEASURED] - PRE - **NO CHECK WATCHES THE ORDER-ITEM NUMBERS THAT LIVE {ORPHAN}
  DOCUMENTS CITE.** `C1` verifies that every RULE id cited by a live document is registered, by four
  id schemes. Order item numbers are a fifth scheme and are checked by nothing. This is load-bearing:
  row four of the completion test inside `GNI_ARCHITECTURE` cites an order item by number, and if
  that number drifted the architecture would cite an item that does not exist while every check in
  the repo stayed green. NOTE (S104): row four now cites a SECOND item number, so the exposure
  doubled at the close that closed the row. The shape of the fix is `C1` generalised, which is also
  what the roadmap 3 specification proposes for abbreviations - one check, several id schemes, one
  register each.
- **5.56** **NEW (S103)** [MEASURED] - PER - **THE RETIRE-CLAUSE DEBT ON SIX ITEMS, PROMOTED INTO {ORPHAN}
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
- **5.57** **NEW (S103)** [MEASURED] - COR - **`C1` DID NOT SEE A DANGLING ID INSIDE THE REGISTER {ORPHAN}
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

- **7.1** PARTLY PAID (S86) - COR. `checked_spans` computed and discarded at the print. {claims: CLM-226}
- **7.2** BLOCKED - COR. Fix shape undecided; per-speaker baskets are in the GRAVEYARD. {claims: CLM-226}
- **7.3** PARTLY DISCHARGED (S86) - PER. Unchanged. {claims: CLM-226}
- **7.4** OPEN (S93) [UNMEASURED] - COR. `GROUNDING SHADOW` counts disagree across instruments. {claims: CLM-226}

### ROOT 2 - LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE - IMPORTANT

- **2.1** HALF-RULED (S86) - COR. Clause two, LABELED coverage, unmeasured. {ORPHAN}
- **2.2** BLOCKED on **2.1** - PER. {ORPHAN}
- **2.3** NARROWED (S87) - PER. {ORPHAN}
- **2.4** ONE READ FINISHES IT - COR. `/stocks` may render frozen prices. {claims: CLM-220}

### ROOT 3 - FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE - IMPORTANT

- **3.1** WIDENED (S86) - COR. A constant confidence value on two dates. {claims: CLM-224}
- **3.2** OPEN - ADA. `data_era` column plus tagging. {ORPHAN}

### ROOT 4 - COST AND HEADROOM - IMPORTANT

- **4.1** OPEN - COR. C2 solver recalibration; **9.19** carries the first log line. {ORPHAN}
- **4.4** OPEN - PER. Measure chars per token PER POSITION. {ORPHAN}
- **4.6** OPEN (S90) - ADA. `gni_mad` monthly token draw rose through the summer. {claims: CLM-621}

### LIFECYCLE + SECURITY - target-independent, never ranked away

**CLOCKS REMAIN PAUSED (DECISION S92-2).** 22 secrets stored. Nothing is due, nothing is overdue,
and no session may raise an item here as "overdue" until James restarts the clocks.

---

## ARCHIVED - THREE ITEMS CLOSE INTO IT THIS GENERATION

Archived is not closed and not solved: not worked under this target, not re-ranked each close,
not re-read at open. Anything here returns only by a new measurement and a ruling.

| what | why archived |
|---|---|
| **9.23** the capped score's consumers, and tables that could not show what the cap hides | CLOSED S109, the session's mission. (a) `frequency_log.escalation_score_raw` CERTIFIED: the first main rows after `440b205` read 18.4 and 21.5, every row before NULL; (b) the adaptive run's logged line reports the written row (`720e374`; run `37201358890` printed id `0de95f4e`, the row's own id); (c) the `/alerts` block that read a column `health_alerts` lacks is removed (DECISION S109-1); (d) `historical_correlations` keeps its capped average, labelled as capped (DECISION S109-2). |
| **9.20** two false statuses on the manual MAD path | CLOSED S109. `mad_preflight.py` check 2 filtered the QUOTA pipeline name; it filters `main` (`ea74cc9`; live preflight: "table empty" before, "Gap since Intelligence: 251 min" after). The four `return True` exits of `mad_runner.py` stay: over 60 runs, 40 of 40 `run-mad success` jobs carried `ARB-FIT`, so no job count was ever wrong; PROTOCOL v21 Part D step 4 now confirms a debate by `ARB-FIT` (DECISION S109-3). |
| **9.16** a workflow record taken from one side only | CLOSED S109 BY MEASUREMENT (DECISION S109-4). Both sides read: 8 of 9 workflows run `actions/setup-python` at 3.11; `gni_selfcheck.yml` runs the runner's own `python3`, unpinned. No live document repeats the S93 sentence. The unpinned interpreter is a lead, not itemised. |
| **9.24** the eight public claims the tree defeated | CLOSED S108 at `7cfc1d2`, the session's mission. They were nine: CLM-498 stated two counts and was bound to the true one, so it was bound FIRST and the check went red (9 DEFEATED) before it went green (0). Workflow copy made count-free - the ninth workflow file is a CI harness run on push, so "9" would have been false (R-S108-2); injection copy now says 81, bound to F-INJ; the home page's time now says scheduled. Read LIVE after Vercel `success`: six pages by HTML hits 0 to 1, the home page by the deployed client chunk (new 1 and 1, old 0 and 0), because its sentences sit in a client branch a fetch never receives. |
| **9.18** the TypeScript half of the position-select surface is unmeasurable | CLOSED S108 BY THE RETIRE CLAUSE, as accepted. Opened S95 with a real measurement (35 `.limit()` sites under `src/app/api/`, no TypeScript parser in a stdlib tool), then carried as a bare "Carried unchanged" for eleven regenerations - no measurement, no ruling, no claim served. The public half it worried about was closed at S106 by reading, not parsing: 9.22(b) moved every count to an exact count and R-S106-3 forbids a limited length shown as a count. The limit stays true and is accepted. |
| **5.24** twenty-two files in `docs/` with no session number | CLOSED S107 BY THE RETIRE CLAUSE, as accepted. Opened S95 and carried unchanged from generation 15 to 26 - twelve regenerations without a measurement or a ruling. The files are fossils the protocol already names as non-sources; numbering them buys nothing a reader needs. Its slot admits 9.24 under the cap. |
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

## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped - this generation's copy was hashed with the
published command's boundary BEFORE the file was written. The item count carries two commands
beside it, and both - plus the CAP - are checked on the ASSEMBLED bytes before the write by
`tools/mk_close_s109.py`, which refuses on any disagreement, on an unbound item, on a binding
that no longer holds against the verdict file, and on an ORPHAN RATE that differs from the
bindings it just wrote. Item **5.51** still asks for a control
probe; this assembler is not one.
Freshness confers no priority: an item found today does not outrank an item found in June unless
a measurement says so. Under the cap it also cannot enter without something leaving.
