# GNI TARGET + WORKING ORDER
**GENERATION 10 — 2026-08-31 (S90 close). SUPERSEDES generation 9 (`GNI_TARGET_AND_ORDER_S89.md`).**
Regenerated, never appended. The LIVE order is the HIGHEST session number.

---

## NEXT SESSION'S MISSION (S91)

**Exercise `_high_escalation == False` once, deliberately — item 8.5.**

Declared because it is the only measurement in the file that discharges FOUR items at once:
**8.5** (the branch has never run), **8.10** (PHI-003 has never fired in 197 runs), and the
**certs for 9.9 and 9.10**, which S90 shipped but could not certify — at `CRITICAL`/`0.5` the
new code and the old code render identically, so the browser proves nothing (R-S90-1).

**Protocol step 8b binds here: 8.5 touches a DETERMINISTIC component, so SIMULATE over stored
history FIRST** — `tools/replay_scorer.py` exists and `tools/design_bench.py` prints the
funnel-preselection finding on every run; do not re-derive it. Decide the mechanism (fixture,
replay, temporary threshold, synthetic row) only after the simulation says what a sub-9 run
would even look like. Read the GRAVEYARD before proposing: recalibrating the LEVEL is dead,
and so is editing a word list.

**Free certs to collect first, in the opening block, before any design work:**
1. **6.7** — the `02:13Z`/`02:43Z` runs after `e54afdf`: Node-20 warning must be **0** (v4
   control = 2). That closes 6.7 across all eight workflows.
2. **Rotation** — `not_mad`'s new key on a SCHEDULED run (S90 certified it only on a dispatch).
   `gh run view <id> --log | grep -m1 'GROQ_API_KEY:'` must show `***`.
3. **9.9 / 9.10** — one SQL: if `frequency_log` has gained a row that is not `CRITICAL`/`0.5`,
   the cert is free and 8.5's rank drops accordingly.

---

## TARGET (unchanged — no phase transition this close)

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**DEFINITION OF DONE — status at this regeneration:**
- the arbitrator reads what it claims to read — ROOT 1 CERTIFIED for CONTENT; 1.14 closed at S89.
- the grounding gate measures reading, not existence — **ROOT 7 DE-RANKED THIS CLOSE with a
  written reason (see the root). Nine sessions untouched; the honest cause is not neglect.**
- the escalation score carries information — **ROOT 8: 8.6 CERTIFIED at S90 by SQL and browser.
  The quarter that held it in the top slot is paid. What remains is 8.5/8.10 — the branches
  that have never executed.**
- the public surface matches the configuration — **ROOT 9: the largest single move of the
  project. S90 shipped six commits here and CERTIFIED four of them in a browser.** What
  remains is 9.5 (the July census flags) and 9.11 (the unmeasured Groq ceiling).

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
diagnosis from `design_bench`'s own banner ("an ABSOLUTE threshold on a PRE-SELECTED set")
and was about to file it as a NEW item 8.11, twenty turns after reading this very table at
session open. The June-01 record had reached the same conclusion five months earlier. The
diagnosis does not need a sixth row; the reader needs to re-open this page whenever something
feels new. See R-S89-1.

**S90 NOTE — the diagnosis acquired a CONSEQUENCE, not a sixth row.** Because escalation is
constant at 10.0/CRITICAL, S90 shipped two fixes (9.9, 9.10) whose correct and incorrect
outputs are IDENTICAL on live data. The constant does not merely mislead measurement now; it
makes verification impossible. That is why 8.5 is the S91 mission: the missing counterexample
is the bottleneck for four items, not one. See R-S90-1.

---

## THE ORDER

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION · URGENT · **TOP**
*S90 shipped six commits here and certified four in a browser. It holds the top slot because
its two open items are the last unaudited public claims; it yields to ROOT 8 the moment 8.5
is designed, since 8.5 unblocks two ROOT 9 certs.*

