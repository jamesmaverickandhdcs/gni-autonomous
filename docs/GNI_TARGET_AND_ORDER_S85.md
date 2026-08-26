# GNI TARGET + WORKING ORDER
**SESSION-NUMBERED BY DESIGN (Protocol v4+).** This file ships and lands as
`docs/GNI_TARGET_AND_ORDER_S{N}.md`. **THE LIVE ORDER IS THE HIGHEST SESSION NUMBER.**
GENERATED: 2026-08-26 (S85 close) · SUPERSEDES: the S84-close generation · HEAD `228634c`
GENERATION: 5

---

## NEXT SESSION'S MISSION (S86)
**CERTIFY `228634c` AGAINST ITS OWN PRE-REGISTERED PREDICTIONS, THEN OPEN ROOT 8.**

A behaviour change shipped to the verdict-bearing call and NOTHING has verified it. The commit
body names five predictions and one failure test; read the first debate after `228634c` and
score them one by one:

| prediction | refuted if |
|---|---|
| `ARB-FIT steps=drop-R1,R3@110w` (no `ctx-trim`) | `ctx-trim@` still present |
| `est` ~4927/5000 | over 5000, or a 413 appears |
| `ARB-ARRIVAL arrived == assembled` | any gap |
| `truncated=0 dropped=0` | either non-zero |
| `ARB-DRYRUN pillars GEO=15/15 FIN=15/15 TECH=N/N` | any pillar short |
| **FAILURE TEST: `GROUNDING SHADOW` arb_hits must NOT rise** | a rise = the depth call was WRONG |

Bank the arb_hits baseline from the S83 harvest and the four S85 runs BEFORE reading the new one
(DECISION S83-2). A cert on "the run went green" is not a cert (R-S83-4). If the failure test
fires, revert is one anchor — `depth=0` back to `depth=min(_depth, 100)`.

Then open **ROOT 8** with BIRD-EYE + **LINEAGE-BEV** (CONTRACT v7): read `escalation_scorer`
bytes and grep `docs/` for the D-11 lineage before proposing anything. It is architectural, so
it is SWOT-gated and its fix is NOT this session's business — the audit is.

---

## TARGET (unchanged — no phase transition this close)

> ### TRUTHFULNESS OF OUTPUT
> Everything GNI publishes is either grounded in something an agent actually read, or is
> visibly labeled as speculation.

**DEFINITION OF DONE — status at this regeneration:**
1. **Arrival is asserted, not assumed.** — **PARTIAL, fix SHIPPED, cert pending.** The
   arbitrator now receives the whole assembled basket (`228634c`). Still open: nothing RAISES
   on a zeroed pillar (1.9), and the cert has not been read.
2. **Label coverage matches fabrication surface.** — OPEN. ROOT 7 unchanged.
3. **GT5-T2 ruled with normalized evidence.** — OPEN, overdue since Jul 30, blocked by 7.3.
4. **Evidence base clean of fallback-era contamination.** — OPEN. ROOT 3.
5. *(implicit, and S85 made it explicit)* **The numbers GNI publishes mean what they appear to
   mean.** — OPEN, and this is now ROOT 8. A saturated scorer publishing CRITICAL 10.0 daily is
   the same disease as a page naming a dead model: an output that reports the instrument rather
   than the world.

---

## THE ORDER

Ranked against the declared target. **Freshness confers no priority.** Work the top. If you
believe the order is wrong, say so and propose a re-order — do not silently work something else.

### ROOT 1 — THE ARBITRATOR'S INTAKE · URGENT UNTIL CERTIFIED, THEN CLOSING
*S83 gave the flat line (n=14). S84 gave the composition. S85 gave the ruling and the fix.*

**The n=4 harvest (25–26 Aug, run ids `32805461099` / `32840260129` / `32927228664` /
`32961518194`), cross-verified through two independent instruments (CLI `gh run view --log` and
the browser log archives — identical to the digit):**

