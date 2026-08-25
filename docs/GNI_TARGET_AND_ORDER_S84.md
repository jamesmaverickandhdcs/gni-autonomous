# GNI TARGET + WORKING ORDER
**SESSION-NUMBERED BY DESIGN (Protocol v4).** This file ships and lands as
`docs/GNI_TARGET_AND_ORDER_S{N}.md`. **THE LIVE ORDER IS THE HIGHEST SESSION NUMBER.**
Every close artifact carries its number; nothing is renamed on copy.
GENERATED: 2026-08-25 (S84 close) · SUPERSEDES: the S83-close generation · HEAD `5a20277`
GENERATION: 4

---

## NEXT SESSION'S MISSION (S85)
**ROOT 1 — HARVEST THE ARB-DRYRUN RUNS (n>=3) AND SHIP THE 1.3 FIX.**

The instrument shipped this session (`5a20277`) and fired correctly on its first run. It now
prints, every debate: the five-tier char split, per-pillar arrival, and what a build-and-measure
greedy fill WOULD select at depth 100/50/20/0. By S85 open there will be three or more runs.
Harvest them all — a gap is a gift, and S83 proved it twice.

Do NOT rule from run #363 alone. Its `TECH=0/6` may be an artifact of a GEO-dominant day.
What n>=3 must settle before the fix is designed:
1. Is a pillar zeroed on every run, or only on dominant-pillar days?
2. Is `assembled` stable near 36, or does it swing with `available` (232 on run #363)?
3. Does `depth=0` fit everything on a BUSY day, or only on a quiet one? Run #363 used
   4434 of 4854 chars at depth=0 — 420 spare. That margin is the whole design question.

Then ship the fix per DECISION S83-1 (per-article COST, depth DERIVED) **plus DECISION S84-1**
below: the cost is measured by building the line, never by an overhead constant.
Bank the behaviour distribution first (DECISION S83-2).

---

## TARGET (unchanged — no phase transition this close)

> ### TRUTHFULNESS OF OUTPUT
> Everything GNI publishes is either grounded in something an agent actually read, or is
> visibly labeled as speculation.

**DEFINITION OF DONE — status at this regeneration:**
1. **Arrival is asserted, not assumed.** — **PARTIAL, instrument now COMPLETE.** 1.4 shipped:
   all five tiers measured, per-pillar arrival counted (1.9 satisfied in the instrument).
   Still open: zero-inclusion WARNs rather than RAISEs, and the fix itself (1.3).
2. **Label coverage matches fabrication surface.** — OPEN, and now **worse than believed**.
   ROOT 7 shows the detector behind the label is calibrated against a basket no speaker read.
3. **GT5-T2 ruled with normalized evidence.** — OPEN, overdue since Jul 30. **Its pre-ruled
   default now rests on a falsified assumption** — see ROOT 7.
4. **Evidence base clean of fallback-era contamination.** — OPEN. ROOT 3.

The phase ends when the order has no urgent and no important items left. It does not end here.

---

## THE ORDER

Ranked against the declared target. **Freshness confers no priority.** Work the top. If you
believe the order is wrong, say so and propose a re-order — do not silently work something else.

### ROOT 1 — THE ARBITRATOR'S INTAKE IS A FIXED CEILING, NOT A SHARE · URGENT
*Now MEASURED end to end. S83 gave the flat line across 14 runs; S84 gave the composition.*
Run #363 (`32805461099`, 25 Aug 03:31Z), the first ARB-DRYRUN run, decomposed the whole
15,000-char arbitrator prompt for the first time:

| tier | chars | share |
|---|---|---|
| `ARB_FINAL` system prompt | ~4,170 (derived) | 27.8% |
| articles (`ctx_room`) | 4,854 | 32.4% |
| R2 + R3@110w + scaffold | 4,467 | 29.8% |
| `constraint_block` (NN-5) | 1,039 | 6.9% |
| `_arb_tail` | 430 | 2.9% |

The arbitrator reads almost as much of its own instructions, and almost as much agent talk, as
it reads of the world. `available=232 assembled=36 arrived=20`.

- **1.1** CLOSED (S82) — audit complete.
- **1.2** SHIPPED (S82) — `8f9b8c8`, ARB-ARRIVAL instrument.
- **1.3** **THE FIX. Open.** Per-article COST (DECISION S83-1), cost MEASURED not estimated
  (DECISION S84-1). The greedy sweep on run #363: depth=100 fits 20/36, depth=50 fits 26/36,
  depth=20 fits 31/36, depth=0 fits 36/36 using 4434 of 4854 chars. The trade is now explicit
  and numeric: **20 articles with 100-char summaries, or 36 headlines.**
  Constraint discovered S84: the per-pillar `[:15]` structure is a deliberate COVERAGE
  guarantee (S37 docstring), so a global score-ordered selection would destroy a designed
  property. The fix must preserve pillar structure while making the cut score-aware.
- **1.4** SHIPPED (S84) — `5a20277`, ARB-DRYRUN. Five tiers + per-pillar arrival + greedy
  simulation, print-only, zero API cost. Satisfies R-S82-2 and folds in 1.9.
- **1.5** CLOSED (S83) — premise proven false by bytes.
- **1.6** CONFIRMED 14/14 (S83) — `/debate` publishes `mad_round1_positions` while `R1=DROPPED`
  every run. The public page shows humans a transcript the verdict-bearer never read.
- **1.7** RE-SPECIFIED (S83) — the surviving overstatement is the four pillar headers, not
  `Total in pool`. **Confirmed live S84:** run #363's headers read `GEO -- 15`, `FIN -- 15`,
  `TECH -- 6` while TECH delivered ZERO articles. The arbitrator was told a tier existed and
  shown none of it.
- **1.8** Success is computed as a DENYLIST (`ctx-trim@0` -> SUCCESS). One grep for
  `not in (` success computations; an allowlist is the right shape.
- **1.9** SATISFIED IN THE INSTRUMENT (S84) — per-pillar arrival now printed. Remains open only
  as an assertion (nothing RAISES on a zeroed pillar).
- **1.10** **PROMOTED from 5.2 — the fallback grep.** Whether ANY GNI call site reads its
  declared fallback is ONE GREP, and GNI's three-account MAD topology assumes a redundancy it
  has never proven. Same bug class as the dead `arb_ctx` computation, which lives in this root.
  Below the line it was never worked in three generations; here it rides with the fix session.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · URGENT
*NEW ROOT this close. It is the target's own wording that it fails.*
`_grounding_basket = list(all_articles) + list(weak_articles)` (`mad_protocol.py:738`), and the
identical shape in `mad_runner.py:167`. Byte-verified: three consumers, one basket.

No speaker ever reads that union. Bull/bear/ostrich read `all_articles` at `[:15]` per pillar;
Swan reads the weak pool; the arbitrator read **20 of 232** on run #363. So a claim is scored
GROUNDED if its entity appears anywhere in a 232-article pool the speaker never saw. The
direction of error is FAIL-OPEN: E-2 withholds less than it should, E-3 labels less than it
should, and every stored `mad_grounding_hits` value was measured this way.

- **7.1** Establish the true scale of the gap per speaker: for one run, count basket size
  against what each speaker actually received. The arbitrator's ratio on run #363 is 20:232.
- **7.2** Decide the fix shape. Per-speaker baskets is the obvious answer and is NOT obviously
  right — a per-speaker basket makes the gate stricter, and **C stays rejected** under 2.1's
  standing law (fail-open is law, gates starve). The honest first move may be to LABEL the
  discrepancy rather than gate on it.
- **7.3** Re-read GT5-T2's July numbers (consultant 118 / arb 27) as a LOWER BOUND, since they
  were produced by this basket. This blocks 2.1 from being ruled on the old evidence.

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM · IMPORTANT
*RE-SPECIFIED this close. Was "consumed, not merely rate-limited" — accumulation only. S84
found the second face: **irreversibility**. The free tier gives you the resource and none of
the machinery you would expect around it: no meter, no retention, and no backup.*
6.1 is CLOSED, and it de-escalated this root from URGENT to IMPORTANT with numbers.

- **6.1** **CLOSED — MEASURED 25 Aug.** Supabase meter **113 MB / 500 MB**; `pg_database_size`
  93 MB; `pipeline_articles` **63.29 MB = 58.55%** of the database (heap 60 MB, index 3.2 MB,
  TOAST 24 kB — not an index runaway, not TOAST bloat). Growth ~569 rows/day recent, ~634
  kB/day all tables. **Runway 520-660 days.** The two 48/day workflows write ~31 rows/day
  combined = ~5% of growth: they are NOT the stock driver. Egress 446 MB / 5 GB (9%), file
  storage 0/1 GB, MAU 0/50,000 — **no second stock exists.** Org `jamesmaverickandhdcs` holds
  six projects, five paused, Lens among none of them: the "different org" claim is CONFIRMED,
  and paused projects do not consume the quota (113 MB total vs ~40-60 MB per project floor).
  Data window is 92 days, not 193: a `TRUNCATE` on 2026-05-24 ~02:50Z (the S35 data reset)
  explains both the `del=0` counters and the epoch.
- **6.5** **NEW — THERE IS NO BACKUP. Ranked on irreversibility, not on target-distance.**
  Project page reads `LAST BACKUP: No backups`. Free tier has no automated backup and no PITR.
  Three months of accumulated intelligence, 93 MB, sits with no copy — while the sister project
  is offline. This is off-target by the discovery policy's own test and is ranked here anyway
  because its failure is total and unrecoverable rather than degrading. **James may overrule
  this ranking; it is recorded as Claude's call under the retire/rank discipline.**
  Cheapest viable form: a scheduled `pg_dump` of the four tables that matter to a private
  repo or Drive, weekly. Design needs its own decisions (where, how often, which secret).
- **6.2** Retention policy, designed from 6.1's numbers. **No longer urgent — 520-660 days.**
  Now specifiable: `pipeline_runs` (943 rows, 272 kB) is the ONLY lever — `pipeline_articles`
  and `article_events` both CASCADE from it. But deleting runs leaves `reports` behind
  (`ON DELETE SET NULL`), so retention creates orphan reports, and a `reports`-anchored delete
  ERRORS on `mad_quality_log` (NO ACTION, no clause). **6.2 cannot be designed before 6.4.**
  Lineage: a 30-day cleanup was specified with numbers in the March 21 sprint briefing and
  assigned to Sprint 3. It was never built. This root is an unshipped prescription, not a new
  discovery — which is the worse disease.
- **6.3** SIZE METER in Mission Control. **Design changed by 6.1's measurement:** the two meters
  disagree by ~20 MB (93 vs 113) and **only the platform's number triggers the 402.** A meter
  built on `pg_database_size` would report "fine" while the platform refuses reads. See
  R-S84-2. Table-level figures agree exactly (63.29 MB both ways); the gap is in the total.
- **6.4** L5 exposure: what the public site shows when Supabase 402s. Still open, and now also
  gates 6.2.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** GT5-T2 decision, overdue since Jul 30. **BLOCKED by 7.3** — the pre-ruled default
  "A, hold" assumed the hit counts were measured against a sound basket. They were not.
  Trigger B iff hits >= ~12 per completed run OR LABELED fired in fewer than half the runs
  that had hits. **C stays rejected: fail-open is law, gates starve.**
- **2.2** Build B only if 2.1 triggers it.
- **2.3** Per-day cut of stored verdict rows across the S80 migration date (24 Jul,
  llama-3.3-70b -> gpt-oss-120b). Free, no provider call. S83's 14 runs gave first
  counter-evidence to the timidity thesis: 11 neutral but 3 bearish incl. 0.67 and 0.71.
- **2.4** **NEW — the public `/stocks` page may render market data frozen since first insert.**
  `stock_prices`: 32 live rows, 21,334 inserts, **zero updates ever**, and **zero rows with a
  `fetched_at` in the last 7 days**. `UNIQUE (ticker, range)` means every refresh conflicts and
  is discarded; nothing updates the existing row. The build output shows a `/stocks` route
  exists. If it reads this table, the site presents stale prices as current — the same shape as
  1.6, and on target. **One grep settles whether anything reads it.**

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** Pin the exact Jul 19-22 window from funnel-log engage/disengage lines, NOT memory
  (S79 says 19-21, S80 says 19-22 — the disagreement is the point).
- **3.2** `data_era` column + tagging, count-before == rows-updated, then exclude in
  GPVS/quality queries. James solo in the SQL editor. **Unblocked by 6.1** — the database is
  at 23% of quota with 520+ days of runway, so adding a column is safe.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.4** Measure chars/token PER POSITION (agent call vs arbitrator call), not once for the
  repo — Lens measured the same model at 3.80/4.19/4.156/4.738 on different prompts.
  `_call_agent` already holds both the char count and `usage.prompt_tokens` in one scope: one
  log line, zero API cost. `//3` over-estimates and is the SAFE direction: do NOT change to
  `//4`.
- **4.1** C2 solver recalibration: teach `compute_depth` the per-request ceiling; fix the stale
  "NOT WIRED" header (live since S51); rewrite the self-test table. **S84 sharpened the target:**
  the solver's own law is "N sacred, D the only lever", and the arbitrator's fit ladder violates
  it — `ctx-trim` is a raw char slice that kills N. Two mechanisms with contradictory laws on
  one prompt. Blocked on the real bill; partially unblocked by 4.4.
- **4.2** Nine 429s per run recover at 46.6-60.4s. W-02's coarse retry uses `base=60.0` and
  DOES clear the TPM window; the observed waits are the INNER `_call_agent` header-derived
  path. Read that site before any claim.
- **4.3** Quota-guard reference correction: Groq TPD refills CONTINUOUSLY at Limit/86400 per
  second; no reset boundary, no `-day` header. Any recovery estimate shaped as "wait until
  tomorrow" is unsound.

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.4** The register has THREE ID schemes and CONTRACT cites three IDs possibly absent from
  it. `GNI_RULES.md` carries `GNI-R-###`, `R-S##-#` and `LR-###` (18 LR lines). A `GNI-R-`
  grep returns SIX lines, yet CONTRACT v5 cites GNI-R-037, GNI-R-076 and GNI-R-233 as live law.
  One repo-wide grep decides whether CORE DISCIPLINE points at anything. *(Generation 2 of 3.)*
- **NEW, unnumbered, one line each:** delete `docs/STATUS.md` (fossil at S46) · the Protocol's
  "read Part C from the repo" is unachievable as written in this environment — Claude cannot
  read a private repo, so the attached copy is a second source with no byte check. A checksum
  step in Part D would close it. Logged, not shipped: see DECISION S84-4.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
- **PROBE-DRIFT: OVERDUE since Aug 24.** Monthly, needs James's explicit authorization each
  run, never on a near-red account.
- **KEYFILE ROTATION: OVERDUE since Aug 9 (16 days).** One account at a time, quiet window
  (~03:30-09:30 UTC). Receipts = `gh secret list` updatedAt before/after; never echo a key.
- **PHISH-HW: OVERDUE since ~Jul 31 (25 days).** OAuth + GitHub Apps review, security log from
  2026-07-18, report the trypatchhog.com mail. Browser, James solo, x3 accounts.
- **PROVIDER + PLATFORM EOL WATCH.** Record every announced end-of-life here at announcement,
  not at death. **Read the meter, not the mail.**
  - `gemini-2.5-flash` dies Oct 16.
  - **NEW (S84):** `actions/checkout@v4` and `actions/setup-python@v5` target Node 20, which
    is deprecated; GitHub is force-running them on Node 24. When that forcing stops,
    `gni_mad.yml` stops — a total outage caused by no change of ours. Pin newer action
    versions before then.
  - **NEW (S84):** Supabase free tier warns by EMAIL at 20% from a limit, then applies a grace
    period, then restricts — and grants no second grace period. GNI is at 23% of the database
    quota today.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.

### RETIRE CANDIDATES — GENERATION 1 OF 3 (the clause completed a full cycle at gen 3)
- **6.2 retention** — enters the count. Its urgency died with 6.1's measurement; if 520 days
  of runway keep it below the line for three generations, close it as accepted then.
- **4.2 retry-window** — enters the count. Narrowed twice, never read, harms nothing observed.
- **5.4 ID schemes** — generation 2 of 3.

---

## CHANGED THIS REGENERATION

**CLOSED:** 6.1 (MEASURED, all four questions answered with evidence) · 5.1 PUSH-GATE
(closed as accepted) · 5.2's CI half (closed as accepted) · 5.3 REFERENCE doc (closed as
accepted).

