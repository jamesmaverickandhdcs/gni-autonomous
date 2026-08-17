# GNI TARGET + WORKING ORDER
**FIXED PATH — `docs/GNI_TARGET_AND_ORDER.md`. Always this path. Archived orders get descriptive
names; only the live one keeps the path, so no session ever hunts for the current version.**

GENERATED: 2026-08-17 (S82 close) · SUPERSEDES: the S81-close generation · HEAD `8f9b8c8`
GENERATION: 2

---

## NEXT SESSION'S MISSION (S83)
**ROOT 1.3 — read the first live ARB-ARRIVAL runs and RULE on starvation.**
The instrument shipped this session and has never fired. Two scheduled MAD runs will exist by
S83 open (02:43 and 10:43 UTC requests, firing 13-60 min later per R-S81-7). Read both, then
rule: is the arbitrator being starved of intelligence, or is the ladder working as designed?
- If starvation is REAL: ship ABSOLUTE per-consumer allotments (R-S81-3). Never by raising a
  cap, never by letting one tier's share be another tier's leftover.
- If it is NOT: say so with the numbers, close 1.3 as accepted, and the mission is complete.
  A mission that ends in "no action needed, here is the evidence" is a SUCCESS.
The grep: `ARB-ARRIVAL` in the MAD workflow log. Do NOT rule from one run.

---

## TARGET (unchanged — no phase transition this close)

> ### TRUTHFULNESS OF OUTPUT
> Everything GNI publishes is either grounded in something an agent actually read, or is
> visibly labeled as speculation.

**DEFINITION OF DONE — status at this regeneration:**
1. **Arrival is asserted, not assumed.** — **PARTIAL.** The instrument exists (`8f9b8c8`) and
   logs included-vs-available with names. Still open: zero-inclusion currently prints a loud
   WARNING but does not RAISE, and four sibling tiers are unmeasured (1.4).
2. **Label coverage matches fabrication surface.** — OPEN. Now byte-verified rather than
   inferred: E-3 labels `blind_spot_explanation` only; `short_focus_threats` and
   `action_recommendation` reach Telegram unlabeled. ROOT 2.
3. **GT5-T2 ruled with normalized evidence.** — OPEN, overdue since Jul 30. ROOT 2.1.
4. **Evidence base clean of fallback-era contamination.** — OPEN. ROOT 3.

The phase ends when the order has no urgent and no important items left. It does not end here.

---

## THE ORDER

Ranked against the declared target. **Freshness confers no priority.** Work the top. If you
believe the order is wrong, say so and propose a re-order — do not silently work something else.

### ROOT 1 — THE ARBITRATOR'S INPUTS ARE UNVERIFIED AND ITS SHARE IS A REMAINDER · URGENT
*Audit CLOSED this session. The mechanism is confirmed; the firing is not measured.*
Byte evidence (S82, full-file census): nothing in 1,211 lines asserts arrived-vs-assembled.
`_keep = _arb_budget_chars - (len(arb_final_user) - len(arb_ctx_fit)) - 40` makes the article
tier a LEFTOVER, and `max(0, ...)` means that if R2/R3 grow, the arbitrator receives ZERO
articles, the log prints `ctx-trim@0`, and the run reports SUCCESS. Reachable, not currently
firing (Aug 17 = `ctx-trim@4983`). This is GNI's structural twin of Lens's `s1=0`.
- **1.1** ✅ CLOSED — audit complete, absence evidenced not assumed.
- **1.2** ✅ SHIPPED — `8f9b8c8`, ARB-ARRIVAL print-only instrument.
- **1.3** **S83 MISSION.** Read the numbers, rule on starvation, fix with absolute allotments
  only if the evidence triggers it.
- **1.4** Widen the instrument to ALL FIVE tiers — `constraint_block`, R1, R2, R3, `_arb_tail`
  compete for the same budget and are unmeasured, so today's log shows articles shrinking
  without naming which tier ate the room (R-S82-2). Do this WITH 1.3 if 1.3 needs it.
- **1.5** `_arb_trunc` reads 0 even when the slice cut mid-article, because the ctx-trim branch
  appends `'\n[ctx trimmed to fit]\n'` after slicing. Read `dropped=N` as "at least N" until
  fixed. Disclosed at ship time, not discovered later.
- **1.6** The public `/debate` page publishes `mad_round1_positions` while `drop-R1` fires on
  EVERY run — humans are shown a transcript the verdict-bearer never read. Squarely on target:
  this is a truthfulness-of-output defect, not a cosmetic one.
- **1.7** `_build_news_context` prints `Total in pool: {total}` into the prompt while rendering
  only `sorted_arts[:15]` per pillar. The model is told a number larger than what it can see —
  an invitation to reason about articles that are not there.
