# GNI S46 -- Session Audit

**Date:** 2026-06-21 (UTC) | **Operator:** James Maverick (Bro Alpha / Team Geeks)
**Model:** Claude Opus 4.8 (via Claude Code + chat) | **Repo:** jamesmaverickandhdcs/gni-autonomous
**Local:** C:/HDCS_Project/03/GNI_Autonomous | **Push:** standard `git push origin main`

> This audit is the ground-truth record of S46. It is written so a FRESH session (also
> Claude, but without this session's working context) can reconstruct exactly what was
> done, why, and what remains. Every commit hash is verified against origin/main via
> `git ls-remote`. Trust this file at the band of "Claude-verified-this-session" (~90-95%),
> not 100% -- re-read code before resuming (Treasure 1 + 2).

---

## 1. HEADLINE -- WHAT SHIPPED

Five commits, each through the full gated arc (BEV -> deep analysis -> propose -> James
decides -> build -> dry-run/verify -> commit -> `git ls-remote` hash confirm). Prior S46
foundation (77f874e token metering, c5104ec Bull de-bias) was already on main before this
session.

| # | Hash | Title | Proof |
|---|------|-------|-------|
| 1 | `460ce84` | false-neutral integrity fix | dry-run 16/16 + 7 rows backfilled |
| 2 | `c40a5c2` | header-aware rate governor | dry-run 30/30 + PRODUCTION-PROVEN |
| 3 | `bb280a4` | MAD agent/consultant/arbitrator redefinition | dry-run 31/31 + 1 live cron clean |
| 4 | `ef3f9bf` | adaptive logs 0 Groq tokens (Cerebras-only) | sum-check (adaptive contributes 0) |
| 5 | `b27474e` | cron drift-fix (:00 -> :13/:43/:58) | YAML valid + traps handled |

**Commit trail (chronological):** 77f874e -> c5104ec -> 460ce84 -> c40a5c2 -> bb280a4 -> ef3f9bf -> b27474e

---

## 2. COMMIT 1 -- FALSE-NEUTRAL INTEGRITY FIX (460ce84)

**The bug (worse than first estimated):** the `mad_succeeded` gate in `mad_runner.py`
LEAKED via a third clause `bool(mad_result.get('mad_bull_case'))`. On Arbitrator-only
failures (429 -> default neutral/0.5) with healthy agents, that clause flipped `mad_succeeded`
to True -> the quality scorer + predictions RAN ON FABRICATED 0.5 NEUTRALS, corrupting the
IEEE-paper prediction dataset for months. This was NOT predicted by the initial mechanism
guess -- it was caught only by BEV (became the named rule "protections-guilty-until-BEV'd",
memory #14).

**The fix:**
- Typed `mad_arb_failed` flag = single source of truth (replaces fragile `confidence==0.5`
  heuristic), set at `mad_protocol.py` `_arb_is_error` branch + JSON-parse-fail branch +
  result dict.
- `_compute_mad_succeeded()` veto in `mad_runner.py`: `mad_arb_failed=True` is an absolute
  veto closing the leaky gate.
- `_assert_mad_integrity()` canary: logs `integrity_violation` if `succeeded && arb_failed`
  ever co-occur (Treasure-3 assertion -- assumption moved INTO code).
- Honest `_mad_telegram_text`: emits INCOMPLETE, not fake NEUTRAL.
- Dashboard: count-exclusion + INCOMPLETE badges on page.tsx / debate / brief / quantum
  (all 4 surfaces).

**Prerequisite (DONE):** `ALTER TABLE reports ADD COLUMN IF NOT EXISTS mad_arb_failed
boolean NOT NULL DEFAULT false` + backfill `UPDATE ... WHERE mad_confidence=0.5 AND
mad_reasoning LIKE '[Agent error%'` -> **7 historical false-neutrals flagged true**
(SELECT-count-first verified, read-back confirmed 7).

**Dry-run:** `ai_engine/tests/dryrun_false_neutral.py` = 16/16 (forced-failure + control),
offline/hermetic.

---

## 3. COMMIT 2 -- HEADER-AWARE RATE GOVERNOR (c40a5c2) [PRODUCTION-PROVEN]

**History lesson that drove the design:** the 429 had been "solved" 4 times (S13->S26:
sleeps 8s->12s->20/30->40/45/90) but NEVER permanently. Every clean run shared
"Used: 6175, Headroom: 78825" (fresh quiet-news morning); every failure had a stressed
quota. **Sleep-tuning only ever "worked" when news went quiet -- calm news solved it, not
the sleeps.** The real cure (adaptive-wait + algorithmic fallback) was DESIGNED in S26 and
NEVER built.

**The LIVE 429 PROBE (the design's foundation -- not a doc claim):** a throwaway probe
(`probe_429_headers.py`, since deleted, ~12.7K tokens) on James's real key observed:
- `retry-after: 4` (coarse, whole seconds -- Groq rounds up; body said 3.675s)
- `x-ratelimit-reset-tokens: 55.73s` = **the BINDING token-bucket signal** (NOT retry-after)
- `x-ratelimit-remaining-tokens: 854` when it hit
- `x-ratelimit-limit-tokens: 12000` = **12K TPM standard tier confirmed (NOT raised)**
- 429 hit on call 9 at Used 11146 + Requested 1589 > 12000

**Key insight:** one MAD run (~21-25K tokens) is ~2x the 12K/min budget. The old flat-40s
UNDERSHOT the real ~56s bucket-reset, retrying into a near-empty bucket. Honor the
token-reset (~56s), NOT the coarse retry-after (4s).

**The build:**
- NEW `ai_engine/mad_rate_governor.py` (pure, stdlib-only, one-way import): `parse_groq_duration`
  (parses "55.73s"/"11m31.2s"/"4"), `compute_wait_from_headers` (prefers token-reset over
  retry-after, +0.5s margin, CAP 75s), `compute_backoff` (15->30->60->120 jitter),
  `is_transient_error`.
- Wired into `mad_protocol.py`: **`max_retries=0`** (Decision A1 -- governor owns all waits,
  removes SDK's counterproductive 4s-into-empty-bucket retries), **`_MAX_ATTEMPTS=3`**
  (Decision B), header-aware `_call_agent` retry via `getattr(e,'response')` guard,
  **body-429 zero-retry gap CLOSED** (retries via backoff), transient non-429 (5xx/timeout/
  conn) gets ONE backoff retry + non-transient fails fast (recovers resilience lost by
  max_retries=0), W-02 arbitrator flat-60s -> bucket-sized wait.
- COMMIT-1 invariant preserved: exhausted -> `[Agent error]` -> `mad_arb_failed` still fires.

**Dry-run:** `ai_engine/tests/dryrun_rate_governor.py` = 30/30 (a-h + invariant).

**PRODUCTION PROOF (the green light):** live MAD cron 2026-06-21 07:14 during CRITICAL
Iran/Hormuz storm. Log: governor waited REAL header windows **45.1s / 55.6s / 46.5s** on
R1/R2/R3, each SUCCEEDED, Arbitrator COMPLETED real verdict **bearish (0.83)**, all fields
populated, 53733 tokens / 21 calls, Status SUCCESS -- the exact scenario that produced
fake-neutral-0.5 on June 20.

---

## 4. COMMIT 3 -- MAD AGENT/CONSULTANT/ARBITRATOR REDEFINITION (bb280a4)

**Origin -- the consultant-deference bug:** in a live debate fact-check, a Personal
Consultant HALLUCINATED "the US VP is Kamala Harris" (actually JD Vance -- the Bull agent
was originally CORRECT), and the Bull CAPITULATED: "I acknowledge the correction... I will
ensure accuracy going forward." Web-search confirmed the situation real + accurate and the
verdict (bearish 0.83) earned; the only flaw was the consultant injecting a false fact and
the agent deferring.

**The literal bug source (found by BEV):** every consultant prompt contained
`FOUNDATION CHECK: If [agent]'s argument contains a factual error or logical contradiction,
correct it FIRST`. The consultant was TOLD to find+correct errors, so it manufactured one.

**James's architectural redefinition (the fix):** all agents + consultants + Arbitrator on
ONE shared senior foundation -- a senior strategist-analyst in Geopolitics + Technology +
Finance (woven, the DOMAIN), whose PRIMARY/defining skill is HIDDEN-PATTERN RECOGNITION +
INVISIBLE LINKING (the connections/brokers/2nd-order effects others miss). On that floor,
each agent applies a relative LENS (direction, NOT competence): Bull=opportunity,
Bear=systemic failure, Black Swan=unknown tail risk, Ostrich=ignored/inertia. Each
consultant = SAME senior caliber, SAME lens as its agent + the function of ALTERNATIVE
DEVELOPER OF INSIGHT (deepens/expands the case IN THE SAME DIRECTION, NEVER corrects/judges).
Equal rank + same lens = no authority to capitulate to, no opposing direction to drift
toward -> kills the deference bug AND reinforces S46 de-bias permanently.

**Build (strings only -- wiring untouched):**
- Shared `SENIOR_FOUNDATION` constant reused by all 11 prompts.
- 4 agents rewritten: foundation + pure lens + preserved mechanics (Bull pre-buttal, Bear
  risk-pricing/scope, Swan UAP/fallout-chain, Ostrich silo-gap/jurisdiction) + explicit
  lens-purity locks ("never hedge/soften/retreat/drift").
- 4 consultants rewritten via shared `_consultant()` scaffold: equal-rank same-lens
  insight-developer; the `FOUNDATION CHECK: correct it FIRST` clause DELETED entirely.
- Arbitrator (`ARB_FINAL`) elevated to same foundation + cross-lens synthesis role; JSON
  schema BYTE-IDENTICAL (parser + Commit-1 frontend safe -- self-check asserted unchanged).
- TIER-1 `GROUNDING_RULE` added to all 9 prompts: "state no named fact unless in provided
  intelligence" (closes the C1 anti-hallucination gap that let "Kamala Harris" through).
- UNCHANGED: call sites, R2/R3 injection wrappers, `_build_news_context`, NN-5 constraints,
  JSON parser, `_validate_mad_output`.

**Token note:** system prompts ~doubled per call (~700 tok vs old ~150-400); per-call still
well under 12K TPM, but more per-minute pressure -> governor waits more -> runtime stretches.
James accepted: pay time for quality (MAD ~6min fine; Lens runs ~30min).

**Dry-run:** `ai_engine/tests/dryrun_mad_redefinition.py` = 31/31 (bug-clause-gone,
lens-locks-present, grounding-in-9, schema-identical, foundation-in-9, end-to-end mock
debate -> parseable bearish 0.68 with mad_arb_failed=False).

**First live cron (12:13 UTC):** ran on the new prompts -> clean bearish 0.83, full fields.
Wiring production-validated. **CAVEAT:** the prompt-QUALITY effect (does senior framing
improve debate? does grounding suppress hallucination in practice?) can only be judged by
READING a real transcript -- not yet done. See brief, NEXT STEP.

---

## 5. COMMIT 4 -- ADAPTIVE LOGS 0 GROQ TOKENS (ef3f9bf)

**The phantom-accounting bug (root cause of the 12:22 MAD quota block):** adaptive runs on
CEREBRAS (verified end-to-end: `analyze(provider='cerebras')` -> `_call_cerebras` only in
the GITHUB_ACTIONS branch, returns None on fail, NO Groq fallback in production). But it
LOGGED a phantom `6175` Groq tokens/run under `pipeline='gni_adaptive'`. `get_today_usage()`
sums `tokens_used` across ALL pipelines unfiltered, so the phantom tokens polluted the shared
85K Groq ceiling and could BLOCK the real scheduled MAD. On a storm day (adaptive firing
repeatedly), the phantom burn tipped the day over and blocked the 12:22 MAD.

**The fix:** log `tokens_used=0` (the truth -- it's Cerebras), KEEP the `log_usage` row (so
`/adaptive-log` + alerts run-history survive -- they read rows for activity/trigger-count,
not just tokens), `requests_used` kept (never summed by the guard).

**Proof:** sum-check (2 mock 0-token adaptive rows + 1 48K mad row -> sum == 48000; adaptive
contributes 0). Frontend confirmed: adaptive-log/page.tsx shows run count + rows (preserved),
Total Tokens shows 0 (accurate), no filter-drop or divide-by-tokens.

---

## 6. COMMIT 5 -- CRON DRIFT-FIX (b27474e)

**The problem:** pipeline/MAD/graph crons were at `:00` (02:00/10:00 etc.). GitHub Actions
DELAYS top-of-hour jobs under load, causing observed drift (02:00 -> ~06:50, 10:00 -> ~12:13).

**The fix:** moved off `:00` to odd minutes, preserving 8h spacing + relative offsets:
- pipeline `13 2`/`13 10` (02:13/10:13)
- MAD `43 2`/`43 10` (02:43/10:43 -- = pipeline +30, handshake preserved)
- graph `58 2`/`58 10` (02:58/10:58 -- = +45, 15min after MAD)

**Two MANDATORY traps (both handled):**
1. `verify-outcomes` job gated on `github.event.schedule == '0 10 * * *'` -> updated to
   `'13 10 * * *'` (or the daily GPVS verifier SILENTLY STOPS).
2. MAD at 10:43 kept INSIDE the 09:00-10:45 GNI-R-122 protection window -> `monitoring_pipeline.py`
   untouched (the :17/:47 option Claude first proposed would have pushed MAD to 10:47, 2 min
   past the window edge -- avoided).

**CRITICAL NOTE:** the quota bucket is per-UTC-CALENDAR-DAY (`usage_date = now(UTC).date()`).
So both daily runs land in the SAME bucket regardless of intra-day spacing. **Cron spacing
does NOT raise daily headroom** -- this fix is for PREDICTABILITY (less GHA drift), NOT quota
relief. (This corrected an initial shared assumption that spacing would help quota -- it
doesn't.)

**Proof:** YAML valid (all 3 files), stale-cron grep clean, comments updated for truth.

---

## 7. THE DEEP-DIVE THAT FOUND THE REAL QUOTA PICTURE (BEV, not yet acted on)

Multiple BEVs traced the quota system end-to-end. Findings that MATTER for next session:

- **Adaptive was never a real Groq cost** -- it's Cerebras; the only burn was the phantom
  log (now fixed by Commit 4). The "adaptive starves MAD" story was a bookkeeping LIE.
- **Real MAD cost is large and now larger:** old baseline ~48,491 tokens/run; Commit 3's
  prompt enlargement pushed it to a plausible ~48-65K/run. **Two real MAD runs ~96-130K/day
  -- AT/OVER the 100K internal hard cap by themselves**, independent of adaptive.
- **The quota gate is BLIND to this:** `check_quota('gni_mad')` gates on a STALE estimate
  `PIPELINE_COSTS['gni_mad'] = 7433` -- under-counts real MAD by ~6.5x. That's why MAD #2
  isn't blocked daily despite the real bucket being high. (This stale constant is the perfect
  Treasure-3 assertion target -- an assumption pretending to be a fact, wrong by 6.5x all
  session.)
- **Sacred-MAD (make MAD always-permitted) is NOT safe alone** -- two sacred MADs (~96-130K)
  would breach the 100K hard cap. The BEV caught this BEFORE we flipped the flag (it would
  have guaranteed a daily breach). The pipeline is sacred (`main.py` sacred=True); MAD is
  non-sacred (`mad_runner.py:467` sacred=False) -- that asymmetry caused the 12:22 block.
- **CAVEAT:** 85K safe / 100K hard are PROJECT-INTERNAL ceilings (`TPD_SAFE_CEILING` /
  `TPD_HARD_LIMIT` in quota_guard.py:19-20), NOT confirmed = Groq's real TPD. The 429 probe
  established TPM=12K only, not TPD.

**The answer James designed (see brief):** two-account MAD split -- MAD cron #1 on Groq
account A, MAD cron #2 on account B (separate Gmails = separate 100K pools). Removes the
constraint at root. NOT YET BUILT.

---

## 8. KNOWN SIDE-NOISE (not addressed, low priority)

- **Source health drifting down:** Mission Control showed 24/47 healthy (was 22/49). 403
  wave grew: Stimson, Amnesty, and now Myanmar Now all 403-failing. Alert-noise only for now,
  but the count is trending down -- if it keeps dropping, source diversity (and report
  quality) eventually suffers. Separate from MAD entirely.
- **Claude Code "auto-update failed: claude.exe in use"** -- harmless; close the extra
  VS Code/Claude Code session. Was the suspected cause of an earlier silent push stall;
  foreground pushes worked cleanly all session once flagged.

---

## 9. DISCIPLINE MOMENTS -- WHERE VERIFY-FIRST SAVED US (for the next Claude to internalize)

1. **The leaky gate** (Commit 1) -- mechanism guess right (429->neutral), but the protection
   guess ("the gate protects the data") was wrong; the gate leaked for months. Caught only
   by BEV. Born the rule: protections guilty until BEV'd.
2. **The 429 design** (Commit 2) -- the docs said honor `retry-after`; the LIVE PROBE proved
   `x-ratelimit-reset-tokens` is the binding signal. Designing from the doc would have built
   the wrong wait.
3. **Sacred-MAD** -- looked like the clean safety net; the BEV proved it would breach the 100K
   hard cap (2 sacred MADs ~96-130K). Caught BEFORE the flag was flipped.
4. **The :17 cron offset** -- Claude's offhand number would have pushed MAD past the protection
   window edge; propose-first + the protection-window BEV produced :13/:43/:58 instead.
5. **Opus 4.8 misread a unified diff once this session** -- caught only by a ground-truth
   re-read. Confirms Treasure 1: Claude-verified-this-session is ~90-95%, never 100%.

**The meta-lesson, stated for the next Claude:** your mechanism guesses are usually right;
your protection / blast-radius / "already-handled" guesses are usually too optimistic. BEV
the protection, not just the mechanism. Tag every claim verified-vs-assumed.