**SHIPPED:** 1.4 — ARB-DRYRUN, commit `5a20277`, 67 insertions / 0 deletions, certified live on
run #363 with self-consistent arithmetic (1039+4467+430+40 = 5976; 10830-5976 = 4854 = the
observed `ctx-trim@4854`).

**PROMOTED:** 5.2's fallback-grep half -> **1.10** (it is one grep, it is ROOT 1's bug class,
and below the line it went unworked for three generations).

**RE-SPECIFIED:** ROOT 6's title and character — from accumulation-only to "free-tier resources
come without the guarantees around them", with irreversibility (6.5) as the second face ·
6.2 (the CASCADE map makes `pipeline_runs` the only lever and makes 6.4 a hard gate) ·
6.3 (must read the PLATFORM meter, not `pg_database_size`) · 1.3 (the trade is now numeric, and
per-pillar coverage is a designed property the fix must preserve) · 1.9 (satisfied in the
instrument, open only as an assertion) · 4.1 (the solver's "N sacred" law vs the ladder's
char slice).

**NEW:** **ROOT 7** (grounding gate measures existence, not reading; three sub-items) ·
6.5 backup absent · 2.4 `/stocks` may publish frozen prices · 1.10 · two EOL-watch entries
(Node 20 forcing, Supabase grace-period mechanics) · two unnumbered ROOT 5 one-liners.

