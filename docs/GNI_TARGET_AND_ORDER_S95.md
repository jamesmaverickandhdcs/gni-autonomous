# GNI TARGET + WORKING ORDER
**GENERATION 15 - 2026-09-03 (S95 close). SUPERSEDES generation 14 (`GNI_TARGET_AND_ORDER_S94.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S96)

**Build the time-series macro map: X = session, Y = White Paper layer, Z = Vision ->
Executable. Measure the gap instead of estimating it.**

WHY THIS IS TOP. It is JAMES'S roadmap (DECISION S93-2) and the last row of it. S93
built the detector, S94 the world model, S95 moved law out of prose and into code.
S96 measures whether any of that closed distance.

**S95 handed it a real axis.** `docs/GNI_RULE_CHECKABILITY_S95.tsv` is machine-readable:
159 rules, 53 CHECKABLE, 106 not, one reason each. Z is no longer an estimate for the
rule layer - it is a ratio that can be recomputed at every close and diffed.

**Definition of done:** a generated artifact - not a hand-drawn one - that plots at
least one measured series per axis, names its source for every point, and states which
points are measured and which are absent. An absent point is shown as absent, never
interpolated. Read R-S95-4 before comparing any figure across generations: compare the
SET, not the integer.

**Scope, stated narrowly because this item invites sprawl:** ONE generated artifact.
Not a dashboard, not a new document type, not a metric framework. If the first honest
version has three points on it, ship three points.

**Discriminating cert (R-S90-1):** change one input figure and the artifact must move;
revert it and the artifact must return byte-identical. An artifact that renders the same
under both has measured nothing.

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

**CLOSED AT S95 - `b70fc08` + the S95 docs commit, certified on CI:**
- **THE S95 MISSION.** All 159 registered rules classified CHECKABLE / NOT with a one-line
  reason each - 53 yes, 106 no - and FIVE shipped as executable checks in
  `tools/gni_rule_checks.py`, running as a second CI job. Markers and
  `docs/GNI_RULE_CHECKABILITY_S95.tsv` come from ONE dict, so prose and table cannot drift.
  Cert across three commits: `b639b54` rule_checks GREEN -> `66c105e` (one manifest row
  removed) rule_checks RED, ONE check failing, harnesses unmoved -> `a5e9c1e` GREEN again.
  `harnesses` failed in all three: that is the CONTROL, not noise.
- **`rule_checks` is the first CI square in GNI that is meant to be green, and is.**
  Job-level reading was required to see it - run-level `conclusion` is `failure` in every
  case because `harnesses` is correctly red (5.14). Never read this workflow at run level.
- **THE FOUR CI EXIT INTEGERS, answered.** S94's UNKNOWN asked whether they still read
  1/1/0/0. They do: `dryrun_false_neutral` 1, `dryrun_mad_redefinition` 1, `dryrun_nn5_gate`
  0, `dryrun_rate_governor` 0, two `ZeroDivisionError`s, signature identical to `33572158050`.
- **5.20 PARTIALLY DISCHARGED.** `tools/gni_rule_checks_fixture.py` is a self-asserting
  selftest over 11 fixture families and runs in CI as the control probe BEFORE the checks.
  `tools/gni_state.py` remains outside; the item stays open for that half only.
- **`R-S92-2` DEMOTED to NOT CHECKABLE, with evidence.** Three check designs died against
  measurement. `src/app/api/health/route.ts:39` carries `.order('run_at', {ascending:
  false}).limit(1000)` - the direct descendant of `limit(332)`. Position-decay lives in HOW
  the constant was derived, not in the call site, and `limit(1000)` and `limit(332)` are
  byte-identical in shape. C3's slot went to `R-S74-1` instead.

**CLOSED AT S94 - `44a3cba`, certified on the live tree:**
- **MISSION DONE.** `tools/gni_state.py` generates ARCHITECTURE section 7 into
  `docs/GNI_ARCHITECTURE_S94.md` and exits 0. Sections 5 and 6 remain empty by design.
  It follows `secret -> workflow -> ENV ALIAS -> code consumer` as one chain, which is the
  part no inventory has had: `gni_pipeline.yml` binds `GROQ_GNI_NOT_MAD` to the env name
  `GROQ_API_KEY`, so a secret-name-only grep reports it as reaching no code at all.
- **DISCRIMINATING CERT PASSED.** Swapping one secret line in `gni_pipeline.yml`
  (`TWELVE_DATA_API_KEY` -> `GROQ_TEST_ONLY`) moved SIX lines of output - both rows, the
  env alias, and the downstream consumers. Reverting restored the file byte-for-byte
  apart from the generation timestamp; `git status --short` empty.
- **THE INSTRUMENT CHECKS ITSELF (R-S93-1).** Seven control probes run BEFORE any repo
  read; breaking one regex deliberately produced `EXIT=2` and NOTHING WRITTEN. Two probes
  encode instrument errors made while building it, so they are regression tests, not
  hypotheticals.
- **SECTION 7 IS THE ONLY THING THAT MOVED.** `awk`-stripping section 7 from both
  `GNI_ARCHITECTURE_S93.md` and `..._S94.md` leaves IDENTICAL files - D1-D7 and 8.4
  untouched - and `grep -c '^## \u00a7'` = 12.
- **CI UNCHANGED BY THE COMMIT.** `33572158050` (`44a3cba`) and `33569548145` (`cf21ff1`)
  carry the same failure signature: two `ZeroDivisionError` tracebacks and the same PASS
  block. Read honestly: the SIGNATURE was compared, not the four exit-code integers.
- **TWO BANKED REGRESSION FIGURES WERE WRONG, and the generator is the correct side.**
  `GROQ_MODEL_FALLBACK` = **4 files**, not 6 (`llm_health_probe.py`, `mad_protocol.py`,
  `nexus_analyzer.py`, `funnel/intelligence_funnel.py`) - generation 13 counted SITES and
  wrote FILES. `TELEGRAM_CHAT_ID` = **1 file**, not 0: `preflight.sh` GUARDS against it,
  which is a negative reference and still a consumer of the string. Reported, not
  reconciled silently, as the mission's own cert clause required.
- **MAD runs READ:** `33524044619` (Sep 1, 220/31/**31**), `33375082629` (Aug 31,
  168/35/**35**), `33318313852` (Aug 30, 148/31/**31**) - all `dropped=0`, `truncated=0`,
  `transcript_errors=0`, `ARB-FIT ctx_depth=0`. With S93's two, **ROOT 1.3's `depth=0` fix
  now holds across FIVE consecutive debates**: no longer two samples, a distribution.
  `33525874914` is a grounding-watch (`ARB-FIT` count 0), not a debate.

**CLOSED AT S93 - `944c4f0`, CI run `33529254247`:**
- **MISSION DONE.** `.github/workflows/gni_ci_harness.yml` - GNI's FIRST push-triggered
  workflow. Runs `ai_engine/tests/dryrun_*.py` on every push, per-file exit codes, job RED
  on any non-zero. No secrets are passed: a hard boundary against quota spend, not a
  grep-based safety claim.
- **CERT, and it DISCRIMINATES inside one run:** `false_neutral`=1, `mad_redefinition`=1
  (both `ZeroDivisionError`, item 5.14), `nn5_gate`=0, `rate_governor`=0 (30/30 checks),
  `JOB RESULT: fail=1`. No deliberate breakage was needed - the control is in the harness
  set. `ModuleNotFoundError`=0, `secrets.`=0.
- **TRAP RETIRED, not carried.** The three "stored but read by no workflow" secrets were
  traced: `GROQ_MODEL_FALLBACK` is read by SIX code SITES in **FOUR FILES**
  [corrected at S94 by `tools/gni_state.py`; generation 13 wrote "six code files"]
  (`llm_health_probe`, `nexus_analyzer`, `mad_protocol`, `intelligence_funnel`)
  and is item **1.12**, open since S85 - the trap was 1.12 under a new name.
  `GROQ_TEST_ONLY` is the fourth probe account, deliberately local-only - and S90's
  wrongness ledger had ALREADY disproven this exact claim. `TELEGRAM_CHAT_ID` is a
  pre-rename remnant that `preflight.sh:75` actively guards against. **Nothing deleted.**
- **MAD runs READ, not counted.** `33484715285` (Sep 1, 200/33/**33**, dropped=0, bearish
  0.52) and `33420957824` (Aug 31, 213/32/**32**, dropped=0, bullish 0.67) - ROOT 1.3's
  `depth=0` fix is holding in production, no ctx-trim on either. `33422581858` is the
  11:13 grounding-watch flavour, not a debate.

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
- **9.15** **NEW (S93) [MEASURED] - PREVENTIVE, not corrective.** `mad_protocol.py:52`
  bottoms out at `os.getenv('GROQ_MODEL_FALLBACK', 'llama-3.3-70b-versatile')` - a model
  retired 2026-08-16. It is the innermost of THREE nested `getenv` calls and `gni_mad.yml`
  feeds both outer names, so it does not fire today; S93's two read debates returned real
  verdicts. Its three siblings default to `gpt-oss-20b`; S89's 9.4 sweep fixed
  `nexus_analyzer` and left this one. **Note for CI:** `gni_ci_harness.yml` passes NO
  secrets, so any harness importing `mad_protocol` resolves `MODEL` to the dead string -
  expected, not a live defect. Do not re-diagnose it from a CI log.
- **9.16** **NEW (S93).** The order and the handoff both state "all 8 workflows on
  `checkout@v7` + `setup-python@v7`". `gni_selfcheck.yml` has NO `setup-python` step - it
  runs `curl` and the runner's `python3` and does not need one. Item 6.7's substance is
  intact; the published sentence claims more than it measured. One line.
- **9.17** **NEW (S94) [MEASURED] - the same shape as 9.16, one generation later.** Both
  `HANDOFF_S93.md` and `GNI_ARCHITECTURE_S93.md` state **"8 scheduled + `gni_ci_harness.yml`
  on push"**. `tools/gni_state.py` reads the trigger blocks and returns **7 scheduled, 1 on
  push, 1 dispatch-only**: `gni_adaptive.yml` has NO `schedule:` key at all - it is fired by
  the heartbeat via `workflow_dispatch`. The count was never measured, only incremented.
  **Now cheap to close AND to keep closed:** the generated section 7 states the three
  numbers, so the fix is to make the prose cite the generator rather than restate it.
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
- **6.9** **OPEN (S93), FIGURES NOW GENERATED (S94).** There is NO dependency manifest - no
  `requirements.txt`, no `pyproject.toml`, no `setup.py`, no `Pipfile`. Section 7.3 of
  `GNI_ARCHITECTURE_S94.md` is now generated and states the real shape: **10 inline install
  steps across 9 workflows, 6 distinct package sets**, with `gni_mad.yml` and
  `gni_pipeline.yml` each carrying TWO different lists in their two jobs. Generation 13's
  "8 inline lists" counted workflows, not steps. **Two sub-findings from the same output,
  filed here rather than as new items:** `gni_ci_harness.yml` installs `groq`, `geopy` and
  `feedparser==6.0.12` on every push although it passes NO secrets and can never reach
  Groq; and `gni_selfcheck.yml` carries no `pip install` at all, which is the same fact
  9.16 records from the `setup-python` side.
- **6.10** **NEW (S94) [MEASURED, n=9] - THE FREE-TIER SCHEDULER GIVES NO TIMING GUARANTEE,
  AND NO DOCUMENT HOLDS THE NUMBER.** The `gni_mad.yml` crons were read BY BYTES and are
  exactly as recorded (`43 2`, `43 10`, `13 11`) - the prose was right, which was the
  prediction that failed. What is wrong is the assumption that a cron time is a start time.
  Nine consecutive `schedule` runs (Aug 29 - Sep 1; zero `workflow_dispatch` among them)
  started **+4h07m to +6h58m after their nominal cron**, and the delay is roughly constant
  within a day and varies between days. R-S87-6's third amendment already forbids recalling
  the band; this item exists because nothing MEASURES it either. It belongs to ARCHITECTURE
  section 6, which is deliberately still empty - so record the number here until section 6
  is generated, and never quote a cron time as an expected start.
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
- **7.4** **NEW (S93) [UNMEASURED, n=2].** `GROUNDING SHADOW` reported 19 consultant + 10
  arb hits on Aug 31 and 2 + 6 on Sep 1 - same code, one day apart, ~9x on the consultant
  side. Either the input varies that much or the counter does. Two samples decide nothing;
  harvest the span before ruling. Feeds this root's re-rank trigger.
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
- **5.15** **NEW (S93) [MEASURED].** `ai_engine/tests/` contains ZERO `__main__` blocks in
  all ten files. For the four `dryrun_*` that is harmless - they execute at top level. For
  `test_groq_guardian.py` (5 classes, 29 `def test_`, 39 asserts), `test_dedup_novelty.py`
  (3/4) and `test_injection_normalize.py` (4/4, `import pytest`) it is fatal: run as a
  script they exit 0 having asserted NOTHING. **36 assertions are invisible.**
  `test_analysis_guardian.py` has no test and no assert at all. S91's "7 green" included
  these. `pytest 9.0.3` is installed locally - run it there BEFORE wiring CI, or the first
  red will be indistinguishable from stale fixtures (the Lens `lens-ci.yml` failure).
- **5.16** **NEW (S93).** The 42 `__main__` selftests OUTSIDE `tests/` - including
  `main.py`, `mad_runner.py`, `adaptive_pipeline.py` - **cannot be answered by CI.**
  Running them runs the pipeline: real Groq calls, real DB writes, real quota. S92's
  handoff assigned this question to S93's mission; that assignment was not achievable and
  is recorded here rather than carried. Needs a different instrument, not a bigger glob.
- **5.17** **NEW (S93).** A detector that is RED on every push becomes background noise and
  stops showing regressions. **Two dispositions, and the first is preferred: fix 5.14, and
  this item closes with it.** Only if 5.14 is deferred again does an expected-fail
  allowlist become necessary - and an allowlist legitimises the red rather than clearing
  it. DECISION S93-1 (James): do not build the allowlist now; bind it to 5.14.
- **5.18** **NEW (S93).** Past sessions' WRONGNESS LEDGERS are never re-read. Each lives in
  its own `HANDOFF_S{N}.md` with no collected home, so a disproven claim can return.
  Proven: `GROQ_TEST_ONLY reaches no workflow` was disproven in S90's ledger
  (`HANDOFF_S90.md:63`) and re-filed by S92 as a fresh trap. GNI_RULES holds LESSONS; the
  GRAVEYARD holds falsified DESIGNS; nothing holds falsified CLAIMS. Candidate fix: extend
  the GRAVEYARD, which is the one structure never observed to rot (D2).
- **5.19** **NEW (S93).** R-S91-4's cited EVIDENCE is disproven while its conclusion holds -
  see the amendment in `GNI_RULES_S93.md`. Filed so the specimen is not cited again.
- **5.20** **NEW (S94) - THE DETECTOR HAS NO DETECTOR.** `gni_ci_harness.yml` globs
  `ai_engine/tests/dryrun_*.py`. `tools/gni_state.py` is outside that glob, so its seven
  control probes - the thing that makes its output trustworthy - execute only when a human
  runs the script by hand. The generator can rot exactly the way the hand-written inventory
  it replaced rotted, and nothing would say so. **Cheap fix, S95-shaped:** a `--selftest`
  flag that runs the probes and exits non-zero, plus a widened glob. Do not widen the glob
  alone: `gni_state.py` shells out to `gh` and `git grep`, and CI has neither `gh` auth nor
  a reason to pay for one.
- **5.21** **NEW (S94) - NO `.gitattributes`, AND NOW IT MATTERS.** The repo has no
  `.gitattributes`, so Windows checkout converts LF to CRLF (`git push` warned on both new
  files at S94). `tools/gni_state.py` writes with `newline="\n"`. A fresh clone followed by a
  re-run can therefore present the WHOLE generated document as changed when nothing about
  the system changed - a false diff in the one file whose purpose is to make real change
  visible. **One line** (`*.md text eol=lf` plus `*.py text eol=lf`) closes it. Filed, not
  fixed: S94's mission was done and the scope was held.
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

- **5.22** **NEW (S95) [MEASURED] — `tools/*.py` ARE FRAGILE TO THE OPERATOR'S CONSOLE AND
  TO STRAY BYTES.** Two defects, one subject. (a) `gni_state.py --stdout` dies with
  `UnicodeEncodeError` on `\u2192` because Windows `print` encodes cp1252; the file-writing
  path is unaffected, so only `--stdout` is broken, and Linux CI would never show it.
  (b) `code_consumers()` splits `git grep` output with `splitlines()`, which also breaks on a
  lone `\r`, yielding a colon-less fragment and `IndexError`. Both are `R-S87-5` / `R-S94-3`
  kin: the environment translates without being asked. Fix shape: `sys.stdout.reconfigure(
  encoding="utf-8")` and `split("\n")` with a colon-count guard that exits 2.
- **5.23** **NEW (S95) — C5'S BLIND SPOT IS WHERE THE ERRORS LIVE.** `tools/gni_rule_checks.py`
  lints itself for hand-written integers, but patch scripts live in `/tmp` and are never
  committed, so nothing lints them. FIVE of this session's SEVEN instrument errors happened
  there. The rule that would have caught them (`R-S81-5`) is shipped as a check that cannot
  see them.
- **5.24** **NEW (S95) [MEASURED] — 22 FILES IN `docs/` CARRY NO SESSION NUMBER.** Of 117
  markdown files, 84 are session-numbered generations of the six live families (78 superseded,
  6 live), 11 belong to one-off numbered families, and **22 have no number at all** -
  including `SUBPAGE_CERTIFICATION.md` and `SUBPAGE_IC_CENSUS.md`. A numbered file can at
  least say "something higher exists, so I am dead". An unnumbered file can never be
  superseded and can never declare itself live. This is D4's mechanism in its general form:
  D4 said no live document points at the deliverable; the bytes say there is no MECHANISM by
  which one could.
- **5.25** **NEW (S95) [MEASURED from §7.2] — TWO SECRETS WHOSE WIRING CONTRADICTS THEIR
  CONSUMERS.** `ALPHA_VANTAGE_API_KEY` is stored and bound to an env alias in
  `gni_pipeline.yml` with **zero** code consumers, while `ai_engine/collectors/alpha_vantage.py`
  reads `TWELVE_DATA_API_KEY`. `GROQ_MAD_EVENING` is referenced by `gni_mad.yml` with **no env
  alias and zero** consumers. Neither is a deletion instruction (S93 ruling); both are
  unexplained, unlike the four `none` rows §7.2 explains. Not chased at S95: out of mission scope.
- **6.11** **NEW (S95) [MEASURED] — ONE UNORDERED `limit(N>1)` IN `ai_engine/`.**
  `ai_engine/mad_runner.py:104` calls `.limit(50)` with no `.order()` in the same chain, so
  which 50 rows Postgres returns is not defined by the query. Found by an AST probe over
  `ai_engine/` (26 `limit(1)` singletons, 7 ordered `limit(N>1)`, this one). Not a run-time
  failure and not measured against `frequency_log` / `reports`; an UNKNOWN, not a defect.
- **9.18** **NEW (S95) — THE TYPESCRIPT HALF OF THE POSITION-SELECT SURFACE IS UNMEASURABLE.**
  35 `.limit()` sites live in `src/app/api/*.ts`, including the `limit(1000)` descendant of
  `limit(332)`. No TypeScript parser is available to a stdlib-only tool, so every AST-based
  measurement this session made covers `ai_engine/` only. Any claim about GNI's
  position-select surface that does not say "Python only" is overstated.

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

**S95 (generation 15). Produced by BYTE COPY of generation 14 plus anchored patches
(DECISION S92-5), with the GRAVEYARD carried inside that copy rather than re-inserted.
The whole of this section is replaced, never appended to.**
- MISSION replaced: S95's rule-to-check pass (done) -> S96's macro map, the last row of
  DECISION S93-2's roadmap.
- THE ORDER: a CLOSED AT S95 block added at the top; the S94, S93 and S92 blocks below keep
  their own session labels.
- **`R-S92-2` demoted from CHECKABLE to NOT CHECKABLE.** The reason is written beside the
  rule and in the CLOSED block. It was `yes` for most of the session and three designs died
  proving otherwise; recording the correction is the point (R-S84-3).
- GRAVEYARD: unchanged at SEVEN rows, carried by byte copy - not retyped, not re-read.
- **RULINGS THIS SESSION: NONE.** James set no new direction; S95 executed DECISION S93-2's
  assignment. There is no DECISION S95-n line and the absence is stated, not inferred.
- Judgements made without a ruling, recorded as mine: (a) the manifest ratchet is NOT added
  to CONTRACT, because C1 enforces it mechanically and adding prose law beside a working
  check is exactly the direction ARCHITECTURE 8.3 argues against; (b) the CRLF repair was
  committed rather than history-rewritten.
- ARCHITECTURE: section 7 REGENERATED at S95 from `tools/gni_state.py`; the ROADMAP table's
  S95 row carries its commit. Sections 5 and 6 remain EMPTY and that is the correct state.
- RULES -> five earned, `R-S95-1` .. `R-S95-5`, each carrying a CHECKABLE marker. The
  register now holds 159 ids and PART 0 gains an UNREGISTERED ID MANIFEST of eight rows,
  which `tools/gni_rule_checks.py` reads as C1's escape source.
- CONTRACT: UNCHANGED at v9, byte-identical, md5 `d7e68e815a17eaffbaedc5d6b4494bde`
  (DECISION S89-6). Protocol: UNCHANGED at v11. Nothing about the rules of engagement
  changed; the law-vs-state test says that is the healthy outcome.

**CLOSED:** the S95 MISSION (classification + five executable checks, cert across three
commits) · 5.20's fixture half · one S94 UNKNOWN (the four CI exit integers, measured
1/1/0/0) · `R-S92-2`'s checkability question, answered NO with evidence.

**NEW ITEMS: SIX. rho = 6/1 = 6.00 this generation, and it is not being hidden.**
**5.22** (tools fragile to console encoding and stray CR) · **5.23** (C5 cannot see the
`/tmp` scripts where 5 of 7 instrument errors lived) · **5.24** (22 unnumbered docs cannot
be superseded) · **5.25** (two secrets whose wiring contradicts their consumers) · **6.11**
(one unordered `limit(50)`) · **9.18** (the TypeScript half is unmeasurable).
**Findings routed OUT of this file this session: NONE.**

**ITEMS CONSIDERED AND DELIBERATELY NOT MINTED:** the `\r\r\n` corruption (repaired within
the session, and its lesson is `R-S95-5`, not a queue row) and `gni_state.py`'s control probe
printing `7/7 pass` after a traceback (the same subject as 5.22 - the probe checks the
instrument's LOGIC, not its robustness, and that sentence belongs beside 5.22, not in a new
number).

## HOW THIS FILE IS MAINTAINED
Regenerated at every close, dated, superseding — never appended. The GRAVEYARD is the ONE
section copied forward verbatim, and at this close it travelled inside a byte copy of
generation 13 rather than being extracted and re-inserted.

**ITEM COUNT, and a WARNING about comparing it across generations.** Expected count stated
IN ADVANCE at this close: **67** = the 63 unique ids that
`grep -oE '\*\*[0-9]+\.[0-9]+\*\*' | sort -u | wc -l` returns on generation 13, plus the
four minted here (9.17, 6.10, 5.20, 5.21). Measured after delivery: see the close's own
grep. **Generation 13 reported 47 by a DIFFERENT method, and 47 and 63 are not two readings
of one quantity - they are two quantities.** R-S81-5's third instance was exactly this shape,
so the method is now written next to the number. Whoever regenerates generation 15 must run
the grep above on THIS file to get their baseline, and must not carry 63 or 67 from memory.

Decisions live here as DECISION lines, by CONTRACT's no-fifth-document ruling — they are
findable only by reading past order files, and that cost was accepted knowingly at v5.
