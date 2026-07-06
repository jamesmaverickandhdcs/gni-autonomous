# GNI Rules -- new/affirmed in S47 (append to registry)

> Assign GNI-R-NNN numbers per the live registry's next-available sequence. Renumber on commit.

## R-S47-1 -- Account isolation needs a DATA dimension, not just separate keys
Separate Groq accounts (separate Gmail = separate 100K pool) only deliver isolation if the
usage-tracking layer is ACCOUNT-AWARE. `groq_daily_usage` summed all rows unfiltered, so two
accounts would still share one computed bucket. Fix shipped: `account` column (default
'morning') + `.eq('account', account)` filter in `get_today_usage` + account stamped on every
`log_usage`. Pattern: the LENS-010 trap recurs one layer up -- separate pools are useless if
the GUARD can't tell them apart. (Born from S47 two-account split, commit 668abeb.)

## R-S47-2 -- Per-cron secret injection via github.event.schedule
Two `cron:` lines feeding one job can inject different secrets by branching on
`github.event.schedule` (the RAW UTC cron string, e.g. `'43 10 * * *'`). Ternary form:
`${{ github.event.schedule == '43 10 * * *' && secrets.GROQ_MAD_EVENING || secrets.GROQ_API_KEY }}`.
NOTE: workflow_dispatch (manual) runs have an EMPTY schedule -> fall through to the default
(morning) branch. Manual runs therefore cannot test the evening account; the real scheduled
cron is the only true test. "Evening" lives in the secret NAME and operator's mental model;
the branch literal is UTC.

## R-S47-3 -- A success PRINT is not proof; verify bytes (paste-corruption corollary)
A heredoc/paste can be mangled by bracketed paste such that the terminal ECHO is garbled yet
the script still prints its "OK" line (the print survives the mash). The OK is then a lie.
After ANY paste-heavy patch, verify the actual file bytes (grep -n the expected anchors),
never trust the success message. This is the existence != correctness rule applied to tooling
output. (Born from S47 Patch-2: garbled echo, printed "Patch 2 OK", greps proved bytes were
actually correct -- corruption was display-only, but we could not have known without checking.)
Mitigation: `printf '\e[?2004l'` before paste-heavy work; prefer ship-to-file over heredoc
(LR-078); single-line git commit messages to avoid multi-line continuation traps.

## R-S47-4 -- GHA scheduled crons drift hours / occasionally skip -- "missing != broken"
GitHub Actions delays scheduled workflows under load (minutes to HOURS), worse right after
pushes, and can skip entirely. A scheduled cron firing late, or a given day's run being
event-triggered (workflow_dispatch/heartbeat) instead of schedule-timed, is NORMAL and
documented since March. Before treating a missing/late scheduled run as a fault: (a) check the
Actions tab for a disabled banner (auto-disable after repeated failures/inactivity is the
real failure mode), (b) confirm the workflow file schedule is intact, (c) otherwise WAIT.
Do not escalate drift to diagnosis. (Affirmed S47 -- James corrected this twice; it recurs
because the symptom looks alarming. Evening cron `43 10` fired ~13:29 UTC = ~2h46m drift = fine.)

## R-S47-5 -- MAD is depth-starved, not article-starved (S48 design axiom)
`_build_news_context` already feeds each agent UP TO 60 articles (15 per-pillar x 4 pillars).
The lever for MAD reasoning quality is NOT article COUNT -- it is per-article DEPTH
(`summary[:100]` -> richer) and reasoning length (R1/R2 `max_tokens=350`). Articles inject as
`[{source}] {title[:80]} (score) -- {summary[:100]}` ~190 chars each. Raising the count past
60 costs the most tokens for the least quality (diminishing returns on headlines) and risks
the ceiling. Spend the ~25K headroom (real run ~55K vs 80K target) on depth+reasoning, not breadth.
(Born from S47 Claude-Code measurement of mad_protocol.py.)

## AFFIRMED (existing rules that proved themselves again in S47)
- R-S46-3 / Trust-tag: files read this session ~90-95%; structure-measured-but-text-unread
  ~50-60%; unread files ~30-40%. The mad_protocol PROMPT TEXT is unread -- treat as a lead.
- R-S46-6 governor owns 429s: survived 429 + two transient 503s live this session (52538 run).
- LENS-010: separate KEYS on same account share the pool; only separate ACCOUNTS isolate.
- LR-078 ship-to-file over heredoc; LR-101 ASCII anchors -- both bit/saved us in Patch 2.
- W2 py_compile before commit; ls-remote verify after push (never trust "pushed").
- Existing "condense-first" pattern (Myanmar P1->P2: summarize each, then bundle) is a PROVEN
  in-codebase pattern available to transplant into MAD for S48 Option B.
