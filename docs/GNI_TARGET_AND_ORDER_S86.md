# GNI TARGET + WORKING ORDER
**SESSION-NUMBERED BY DESIGN (Protocol v4+).** This file ships and lands as
`docs/GNI_TARGET_AND_ORDER_S{N}.md`. **THE LIVE ORDER IS THE HIGHEST SESSION NUMBER.**
GENERATED: 2026-08-28 (S86 close) · SUPERSEDES: the S85-close generation · HEAD `a4514ee`
GENERATION: 6

---

## NEXT SESSION'S MISSION (S87)
**SHIP 8.2 — `score_breakdown` PERSISTENCE — THEN SWOT THE RECALIBRATION (8.3).**

ROOT 1's cert is read, so ROOT 1 drops out of the top slot exactly as generation 5 said it
would. ROOT 8 is now the top root, and its audit (8.1) is DONE — done by bytes, this session.
What remains is that **nothing about ROOT 8 is provable by SQL until `score_breakdown` is
stored**, and that is the smallest commit this root admits.

| step | what | done when |
|---|---|---|
| 8.2 | persist `score_breakdown` (per-pillar hits, base, diversity, combo, gate) to `reports` | one run writes a row with a readable breakdown |
| 8.3 | SWOT the recalibration, having READ the March design first | lettered options with `LINEAGE:` |

**LINEAGE-BEV IS PRE-PAID FOR 8.3.** The design D-11 calls "June Option B" does not exist in
`docs/` under that name (F-86-6). It is in the **2026-03-24 conversation record**, where it is
called **"Fix 2 / Recalibration Strategy"** and "Option B" names a different thing (frequency
controller display). Its content: two-tier signal lists (background 0.3 / escalation 1.5),
`base = min(sum, 7.0)`, combos become meaningful. **It never carried exact values** — its own
author wrote that the values must be read from the full lists, not guessed. So 8.3 derives
values (R-S81-5); it does not "implement Option B".

**James may flip this to 1.11**, whose numeric trigger fired this session. The case for ROOT 8
first: a false number is published daily to the site, Telegram and the frequency controller,
while 1.11's cost so far is one TECH article on one run. The case for 1.11: it is a standing
pre-ruled commitment and the loss grows with volume. Ranked, not assumed.

---

## TARGET (unchanged — no phase transition this close)

> ### TRUTHFULNESS OF OUTPUT
> Everything GNI publishes is either grounded in something an agent actually read, or is
> visibly labeled as speculation.

**DEFINITION OF DONE — status at this regeneration:**
1. **Arrival is asserted, not assumed.** — **CERTIFIED (S86), narrowed.** `228634c` proven on
   two post-change runs: arrived 20 → 39-41, TECH 0 → 9-12, dropped 10-18 → 0-2. Not "done":
   the fix holds **only while `assembled` stays at or under ~40** (F-86-9), and 1.6/1.8 are open.
2. **Label coverage matches fabrication surface.** — OPEN. ROOT 7 unchanged.
3. **GT5-T2 ruled with normalized evidence.** — **HALF-RULED (S86).** Clause 1 answered from
   n=20: 8.3 arb hits/run against a `>= ~12` trigger, and the scale error runs the SAFE way
   (our number INCLUDES dialect; the trigger excludes it), so trigger B does not fire and
   default A stands. Clause 2 (LABELED coverage) is still unmeasured.
4. **Evidence base clean of fallback-era contamination.** — OPEN, and **WIDER than ROOT 3
   describes**: `mad_confidence = 0.5` exactly appears 11× in June and 7× in July (F-86-8).
5. **The numbers GNI publishes mean what they appear to mean.** — OPEN. **ROOT 8, audited this
   session, fix not started.**

---

## THE ORDER

Ranked against the declared target. **Freshness confers no priority.** Work the top. If you
believe the order is wrong, say so and propose a re-order — do not silently work something else.

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT · **TOP**
*Audited by bytes at S86. Every claim below is now byte-backed, not register-quoted.*

**8.1 CLOSED (S86) — the audit.** `ai_engine/analysis/escalation_scorer.py`, 191 lines:
- Saturation layer 1: `min(len*1.5, 5) + min(len*1.0, 5) + min(len*0.8, 4)` — **max 14 against
  a final cap of 10.** Four TECH hits, five GEO, five FIN saturate every pillar; the lists carry
  `'china'`, `'russia'`, `'military'`, `'dollar'`, `'tariff'` — daily words.
