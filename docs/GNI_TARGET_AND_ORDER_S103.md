# GNI TARGET + WORKING ORDER
**GENERATION 23 - 2026-09-09 (S103 close). SUPERSEDES generation 22
(`GNI_TARGET_AND_ORDER_S102.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S104)

**ITEM 5.54: GIVE SECTIONS FIVE AND SIX A STALENESS CHECK. IT IS THE OTHER HALF OF ROADMAP TWO'S
ROW FOUR, AND IT IS THE HALF THAT HAS NEVER HAD ONE.**

WHY THIS AND NOT ROADMAP 3. Roadmap 3 was specified at the S102 close and its own sequencing put
S104 at the roadmap-3 commitment. DECISION S103-1 moved that by one session, because roadmap 2 did
not close at S103 and this project has never once run an arc to completion. Starting a new roadmap
while the previous one stands at three of four, with one named item left, is how SUBPAGE-IC died -
renamed near its end and never declared. **DECISION S103-2 binds the other side of that: roadmap 3
begins at S105 whatever happens, and if 5.54 has not closed by then roadmap 2 is DECLARED NOT
ACHIEVED with the reason written down.** A plan without a completion test is the thing this file
spends every generation opening items about, and that includes a plan of ours.

WHAT IS ACTUALLY MISSING. `C2` checks section seven's workflow counts against the YAML. `C6`, as of
S103, checks every `INPUT ... md5` line the macro map declares against the LIVE file of its family.
Sections FIVE and SIX have nothing at all. This is not hypothetical and S103 measured it: section
five shipped at the S102 close stamping `86 tracked *.py` at HEAD `9e11f57` while the tree at that
close held 89, wrong by three from the moment it was published, and no check, probe or reader saw
it until S103 re-ran the generator. The generator counts the INDEX and stamps HEAD (item **5.52**),
so any tool committed after it runs makes its own stamp false.

THE SHAPE THE FIX ALREADY HAS. Every generated artefact in this repo publishes the fingerprint of
what it read: section five a `source manifest md5`, section six a `snapshot md5`, section seven a
workflow `manifest md5`, the macro map two `INPUT` lines. `C6` now loops over the map's declared
fingerprints, resolves each to the live file of its family and compares path AND content. The same
loop, pointed at the architecture's three stamps, closes row four. **It is one item and one check,
not three** - splitting it by section would hard-code the count this repo just finished removing.

DEFINITION OF DONE, written before the work: a check that derives each generated section's declared
fingerprint from the live tree and goes RED when they disagree, with no count of sections written
anywhere in the file; at least one fixture family per failure shape it can detect; the S102 section
five staleness replayed as the cert against the real commit that carried it; row four of the
completion test in `GNI_ARCHITECTURE` updated from bytes; and roadmap 2 declared FOUR OF FOUR with
its evidence, or NOT ACHIEVED with the reason.

CONSTRAINT THAT IS ALREADY MEASURED AND MUST NOT BE REDISCOVERED: `gni_state.py --no-gh` returns
an EMPTY stored-secret list, so section seven regenerated inside CI does not reproduce its
committed bytes. A "re-render and compare" check is therefore wrong for section seven and would be
red forever for the wrong reason. Compare the DECLARED fingerprint against the tree, never the
re-rendered document against the committed one.

THE ONE THING TO RULE AT THE OPEN: whether the check also covers section seven's SECRETS. The
workflow manifest hashes workflow bytes only; a secret added or removed leaves section seven stale
against its source with its published fingerprint still green. That is a real hole and it is
DISCLOSED rather than fixed; whether 5.54 must close it is a scope ruling and it is James's.

## TARGET - UNCHANGED

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

Roadmap 2 is **3 of 4** (Protocol PART C step 4a). Rows one, two and three hold; row four is
PARTIAL and is now HALF closed - the macro-map half shipped at S103 as item 5.50, the section
five and six half has never had a check and is item **5.54**, the mission below.

**Generation 22 opened this paragraph by declaring roadmap 2 COMPLETE and closed it by stating
three of four, four sentences apart, in the live queue.** S103 caught it at the open. Nothing had
lied to the file: the first two sentences were written while the close still expected row four to
ship, and the correction was appended instead of replacing them. That is the whole disease in one
paragraph - not a false claim inserted, a true claim left standing after it stopped being true -
and it is why the completion test in `GNI_ARCHITECTURE` is the scoreboard and this section is a
pointer to it.

**DEFINITION OF DONE - status at this regeneration:**
- the arbitrator reads what it claims to read - ROOT 1, ARCHIVED at S96. Unchanged.
- the escalation score carries information - ROOT 8, ARCHIVED at S96. Unchanged.
- the grounding gate measures reading, not existence - ROOT 7 IMPORTANT, still blocked on
  item **7.1**'s instrument. Unchanged.
- the public surface matches the configuration - **ROOT 9 stays TOP**, unchanged this close.
  But see ROOT 6: the CONFIGURATION itself no longer matches what runs, which is a second
  door into the same target and is why ROOT 6 gained two items.

---
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

**EXPECTED ITEM COUNT: 69 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**
Generation 21 held 67, generation 22 held 66. This close CLOSED ONE item, archived below - the
check that read one of the macro map's two inputs - and opened four. Their ids are deliberately
NOT repeated here: a closed id cited in the queue counts as a queue item, which is how generation
18's counts first disagreed at 52 and 56 and generation 19's at 61 and 64. The count RISES while a
mission completed, and that is honest rather than embarrassing: one of the three new items is the
retire-clause debt finally becoming a numbered piece of work instead of a paragraph six generations
old. Every id is bolded so the published command is true of the file it sits in, and a second
differently-shaped scan is printed beside it to reconcile against (R-S98-6):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S103.md \
  | grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S103.md \
  | grep -oE '[0-9]+\.[0-9]+' | sort -u | wc -l
```

Both must print **69**. If they disagree, an id is unbolded or a decimal has entered the prose,
and the count is not to be trusted until they agree. BOTH WERE RUN ON THE ASSEMBLED BYTES BEFORE
THIS FILE WAS WRITTEN, by a stand-in script that refuses to write when they disagree with each
other or with the number above (R-S95-1). It was a stand-in because `tools/mk_order_s101.py`,
which the S101 close credits with exactly this, IS NOT IN THE TREE - see the ROOT 5 item that
opens on it. The published range is line-anchored: an inline mention of the closing heading
inside this very paragraph does NOT end it, and a naive text split on it silently returns an
empty segment that counts zero and zero. That was caught this close, by running both commands.

### ROOT 9 - PUBLIC COPY AND REPORTED STATUS DRIFT FROM WHAT WAS MEASURED - URGENT - **TOP**

- **9.19** OPEN (S96) [PARTLY MEASURED at S98] - COR - DEGRADE-SILENT. A run in which `ctx-trim`
  leaves ZERO articles still reports SUCCESS. First byte evidence at S98 (`ARB-FIT: ctx_depth=0
  est=4997/5000`); still not the zero-article case. Next move: find a run at `ctx-trim@0`.
- **9.20** OPEN (S98) [PROPOSED, UNMEASURED] - COR. `mad_runner.py` prints `MAD skipped cleanly`
  and returns True. NOTE (S99): this is NOT the GitHub job-level `skipped` that R-S84-4's
  amendment describes; they look alike in a run list and are different doors. Do not conflate.
- **9.16** OPEN (S93) - COR. Records are from the `setup-python` side only.
- **9.17** OPEN (S94) - COR. Same shape as **9.16**, one generation later.
- **9.18** OPEN (S95) - COR. Carried unchanged.
- **9.5** OPEN - COR. Eight unresolved S69 census flags; F14 renders BEARISH over a stale basis.
- **9.11** OPEN - COR. `research/page.tsx` publishes a Groq daily-token figure against a May record.
- **9.12** OPEN [PROPOSED, not measured] - COR. `/about/devops` compares a three-account token SUM.

- **9.21** OPEN (S101) [PROPOSED, not measured] - COR - **NO PUBLIC PAGE HAS BEEN READ AGAINST
  THE PUBLISHED FRESHNESS BOUND. THIS IS THE NEXT MISSION.** `GNI_ARCHITECTURE` section ten
  promises that every public page stating a monitoring cadence states the MEASURED current-regime
  bound with its window, never the declared cron. Whether any page does is still unmeasured. It was
  named the S103 mission by generation 21 and DEMOTED by generation 22 when the roadmap's own
  scoreboard was re-run; it remains the top of ROOT 9 and is the clear candidate for S104. S102
  RAISED THE STAKES rather than discharging any of it: the bound moved from twelve hours to eight,
  so any page that was accidentally right is now wrong, and any page that was wrong is wrong by a
  different amount. Kin of **9.11** and **9.12**, with one difference - this one has a written
  promise to be checked against, so the reading has a verdict waiting. Carried, not closed: the
  DoD at the top of this file requires the reading AND a check that keeps reading.

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
  (`tools/gni_runtime.py`, the delivery table in section 6). Derived lateness band at this close: **744 min**.
  Un-archives the lateness row by measurement, per the ARCHIVED section's own condition.
- **6.5** OPEN - COR - **THERE IS NO BACKUP.** Still the highest single-point loss in the system,
  now for EIGHT generations, and never the mission. Said plainly rather than re-ranked again.
- **6.3** RE-SPECIFIED (S89) - ADA. Meter against tables; the difference is unexplained.
- **6.4** OPEN - ADA. L5 exposure when Supabase 402s. Paired with **5.30**.

- **6.13** **NEW (S101)** [MEASURED] - COR - **EVERY CADENCE FIGURE SECTION SIX PUBLISHES SPANS A
  REGIME BOUNDARY.** The delivery ratio, the median lateness and the derived lateness band are all
  averaged across a step change the generator itself warns about in its own prose. Section ten
  refuses those figures and publishes per-regime numbers with their windows instead, so the
  document now disagrees with itself between two sections. `C7` catches this shape in section ten
  and nothing catches it in section six. Same class as the GRAVEYARD's ruling on a window average.

- **6.15** **NEW (S102)** [MEASURED] - PRE - **THE POLICY IS NARROWER THAN THE PROBLEM CLASS IT
  SERVES.** Section ten's policy fires when the freshness error budget is exhausted, and its
  corrective clause ranks a cause that IS ours above the next mission. The detector defect opened
  in ROOT 5 this close is the same disease one level up - a published claim that is untrue about
  GNI itself - and the policy cannot reach it, because the budget is NOT exhausted and the
  truthfulness of an instrument is not the freshness of a bound. **RULED at this close: the policy
  is NOT widened.** A trigger that needs judgment is a ruling wearing a policy's uniform, and
  widening it would place four of this session's findings at the top of the queue at once, which
  is not a ranking. Recorded so a future clause is EARNED by first building the instrument that
  could fire it, rather than written on the strength of wanting one.

### ROOT 5 - INSTITUTIONAL HARDENING - the roadmap's own root

- **5.35** **NEW (S99)** [MEASURED, DISCLOSED AT SHIP TIME] - PER - **`gni_runtime.py`'s PAIRING
  ASSUMES FIFO AND REFUSES AT THE WINDOW EDGE.** Two limitations, both written into section 6.5
  rather than left to be found: (a) ordered matching assumes the scheduler delivers slots in
  order, and MAD's 10:43 and 11:13 slots are 30 minutes apart against a 12-hour band, so an
  out-of-order delivery would mis-pair silently; (b) against a synthetic uniform 12-hour lag the
  pairing REFUSES with "a run BEFORE its slot at the window edge" even though delivery was
  complete. The failure direction is safe - NOT MEASURABLE rather than a wrong number - but it is
  a false negative. Fix: widen run collection past the window end without letting the previous
  day's runs leak in.
- **5.36** **NEW (S99)** [MEASURED] - PRE - **THE SNAPSHOTS HAVE NO RETENTION.**
  `docs/gni_runtime_snapshot_S99.json` is 182,578 bytes and section 6 is regenerated every close,
  so one lands per session. That is deliberate - the snapshot IS the evidence and must be in the
  tree for the byte-identity test - but nothing says when an old one may go. Kin of **6.5** and of
  the Lens retention lesson: a stock grows, a flow does not. Decide the policy before there are
  twenty.
- **5.30** OPEN (S98) [MEASURED] - COR. `_fetch_relevant_articles` returns an empty pool from
  three places and `run_mad_protocol` divides by its size. Written fail-open, behaves fail-hard.
  The policy question IS the item: what should MAD publish when it has no articles?
- **5.31** OPEN (S98) [MEASURED] - PRE. Model resolution has no floor; resolved at module import.
- **5.32** OPEN (S98) [MEASURED] - PER. `dryrun_two_account_split.py` sits at the REPO ROOT,
  outside the CI glob, exits 1, never read.
- **5.28** OPEN (S96) - COR. An unverifiable checksum. Practice continued this generation.
- **5.29** OPEN (S96) - PER. The register has six entry shapes. Load-bearing: C6 reads it through
  the generator's parser. S99 appended in the dominant shape and did not regularise.
- **5.21** OPEN (S94) - PRE. No `.gitattributes`. Unchanged at this close: the register alone is
  `i/lf w/crlf`, and S99's append deliberately preserved its CRLF rather than silently
  converting 1556 line endings inside a docs commit.
- **5.20** PARTIALLY DISCHARGED (S94/S95) - PRE. Fixture at 14 families. What remains is the
  control probe's own evidence.
- **5.22** OPEN (S95) [ONE INSTANCE MEASURED at S99] - PER. Console fragility of `tools/*.py` on
  Windows. Instance: `python tools/gni_state.py --stdout` dies with `UnicodeEncodeError` on
  `\u2192` under cp1252 and exits 1 - an exit code its own docstring does not list. The
  file-writing path is safe (`write_text(encoding="utf-8")`); only `--stdout` is affected.
  `tools/gni_runtime.py` reconfigures stdout at import and does not have it.
- **5.23** OPEN (S95) - PER. C5's blind spot.
- **5.24** OPEN (S95) - PER. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**
- **5.25** OPEN (S95) - PRE. Carried unchanged from generation 15. **RETIRE CLAUSE DUE.**
- **5.15** OPEN (S93) - PER. Selftest coverage.
- **5.16** OPEN (S93) [ONE INSTANCE MEASURED at S98] - PER. `__main__` blocks outside `tests/`.
- **5.18** OPEN (S93) - PER. Unread wrongness ledgers. Discharged by hand twice now: once when
  a session record ruled the standdown out as the cadence collapse's cause, and again at S101 when
  the records returned four rule ids the register had lost. Still no instrument.
- **5.19** OPEN (S93) - PER. R-S91-4's disproven evidence.
- **5.5** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.6** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.7** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.8** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.11** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.12** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**

**THE SIX LINES ABOVE ARE A DEBT THIS GENERATION IS PAYING - BY PROMOTION, WHICH IS THE RETIRE
CLAUSE'S OWN SECOND OPTION.** The clause says an item unworked below the line for three
regenerations is CLOSED as accepted or PROMOTED with a written reason, and dropping one silently is
neither. Generations 16 and 17 replaced their text with the bare line "Carried unchanged from
generation 15", so the live order no longer states what they ARE, and closing an item whose text
this file does not hold would be R-S98-1's disease (a compression that replaced its own subject).
Generation 18 recorded the debt and named the remedy; generations 19 through 22 carried it forward
unpaid, four closes running, each one reading the same paragraph and deferring. **They are now item
5.56**, with the fragments S103 recovered written into it, so the work has a number, a home and a
count. What was wrong was never the ruling; it was that an obligation with no id is a paragraph,
and a paragraph is something a close can read and postpone.

- **5.38** **NEW (S100)** [MEASURED] - ADA - **THE TREE CREATES ITS OWN PATH ROOTS, SO A FILE
  ANSWERS TO SEVERAL NAMES.** 29 of 80 tracked modules call `sys.path.append` or
  `sys.path.insert`, 35 calls in total, published in ARCHITECTURE section 5's path-roots
  subsection. Consequence:
  `ai_engine/analysis/mad_protocol.py` is imported as `analysis.mad_protocol`, never by the
  `ai_engine.` prefix, and the same file also answers to a bare `mad_protocol`. This is not a
  style note - it is why the FIRST version of `gni_blocks.py` reported 3 internal edges across
  79 modules and zero test coverage, both impossible, and it will break the next reader that
  assumes package-relative names. No fix is proposed here: consolidating the roots is a large
  refactor with a real regression surface, and the item exists to make the cost visible and
  RULED rather than rediscovered. A decision is wanted before any import is touched.
- **5.39** **NEW (S100)** [MEASURED] - PRE - **61 OF 68 NON-TEST MODULES ARE IMPORTED BY NO TEST
  MODULE, AND 5 OF 11 TESTS IMPORT ONLY `mad_protocol`.** ARCHITECTURE section 5's test-import
  table. Coverage here means one
  thing only - a test names the module in an import - so the true figure is not better than this
  and may be worse. Note this compounds the standing item that the 36 assertions under
  `ai_engine/tests/` have never been run in CI: a test that is neither run nor imports what it
  claims to test is two failures, not one.
- **5.40** **NEW (S100)** [MEASURED] - PER - **35 OF 965 MODULE-LEVEL SYMBOLS ARE READ NOWHERE,
  AND 23 MODULES ARE IMPORTED BY NOTHING.** The two no-static-reference tables in ARCHITECTURE
  section 5. This is the class that produced
  DET-DEAD and `_FORCE_PROVIDER` five months apart, both found by accident; it is now a standing
  table. It is NOT a deletion list - pytest finds `test_*` by name, and a module can be reached by
  a workflow entrypoint. The work is a TRIAGE: join the unreferenced-module table against
  section 7's entrypoint column,
  subtract pytest discovery from the lonely-symbol table, and rule on the remainder. Do not delete anything before
  that join exists in writing.
- **5.41** **NEW (S100)** [MEASURED] - COR - **NOTHING GOES RED WHEN SECTION 5 OR SECTION 6 GOES
  STALE.** `tools/gni_rule_checks.py` holds six checks; C2 compares section 7's workflow counts against
  the YAML and C6 compares the macro map against the register. Section 6 shipped at S99 and
  section 5 at S100, both generated, both with NO staleness check. Roadmap 2's completion test
  row 4 records the reason as "sections 5 and 6 cannot be stale because they do not exist" -
  that sentence stopped being true two commits ago and the row was never revisited. Fix shape:
  a C7 that imports the generators' OWN parse functions and compares the stamped manifest md5
  against a live recomputation - the precedent C6 set by importing `gni_macro_map.parse_rules`
  rather than writing a second parser (R-S96-3). `gni_blocks.py` and the patched `gni_state.py`
  were both written with importable `norm_md5` and collect functions so this is cheap.
- **5.42** **NEW (S100)** [MEASURED] - PER - **`HEAD` IN A GENERATED STAMP IS DECORATIVE AND GOES
  STALE AT THE COMMIT THAT SHIPS IT.** All three generators stamp the short HEAD. Observed this
  close: section 5 carried `b769acc` and section 7 carried `cbd34a7` in the SAME document,
  because they were generated either side of a commit; and after `3268c14` both are stale while
  the content is current. The manifest md5 is the field that actually carries identity - it is
  computed from the inputs and moves only when they move. Options: drop HEAD, or keep it and say
  in the stamp that it names the commit at RENDER time and is not a freshness claim. Small, but
  it is a published figure that is wrong by construction, which is the target.
- **5.43** **NEW (S100)** [MEASURED] - PRE - **`gni_state.py` LINE 323 HOLDS A HAND-WRITTEN
  `7/7`.** `print(f"CONTROL PROBE: 7/7 pass ...")`. It is CORRECT TODAY - there are exactly seven
  `fails.append` sites, counted by AST this close - and that is the whole danger: it is right by
  coincidence and unprotected against the eighth. This is the pattern C5/R-S81-5 forbids, and
  `gni_runtime.py`'s own docstring records that this same literal was once wrong by one when
  counted. Fix shape: count the failures, as `gni_blocks.py` and `gni_runtime.py` both do.
  DELIBERATELY NOT fixed inside the S100 patch, which was authorised for two items.
- **5.44** **NEW (S100)** [MEASURED] - COR - **`gni_state.py` PROMISES EXIT CODES IT DOES NOT
  DELIVER ON TWO PATHS.** Its docstring lists 0 / 2 / 3. `main()` calls `splice(src.read_text(...))`
  with no `src.is_file()` guard and no `except ValueError`, so a mistyped `--src` and a document
  missing the section-7 boundary both die with a traceback and exit 1. `gni_runtime.py` guards
  both. Same class as the standing item about an exit code absent from its own docstring.
- **5.45** **NEW (S100)** [MEASURED] - PRE - **THE GRAVEYARD CARRIES A DOUBLED END SENTINEL.**
  `<!-- GRAVEYARD-END -->` appears twice, and `---` immediately above it appears twice. The
  published md5 covers only through the FIRST sentinel, so the value is stable today; but any
  future copy that bounds the section differently silently produces a different hash for the same
  seven rows. Do NOT quietly delete the duplicate: generations 16, 17, 18 and 19 all publish
  `3e8ac222c6ef212261676c02d7d56f6f`, and removing bytes inside the hashed region breaks a value
  four generations have carried. The fix is a ruling on which boundary is canonical, then one
  deliberate re-baselining that says so.

- **5.47** **NEW (S101)** [MEASURED] - PRE - **ONE-SHOT PATCH SCRIPTS HAVE NO POLICY, AND THE TREE
  CURRENTLY SAYS BOTH THINGS.** Four S95 one-shot scripts are committed under `tools/`; S100's
  order generator was deleted after use, and S101 deleted four more. Whichever answer is right,
  the committed ones sit inside section five's module count and its dead-surface census forever,
  and the deleted ones cannot be re-run to reproduce their own output. A ruling, then one sweep.
- **5.48** **NEW (S101)** [MEASURED] - PRE - **THE HARVEST CAP SPANS THE SLO WINDOW TODAY AND WILL
  NOT IF DELIVERY RECOVERS.** `gni_runtime.py` caps the harvest at three hundred runs. At the
  current rate that is about two months of heartbeat history; at the rate before the break it is
  about nine days, and a fortnight-long window would truncate silently. `C7` raises an instrument
  error rather than a pass when the snapshot cannot span the published window, so the failure is
  loud - but nothing PREVENTS it, and it appears only when things get BETTER.
- **5.49** **NEW (S101)** [MEASURED] - PRE - **"ROW FOUR" NAMES TWO DIFFERENT ROWS.** The roadmap
  table's fourth row is the session that ships the SLO; the completion test's fourth row is the
  one that says nothing goes red when a generated section goes stale. The S100 handoff used both
  senses in a single sentence. Cheap to fix, and exactly the ambiguity that produces a wrong claim
  at a close.

- **5.51** **NEW (S102)** [MEASURED] - PRE - **THE GENERATOR THAT WROTE THE PREVIOUS GENERATION IS
  NOT IN THE TREE.** `tools/mk_order_s101.py` is credited by the S101 close with running both
  published counting commands on the assembled bytes before writing, and with catching the carried
  item that cost the two generations before it a rewrite each. `ls tools/` holds `mk_order_s95.py`
  and nothing else of that family. The tool never entered the repo. This generation was therefore
  assembled by a stand-in script written at the close and thrown away, which is the same standing
  as no tool at all. Rebuilding it is a session with a control probe, not a close-time chore.
- **5.52** **NEW (S102)** [MEASURED] - COR - **THE PUBLISHED REGENERATION ORDER CANNOT HOLD.**
  HANDOFF POINTERS prints one sequence - stage, blocks, state, map, detector, fixture, commit -
  before one commit. It cannot be run that way. `gni_blocks` and `gni_state` count the INDEX but
  stamp HEAD, so running them before the mission commit writes the index's file list under a HEAD
  that predates the work. Both also splice into the live architecture, so the map must run AFTER
  them or its architecture stamp is stale on arrival - and by the item above, nothing would catch
  that. This session needed four commits and four map runs. The correct order should be decided
  AFTER the tools are fixed, not written down from one session's improvisation.
- **5.53** **NEW (S102)** [PROPOSED, not measured] - PRE - **NO ONE KNOWS WHICH BRANCHES THE
  FIXTURE EXERCISES.** The sixteen families that existed before this close never entered the
  window branch of the detector's gap calculation: the synthetic history starts at two in the
  morning, so no run ever fell inside a protection window, so the branch that suppresses runs
  returned False for every run since the check shipped. Two new families fixed that ONE branch.
  Whether any other branch of any other check is equally unvisited has never been asked. A
  coverage read of the fixture against the detector is the measurement, and the answer decides
  whether this is one defect or a class.

- **5.54** **NEW (S103)** [MEASURED] - COR - **SECTIONS FIVE AND SIX HAVE NO STALENESS CHECK OF
  ANY KIND, AND SECTION FIVE HAS ALREADY SHIPPED STALE.** `C2` checks section seven's counts
  against the YAML; `C6` checks every fingerprint the macro map declares. Sections five and six
  publish fingerprints of their own - a `source manifest md5` over tracked `*.py` and a
  `snapshot md5` - and nothing reads either. Measured at S103: section five shipped in the S102
  close stamping `86 tracked *.py` at HEAD `9e11f57`, while the tree at that close held **89**.
  Wrong by three from the moment it was published, and invisible until a generator was re-run for
  an unrelated reason. The mechanism is item **5.52**: the generator counts the INDEX and stamps
  HEAD, so every tool committed after it runs falsifies its stamp. **THIS IS THE NEXT MISSION** and
  it is the last unmet half of roadmap 2's row four (DECISION S103-1). One item and one check, not
  three - splitting by section would hard-code the count the check shipped this close removed.
  Constraint already measured, do not rediscover: `gni_state.py --no-gh` returns an EMPTY stored
  secret list, so re-rendering section seven inside CI cannot reproduce its committed bytes. The
  check compares the DECLARED fingerprint against the tree, never a re-render against the commit.
- **5.57** **NEW (S103)** [MEASURED] - COR - **`C1` DID NOT SEE A DANGLING ID INSIDE THE REGISTER
  ITSELF.** `GNI-R-118` is cited as law by `ai_engine/monitoring_pipeline.py:42`, and it is cited
  in the register's own prose in the S102 `GNI-R-122` amendment. It is defined nowhere and was in
  no manifest. `C1` went RED at the S103 close only when the HANDOFF and this file cited it too -
  one generation after the register began citing it. Either `C1` exempts the register from its own
  scan or the citation form differs; the cause is UNMEASURED and settling it is this item. Two
  consequences travel with it, and both are bigger than the id. The register is the document most
  likely to cite ids, so an exemption there is an exemption where it matters most. And `C1` reads
  live DOCUMENTS only - `ai_engine/` cites rule ids in comments and nothing verifies them, which is
  how this one sat unregistered for months while every check stayed green. Manifested as
  `DANGLING-LAW` at this close, which records the fact without asserting a home it does not have.
- **5.55** **NEW (S103)** [MEASURED] - PRE - **NO CHECK WATCHES THE ORDER-ITEM NUMBERS THAT LIVE
  DOCUMENTS CITE.** `C1` verifies that every RULE id cited by a live document is registered, by the
  four id schemes `R-S##-#`, `LR-###`, `GNI-R-###` and `NN-PHI-*`. Order item numbers are a fifth
  scheme and are checked by nothing. This is load-bearing as of this close: row four of roadmap 2's
  completion test, inside `GNI_ARCHITECTURE`, cites item **5.54** by number, and that number was
  chosen at the S103 close before this file existed. If the number had drifted, the architecture
  would cite an item that does not exist and every check in the repo would stay green. The shape of
  the fix is `C1` generalised, which is also what the roadmap 3 specification proposes for
  abbreviations - one check, several id schemes, one register each.
- **5.56** **NEW (S103)** [MEASURED] - PER - **THE RETIRE-CLAUSE DEBT ON 5.5, 5.6, 5.7, 5.8, 5.11
  AND 5.12, PROMOTED INTO WORK RATHER THAN CARRIED A SEVENTH TIME.** Generations 16 and 17 replaced
  the six items' text with the bare line "Carried unchanged from generation 15", so the live order
  has not stated what they ARE since. Generation 18 recorded the debt and named the remedy - read
  their full text out of `GNI_TARGET_AND_ORDER_S95.md` and close or promote each in writing - and
  assigned it to S100. S100, S101 and S102 each carried it forward unpaid. S103 read enough to see
  why: **it is not a close-time chore.** It needs an old file opened, six items recovered, and six
  rulings made, which is a session's shape and not a paragraph's. Partial recovery at S103, from
  `GNI_TARGET_AND_ORDER_S95.md` lines 411-420: **5.5** is `DEBT_REGISTER_S69.md` and its one reader
  in five months; **5.6** is PARTLY PAID at S90, the register's PART 1 / PART 2 restructure;
  **5.7** is BYTE-CONFIRMED at S88, `_lower`/`_upper` still rendering `--` on `/autonomy`, which is
  a PUBLIC page and therefore ROOT 9's subject rather than ROOT 5's; **5.8** is unnumbered items
  being invisible to the uniqueness assert; **5.11** is the dead-symbol / unwired-module CI
  detector, which S91 converted and which line 535 of that file says was NOT a retire candidate.
  **5.12 HAS NO TEXT IN `GNI_TARGET_AND_ORDER_S95.md` AT ALL** - it is not merely compressed, it is
  unrecovered, and the earlier generation that holds it has not been found. Closing any of the six
  from these fragments would be R-S98-1's disease, so none is closed here. The debt is DISCHARGED
  BY PROMOTION, which is the retire clause's own second option, and it stops being a paragraph
  that four closes could read and defer.

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
| **5.50** `C6` read one of two inputs | CLOSED S103 at `6c05076` + `60af1a5`, CI green at job level on both. `C6` now loops over every `INPUT ... md5` line the map declares, resolves each to the LIVE file of its family - not to the file the line names - and compares path AND content, with no count of inputs anywhere in `tools/gni_rule_checks.py`. The defect was never a hard-coded two: the INPUT pattern was interpolated from the map's `GENERATED from` stamp, which names the register by construction. Fixture families `19-map-stale-arch-md5`, `20-map-arch-renamed` and `21-map-third-input`; 21 families, 0 mismatches. Certified against REAL commits: at `b7eaab4` that commit's own detector reports PASS and 7 checked 0 failed on the same tree where today's reports `GNI_ARCHITECTURE md5 a4fb9fce...` against the map's stamped `0d944f64...` - the md5 pair the S102 record captured when the defect was first seen, recovered from git rather than from prose - and at `3268c14` today's reports a RENAME with no md5 in it while the file the map names still hashes to exactly its stamped value. It then fired once more, unplanned, on the live tree between the generators and the map regeneration. |
| **ROOT 1** | CERTIFIED for content and ordering (S96). |
| **ROOT 8** | discharged in part at S91; the rest waited five generations under a target it does not serve. |
| the published band table | wrong in two of five rows - real, measured, not reachable before roadmap 2. |
| the dependency manifest | a roadmap-2 by-product. Note (S99): `GNI_ARCHITECTURE` section 7.3 cites an item in the six-range that this order does not carry - a dangling item citation, the order-file twin of what C1 checks for rule ids. That number is therefore NOT reused; S99 opened **6.10** and **6.11** instead. The exact id is in `GNI_ARCHITECTURE` section 7.3, deliberately not repeated here so the count commands stay true. |
| `mad_runner.py` unordered `limit(50)` | kin of R-S92-2, no consumer waiting. |
| **5.33** section 7's own clock | CLOSED S100 at `3268c14`. The stamp carries HEAD, the workflow file count and an EOL-normalised manifest md5; byte-identical on two renders two seconds apart, and the md5 MOVES when a workflow changes. |
| **5.34** `--session` default=94 | CLOSED S100 at `3268c14`. Now `required=True`; a bare invocation exits 2. |
| **5.37** two unregistered rule ids | CLOSED S101 at `3b3b54a`. Four March-2026 ids recovered VERBATIM from four independent session records and confirmed by their own id citations inside `ai_engine/monitoring_pipeline.py`, then registered in PART 0. Manifest eight rows to six. `GNI-R-122`'s manifest gloss was itself an inference, and it was wrong. |
| **6.11** the promise and the cadence disagree | CLOSED S101 at `b7eaab4`. ANSWERED rather than fixed, which is what the item asked for: GNI has two cadences and not one, and both are published per regime with their windows in `GNI_ARCHITECTURE` section ten. What GNI promises is now written down, and `C7` fails when the written number stops being true. |
| **6.8** heartbeat standdown | CLOSED S101 at `b7eaab4` WITH ITS ROOT CAUSE, which the item had asked for since S90: `GNI-R-122` is a protection-window rule justified by token collision and `GNI-R-114` says the heartbeat spends none. Reopened the same close as the fix item, now also closed below - the question was answered at S101, the fix at S102. |
| **6.12** the watcher that checks nothing | CLOSED S102 at `9e11f57`. The standdown is gone from `ai_engine/monitoring_pipeline.py:317-321`; `GNI-R-122` is AMENDED (S102) with its March-2026 sentence preserved verbatim, bound to the ADAPTIVE or MANUAL runs its own purpose clause names. The published bound FELL from 12 h to 8 h, derived by `C7`, and `C7` no longer assumes the standdown exists - `heartbeat_stands_down()` asks the tree by AST, so the bound rises again if the call returns. Certified by fixture families `17-standdown-absent` and `18-standdown-reinstated`, differing by one call and by nothing else, and re-derived at `608e5ed` against a freshly harvested snapshot that agrees with the committed one digit for digit. Two Groq-based subject tests were disproven first: neither pipeline imports groq, and a text grep captures the watcher on its own `GNI-R-114` citations. |
| **5.46** the roadmap's stale scoreboard | CLOSED S102. The completion test in `GNI_ARCHITECTURE` was re-run for the first time since the S98 close and its status table rewritten from bytes: row one holds, row two holds (each generator rendered twice two seconds apart, `cmp`-identical, md5s published in the table), row three holds since S101, row four is PARTIAL and names item **5.50** as its fix. **Roadmap 2 is three of four, not one of four.** Two rows had been quietly true for several closes; a scoreboard nobody re-runs is a claim, not a measurement, which is what this item said and why it is closed by reading rather than by building. |
| **6.14** the snapshot's three stamps | CLOSED S102 at `d9ebebb`. Section six is now generated from `gni_runtime_snapshot_S102.json`, harvested this session at HEAD `8ce57fc`. Filename, `harvested_head` and newest run all name this session; the one-commit lag between harvest and commit is what harvest-then-commit means, not a defect. It could not be closed at `608e5ed`, where the close message claimed it: only `SLO-CFG` had moved, which is section ten's, and the item is section six's. The overclaim is recorded in the S102 handoff. |

**LEFT THE ARCHIVE THIS CLOSE: the lateness band.** It was archived because "a free-tier
scheduler gives no timing guarantee". A new measurement met the ARCHIVED section's own return
condition: the free tier gives no DELIVERY guarantee either, that is a different property, and it
had never been measured. It returned as items **6.10** and **6.11**; the second of those closed at S101 and is in the table above.

`docs/GNI_RULE_CHECKABILITY_S95.tsv` remains RETIRED (S96) - on disk, out of the queue.

## CHANGED THIS REGENERATION

- **DECISION S103-1 (James), ruled at the OPEN, before the work.** Row four of roadmap 2's
  completion test is read AS WRITTEN: it names four surfaces - sections five, six, seven and the
  macro map - so closing the macro-map half does NOT close the row. The S98 status table recorded
  sections five and six as ABSENT rather than as excluded, which means the row was waiting for them
  rather than ignoring them; and the row's own published command settles it without interpretation,
  because flipping a section five figure today still exits 0. Reading the row narrowly would have
  bought a fourth row by interpretation, and a completion test amended when it is about to fail is
  padding at the roadmap level - the disease section 10.3 is written against, one level up.
  Roadmap 2 stays at **3 of 4**.
- **DECISION S103-2 (James).** Roadmap 3 begins at **S105** regardless of outcome. If item 5.54 has
  not closed by then, roadmap 2 is DECLARED NOT ACHIEVED and the reason is written into the record.
  This is an anti-SUBPAGE-IC guard placed on our own plan: DECISION S103-1 deferred roadmap 3 by one
  session, and a second deferral would make it a pattern rather than a ruling. Every plan needs a
  completion test, including this one.
- SHIPPED: item **5.50**, in two commits, CI green at job level on both pushed tips
  (`rule_checks success` + `harnesses success`). `6c05076` the check, the control probe and three
  fixture families; `60af1a5` sections five, six and seven restamped at `6c05076`, row four updated
  from bytes, and the macro map regenerated LAST.
- CLOSED: **5.50**. NEW: **5.54**, **5.55**, **5.56**, **5.57**. rho = **1 / 4**.
- **THE CLOSE'S OWN DETECTOR CAUGHT THE CLOSE.** `C1` went RED on the first run after these
  documents were staged: `GNI-R-118`, written into the HANDOFF and this file while recording that
  the rule was acquitted, is registered nowhere. The id has been cited inside the register itself
  since the S102 amendment and `C1` never said so. That is item **5.57**; the row is manifested
  here as `DANGLING-LAW`. `C6` also went RED on the same run, exactly as predicted, because the
  register moved to `_S103.md` while the map still named `_S102.md` - the check this session
  shipped gating its own close, which is what step 9a exists for.
- **THE RETIRE CLAUSE IS PAID.** **5.5**, **5.6**, **5.7**, **5.8**, **5.11** and **5.12** are
  PROMOTED into item **5.56** with their recovered fragments and the reason written down. Four
  closes carried this paragraph unpaid; S103 established why - it is a session's work, not a
  close's - and gave it a number so it can be ranked like everything else.
- WRONG THIS CLOSE, AND WHO CAUGHT IT: **ten claims**, all mine, none reaching a shipped artefact.
  The two that matter: I stated the S102 silence existed at no commit boundary, having read four
  commit messages instead of measuring four trees - `git show` disproved it in one command and the
  cert this session shipped is built from exactly those trees. And I ruled a re-harvest could
  exhaust the error budget, four hours after echoing the handoff line that disproves it: two
  harvests three days apart agree digit for digit because the published window is frozen history.
  The pattern in the rest is one thing: on the mission I read bytes first, and on the diagnostics I
  guessed explanations first. Three consecutive shell predictions failed in the same five minutes.
- MEASURED AND CLOSED, not carried: SLO-1 is no longer unwired-and-unmeasured. Post-fix run
  `34335454766`, inside a protection window, logs all three checks executing - divergence, consensus
  and escalation. Ten post-fix heartbeat runs, zero non-success. `GNI-R-118` was suspected of being
  the standdown's twin and is NOT: it suspends the ADAPTIVE pipeline after the checks have run,
  which is `GNI-R-114`'s own subject, correctly scoped where `GNI-R-122` was not.
- NOT DONE, AND DECLARED RATHER THAN SKIPPED: no re-harvest. The published SLO window
  `08-27..09-03` is frozen history and a re-harvest cannot move it; moving the window is a separate
  act that carries SLO-3's regime rule with it, and it should be taken deliberately rather than as
  a side effect of a close. `npm run build` not run. The CONTRACT stays at **v10**, byte-identical.
- PROTOCOL RAISED TO **v17**: PART B's template is corrected to the shape five consecutive closes
  have actually shipped. See the version log in that file.

## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped - this generation's copy was verified against
generation 17's published md5 BEFORE the file was written, and again inside the assembled file
(R-S95-1). The item count carries two commands beside it and both are run on the ASSEMBLED bytes
before the file is written, by something that REFUSES to write when they disagree with each other
or with the declared count. At this close that something was again a stand-in, for the
second generation running, because the tool the S101 close credits with the job is still not in the
tree; that is item **5.51** and until it closes, this sentence describes a practice rather than a
program. Two generations is where a trap becomes a practice, which this file has said before. Four closes running,
the same failure has been looked for - a closed id cited in the sentence announcing its closure -
and this close is the first where the check found none, having been run before the write rather
than after (R-S98-6).
Freshness confers no priority: an item found today does not outrank an item found in June unless
a measurement says so.
