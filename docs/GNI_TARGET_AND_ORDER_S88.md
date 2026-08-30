# GNI TARGET + WORKING ORDER
**SESSION-NUMBERED BY DESIGN (Protocol v4+).** This file ships and lands as
`docs/GNI_TARGET_AND_ORDER_S88.md`. **THE LIVE ORDER IS THE HIGHEST SESSION NUMBER.**

GENERATION 8 · 2026-08-30 · supersedes `GNI_TARGET_AND_ORDER_S87.md` (generation 7).
Regenerated, never appended. HEAD at close: `737ef06`.

---

## NEXT SESSION'S MISSION (S89)

**CERTIFY `ee813c0` + `737ef06` (item 8.6/8.4), THEN PIN THE NODE-20 ACTIONS (item 6.7),
CANARY FIRST.**

| item | what "done" looks like |
|------|------------------------|
| 8.6 cert | one post-commit `reports` row has `escalation_score_raw` NOT NULL, equal to the blob's nested `raw_score`, while `escalation_score` stays 10.0 — and `/autonomy` renders three live cells in the browser |
| 6.7 | `gni_selfcheck.yml` runs green on the new action majors, THEN the remaining 7 workflows are swept in one commit |

**PRE-REGISTERED CERT PREDICTIONS (written before the run exists, R-S85-6 / step 8c):**
1. `escalation_score_raw` is NOT NULL on the first post-`ee813c0` row
2. its value is **> 10.0**
3. `escalation_score` on the same row is **exactly 10.0**
4. `escalation_score_raw` == `(full_analysis::jsonb)->'score_breakdown'->>'raw_score'`
5. `escalation_score_lower` and `escalation_score_upper` stay **NULL** (5.7 untouched)
6. `/autonomy` shows `Final Score 10.0` · `Raw Magnitude 1x–2x.x` · `Upper Bound --`

**FAILURE TEST:** if the insert throws, the column name or type is wrong and the pipeline is
DOWN — check `gh run list --workflow=gni_pipeline.yml` conclusion FIRST, before reading any row.

**CERT QUERY (SQL EDITOR ONLY — never paste into bash, R-S88-1):**
```
select created_at, escalation_score, escalation_score_raw,
       escalation_score_lower, escalation_score_upper,
       (full_analysis::jsonb)->'score_breakdown'->>'raw_score' as raw_in_blob
from reports order by created_at desc limit 3;
```

---

## TARGET (unchanged — no phase transition this close)

**TRUTHFULNESS OF OUTPUT.** What GNI says must be what GNI measured.

**DEFINITION OF DONE — status at this regeneration:**
- the arbitrator reads what it claims to read — ROOT 1 CERTIFIED for CONTENT; **1.14 opens the
  ORDERING question: MAD can start before the pipeline it reads has finished**
- the grounding gate measures reading, not existence — ROOT 7 OPEN
- the escalation score carries information — **ROOT 8: three-quarters answered.** The instrument
  is proven saturated, the level is proven unfixable inside this corpus, the magnitude is
  PERSISTED (`ee813c0`) and the cap is PUBLICLY STATED (`737ef06`). Certification is the open
  quarter.
- the public surface matches the configuration — ROOT 9 OPEN, and WIDER than at generation 7

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
| **8.9 (NEW)** | GEO pillar "active" 196/196 | GEO hits are 8–19 against a cap of 5 — the pillar cannot be inactive |
| **8.10 (NEW)** | PHI-003 gate "protecting" the score | it has never fired in 196 runs; `combo_bonus < 3` mutes it exactly when combos fire |

Its use is predictive — when a metric is >90% constant, ask WHO GUARANTEED IT before tuning it.

---

## THE ORDER

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT · **TOP**

- **8.1** CLOSED (S86) — the audit. Saturation across three layers, confirmed by bytes.
- **8.1a** OPEN — D-11's feeds list misses three consumers: arb prompt L989, `nexus_analyzer:567`,
  `self_bias_gate:46`. Unchanged this close.
- **8.1b** OPEN — NN-5 is a deliberate hard-correction channel (`1da3dfe`) whose switch is stuck.
  Since no recalibration is coming, the switch stays stuck by design decision, not by neglect.