- Layer 2: `diversity_bonus = (active-1)*1.5 = 3.0`, guaranteed by the funnel's pillar quota.
- Layer 3: `CRITICAL_COMBOS` matched with `all(kw in combined_text)` over the joined corpus —
  `hormuz`+`iran` fires on any oil story.
- **The PHI-003 gate mutes itself:** its condition includes `combo_bonus < 3`, and the combos
  reach 3 on ordinary days. D-11's claim was right, and the bytes say exactly why.

**8.1a NEW FINDING — the feeds list in D-11 is INCOMPLETE. Three consumers were unlisted:**

| consumer | site | in D-11? |
|---|---|---|
| **Arbitrator prompt** (`mad_protocol.py:989` `_high_escalation` → `_hard_constraints`) | measured 6/6 | **no** |
| `nexus_analyzer.py:567/569` branching | grep | **no** |
| `self_bias_gate.py:46` | grep | **no** |
| frequency controller · historical_correlations · alerts · escalation_level | grep | yes |

**8.1b NEW FINDING — NN-5 is a crisis channel that never leaves crisis mode.**
`_high_escalation` is True on **6 of 6** measured runs, and `NN-5: 2 hard constraint(s)` printed
with zero variance across three days. `1da3dfe` (2026-05-17) shows this was **deliberate design**
— "hard correction channel, Black Swan + Ostrich enforced at code level for HIGH/CRITICAL". The
defect is therefore NOT the constraints and NOT their asymmetry; **it is that the switch cannot
go False.** Fixing the scorer restores NN-5 to its designed behaviour with no change to NN-5.
Corollary: the `if _high_escalation:` False branch has never executed in production, and
`mad_protocol.py:1303`'s selftest fixture hardcodes `'escalation_level': 'CRITICAL'` — so the
branch is untested in both places.
**NOT SUPPORTED:** that NN-5 biases the verdict. See F-86-7 and W-86-4 — the data refutes it.

**8.1c ROOT 8 COSTS ROOT 1 BUDGET.** ARB-DRYRUN prints `constraint=987` against `ctx_room=5091`.
At ~124 chars/article that is **6-7 articles per run**, spent by an always-on branch. Recorded
as a link, NOT as a promise: a stopgap never closes a root, and freed capacity goes where the
system sends it (R-S82-3).

- **8.2** **NEXT.** Persist `score_breakdown` to `reports`. Smallest first commit; everything
  else in this root is unprovable by SQL without it.
- **8.3** SWOT the recalibration. Read the March-24 design first (see MISSION). Derive values
  from the live corpus; never hand-pick (R-S81-5).
- **8.4** Decide what the PUBLIC surface says meanwhile. A caveat is cheaper than a
  recalibration and can ship first.
- **8.5** **NEW.** Exercise the `_high_escalation == False` path once, deliberately, before 8.3
  ships. A branch that has never run is not a branch that works.

### ROOT 1 — THE ARBITRATOR'S INTAKE · **CERTIFIED, NOW CLOSING** (1.11 excepted)

**1.3 CLOSED (S86) — CERTIFIED.** Two post-change runs on `a4514ee`:

| run | available | assembled | arrived | trunc | dropped | GEO | FIN | TECH | ctx-trim | arb hits |
|---|---|---|---|---|---|---|---|---|---|---|
| `33075059391` | 209 | 43 | 41 | 1 | 2 | 15/15 | 15/15 | 12/13 | **@5091** | 10 |
| `33114821663` | 233 | 39 | **39** | **0** | **0** | 15/15 | 15/15 | **9/9** | **gone** | 10 |

Run 2 satisfies **all five predictions exactly**. Run 1 satisfies two. The difference is not two
outcomes but **one boundary: `assembled` 39 vs 43.** Below ~40 the ladder never cuts; above it,
ctx-trim returns and the pillar-ordered tail dies again. The predictions were not wrong — they
omitted a condition (R-S86-5).
**FAILURE TEST DID NOT FIRE:** arb hits 10 and 10, against a pre-registered baseline of n=20
(mean 8.3, max 13, SD 2.6) banked before either run was read.