**RE-RANKED:** **ROOT 1 returns to the top; ROOT 6 drops from URGENT to IMPORTANT.**
Justification naming the target: 6.1 measured the runway at 520-660 days and found no second
stock, so ROOT 6's urgency was a hypothesis that measurement retired — which is exactly what a
measurement is for. ROOT 1 has a live instrument collecting evidence for a fix that is one
session away, and it is definition-of-done #1. **ROOT 7 enters as URGENT immediately below
ROOT 1**, because it fails the target's literal wording ("actually read") and because it
invalidates the evidence base for 2.1, but it needs its own audit before a fix is designable,
where ROOT 1's fix is nearly designed.

**DECISION S84-1:** the 1.3 fix measures per-article cost by **BUILDING THE LINE AND TAKING
`len()`**, never by an overhead constant. Why: the byte read gives cost as
`21 + len(src) + len(title[:80]) + len(str(score)) + len(summary[:depth])` — it varies per
article by roughly 114-130 chars with source and title length, so any formula with a fixed
overhead is wrong on every run. `_build_news_context` and `_assemble_arb` are PURE, so the
alternative is free. This is how ARB-DRYRUN already works and it satisfies R-S81-5 by
construction. Delegated by James ("your call" standing at option C).

**DECISION S84-2:** ARB-DRYRUN shipped as a **dry run, not a fix** — it logs what a greedy fill
WOULD select and applies nothing. Why: the same shape as DECISION S82-1 (print-only over
fix-now), which was scoped for two runs and harvested fourteen. Claude's three pre-registered
predictions for the first run were wrong or half-wrong (see WRONG ledger), which is the
argument for the dry run stated as evidence rather than as caution.