| run | available | assembled | arrived | GEO | FIN | TECH |
|---|---|---|---|---|---|---|
| 25 Aug 03:31Z | 232 | 36 | 20 | 15/15 | 6/15 | **0/6** |
| 25 Aug 11:02Z | 207 | 38 | 20 | 15/15 | 6/15 | **0/8** |
| 26 Aug 03:51Z | 234 | 37 | 20 | 15/15 | 6/15 | **0/7** |
| 26 Aug 11:18Z | 212 | 38 | 20 | 15/15 | 6/15 | **0/8** |

Four runs, four days, four different news days, and the arrival profile does not move by one
article. **The cut point is structural, not editorial.** The TECH pillar was zeroed EVERY run —
answering S84's open question, which had guessed it might be an artifact of a GEO-dominant day.
It is not. `by_pillar` order is (geo, fin, tech, other) and the ctx-trim slice cuts the tail, so
the last pillar dies whole, every time, unnamed to the model.

- **1.1** CLOSED (S82). **1.2** SHIPPED (S82) `8f9b8c8`. **1.4** SHIPPED (S84) `5a20277`.
  **1.5** CLOSED (S83). **1.10** CLOSED (S85 — see below).
- **1.3** **SHIPPED (S85) `228634c` — CERT PENDING.** `arb_ctx_fit` built at `depth=0`; the
  arbitrator now gets every assembled article as a headline anchor instead of 20 with 100-char
  summaries. Also fixed in the same commit: `ARB-FIT` printed `ctx_depth=min(_depth,100)`, a
  hardcoded echo that would have kept reporting 100 while the real value was 0.
  **Not closed until the cert is read.** Reverting is one anchor.
- **1.6** OPEN, CONFIRMED 14/14 (S83) + 4/4 (S85) — `/debate` publishes `mad_round1_positions`
  while `R1=DROPPED` on every run. The public page shows humans a transcript the verdict-bearer
  never read. **Unchanged by `228634c`** — R1 is still dropped by the ladder.
- **1.7** OPEN — the surviving overstatement is the four pillar headers (`[TECH -- 8 articles]`
  printed while zero arrived). `228634c` should make headers and content agree; **verify at
  cert**, then close if they do.
- **1.8** **RE-SPECIFIED (S85). The order's own description was wrong in both halves.** There is
  no `ctx-trim@0`-based denylist: `grep -rn 'not in ('` returns 7 code sites and NONE is a
  success computation. The real chain is `success = _update_report_with_mad(...)` (a DB-write
  result, `mad_runner.py:582`) AND `mad_succeeded = _compute_mad_succeeded(...)` (L275). The live
  defect is different and sharper: that function's docstring says it "closes the old leak where
  `bool(mad_bull_case)` flipped success True on an Arbitrator-only failure" — and
  `bool(mad_result.get('mad_bull_case', ''))` **is still the last clause of its OR chain.** The
  `mad_arb_failed` veto guards one door; the OR chain leaves the other open. One byte-read of
  L275-295 against the veto settles whether the leak is live.
- **1.9** OPEN as an assertion — per-pillar arrival is printed, nothing RAISES on a zeroed pillar.
  **Re-rank after cert:** if `228634c` makes zeroed pillars impossible in practice, this drops.
- **1.11** **NEW — round-robin pillar fill, DEFERRED WITH A TRIGGER (DECISION S85-3).** At
  `depth=0` the greedy fill takes 100% of assembled on all four harvested runs, so a fill-order
  change is a NO-OP today and could not be certified if shipped. But headroom is shrinking:
  spare chars ran 420 → 367 → 190 → **177** as `assembled` ran 36 → 37 → 38 → 38, i.e. ~124
  chars per article and roughly **1.4 articles of margin left**. **TRIGGER: ship 1.11 when
  `assembled >= 39` appears in any ARB-DRYRUN line, or when `ctx-trim@` returns to ARB-FIT.**
  At that point the loss resumes and pillar-ordered loss kills TECH again. Measure first: add a
  round-robin variant line to ARB-DRYRUN, print-only, before changing the fill.
