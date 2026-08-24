# GNI TARGET + WORKING ORDER
**FIXED PATH — `docs/GNI_TARGET_AND_ORDER.md`. Always this path. Archived orders get descriptive
names; only the live one keeps the path, so no session ever hunts for the current version.
NEVER put a session number in this filename (Protocol v3 Part A).**

GENERATED: 2026-08-24 (S83 close) · SUPERSEDES: the S82-close generation · HEAD `a1011a9`
GENERATION: 3

---

## NEXT SESSION'S MISSION (S84)
**ROOT 6.1 — MEASURE GNI's SUPABASE STOCK. Then ROOT 1.4+1.3-fix together.**

6.1 first, and it is minutes of work, because it is the only item whose failure mode is a
PUBLIC one: L5 serves a public Vercel site from Supabase, so a Fair-Use 402 breaks a website,
not merely an unattended pipeline — and a cached page keeps serving while the data behind it
is dead. Project Lens went fully offline on 23 Aug 2026 from exactly this cause and cannot
recover until 11 Sep. GNI is in a DIFFERENT Supabase org and is alive (verified 24 Aug), but
`grep -rn "\.delete()"` across every `.py` in GNI_Autonomous returns **ZERO** — there is no
retention code at all. Three free questions: total DB size and the per-table split; whether
`gni_heartbeat` and `gni_selfcheck` (48 runs/day EACH) write rows; and the runway in DAYS.
**Measure only. Do NOT copy Lens's fix — its shrink worked on the shape of ITS table.**

Then ROOT 1.4 + the 1.3 fix, shipped together per DECISION S83-1, gated on reading
`check_grounding` first (below).

---

## TARGET (unchanged — no phase transition this close)

> ### TRUTHFULNESS OF OUTPUT
> Everything GNI publishes is either grounded in something an agent actually read, or is
> visibly labeled as speculation.

**DEFINITION OF DONE — status at this regeneration:**
1. **Arrival is asserted, not assumed.** — **PARTIAL, and now MEASURED.** The instrument ran
   14 debates (18-24 Aug). Zero-inclusion never fired. Still open: zero-inclusion WARNs
   rather than RAISEs, four sibling tiers unmeasured (1.4), and arrival is not counted by
   DISTINCT pillar (1.9).
2. **Label coverage matches fabrication surface.** — OPEN. E-3 labels `blind_spot_explanation`
   only; `short_focus_threats` and `action_recommendation` reach Telegram unlabeled. ROOT 2.
3. **GT5-T2 ruled with normalized evidence.** — OPEN, overdue since Jul 30. ROOT 2.1.
4. **Evidence base clean of fallback-era contamination.** — OPEN. ROOT 3.

The phase ends when the order has no urgent and no important items left. It does not end here.

---

## THE ORDER

Ranked against the declared target. **Freshness confers no priority.** Work the top. If you
believe the order is wrong, say so and propose a re-order — do not silently work something else.

### ROOT 6 — FREE-TIER RESOURCES ARE CONSUMED, NOT MERELY RATE-LIMITED · URGENT
*NEW ROOT this close. Mirrored from Lens's proposed R9, stated in GNI's own terms.*
Every quota discipline GNI owns governs a **FLOW** — `quota_guard.py` reserves tokens per
account-day, the rate governor paces per minute. Storage is a **STOCK**: it only grows, nothing
meters it, and the failure is not a slow degradation but a hard 402 on every read at once.
- **6.1** **S84 MISSION.** Measure: `pg_database_size`, the per-table split (size, row count,
  and the index/TOAST split reported SEPARATELY — a lumped figure cannot tell a runaway index
  from TOAST bloat), whether the two 48/day workflows write rows, and the runway in days.
  James solo in the Supabase SQL editor. Measurement only, no deletion, no schema change.
- **6.2** Retention policy, designed from 6.1's numbers — not from Lens's. GNI_Autonomous has
  none; the 365-day cleanup James remembered is real but lives in the **GNI_Myanmar** repo,
  a different codebase frozen at `9d1a6e5` for diploma evidence, so it protects nothing here.