- **NOTE (R-S82-3):** C1 transcript-carry certified PASS and did NOT close this root. It freed
  prompt room and the arbitrator gained none of it — still riding the full ladder three weeks
  later. Do not treat C1's cert as evidence about arbitrator starvation.

### ROOT 2 — LABEL COVERAGE IS NARROWER THAN THE FABRICATION SURFACE · IMPORTANT
Now byte-verified (S82): the E-3 label path wraps `blind_spot_explanation` alone.
- **2.1** GT5-T2 decision, overdue since Jul 30. Normalize hits per COMPLETED run before ruling
  (52 raw across ~4 live arbs is ~13/run, not a 2x worsening). Pre-ruled default: **A, hold**.
  Trigger **B** (extend the same fail-open `check_grounding` join to short_focus + action) iff
  hits >= ~12 per completed run OR LABELED fired in fewer than half the runs that had hits.
  **C (gate/regenerate) stays rejected: fail-open is law, gates starve.**
- **2.2** Build B only if 2.1 triggers it.
- **2.3** Verdict-confidence timidity (five verdicts all 0.48-0.53) — is gpt-oss hedging where
  3.3-70b committed? Feeds 2.1, decides nothing alone.

### ROOT 3 — FALLBACK-ERA CONTAMINATION IN THE EVIDENCE BASE · IMPORTANT
Jul 19-22 rows written by the 8b fallback during the MODEL-404 blackout pollute every quality
baseline the target depends on.
- **3.1** Pin the exact window from funnel-log engage/disengage lines, NOT memory (S79 says
  19-21, S80 says 19-22 — the disagreement is the point).
- **3.2** `data_era` column + tagging, count-before == rows-updated, then exclude in GPVS/quality
  queries. James solo in the Supabase SQL editor.

### ROOT 4 — COST AND HEADROOM · IMPORTANT (serves the target where starvation causes fabrication)
- **4.4** **Measure the real chars/token divisor.** `_call_agent` already holds both the prompt
  character count and `usage.prompt_tokens` IN THE SAME SCOPE — one log line, zero API cost,
  no probe. Lens measured 3.435-3.713 for its mix, so `//3` over-estimates ~14-19%, which is
  the SAFE direction: **do not change it to //4 without GNI's own measurement.** Promoted above
  4.1 because it unblocks 4.1 independently of the quota read.
