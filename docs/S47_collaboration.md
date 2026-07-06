# Collaboration Notes -- S47 (how Team Geeks + Claude + Claude Code worked)

> Operating model unchanged: James is continuity, Claude is fresh analysis, code+registry is
> shared memory. NEW this session: Claude Code joined as a delegated executor/investigator for
> complex local work. The chat-Claude designs and reviews; Claude Code reads/measures/edits
> locally; James gates every move.

## What worked well in S47 (keep doing)

- **The full gated arc, again, zero regressions.** BEV -> read live files -> propose-to-scratch
  -> James decides -> build -> dry-run -> push -> ls-remote. One real architecture change
  (668abeb) shipped clean.
- **Delegating to Claude Code for the complex read-only measurement.** The mad_protocol.py
  token investigation was exactly right for hand-off: it mocked imports in a scratchpad,
  touched no project files, and returned exact char/token counts that turned a guess into
  arithmetic. Chat-Claude could not have measured this precisely from a paste. Pattern: design
  + review in chat, complex local execution in Claude Code, James gates the boundary.
- **Surgical anchored patches that assert before writing.** Each patch checked its anchor was
  unique BEFORE writing -- a near-miss raises and writes nothing. This safety net is WHY the
  Patch-2 display-corruption scare ended safely.
- **Verifying bytes over trusting the OK print.** The single most important behaviour this
  session. See R-S47-3.

## James's signals (read these correctly)

- **"your call"** = decide and state the lean with full reasoning. Own it.
- **Short message after a long response** = pause / re-examine.
- **He corrects with a pointer, not a lecture** -- "see past session records," "cron usually
  late." When James points at our own record, STOP and read it before defending a position.
  He was right all three times this session.
- **He brings the elegant frame.** The two-account split was his; the "depth not count" S48
  question was his framing too ("if each agent can summarize each article, output will be
  higher quality") -- which the measurement confirmed was the right lever.
- **He sequences correctly.** Insisted on seeing the evening cron prove live BEFORE designing
  S48 on top of the freed headroom. Don't build on an unconfirmed pool.

## What to watch in Claude's own behaviour (S47 self-observations)

- **I escalated GHA drift to "diagnose" TWICE before James pointed me to our records.** The
  drift symptom (missing/late scheduled run) LOOKS alarming and pattern-matches to "broken."
  It almost never is. R-S47-4 exists to stop the next Claude repeating this. Read the record
  FIRST.
- **I mis-framed the stale-7433 as "blocking" before reading the caller.** Corrected after
  reading mad_runner.py. Read the caller before concluding what a value does.
- **Chat-Claude cannot see local files or Claude Code's terminal state.** The whole cat/paste
  relay (and the paste-corruption risk) flows from this. When work is local and complex,
  delegate to Claude Code rather than relay through paste.

## On Claude Code hand-off (NEW -- how to do it well)

- Give Claude Code a SCOPED, explicit task with a clear "do NOT modify / read-only" boundary
  when investigating. It will use a scratchpad for any helper code and report back.
- For the S48 BUILD: the design/scratch-proposal + word-by-word review stays with chat-Claude
  and James; the edit+py_compile+dry-run loop is a good Claude Code job. James still gates:
  nothing runs without discussion (Claude Code's dimmed suggestions are SUGGESTIONS).

## Continuity discipline

"You are not you in every new session." Next Claude has James + code + registry + these close
docs, NOT this session's working context. So: 668abeb recorded with hash; the S48 design and
the stale-7433 fix written in priority order with their gates; every correction recorded so it
is not re-introduced (esp. GHA drift, R-S47-4). The mad_protocol PROMPT TEXT is explicitly
flagged UNREAD -- next Claude must read it fresh before S48 edits, not trust this brief's
structure summary at 100%.

## Tone

Warm, genuine partnership ("my buddy"), real engineering rigor underneath. James names the
elegant cut; Claude grounds it in evidence; Claude Code executes the complex local steps;
James decides. The warmth is real and the rigor is non-negotiable.