- **1.11** **URGENT — TRIGGER FIRED (DECISION S85-3 discharged).** Both conditions met on
  `33075059391`: `assembled = 43 >= 39` **and** `ctx-trim@5091` returned. Round-robin is no
  longer a no-op and is now certifiable. Ship per S85's own instruction: **measure first** — add
  a round-robin variant line to ARB-DRYRUN, print-only, then change the fill.
  **RE-RANK TRIGGER:** if any run prints a pillar below 50% of its available count, 1.11 jumps
  above ROOT 8 without further debate.
- **1.6** OPEN, CONFIRMED 14/14 + 4/4 + **2/2 (S86: `R1=DROPPED` on both cert runs)** —
  `/debate` publishes `mad_round1_positions` the verdict-bearer never read. Unchanged by
  `228634c`.
- **1.7** **ANSWERED IN PART (S86).** Headers and content now agree at the pillar level
  (`TECH=9/9`, `12/13`). One-article discrepancy remains between ARB-ARRIVAL's `TECH=12` and
  greedy's `TECH:11` on the truncated run — consistent with the partial-line trap. Close after
  one clean read on a `truncated=0` run.
- **1.8** OPEN, unchanged from generation 5's re-specification: `bool(mad_result.get(
  'mad_bull_case',''))` is still the last clause of `_compute_mad_succeeded`'s OR chain
  (`mad_runner.py` L275-295) inside a function whose docstring says that leak was closed. One
  byte-read against the `mad_arb_failed` veto settles it.
- **1.9** **DE-RANKED as generation 5 pre-authorised.** Zeroed pillars did not occur on either
  cert run; the RAISE is no longer urgent. Kept as an assertion item under 1.11's measurement.
- **1.12** OPEN, unchanged. `GROQ_MODEL_FALLBACK` reaches no workflow; `nexus_analyzer.py:29`
  defaults to `llama-3.1-8b-instant`, a corpse. **Do NOT wire the secret before reading its
  value.** Fix the two code defaults, or read the value first.
- **1.1 / 1.2 / 1.4 / 1.5 / 1.10** CLOSED in earlier sessions.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · URGENT
Basket re-verified by bytes at S85 (`mad_protocol.py:738` = `all + weak`). `228634c` improved the
arbitrator's ratio (now ~39-41 : 209-233, roughly 18%) and did not close the root.

- **7.1** **PARTLY PAID (S86), and it grew a second half.** The arbitrator's post-`228634c`
  ratio is measured above. NEW: **`check_grounding` already computes `checked_spans`
  (`mad_grounding_gate.py:213/220/286`) and the log line throws it away** (F-86-2). The
  denominator needed for a RATE exists and is discarded at the print. One log-line change makes
  every future grounding number normalizable.
- **7.2** Decide the fix shape. Per-speaker baskets make the gate STRICTER and **C stays
  rejected** under 2.1's standing law (fail-open is law, gates starve). Labelling first.
- **7.3** **PARTLY DISCHARGED (S86).** Its blocking function is spent: 2.1's first clause is
  ruled from the per-run instrument (see 2.1). What survives is the July numbers as a lower
  bound for clause 2 only.
- **7.4** **NEW — TWO INSTRUMENTS, ONE WORD, DIFFERENT COUNTERS.** The per-run line prints
  `len(grounding_shadow['consultant_hits'])` (`mad_protocol.py:1164-1168`) and L753 extends the
  bucket with `_g['hits']` **entire — dialect included**. `check_grounding`'s own `hit_count`
  (L299) excludes dialect, and the watch digest excludes it per GT-1. So the two published
  numbers are on different scales, and no document said so. Cheap fix: print `hit_count`
  alongside, or state the scale at the call site. **Until then, never compare the two.**

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION, AND NOBODY OWNS THE DRIFT · IMPORTANT
- **9.1 / 9.2** SHIPPED (S85) `2afec7b` / `bb9e299`.
- **9.3** OPEN — "4 pipelines" wrong in six places (`methodology:25,115`, `research:105`,
  `devops:74,124`, `about:174`); `gh workflow list --all` = 8, all active. **Vocabulary ruling,
  James's call** (DECISION S85-5). `devops:40`'s `const pipelines = [` array must move with the
  heading.
- **9.4** OPEN — `src/app/api/stock-context/route.ts:81` defaults to a dead model. Pairs with 2.4.
- **9.5** OPEN — eight unresolved S69 census flags, RE-CERT never ran. **F14 remains the ugly
  one:** `/comparison` can render "Both signals point BEARISH" over a NEUTRAL verdict.
- **9.6** OPEN — three ID schemes in the register (`GNI-R-###` ×7 lines, `R-S##-#` ×105, plus
  `LR-###`); CONTRACT cites GNI-R-037 / 076 / 233 as live law. LINEAGE-BEV depends on `docs/`
  greps, so register coherence is now a dependency of the gate.

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM · IMPORTANT
- **6.5** **THERE IS NO BACKUP.** Unchanged and still true. `LAST BACKUP: No backups`; no PITR
  on free tier. Cheapest viable form: scheduled `pg_dump` of the four tables that matter,
  weekly, to a private repo. Ranked on irreversibility (DECISION S84-5).