- **4.1** C2 solver recalibration: teach `compute_depth` the per-request ceiling so R1 escapes
  the 768 band; fix the stale "NOT WIRED — do not import" header (imported and live since S51);
  rewrite the self-test table. **Blocked on: the real bill (Unknown #1) — partially unblocked by
  4.4.**
- **4.2** Nine 429s per run recover at 46.6-60.4s. S82 narrowed this: W-02's coarse retry uses
  `base=60.0` and DOES clear the TPM window; the observed waits are the INNER `_call_agent`
  header-derived path, which does not. Read that site before any claim. Cheapest possible fix
  if real (one constant, failure path only).
- **4.3** Quota-guard reference correction: Groq TPD refills CONTINUOUSLY at Limit/86400 per
  second (~8,333/hour at 200K); there is no reset boundary and no `-day` header. GNI reserves
  per-account-DAY (17,500 + 80,000 of 100K). The split may be sound; what is unsound is any
  recovery estimate shaped as "wait until tomorrow." Audit, then correct comments.

### ROOT 5 — INSTITUTIONAL HARDENING · BELOW THE LINE (high long-term value, not target-critical)
- **5.1** PUSH-GATE: Actions test-gate blocking red pushes (the 61adb50 lesson). Soft mode first.
- **5.2** Dead-symbol / unwired-module CI check. GNI's DET-DEAD and Lens's `_FORCE_PROVIDER` are
  the same bug class five months apart, both found by accident. **New GNI specimen found this
  session: `arb_ctx` is built at L713 with full depth, then superseded by `arb_ctx_fit` at the
  arb site and never read** — third instance of the class, still no detector. Highest-leverage
  single gate available to either repo.
- **5.3** A REFERENCE doc for GNI — what each position is, its model, key, caller, writer, known
  defects. Every GNI doc describes CHANGE; none describes the system as it IS, which is why every
  session re-derives architecture by grepping. Prefer generated over hand-written.

### LIFECYCLE + SECURITY — target-independent, deadline-driven, never ranked away
- **KEYFILE ROTATION: OVERDUE since Aug 9 (8 days).** One account at a time, quiet window
  (~03:30-09:30 UTC, clear of both cron waves). Never mid-debate. Receipts = `gh secret list`
  updatedAt before/after; never echo a key.
- **PHISH-HW: OVERDUE since ~Jul 31 (17 days).** OAuth+GitHub Apps review, security log from
  2026-07-18, report the trypatchhog.com mail. Browser, James solo, x3 accounts.
- **PROBE-DRIFT: due ~Aug 24 (7 days out).** Monthly, needs James's explicit authorization each
  run, never on a near-red account.
- **OC-A**: closed Jul 25, next quarterly re-check ~Oct 25.

### RETIRE CANDIDATES — generation 2 of 3
At generation 3 each is CLOSED as accepted or PROMOTED with a written reason. Silent dropping is
neither.
TRANS-COUNT-CERT · CI-DEGRADE · mojibake print · adaptive-tidy (escalation pinned 10/10 since
Jul 18 keeps dispatching ~12 Adaptive runs/day) · promotion-proposal parser UX wart · fallback
live-fire (trigger-parked by design) · the parked 16 from HANDOFF_S79 · `docs/STATUS.md` (fossil
frozen at S46, retired as a file type at Protocol v1 but never deleted).

---

## CHANGED THIS REGENERATION

**CLOSED:** ROOT 1.1 (audit complete, absence evidenced) · ROOT 1.2 (shipped `8f9b8c8`) ·
the "does anything verify arrival" Unknown from HANDOFF_S81 (answered: no).

**SHIPPED:** `8f9b8c8` ARB-ARRIVAL instrument — 1 file, 33 insertions, behaviour-unchanged,
verified structurally rather than asserted.

**PROMOTED:** 4.4 chars/token measurement above 4.1, because it unblocks 4.1 at zero cost ·
ROOT 5.2 gains a third specimen (`arb_ctx`) found this session.

**NEW (all found this session, all recorded before analysis per the discovery policy):**
1.4 five-tier instrument widening · 1.5 `_arb_trunc` blind spot · 1.6 public /debate shows R1 ·
1.7 `Total in pool` overstatement · 4.4 chars/token · the C1-did-not-close-the-root note.

**RE-RANKED:** ROOT 1 stays URGENT but its character changed — it was "a candidate silent live
failure, unconfirmed"; it is now "a confirmed mechanism, unmeasured firing." The audit converted
suspicion into a specific line of code.

**DECISION S82-1:** ARB-ARRIVAL shipped as print-only (A) over persist-to-schema (B) and
instrument-plus-fix (C). Why: 1.3's own trigger is "if starvation is real", and choosing an
allotment number before measuring would be a hand-derived guard value (R-S81-5); B adds a schema
change, top of the blast-radius ladder (LR-104), and is better informed after A's numbers exist.
Delegated by James ("your call"), recorded as delegated.

**DECISION S82-2:** Decisions get NO separate D-register. They live as DECISION lines here, in the
close that made them. Why: GNI already carries two rule registers, and a fifth document type
worsens the which-doc problem ROUTING exists to solve. Accepted cost, in writing: decisions are
findable only by reading past order files.

**DECISION S82-3:** A close is a CHECKPOINT, not a hard stop — work may continue after a close if
the order is regenerated again and the amendment logged. Why: the hard-stop reading has been
broken three times across both projects, every time by legitimate work. What caused harm in Lens
was continuing WITHOUT regenerating. Bind that, permit the rest. Delegated by James.

**DECISION S82-4:** CONTRACT v2's model roster evicted as state; v3's economy rule KEPT as law but
de-rostered (model names removed). Why: the roster was already false — it named Opus 4.8 while
S82 ran on Opus 5 — but the underlying principle is a genuine rule of engagement.

**DOCS SHIPPED THIS CLOSE:** CONTRACT v5 · Transfer Protocol v2 (Parts A/B/C/D rebuilt; the close
prompt now regenerates an order, which it never did before) · R-S82-1..5 appended · HANDOFF_S82.

**RETIRED:** nothing. Generation 2 cannot retire; generation 3 must.

---

## HOW THIS FILE IS MAINTAINED
1. **FIND** — record every weak point with its evidence immediately, whatever the mission.
2. **CLASSIFY** — a silent live failure is urgent under any target. Everything else ranks by
   distance to the declared target, with a written justification naming it. Perishable evidence
   sets a DEADLINE, not a rank.
3. **ANALYSE** at close, not mid-session. The test: "does this change what I should do in the next
   hour?" The two rationalisations that are NOT triggers: "this is interesting" and "I'm already
   in the file."
4. **RE-ORDER** — regenerate, dated, superseding. Never appended.
5. **WORK THE TOP.**

*Mirrors the Lens discovery policy by reference, stated in GNI's own terms against GNI's own
evidence — never by paste. Dual sources of truth are how S2-D died. Logged on both sides.*