- **9.1 / 9.2** CLOSED in earlier sessions.
- **9.3** **CLOSED (S90), CERTIFIED IN BROWSER.** Three commits. `2a6243c` swept the residue
  `223da0f` left behind — `methodology:31` still carried `~6,175/run (reservation estimate)`
  because the S89 commit edited that file twice for the workflow count and never touched the
  token line, while its own message claimed the replacement. Then `5b2689c` and `da61b13`
  corrected the FIGURE itself: `~17,780/run (measured avg, 61 runs, Aug 2026)` for
  `gni_pipeline` and `~68,509/run (measured avg, 61 runs, Aug 2026; range 7.4K-97K)` for
  `gni_mad`, replacing a static `~80,000` that stood beside a live value on `/about/devops`.
  Table count `37 → 33` (`public` BASE TABLE, counted this session). All three verified on
  `gni-autonomous.vercel.app/methodology`.
- **9.4** SHIPPED (S89). `nexus_analyzer.py:29` no longer defaults to the dead
  `llama-3.1-8b-instant`. `stock-context/route.ts:81` still defaults to
  `llama-3.3-70b-versatile` and was NOT touched — that model is alive; verify before assuming
  it is the same defect.
- **9.5** OPEN — **now the highest-ranked open item in the root.** Eight unresolved S69 census
  flags; F14 (`/comparison` renders BEARISH over a NEUTRAL verdict) is the ugly one. RE-CERT
  never ran. Unaudited since July. This is an AUDIT, not a fix — scope it before starting.
- **9.6** **CLOSED (S90) except for two unrecovered IDs.** `8edcf12`. The finding was not
  "three ID schemes" but CITATION DRIFT: `GNI-R-076` was minted 2026-03-22 as a DATABASE rule
  ("ALTER TABLE for new column additions before any writes"), while the read-the-full-file text
  CONTRACT attributed to it is `GNI-R-037`'s own. The BIRD-EYE attribution is CONTESTED between
  `GNI-R-037` and `GNI-R-180` in the record, so CONTRACT v8 asserts NO id for it. Eight
  cited-but-unregistered IDs are now in `GNI_RULES_S90.md` PART 0; `R-S54-1..4` were recovered
  verbatim. **RESIDUE: `LR-101` and `GNI-R-122` are still cited by live documents and their
  original text has not been found. Do not restate them as law from inferred meaning.**
- **9.7** **CLOSED (S90), CERTIFIED IN BROWSER.** The `levels` table on `/autonomy` reads
  `9–10 / 7–9 / 5–7 / 3–5 / 0–3` and the ring highlight sits on the matching row.
- **9.8** **CLOSED (S90).** `e3a4e95` — the `gni_pipeline.yml:5` comment claimed "8h spacing
  preserved" on a `02:13`/`10:13` pair that is 8h then 16h. Fossil grep for the string across
  `.github/` and `src/` returns 0.
- **9.9** **SHIPPED (S90) `99a9dac` + `59d57ac`, CERT BLOCKED ON 8.5.** `/autonomy` and
  `/health` both now render the MEASURED `recommended_interval_hours` through a
  `formatInterval` helper, with `intervalMap` demoted to a fallback and `!= null` rather than
  `||` so a stored `0` cannot fall through. **The `/health` half was a SIBLING SWEEP the
  `/autonomy` fix missed — R-S55-1, found only because the sweep was run afterwards.**
  Consumer census is closed: `api/stocks/route.ts:15` also holds an `intervalMap`, but it is
  Yahoo chart intervals and unrelated.
- **9.10** **SHIPPED (S90) `59e4023`, CERT BLOCKED ON 8.5.** `/autonomy` reads
  `escalation_level` from `frequency_log`; `scoreToLevel` is DELETED — the last 9/7/5/3 ladder
  in the frontend is gone. **DECISION S89-2's blocker was FALSE:** it said the fix required
  adding the column to `/api/health/route.ts:40`, but `:40` is the `reports` select and
  `/autonomy`'s level comes from `frequency_log`, which is selected with `*`. The API was never
  touched. `frequency_controller.py:104` is the writer (not `main.py:316`, which does not exist).
