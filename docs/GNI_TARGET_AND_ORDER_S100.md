# GNI TARGET + WORKING ORDER
**GENERATION 19 - 2026-09-04 (S100 close). SUPERSEDES generation 18 (`GNI_TARGET_AND_ORDER_S99.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S101)

**ROADMAP 2 ROW 4: THE SLO. Declare what GNI promises, in writing, and make something go RED
when the promise is not met.**

WHY THIS IS TOP. It is JAMES'S roadmap 2 (DECISION S96-1), and rows 1-3 are now shipped: the
detector at S98, section 6 at S99, section 5 at S100 (`cbd34a7`). Row 2's completion test PASSES
for the first time - sections 5, 6 and 7 all generate byte-identically (`5ed36f4c...` on two
renders), section 7's own clock removed at `3268c14`.

The SLO is the row that makes the previous three matter. Section 6 measured that the two
30-minute crons deliver 282 and 292 of 768 declared slots; section 5 measured that 61 of 68
non-test modules are imported by no test. Neither of those turns anything red. An SLO is the
mechanism that does.

THE ONE ITEM RANKED ABOVE THIS, carried unresolved from the S99 close for James to rule at the
S101 open: item **6.11**. S99 ranked it above its own mission and did not self-authorise it;
at the S100 open James ruled the mission plus 5.33 and 5.34 instead, so 6.11 was NOT worked and
NOT withdrawn. It asks what cadence GNI actually has and what it should therefore PROMISE -
which is the SLO question wearing different clothes. Ruling it and row 4 together may be one
session rather than two. That is a suggestion, not a re-rank.

DEFINITION OF DONE, written before the work: a named, committed statement of what GNI promises
on cadence and on freshness; a check that FAILS when the promise is not met, wired into
`gni_ci_harness.yml`; and the check demonstrated failing on a case it must catch and passing on
one it must miss (R-S98-6). A promise nothing can falsify is not an SLO.

## TARGET - UNCHANGED

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

Roadmap 2 is **2 of 4** (Protocol PART C step 4a). Row 2 shipped at this close; its written
completion test lives in `GNI_ARCHITECTURE_S99.md` with a per-row status table, and that table
now names a failing row the S98 close did not know about: **row 2 fails on section 7's own
account**, not only because section 5 is missing.

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

## THE CROSS-ROOT DIAGNOSIS (carried from generation 7 - now with five instances)

> **GNI repeatedly measures what it has already guaranteed itself, and publishes the result as
> a fact about the world.**

| instance | what is measured | what it actually is |
|---|---|---|
| ROOT 7 | "the span exists in the pool" | reported as "the agent read it" |
| ROOT 8 gate | `_high_escalation` True six of six | a crisis channel that cannot leave crisis mode |
| ROOT 8 bonus | `diversity_bonus` at ceiling in most runs | the S39 funnel quota guarantees all three pillars |
| ROOT 8 GEO | GEO pillar "active" in every run | GEO hits far exceed the cap - the pillar cannot be inactive |
| ROOT 8 PHI | the PHI gate "protecting" the score | it has never fired; its own mute condition fires with it |

Its use is predictive - when a metric is nearly constant, ask WHO GUARANTEED IT before tuning it.
No sixth instance was added this close and no row changed.

**S99 NOTE - the S98 form of this diagnosis held again, four times, and once in the reverse
direction.** Three S98 instruments reported clean results about themselves; S99 produced four
more (R-S98-6's amendment lists them). The reverse case is new and worth the line: a measure can
also be bounded by the thing it measures, so it reports its SMALLEST possible answer exactly
where the truth is largest - a 365-minute lag read as 5 minutes (R-S99-1). Ask not only "who
guaranteed this constant" but "what is the largest number this instrument could ever return".

---

## THE ORDER

Every line carries an ISO/IEC 14764 class (DECISION S92-4): **COR**rective (something is broken),
**ADA**ptive (the world moved), **PER**fective (it works, it could be better), **PRE**ventive
(nothing is broken yet).

**EXPECTED ITEM COUNT: 59 distinct numbered items between `## THE ORDER` and `## ARCHIVED.**
Generation 18 held 53. This close CLOSED TWO items, both archived below - section 7's render
clock and `gni_state.py`'s `--session` default - and opened eight. Their ids are deliberately
NOT repeated here: a closed id cited in the queue counts as a queue item, which is how the two
counts first disagreed at 61 and 64 while this file was being assembled. The mission was a ROADMAP ROW, not an order item, so it is not counted as a
closure; generation 18 said the same thing about its own mission and that phrasing is kept
deliberately. Every id is bolded so the published command is true of the file it sits in, and a
second differently-shaped scan is printed beside it to reconcile against (R-S98-6):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S100.md \
  | grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l
sed -n '/^## THE ORDER/,/^## ARCHIVED/p' docs/GNI_TARGET_AND_ORDER_S100.md \
  | grep -oE '[0-9]+\.[0-9]+' | sort -u | wc -l
```

Both must print **59**. If they disagree, an id is unbolded or a decimal has entered the prose,
and the count is not to be trusted until they agree.

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

### ROOT 6 - FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM - **RE-RANKED UP (S99)**

**RE-RANK, with the reason generation 18 owes for it.** This root sat below ROOT 5 for four
generations as a storage-and-backup root. S99 measured that it also holds a LIVE CAPABILITY GAP:
the two 30-minute crons deliver about a third of their declared slots, and the guarantee GNI
publishes about its own detection latency rests on the cadence that is not happening. That is
target-bearing, not housekeeping.

- **6.11** **NEW (S99)** [MEASURED] - COR - **THE PROMISE AND THE CADENCE DISAGREE BY AN ORDER OF
  MAGNITUDE.** The heartbeat is designed to wake the adaptive pipeline the moment the escalation
  delta crosses its threshold, and the whole crisis posture rests on a 30-minute watch:
  `gni_heartbeat.yml` declares `0,30 * * * *` and `monitoring_pipeline.py` is the zero-Groq
  watcher behind it. The March-2026 rules that state this IN WORDS are deliberately NOT cited by
  id here - two of the three are absent from the register, which is item **5.37**.
  Measured over 16 complete days (`docs/gni_runtime_snapshot_S99.json`):
  `gni_heartbeat.yml` delivered 282 of 768 declared slots, `gni_selfcheck.yml` 292 of 768, and the
  per-day figure runs from 4 percent to 77 percent. Real spacing between heartbeats is 2-7 hours.
  Nothing published anywhere states this. **The question the item asks is NOT "how do we make
  GitHub faster" - there is no lever there. It is: what cadence does GNI actually have, and what
  should it therefore PROMISE?** Answer that before changing any cron. Kin of **9.11**/**9.12**:
  a published figure that no longer describes the system.
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
- **6.8** OPEN (S90) - ADA. Heartbeat standdown suspends a block of zero-Groq checks daily.
  NARROWED (S99): this was the obvious candidate for **6.11** and it is NOT the cause. The
  standdown is ~4h15m/day = ~17 slots per 48 hours, against 66 unexplained; and it suspends
  CHECKS INSIDE a run, which still appears in the run list. Ruled out by arithmetic, not by
  opinion. The item stands on its own original merit (a rationale that cites token collision for
  a zero-Groq workflow).

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
- **5.37** **NEW (S99)** [CAUGHT BY THE DETECTOR] - COR - **TWO MORE UNREGISTERED RULE IDS, AND
  C1 FAILED THIS CLOSE'S OWN DRAFT OVER THEM.** Generation 18's first draft cited three March-2026
  heartbeat/adaptive rule ids recovered from the session records; `tools/gni_rule_checks.py` C1
  failed on two as unregistered and unmanifested BEFORE the docs commit. Same class as the eight
  S90 recovered into PART 0 - now ten. The citations were removed rather than the ids invented:
  DECISION S90-4 ruled that guessing an id repeats the failure being fixed. WHAT IS OWED: recover
  both from the session records with their evidence and enter them in PART 0, or declare them lost
  in writing. Their subject is the cadence promise in **6.11**, so the two travel together.
  FOR THE RECORD: the detector S98 spent a whole session making green just failed the session that
  wrote it. That is the first time a check in this repo has caught its own close.
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
- **5.18** OPEN (S93) - PER. Unread wrongness ledgers. Discharged once this close by hand: the
  session record is what ruled out **6.8** as **6.11**'s cause.
- **5.19** OPEN (S93) - PER. R-S91-4's disproven evidence.
- **5.5** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.6** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.7** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.8** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.11** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**
- **5.12** OPEN - PER. **RETIRE CLAUSE DUE - AND UNDISCHARGEABLE AS WRITTEN.**

**THE SIX LINES ABOVE ARE A DEBT THIS GENERATION IS RECORDING, NOT PAYING.** The retire clause
says an item unworked below the line for three regenerations is CLOSED as accepted or PROMOTED
with a written reason, and dropping one silently is neither. Generations 16 and 17 carried
**5.5**, **5.6**, **5.7**, **5.8**, **5.11** and **5.12** as the bare line "Carried unchanged from
generation 15" - so the current order no longer states what they ARE. Generation 18 cannot close
or promote an item whose text it does not hold, and inventing one would be R-S98-1's disease
(a compression that replaced its own subject). **S100 discharges this by reading
`GNI_TARGET_AND_ORDER_S95.md` or earlier for their full text, then closing or promoting each in
writing.** Recorded as a debt so that the next close cannot inherit it silently.

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

## ARCHIVED - TWO ITEMS CLOSE INTO IT THIS GENERATION

Archived is not closed and not solved: not worked under this target, not re-ranked each close,
not re-read at open. Anything here returns only by a new measurement and a ruling.

| what | why archived |
|---|---|
| **ROOT 1** | CERTIFIED for content and ordering (S96). |
| **ROOT 8** | discharged in part at S91; the rest waited five generations under a target it does not serve. |
| the published band table | wrong in two of five rows - real, measured, not reachable before roadmap 2. |
| the dependency manifest | a roadmap-2 by-product. Note (S99): `GNI_ARCHITECTURE` section 7.3 cites an item in the six-range that this order does not carry - a dangling item citation, the order-file twin of what C1 checks for rule ids. That number is therefore NOT reused; S99 opened **6.10** and **6.11** instead. The exact id is in `GNI_ARCHITECTURE` section 7.3, deliberately not repeated here so the count commands stay true. |
| `mad_runner.py` unordered `limit(50)` | kin of R-S92-2, no consumer waiting. |
| **5.33** section 7's own clock | CLOSED S100 at `3268c14`. The stamp carries HEAD, the workflow file count and an EOL-normalised manifest md5; byte-identical on two renders two seconds apart, and the md5 MOVES when a workflow changes. |
| **5.34** `--session` default=94 | CLOSED S100 at `3268c14`. Now `required=True`; a bare invocation exits 2. |

**LEFT THE ARCHIVE THIS CLOSE: the lateness band.** It was archived because "a free-tier
scheduler gives no timing guarantee". A new measurement met the ARCHIVED section's own return
condition: the free tier gives no DELIVERY guarantee either, that is a different property, and it
had never been measured. It returns as items **6.10** and **6.11**.

`docs/GNI_RULE_CHECKABILITY_S95.tsv` remains RETIRED (S96) - on disk, out of the queue.

## CHANGED THIS REGENERATION

- **DECISION S99-1 (Claude, delegated by James with "your call").** The section 5 / 6 / 7 boundary,
  written BEFORE the first line of the generator: section 7 is what is DECLARED (workflow YAML +
  `gh secret list`), section 6 is what ACTUALLY RAN (Actions run history), section 5 is what is
  WRITTEN (the AST). Section 6 does NOT answer "what calls what" even though generation 17's
  mission text used that phrase - `gni_state.py:233` and section 5's own planned contents already
  assign `who calls it` to section 5, and two sections answering one question is a routing error.
  Chosen over "source-based call chains" (needs S100's AST early, and publishes reachability as
  if it were execution) and over "both, by scenario" (depends on a section 5 that does not exist).
- **DECISION S99-2 (Claude, delegated).** The generator SPLITS harvest from render. `--harvest`
  calls `gh` and writes a git-tracked snapshot; the render reads only that snapshot. Chosen over
  calling `gh` inline, which cannot satisfy "unchanged tree reproduces byte-identically" because
  the evidence changes every 30 minutes, and over a manual harvest outside any tool, which makes
  the harvest a habit rather than an artifact. Cost accepted: one 182 KB file per session, filed
  as **5.36**.
- **DECISION S99-3 (James).** Section 6.1 publishes the per-day delivery DISTRIBUTION beside every
  window figure. Chosen over a bare window ratio, which put a published figure in the GRAVEYARD at
  DECISION S90-3, and over "a last-N-days ratio", which needs a hand-written N and would trip C5.
  Nothing is hand-written: the spread is derived from the same per-day table section 6.4 prints.
- **DECISION S99-4 (Claude, reversible).** Lateness is attributed by ORDERED MATCHING and published
  only where delivery was complete. The nearest-preceding-slot method is rejected IN the section
  and re-probed on every run, because it is bounded by slot spacing and reported a 365-minute lag
  as 5 minutes. Where no pairing exists, section 6 prints the reason instead of a number.
- **DECISION S99-5 (Claude, reversible).** Runs are attributed to the SLOT they served wherever a
  pairing exists, not to their creation day. Creation-day attribution published 114 percent for
  `gni_market.yml`. The fallback is named inside the output rather than left for a reader to find.
- SHIPPED: **roadmap 2 row 2** - `2bfef91`, CI green at JOB level (run `33851242047`,
  `harnesses success` + `rule_checks success`). `tools/gni_runtime.py`,
  `docs/gni_runtime_snapshot_S99.json`, section 6 in `docs/GNI_ARCHITECTURE_S99.md`.
- CLOSED: **nothing**. rho = **0 / 7** this generation. The mission was a roadmap row rather than
  an order item, so the queue grew by construction; recorded plainly because a ratio dressed up is
  the loop the discovery policy exists to catch.
- NEW: **5.33**, **5.34**, **5.35**, **5.36**, **5.37**, **6.10**, **6.11**. **5.37** was opened
  by the detector failing this close's own draft, not by a session reading code.
- RE-RANKED: **ROOT 6** moves above ROOT 5, with the written reason in the root itself - it now
  holds a live capability gap, not only storage and backup.
- UN-ARCHIVED: the lateness band, by measurement, per the ARCHIVED section's own return condition.
- RECORDED AS A DEBT, NOT PAID: the retire clause on **5.5**, **5.6**, **5.7**, **5.8**, **5.11**
  and **5.12**. Their text was compressed away before generation 16; S100 reads
  `GNI_TARGET_AND_ORDER_S95.md` or earlier and closes or promotes each in writing.
- NOT DONE, AND DECLARED RATHER THAN SKIPPED: `npm run build` before the mission commit. CONTRACT
  requires it; this commit touched only `tools/` and `docs/` and no file under `src/`. Whether the
  rule should be scoped to src-touching commits is a CONTRACT question and is James's, not mine,
  so the contract is unchanged at v10 and the omission is on the record instead.

## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped - this generation's copy was verified against
generation 17's published md5 BEFORE the file was written, and again inside the assembled file
(R-S95-1). The item count carries two commands beside it and both were run on the ASSEMBLED file,
not on a draft: they disagreed at 52 against 56 on the first attempt, four bare decimals had
entered the prose, and the prose was rewritten rather than the command weakened (R-S98-6).
Freshness confers no priority: an item found today does not outrank an item found in June unless
a measurement says so.