- **1.12** **NEW — `GROQ_MODEL_FALLBACK` is a secret that never reaches the code.** 1.10's grep
  answered its own question (five call sites DO read a declared fallback: `llm_health_probe:97`,
  `main.py:96-99`, `self_healing_runner.py:61-64`, `nexus_analyzer:138`,
  `alpha_vantage`/`outcome_verifier`), then produced a worse finding.
  `grep -rni 'fallback' .github/` returns **0** — no workflow passes the secret, and `.env` does
  not set it. So `os.getenv('GROQ_MODEL_FALLBACK')` is `None` in CI and the code defaults apply:
  `nexus_analyzer.py:29` defaults to **`llama-3.1-8b-instant`**, a model this repo's own
  `MODEL_CLIFF_AUDIT_S60.md` lists as dying Aug 16. Its failover retries into a corpse.
  `mad_protocol.py:52`'s `llama-3.3-70b-versatile` is a THIRD-level default behind
  `GROQ_MAD_MODEL` and `GROQ_MODEL` (both passed by `gni_mad.yml:59-60`) and is therefore
  unreachable — dead text, not a live path. **Do NOT "fix" this by wiring the secret into the
  workflows: nobody has read its VALUE, and if the value is also a corpse, wiring it spreads one
  dead default to four call sites.** Fix the two code defaults, or read the value first.
  *Lineage: S68's swap-day plan specified a 6-file default sweep; `497df4a` + `e526bf6` paid four
  of six. Not a new discovery — an unfinished one.*

### ROOT 8 — GNI PUBLISHES A SATURATED INSTRUMENT AS A MEASUREMENT OF THE WORLD · URGENT
*NEW ROOT this close, promoted out of `docs/DEBT_REGISTER_S69.md` where it has sat since S74.*

**D-11, born 2026-07-17, never worked: 109 of 110 scored reports read escalation 10.0.** The
lone 5.0 is the PHI-003 gate's single firing in 17 calm-sentiment opportunities. Saturation is
three-layer: base caps sum to 5+5+4=14 against a cap of 10; the diversity bonus is guaranteed by
the S39 14/4/4 quota; and `CRITICAL_COMBOS` fire near-daily (hormuz+iran = +3), which also mutes
the gate's own `combo_bonus < 3` condition. `score_breakdown` is not persisted to `reports`, so
the combo theory is unverifiable by SQL — any fix must add persistence first.

**Why this is URGENT and why it ranks ABOVE ROOT 7:** the number is published. It reaches the
public site, Telegram CRITICAL alerts, `escalation_level`, `historical_correlations.avg_
escalation_score`, and it drives the frequency controller that decides how often the organism
runs. S79's handoff recorded "Escalation pinned 10/10 CRITICAL (US-Iran) since Jul 18" as a fact
about the world; D-11 says it is a fact about the scorer. Publishing a false number outranks
failing to add a true caveat, which is ROOT 7's shape. **James may flip this ranking.**

- **8.1** Audit `escalation_scorer` by bytes: the three saturation layers, the cap, the combos
  table, and whether `score_breakdown` exists anywhere. LINEAGE-BEV first — D-11 names a June
  "Option B" design that was never executed, and that design must be read before a new one.
- **8.2** Add `score_breakdown` persistence to `reports`. Nothing about this root is provable
  without it, and it is the smallest possible first commit.
- **8.3** SWOT the recalibration. Architectural, keyword-deterministic (not model-coupled), so
  it is safe to do now that the cliff has passed — the register's own stated precondition.
- **8.4** Decide what the PUBLIC surface says in the meantime. A saturated 10.0 shown without a
  caveat is the target's literal failure; a label is cheaper than a recalibration and can ship
  first.

### ROOT 7 — THE GROUNDING GATE MEASURES "EXISTS IN THE POOL", NOT "WAS READ" · URGENT
**Re-verified BY BYTES this session** (`mad_protocol.py:738`):
`_grounding_basket = list(all_articles or []) + list(weak_articles or [])`. Three consumers, one
basket, no speaker reads the union.

**`228634c` changed this root's arithmetic and did NOT close it.** The arbitrator's ratio was
20:232; it is now `assembled`:`available`, roughly 38:212 — better by ~2x, still ~18%. The gate
still scores a claim GROUNDED because its entity appears in a pool the speaker never saw.
*This also cleared the S83 ship gate: because the basket is the FULL union rather than the arb's
trimmed slice, cutting arb depth could not weaken the automated gate. Verified by bytes, not by
the handoff's claim about them.*