- **9.11** OPEN — `research/page.tsx:105` publishes `Groq 100K tokens/day`; the May record says
  85,000. **Cannot be measured while headroom exists** — it needs a 429 body, and forcing one
  endangers a sacred run. Read it opportunistically if a 429 ever occurs naturally.
- **9.12** **NEW [PROPOSED, not measured].** `/about/devops` renders `83,933 Tokens Today (All
  Accounts)` against an `85K safe ceiling` progress bar, beside `100,000 Limit Per Account` and
  `Worst Account Today 67%`. The bar compares a THREE-ACCOUNT SUM to a PER-ACCOUNT ceiling, so
  the page reads 98.7% full when the worst account is at 67%. Seen in a browser only; the
  render path has NOT been read. Same family as 9.3 — a published number whose units are wrong.

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT
*8.6's cert is paid, so the root leaves the top slot exactly as generation 9 specified. It
returns to the top the moment 8.5 is designed — 8.5 is the S91 mission.*

- **8.1** CLOSED (S86) — the audit. Saturation across three layers, confirmed by bytes.
- **8.1a** OPEN — D-11's feeds list misses three consumers: arb prompt L989,
  `nexus_analyzer:567`, `self_bias_gate:46`. Unchanged this close.
- **8.1b** OPEN — NN-5 is a deliberate hard-correction channel (`1da3dfe`) whose switch is
  stuck. Since no recalibration is coming, the switch stays stuck by design decision, not by
  neglect. `gni_adaptive` logs 0 Groq because its CRITICAL path is Cerebras (`about/devops:40`).
- **8.1c** OPEN and GROWING — `constraint=1092` of `ctx_room=4762` on `33180919784` (was
  987/5091 at S86): ~19% → ~23% of arbitrator context spent by an always-on branch.