- **8.1c** OPEN and GROWING — `constraint=1092` of `ctx_room=4762` on `33180919784`
  (was 987/5091 at S86): ~19% → ~23% of arbitrator context spent by an always-on branch.
- **8.2** CLOSED (S87) — CERTIFIED 4/4. `4b220ab` merges five unpublished scorer fields.
- **8.3** RULED (S87) — NO RECALIBRATION OF THE LEVEL. See GRAVEYARD row 1.
- **8.4** **SHIPPED (S88) `737ef06`.** `/autonomy` now reads: *"Final score is capped at 10 and
  has been at the cap on every measured run. Raw magnitude is the uncapped signal."*
  Count-free by DECISION S88-1. **Cert is visual, in the browser, with 8.6's.**
- **8.5** OPEN, **RANK RAISED AGAIN.** Exercise `_high_escalation == False` once, deliberately.
  S87 removed the only natural trigger; the selftest fixture hardcodes CRITICAL. S88 adds a
  sibling: **PHI-003 has never fired either (8.10)**. Two untested branches in one scorer.
- **8.6** **SHIPPED (S88) `ee813c0`, CERT PENDING.** `escalation_score_raw double precision`
  added by migration; written by `supabase_saver.py:163` with the house fallback pattern;
  selected in `/api/health` and `/api/latest`; rendered on `/autonomy` in the cell that used to
  show the never-written Lower Bound. `BLOCKER: none. MEASURED — the cert needs one scheduled
  pipeline run, nothing else.`
- **8.7** **RE-SPECIFIED BY MEASUREMENT (S88). The score half is CLOSED; the evidence half is
  OPEN.** Dropping `ceasefire` changes 0 of 196 runs (GRAVEYARD row 2). What survives: `ceasefire`
  reaches the PUBLISHED `signals_found` top-5 in **2 of 196 runs**, so GNI has twice filed a
  de-escalation word as geopolitical danger evidence. The remaining work is the direction-neutral
  audit of the published EVIDENCE STRINGS (`factors`, `signals_found`), not of the arithmetic.
  `sanction`, `troops`, `naval`, `dollar`, `gold`, `treasury` are the other candidates.
- **8.8** OPEN — 19 keywords never fire in 192 runs: GEO 1 (`invasion`), TECH 3, **FIN 15**.
  **DO NOT DELETE THEM** — their silence is the finding: the financial system has not broken
  once in this window. Absence is evidence (Protocol step 8h).
- **8.9** **NEW.** GEO pillar is CAP-SATURATED on 196/196 runs (hits min 8 / median 14 / max 19
  vs cap 5). This is WHY 8.7's word-list fix was inert, and it generalises: no edit to
  `GEO_SIGNALS` can move the score while headroom is zero. Measure headroom before any list
  proposal (R-S88-5). TECH and FIN headroom is UNMEASURED — measure both before 8.8.
- **8.10** **NEW.** PHI-003 has never fired in 196 runs. It requires calm sentiment AND calm risk
  AND `combo_bonus < 3` AND `final_score > 5` — and combos fire near-daily, so the gate is muted
  exactly when it would matter. Pairs with 8.5: both are dead branches in the same file. Also:
  `final_score = max(final_score, 1.0)` is an undocumented floor that min-raw 5.6 can never reach.

### ROOT 1 — THE ARBITRATOR'S INTAKE · CERTIFIED FOR CONTENT, OPEN FOR ORDERING
- **1.14** **NEW, URGENT — THE PIPELINE↔MAD ORDER CAN INVERT, AND DID.** Promoted from the S87
  trap on its second carry, with measurement. On 2026-08-30 MAD `33318313852` STARTED at
  14:58:17Z; pipeline `33318041130` FINISHED at 14:58:20Z — the debate began **3 seconds before
  the articles it debates were written**. All 28 runs are `event=schedule`; no human hand.
  The law is exact: real gap = 30 min designed MINUS (pipeline lateness − MAD lateness); pipeline
  duration is stable at 6m02–6m35 over 12 runs, so the order flips whenever that difference
  exceeds ~23m45s. Measured 23m50s on the inverted pair. 8 pairs measured, median gap 15m02s,
  min 3m21s — **the designed 30 min was never once achieved.**
  `BLOCKER: ASSERTED, UNTESTED` — job START is not the DB READ, so a stale debate is not yet
  proven. **The one measurement that settles it:** read `33318313852`'s log for its article
  fetch timestamp and article count, and compare against `33318041130`'s written row.
  If stale, this is a silent live failure and outranks everything (ABSOLUTE rule).