- **7.1** Establish the true gap per speaker: basket size vs what each speaker actually received,
  for one run. Recompute the arbitrator's ratio post-`228634c`.
- **7.2** Decide the fix shape. Per-speaker baskets make the gate STRICTER and **C stays
  rejected** under 2.1's standing law (fail-open is law, gates starve). Labelling the discrepancy
  may be the honest first move.
- **7.3** Re-read GT5-T2's July numbers (consultant 118 / arb 27) as a LOWER BOUND. Blocks 2.1.

### ROOT 9 — PUBLIC COPY DRIFTS FROM CONFIGURATION, AND NOBODY OWNS THE DRIFT · IMPORTANT
*NEW ROOT this close. Two commits shipped against it; the root is not the two lines.*

The pattern, proven three times in one session: a page is written TRUE, something changes
elsewhere, and the sweep never reaches the page. `/methodology` was made honest at S77 on Jul 21
and named `llama-3.3-70b-versatile`, which was correct that day; the model swap landed Jul 23-24
and touched code, secrets and workflows but not the copy. Five weeks later the public site was
still telling readers GNI runs on a model that died Aug 16.

- **9.1** SHIPPED (S85) `2afec7b` — `/methodology` Stage 4a + tech stack now cite the
  `GROQ_MODEL` secret instead of a model name. Model names are CONFIG, not methodology: removed
  rather than updated, per S77's count-free-prose precedent.
- **9.2** SHIPPED (S85) `bb9e299` — `/about` infra table drops `(Llama 3)`. **This closed the
  unpaid half of S69 census flag F5**, which named TWO sites and was folded into CLIFF scope;
  CLIFF was DECLARED ACHIEVED at S81 with F5's second site still live. See R-S85-4.
- **9.3** **OPEN — "4 pipelines / 4 workflows" is wrong in SIX places and the fix needs JAMES.**
  Sites: `methodology:25`, `methodology:115`, `research:105`, `devops:74`, `devops:124`,
  `about:174`. `gh workflow list --all` returns **8, all active** (adaptive, graph, heartbeat,
  mad, market, pipeline, selfbias, mission-control). The count is wrong; but whether
  `gni_graph` / `gni_market` / `gni_selfbias` / `gni_selfcheck` are "autonomous pipelines" or
  "supporting workflows" is a VOCABULARY ruling, not an arithmetic one, and Claude picking a
  number would violate R-S81-5. `devops:40` also holds a real `const pipelines = [` array — the
  heading and the array must move together or the page contradicts itself.
- **9.4** **OPEN — `src/app/api/stock-context/route.ts:81` defaults to a dead model**
  (`process.env.GROQ_MODEL || 'llama-3.3-70b-versatile'`). Code, not copy; different blast
  radius; unknown whether Vercel sets `GROQ_MODEL`. Pairs with 2.4.
- **9.5** **OPEN — the S69 subpage census has EIGHT unresolved flags and its RE-CERT never ran.**
  `docs/SUBPAGE_IC_CENSUS.md` + `docs/SUBPAGE_CERTIFICATION.md`: F2, F3, F8, F9, F12, F13, F14,
  F15 carry no closure, and S79's parked list (F3 legend, WORD-CONV, PHASE-NARR, WEIGHT-PRIOR,
  RE-CERT screenshot pass) was never worked. **F14 is on-target and ugly:** `/comparison` renders
  an AGREE banner reading "Both signals point BEARISH" while the MAD verdict is NEUTRAL, because
  the AGREE logic treats NEUTRAL as agreement. That is the site asserting a false fact to a
  reader. *S82's framing called this arc CLOSED; it was not (W-85-8).*
- **9.6** **PROMOTED from 5.4 at generation 3 of 3, with a written reason.** The register carries
  three ID schemes (`GNI-R-###`, `R-S##-#`, `LR-###`) and CONTRACT cites GNI-R-037 / 076 / 233 as
  live law while only six `GNI-R-` lines exist. **Reason for promotion rather than closure:**
  CONTRACT v7's LINEAGE-BEV gate now RUNS ON `docs/` greps, so an incoherent register is no
  longer cosmetic — it is a dependency of the gate that protects every proposal. (Note: the
  pre-commit hook prints a `GNI-R-233 SELF-AWARENESS CHECK` banner on every commit, so at least
  one of the three cited IDs is live in tooling; one grep settles the other two.)

