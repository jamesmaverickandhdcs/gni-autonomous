# HANDOFF S102 -> S103
DATE: 2026-09-07 (UTC) | HEAD: `d9ebebb` + the S102 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES_S102.md by ID. **CONTRACT stays v10** - byte-identical to
S101, md5 `9e4b804c4923bcd41b9f62766989a046` (EOL-normalised) verified after the copy, not by name.
**Protocol stays v16**, md5 `9aaa9bf2ac1131f1d166c83e30c42c69`. The regeneration order it implies
was proven impossible this session and was filed as an ITEM, not rewritten into law - see 5.52.
SIX files ship session-numbered, plus the generated map and the harvested snapshot.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S102.md` (generation 22). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **MEASURED THIS SESSION at JOB level, not banked** -
  09-05 and 09-06 both `2 debate + 1 watch`, 09-07 morning debate only at read time. Seven runs,
  all `success`, `run-mad` and `grounding-watch` alternating exactly. Re-run it; do not quote it.
L3 GPVS: untouched, twenty-one sessions. L4 Quota: not re-measured. Repo is PUBLIC.
L5 Public: **seven commits** - `9e11f57`, `8ce57fc`, `608e5ed`, `d9ebebb`, then the close set at
  `44ca125` / `9fbd96c` / `1f85483`, plus the second regeneration. Three of those seven exist only
  because a staging step reported success while putting four documents where nothing reads them.
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, eleven generations.
SCHEDULE: **check gap p90 is 7.31 h, bound published at 8 h** (window 08-27..09-03). Every heartbeat
  run now performs its check; effective check gaps and run gaps are the same series.
PLATFORM: 9 workflows. SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2).
Target: TRUTHFULNESS OF OUTPUT, unchanged. Detector: **7 checks green**. Fixture: **18 families**.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | the standdown is gone; the bound FELL 12 h -> 8 h, derived not chosen | `9e11f57` |
| the amendment | `GNI-R-122` binds ADAPTIVE or MANUAL runs - its own purpose clause's words | RULES S102 |
| verbatim preserved | March-2026 sentence untouched; id not re-declared, so `C3` sees no duplicate | `C3` green |
| no new marker | a second `CHECKABLE:` would have moved the rule into the map's AMBIGUOUS bucket | 184 -> 184 |
| **two subject tests DIED** | neither pipeline imports groq; a text grep captures the watcher on its own `GNI-R-114` lines | AST + grep |
| the one that lived | callers of `is_protection_window` = exactly `{adaptive_pipeline.py:226}` | AST |
| `C7` stopped assuming | `heartbeat_stands_down()` asks the tree, so the bound rises again if the call returns | `9e11f57` |
| cert | families `17-standdown-absent` / `18-standdown-reinstated`, one call apart | 18/18 |
| **the fixture was blind** | 16 families never entered the window branch - the history starts at 02:00 | 5.53 |
| DoD clause 3 | fresh harvest agrees with the committed one DIGIT FOR DIGIT on the same window | `608e5ed` |
| zero margin, DISCLOSED | 4 of 40 is 10.0% - ON the budget; at 39 gaps the same four derive 10 h | 10.3 |
| items CLOSED | **6.12**, **6.14**, **5.46** - the last by RE-RUNNING a test nobody had run since S98 | order gen 22 |
| NEW ITEMS | **FIVE.** 5.50-5.53, 6.15. rho = **3/5** | order gen 22 |
| the order counted itself | both published commands run on the ASSEMBLED bytes before the write | 66 = 66 |
| **ROADMAP 2 IS 3 OF 4** | rows 2 and 3 had been quietly true for closes; the table still said 1 of 4 | ARCH 10 |
| the mission REVERSED | 9.21 -> 5.50, on a measurement, which is the only reversal the order allows | S102-4 |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S102.md` - generation 22, dated, superseding generation
21 from earlier in this same close. **66 items**,
with the same TWO differently-shaped counting commands printed beside the number, both run on the
assembled bytes before the write. They were run by a STAND-IN script written at this close and
thrown away, because `tools/mk_order_s101.py` - which the S101 record credits with exactly this job
- **is not in the tree**. That is item 5.51. The GRAVEYARD still has SEVEN rows, md5
`3e8ac222c6ef212261676c02d7d56f6f` - a **seventh** generation publishing the same value, carried by
bytes and verified with the PUBLISHED command, not a rewritten one. S103's MISSION is at the top of
that file. It was DECLARED rather than selected - the section 10 policy did not fire, because the
error budget is not exhausted (DECISION S102-2) - and then it was CHANGED, from 9.21 to 5.50, when
roadmap 2's completion test was re-run and row four turned out to be the last one standing
(DECISION S102-4). Generation 21 named 9.21 and stands in git history.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do any public pages state a monitoring cadence at all? | never read | 9.21 - top of ROOT 9, likely S104 |
| Does the bound hold once a heartbeat run executes the new code? | zero post-fix runs | re-harvest at S103 open |
| Can a heartbeat run now FAIL where it used to report success? | expected, unobserved | watch the next window |
| Which branches of the detector does the fixture never enter? | one found, rest unasked | 5.53 |
| Does closing row four CLOSE roadmap 2, given sections 5 and 6 have no staleness check? | a scope question | rule it at the S103 open |
| Why is POST suppression 29% when the windows cover 17.7% of the clock? | not separated | 5.49's sibling in 10.7 |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |
| Is `GNI-R-115`'s interval table anywhere in the tree? | searched, not found | read `adaptive_pipeline.py` |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| `608e5ed` retired item 6.14 | only SLO-CFG moved; 6.14 is section SIX's, and section six still read S99 | re-reading the item to close it, AFTER the push |
| the fixture will break under the new predicate | it cannot: its history starts at 02:00, so no run is ever in a window | running it - the prediction was wrong and became item 5.53 |
| the harvest covers ~6 days | 20 days. I divided 300 by the DECLARED cron; delivery is ~15/day, not 48 | reading the snapshot's own span |
| the +2 line offset came from the close-time rename | `git show --stat 1d3cc23` holds three files, none of them the architecture | the commit itself |
| `--stdout` would let me look without writing | it wrote the snapshot anyway | its own `WROTE` line |
| a text split on the closing heading finds the order section | it stops at an INLINE mention and returns zero of zero | running both counts before the write |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- EIGHTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  Use `git diff -w`, and **never md5 a checked-out file** - hash what a tool just wrote, or
  normalise first. Generators write LF; humans append CRLF. *Expires when 5.21 ships.*