- **6.2** Retention policy. **Retire count: generation 3 of 3 — RULED THIS CLOSE, see CHANGED.**
- **6.3** SIZE METER in Mission Control — platform meter (113), never `pg_database_size` (93).
- **6.4** L5 exposure when Supabase 402s. Gates 6.2.
- **6.1** CLOSED (S84).

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** **HALF-RULED (S86) — trigger B does NOT fire.** n=20 per-run arb hits: mean **8.3**,
  median 9, min 3, max 13, SD 2.6, against the `>= ~12 per completed run` trigger. The scale
  mismatch (7.4) runs the SAFE way: our figure INCLUDES dialect, the trigger's source excluded
  it, so the true value is at or below 8.3. **Default A stands.** Clause 2 — "LABELED fired in
  fewer than half the runs that had hits" — is unmeasured and is all that keeps 2.1 open.
- **2.2** Build B only if 2.1's second clause triggers it.
- **2.3** **RE-SPECIFIED BY DATA (S86). The migration frame cannot answer the question.** The
  per-month cut is now run:

  | month | runs | bull | neut | bear | avg conf | sd | `conf = 0.5` exactly |
  |---|---|---|---|---|---|---|---|
  | 2026-05 | 17 | 0 | 1 | 16 | 0.794 | 0.024 | 0 |
  | 2026-06 | 61 | 0 | 23 | 35 | 0.696 | 0.128 | **11** |
  | 2026-07 | 58 | 1 | 40 | 16 | 0.582 | 0.061 | **7** |
  | 2026-08 | 52 | 4 | 39 | 9 | 0.549 | 0.054 | 0 |

  Bearish 94% → 17%; confidence 0.794 → 0.549. **This is a four-month slide, not a step at any
  commit** — so "did the Jul-24 migration make the arbitrator timid?" is unanswerable as posed,
  and S82's "five verdicts all 0.48-0.53 timidity band" was an artifact of n=5 (Aug sd = 0.054
  spans ~0.44-0.66). Re-specified question: **what varies continuously?** Candidates: world
  volatility, article mix, prompt growth, corpus drift. **No control exists** — the honest
  status is "measured, uncaused".