- **8.2** CLOSED (S87) — CERTIFIED 4/4. `4b220ab` merges five unpublished scorer fields.
- **8.3** RULED (S87) — NO RECALIBRATION OF THE LEVEL. See GRAVEYARD row 1.
- **8.4** **CLOSED (S90), CERTIFIED IN BROWSER.** `737ef06`'s `ESCALATION EVIDENCE — SCORE
  BREAKDOWN (GNI-R-117)` panel renders three live cells on `/autonomy`.
- **8.5** OPEN — **S91 MISSION.** Exercise `_high_escalation == False` once, deliberately.
  S87 removed the only natural trigger; the selftest fixture hardcodes CRITICAL. **Now
  load-bearing for FOUR items:** itself, 8.10, and the certs for 9.9 and 9.10. Simulate over
  stored history before designing (Protocol 8b).
- **8.6** **CLOSED (S90) — CERTIFIED, SQL AND BROWSER.** Post-`ee813c0` scheduled run
  `33373867572` (created `08:38:35Z`) wrote row `08:40:47Z` with
  `escalation_score_raw = 26.4`, matching `full_analysis->score_breakdown->raw_score` exactly.
  Six pre-registered predictions, six passes. The two rows beneath it still show `raw = null`
  with a populated blob, so the commit — not luck — is the cause, proven inside one query.
  Browser: `Final Score 10.0 · Raw Magnitude (uncapped) 26.4 · Upper Bound --`.
  **26.4 against a cap of 10 is 2.64x saturation, now standing on a live published row.**
- **8.7** RE-SPECIFIED (S88). Score half CLOSED; the direction-neutral audit of published
  EVIDENCE STRINGS (`factors`, `signals_found`) is what remains. Unchanged.
- **8.8** OPEN — 19 keywords never fire in 192 runs: GEO 1 (`invasion`), TECH 3, **FIN 15**.
  **DO NOT DELETE THEM** — their silence is the finding. Absence is evidence (Protocol step 8h).
- **8.9** DE-SCOPED (S89) — measure TECH/FIN headroom only when a list edit is actually
  proposed. With list edits in the GRAVEYARD, the measurement has no consumer.
- **8.10** OPEN — PHI-003 has never fired in 196 runs. **Pairs with 8.5 and is discharged by
  the same measurement.** Also: `final_score = max(final_score, 1.0)` is an undocumented floor
  that min-raw 5.6 can never reach.

### ROOT 1 — THE ARBITRATOR'S INTAKE · CERTIFIED FOR CONTENT AND FOR ORDERING
- **1.1 / 1.2 / 1.3 / 1.4 / 1.5 / 1.7 / 1.8 / 1.10 / 1.14** CLOSED in earlier sessions.
- **1.6** OPEN, confirmed 14/14 + 4/4 + 2/2, RE-CONFIRMED LIVE 2026-08-30:
  `ARB-ARRIVAL: ctx_chars=3790/3790 R1=DROPPED` while `/debate` publishes R1. Open since S83.
  **A ROOT 9 defect wearing a ROOT 1 number — cross-listed here rather than re-homed, because
  moving it would break the id that three sessions of evidence cite.**
- **1.9** **CLOSED AS ACCEPTED (S90) — the retire clause discharged, four generations late.**
  Its text, recovered from `ee92a5a:93`: *"SATISFIED IN THE INSTRUMENT (S84) — per-pillar
  arrival now printed. Remains open only as an assertion (nothing RAISES on a zeroed pillar)."*
  **Closed rather than promoted because the evidence says the assertion would be wrong:** S85's
  n=4 harvest measured `TECH=0/N` on all four runs, so a zeroed pillar is the NORMAL state, and
  a raise would fire constantly against a fail-open law (2.1). The instrument half — per-pillar
  arrival printed every run — already gives the visibility an assertion was meant to give.
  See DECISION S90-1.
- **1.11** OPEN, TRIGGER FIRED (S86), boundary pinned 39–41 (S87). Round-robin pillar fill.
  **The top OPEN item in ROOT 1.**
- **1.12** OPEN, load-bearing: `GROQ_MODEL_FALLBACK` reaches NO workflow, which is why 9.4's
  default mattered. **Do not wire it before reading its value.**
- **1.13** OPEN — TECH starved in two layers independently (funnel 4 of 22; ladder dies first).
- **1.14b** OPEN — make `mad_runner` print the report id it fetched and the id it updated. One
  print; converts the strongest remaining inference into a byte.
- **1.15** **NEW — NUMBERED AT LAST, four sessions after it was found.** F-86-1: `228634c`
  replaced a hardcoded `str(min(_depth,100))` echo in the `ARB-FIT ctx_depth` line with a
  hardcoded `str(0)` — the same defect class it was fixing, currently latent because the real
  value is 0. It has survived S86–S89 as an unnumbered lead, which is item 5.8 proving itself
  again. Fix when the arbitrator file is next opened.

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM
- **6.1** CLOSED (S84). **6.6** CLOSED (S89) — Lens runs on its own Supabase project.
- **6.2** DE-RANKED (S89). Runway ~550 days at 0.7 MB/day; the obvious deletion target is in
  the GRAVEYARD. What remains is a long-fuse question about what SHOULD age out.
- **6.3** SIZE METER — RE-SPECIFIED (S89). Meter 113 MB vs 87 MB of tables: 26 MB (23%) is not
  in any table. Read the real figure, do not compute it.
- **6.4** L5 exposure when Supabase 402s. Reduced by 6.6 but not removed: GNI can still 402
  itself, and there is no backup.
- **6.5** **THERE IS NO BACKUP.** Unchanged, still true, still the highest-ranked genuinely
  open item in this root.
- **6.7** **SHIPPED ACROSS ALL EIGHT (S90) `e54afdf`, CERT PENDING ONE SCHEDULED RUN.**
  `gni_mad.yml` and `gni_pipeline.yml` pinned to `checkout@v7` + `setup-python@v7`.
  **The order's "4 call sites each" was a banked figure and it was wrong in shape:** it is 2
  per ACTION per file, so a `count==1` or `count==4` assert aborts. The patch asserted 2 and 2
  and the post-sweep grep for any non-v7 pin across `.github/` returns **0**.
  Cert: Node-20 warning must be 0 on the next scheduled run of each (v4 control = 2).
- **6.8** **NEW.** The heartbeat's protection/blackout standdown suspends ~4h15m of checks per
  day, and `GNI-R-122`'s stated reason is token collision — but `GNI-R-114` makes heartbeat a
  ZERO-Groq workflow, so the justification does not apply to what is being suspended. Only the
  adaptive TRIGGER needs withholding; the zero-cost divergence, consensus and delta checks do
  not. **S89 found this and left it unnumbered; numbering it is the fix for that.** Note the
  retraction that travels with it: the claimed 43-minute unguarded gap before `02:13` does NOT
  exist — `BLACKOUT_WINDOWS` butts against `PROTECTION_WINDOWS` with no gap.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · **IMPORTANT**
**DE-RANKED FROM URGENT AT THIS CLOSE (DECISION S90-2), with the reason generation 9 demanded.**
Nine sessions untouched, and the cause is not freshness stealing its turn: its only remaining
urgent work is **7.2, "decide the fix shape"**, and the only shape ever proposed —
per-speaker baskets — is in the GRAVEYARD. No replacement can be designed because the
measurement that would inform one does not exist: `checked_spans` is computed and discarded
(7.1). So the root is BLOCKED ON AN INSTRUMENT, and an instrument gap ranks as IMPORTANT.
**RE-RANK TRIGGER, written so it is checkable: once 7.1's one print lands and `checked_spans`
shows the gate passing spans that were never read at a measurable rate, ROOT 7 returns to
URGENT with that rate as its evidence.** Calling it urgent for a tenth session while nobody
can act on it is the "decorative rank" generation 9 warned about.
- **7.1** PARTLY PAID (S86) — `checked_spans` computed and discarded at the print. R-S87-7
  instance. **This one print is now the root's critical path.**
- **7.2** BLOCKED — decide the fix shape. Per-speaker baskets are in the GRAVEYARD.
- **7.3** PARTLY DISCHARGED (S86). Unchanged.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** HALF-RULED (S86) — clause 2 (LABELED coverage) unmeasured; the only thing keeping it open.
- **2.2** Build B only if 2.1's second clause triggers it.
- **2.3** NARROWED (S87) — external explanations eliminated; remaining candidates are internal.
- **2.4** `/stocks` may render frozen prices. Render path read, fetch path NOT. One read finishes it.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** WIDENED (S86) — `conf = 0.5` exactly on Jun 11 and Jul 7; wider than Jul 19–22.
- **3.2** `data_era` column + tagging. **Originally due ~Aug 2; now ~30 days overdue.** Recorded
  so the age is visible, not re-ranked. **LR-104 binds: schema work needs a session opening, not
  a session tail** — S90 deferred it on exactly that ground and then broke the same rule ten
  minutes later on a credential (see R-S90-4).

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.1** C2 solver recalibration. `ctx-trim` fired again at S87, so not dormant.
- **4.2** CLOSED AS ACCEPTED (S86). **4.5** CLOSED (S89) — the 14-day bill, measured.
- **4.3** Groq TPD refills continuously.
- **4.4** Measure chars/token PER POSITION. `//3` is SAFE; do not move to `//4`.
- **4.6** **NEW, from 9.3's measurement.** The monthly `groq_daily_usage` series shows
  `gni_mad` climbing 28,694 (Jun) → 83,479 (Jul) → 68,509 (Aug) and `gni_pipeline` 6,502 →
  15,980 → 17,780, with everything before June being the flat `6175`/`7433` reservation era.
  **Cost is not stable across regimes and no item currently watches the trend.** 4.5 measured a
  14-day window and closed; this is the longer series it implies.

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** `DEBT_REGISTER_S69.md` — one reader in five months is still not a register.
- **5.6** **PARTLY PAID (S90).** `GNI_RULES_S90.md` was RESTRUCTURED, not merely appended:
  PART 1 indexes every ACTIVE rule by TRIGGER (what you are about to do), PART 2 names EIGHT
  CLUSTERS where several numbered rules are one lesson, PART 3 is the S89 register verbatim.
  All 134 ids carried, none lost, verified by grep. **The measurement that motivated it: 134
  rules registered, 18 cited by the live document set.** CLUSTER A — the patch anchor — holds
  ten rules across eight sessions and still fired twice at S90; that ratio is the open half of
  5.6, and no restructure closes it. Pairs with 9.6.