- NEW: **the generators count the INDEX but stamp HEAD.** Running them before the mission commit
  writes the index's file list under a HEAD that predates the work. Commit first, then regenerate,
  then commit again. *Expires with 5.52.*
- NEW: **`gni_blocks` and `gni_state` splice into the LIVE architecture**, so the macro map must run
  AFTER them or its architecture stamp is stale on arrival - and `C6` will not say so.
  *Expires with 5.50.*
- NEW: **`gni_runtime.py --stdout` still WRITES the snapshot.** `--stdout` is not a dry run.
  *Expires when the flag is fixed or documented.*
- NEW: **a published checksum is its command.** The graveyard hash reproduces only with
  `sed ... | tr -d '\r' | md5sum`; a Python rewrite that drops sed's final newline gives a
  different digest and looks like corruption. *Expires never - this one is a rule waiting.*
- CARRIED: **`--limit` truncates from the OLD end.** Check whether the returned count equals the
  limit before believing the oldest day. *Expires with 5.48.*
- CARRIED: **`gni_runtime.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows.** *Expires with 5.22.*
- EXPIRED, do not carry: the S99 snapshot's disagreeing stamps. Nothing reads it now (6.14 closed).

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S102 close commit (verify by ls-remote) TREE CLEAN -- seven commits, THREE order items closed, five opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = item **5.50**, MAKE `C6` READ BOTH OF THE MACRO MAP'S INPUT LINES: loop over EVERY `INPUT ... md5` line with no hard-coded count, ship at least one fixture family that goes RED on a stale ARCHITECTURE stamp while the register stamp is fresh, replay S102's own evidence as the cert (an architecture edit with no map regeneration must go RED where it was SILENT four times), then update row four of the completion test from bytes. **This is the LAST unmet row of roadmap 2**
ROADMAP = **ROADMAP 2 IS 3 OF 4, not the 1 of 4 its own scoreboard claimed for four closes.** The completion test in `GNI_ARCHITECTURE` was re-run at this close for the first time since S98: row 1 holds, row 2 holds (each generator rendered twice two seconds apart, `cmp`-identical), row 3 holds since S101, row 4 is PARTIAL and names item 5.50. That re-run is why the mission changed from 9.21 to 5.50 (DECISION S102-4) - freshness confers no priority UNLESS A MEASUREMENT SAYS SO, and one did. The section ten policy did NOT fire and was NOT widened (DECISION S102-2); it stays narrow and stays armed, because the bound has ZERO margin and the next window that loses one gap exhausts the budget and selects S104's mission with nobody choosing
ORDER = `docs/GNI_TARGET_AND_ORDER_S102.md` (highest number = live) is the queue, **generation 22** -- 66 items, TWO counting commands printed beside the number, both run on the assembled bytes BEFORE the write by a stand-in script because the real generator is not in the tree (5.51); CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`, seventh generation, hashed with its PUBLISHED command). FIRST MOVE: read the mission block, then rule whether closing row four CLOSES roadmap 2, given that the row also asks for staleness detection on sections five and six for which no check exists at all
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); an instrument checks its own expectations with a control probe (R-S93-1) built from the REAL tree's bytes (R-S100-1); verification is computed BEFORE the write (R-S95-1); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches (R-S98-6); an instrument bounded by what it measures reports its smallest answer where the truth is largest (R-S99-1); a fix is not shipped until the recipient has verified the bytes (R-S100-3)

