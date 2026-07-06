# GNI S47 -- Next-Session Brief

**Written at S46 close, 2026-06-21, for the next session (also Claude, but WITHOUT this
session's working context).**

> Read this FIRST in S47. Then read `S46_Session_Audit.md` for full detail. Then -- per
> Treasure 2 (model-change re-audit) -- re-read the actual MAD code with fresh eyes before
> touching anything; do not trust this brief's code claims at 100%, trust them as leads
> (~40-50%) and verify against the live files. The operator (James) is the continuity; you
> are fresh analysis; the code + registry is the shared memory. Say "assumed, not verified"
> and let James aim BEV at the soft spots.

---

## WHERE WE ARE (one paragraph)

S46 shipped FIVE commits to origin/main (all `git ls-remote`-verified):
`460ce84` false-neutral integrity, `c40a5c2` rate governor (production-proven),
`bb280a4` MAD redefinition, `ef3f9bf` adaptive-0-token, `b27474e` cron drift-fix. MAD now
survives 429 storms (governor waits the real ~56s token-reset window), can't emit fabricated
neutrals (typed `mad_arb_failed` flag), debates on a senior G+T+F hidden-pattern foundation
with equal-rank insight-developer consultants (deference bug killed), and adaptive no longer
pollutes the Groq budget with phantom tokens. Nothing is half-built. Two real threads remain
open (below).

---

## TOP PRIORITY S47 -- TWO-ACCOUNT MAD SPLIT (James's design)

**This is the answer to the open "does 2xMAD fit the budget?" problem. Do this first.**

**Idea (simple + elegant):** point MAD cron #1 (02:43 UTC) at Groq ACCOUNT A and MAD cron #2
(10:43 UTC) at Groq ACCOUNT B (separate Gmails = separate 100K TPD pools). Each daily MAD
(~48-65K) then draws on its OWN dedicated ceiling instead of two MADs sharing one. The budget
constraint DISSOLVES. Cleaner than all alternatives (correcting the stale estimate / trimming
prompts / sacred-MAD which is unsafe).

**MAKE-OR-BREAK CHECKS -- all must be BEV'd, none assumed:**
1. **TRUE ACCOUNT ISOLATION** -- account B must be a genuinely separate Groq account (different
   Gmail) with its own 100K TPD. The LENS-010 trap: a separate KEY on the SAME account shares
   the pool = useless. This exact trap bit `GROQ_API_KEY_2` in S46 (removed). Confirm with
   James that account B is a real separate account.
2. **PER-CRON KEY INJECTION** -- both MAD crons are two `cron:` lines in the SAME `gni_mad.yml`
   feeding the same job. Need the workflow to branch on `github.event.schedule` (`43 2` ->
   key A, `43 10` -> key B) to inject a different secret per cron. BEV how `gni_mad.yml` sets
   `GROQ_API_KEY` today.
3. **QUOTA-GUARD PER-ACCOUNT AWARENESS** (the REAL work) -- `quota_guard` logs all usage to one
   `groq_daily_usage` table summed together. If MAD-A and MAD-B both log there summed, the
   guard falsely thinks they share a pool and may block MAD #2. The guard needs an ACCOUNT
   DIMENSION so it checks the right account's bucket per run.

**Work split:** TRIVIAL = the per-cron key branch. REAL = make `quota_guard` account-aware.

**Sequence:** BEV `gni_mad.yml` key-injection + `quota_guard` usage-tracking -> propose ->
James decides -> dry-run -> commit -> `ls-remote` verify. Full gated arc, fresh session.

---

## PREREQUISITE NUMBER (get this early -- it gates several decisions)

**Re-measure REAL MAD tokens/run live** from `groq_daily_usage WHERE pipeline='gni_mad'` for
the post-Commit-3 runs. The only figure on record (48,491) PREDATES Commit 3's prompt
enlargement. This single number:
- confirms each account in the two-account split has headroom,
- tells whether 2xMAD genuinely exceeds the budget (if ~110-130K, it's a real structural
  fact, not just a stale estimate),
- is the first Treasure-3 assertion to write (see below).

---

## SECOND PRIORITY -- APPLY FOUR TREASURES TO GNI (James wants this, full)

The Four Treasures (memory #12-15; Lens-transfer docx already built) applied to GNI in full
is a MULTI-SESSION arc. Highest-value single piece to start with:

**Treasure 3 -- assertion sweep.** Convert GNI's load-bearing ASSUMPTIONS into runtime
ASSERTIONS that shout on violation. **Live first target:** the stale
`PIPELINE_COSTS['gni_mad'] = 7433` in `quota_guard.py` -- it's been wrong by ~6.5x ALL SESSION,
silently masking the real MAD cost. Make it an assertion that FIRES when the real metered MAD
cost diverges from the estimate. That single assertion would have surfaced the whole
quota problem weeks earlier. This is the leaky-gate pattern, and Treasure 3 is its cure.

Other treasures applied to GNI (later sessions): T1 = tag every guard "last verified by which
model, when"; T2 = fresh-eyes re-audit of the parts no current model has read (pipeline,
funnel, GPVS verifier, entity graph); T4 = mostly in place (memory + commit-hash tracking).

---

## WATCH ITEMS (verification, not building -- do when crons land)

1. **Read the Commit-3 debate transcript fresh** -- this is the REAL quality test, not yet
   done. Confirm: agents argue at senior G+T+F hidden-pattern level; consultants DEVELOP
   (not correct); NO hallucinated facts; verdict stays calibrated. If something reads off ->
   tuning for a follow-up, NOT a failure (Commit 3 was a big prompt change to the heart of MAD;
   real-model behavior is the final exam).
2. **Confirm adaptive now logs 0 tokens** in production (Commit 4 working) -- check
   `groq_daily_usage` for `gni_adaptive` rows showing tokens_used=0.
3. **Confirm new cron times** -- pipeline/MAD/graph now fire at 02:13/10:13, 02:43/10:43,
   02:58/10:58 UTC; check whether GHA drift is reduced (Commit 5).

---

## PENDING OFFERS (James can pick up anytime)

- **Onboarding prompt set** (continuity-leak cure) -- a complete prompt set so any fresh
  session boots into full context fast. Not yet drafted.
- **Transfer Four Treasures to Lens** -- docx `GNI_to_Lens_Four_Treasures.docx` is BUILT.
  James uploads it in his next LENS session -> append to `lens-DOC-002` as LR entries.
  (Memory edits are project-scoped; this lives in Lens's own registry.)

---

## OPERATOR CONTRACT REMINDERS (apply with James from message 1)

- Warm informal tone ("my buddy") + strict engineering rigor. Cut preamble; answer first;
  justify only if asked. Lettered options A/B/C/D with honest lean stated.
- **"BEV" = HARD STOP**, diagnose-only until full state shown. Hard gates in order:
  BIRD-EYE -> DEEP ANALYSIS -> SWOT (if architectural) -> PROPOSE -> JAMES DECIDES -> BUILD+TEST.
- **"your call my buddy"** = decide and state the lean with full reasoning (he trusts the
  analysis; own the call).
- **Short message after a long Claude response** = pause signal, re-examine.
- **James never runs anything without discussing first** -- Claude Code's dimmed pre-typed
  suggestions are SUGGESTIONS, not completed actions. Never assume a dimmed line was executed.
- One-question rule: ask only the single most important question.
- Pause-over-push past deep-work mark (LR-077).

## WORKFLOW REMINDERS

- GNI push: standard `git push origin main`, then ALWAYS `git ls-remote origin main` to
  confirm the hash (an earlier push stalled silently on background credentials -- verify
  against the remote, never trust the "pushed" message).
- Lens push (if in Lens): `git push https://fintelplan@github.com/fintelplan/project-lens.git main`
- `py_compile` before every commit (W2). Dry-run harnesses are offline/hermetic
  (`os.environ.setdefault('GROQ_API_KEY','test-dummy-key')` + `GITHUB_ACTIONS='true'` +
  monkeypatched client/sleep).
- LR-101: patch anchors must be PURE ASCII -- no box-drawing, arrows, emoji, non-ASCII.
- LR-078: ship-to-file patch over bash heredoc (heredocs corrupt with bracketed paste).
- Close the extra VS Code/Claude Code session if a push prompts for credentials.

## TRUST CALIBRATION FOR S47 (Treasure 1 + 2)

A version/session change partially resets prior verifications. This brief's code claims are
LEADS (~40-50%), not ground truth. Re-read the live files before resuming. Claude-verified-
this-session-in-detail ~90-95% (never 100%); unverified estimates ~50-60%; earlier-model
unread code ~30-40%. Guards don't get tenure.
