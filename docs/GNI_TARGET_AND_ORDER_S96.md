# GNI TARGET + WORKING ORDER
**GENERATION 16 - 2026-09-03 (S96 close). SUPERSEDES generation 15 (`GNI_TARGET_AND_ORDER_S95.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.
**THIS IS A PHASE-TRANSITION REGENERATION (CONTRACT PHASE TRANSITION, Protocol v12 PART C 4a).**
Every surviving item below was RE-CLASSIFIED at this close under ISO/IEC 14764 and nothing was
inherited. Carried items are restated in ONE line each with their class; generation 15 holds the
full prior text and is in git. An item that is not on this list is CLOSED, ARCHIVED or RETIRED,
and each of those appears by number in CHANGED THIS REGENERATION. Nothing left silently.

---

## NEXT SESSION'S MISSION (S98 - there is no S97 build session)

**Make the detector GREEN. Ship 5.14 + 5.17 + 9.15, then C6 (map staleness) and M4 (generator
naming) on top of the same commit series.**

WHY THIS IS TOP. It is JAMES'S roadmap 2, row 1 (DECISION S96-1). `harnesses` has been RED on
every push for three sessions and the handoff has carried a trap saying so THREE TIMES. A
detector that is red on every push is not a detector: today it reads `fail=1`, and on the day a
real regression arrives it will also read `fail=1`. The difference is zero. Every later row of
roadmap 2 builds NEW generated code, and new code is exactly what a working detector is for.

**Definition of done:** one push to `main` with no functional change reaches
`conclusion: success` with BOTH jobs green, verified job-level, never run-level:
`gh run view <id> --json jobs --jq '.jobs[] | [.name,.conclusion] | @tsv'`.
Then ONE input is broken deliberately and the same command shows RED. Green alone is not a
cert; the pair is (R-S90-1).

**Scope, stated narrowly:** 5.14 and 5.17 are the mission. 9.15 rides along because it is three
lines and has been carried as a trap three times. C6 and M4 are on the list because both are
S96's own debts and both are small; if the session runs long, C6 and M4 move to S99 AS A
WRITTEN DECISION, not by silence.

**Read before designing 5.14:** DECISION S91-2 ruled that the guard's PLACE is a design
question needing options - harness, or `compute_depth`, or the caller. It touches production.
Lettered options with `LINEAGE:` lines, and James rules.

## TARGET - UNCHANGED (this close ended a ROADMAP, not a target)

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

James ruled at the S96 close: no new target. DEGRADE-SILENT - a run that reports SUCCESS while
producing nothing - sits UNDER this target, so the target that would catch it is the one already
declared. What was declared ACHIEVED is DECISION S93-2's four-session roadmap, with evidence:
`944c4f0` - `44a3cba` - `b639b54` - `09588b2`. The declaration and its ARCHIVE live in
`GNI_ARCHITECTURE_S96.md`, and roadmap 2 is declared there WITH ITS WRITTEN COMPLETION TEST
(CONTRACT v10, born this close).

**DEFINITION OF DONE - status at this regeneration:**
- the arbitrator reads what it claims to read - ROOT 1 CERTIFIED for content and ordering.
  **ARCHIVED at this close** by James's ruling; see ARCHIVED ROOTS.
- the escalation score carries information - ROOT 8. **ARCHIVED at this close.** 8.5 was
  discharged at S91; what remained was never going to be reached under this target.
- the grounding gate measures reading, not existence - ROOT 7 IMPORTANT, still blocked on
  7.1's instrument. Unchanged.
- the public surface matches the configuration - **ROOT 9 stays TOP**, and now carries 9.19,
  the first item under this target about a RUN's own reported status rather than a page's copy.

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

**md5 OF THIS SECTION, WITH THE COMMAND THAT PRODUCES IT (R-S96-2, item 5.28):**
```bash
sed -n '/^## .*GRAVEYARD/,/^<!-- GRAVEYARD-END -->/p' docs/GNI_TARGET_AND_ORDER_S96.md | md5sum
```
Expected: `3e8ac222c6ef212261676c02d7d56f6f`. Generation 15 published `203d371bc1d5522cd259ed1daf4bb0ab` with no
command; no span of that file reproduces it. A checksum without its command is decoration.

## THE CROSS-ROOT DIAGNOSIS (carried from generation 7 — now with five instances)

> **GNI repeatedly measures what it has already guaranteed itself, and publishes the result as
> a fact about the world.**

| instance | what is measured | what it actually is |
|---|---|---|
| ROOT 7 | "the span exists in the pool" | reported as "the agent read it" |
| 8.1b | `_high_escalation` True 6/6 | a crisis channel that cannot leave crisis mode |
| 8.1 | `diversity_bonus` = 3.0 in 175/191 | the S39 funnel quota (14/4/4) guarantees all three pillars |
| 8.9 | GEO pillar "active" 196/196 | GEO hits are 8–19 against a cap of 5 — the pillar cannot be inactive |
| 8.10 | PHI-003 gate "protecting" the score | it has never fired in 196 runs; `combo_bonus < 3` mutes it exactly when combos fire |

Its use is predictive — when a metric is >90% constant, ask WHO GUARANTEED IT before tuning it.

**S89 NOTE — no sixth instance was added, and that is the finding.** S89 re-derived this
diagnosis from `design_bench`'s own banner and was about to file it as a NEW item 8.11, twenty
turns after reading this very table at session open. The June-01 record had reached the same
conclusion five months earlier. See R-S89-1.

**S90 NOTE — the diagnosis acquired a CONSEQUENCE, not a sixth row.** Because escalation is
constant at 10.0/CRITICAL, S90 shipped two fixes (9.9, 9.10) whose correct and incorrect
outputs are IDENTICAL on live data. See R-S90-1.

**S91 NOTE — 8.1b's row is now MEASURED ON THE INPUT, and the instance is confirmed.**
`SELECT escalation_level, risk_level, count(*) FROM reports GROUP BY 1,2` over the whole
199-row corpus: `CRITICAL` 198 rows at `escalation_score` **exactly 10.0** (min = max), and
ONE `ELEVATED`/`Medium` row at 5.0 (2026-06-22). The "True 6/6" of 8.1b was a sample; the real
figure is **198/199 = 99.5%**. Also Protocol 8h: the gate is three OR'd clauses and TWO OF
THEM HAVE NEVER DECIDED A RUN — every row with `risk_level` High/Critical also has
`escalation_level` CRITICAL, so the escalation clause alone has always carried the decision.

---



## THE ORDER - RE-CLASSIFIED AT THE PHASE TRANSITION

Every line carries an ISO/IEC 14764 class (DECISION S92-4): **COR**rective (something is
broken), **ADA**ptive (the world moved), **PER**fective (it works, it could be better),
**PRE**ventive (nothing is broken yet). The class is the first thing re-read when ranking,
because "urgent" is a feeling and a class is a claim about what happens if nobody acts.

**EXPECTED ITEM COUNT: 36 distinct numbered items between `## THE ORDER` and
`## ARCHIVED AT THIS CLOSE`.** Method beside the number, so a later session re-greps instead of
recalling - and note that several items share one line, so counting LINES gives a different and
wrong answer (S96 predicted 41 by counting lines and the correct method returned 36):

```bash
sed -n '/^## THE ORDER/,/^## ARCHIVED AT THIS CLOSE/p' docs/GNI_TARGET_AND_ORDER_S96.md \
  | grep -oE '\*\*[0-9]+\.[0-9]+' | sort -u | wc -l
```

### ROOT 9 - PUBLIC COPY AND REPORTED STATUS DRIFT FROM WHAT WAS MEASURED - URGENT - **TOP**

- **9.19** **NEW (S96) [MEASURED elsewhere, UNMEASURED here] - COR - DEGRADE-SILENT.** A run in
  which `ctx-trim` leaves ZERO articles still reports SUCCESS. The status GNI publishes about
  its own run disagrees with what the run produced, which is this target's exact shape one
  layer below the web pages. Carried in from the S97 advisory session. FIRST MOVE is to
  measure, not to fix: find a run with `ctx-trim@0` and read what it reported.
  ROOT 6 is the CAUSE (a free-tier limit degrading output); ROOT 9 is the DEFECT (the silence).
- **9.15** **OPEN (S93) - PRE - carried as a trap three times, which makes it an unregistered
  rule (Protocol PART B).** `gni_ci_harness.yml` passes NO secrets, so a harness importing
  `mad_protocol` resolves `MODEL` to the dead `llama-3.3-70b-versatile` string. **NOT archived** -
  James's ruling at the S96 close. Rides with S98's mission.
- **9.16** **OPEN (S93) - COR.** Order and handoff both said "all 8 workflows on `setup-python`";
  the records are from the `setup-python` side only.
- **9.17** **OPEN (S94) - COR.** Same shape as 9.16, one generation later.
- **9.18** **OPEN (S95) - COR.** Carried from generation 15 unchanged.
- **9.5** OPEN - COR. Eight unresolved S69 census flags; F14 renders BEARISH over a stale basis.
- **9.11** OPEN - COR. `research/page.tsx:105` publishes `Groq 100K tokens/day` against a May record.
- **9.12** OPEN [PROPOSED, not measured] - COR. `/about/devops` compares a three-account token SUM.

### ROOT 5 - INSTITUTIONAL HARDENING - now the ROADMAP'S OWN ROOT

Roadmap 2 lives here. This ROOT stops being "below the line" at this close: three of four
roadmap-2 rows land in it.

- **5.14** **OPEN (S91) [MEASURED] - COR - S98 MISSION.** Three of ten runnable harnesses are
  dead, one cause: `all_articles=[]` meets a depth solver added by `c3ce662` (2026-06-27).
  DECISION S91-2: the guard's PLACE needs lettered options; it touches production.
- **5.17** **OPEN (S93) - COR - S98 MISSION.** A detector RED on every push is background noise.
  Allowlist, paired with 5.14.
- **5.26** **NEW (S96) [MEASURED] - PRE - C6, THE MAP HAS NO GUARD.** `docs/GNI_MACRO_MAP_S95.md`
  was committed at `09588b2` reading 159 markers. By the end of the SAME session the register
  held **164** (61 CHECKABLE / 103 not) and the map was stale - the exact disease the map was
  built to diagnose in the TSV, contracted on day one. Nothing turns red. Check: the map's
  stamped source count equals the register's live count, else `rule_checks` RED. This closes the
  roadmap's own loop - S93's detector watches S96's map, S95's fixture watches the detector.
- **5.27** **NEW (S96) [MEASURED] - PER - M4, THE GENERATOR NAMES ITS OWN OUTPUT.**
  `tools/gni_macro_map.py` names the artifact after the REGISTER generation it read, so at the
  S96 close it wrote `GNI_MACRO_MAP_S95.md` - outside "highest number = live". `git mv` does not
  fix it; the next run undoes the rename. Fix is a required `--session` argument plus a
  `GENERATED from <register>, <N> markers` stamp. **Note the trap in the trap:** when the
  register IS regenerated in the same session the two numbers coincide and the defect is
  invisible - it was invisible in exactly that way while this order was being written. R-S96-1.
- **5.28** **NEW (S96) [MEASURED] - COR - AN UNVERIFIABLE CHECKSUM.** The S95 LOAD CHECK ordered
  the graveyard carried with md5 `203d371bc1d5522cd259ed1daf4bb0ab`. Fourteen spans of the live
  file were tried - section, table, rows only, with and without the heading, LF and CRLF - and
  none reproduces it. Two clauses later the same line says the METHOD is written beside the
  number. Fix: every checksum a handoff asks a later session to verify ships with its literal
  command. This generation does that; see the GRAVEYARD note. R-S96-2.
- **5.29** **NEW (S96) [MEASURED] - PER - THE REGISTER HAS SIX ENTRY SHAPES.** `- **ID** -`,
  `**ID** -`, `ID: text`, `- ID (Title):`, `## ID - TITLE`, `- **ID - Title:**`. Four CHECKABLE
  markers sit BELOW the heading that follows their rule (`:289`, `:589`, `:1305`, `:1347`) -
  R-S93-1's marker reads as if it belonged to S94. NN-PHI-1..7 share one paragraph, so three
  markers cannot be bound to an owner by any parser. A first parser bound 103 of 159 markers to
  ONE rule and reported nothing. **Do not fix by rewriting the register**; regularise the shape
  at the next close that touches it. R-S96-3.
- **5.22 / 5.23 / 5.24 / 5.25** OPEN (S95) - PER, PER, PER, PRE. Carried unchanged: console
  fragility of `tools/*.py`; C5's blind spot; and generation 15's two remaining new items.
- **5.20** PARTIALLY DISCHARGED (S94/S95) - PRE. The fixture exists and runs first in CI.
  What remains is the control probe's own evidence.
- **5.21** OPEN (S94) - PRE. No `.gitattributes`. S95 wrote `\r\r\n` across 1235 lines with all
  five checks green. Still unshipped, and it is a precondition for trusting any md5 of a
  checked-out file - see 5.28.
- **5.15 / 5.16 / 5.18 / 5.19** OPEN (S93) - PER. Selftest coverage, `__main__` blocks outside
  `tests/`, unread wrongness ledgers, R-S91-4's disproven evidence.
- **5.5 / 5.6 / 5.7 / 5.8 / 5.11 / 5.12** OPEN - PER. Carried unchanged from generation 15.

### ROOT 7 - THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" - IMPORTANT

- **7.1** PARTLY PAID (S86) - COR. `checked_spans` computed and discarded at the print. The
  instrument everything else in this ROOT waits on.
- **7.2** BLOCKED - COR. Fix shape undecided; per-speaker baskets are in the GRAVEYARD.
- **7.3** PARTLY DISCHARGED (S86) - PER. Unchanged.
- **7.4** OPEN (S93) [UNMEASURED, n=2] - COR. `GROUNDING SHADOW` counts disagree across instruments.

### ROOT 6 - FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM

- **6.5** OPEN - COR - **THERE IS NO BACKUP.** Still the highest single-point loss in the system.
  It has been the highest for six generations and has never been the mission. Say that plainly
  rather than re-ranking it again.
- **6.3** RE-SPECIFIED (S89) - ADA. Meter 113 MB vs 87 MB of tables; 26 MB unexplained.
- **6.4** OPEN - ADA. L5 exposure when Supabase 402s.
- **6.8** OPEN (S90) - ADA. Heartbeat standdown suspends ~4h15m/day of zero-Groq checks.

### ROOT 2 - LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE - IMPORTANT

- **2.1** HALF-RULED (S86) - COR. Clause 2, LABELED coverage, unmeasured.
- **2.2** BLOCKED on 2.1 - PER. **2.3** NARROWED (S87) - PER. **2.4** ONE READ FINISHES IT - COR:
  `/stocks` may render frozen prices; render path read, fetch path not.

### ROOT 3 - FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE - IMPORTANT

- **3.1** WIDENED (S86) - COR. `conf = 0.5` exactly on Jun 11 and Jul 7.
- **3.2** OPEN - ADA. `data_era` column + tagging. Originally due ~Aug 2. **The overdue count is
  deliberately not restated here**: LIFECYCLE clocks are PAUSED (DECISION S92-2) and a number
  that keeps growing under a stopped clock is theatre.

### ROOT 4 - COST AND HEADROOM - IMPORTANT

- **4.1** OPEN - COR. C2 solver recalibration; `ctx-trim` fired again at S87. **Now paired with
  9.19** - the same trim, seen from the cost side.
- **4.4** OPEN - PER. Measure chars/token PER POSITION. `//3` is SAFE; do not move to `//4`.
- **4.6** OPEN (S90) - ADA. `gni_mad` 28,694 (Jun) to 83,479 (Jul) to 68,509 (Aug).

### LIFECYCLE + SECURITY - target-independent, never ranked away

**CLOCKS REMAIN PAUSED (DECISION S92-2).** 22 secrets stored. Nothing is due, nothing is
overdue, and no session may raise an item here as "overdue" until James restarts the clocks.
The pause is itself the state, and it is recorded so that a later session does not rediscover
the deadlines and treat them as live.

---

## ARCHIVED AT THIS CLOSE (James's ruling, DECISION S96-1)

Archived is not closed and not solved. It means: not worked under this target, not re-ranked
each close, not re-read at open. Anything here returns only by a new measurement and a ruling.

| what | why archived |
|---|---|
| **ROOT 1** (1.6, 1.11, 1.12, 1.13, 1.15) | CERTIFIED for content and ordering. What remains is refinement of a certified path. |
| **ROOT 8** (8.1a, 8.1b, 8.1c, 8.7, 8.8, 8.10) | 8.5 discharged at S91 by measurement. The rest has waited five generations under a target it does not serve. |
| **9.13** | The published band table is wrong in two of five rows - real, measured, and not reachable before roadmap 2. |
| **6.9** | No dependency manifest. Figures are generated now; the manifest is a roadmap-2 §5 by-product. |
| **6.10** | Lateness band +4h07m..+6h58m, n=9. A free-tier scheduler gives no timing guarantee; measuring it further changes nothing. |
| **6.11** | `mad_runner.py:104` unordered `limit(50)`. Kin of R-S92-2, no consumer waiting. |

**`docs/GNI_RULE_CHECKABILITY_S95.tsv` is RETIRED** - not deleted. The macro map reads the
register directly, so the TSV has no consumer, and it was already five rows behind the register
on the day it was written. It stays on disk as the S95 artifact it is; it leaves the order. Any
session that reads it must read the register instead. (Same treatment as
`SUBPAGE_CERTIFICATION.md`; DECISION S92-2's principle - retire from the queue, never from disk.)

---

## CHANGED THIS REGENERATION

- **DECISION S96-1 (James).** PHASE TRANSITION executed. DECISION S93-2's roadmap declared
  ACHIEVED with four commits; the arc archived; TARGET unchanged (TRUTHFULNESS OF OUTPUT);
  roadmap 2 declared (S98 detector - S99 §6 - S100 §5 - S101 SLO) WITH a written completion
  test; ROOT 1, ROOT 8, 9.13, 6.9, 6.10, 6.11 archived; 9.15 explicitly NOT archived.
- **DECISION S96-2 (James).** CONTRACT to v10: a declared roadmap carries its own written
  completion test, stored in ARCHITECTURE beside the roadmap. Chosen over homing it in
  GNI_RULES, because a roadmap is declared at CLOSE and the close reads CONTRACT.
- **DECISION S96-3 (James, on S96's counter-proposal).** M4 moves to S98 with C6: renaming the
  map by hand is undone by the next run, so the fix is code, and code is not close work. The
  S96 close carries the exception in writing instead (5.27).
- **DECISION S96-4 (James).** Protocol to v12: PART C gains step 4a ROADMAP CHECK. Steps were
  NOT renumbered - CONTRACT and Protocol both cite "PART C step 5" and "step 13" by number.
- CLOSED: **S96's mission** - `09588b2`, `tools/gni_macro_map.py` + the generated map, cert
  passed with three negative controls.
- CLOSED: nothing else. No item was closed by argument this session.
- NEW: **9.19** (DEGRADE-SILENT), **5.26** (C6), **5.27** (M4 naming), **5.28** (unverifiable
  checksum), **5.29** (six entry shapes). rho = **5 / 1** this generation.
- ARCHIVED: ROOT 1, ROOT 8, 9.13, 6.9, 6.10, 6.11 - see the table above.
- RETIRED: `GNI_RULE_CHECKABILITY_S95.tsv`, with the reason written.
- CORRECTED: the banked **53 CHECKABLE / 106 not** appears in generation 15 at four places and
  in `HANDOFF_S95.md` at three. The measured figure at the S95 close was **57 / 102 of 159**.
  Both live documents are superseded by this generation and by `HANDOFF_S96.md`. The commit
  message of `6989fad` carries the wrong figure permanently and cannot be edited; that is the
  record. Generation 14 and earlier keep their own text - history is not rewritten.
- RE-CLASSIFIED: all 41 surviving items, under ISO/IEC 14764. Nothing was inherited.

## HOW THIS FILE IS MAINTAINED

Regenerated at every close, dated, superseding, never appended. The GRAVEYARD is the single
exception and is copied BY BYTES, never retyped (CONTRACT v9's method note). The item count
above carries its grep beside it. Freshness confers no priority: an item found today does not
outrank an item found in June unless a measurement says so.
