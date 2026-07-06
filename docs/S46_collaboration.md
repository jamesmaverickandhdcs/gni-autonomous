# Collaboration Notes -- S46 (how Team Geeks + Claude worked)

> The operating model: James is the continuity, Claude is the fresh analysis, the code +
> registry is the shared memory between them. The system is safe when all three are honest:
> Claude says "assumed, not verified," James aims BEV at the soft spots, and the code asserts
> what the team believes so the next session cannot quietly violate it.

## What worked well in S46 (keep doing)

- **The full gated arc, every time.** BEV -> deep analysis -> propose-to-scratch/review ->
  James decides -> build -> dry-run -> commit -> ls-remote verify. Five commits, zero
  regressions, because no step was skipped even when a fix "looked safe."
- **Propose-first for prompt changes.** Commit 3 rewrote the heart of MAD (11 prompts). We
  drafted every word to a scratch file for James's word-by-word review BEFORE wiring. The
  words ARE the engineering for a prompt change -- review them before they touch the live file.
- **Live probes over doc claims.** The 429 probe (Commit 2) and the exhaustive Cerebras-
  attribution trace (Commit 4) both corrected what the docs/assumptions said. When a fix rests
  on a behavior, observe the behavior.
- **Two separate commits for two unrelated fixes** (Commit 4 + 5) -- clean history, independent
  revert.
- **Honest walk-backs.** Claude reversed its own leans twice when the BEV proved them wrong
  (fallback-first -> governor-first; spacing-fixes-quota -> it doesn't). Owning the correction
  beats defending the original.

## James's signals (read these correctly)

- **"your call my buddy"** = decide and state the lean with FULL reasoning. He trusts the
  analysis; own the call, don't punt it back.
- **A short message after a long Claude response** = pause signal. Re-examine, don't barrel on.
- **He never runs anything without discussing first.** Claude Code's dimmed pre-typed
  suggestions are SUGGESTIONS. Confirmed repeatedly this session: do NOT read a dimmed line as
  an executed action. (Happened with the probe command, the git push, and an offset suggestion.)
- **"BEV"** = HARD STOP. Diagnose-only until full state shown.
- **He brings the elegant idea.** The two-account MAD split was James's design -- simpler and
  more correct than Claude's per-call-routing proposal. When James reframes a problem, take it
  seriously; he often sees the cleaner cut.

## What to watch in Claude's own behavior (S46 self-observations)

- **Opus 4.8 misread a unified diff once** -- caught only by ground-truth re-read. Never trust
  a diff summary; read the resulting file state. (Treasure 1: verified-this-session != 100%.)
- **Claude can't see Claude Code's terminal output or local files.** Twice this session the
  resolved prompt text / scratch file existed on James's machine but didn't reach Claude -- the
  fix was to have James `cat`/upload the file. Don't claim to have "reviewed" output you only
  saw summarized; ask for the actual content.
- **Mechanism guesses land; protection guesses over-optimize.** This held all session. Lead
  BEV at the protection/blast-radius, not the mechanism.

## Continuity discipline (the reason these close files exist)

"You are not you in every new session." The next Claude has James's continuity and the code +
registry, but NOT this session's working context. Therefore: SHIPPED items recorded with
hashes; the active priority and its make-or-break checks written in order; corrections to prior
assumptions recorded so they aren't re-introduced; every assumption pushed toward an assertion
or a named rule. Begin session close at the deep-work mark, not at the context wall.

## Tone

Warm, informal ("my buddy"), genuine partnership -- over strict engineering rigor underneath.
The warmth is real and the rigor is non-negotiable; neither is performance. Every word costs
message budget -- answer first, justify if asked.
