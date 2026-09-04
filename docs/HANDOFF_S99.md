# HANDOFF S99 -> S100
DATE: 2026-09-04 | HEAD: `2bfef91` + the S99 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S99-3; every rule carries
a **CHECKABLE** marker). **CONTRACT stays v10** - byte-identical to S96, nothing changed.
**Protocol is now v14** (PART D step 4: separate the MAD debate from the watch at JOB level).
SIX files ship session-numbered, plus the generated map.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S99.md` (generation 18). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **PERISHABLE - do not quote, run it** (R-S98-2);
  the daily unit is 2 debate + 1 watch. Separate them at JOB level, not by log grep:
  `gh run list --workflow=gni_mad.yml --limit 20 --json databaseId,createdAt,conclusion`
  then `gh run view <id> --json jobs` - debate = `run-mad success`, watch = the reverse.
  Ids already read: `33768475533`, `33770071442`, `33727779523`.
L3 GPVS: untouched, eighteen sessions. L4 Quota: not re-measured.
L5 Public: **one commit** - `2bfef91` (plus the S99 docs commit).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, eight generations.
SCHEDULE: **declared unchanged, DELIVERY MEASURED - see item 6.11.** PLATFORM: 9 workflows.
SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2). Target: TRUTHFULNESS OF OUTPUT, unchanged.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | ARCHITECTURE section 6 RUNTIME VIEW, generated | `2bfef91` |
| the tool | `tools/gni_runtime.py`, 692 lines, harvest/render split | 23 self-counted probes |
| byte-identity | two renders 2s apart, unchanged tree | md5 `fb6e3f1e...` twice |
| it moves | one run removed from the snapshot | 5 published figures changed |
| CI | job level, this exact SHA | run `33851242047`, both jobs green |
| **the finding** | the two 30-min crons deliver **282 and 292 of 768** declared slots | section 6.1 |
| **the cliff** | 18 slots on Aug 26 -> 3 on Aug 27; BOTH workflows, no commits in the gap | runs-per-day |
| the control arm | all five low-frequency crons: **100%**, every day, 16 days | section 6.1 |
| the band | derived **744 min (12.4 h)** - above every band R-S87-6 records | section 6.2 |
| the rejected measure | nearest-slot reads a 365-min lag as **5 min** | probed every run |
| 6.8 ruled OUT | standdown = ~17 slots per 48h against 66 unexplained, and it skips CHECKS | arithmetic |
| section 7 fails | `gni_state.py` renders a clock into its own stamp | `06:14:00Z` vs `:04Z` |
| **the detector bit** | C1 FAILED this close's own draft - two cited rule ids are unregistered | pre-commit run |
| NEW ITEMS | **SEVEN.** 5.33 5.34 5.35 5.36 5.37 6.10 6.11. rho = **0/7**, nothing closed | order gen 18 |
| RULES | `R-S99-1..3` + amendments to R-S98-6, R-S87-6 (fourth), R-S84-4 | rules appendix |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S99.md` - generation 18, dated, superseding. **53 items**,
with TWO differently-shaped counting commands printed beside the number. They DISAGREED at 52/56
on the first assembly - four bare decimals had entered the prose - and the prose was rewritten
rather than the command weakened. The count then moved 52 -> 53 when C1 failed the draft and
item 5.37 was opened; both commands were re-run on the FINISHED file, not on the draft. **The GRAVEYARD still has SEVEN rows**, copied by bytes and
verified against generation 17's md5 before the file was written AND again inside it. S100's
MISSION is at the top of that file, with the one item ranked above it for James to rule.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| WHY the 30-minute crons lost ~86% of slots | measured, uncaused | 6.11 - and there may be no lever |
| Did the low-frequency lateness grow over the same span? | never measured per-day | a per-day band from the snapshot |
| Does a `ctx-trim@0` run really report SUCCESS? | still unmeasured | 9.19 |
| What do 5.5, 5.6, 5.7, 5.8, 5.11, 5.12 actually SAY? | text lost before gen 16 | read `..._S95.md` or earlier |
| What do the two unregistered heartbeat rule ids SAY? | in session records only | 5.37 |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| How many of the 61 CHECKABLE survive a build? | 1 of 5 died at S95 | roadmap 2 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| `grep -c $'\r'` says six files have 0 CR bytes | the register held **1556** | `tr -cd` control probe |
| the crons are being SKIPPED; degradation was GRADUAL | gaps STRETCHED, then fell off a CLIFF | runs-per-day count |
| `tool \| tail -2; echo $?` proves the tool refuses | `$?` was **`tail`'s** exit code | re-run without a pipe |
| the flip test moved the output | `.pop()` took a run OUTSIDE the window; only the hash moved | my own grep finding nothing |
| `grep -c '1[0-9][0-9]%'` finds values over 100% | it returned 6 - **`100%` matches it** | reading the row directly |
| `spacing > max(late)` means lateness is measurable | **inverted** - it passes for the tight crons it must reject | measuring my own code first |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- FIFTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  The REGISTER alone is `i/lf w/crlf`; S99 appended in CRLF deliberately rather than convert
  1556 line endings inside a docs commit. Use `git diff -w`, and **never md5 a checked-out
  file** - hash what a tool just wrote. *Expires when 5.21 ships.*
