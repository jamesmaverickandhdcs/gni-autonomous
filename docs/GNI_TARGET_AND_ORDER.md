# GNI TARGET + WORKING ORDER
**FIXED PATH — `docs/GNI_TARGET_AND_ORDER.md`. Always this path. Archived orders get descriptive
names; only the live one keeps the path, so no session ever hunts for the current version.**

GENERATED: 2026-08-17 (S81 close) · SUPERSEDES: nothing (first generation) · HEAD `43f74fc`

---

## NEXT SESSION'S MISSION (S82)
**ROOT 1.1 + 1.2 — audit whether anything verifies what the arbitrator RECEIVED, and if
nothing does, ship the instrumentation commit that makes it visible.**
One mission. The close asks "did we complete it?", not "did we fix everything we found?"
A session that ships one thing and logs six is a success.

---

## PHASE TRANSITION LOGGED

**PREVIOUS TARGET: "Survive the Aug-16 Groq model cliff." DECLARED ACHIEVED, WITH EVIDENCE:**
- Whole organism migrated to `openai/gpt-oss-120b` (S78-S80), fallback armed on 20b, MAD
  migrated with a pre-death baseline banked in git (`probe_results.jsonl`, 4124e2e).
- Five consecutive real MAD verdicts post-migration, zero 413s.
- Aug 17 09:41 UTC: `gh run list -L 40` grouped by conclusion = **success 40, failures 0**,
  spanning Aug 16. Three weeks unattended, through the cliff, no human touch.
- Lens's half of the cliff shipped separately and is tracked in the Lens repo.
This target is CLOSED. It is not reopened by anything below.

**NEW TARGET (declared S81 close; James delegated the call this once — recorded as delegated,
not drifted, so the record cannot be misread later):**

> ### TRUTHFULNESS OF OUTPUT
> Everything GNI publishes is either grounded in something an agent actually read, or is
> visibly labeled as speculation.

**DEFINITION OF DONE — all four, each falsifiable:**
1. **Arrival is asserted, not assumed.** Every consumer that assembles inputs under a budget
   logs what was INCLUDED against what was AVAILABLE, and zero inclusion of a required input
   raises rather than passing quietly.
2. **Label coverage matches fabrication surface.** Every free-text field that reaches Telegram
   (blind_spot, short_focus, action) is inside the E-3 estimative-label path, or is ruled
   out of scope in writing with a reason.
3. **GT5-T2 is ruled with normalized evidence** — arb-level fabrication hits per COMPLETED run,
   not raw counts, with the label-fire rate beside them.
4. **The evidence base is clean of fallback-era contamination** — Jul 19-22 rows tagged and
   excluded from quality/GPVS queries.

When the order below has no urgent and no important items left — only accepted retire
candidates and lifecycle maintenance — the phase ends and James declares the next target.

---

## THE ORDER

Ranked against the declared target. **Freshness confers no priority.** Work the top, not the
newest and not the most interesting. If you believe the order is wrong, say so and propose a
re-order — do not silently work something else.

### ROOT 1 — NOTHING VERIFIES WHAT THE ARBITRATOR RECEIVED  ·  URGENT
*Why urgent under any target: this is a candidate SILENT LIVE FAILURE, and a silent failure
defeats every target. Not yet confirmed — the audit is step 1.1.*
Evidence: ARB-FIT rides the full ladder on every run (`drop-R1,R3@110w,ctx-trim@~5K`), so the
arbitrator's context is trimmed to ~5,000 chars EVERY debate. Nothing currently counts what
survived the trim. Lens measured the same shape and found its synthesis position running 16
consecutive waves with zero or one of four required inputs while reporting SUCCESS.
- **1.1** Read `mad_protocol.py:964-998` (assembly) + the ladder + the parse path. Answer one
  question: does anything assert arrived-vs-assembled? Report verified-vs-assumed per claim.
