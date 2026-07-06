# GNI S47 -- Session Audit (2026-06-23)

**Model used:** Opus 4.8 (chat interface, NOT Claude Code for this session's reasoning;
Claude Code used as a delegated read-only investigator near the end).
**Branch:** main | **HEAD at close:** `668abeb` (verified on origin via ls-remote).
**One-line:** Built, shipped, and PRODUCTION-PROVED the two-account MAD split; then deeply
analysed the MAD reasoning-quality / article-budget question and banked the S48 design.

---

## THE HEADLINE

S46 closed with the two-account MAD split as TOP PRIORITY (James's design) and one hard
prerequisite: measure the real post-Commit-3 MAD cost. S47 did the prerequisite, built the
split, and saw it run live on BOTH accounts the same UTC day. The budget constraint that
PENDING'd a real afternoon report on 2026-06-22 is now dissolved at the root.

---

## CHRONOLOGY OF MOVES (what we did, in order)

### 1. Prerequisite measured -- real MAD cost
- The stale estimate `PIPELINE_COSTS['gni_mad']=7433` was ~8.5x too low.
- Real metered MAD this session: **63,005 / 58,221 / 52,538 tokens** over 20-21 Groq calls.
- Confirmed: 2xMAD/day on ONE account = ~126K MAD alone, over the 100K hard cap. The split
  was not just elegant -- it was structurally necessary. PROVEN, not assumed.

### 2. BEV of the three make-or-break checks (read live files, not memory)
Files read in full this session (ground truth, ~90-95% trust):
- `gni_mad.yml` -- key injected at step-level `env: GROQ_API_KEY`. Cron `43 2` + `43 10` UTC
  CONFIRMED matching the doc (my earlier S46-doc-vs-runs worry was a FALSE ALARM -- the
  off-schedule runs were workflow_dispatch/heartbeat, not the scheduled crons).
- `quota_guard.py` -- `get_today_usage()` summed ALL rows unfiltered (LENS-010 shape, no
  account dimension). `check_quota('gni_mad', sacred=False)` -> non-sacred path ->
  `needed = 7433 + 15000 = 22433`. THIS (not the stale number alone) is why the 15:37
  block fired: the gate checks against a stale estimate, runs the real ~58-63K anyway, and
  only catches the overrun by accident on the day's 2nd run.
- `mad_runner.py` -- calls `check_quota` as NON-sacred; account is determined ENTIRELY by
  which `GROQ_API_KEY` the workflow injects (mad_protocol reads env, never names an account).
  So per-cron key injection IS the account switch.

### 3. CORRECTION I made mid-session (logged honestly)
I initially said the stale 7433 was "blocking runs." After reading `mad_runner.py` I
corrected: the sacred branch ignores pipeline_cost; MAD hits the non-sacred path; the block
is the stale-estimate-vs-real-cost gap, not the number in isolation. Reset-to-zero applied.

### 4. James's L2 decisions (gated, James decided)
- Q1: manual workflow_dispatch uses the MORNING key (accepted; real 10:43 cron is the test).
- Q2: column `account`, values **'morning' / 'evening'** (NOT 'primary'/'evening').
- Account B = `GROQ_MAD_EVENING`, genuinely separate Gmail account (LENS-010 trap cleared).

### 5. THE BUILD (three files, surgical anchored patches)
Shipped as `668abeb` (commit msg single-line to dodge bracketed-paste; em-dash -> `--`):
- **gni_mad.yml**: `GROQ_API_KEY` line became a ternary on `github.event.schedule == '43 10 * * *'`
  -> evening cron uses `GROQ_MAD_EVENING`, else `GROQ_API_KEY`. Added `GNI_MAD_ACCOUNT` label
  (`'evening'` on the 10:43 cron, else `'morning'`).
- **quota_guard.py**: `get_today_usage(client, account='morning')` + `.eq('account', account)`
  filter; `log_usage(..., account='morning')` + `'account': account` in insert;
  `check_quota(pipeline, sacred=False, account='morning')` passes account through.
- **mad_runner.py**: reads `GNI_MAD_ACCOUNT` env once, threads into `check_quota` + `log_usage`.

### 6. SCHEMA (L2, James ran in Supabase)
`ALTER TABLE groq_daily_usage ADD COLUMN account text NOT NULL DEFAULT 'morning';`
Default 'morning' = every existing/historical row backfills to morning automatically (no
backfill script, nothing breaks). Confirmed via information_schema: `account | text |
'morning'::text | NO`.

### 7. THE PATCH-2 PASTE-CORRUPTION CATCH (a Treasure-3 moment)
The `quota_guard.py` heredoc patch's terminal echo showed garbled bytes (`PYEOF(...)...write(s)`)
but printed "Patch 2 OK". I REFUSED the OK print and demanded grep verification. Five greps
proved the bytes were actually correct -- the corruption was DISPLAY-ONLY. Lesson held:
existence of a success message != correctness. Verify ground truth, not the checkmark.

### 8. DRY-RUN (offline, hermetic, ship-to-file not heredoc)
`dryrun_two_account_split.py` (fake in-memory Supabase, monkeypatched client) proved:
morning bucket 69180, evening bucket 0 (isolated); evening ALLOWED on fresh pool while
morning BLOCKED at 69180 (reproduced the real 15:37 block exactly); no leak either direction.
DRY-RUN PASSED before any push.

### 9. PUSH + VERIFY
`git push origin main` -> `git ls-remote origin main` =
`668abeb8deddc9c67547529e6094dd9eb7f525f6`. Hash confirmed ON ORIGIN (never trust "pushed").
Pre-commit hook fired (key-safety + GNI-R-233 banner), passed "No .env files staged".

### 10. LIVE PROOF -- BOTH ACCOUNTS, SAME UTC DAY (2026-06-23)
- Morning dispatch/heartbeat MAD ~06:34 UTC: `MAD account: morning`, logged 58,221 to
  `account='morning'`. Quality 88.3%, verdict neutral 0.62.
- Evening MAD ~13:29 UTC (10:43 cron, GHA-drifted): `MAD account: evening`,
  **`Used today: 0 | Headroom: 85000`** despite morning account already at ~64K SAME DAY.
  Logged 52,538 to `account='evening'`. Quality 93.3%, verdict neutral 0.67.
- groq_daily_usage confirmed: morning rows (adaptive 0, pipeline 6175, mad 58221) +
  evening row (mad 52538), fully isolated. **SPLIT PROVEN END-TO-END IN PRODUCTION.**

### 11. GHA DRIFT FINDING (re-confirmed from past records, James corrected me TWICE)
Scheduled crons routinely fire late (sometimes hours), occasionally skip, never "missing =
broken" by default -- documented since March (known GitHub limitation, worsened by recent
pushes). I twice escalated drift to "let's diagnose"; James correctly pointed to our own
records. The evening cron landing ~2h46m late (10:43 cron firing 13:29) is NORMAL drift,
not a fault. The yml schedule is correct; runs are event/drift-timed on top of it.