### ROOT 6 — FREE-TIER RESOURCES COME WITHOUT THE GUARANTEES AROUND THEM · IMPORTANT
- **6.1** CLOSED (S84, measured). 113/500 MB platform meter; `pipeline_articles` 58.55%; runway
  520-660 days; no second stock; `TRUNCATE` 2026-05-24 explains the epoch.
- **6.5** **THERE IS NO BACKUP.** `LAST BACKUP: No backups`; free tier has no automated backup
  and no PITR. Three months of intelligence, 93 MB, no copy. Ranked on irreversibility rather
  than target-distance — a knowing exception (DECISION S84-5), James may overrule. Cheapest
  viable form: scheduled `pg_dump` of the four tables that matter, weekly, to a private repo.
- **6.2** Retention policy. `pipeline_runs` is the ONLY lever (articles + events CASCADE from
  it); deleting runs orphans `reports` (`SET NULL`), and a `reports`-anchored delete ERRORS on
  `mad_quality_log` (NO ACTION). **Cannot be designed before 6.4.** *(Retire count: gen 2 of 3.)*
- **6.3** SIZE METER in Mission Control — must read the PLATFORM meter (113) not
  `pg_database_size` (93); only the platform number triggers the 402 (R-S84-2).
- **6.4** L5 exposure: what the public site shows when Supabase 402s. Gates 6.2.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** GT5-T2 decision, overdue since Jul 30. **BLOCKED by 7.3.** Trigger B iff hits >= ~12
  per completed run OR LABELED fired in fewer than half the runs that had hits. **C stays
  rejected: fail-open is law, gates starve.**
- **2.2** Build B only if 2.1 triggers it.
- **2.3** Per-day cut of stored verdict rows across the S80 migration date (24 Jul). Free, no
  provider call. **S85 adds four fresh data points** to the timidity question — read them with
  the S83 eleven when 2.3 runs.
- **2.4** `/stocks` may render prices frozen since first insert: 32 live rows, 21,334 inserts,
  **zero updates ever**, zero rows with `fetched_at` inside 7 days; `UNIQUE (ticker, range)` means
  every refresh conflicts and is discarded. One grep settles whether anything reads the table.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** Pin the exact Jul 19-22 window from funnel-log engage/disengage lines, not memory
  (S79 says 19-21, S80 says 19-22 — the disagreement is the point).
- **3.2** `data_era` column + tagging, count-before == rows-updated, then exclude in GPVS/quality
  queries. James solo in SQL. Unblocked by 6.1.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.4** Measure chars/token PER POSITION, not once for the repo. `_call_agent` holds both the
  char count and `usage.prompt_tokens` in one scope: one log line, zero API cost. `//3`
  over-estimates and is the SAFE direction — do NOT change to `//4`.
- **4.1** C2 solver recalibration: per-request ceiling, stale "NOT WIRED" header, self-test table.
  The solver's law is "N sacred, D the only lever" while the fit ladder's `ctx-trim` kills N —
  two mechanisms with contradictory laws on one prompt. **`228634c` may have changed this
  materially:** if `ctx-trim` no longer fires, the contradiction is dormant. Check at cert.
- **4.2** Nine 429s/run recovering at 46.6-60.4s; the observed waits are the INNER `_call_agent`
  header-derived path, not W-02's `base=60.0`. Read the site before any claim. *(Gen 2 of 3.)*
- **4.3** Groq TPD refills CONTINUOUSLY at Limit/86400 per second; no reset boundary, no `-day`
  header. Any "wait until tomorrow" recovery estimate is unsound.
