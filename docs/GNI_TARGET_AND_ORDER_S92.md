# GNI TARGET + WORKING ORDER
**GENERATION 12 - 2026-09-01 (S92 close). SUPERSEDES generation 11 (`GNI_TARGET_AND_ORDER_S91.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S93)

**Run the test harnesses in CI.** A workflow that executes `ai_engine/tests/dryrun_*.py`
on every push and fails the run on a non-zero exit.

WHY THIS IS TOP. Ten harnesses and 42 `__main__` selftests exist; NONE is executed by any
workflow. Three harnesses died on 2026-06-27 (`c3ce662`) and failed LOUDLY, unread, for two
months (item 5.14). This is the cheapest possible fix for the failure class that has cost
GNI the most, it is Layer 0 of the tiered-repair design in ARCHITECTURE section 8.4, and it
costs nothing: the harnesses are offline by design - no Groq call, no DB write.

**Definition of done:** a pushed commit whose CI run shows the harness job RED because of
the three known-dead harnesses, then GREEN after 5.14's fix - or RED-then-documented if 5.14
is deferred. A green-on-first-try result means the job is not actually running them; verify
by making one harness fail on purpose first (R-S90-1: a cert must discriminate).

**NO FIRST MOVE AT OPEN.** The credential block that headed S91 and S92 is struck - see
DECISION S92-1 and S92-2 below. Open with the mission.

---

## TARGET (unchanged — no phase transition this close)

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**DEFINITION OF DONE — status at this regeneration:**
- the arbitrator reads what it claims to read — ROOT 1 CERTIFIED for CONTENT; 1.14 closed at S89.
- the grounding gate measures reading, not existence — ROOT 7 IMPORTANT (DECISION S90-2),
  blocked on 7.1's instrument. Unchanged this close.
- the escalation score carries information — **ROOT 8: 8.5 DISCHARGED at S91 by a two-arm
  dry-run. Both arms of the NN-5 gate are now proven to execute and to differ.** What remains
  is 8.10 — which S91 proved is NOT discharged by the same measurement (DECISION S91-1).
- the public surface matches the configuration — **ROOT 9 stays TOP. S91 added two items to
  it (9.13, 9.14), both found while working ROOT 8.** 9.14 is S92's mission.

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

## THE ORDER

**CLOSED AT S92 - `416a2fb`, `9d2dba8`, browser-certified on live data:**
- **9.14 CLOSED.** `limit(5)` -> `limit(1000)`, `select('*')` -> five columns, and the page
  gained a block selecting rows BY DIVERGENCE (stored interval != published band).
- **9.9 CERTIFIED.** `/autonomy` renders `1.5h` and `1h` - the stored values. The deleted
  constant ladder would render `2h` and `30 min`. It discriminates.
- **9.10 CERTIFIED.** `HIGH` and `CRITICAL` come from the `escalation_level` column.
- **9.13 now has PUBLISHED evidence** - the same page shows the band table and the two runs
  that contradict it. Still open: the band table remains wrong in 2 of 5 rows.
- **NEW: the ARCHITECTURE document** (`docs/GNI_ARCHITECTURE_S92.md`, arc42). The S92
  diagnosis D1-D7 lives in its section 11 and is NOT duplicated here - one finding, one home.
  Sections 5, 6 and 7 are empty by design and are filled by the S94 generator.
- **NEW WORK, ranked below the S93 mission:** S94 `tools/gni_state.py` generating
  ARCHITECTURE 5/6/7 - S95 classify all 134 rules checkable/not and make the top five
  executable - S96 the macro time-series map. One mission each.

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION · URGENT · **TOP**
*Holds the top slot. S91 did not work this root as its mission but added two items to it while
working ROOT 8, and one of them (9.14) is S92's mission because it unblocks two shipped items.*

- **9.1 / 9.2 / 9.3 / 9.4 / 9.6 / 9.7 / 9.8** CLOSED in earlier sessions. 9.3, 9.7, 9.8
  certified in a browser at S90; 9.6 closed except two unrecovered IDs (`LR-101`, `GNI-R-122`).
- **9.5** OPEN — eight unresolved S69 census flags; F14 (`/comparison` renders BEARISH over a
  NEUTRAL verdict) is the ugly one. RE-CERT never ran. Unaudited since July. This is an AUDIT,
  not a fix — scope it as a session, not a task.
- **9.9** **SHIPPED (S90) `99a9dac` + `59d57ac`, CERT BLOCKED — but NOT by 8.5.** S91 measured
  the blocker precisely: `/autonomy` and `/health` read `frequency_log[0]`, which is
  `CRITICAL`/`0.5`, where `formatInterval(0.5)` = `30 min` = `intervalMap['CRITICAL']`. The
  outputs coincide. **The discriminating rows EXIST** — see 9.14.
- **9.10** **SHIPPED (S90) `59e4023`, CERT BLOCKED, same cause as 9.9.**
- **9.11** OPEN — `research/page.tsx:105` publishes `Groq 100K tokens/day`; the May record says
  85,000. Needs a 429 body; forcing one endangers a sacred run. Read it opportunistically.
- **9.12** OPEN [PROPOSED, not measured]. `/about/devops` compares a THREE-ACCOUNT token SUM to
  a PER-ACCOUNT ceiling, so the bar reads 98.7% full when the worst account is at 67%. Seen in
  a browser only; the render path has NOT been read.
- **9.13** **NEW (S91) [MEASURED].** The published band table is WRONG IN TWO OF FIVE ROWS.
  `autonomy/page.tsx:146` and `health/page.tsx:197` both publish
  `CRITICAL=30min - HIGH=2h - ELEVATED=4h - MODERATE=6h - LOW=12h`. The backend
  (`frequency_controller.py`, `FREQUENCY_MAP` + `get_recommended_interval`) says
  **CRITICAL = 1.0h** (0.5 only when `score >= 9.5`) and **HIGH = 2.0h** (1.5 when
  `score >= 8.5`). So CRITICAL is wrong outright and HIGH is wrong for its upper half.
  `intervalMap` at `autonomy:66` and `health:163` carries the same two errors, and neither
  map has a `NONE` key though `FREQUENCY_MAP` does. **This is 9.10's twin: 9.10 deleted the
  frontend's score->level ladder, and this is the frontend's surviving level->interval ladder.**
  Rank: below 9.14 because 9.14 unblocks two certs and this one is a copy fix.
- **9.14** **NEW (S91) — S92's MISSION.** `api/health/route.ts:39` selects `frequency_log`
  with `.limit(5)`, and the five newest rows are all `CRITICAL`/`0.5`. The two stored rows that
  discriminate old code from new — `2026-03-22 CRITICAL/1.0` and `2026-05-01 HIGH/1.5` — are
  outside the window. Raising it makes 9.9's and 9.10's certs FREE and DISCRIMINATING
  (R-S90-1), with no live non-CRITICAL run needed. Read the other consumers of that route
  before changing the number (R-S55-1); `/autonomy` maps the array at `page.tsx:203`.

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT
*8.5 is DISCHARGED. The root's remaining open items are 8.1a/8.1b/8.1c, 8.7, 8.8 and 8.10.*

- **8.1** CLOSED (S86) — the audit. Saturation across three layers, confirmed by bytes.
- **8.1a** OPEN — D-11's feeds list misses three consumers: arb prompt L989,
  `nexus_analyzer:567`, `self_bias_gate:46`. Unchanged this close.
- **8.1b** OPEN — NN-5 is a deliberate hard-correction channel (`1da3dfe`) whose switch is
  stuck. **S91 re-measured the stuckness on the INPUT: 198/199 rows are CRITICAL at exactly
  10.0.** The switch stays stuck by design decision, not by neglect.
- **8.1c** OPEN and now MEASURED IN ISOLATION. Production figure unchanged
  (`constraint=1092` of `ctx_room=4762` on `33180919784`, ~23%). **S91 measured the branch's
  own contribution directly: 555 chars of arbitrator prompt on a stubbed 8-article run
  (`dryrun_nn5_gate.py`, A6).** The two numbers are not comparable as-is — the harness uses a
  short stubbed agent reply and `_compress(x, 60)` bounds each constraint — but the branch's
  cost is now a measurable quantity rather than an inference.
- **8.2** CLOSED (S87) — CERTIFIED 4/4. **8.3** RULED (S87) — see GRAVEYARD row 1.
- **8.4** CLOSED (S90), certified in browser. **8.6** CLOSED (S90), certified SQL + browser.
- **8.5** **CLOSED (S91) — DISCHARGED BY MEASUREMENT.** `33578de` adds
  `ai_engine/tests/dryrun_nn5_gate.py`: two arms, identical 8-article pool, differing only in
  the report's `risk_level`/`escalation_level`. CONTROL (`High`/`CRITICAL`) prints
  `NN-5: 2 hard constraint(s)` and the arbitrator prompt contains `HARD CONSTRAINTS`;
  TREATMENT (`Medium`/`ELEVATED`) prints nothing and the prompt contains none. TREATMENT still
  returns `mad_verdict='bearish'`, `mad_arb_failed=False` — **the gate closing does not break
  the protocol**, which is the load-bearing result. 6/6, EXIT=0, zero Groq, zero DB.
  **TREATMENT's values are not invented:** they are the one stored `reports` row in 199 for
  which the gate evaluates False (2026-06-22, score 5.0).
- **8.7** RE-SPECIFIED (S88). Score half CLOSED; the direction-neutral audit of published
  EVIDENCE STRINGS (`factors`, `signals_found`) is what remains. Unchanged.
- **8.8** OPEN — 19 keywords never fire in 192 runs: GEO 1, TECH 3, **FIN 15**.
  **DO NOT DELETE THEM** — their silence is the finding (Protocol 8h).
- **8.9** DE-SCOPED (S89). With list edits in the GRAVEYARD, the measurement has no consumer.
- **8.10** OPEN — PHI-003 has never fired in 196 runs. **NO LONGER PAIRED WITH 8.5**
  (DECISION S91-1): generation 10 said this item was "discharged by the same measurement", and
  S91 proved it is not — `dryrun_nn5_gate.py` exercises the NN-5 gate in `mad_protocol`, which
  never touches PHI-003. **The cheap route is now visible though: add a third arm to
  `dryrun_nn5_gate.py`.** The harness pattern is built, proven and committed; 8.10 needs the
  conditions that mute PHI-003 identified, then one arm. Also still open:
  `final_score = max(final_score, 1.0)` is an undocumented floor that min-raw 5.6 cannot reach.

### ROOT 1 — THE ARBITRATOR'S INTAKE · CERTIFIED FOR CONTENT AND FOR ORDERING
- **1.1–1.5 / 1.7 / 1.8 / 1.10 / 1.14** CLOSED in earlier sessions. **1.9** CLOSED AS ACCEPTED
  (S90, DECISION S90-1) — the retire clause discharged.
- **1.6** OPEN, confirmed 14/14 + 4/4 + 2/2, RE-CONFIRMED LIVE 2026-08-30:
  `ARB-ARRIVAL: ctx_chars=3790/3790 R1=DROPPED` while `/debate` publishes R1. Open since S83.
  A ROOT 9 defect wearing a ROOT 1 number — cross-listed, not re-homed.
- **1.11** OPEN, TRIGGER FIRED (S86), boundary pinned 39–41 (S87). Round-robin pillar fill.
  **Top open item in this root.**
- **1.12 / 1.13 / 1.15** unchanged from generation 10. 1.15 is the `str(0)` echo (F-86-1).

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM
- **6.1** CLOSED (S84). **6.6** CLOSED (S89). **6.2** DE-RANKED (S89) — runway ~550 days.
- **6.3** SIZE METER — RE-SPECIFIED (S89). Meter 113 MB vs 87 MB of tables; 26 MB unexplained.
- **6.4** L5 exposure when Supabase 402s. **6.5** **THERE IS NO BACKUP** — still the highest
  genuinely open item in this root.
- **6.7** **CLOSED (S91) — CERTIFIED ACROSS ALL EIGHT WORKFLOWS.** `e54afdf` (S90) pinned
  `gni_mad` and `gni_pipeline` to `checkout@v7` + `setup-python@v7`; S91 certified them on the
  first scheduled runs after the commit. `grep -c 'Node 20 is being deprecated'`:
  post-fix `33420536876` = **0**, `33422581858` = **0**; pre-fix controls `33318041130` = **8**
  and `33319340901` = **4**. **The order's banked "v4 control = 2" was wrong** — the control
  discriminates far more strongly than recorded, in the safe direction.
- **6.8** OPEN (S90) — the heartbeat standdown suspends ~4h15m/day of ZERO-Groq checks on a
  token-collision rationale that `GNI-R-114` contradicts. Only the adaptive TRIGGER needs
  withholding. The claimed 43-minute unguarded gap does NOT exist (retraction travels with it).

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · **IMPORTANT**
DE-RANKED at S90 (DECISION S90-2) with a checkable re-rank trigger. Untouched at S91.
- **7.1** PARTLY PAID (S86) — `checked_spans` computed and discarded at the print. **This one
  print is the root's critical path and the re-rank trigger.**
- **7.2** BLOCKED — decide the fix shape. Per-speaker baskets are in the GRAVEYARD.
- **7.3** PARTLY DISCHARGED (S86). Unchanged.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** HALF-RULED (S86) — clause 2 (LABELED coverage) unmeasured.
- **2.2** Build B only if 2.1's second clause triggers it.
- **2.3** NARROWED (S87) — remaining candidates are internal.
- **2.4** `/stocks` may render frozen prices. Render path read, fetch path NOT. One read finishes it.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** WIDENED (S86) — `conf = 0.5` exactly on Jun 11 and Jul 7.
- **3.2** `data_era` column + tagging. **Originally due ~Aug 2; now ~31 days overdue.**
  **LR-104 binds: schema work needs a session opening.** Recorded so the age is visible.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.1** C2 solver recalibration. `ctx-trim` fired again at S87, so not dormant.
- **4.2** CLOSED AS ACCEPTED (S86). **4.5** CLOSED (S89). **4.3** Groq TPD refills continuously.
- **4.4** Measure chars/token PER POSITION. `//3` is SAFE; do not move to `//4`.
- **4.6** OPEN (S90) — `gni_mad` 28,694 (Jun) -> 83,479 (Jul) -> 68,509 (Aug); `gni_pipeline`
  6,502 -> 15,980 -> 17,780; everything before June is the flat `6175`/`7433` reservation era.
  Cost is not stable across regimes and no item watches the trend.

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** `DEBT_REGISTER_S69.md` — one reader in five months is still not a register.
- **5.6** PARTLY PAID (S90). Register restructured into PART 1 (by TRIGGER), PART 2 (eight
  CLUSTERS), PART 3 (S89 verbatim). 134 rules registered, **18 cited** by the live document set.
  CLUSTER A holds ten rules and still fired twice at S90; that ratio is the open half.
- **5.7** BYTE-CONFIRMED (S88). `_lower`/`_upper` still render `--` on `/autonomy`.
- **5.8** OPEN — unnumbered items are invisible to the uniqueness assert and vanish. Four
  survivals in five sessions (S90 evidence). **S91 adds nothing to the count: every finding
  this session was numbered at this close.**
- **5.9** SHIPPED (S89). **5.10** CLOSED (S90). **5.12** OPEN (S90) — two unread registers.
- **5.11** OPEN, PROPOSED — reopen 5.2 (dead-symbol / unwired-module CI detector).
  **S91 MOVED THIS FROM SEVEN HAND-FOUND INSTANCES TO A MEASURED RATE — see 5.14.**
- **5.13** **CLOSED (S91) — PREMISE DISPROVEN BY BYTES.** The item said the register's
  header line 2 still read a stale model roster. `grep -n 'Sonnet 4.6\|Team Geeks'
  GNI_RULES_S90.md` returns NOTHING: S90's own restructure rewrote that header to
  `# Bro Alpha (James Maverick) + Claude - Reference by ID` in the same close that
  numbered the item. The defect was fixed and recorded as open by one session.
  Closed rather than retired: nothing is owed.
- **5.14** **NEW (S91) [MEASURED] — THREE OF TEN RUNNABLE HARNESSES ARE DEAD, ONE CAUSE.**
  `dryrun_false_neutral.py`, `dryrun_mad_redefinition.py` and `mad_protocol.py`'s own
  `__main__` selftest all call `run_mad_protocol(..., all_articles=[])`. Since `c3ce662`
  (2026-06-27) that function computes `_eff_n` from `all_articles` and calls `compute_depth`,
  which divides by `n_articles` — so an empty pool raises `ZeroDivisionError` **before the
  protocol is reached**. The harnesses were last touched `460ce84` (2026-06-21), six days
  BEFORE the wiring. They have been dead for over two months and nothing reported it.
  S89's record cites `dryrun_false_neutral`'s "16/16" as live evidence; that claim was true in
  June and is false now.
  **Measured, not guessed:** 10 harnesses classified for network use and then run with a
  90s timeout — 3 dead (all `ZeroDivisionError`), 7 green. `dryrun_two_account_split.py` also
  exits 1 but with a DIFFERENT cause and is not part of this item.
  **NOT FIXED THIS SESSION, deliberately — see DECISION S91-2.** The fix is a design choice
  between patching three callers and adding an `n_articles == 0` guard inside
  `mad_budget_solver.compute_depth`, and the second touches production. It needs a SWOT, not a
  session tail.
  **Also recorded, unmeasured:** 42 modules OUTSIDE `tests/` carry a `__main__` selftest,
  including `main.py`, `mad_runner.py` and `adaptive_pipeline.py`. None were run — running them
  would run the pipeline. That surface is untested and unmeasurable by the method used here.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away

**RULED AT S92 - THE CLOCKS ARE STOPPED. Read this before treating anything below as due.**
- **KEYFILE ROTATION: STRUCK** (DECISION S92-1). The "OVERDUE since Aug 9" date has no
  recoverable origin, the two March policy documents disagree on cadence, and S90 measured
  PHISH-HW clean. Governed now by the published handbook policy alone - six months, or on
  exposure - which is a dormant condition, not a countdown. See R-S92-1.
- **EVERY OTHER DEADLINE IN THIS SECTION: PAUSED** (DECISION S92-2) until the work in
  progress completes. PROBE-DRIFT's clock is stopped for a second reason: no live document
  states what it tests, and nothing can be overdue when nobody can say what it is for.
- Nothing here may claim a session's OPENING again. R-S92-1 applies to every row.
**WRITTEN OUT IN FULL. "Unchanged from generation N" is BANNED here (DECISION S88-4).**

- **KEYFILE ROTATION: ONE OF THREE DONE, NOW DEFERRED TWICE. OVERDUE since Aug 9 (~23 days).**
  `GROQ_GNI_NOT_MAD` rotated at S90 and **CERTIFIED TWICE**: on a dispatch (`33416590413`,
  S90) and now on a SCHEDULED run — `33420536876` (2026-08-31 17:37Z) shows
  `GROQ_API_KEY: ***` and concluded `success`. The old key may be revoked in the `not_mad`
  Groq dashboard. **REMAINING: `GROQ_API_KEY`** (feeds `gni_mad` morning AND `gni_adaptive`
  AND `gni_heartbeat` — blast radius THREE workflows) **and `GROQ_MAD_EVENING`** (evening MAD
  only). **These are the FIRST MOVE at the S92 open** (DECISION S91-3).
- **PHISH-HW: PARTLY PAID (S90), OVERDUE since ~Jul 31 (~32 days).** DONE: security logs read
  on both accounts; OAuth/GitHub-App inventories read; PAT tabs read — "No personal access
  token created" on both, which is itself a finding, because `MYANMAR_DISPATCH_PAT` exists as
  a secret. Foreign-country session events EXPLAINED (VPN).
  **REMAINING, James solo, browser:** revoke `Cerebras Inference` (Never used, both accounts)
  and `GitHub Desktop` (7 months unused); check the fine-grained token tab and the third
  account for `MYANMAR_DISPATCH_PAT`; report the trypatchhog.com mail to Gmail and GitHub.
  **DO NOT revoke** GitHub CLI, Git Credential Manager, Supabase or Groq Console — all in use.
- **PROBE-DRIFT: OVERDUE since Aug 24 (~8 days), AND ITS INSTRUMENT IS UNARMED.**
  `mad_model_probe.py` is tracked and intact (`13aed42`, repo ROOT not `tools/`), but
  `../groq_probe_key.txt` is **0 BYTES, dated Jul 7**, so the probe has been unrunnable since
  July and the overdue clock measures the wrong thing. **Second, separate gap: what
  PROBE-DRIFT actually TESTS is not written in any live document.** `llm_health_probe` tests
  AVAILABILITY only. Recover the definition from S57-era records; do not infer it.
  S91 note: `mad_model_probe.py` classified `net=1 stub=0` and was deliberately NOT run.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.
- **PROVIDER + PLATFORM EOL WATCH — record at announcement, not at death.**
  - `actions/checkout@v4` + `actions/setup-python@v5` -> item 6.7. **CLOSED AND CERTIFIED
    ACROSS ALL EIGHT WORKFLOWS AT S91.**
  - **Node 20 is ITSELF now deprecated on GitHub runners** — the post-fix logs state that
    workflows run on **Node 24 by default**, citing a 2025-09-19 changelog. Recorded at
    announcement. No action required while all eight are on v7.
  - `gemini-2.5-flash` dies Oct 16 (Lens's lens2 runs on it).
  - `llama-3.1-8b-instant` died Aug 16 — last hardcoded default removed at S89 (9.4).
  - Supabase free tier warns by EMAIL at 20% of a limit, then a grace period, then restricts,
    with no second grace period. Storage 113/500 MB. No longer shared with Project Lens.

### RETIRE CANDIDATES — the clause, honestly counted
- **4.4** — promoted with a written reason at generation 7; carried on that reason.
- **5.11** — third generation, and it is NOT a retire candidate this close: S91 converted it
  from an anecdote into a measured rate (5.14), which is the work the clause exists to force.
- **5.12 / 5.13** — second generation. Not candidates yet.
- **8.9** — de-scoped at S89, third generation. **Re-check at generation 12: if no list edit
  has been proposed by then, close it as accepted.**
- **1.9 / 5.10** — DISCHARGED at S90. No item is dropped silently this close.

---

## CHANGED THIS REGENERATION

**S92 (generation 12). Produced by BYTE COPY of generation 11 plus anchored patches, not by
retyping - CONTRACT v9 records the method change and its reason (D2).**
- MISSION replaced: 9.14 (done) -> S93's CI harness job.
- FIRST MOVE AT OPEN: deleted. It had headed two consecutive generations.
- LIFECYCLE: KEYFILE struck; all other clocks paused; PROBE-DRIFT double-struck.
- THE ORDER: 9.14 closed; 9.9 and 9.10 certified; 9.13 evidence upgraded to published.
- ADDED: S94, S95, S96 as ranked work below the S93 mission.
- GRAVEYARD: unchanged at SEVEN rows, carried by byte copy - not retyped, not re-read.
- DECISION S92-1: KEYFILE ROTATION deadline struck. Ruled by James after the origin search
  came back empty and the two March policies were found to disagree. R-S92-1 minted.
- DECISION S92-2: all LIFECYCLE clocks paused until work in progress completes. Ruled by
  James: "work that breeds work is the loop hole."
- DECISION S92-3: one discipline per concern - arc42 for structure, PM for the queue, SRE
  for the operation, ITIL configuration management for the inventory, ISO/IEC 14764 for
  classifying items, DevOps for commit-to-production. Written into ARCHITECTURE section 4.
- DECISION S92-4: the S92 diagnosis is homed in ARCHITECTURE section 11, not in a new
  document and not in this file. CONTRACT v9 adds ARCHITECTURE as the fifth ROUTING home;
  M3's refusal of a fifth home for DECISIONS is untouched.
- DECISION S92-5: close artifacts are produced by byte copy plus anchored patch. The
  GRAVEYARD is the only structure ever copied by bytes and the only one never seen to rot.

**CLOSED:** **8.5** (discharged by measurement, `33578de`) · **6.7** (certified across all
eight workflows, with a discriminating control) · **5.13** (premise disproven by bytes —
S90 fixed the header in the same close that filed the item).

**NEW ITEMS:** **5.14** (three of ten harnesses dead, one cause, measured) · **9.13** (the
published band table is wrong in two of five rows) · **9.14** (`limit(5)` hides the rows that
would certify 9.9 and 9.10).

**RE-SPECIFIED:** **8.10** — un-paired from 8.5, with the cheap route named (a third arm on the
committed harness) · **8.1b** — re-measured on the input at 198/199 · **8.1c** — the branch's
own prompt cost measured in isolation (555 chars) · **5.11** — moved from seven hand-found
instances to a measured rate.

**RE-RANKED:** nothing. ROOT 9 stays TOP, ROOT 8 second. 9.14 becomes the top open item in
ROOT 9 and S92's mission because it unblocks two already-shipped items for one line of change.

**GRAVEYARD:** unchanged at SEVEN rows, copied forward verbatim from generation 10.

**DECISION S91-1** — the S91 mission's own framing was WRONG, and this is recorded rather than
quietly corrected. Generation 10 declared 8.5 "load-bearing for FOUR items: itself, 8.10, and
the certs for 9.9 and 9.10". S91 disproved all three couplings by bytes: 8.5's condition is
`_high_escalation == False`, i.e. level NOT in (HIGH, CRITICAL), i.e. **score < 7**; 9.9's
discriminating condition is **score 9.0–9.4** (where stored interval is `1.0` and the map says
`30 min`) — the two conditions are mutually exclusive, so no single run can satisfy both. And
8.10's PHI-003 gate lives in the escalation scorer, which `dryrun_nn5_gate.py` never touches.
Chosen over silently working the mission as declared: Protocol step 7 requires saying so.
**Cost accepted:** the mission was still worth running — it discharged 8.5 and found 5.14 —
but the "four items" claim inflated its value at declaration time and would have inflated the
close's claim of success.

**DECISION S91-2** — 5.14 NOT fixed this session. Chosen over patching the three callers
immediately. Reason: the same-session fix bar requires a live position failing or provably
about to fail silently, perishable evidence, or James ruling it, and none applies — the dead
harnesses fail LOUDLY and have done so for two months. The fix is also a genuine design
choice: patch three callers (test-only, no production risk, leaves the trap armed for the
next caller) versus guard `n_articles == 0` inside `compute_depth` (fixes the class, touches
production, and needs the three empty-pool paths in `_fetch_relevant_articles` reasoned about
first). That is a SWOT, not a session tail. **Cost accepted:** the harnesses stay dead one
more session, and the record now says so explicitly instead of implying they work.

**DECISION S91-3** — `GROQ_API_KEY` and `GROQ_MAD_EVENING` DEFERRED A SECOND TIME, to the S92
OPENING. Chosen over doing them now. Reason: LR-104 puts credential work at a session opening,
S90 deferred them on exactly that ground, and R-S90-4 says a rule invoked to defer one item
binds every item of its class — breaking it here would break it in the direction the rule was
minted to prevent, on the key with the LARGEST blast radius of the three. **Cost accepted:**
the rotation is now ~23 days overdue and a second deferral is the point at which a deferral
becomes a habit; it is therefore written into S92's mission block as the FIRST MOVE, not left
in the lifecycle section to be noticed.

**NOT DONE, NAMED:** 9.5 (the July census audit — still scoped as a session) · 9.11 (needs a
429 that cannot be safely forced) · 9.12 (render path never read) · 9.13 (numbered today, not
fixed) · 3.2 (schema, LR-104) · PHISH-HW's browser remainder · two of three key rotations ·
5.14's fix · the 42 unmeasured `__main__` selftests outside `tests/`.

---

## HOW THIS FILE IS MAINTAINED
Regenerated at every close, dated, superseding — never appended. The GRAVEYARD is the ONE
section copied forward verbatim, and at this close it was extracted from generation 10 BY
BYTES rather than retyped. Item numbers must be unique; state the expected count in advance
and grep it before delivery — **this close stated 62 and measured 47** (R-S81-5, third
instance; from S92 the expected count is derived from the previous generation's grep plus
the delta, never recalled). The 47 carry no duplicates: the three ids that appear twice
(4.4, 5.11, 8.9) are the deliberate root-plus-RETIRE-CANDIDATES cross-references. Decisions live here as DECISION lines, by CONTRACT's
no-fifth-document ruling — they are findable only by reading past order files, and that cost
was accepted knowingly at v5.