### 12. WATCH ITEMS CLEARED THIS SESSION
- Commit-3 transcript read fresh: consultants DEVELOP not correct, no hallucination (Vance
  correct, not Harris), Swan pulls real weak signals (Qatar LNG / Myanmar-700 / Nvidia-water).
  bb280a4 PROVEN.
- Adaptive logs 0 Groq tokens: confirmed (`gni_adaptive | 0` row). Commit 4 (ef3f9bf) PROVEN.
- New cron times: yml confirmed `43 2` / `43 10`.

### 13. S48 ANALYSIS (deep, grounded -- the next session's opener)
Delegated a READ-ONLY investigation of `mad_protocol.py` to Claude Code. Measured facts:
- Each agent already receives UP TO 60 articles (15 per-pillar x 4 pillars), as
  `title[:80] + summary[:100]` -- i.e. ~60 ONE-LINE headlines, ~190 chars (~40-55 tok) each.
- Black Swan gets the weak pool (same 60 cap, ASC sort). Bull/Bear/Ostrich/Arb get scored pool.
- System prompts: SENIOR_FOUNDATION ~277 tok (in all 11), agents ~670-749 tok each,
  consultants ~660-690, ARB_FINAL ~1042.
- max_tokens: R1/R2 agents 350, consultants 250, R3 agents 600, Arbitrator 600.
- 21 calls exactly (12 agent + 8 consultant [R1+R2 only] + 1 arb). Metering separates
  prompt/completion/total/calls; counts retries+guardian-rejects (real billed cost).
**KEY INSIGHT:** MAD is NOT article-starved (already 60/agent). It's DEPTH-starved -- agents
reason over 60 headlines, not 60 summaries. The lever is depth-per-article + reasoning-length,
NOT article count. More articles past 60 = most tokens for least quality (diminishing returns)
and risks the ceiling.

---

## WHAT WORKED (keep doing)
- Full gated arc held: BEV -> read live files -> propose-to-scratch -> James decides ->
  build -> dry-run -> push -> ls-remote. Zero regressions.
- Surgical anchored patches (assert anchor unique BEFORE writing) caught nothing-broke even
  when terminal echo lied.
- Delegating the complex read-only measurement to Claude Code worked cleanly (it mocked
  imports in a scratchpad, touched no project files, returned exact numbers).
- James corrected me 3x (stale-7433 framing; GHA drift x2). Each time: reset, re-grounded.

## TRUST-CALIBRATION NOTES FOR NEXT CLAUDE
- Files I READ THIS SESSION in detail (~90-95%): gni_mad.yml, quota_guard.py, mad_runner.py,
  and (via Claude Code) the measured structure of mad_protocol.py.
- Files I have NOT read this session (~30-40%): the actual prompt TEXT of mad_protocol.py
  (only its sizes/structure measured), the funnel, GPVS, entity graph. Re-read before editing.
- The S48 token math is grounded in Claude Code's measurements + 3 real metered runs = solid.