- **4.5** **STILL UNREAD SINCE JUL 27 — C1's real token bill.** The `groq_quota` line is a
  TELEGRAM artifact, not a workflow log. Predicted 60-75K vs July's 91-93%. Blocks 4.1.

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.5** **NEW — `docs/DEBT_REGISTER_S69.md` has no reader.** 131 lines, D-1..D-11, V-1..V-3, a
  13-row James-deferral ledger, S70 and S74 appends, then silence since 2026-07-17. No handoff,
  order or contract cites it. S85 found it by accident. Decide its fate: either it gets a read
  step in Part D, or its live rows migrate into this order and the file is archived. **Do not
  leave it as-is — that is the third instrument this project has built and stopped reading.**
  Live rows worth migrating: **J-1** (W-10 TPM re-ruling, overdue since Jun 12) · **J-5**
  (a dated deferral resting on a possibly-UNTRACKED probe file) · **J-6** (raw-429 SQL cleanup,
  status unknown) · **D-5** (Fox News in `source_weights`, flagged twice, closed zero times) ·
  **D-10** (staging checker, unknown since Mar 23).
- **NEW, unnumbered:** delete `docs/STATUS.md` (fossil at S46).

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
- **PROBE-DRIFT: OVERDUE since Aug 24.** Monthly, needs James's explicit authorization each run,
  never on a near-red account.
- **KEYFILE ROTATION: OVERDUE since Aug 9 (17 days).** One account at a time, quiet window
  (~03:30-09:30 UTC). Receipts = `gh secret list` updatedAt before/after; never echo a key.
- **PHISH-HW: OVERDUE since ~Jul 31 (26 days).** OAuth + GitHub Apps review, security log from
  2026-07-18, report the trypatchhog.com mail. Browser, James solo, x3 accounts.
- **PROVIDER + PLATFORM EOL WATCH.** Record every announced EOL here at announcement, not at
  death. **Read the meter, not the mail.**
  - `gemini-2.5-flash` dies Oct 16.
  - `actions/checkout@v4` + `actions/setup-python@v5` target Node 20 (deprecated); GitHub is
    force-running them on Node 24. When forcing stops, `gni_mad.yml` stops — a total outage
    caused by no change of ours. Pin newer action versions before then.
  - Supabase free tier warns by EMAIL at 20% from a limit, then a grace period, then restricts,
    with no second grace period. GNI is at 23% of the database quota.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.

### RETIRE CANDIDATES — the clause, honestly counted
- **6.2 retention** — generation 2 of 3.
- **4.2 retry-window** — generation 2 of 3.
- **5.4 ID schemes** — reached generation 3 and was **PROMOTED to 9.6 with a written reason**
  (LINEAGE-BEV now depends on `docs/` greps). Not dropped silently, not closed as accepted.

---

## CHANGED THIS REGENERATION

**MISSION: COMPLETED.** S85's declared mission was "harvest ARB-DRYRUN n>=3, then ship the 1.3
fix". n=4 harvested and cross-verified through two instruments; fix shipped as `228634c`.

**SHIPPED:** 1.3 — `228634c` (arb depth=0 + the `ctx_depth` echo fix), 2 insertions / 2
deletions, COMPILE OK, anchors 1/1 · 9.1 — `2afec7b` · 9.2 — `bb9e299`.

**CLOSED:** 1.10 (the fallback grep — answered, and it spawned 1.12) · S69 census flag F5 (both
sites, five weeks after the arc that owned it was declared achieved).

**RE-SPECIFIED:** 1.8 (there is no `ctx-trim@0` denylist; the live defect is `bool(mad_bull_case)`
still sitting in `_compute_mad_succeeded`'s OR chain, in a function whose docstring says that leak
was closed) · 1.9 (re-rank after cert) · 7.x (the ratio changed, the root did not) · 4.1 (may be
dormant if `ctx-trim` stops firing).

**NEW:** **ROOT 8** (escalation saturation — promoted out of a register nobody reads) ·
**ROOT 9** (public copy drift, six items) · 1.11 round-robin with a numeric trigger ·
1.12 the unwired fallback secret · 4.5 C1's unread bill, broken out because it blocks 4.1 ·
5.5 the unread debt register.