- **6.3** A SIZE METER in Mission Control. GNI's advantage over Lens: a health job already runs
  every 30 minutes and already reports. One DB-size line makes the stock visible. Lens broke
  its own "read the provider mail" rule twice (Cerebras EOL, Supabase 20% warning) before
  concluding the rule was wrong — **read the METER, not the mail.**
- **6.4** L5 exposure: establish what the public site shows when Supabase 402s. A cached page
  serving stale intelligence while the database is dead is a truthfulness-of-output failure,
  which puts this sub-item ON target rather than merely operational.

### ROOT 1 — THE ARBITRATOR'S INTAKE IS A FIXED CEILING, NOT A SHARE · URGENT
*Character changed AGAIN this close. S82: "a confirmed mechanism, unmeasured firing."
S83: MEASURED across 14 debates — and it is not the s1=0 catastrophe.*
`arrived` sat at **19-21 (mean 20.2) on all 14 runs** while `available` swung 132→237 (1.8x)
and `assembled` 31→38. Coverage therefore FALLS as news volume rises: 14.4% on the quietest
day, **8.4% on the busiest**. The full fit ladder fired 14/14; `truncated=1` 14/14; zero-
inclusion WARNING never fired. ~230-250 chars/article at `depth=100` against ~5,000 surviving
chars = ~20 articles, always.
- **1.1** ✅ CLOSED (S82) — audit complete.
- **1.2** ✅ SHIPPED (S82) — `8f9b8c8`, ARB-ARRIVAL instrument.
- **1.3** ✅ **RULED THIS SESSION.** Not starved to zero; the defect is a fixed-ceiling intake
  decoupled from volume and from cross-pillar significance. **Fix is per-article COST, not
  allotments** — see DECISION S83-1. Remains open as the FIX, not as the question.
- **1.4** Widen the instrument to ALL FIVE tiers (`constraint_block`, R1, R2, R3, `_arb_tail`).
  Ship WITH the 1.3 fix so the cert can attribute which tier gained (R-S82-2).
- **1.5** ✅ **CLOSED — the premise was false.** `_arb_trunc` does NOT always read 0: the
  instrument re-derives the slice (`arb_ctx_fit[:_keep]`) rather than reading the assembled
  prompt, so `'\n[ctx trimmed to fit]\n'` is never in the string the `endswith` test sees.
  `dropped=N` is EXACT, and conservative-HIGH by one (a partially delivered article counts as
  fully dropped). The S82 trap said "at least N" and would have inverted the 1.3 ruling.
- **1.6** ⬆️ **UPGRADED — 14/14 CONFIRMED, no longer a suspicion.** `R1=DROPPED` on every run
  while `/debate` publishes `mad_round1_positions`. The public page has shown humans a
  transcript the verdict-bearer never read, every run for a week. Squarely on target.
- **1.7** ✏️ **RE-SPECIFIED — the order named the wrong line.** `Total in pool: {total}` is
  appended at the very END of `articles_ctx`, so on any ctx-trim run it is sliced off and
  never reaches the arbitrator. What DOES reach it is
  `f'\n[{pillar.upper()} -- {len(arts)} articles]\n'` — each pillar header states the FULL
  pillar count while only 15 are rendered, and those headers sit at the START of each block so
  they survive every trim. 1.7 also fires at full strength for the four AGENTS (untrimmed).
- **1.8** **NEW — success is computed as a DENYLIST.** GNI's own specimen: `ctx-trim@0` gives
  the arbitrator zero articles and the run still reports SUCCESS. Lens's orchestrator used
  `ok = status not in (...)` and printed ✅ over nine distinct failure statuses, which is how
  Lens produced ZERO intelligence for a full day with green runs. A denylist can only ever be
  a list of the failures somebody remembered. One grep across GNI for `not in (` success
  computations; an allowlist is the right shape.
- **1.9** **NEW — arrival is counted in ROWS, not in DISTINCT PILLARS.** `arrived=20` counts
  lines starting `'  - ['`. Twenty could be 15 geo + 5 fin, i.e. one pillar dominating while
  the number looks healthy. Lens's `s1=4/4` was satisfied by four copies of ONE lens. Amends
  R-S81-3. Fold into 1.4's instrument widening — per-pillar arrival counts, not a total.