**DECISION S84-3:** no CONTRACT v6. Nothing this session changed a rule of engagement; the
earned lessons are rules and order items. The contract already indicts itself under its own
law-vs-state test (R-S82-5) at v1->v5 in six weeks.

**DECISION S84-4:** no Protocol v4 this close, despite a real gap found in v3. The gap: Part C
step 0 says "read Part C from the repo", and Claude cannot read a private repo — the file
reaches a session only as an attachment, which is a second copy with no byte check, i.e. the
dual-source-of-truth hole v3 was written to close, one level up. Why not fix it now: the fix is
a rule-of-engagement change found in the closing minutes and not yet ruled by James, and
shipping a protocol version on Claude's own initiative at close is the drift the law-vs-state
test exists to catch. Logged as a ROOT 5 one-liner for James to rule.

**DECISION S84-5:** 6.5 (backup) is ranked on IRREVERSIBILITY rather than target-distance,
which the discovery policy does not provide for. Recorded as a knowing exception with the cost
stated: it puts an off-target item above on-target ROOT 2 items. James may flip it.

**AMENDS R-S81-1** (no new number): zero-match indicts the pattern first — extended, because a
redirected failure is not silence. `gh run view --log > file 2>&1` writes the ERROR MESSAGE into
the file, so the corpus exists, is non-empty, and reads as valid text, while every `grep -c`
against it returns 0. S84 nearly read "ARB-DRYRUN fired 0 times" off a one-line file containing
a TLS timeout. `wc -l` BEFORE grep, always, on any cached artifact.