- **1.2** Instrumentation commit — behaviour-unchanged, one log line: articles/rounds included
  vs available, chars dropped per ladder step, and WHICH content was dropped by name.
  *(Lens's biggest defect in five months was found by exactly this, not by reasoning.)*
- **1.3** If starvation is real: fix with ABSOLUTE per-consumer allotments (R-S81-3), never by
  raising a cap and never by letting one tier's share be another tier's leftover.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE  ·  IMPORTANT
Evidence: E-3 labels the blind spot only. Grounding-watch arb-level hits rose 28 -> 32 -> 52 as
the arbitrator came back to life, and the fabricated spans in the Jul digests appear in
short_focus and action text too (DSN telemetry, OFAC/Copernicus feeds, Kazakhstan).
- **2.1** GT5-T2 decision, overdue since Jul 30. Normalize hits per COMPLETED run before ruling
  (52 raw across ~4 live arbs is ~13/run, not a 2x worsening). Pre-ruled default: **A, hold** —
  labels plus counting. Trigger **B** (extend the same fail-open `check_grounding` join to
  short_focus + action) iff hits >= ~12 per completed run OR LABELED fired in fewer than half
  the runs that had hits. **C (gate/regenerate) stays rejected: fail-open is law, gates starve.**
- **2.2** Build B only if 2.1 triggers it.
- **2.3** Verdict-confidence timidity (five verdicts all 0.48-0.53) — judge whether gpt-oss is
  hedging where 3.3-70b committed. Feeds 2.1, decides nothing alone.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE  ·  IMPORTANT
Jul 19-22 rows were written by the 8b fallback during the MODEL-404 blackout and silently
pollute every quality baseline the target depends on.
- **3.1** Pin the exact window from funnel-log engage/disengage lines, NOT from memory
  (S79 says 19-21, S80 says 19-22 — the disagreement is the point).
- **3.2** `data_era` column + tagging update, count-before == rows-updated, then exclude in
  GPVS/quality queries. James solo in the Supabase SQL editor.

### ROOT 4 — COST AND HEADROOM  ·  IMPORTANT (serves the target only where starvation causes fabrication)
- **4.1** C2 solver recalibration: teach `compute_depth` the per-request ceiling so R1 escapes
  the 768 band; fix the solver's stale "NOT WIRED — do not import" header (it has been imported
  and live since S51); rewrite the self-test table. Needs 2-3 billed post-C1 runs as data —
  those now exist. **Blocked on: the real bill (Unknown #1).**
- **4.2** Finding-4 read: nine 429s per run recover at 46.6-60.4s, i.e. mostly INSIDE one 60s TPM
  window, which would make each retried call fit twice. Read the retry/backoff site before any
  claim. Cheapest possible fix if real (one constant, failure path only).
- **4.3** Quota-guard reference correction: Groq TPD refills CONTINUOUSLY at Limit/86400 per
  second (~8,333/hour at 200K) — there is no daily reset boundary and no `-day` header exists.
  GNI reserves per-account-DAY (17,500 + 80,000 of 100K). The split may still be sound; what is
  unsound is any recovery estimate shaped as "wait until tomorrow." Audit, then correct comments.

### ROOT 5 — INSTITUTIONAL HARDENING  ·  BELOW THE LINE (high long-term value, not target-critical)
- **5.1** PUSH-GATE: Actions test-gate blocking red pushes (the 61adb50 lesson). Soft mode first
  (gate runs, red alerts Telegram, pushes still land); hard mode is a branch-protection decision.
- **5.2** Dead-symbol / unwired-module CI check. GNI's DET-DEAD (70 injection patterns imported
  by nothing since March) and Lens's `_FORCE_PROVIDER` are the same bug class, five months apart,
  both found by accident. Neither repo has a detector. Highest-leverage single gate available.
- **5.3** A REFERENCE doc for GNI — what each position is, its model, key, caller, writer, known
  defects. Every doc GNI has describes CHANGE; none describes the system as it IS, which is why
  every session re-derives architecture by grepping. Prefer generated over hand-written.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
- **KEYFILE ROTATION: OVERDUE since Aug 9.** One account at a time, in the quiet window
  (~03:30-09:30 UTC, clear of both cron waves). Never mid-debate. Receipts = `gh secret list`
  updatedAt before/after; never echo a key.
- **PHISH-HW: OVERDUE since ~Jul 31.** OAuth+GitHub Apps review, security log from 2026-07-18,
  report the trypatchhog.com mail in Gmail. Browser, James solo, x3 accounts.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.
- **PROBE-DRIFT**: ~Aug 24, monthly, needs James's explicit authorization each run, never on a
  near-red account.

### RETIRE CANDIDATES — below the line for the first generation
An item unworked below the line for THREE regenerations is either closed as accepted or
promoted with a written reason. **Dropping one silently is neither.**
TRANS-COUNT-CERT · CI-DEGRADE · mojibake print · adaptive-tidy (escalation pinned 10/10 since
Jul 18 keeps dispatching ~12 Adaptive runs/day) · promotion-proposal parser UX wart · fallback
live-fire (trigger-parked by design) · the parked 16 from HANDOFF_S79.

---

## CHANGED THIS REGENERATION
First generation — everything below is the conversion of S80's flat queue plus S81's findings
into a ranked order under a declared target.
- **CLOSED:** RULES-APPEND (committed 381886d) · OC-A (Jul 25, all 3 accounts) · MAD-CERT
  (passed x5) · LENS-SESSION (brief written + committed to Lens as 9b2836d) · CLIFF Aug 16
  (survived, evidence above) · E3-WATCH (fired live; the watching question folds into 2.1).
- **PROMOTED:** the arbitrator-arrival question, which did not exist as an item in July, is now
  ROOT 1 and outranks everything by the absolute rule.
- **DEMOTED:** C2 solver work moves from "S82 opener" to 4.1 — it is cost, and cost serves the
  new target only indirectly.
- **MERGED:** "gpt-oss debate QUALITY" (old #12) into 2.3; "GT5-T2" (old #4) into 2.1.
- **RE-RANKED:** PUSH-GATE from IMPORTANT to below-the-line (5.1) — it protects the repo, not
  the output's truthfulness.
- **NOTED OVERDUE, NOT RE-RANKED:** keyfile (Aug 9) and PHISH-HW (Jul 31) sit in LIFECYCLE
  because a deadline sets a date, not a rank.
- **RETIRED:** nothing yet. First generation cannot retire.

## HOW THIS FILE IS MAINTAINED
1. **FIND** — record every weak point with its evidence immediately, whatever the mission.
   Suppressing a finding is worse than acting on it out of order.
2. **CLASSIFY** — a defect causing a SILENT LIVE FAILURE is urgent under any target. Everything
   else is ranked by distance to the declared target, with a one-line written justification
   naming that target. Perishable evidence sets a DEADLINE, not a rank.
3. **ANALYSE** at close, not mid-session. The test: "does this change what I should do in the
   next hour?" If no, record and continue. Only three things force analysis now: the finding is
   upstream of the current mission and would make the pending change harmful; a live position is
   failing silently right now; or the evidence is perishable (that is ACTION — bank it).
4. **RE-ORDER** — regenerate this file, dated, superseding. Never appended.
5. **WORK THE TOP.**

*Mirrors the Lens discovery policy by reference, stated in GNI's own terms against GNI's own
evidence — never by paste. Dual sources of truth are how S2-D died. Logged on both sides.*