- **NOTE (R-S82-3):** C1 transcript-carry certified PASS and did NOT close this root.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
- **2.1** GT5-T2 decision, overdue since Jul 30. Normalize hits per COMPLETED run before
  ruling. Pre-ruled default: **A, hold**. Trigger **B** iff hits >= ~12 per completed run OR
  LABELED fired in fewer than half the runs that had hits. **C stays rejected: fail-open is
  law, gates starve.**
- **2.2** Build B only if 2.1 triggers it.
- **2.3** ⬆️ **PROMOTED and RE-SPECIFIED — this is no longer a musing, it is a measurement.**
  Was: "five verdicts all 0.48-0.53 — is gpt-oss hedging where 3.3-70b committed?" S83's 14
  runs give the first counter-evidence: 11 neutral (0.48-0.53) but **3 bearish including 0.67
  and 0.71**, which break the band. Lens proved the METHOD on two positions: a per-day cut of
  stored rows across the migration date settles it, free, no provider call. **Do the same cut
  across GNI's S80 migration date (24 Jul, llama-3.3-70b → gpt-oss-120b) on stored verdict
  rows.** The S80 cert measured mechanics only — zero 413, zero empties, verdict arrives —
  and never asked whether the instrument's BEHAVIOUR changed. Blocks nothing; unblocks 2.1.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
- **3.1** Pin the exact Jul 19-22 window from funnel-log engage/disengage lines, NOT memory
  (S79 says 19-21, S80 says 19-22 — the disagreement is the point).
- **3.2** `data_era` column + tagging, count-before == rows-updated, then exclude in
  GPVS/quality queries. James solo in the Supabase SQL editor. **Sequence after 6.1** — do not
  add a column to a database whose size is unmeasured.

### ROOT 4 — COST AND HEADROOM · IMPORTANT
- **4.4** ✏️ **RE-SPECIFIED — there is no single "GNI divisor" to measure.** Lens measured the
  SAME provider and model at 3.80, 4.19, 4.156 and 4.738 chars/token on different prompts:
  the ratio is CONTENT-dependent, not a model constant. So measure PER POSITION (agent call vs
  arbitrator call), not once for the repo. `_call_agent` already holds both the prompt char
  count and `usage.prompt_tokens` in the same scope — one log line, zero API cost. `//3`
  over-estimates and is the SAFE direction: **do not change it to `//4`.**
- **4.1** C2 solver recalibration: teach `compute_depth` the per-request ceiling so R1 escapes
  the 768 band; fix the stale "NOT WIRED — do not import" header (imported and live since
  S51); rewrite the self-test table. **Blocked on the real bill — partially unblocked by 4.4.**
- **4.2** Nine 429s per run recover at 46.6-60.4s. S82 narrowed it: W-02's coarse retry uses
  `base=60.0` and DOES clear the TPM window; the observed waits are the INNER `_call_agent`
  header-derived path, which does not. Read that site before any claim.
- **4.3** Quota-guard reference correction: Groq TPD refills CONTINUOUSLY at Limit/86400 per
  second; there is no reset boundary and no `-day` header. GNI reserves per-account-DAY. The
  split may be sound; what is unsound is any recovery estimate shaped as "wait until tomorrow."

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE
- **5.1** PUSH-GATE: Actions test-gate blocking red pushes (the 61adb50 lesson). Soft mode first.
- **5.2** Dead-symbol / unwired-module CI check. GNI's DET-DEAD, `arb_ctx`, and Lens's
  `_FORCE_PROVIDER` are one bug class; Lens has since found the same shape a fourth time
  (every declared fallback leg in its registry was unreachable — not one call site read one).
  Highest-leverage single gate available to either repo.
- **5.3** A REFERENCE doc for GNI — what each position is, its model, key, caller, writer,
  known defects. Every GNI doc describes CHANGE; none describes the system as it IS.