**RE-RANKED:** **ROOT 8 enters directly below ROOT 1 and above ROOT 7.** Justification naming
the target: ROOT 8 is a false NUMBER already on the public site, in Telegram alerts and in the
frequency controller; ROOT 7 is a true LABEL that is under-applied. Publishing a falsehood
outranks omitting a caveat. ROOT 1 stays top only until its cert is read — after that it drops.
ROOT 9 enters as IMPORTANT rather than URGENT because its two live falsehoods were fixed this
session and the remainder is either a vocabulary ruling (9.3) or unaudited (9.5).

**DECISION S85-1 — the 1.3 fix is `depth=0`, not a fill-order change.** Chosen over round-robin
(1.11) and over per-pillar allotments. Why: DECISION S83-1 had already ruled the direction as
per-article COST and reasoned that ordering/allotment fixes cannot raise coverage while the share
is stable — the n=4 harvest confirms the share is stable to the article. The value was DERIVED,
not picked (R-S81-5): the greedy sweep fits 36/36, 37/37, 38/38, 38/38 at `depth=0`, never fits
at 100 or 50, and cleared depth=20 by **2 chars** once. Lineage carried the weight: the S27
founding design grounded each debate in ALL articles, the 20-article ceiling is drift from S37's
`[:15]` budget cap, and the fabrication class (specimens 1/2/5) is insertion of entities ABSENT
from the basket — detected by breadth, not by 100-char summaries. C1 already runs R2/R3 at
`depth=0`; the arb tier was the last one left.

**DECISION S85-2 — CONTRACT v7: LINEAGE-BEV enters the GATE SEQUENCE.** Ruled by James. Every
lettered proposal carries a `LINEAGE:` line naming the grep or file read. Rationale in full at
R-S85-1 and in the contract itself; the short form is that Claude's lean steers James's ruling,
so an unresearched lean launders itself into an operator decision.

**DECISION S85-3 — round-robin is NOT shipped, and the reason is certifiability.** At `depth=0`
it is a no-op on all four harvested runs, so shipping it would put unverifiable code in the
verdict path. Deferred to 1.11 with a NUMERIC trigger (`assembled >= 39`, or `ctx-trim@` returns)
rather than a vague "later" — the failure mode this project keeps hitting is the deferral with no
instrument (R-S69-2, D-11, F5).

**DECISION S85-4 — two public-copy commits shipped mid-session, off-mission, knowingly.**
Justified under the same-session fix bar clause (a): a live public falsehood is urgent under any
target. Recorded as an exception with its cost stated — it spent ~40% of a session whose mission
was ROOT 1. The mission still completed, so the cost was affordable; that does not make it free.

**DECISION S85-5 — Claude does NOT pick the pipeline count (9.3).** "4 pipelines" is wrong
(8 active) but the right number depends on whether four supporting workflows count as pipelines.
That is James's vocabulary, and R-S81-5 forbids Claude hand-deriving a value it can only guess.

**TRAP DISPOSITION (promote or expire, no trap rides forward unchanged twice):**
- `gh run view --log` TLS failure — **EXPIRED AND RETIRED.** 5/5 exit 0 across five runs this
  session, and the browser-zip cross-check matched the CLI output to the digit.
- ARB-DRYRUN partial-line inflation — **KEPT with a sharper expiry:** expires when the cert shows
  `truncated=0`, because `228634c` should remove mid-line cuts entirely.
- `_arb_asm` denominator (`fits=N/assembled`, never against `available`) — **KEPT**, expires when
  1.7 lands.
- **NEW TRAP:** MSYS/MINGW `grep` silently IGNORES `--include` when the command also expands an
  unquoted variable of `--exclude-dir` flags. Proven: a `--include='*.py'` run returned `.md` and
  `.ts` paths, and the 4-include and 1-include variants produced byte-identical output. A
  standalone `--include` works. Expires when the cause is identified. Until then: pass explicit
  PATHS, not `--include`, on any census that matters.

**DOCS SHIPPED THIS CLOSE:** this order (generation 5) · HANDOFF_S85 · CONTRACT v7 ·
Protocol v5 · GNI_RULES + R-S85-1..6.

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

*Mirrors the Lens discovery policy by reference, stated in GNI's own terms against GNI's own
evidence — never by paste. Dual sources of truth are how S2-D died. Logged on both sides.*