- **5.7** BYTE-CONFIRMED (S88). Seven `reports` columns never written; two RENDERED on
  `/autonomy`. 8.6 fixed one of the two cells; `_lower`/`_upper` still render `--`.
- **5.8** OPEN — UNNUMBERED items are invisible to the uniqueness assert and vanish.
  **S90 evidence, and it is the strongest yet: FOUR unnumbered leads from S85–S89 were found
  only because James asked for a re-read** — F-86-1 (now 1.15), the heartbeat standdown (now
  6.8), and the two registers nobody reads (now 5.12). Four survivals in five sessions.
- **5.9** SHIPPED (S89) `bb6bd2f` — `docs/STATUS.md` deleted.
- **5.10** **CLOSED (S90).** The generation-1/2 retire roster HAS a disposition and nothing was
  dropped silently: `d3a2f20` (generation 3) line 184 reads *"RETIRE CANDIDATES — GENERATION 3
  OF 3, RESOLVED AS THE CLAUSE REQUIRES"* and line 275 *"all eight generation-3 candidates
  resolved above — four closed as accepted, four promoted"*; `the parked 16` CLOSED AS ACCEPTED
  as a set, `CI-DEGRADE` PROMOTED to 5.1. The clause worked; only its record was unread.
- **5.11** OPEN, PROPOSED — reopen 5.2 (dead-symbol / unwired-module CI detector). **The count
  is now SEVEN hand-found instances of the class**, S90 adding the unreachable `||` on `/health`
  and the `str(0)` echo (1.15). Still unmeasured.