- **5.4** **NEW - the register has THREE ID schemes, and CONTRACT cites three IDs absent from it.**
  `GNI_RULES.md` carries `GNI-R-###` (bold, no dash), `R-S##-#` (dash + parenthetical) and
  `LR-###` borrowed from Lens. Only FIVE `GNI-R-` lines exist (240, 241, 242 + two passing
  mentions), yet CONTRACT v5 cites GNI-R-037, GNI-R-076 and GNI-R-233 as live law. Either they
  live in another file or they were lost. One repo-wide grep settles it. Cheap, and it decides
  whether the contract's CORE DISCIPLINE section points at anything.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
- **PROBE-DRIFT: DUE TODAY (Aug 24).** Monthly, needs James's explicit authorization each run,
  never on a near-red account.
- **KEYFILE ROTATION: OVERDUE since Aug 9 (15 days).** One account at a time, quiet window
  (~03:30-09:30 UTC). Receipts = `gh secret list` updatedAt before/after; never echo a key.
- **PHISH-HW: OVERDUE since ~Jul 31 (24 days).** OAuth+GitHub Apps review, security log from
  2026-07-18, report the trypatchhog.com mail. Browser, James solo, x3 accounts.
- **PROVIDER + PLATFORM EOL WATCH (new this close).** Record every announced end-of-life as a
  DATED item here at announcement, not at death. Lens lost five positions to a Cerebras
  free-tier termination announced a month in advance by email and never read, then lost its
  whole database to a Supabase Fair-Use restriction warned at 20% by email and never read.
  **Read the meter, not the mail.** Known: `gemini-2.5-flash` dies Oct 16.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.

### RETIRE CANDIDATES — GENERATION 3 OF 3, RESOLVED AS THE CLAUSE REQUIRES
Every item below is CLOSED or PROMOTED with a written reason. None dropped in silence.
- **TRANS-COUNT-CERT** — **CLOSED AS ACCEPTED.** The fix shipped at S75; the cert was to be
  taken from any green run. 40/40 green through the Aug-16 cliff and 21/21 MAD runs green
  through 24 Aug is that evidence, arriving by accumulation rather than by ceremony.
- **CI-DEGRADE** — **PROMOTED to 5.1.** It is the same gate as PUSH-GATE; carrying it
  separately was a routing error, not a second item.
- **mojibake print** — **CLOSED AS ACCEPTED.** One cosmetic funnel print, no consumer, three
  generations below the line. Accepting it in writing costs less than reading it again.
- **adaptive-tidy** — **PROMOTED to 6.x scope.** Escalation pinned 10/10 since Jul 18 keeps
  dispatching ~12 Adaptive runs/day. Under ROOT 6 that is no longer tidiness — run frequency
  is an input to the storage stock, so 6.1 must count whether Adaptive writes rows.
- **promotion-proposal parser UX wart** — **CLOSED AS ACCEPTED.** A reply of "Keep" returns
  "Unrecognised"; proposals need no reply at all. Documented here as intended behaviour.
- **fallback live-fire** — **PROMOTED to 5.2.** Lens's finding makes this urgent in kind: it
  discovered that not one call site in its repo ever read a declared fallback leg. **Whether
  any GNI call site reads its declared fallback is ONE GREP**, and GNI's three-account MAD
  topology assumes redundancy it has never proven.
- **the parked 16 from HANDOFF_S79** — **CLOSED AS ACCEPTED, as a set.** Parked since July,
  never re-read, and the discovery policy is explicit that a parked list nobody reads is the
  accumulation disease. Anything real among them will be re-found by the work; re-finding is
  cheaper than carrying an unread list for a fourth generation.
- **`docs/STATUS.md`** — **PROMOTED to a one-line action:** delete it. A fossil frozen at S46
  that three protocol versions have called a fossil is not a candidate any more.

---

## CHANGED THIS REGENERATION

**CLOSED:** ROOT 1.3 (RULED on n=14, no action needed on the question — the fix is now a
separate item) · ROOT 1.5 (premise proven FALSE by bytes) · four retire candidates closed as
accepted, four promoted, all eight written.

**RE-SPECIFIED:** 1.7 (the overstatement that reaches the arbitrator is the four PILLAR
HEADERS, not `Total in pool`, which the trim removes) · 2.3 (from a musing to a per-day cut
across the S80 migration date) · 4.4 (per POSITION, not one divisor for the repo).