**AMENDS R-S67-2** (no new number): verify the instrument's RANGE — extended to its EPOCH. A
cumulative counter and the data it counts can have different start times.
`pg_stat_user_tables.stats_reset` read 2026-02-12 for every table in every schema (a
platform-side reset), while `pipeline_articles` data began 2026-05-24 after a TRUNCATE. Dividing
rows by the counter's window instead of the data's own span understated the growth rate by 2.1x
and overstated the runway by 40%.

**DOCS SHIPPED THIS CLOSE:** GNI_TARGET_AND_ORDER generation 4 · HANDOFF_S84 · R-S84-1..3 plus
two amendments appended. CONTRACT unchanged (v5 stands). Protocol unchanged (v3 stands).

**RETIRED:** none due — the clause completed a full cycle at generation 3. Three items enter
the new count above.

---

**DECISION S84-6 (post-close amendment, logged per CONTRACT v5's checkpoint rule):** EVERY
close artifact is session-numbered, in the repo as well as the download, and the live file is
the HIGHEST NUMBER. Ruled by James. Why: filename negotiation at close has burned tokens across
many sessions and buys nothing. Claude first argued for renaming fixed-path files on copy and
was WRONG - v3's rule exists to stop the opening prompt reading a stale literal path, but no
session reads the repo at all; it is private, the container is empty, and every file arrives as
an attachment. The failure also inverts in the safe direction: a missing numbered file is
visible, a silently-failed fixed-path copy is not, and S84 hit exactly that twice. Completeness
is now checked by re-reading the END of the previous session's record, where the close prints a
FILE MANIFEST. **Supersedes DECISION S84-4.** Shipped as CONTRACT v6 + Protocol v4.

**AMENDS THIS REGENERATION (checkpoint rule, not a silent edit):** the S84 close continued past
its own LOAD CHECK to ship the above. Three strays were removed from `docs/` and
`docs/HANDOFF_S83.md` was restored with `git checkout --`; the restored copy carries the
wrongness row "R-S81-3 is the wrong rule to amend -- I RETRACTED A CORRECT CLAIM", which the
working draft had silently dropped.
## HOW THIS FILE IS MAINTAINED
1. **FIND** — record every weak point with its evidence immediately, whatever the mission.
2. **CLASSIFY** — a silent live failure is urgent under any target. Everything else ranks by
   distance to the declared target, with a written justification naming it. Perishable
   evidence sets a DEADLINE, not a rank.
3. **ANALYSE** at close, not mid-session. The test: "does this change what I should do in the
   next hour?" The two rationalisations that are NOT triggers: "this is interesting" and
   "I'm already in the file."
4. **RE-ORDER** — regenerate, dated, superseding. Never appended.
5. **WORK THE TOP.**

*Mirrors the Lens discovery policy by reference, stated in GNI's own terms against GNI's own
evidence — never by paste. Dual sources of truth are how S2-D died. Logged on both sides.*