- **5.12** **NEW — NUMBERED AT LAST, five sessions after S85 found them.**
  `SUBPAGE_IC_CENSUS.md` and `SUBPAGE_CERTIFICATION.md` are two more registers nothing reads.
  S85 recorded three such files; only `DEBT_REGISTER_S69.md` was numbered (5.5), and these two
  vanished for five sessions — 5.8's disease, third and fourth instances.
- **5.13** **NEW.** The `GNI_RULES` header line 2 still reads
  `Team Geeks | James Maverick + Claude Sonnet 4.6`. CONTRACT v5 evicted the model roster from
  law as STATE; this is the same roster surviving in a law-adjacent file, and it is wrong
  (S90 ran on Opus 5). One line. Fix when the register is next regenerated.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
**WRITTEN OUT IN FULL. "Unchanged from generation N" is BANNED here (DECISION S88-4).**
- **PHISH-HW: PARTLY PAID (S90), OVERDUE since ~Jul 31 (~31 days).** DONE: security logs read
  on both `jamesmaverickandhdcs` and `fintelplan`; OAuth/GitHub-App inventories read (6 apps
  and 4 apps respectively); PAT tabs read — **"No personal access token created" on both**,
  which is itself a finding, because `MYANMAR_DISPATCH_PAT` exists as a secret and its token is
  therefore in the fine-grained tab, on the third account, or expired. Foreign-country session
  events (Netherlands Jul 6, Tokyo Jul 7 / Jun 12 / Jun 18) EXPLAINED: James uses a VPN.
  **REMAINING, James solo, browser:** revoke `Cerebras Inference` (Never used, both accounts)
  and `GitHub Desktop` (7 months unused); check the fine-grained token tab and the third
  account for `MYANMAR_DISPATCH_PAT`; report the trypatchhog.com mail to Gmail and GitHub.
  **DO NOT revoke** GitHub CLI, Git Credential Manager, Supabase or Groq Console — all in use.