- NEW: **`tools/gni_state.py` still has `--session` defaulting to 94.** A bare invocation writes
  `docs/GNI_ARCHITECTURE_S94.md`. Protocol step 9a sends every close past this. *Expires with 5.34.*
- NEW: **`gni_runtime.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows** or it exits on a
  cp1252 encode. The file-writing path is safe. *Expires with 5.22.*
- EXPIRED, do not carry: the macro map's bare-invocation trap (one session has now run it).

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `2bfef91` + the S99 docs commit (verify by ls-remote) TREE CLEAN -- one mission commit, zero order items closed, seven opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = ARCHITECTURE section 5 BUILDING BLOCK VIEW, GENERATED FROM THE AST by a named tool in `tools/`, byte-identical on a second run; the pattern to follow is `tools/gni_runtime.py`, NOT `tools/gni_state.py`, which renders a clock into its own output
ROADMAP = ROADMAP 2 is JAMES'S (DECISION S96-1) and is **2 of 4**: S98 detector ACHIEVED -- S99 section 6 ACHIEVED (`2bfef91`, CI run `33851242047` green at JOB level) -- S100 section 5 -- S101 SLO. Its WRITTEN COMPLETION TEST is in `GNI_ARCHITECTURE_S99.md`; row 2 now fails on SECTION 7's own account (item 5.33), not only because section 5 is missing
ORDER = `docs/GNI_TARGET_AND_ORDER_S99.md` (highest number = live) is the queue -- 53 items, TWO counting commands printed beside the number and both must agree; CARRY THE GRAVEYARD (7 rows) and verify it with the command printed under it
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1, amended S98); an instrument checks its own expectations with a control probe (R-S93-1); verification is computed BEFORE the write (R-S95-1); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches (R-S98-6, amended S99 - probe it against a case it must CATCH and one it must MISS); an instrument bounded by what it measures reports its smallest answer where the truth is largest (R-S99-1)

## 8. POINTERS (<=5 lines)
`tools/gni_runtime.py --harvest --session N` then `--session N`: exit 2 = the INSTRUMENT refused,
exit 3 = an input is missing; the snapshot is the evidence and lives in the tree. `--stdout` needs
`PYTHONIOENCODING=utf-8` on Windows. `tools/gni_rule_checks.py .` = six checks. **Protocol PART C
step 9a: regenerate the map AFTER appending rules.** Separate MAD debate from watch at JOB level
(R-S84-4 amended); a `skipped` job reports `completedAt` BEFORE `startedAt`, so exclude it from any
duration arithmetic. Never put SQL and bash in one message (R-S88-1).

## DIARY S99
The mission was a generator and it took an hour; the rest of the session was my own instruments
lying to me, six times, each one caught only because something else was measured a second way.
A grep said zero carriage returns in a file holding 1556. An exit code belonged to `tail`. A flip
test moved a hash and nothing else. A pattern hunting for values over one hundred percent matched
one hundred percent itself. And the measurability test I wrote to keep section 6 honest was
inverted: it passed for exactly the workflows it existed to reject, and I only found that because
I measured my own code before trusting it, which I had not done the five previous times. The
finding underneath all of it is the same shape: the system has been telling itself it watches
every thirty minutes, and it watches every three to seven hours, and every run said success.
The close earned one more. C1 - the citation check S98 spent a session making green - failed
this close's own draft, because I had cited two rule ids recovered from a chat transcript that
were never in the register. First time a check here has caught the session that wrote it. I
removed the citations rather than invent the ids, which is what DECISION S90-4 exists to say.
