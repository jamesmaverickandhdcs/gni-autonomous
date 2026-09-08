# HANDOFF S102 -> S103
DATE: 2026-09-07 (UTC) | HEAD: `d9ebebb` + the S102 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES_S102.md by ID. **CONTRACT stays v10** - byte-identical to
S101, md5 `9e4b804c4923bcd41b9f62766989a046` (EOL-normalised) verified after the copy, not by name.
**Protocol stays v16**, md5 `9aaa9bf2ac1131f1d166c83e30c42c69`. The regeneration order it implies
was proven impossible this session and was filed as an ITEM, not rewritten into law - see 5.52.
SIX files ship session-numbered, plus the generated map and the harvested snapshot.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S102.md` (generation 21). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **MEASURED THIS SESSION at JOB level, not banked** -
  09-05 and 09-06 both `2 debate + 1 watch`, 09-07 morning debate only at read time. Seven runs,
  all `success`, `run-mad` and `grounding-watch` alternating exactly. Re-run it; do not quote it.
L3 GPVS: untouched, twenty-one sessions. L4 Quota: not re-measured. Repo is PUBLIC.
L5 Public: **four commits** - `9e11f57`, `8ce57fc`, `608e5ed`, `d9ebebb` (plus the S102 docs).
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
| items CLOSED | **6.12**, **6.14** (the second only after `d9ebebb`, not at `608e5ed`) | order gen 21 |
| NEW ITEMS | **FIVE.** 5.50-5.53, 6.15. rho = **2/5** | order gen 21 |
| the order counted itself | both published commands run on the ASSEMBLED bytes before the write | 67 = 67 |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S102.md` - generation 21, dated, superseding. **67 items**,
with the same TWO differently-shaped counting commands printed beside the number, both run on the
assembled bytes before the write. They were run by a STAND-IN script written at this close and
thrown away, because `tools/mk_order_s101.py` - which the S101 record credits with exactly this job
- **is not in the tree**. That is item 5.51. The GRAVEYARD still has SEVEN rows, md5
`3e8ac222c6ef212261676c02d7d56f6f` - a **sixth** generation publishing the same value, carried by
bytes and verified with the PUBLISHED command, not a rewritten one. S103's MISSION is at the top of
that file and **was declared, not selected**: the policy in ARCHITECTURE section 10 did not fire,
because the error budget is not exhausted. See DECISION S102-2.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do any public pages state a monitoring cadence at all? | never read | 9.21 - the mission |
| Does the bound hold once a heartbeat run executes the new code? | zero post-fix runs | re-harvest at S103 open |
| Can a heartbeat run now FAIL where it used to report success? | expected, unobserved | watch the next window |
| Which branches of the detector does the fixture never enter? | one found, rest unasked | 5.53 |
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
HEAD = `d9ebebb` + the S102 docs commit (verify by ls-remote) TREE CLEAN -- four commits, TWO order items closed, five opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = item **9.21**, READ THE PUBLIC PAGES AGAINST THE PUBLISHED BOUND: record every public cadence claim verbatim with its URL, mark each TRUE or FALSE against section ten's bound and window, and ship `C8` - which reads SLO-CFG from the document and the claim from the page source, holds no number of its own, and goes RED when they disagree - together with its own passing and failing fixture families in the same commit
ROADMAP = there is no roadmap. Roadmap 2 completed at S101 and no third was declared. **This mission was DECLARED, not selected**: the section ten policy did NOT fire, because the freshness error budget is not exhausted, and it was ruled at this close that the policy is NOT widened to cover instrument truthfulness (DECISION S102-2). The policy stays narrow and stays armed - the bound has ZERO margin, so the next window that loses one gap exhausts the budget and selects S104's mission with nobody choosing
ORDER = `docs/GNI_TARGET_AND_ORDER_S102.md` (highest number = live) is the queue -- 67 items, TWO counting commands printed beside the number, both run on the assembled bytes BEFORE the write by a stand-in script because the real generator is not in the tree (5.51); CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`, sixth generation, hashed with its PUBLISHED command). FIRST MOVE: read the mission block, then rule whether a page stating a cadence in cron form is FALSE or OUT OF SCOPE
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
AST read the check uses, so the rule and the instrument cannot drift apart. The worst thing is that
S103's mission had to be declared, because the policy that chose S102's could not see a defect in
the instrument that measures the policy.