- **1.6** OPEN, confirmed 14/14 + 4/4 + 2/2 — `/debate` publishes R1, which the verdict-bearer
  never read. Unchanged. **This is a TRUTHFULNESS defect on a public page and has been open
  since S83; it should be reconsidered against ROOT 9 at the next regeneration.**
- **1.7** OPEN — needs one `truncated=0` run to settle partial-line inflation. **NOTE THE
  CONFLICT:** S86 recorded `truncated=0` and pillar-sum 39 == arrived 39 on run `33114821663`.
  Either 1.7 is already discharged or the trap it names is narrower than written. One read.
- **1.8** OPEN, unchanged — `bool(mad_bull_case)` may still leak success past the veto; L275-295.
- **1.9** DE-RANKED, unchanged.
- **1.11** OPEN, TRIGGER FIRED (S86), boundary pinned 39–41 (S87). Round-robin pillar fill.
  Ranked below 1.14 because 1.14 is an ordering failure and 1.11 is a composition improvement.
- **1.12** OPEN, unchanged — `GROQ_MODEL_FALLBACK` reaches no workflow. **Do not wire it before
  reading its value.**
- **1.13** OPEN — TECH starved in two layers independently (funnel 4 of 22; ladder dies first).
  **S88 adds the missing half: TECH's own cap headroom is unmeasured (8.9).**
- **1.1 / 1.2 / 1.3 / 1.4 / 1.5 / 1.10** CLOSED in earlier sessions.

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION · **RANK RAISED TO URGENT**
*Justification naming the target: 8.6 published a second number beside the level. A page that
computes the level from a DIFFERENT threshold table than the engine will now show readers two
numbers that contradict each other. The cap has hidden this for 196 runs; it stops hiding it.*
- **9.7** **NEW, URGENT.** THREE threshold tables existed for one scorer:
  `escalation_scorer.py:118-127` = **9/7/5/3** · `autonomy/page.tsx:38` `scoreToLevel` =
  **8/6/4/2** · `design_bench.py:39` = 8/6/4/2, **fixed this session in `e7e2453`**. At a score
  of 8.0 the engine says HIGH and the public page says CRITICAL. Never observed because 196/196
  sit at 10.0 — a latent defect that 8.6 makes visible. Fix is one line; the sweep is the item.
- **9.8** **NEW.** `autonomy/page.tsx:38` carries the comment *"FT-11: no escalation_level column
  in DB"*. FALSE — `supabase_saver.py:162` writes it and `information_schema` lists
  `escalation_level text`. A false comment caused a whole client-side re-derivation (9.7).
  Grep for other `FT-` comments; they are census artifacts that became code lore.
- **9.3** OPEN — "4 pipelines" wrong in six places. **The word is James's call (DECISION S85-5).**
- **9.4** OPEN — `stock-context/route.ts:81` defaults to a dead model. Pairs with 2.4.
- **9.5** OPEN — eight unresolved S69 census flags; F14 (`/comparison` renders BEARISH over a
  NEUTRAL verdict) is the ugly one. RE-CERT never ran. Unaudited since July.
- **9.6** OPEN — three ID schemes in the register. Pairs with 5.6.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · URGENT
- **7.1** PARTLY PAID (S86). `checked_spans` computed and discarded at the print. R-S87-7 instance.
- **7.2** Decide the fix shape. Per-speaker baskets are in the GRAVEYARD. Unchanged.
- **7.3** PARTLY DISCHARGED (S86). Unchanged.
- **7.4** OPEN — per-run line counts include dialect, the digest excludes it. Never compare them.

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM · **RANK RAISED**
- **6.7** **NEW, URGENT — NODE 20 DEPRECATION IS LIVE IN TODAY'S LOGS.** Every workflow run now
  prints *"Node 20 is being deprecated. This workflow is running with Node 24 by default."*
  8 workflows, 19 call sites, all on `actions/checkout@v4` + `actions/setup-python@v5`.
  Current majors, read from GitHub not memory on 2026-08-30: **`checkout@v7.0.1`,
  `setup-python@v7.0.0`** — three majors behind. When the forced Node 24 run stops, EVERY
  workflow stops, from no change of ours. `BLOCKER: none. MEASURED — versions read from the
  API, call sites greped.` **Canary = `gni_selfcheck.yml`** (runs every 30 min, holds `checkout`
  only, produces no intelligence). **TRAP: `gni_mad.yml` and `gni_pipeline.yml` each contain TWO
  jobs with these actions — a patch asserting `count==1` will abort there.**