- **KEYFILE ROTATION: ONE OF THREE DONE (S90), still OVERDUE since Aug 9 (~22 days).**
  `GROQ_GNI_NOT_MAD` rotated and **CERTIFIED**: `gh run view 33416590413 --log` shows
  `GROQ_API_KEY: ***` and the run concluded `success`. Old key may now be revoked in the
  `not_mad` Groq dashboard. **REMAINING: `GROQ_API_KEY` (morning — feeds `gni_mad` morning
  slot AND `gni_adaptive` AND `gni_heartbeat`, so blast radius is THREE workflows) and
  `GROQ_MAD_EVENING` (evening MAD only).** The ritual, recovered from the record and now
  proven: dashboard → create key → `gh secret set <NAME>` and **paste at the hidden prompt**
  (never `< file`, never `echo`) → `gh secret list` timestamps before/after → **dispatch the
  workflow and grep the env dump for `***`** → revoke the old key only after a green run.
  **A bare Enter at the prompt writes an EMPTY secret and prints `✓ Set`** — that happened at
  S90 and took `gni_pipeline` down until a re-set; see R-S78-1's amendment.
- **PROBE-DRIFT: OVERDUE since Aug 24 (~7 days), AND ITS INSTRUMENT IS UNARMED.**
  `mad_model_probe.py` is tracked and intact (`13aed42`, 306 lines, repo ROOT not `tools/`),
  but **`../groq_probe_key.txt` is 0 BYTES, dated Jul 7** — the night it was created. So the
  probe has been unrunnable since July, and the overdue clock is measuring the wrong thing.
  **Second, separate gap: what PROBE-DRIFT actually TESTS is not written in any live document.**
  `llm_health_probe` (which runs every pipeline) tests AVAILABILITY only — primary model, then
  fallback. Drift of BEHAVIOUR is what the monthly probe was for, and the definition lives only
  in S57-era records. **Recover the definition before running it; do not infer it.**
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.
- **PROVIDER + PLATFORM EOL WATCH — record at announcement, not at death.**
  - `actions/checkout@v4` + `actions/setup-python@v5` → item 6.7. **All 8 workflows now on v7;
    cert pending one scheduled run of `gni_mad` and `gni_pipeline`.**
  - `gemini-2.5-flash` dies Oct 16 (Lens's lens2 runs on it).
  - `llama-3.1-8b-instant` died Aug 16 — last hardcoded default removed at S89 (9.4).
  - Supabase free tier warns by EMAIL at 20% of a limit, then a grace period, then restricts,
    with no second grace period. Storage 113/500 MB. No longer shared with Project Lens.

### RETIRE CANDIDATES — the clause, honestly counted
- **1.9** — **DISCHARGED THIS CLOSE as CLOSED AS ACCEPTED, with the reason written into the
  item.** The generation-4-of-3 violation generation 9 recorded is now closed. It was
  dischargeable only because the text was recovered from `ee92a5a:93` — the clause cannot be
  applied to an item nobody can read, which is a lesson for 5.8 as much as for the clause.
- **4.4** — promoted with a written reason at generation 7; carried on that reason.
- **5.10 / 5.11** — 5.10 CLOSED this close; 5.11 is in its second generation, not a candidate yet.
- **8.9** — de-scoped at S89, second generation. Not a candidate yet; re-check at generation 12.
- No item is dropped silently this close. Generations 1–7 verified by grep at S88; generation 3's
  disposition READ at S90 (5.10).

---

## CHANGED THIS REGENERATION

**CLOSED:** 8.6 (certified, SQL + browser) · 8.4 (certified in browser) · 9.7 (certified) ·
9.3 (certified, plus two corrections of its own figure) · 9.8 (`e3a4e95`) · 9.6 (except two
unrecovered IDs) · 5.10 (generation 3's disposition read) · **1.9 (retire clause discharged)**.

**SHIPPED, CERT PENDING:** 6.7 (all eight workflows; awaits one scheduled run) · 9.9 and 9.10
(await a non-CRITICAL run — i.e. 8.5).

**NEW ITEMS:** 1.15 (F-86-1, four sessions unnumbered) · 6.8 (heartbeat standdown rationale) ·
9.12 (quota gauge unit mismatch) · 4.6 (cost trend across regimes) · 5.12 (two unread
registers, five sessions unnumbered) · 5.13 (stale roster in the rules header).

**RE-RANKED:** ROOT 9 to TOP (ROOT 8's holding condition — 8.6's cert — is paid, exactly as
generation 9 specified) · **ROOT 7 URGENT → IMPORTANT with a written reason and a checkable
re-rank trigger** · 8.5 raised to S91's mission on the strength of unblocking four items ·
1.11 is now the top open item in ROOT 1 · 9.5 is now the top open item in ROOT 9.

**GRAVEYARD GAINED A ROW:** swapping a published figure for a fresher one without its window.

**DECISION S90-1** — item 1.9 CLOSED AS ACCEPTED rather than promoted. Chosen over promotion
because S85's n=4 harvest measured `TECH=0/N` on every run: a raise-on-zeroed-pillar assertion
would fire constantly against a fail-open law (2.1), and the per-pillar arrival print already
delivers the visibility. Cost accepted: a zeroed pillar remains a WARN-by-inspection condition,
not an enforced one.

**DECISION S90-2** — ROOT 7 DE-RANKED from URGENT to IMPORTANT. Chosen over "work it now" and
over "leave it urgent". Reason: 7.2 is the urgent half and its only proposed shape is in the
GRAVEYARD, while the measurement needed to design a replacement does not exist (7.1's
`checked_spans` is discarded). A root blocked on an instrument is IMPORTANT, not URGENT.
Re-rank trigger written into the root so the decision is reversible on evidence, not on mood.

**DECISION S90-3** — a published figure must carry the WINDOW that produced it. Chosen after
S90 shipped `~16,144/run` in the morning and disproved it in the afternoon: the monthly series
shows two regimes (a flat `6175` reservation era through May, metered from June), so an average
across the boundary is reproducible from no window at all. Applied to both published token
figures; added to the GRAVEYARD as a direction, not just a fix.

**DECISION S90-4** — CONTRACT v8 asserts NO rule id for BIRD-EYE. Chosen over substituting
`GNI-R-180`, which the record supports only in a summary while assigning `GNI-R-037` the
read-the-full-file text elsewhere. Guessing an id would repeat the exact failure being fixed.
Cost accepted: the gate sequence's first step cites a contested id rather than a clean one.

**DECISION S90-5** — `GROQ_API_KEY` and `GROQ_MAD_EVENING` rotations DEFERRED to S91 rather
than completed at S90. Chosen after the `not_mad` rotation produced an empty secret and a red
pipeline: `LR-104` says credential work needs a session opening, and the morning key's blast
radius is three workflows against `not_mad`'s one.

**NOT DONE, NAMED:** 9.5 (the July census audit — scoped as a session, not a task) · 9.11
(needs a 429 that cannot be safely forced) · 3.2 (schema work, needs a session opening) ·
PHISH-HW's browser remainder · two of three key rotations.

---

## HOW THIS FILE IS MAINTAINED
Regenerated at every close, dated, superseding — never appended. The GRAVEYARD is the ONE
section copied forward verbatim. Item numbers must be unique; state the expected count in
advance and grep it before delivery. Decisions live here as DECISION lines, by CONTRACT's
no-fifth-document ruling — they are findable only by reading past order files, and that cost
was accepted knowingly at v5.