**UPGRADED:** 1.6 from suspicion to 14/14 confirmed · 2.3 promoted, now free to run.

**NEW:** ROOT 6 (four sub-items) · 1.8 denylist success computation · 1.9 arrival counted in
rows not distinct pillars · the PROVIDER + PLATFORM EOL WATCH block.

**RE-RANKED:** ROOT 6 enters ABOVE ROOT 1. Justification naming the target: 6.1 is minutes of
measurement, its failure mode is a public site serving stale intelligence (a truthfulness
failure, not merely an outage), and the sister project is living proof — offline since 23 Aug,
recovering no earlier than 11 Sep. ROOT 1 is urgent but it is not on a clock.

**DECISION S83-1:** the ROOT 1.3 fix is **per-article COST (B)**, NOT absolute per-consumer
allotments (C) as the S82 order pre-ruled. Why: the arbitrator's share is already stable at
62-65% of built context, so redistributing shares cannot raise coverage; the binding constraint
is ~230-250 chars per article. Lineage supports it — the founding S27 design fed the debate
ALL 300+ articles; the documented fabrication class is entity/geography/quantity insertions
ABSENT FROM THE BASKET (specimens 1, 2, 5, with the arbitrator itself publishing "Caucasus
region" to site and Telegram on zero anchor), and detecting absence needs BREADTH, not 100-char
summaries; C1 already established "read once, argue forward" with depth=0 slim anchors for
R2/R3. **The depth value must be DERIVED from the measured chars/article, never hand-picked
(R-S81-5).** Delegated by James ("your call"), recorded as delegated.

**DECISION S83-2:** before the 1.3 fix ships, BANK the arbitrator's current behaviour
distribution from the 14 harvested runs (verdict confidence, blind-spot length, GROUNDING
SHADOW hits per run). Why: Lens's D-016 migration passed its cert on mechanics while S2-E's
actor extraction doubled and S2-D's claim extraction TRIPLED — its headline `consistency`
metric moved 0.834→0.853 and hid it for three weeks. A cert that watches mechanics has not
certified the instrument. Its S2-D probe, given a real calibration band, then predicted live
behaviour to the digit.

**DECISION S83-3:** no CONTRACT v6. The cert lesson lands in `GNI_RULES.md` only. Why: the
contract went v1→v5 in six weeks and already indicts itself under its own law-vs-state test
(R-S82-5); one earned rule does not justify a version. Promote to law if a later session needs
it as law. Delegated by James.

**DECISION S83-4:** the denylist finding lands as item **1.8 under ROOT 1**, not under ROOT 5.
Why: GNI's own specimen lives in ROOT 1 (`ctx-trim@0` → SUCCESS), evidence belongs with its
item, and ROOT 5 is below the line so it would never be worked. Delegated by James.

**DECISION S83-5:** Transfer Protocol v3 — the CLOSE stops being pasted. Part D now reads the
protocol from the repo and the close is invoked by name. Why: byte-verified this session,
`sed -n '/PART D/,/PART E/p' | grep -c "Transfer_Protocol"` returns **0** — the closing prompt
had no path into a session except James's fingers, and a prompt in two places is a dual source
of truth. Lens shipped the identical fix after its pasted close was found to have silently
lost two clauses. No CONTRACT change needed: v5 already cites the prompts BY PATH; v3 merely
makes that path get walked.

**AMENDS R-S81-3** (not a new rule number): "a count says the tier shrank, a name says which
perspective was lost" now also requires counting DISTINCT IDENTITY rather than rows. Lens paid
for re-minting a rule it already had; taking that lesson immediately is why this is an
amendment.

**DOCS SHIPPED THIS CLOSE:** Transfer Protocol v3 · GNI_TARGET_AND_ORDER generation 3 ·
HANDOFF_S83 · R-S83-1..6 appended. CONTRACT unchanged (v5 stands).

**RETIRED:** all eight generation-3 candidates resolved above — four closed as accepted, four
promoted. The retire clause has now completed one full cycle.

---

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