- **6.5** **THERE IS NO BACKUP.** Unchanged and still true.
- **6.2** Retention policy. Promoted at generation 3 (S86); unchanged.
- **6.3** SIZE METER in Mission Control. Unchanged.
- **6.4** L5 exposure when Supabase 402s. Gates 6.2.
- **6.6** OPEN — four `lens_*` tables share GNI's 500 MB project; every runway figure includes
  another system's growth. **Requires the SQL editor, not bash (R-S88-1).**
- **6.1** CLOSED (S84).

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** HALF-RULED (S86) — clause 2 (LABELED coverage) unmeasured; that is the only thing
  keeping 2.1 open.
- **2.2** Build B only if 2.1's second clause triggers it.
- **2.3** NARROWED (S87) — both external explanations eliminated by replay. Remaining candidates
  are all INTERNAL: article mix, prompt growth, corpus drift, agent habituation.
- **2.4** `/stocks` may render frozen prices. One grep settles it.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** WIDENED (S86) — `conf = 0.5` exactly on Jun 11 and Jul 7; wider than Jul 19–22.
- **3.2** `data_era` column + tagging. Unchanged. **Originally due ~Aug 2 as "QUARANTINE SQL";
  missed during the Jul-27→Aug-17 gap. Recorded so the age is visible, not re-ranked.**

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.5** **STILL UNREAD SINCE JUL 27 (34 days)** — C1's real token bill, in the `groq_quota`
  TELEGRAM line, not the workflow log. `BLOCKER: none. This is a READ, not a measurement —
  it has never been attempted, which is different from being blocked.`
- **4.1** C2 solver recalibration. `ctx-trim` fired again at S87, so not dormant.
- **4.4** Measure chars/token PER POSITION. `//3` is SAFE; do not move to `//4`.
- **4.3** Groq TPD refills continuously.
- **4.2** CLOSED AS ACCEPTED (S86).

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** `DEBT_REGISTER_S69.md` has no reader. Unchanged.
- **5.6** `GNI_RULES.md` is now **55,666 bytes** (was 52,174) — it grew again this close. Largest
  artifact in the set, ~41% of the opening read, and no session reads it end to end. Pairs with
  9.6. **S88 note: the GRAVEYARD section is the counter-experiment — a short, mandatory,
  regenerated list beats a long, optional, appended one. If GRAVEYARD works, migrate more.**
- **5.7** **BYTE-CONFIRMED (S88), no longer a census.** Seven `reports` columns are never written
  by `supabase_saver`. Two of them — `escalation_score_lower` / `escalation_score_upper` — are
  **RENDERED on `/autonomy`**, so the panel has been showing `--` in two of three cells since it
  shipped. `sentiment_score_lower/upper` DO get the fallback pattern
  (`float(report.get("x_lower", report.get("x", 0.0)))`); escalation never received it.
- **5.8** **NEW.** UNNUMBERED items are invisible to the uniqueness assert and vanish without a
  disposition. Proof: "delete `docs/STATUS.md`" appeared unnumbered in generations 4, 5 and 6 and
  is absent from generation 7 with no CLOSED or RETIRED line. Every item gets an ID from now on.
- **5.9** **RECOVERED FROM GENERATION 6.** Delete `docs/STATUS.md` — a fossil frozen at S46,
  retired as a file type at Protocol v1, never deleted. One `git rm`.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
**WRITTEN OUT IN FULL. "Unchanged from generation N" is BANNED here (DECISION S88-4): a
compressed deadline is an invisible deadline, and this block lost its visibility for exactly
one regeneration at generation 7.**
- **PHISH-HW: OVERDUE since ~Jul 31 (~30 days).** OAuth + GitHub Apps review, security log from
  2026-07-18, report the trypatchhog.com mail. Browser, James solo, ×3 accounts.