- **2.4** `/stocks` may render prices frozen since first insert. One grep settles it.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** Pin the exact window from funnel-log engage/disengage lines, not memory. **WIDENED:**
  the `conf = 0.5` exact count (2.3's table) puts 11 defaulted rows in **June** and 7 in July —
  outside the Jul 19-22 window this item describes. March's record calls this the MAD JSON parse
  default. Whatever 3.1 pins, it must explain June.
- **3.2** `data_era` column + tagging, count-before == rows-updated, exclude in GPVS/quality
  queries. James solo in SQL.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.5** **STILL UNREAD SINCE JUL 27 — C1's real token bill.** TELEGRAM `groq_quota` line, not
  a workflow log. Blocks 4.1.
- **4.1** C2 solver recalibration. **`228634c` did NOT make this dormant:** `ctx-trim` fired on
  one of two cert runs, so the "N sacred" / "ctx-trim kills N" contradiction is live above
  `assembled ≈ 40`. Answered from the cert; item stands.
- **4.4** Measure chars/token PER POSITION. `//3` over-estimates and is SAFE; do not move to `//4`.
- **4.2** Nine 429s/run at 46.6-60.4s; read the site before any claim. *(Retire gen 3 of 3 —
  RULED THIS CLOSE, see CHANGED.)*
- **4.3** Groq TPD refills continuously; "wait until tomorrow" estimates are unsound.

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** `docs/DEBT_REGISTER_S69.md` has no reader. **S86 read it and paid for it** — the read
  is what produced 8.1a and F-86-6. Live rows worth migrating: **J-1**, **J-5**, **J-6**,
  **D-5**, **D-10**. Decide its fate; do not leave it as-is.
- **NEW, unnumbered:** delete `docs/STATUS.md` (fossil at S46).

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
- **PROBE-DRIFT: OVERDUE since Aug 24 (4 days).** Needs James's explicit authorization each run.
- **KEYFILE ROTATION: OVERDUE since Aug 9 (19 days).** One account at a time, quiet window.
  Receipts = `gh secret list` updatedAt before/after; never echo a key.
- **PHISH-HW: OVERDUE since ~Jul 31 (28 days).** Browser, James solo, x3 accounts.
- **PROVIDER + PLATFORM EOL WATCH.** Record at announcement, not at death. Read the meter, not
  the mail. · `gemini-2.5-flash` dies Oct 16. · `actions/checkout@v4` + `setup-python@v5` are
  Node-20 and force-run on Node 24; pin newer versions before forcing stops. · Supabase free tier
  warns by email at 20% from a limit; GNI is at 23% of the database quota.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.

### RETIRE CANDIDATES — the clause, honestly counted
- **6.2 retention** — reached generation 3. **PROMOTED with a written reason** (see CHANGED).
- **4.2 retry-window** — reached generation 3. **CLOSED AS ACCEPTED** (see CHANGED).

---

## CHANGED THIS REGENERATION

**MISSION: COMPLETED.** S86's declared mission was "certify `228634c` against its five
pre-registered predictions plus the arb_hits failure test, then open ROOT 8". Both halves done:
the cert is read on two runs, and ROOT 8's audit (8.1) is closed by bytes.

**CLOSED:** 1.3 (certified) · 8.1 (audited) · 7.3's blocking role · one trap expired.

**PARTLY PAID:** 7.1 (arb ratio recomputed; `checked_spans` finding added) · 2.1 (clause 1
ruled) · 1.7 (headers agree; one clean run needed).

**RE-SPECIFIED:** 2.3 (a slide, not a step — the migration frame cannot answer it) · 3.1
(widened by June's 11 defaulted rows) · 4.1 (NOT dormant; live above `assembled ≈ 40`) ·
1.9 (de-ranked as pre-authorised).

**NEW:** 7.4 (two instruments, one word, different counters) · 8.1a (three unlisted consumers) ·
8.1b (a crisis channel that never leaves crisis mode) · 8.1c (ROOT 8 spends ROOT 1's budget) ·
8.5 (exercise the False branch).

**RE-RANKED: ROOT 8 takes the top slot; ROOT 1 drops to CLOSING.** Justification naming the
target: generation 5 pre-authorised exactly this ("ROOT 1 stays top only until its cert is read")
and the cert is read. ROOT 8 publishes a false NUMBER daily; ROOT 7 under-applies a true LABEL;
publishing a falsehood outranks omitting a caveat. **1.11 is the exception and stays URGENT
inside a closing root**, because its own numeric trigger fired.

**DECISION S86-1 — `228634c` IS CERTIFIED; ROOT 1.3 CLOSES.** Chosen over "partially certified"
and over revert. Why: run `33114821663` satisfies all five predictions exactly and the failure
test did not fire on either run, against a baseline banked before either was read. The
divergence on `33075059391` is explained by a single measured variable (`assembled` 43 vs 39)
and is the subject of 1.11, not a defect of `228634c`.

**DECISION S86-2 — the failure test was REFINED BEFORE any post-change run was read.** Raw
`arb_hits >= 14` now triggers an INVESTIGATION, not an automatic revert; revert requires a rise
sustained over three debates that output-volume growth cannot explain. Why: S81's own record
already ruled this confound once ("arb-level hits rose 28 → 32 → 52 **as the arbitrator came
back to life**… ~13/run, not a 2x worsening"), and `228634c` roughly doubles the arbitrator's
input. Timing is the safeguard — the refinement was written while zero post-change runs existed.

**DECISION S86-3 — 2.1's first clause is RULED without new instrumentation.** Trigger B does not
fire. Why: the per-run `GROUNDING SHADOW` line is already normalized per completed run, which is
the normalization 7.3 was blocking on; n=20 gives 8.3 against `>= ~12`; and the known scale
error (7.4) can only lower our figure, never raise it. Cost accepted: clause 2 is still
unmeasured, so 2.1 does not close.

**DECISION S86-4 (delegated, "your call") — PART D REMAINS A STATIC TEMPLATE.** Chosen over
shrinking the pasted prompt to four lines that delegate to the file. Why: shrinking converts
eight procedural steps from James's instruction into attachment content, and that change is
unmeasurable — the same certifiability logic that deferred round-robin at S85. The drift found
this session was NOT caused by the paste being long; it was caused by two agreed corrections
never reaching the file (a sweep failure, R-S82-4). **TRIGGER for the shrink option: a second
independent paste-vs-file divergence.** Consequence: PART D is instantiated from the file's
bytes at every open, never from a chat transcript (R-S86-4).

**DECISION S86-5 — NO CONTRACT v8.** Six rules earned; none changes a rule of engagement.
`git log -S` joins LINEAGE-BEV as a third evidence stage, which is close to law, but CONTRACT v7
already requires the `LINEAGE:` line to name evidence and does not enumerate sources. One earned
rule does not justify a version bump; RULES is its home. Also honours the law-vs-state test —
CONTRACT ran v1→v7 in six weeks.

**DECISION S86-6 — 6.2 (retention) is PROMOTED at generation 3, not closed.** Reason in writing:
it is gated by 6.4 (unread), and the thing it protects against — the 402 that took Lens fully
offline — has a live precedent in the sister project. Promoted means it must be worked or
re-justified next close, not carried a fourth time.

**DECISION S86-7 — 4.2 (retry window) is CLOSED AS ACCEPTED at generation 3.** Reason in
writing: the observed waits were traced to the inner `_call_agent` header-derived path, the runs
recover, and no live position fails. Accepting a known, benign discrepancy is a legitimate
outcome of the retire clause; carrying it a fourth time is not.

**TRAP DISPOSITION (promote or expire, no trap rides forward unchanged twice):**
- ARB-DRYRUN partial-line inflation — **EXPIRED AND RETIRED.** Its stated expiry was "when the
  cert shows `truncated=0`". Run `33114821663`: `truncated=0`, and pillar sum 15+15+9 = 39 =
  `arrived`, exact. On the `truncated=1` run the sum was 42 against `arrived=41` — the trap's
  described behaviour, one last time, on its way out.
- `_arb_asm` denominator (`fits=N/assembled`, never against `available`) — **KEPT**, expires
  when 1.7 lands. Second carry: **it must be promoted or expired at the S87 close.**
- MSYS/MINGW `grep` drops `--include` beside an unquoted variable of excludes — **KEPT**,
  expires when the cause is identified. Second carry: **promote or expire at the S87 close.**
- **NEW TRAP:** the MAD schedule moved ~9.5 hours on Aug 27 (03:3x/11:0x/11:4xZ → 13:0x/20:4x/
  21:0xZ) with no change of ours and no known cause. Never infer debate-vs-watch from the clock;
  use `ARB-FIT`. Expires when the cause is identified or the schedule holds 7 days.

**DOCS SHIPPED THIS CLOSE:** this order (generation 6) · HANDOFF_S86 · GNI_RULES + R-S86-1..6 ·
Protocol v6. **CONTRACT is UNCHANGED and stays at v7 — carry `CONTRACT_S85.md` forward.**

---

## HOW THIS FILE IS MAINTAINED
1. **FIND** — record every weak point with its evidence immediately, whatever the mission.
2. **CLASSIFY** — a silent live failure is urgent under any target. Everything else ranks by
   distance to the declared target, with a written justification naming it. Perishable evidence
   sets a DEADLINE, not a rank.
3. **ANALYSE** at close, not mid-session. The test: "does this change what I should do in the
   next hour?" The two rationalisations that are NOT triggers: "this is interesting" and "I'm
   already in the file."
4. **RE-ORDER** — regenerate, dated, superseding. Never appended.
5. **WORK THE TOP.**