## 8. POINTERS (<=5 lines)
`tools/gni_rule_checks.py` holds SEVEN checks. `C7` now calls `heartbeat_stands_down(root)`, which
walks `monitoring_pipeline.py` for a Call to `is_protection_window`; no call means `windows = []`
and the check gaps ARE the run gaps. `C6` still reads only the register's `INPUT` line - that is
5.50 and it is why the map must be regenerated LAST. Order that worked, four commits deep:
fix -> commit -> `gni_blocks` -> `gni_state` -> `gni_runtime` -> `gni_macro_map` -> detector ->
fixture -> commit.

## NOTE ON THIS FILE'S OWN SHAPE
S99 shipped ROADMAP and GATE in place of PART B's TRAP and FIRST MOVE; S100, S101 and now S102 have
carried that shape. FIRST MOVE is folded into the ORDER line, TRAP is section 6. Four closes is not
a deviation, and the template still says otherwise. S101 called this an unregistered rule and filed
it as 5.49's sibling; it was not ruled this close either, and saying so a second time without ruling
it is how a trap becomes a practice. **It is now older than most open order items.**

## DIARY S102
The mission was to make a watcher that reported success without checking anything actually check.
It took four commits and it worked: the published bound fell from twelve hours to eight, derived by
the check rather than chosen, and two independent harvests three days apart agree on it digit for
digit. But the mission turned out to be a special case of something larger, and the larger thing
kept appearing. The heartbeat exited zero having performed no check. `C6` reports the macro map
fresh while reading one of its two inputs. The detector's own fixture went green on a branch it had
never entered, because its synthetic history starts at two in the morning and therefore no run has
ever fallen inside a protection window. Three instruments, one disease: green on ground never
walked. I proved the second one four times in a single session, twice by accident.
Then I did it myself. I wrote in a pushed commit message that item 6.14 was retired, when I had
moved section ten's pointer and left section six reading the old snapshot. The harvester had
printed the next command on the screen and I had not run it. Nothing caught that: not a check, not
a probe, not a patch script refusing an anchor. I caught it an hour later by re-reading the item in
order to close it. Everything else that went wrong this session was caught by something the repo
built on purpose - an assertion, a fixture, a counting command run before a write - and the one
failure that reached a pushed artifact was the one where I described work instead of running it.
The best thing here is not the eight hours. It is that the amendment's subject test is now the same
AST read the check uses, so the rule and the instrument cannot drift apart.
Then the close reopened itself. After generation 21 was committed and the mission set to 9.21, one
command re-ran roadmap 2's completion test - which nobody had run since S98 - and two of its four
rows had quietly become true. The roadmap was at three of four while its own scoreboard said one of
four, and the single remaining row is closed by the very item I had just ranked second. So the
mission changed on a number, which is the one reversal the order permits, and generation 22 says
so out loud rather than quietly. It is a small thing and it is the whole point: the scoreboard was
not wrong because anyone lied to it. It was wrong because for four closes nobody asked it again.