- **KEYFILE ROTATION: OVERDUE since Aug 9 (~21 days).** One account at a time, quiet window
  ~03:30–09:30 UTC. Receipts = `gh secret list` updatedAt before/after; never echo a key.
  **NOTE: the "quiet window" assumes the old schedule. Lateness now runs 4–12 h (see 1.14) —
  re-derive the window from `gh run list` on the day, do not trust the stored hours.**
- **PROBE-DRIFT: OVERDUE since Aug 24 (~6 days).** Monthly, needs James's explicit authorization
  each run, never on a near-red account.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.
- **PROVIDER + PLATFORM EOL WATCH — record at announcement, not at death.**
  - **`actions/checkout@v4` + `actions/setup-python@v5` → item 6.7, LIVE WARNING TODAY.**
  - `gemini-2.5-flash` dies Oct 16 (Lens's lens2 runs on it).
  - Supabase free tier warns by EMAIL at 20% of a limit, then a grace period, then restricts,
    with no second grace period. Storage 113/500 MB, shared with Project Lens (6.6).

### RETIRE CANDIDATES — the clause, honestly counted
- **1.9** — de-ranked at generation 5, unworked since. **Generation 3 of 3 — DUE AT S89.** It is
  CLOSED as accepted or PROMOTED with a written reason at the next close. Not this one.
- **4.4** — promoted with a written reason at generation 7; carried on that reason.
- No item is dropped silently this close. **Generations 1–7 verified by grep this session:**
  5.1 / 5.2's CI half / 5.3 were CLOSED AS ACCEPTED at S84, and 5.2's fallback half was PROMOTED
  to 1.10 — the clause worked, and S88's initial claim that they vanished was WRONG (R-S88-3).

---

## CHANGED THIS REGENERATION

**MISSION: HALF COMPLETED, AND THE OTHER HALF ANSWERED RATHER THAN SHIPPED.** S88's declared
mission was "ship 8.6 (publish the uncapped magnitude), then 8.7 (polarity)". **8.6 SHIPPED**
(`ee813c0`), cert pending on the next scheduled run. **8.7 was MEASURED instead of shipped**:
the proposed one-line fix moves 0 of 196 runs, so shipping it would have been unverifiable code
in the public path. The item was re-specified around what survives. **8.4 shipped unplanned**
(`737ef06`) because 8.6 cleared its gate mid-session — logged as an in-mission extension, not
scope drift, since 8.4's own text names 8.6 as its only blocker.

**SHIPPED:** 8.6 `ee813c0` · design_bench threshold fix + 8.7 candidate `e7e2453` ·
8.4 `737ef06`. Three commits, all with `npm run build` 40/40 and explicit staging.

**CLOSED:** 8.7's score half (measured to zero effect) · the S87 spacing trap (promoted).

**NEW:** 1.14 (pipeline↔MAD inversion, MEASURED) · 6.7 (Node 20 EOL, live warning) ·
8.9 (GEO cap saturation) · 8.10 (PHI-003 never fires) · 9.7 (three threshold tables) ·
9.8 (the false FT-11 comment) · 5.8 (unnumbered items vanish) · 5.9 (STATUS.md, recovered) ·
the GRAVEYARD section.

**RE-RANKED:** **ROOT 9 rises to URGENT** — 8.6 published a second number, and 9.7 means the
page can now contradict the engine in public. **ROOT 6 rises** on 6.7 alone. ROOT 8 keeps the
top slot only until 8.6's cert is read; after that it drops behind ROOT 9 and 1.14.

**DECISION S88-1 — 8.4 ships COUNT-FREE (option A over B and C).** Chosen over B ("the cap, not
the world") and C (the full numbers: 196 runs, 10.3–26.8, median 19.2). Reason: C's four
constants are exactly ROOT 9's disease — `196` was `193` two hours earlier and will be `197`
tomorrow, so C would have closed one instance of ROOT 9 by creating another. B editorialises one
step toward the false exoneration that 8.4's own text forbids. S77's count-free-prose precedent
and S85's 9.1 (remove rather than update) both point at A. `LINEAGE:` line carried.

**DECISION S88-2 — the ORDER gains a GRAVEYARD section, carried forward verbatim at every
regeneration; Protocol swept to v8 the same close (R-S82-4).** Chosen over a new register file
(M3's no-fifth-document rule holds) and over relying on `tools/design_bench.py` alone (it covers
the scorer only; round-robin and per-speaker baskets have no tool). Reason: the June option-B
design survived five sessions because "regenerate, never append" quietly discards refutations
along with everything else. **Cost accepted in writing: a carried-forward block is exactly the
mechanism that produced this project's hazard-accumulation failures, so GRAVEYARD is capped at
one screen and every row must name the MEASUREMENT that killed it — a row without evidence is
deleted at the next close, not carried.**

**DECISION S88-3 — 8.7 is NOT shipped; the item is re-specified around published evidence.**
Chosen over shipping the one-line `ceasefire` removal anyway ("it is still more correct"), and
over dropping 8.7 entirely. Reason: replayed n=196 the edit moves 0 runs, and DECISION S85-3's
precedent is explicit — an unverifiable change does not go into the public path, however
plausible. What survives measurement is the 2-of-196 appearance in published `signals_found`,
which is a truthfulness defect about EVIDENCE, not about arithmetic. `LINEAGE:` line carried
(GRAVEYARD row 2, R-S87-1, the bench output).

**DECISION S88-4 — DECISION S87-6 IS ADOPTED, and the LIFECYCLE block may never be compressed.**
Ruled by James this close, ending the pending status carried from S87. Every item claiming a
block names the measurement that established it or is marked `ASSERTED, UNTESTED`; an untested
blocker may not stop work. Extended by S88's own evidence: generation 7 compressed LIFECYCLE to
"Unchanged from generation 6", which made three overdue security deadlines and a live platform
EOL invisible in the file every session is required to read. **Compression is the same failure as
an unexamined blocker: both make work disappear without anyone deciding it should.**

**DECISION S88-5 — the Node-20 pin waits for S89 and goes canary-first.** Chosen over shipping
it this session. Reason is ATTRIBUTION, not risk appetite: `ee813c0` is uncertified, and changing
all 8 workflows before its cert would make a failed next run un-diagnosable between the column
write and the action bump. Three major versions is not a version bump, it is a migration.
`gni_selfcheck.yml` runs every 30 min, holds `checkout` only and produces no intelligence — it is
the canary. Recorded as James's ruling.

**TRAP DISPOSITION (promote or expire, no trap rides forward unchanged twice):**
- pipeline↔MAD spacing — SECOND CARRY → **PROMOTED**: the lesson into **R-S87-6 as an AMENDMENT**
  (not a new number — the existing rule already owns scheduler timing, and Lens paid for
  re-minting LR-119 as LR-144), and the work into **item 1.14** with a named measurement.
- NEW TRAP (first carry, temporary): `/autonomy` will render `Raw Magnitude --` until the first
  post-`ee813c0` pipeline run writes a row. Anyone opening the page before then sees the same
  `--` the never-written Lower Bound used to show and will read the ship as a failure.
  **Expires the moment cert prediction 1 is checked.**

**ITEM UNIQUENESS — 54 distinct item IDs, with exactly two intentional repeats.**
The count was pre-registered at **53** and the grep returned **54**; ROOT 8 was counted as 12
items when it holds 13. Logged in the wrongness ledger — **second consecutive close where the
pre-registered count was off by exactly one, which is now a pattern, not an accident: both
misses came from counting a root's items from memory instead of listing them.** The assert did
its job both times. `1.9` and `4.4` appear twice by design — once in THE ORDER and once under
RETIRE CANDIDATES, which is the retire clause showing its working. Verify:
```
grep -oE '\*\*[0-9]+\.[0-9]+[a-c]?\*\*' docs/GNI_TARGET_AND_ORDER_S88.md | sort | uniq -d
```
must print ONLY `**1.9**` and `**4.4**`, and `... | sort -u | wc -l` must print 54.

---

## HOW THIS FILE IS MAINTAINED
Regenerated at every close, dated, superseding. Never appended — **except the GRAVEYARD, which
is carried forward verbatim (DECISION S88-2, Protocol v8 PART C step 5).** One mission per
session, taken from the top. Decisions live here as DECISION lines — GNI mints no separate
D-register. FRESHNESS CONFERS NO PRIORITY.
