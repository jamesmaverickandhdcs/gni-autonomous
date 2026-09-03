# HANDOFF S96 -> S98
DATE: 2026-09-03 | HEAD: `09588b2` + the S96 docs commit (verify by ls-remote) | MODEL: Opus 5
**S97 WAS AN ADVISORY SESSION HELD IN A SEPARATE CHAT. No commits, no numbered artifacts, no
`*_S97.md` files. Its entire output is roadmap 2 and the DEGRADE-SILENT finding, both merged
into order generation 16. NOTHING FROM S97 IS MISSING - do not search for it.**
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S96-5; every rule carries
a **CHECKABLE** marker). **CONTRACT is now v10** (PHASE TRANSITION amended).
**Protocol is now v12** (PART C step 4a, ROADMAP CHECK). SIX files ship session-numbered.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S96.md` (generation 16). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **2 debate + 1 watch, UNREAD** - `33602968900`,
  `33643625612` (ARB-FIT present) and `33646366334` (absent). Measured at this close, not
  carried from the open: `gh run list --workflow=gni_mad.yml --limit 15 --json databaseId,createdAt`.
L3 GPVS: untouched, fifteen sessions. L4 Quota: not re-measured.
L5 Public: **1 commit** - `09588b2` (macro map + generator), plus the S96 docs commit.
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, highest single
  point of loss for six generations and never once the mission.
SCHEDULE: unchanged. Never quote a cron as a start time. PLATFORM: 9 workflows = 7 scheduled +
  1 push + 1 dispatch-only. SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2); nothing due.
Target: TRUTHFULNESS OF OUTPUT, **unchanged - this close ended a ROADMAP, not a target.**

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | macro map generated, X/Y/Z, source named per point, absent shown absent | `09588b2` |
| cert | flip one marker -> Z 35.8 to 35.2 + md5 moves; revert -> byte-identical | 2 runs |
| negative controls | no `docs/`, no register, renamed ROADMAP heading -> **exit 2**, nothing written | 3 runs |
| portability | `os.path.join` made Windows and Linux emit DIFFERENT bytes from ONE input | `head -25` |
| the tell | every figure in the summary line matched across platforms; only the md5 differed | R-S96-4 |
| measured Z | **57 CHECKABLE / 102 not of 159** at the S95 close - the banked 53/106 is WRONG | register grep |
| Z at S96 close | **61 / 103 of 164** after this close's five rules | map re-run |
| the map is stale | it read 159; the register now holds 164, and NOTHING turns red | item 5.26 |
| graveyard md5 | gen 15's `203d371b...` reproduces from NO span of gen 15. Fourteen tried | item 5.28 |
| register shape | SIX entry shapes; a first parser bound 103 of 159 markers to ONE rule, silently | item 5.29 |
| PHASE TRANSITION | roadmap 4/4 ACHIEVED, arc archived, roadmap 2 declared WITH a completion test | ARCHITECTURE |
| CONTRACT v10 | a declared roadmap carries its own written completion test | version log |
| Protocol v12 | PART C 4a ROADMAP CHECK. The sweep found ZERO hits - that was the finding | version log |
| NEW ITEMS | **FIVE.** 9.19 - 5.26 - 5.27 - 5.28 - 5.29. rho = **5/1** | order gen 16 |
| RULES | `R-S96-1` .. `R-S96-5`, each with a CHECKABLE marker | rules appendix |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S96.md` - generation 16, dated, superseding, and the
first PHASE-TRANSITION regeneration: every surviving item RE-CLASSIFIED under ISO/IEC 14764,
nothing inherited. **36 items**, and the counting COMMAND is printed beside the number because
S96 predicted 41 by counting lines and was wrong. **The GRAVEYARD still has SEVEN rows** and now
publishes the command that reproduces its md5. S98's MISSION is at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| What did the 2 unread debates decide? | never opened | read them before ranking ROOT 9 |
| Does a `ctx-trim@0` run really report SUCCESS? | inherited from S97 advisory, unmeasured | 9.19, first move |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| Why does `dryrun_two_account_split.py` exit 1? | not ZeroDivisionError | unread |
| Which 3 markers belong to which NN-PHI rule? | unbindable by any parser | 5.29 |
| What produced gen 15's graveyard md5? | no span of the file reproduces it | 5.28; may be unrecoverable |
| How many of the 61 CHECKABLE survive a build? | 1 of 5 died at S95 (20%) | roadmap 2 |
| Is `harnesses` red for ONE cause or three? | 5.14 says one cause, never re-confirmed | S98 mission |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| Z = 53/159 = 33.3%, stated repeatedly | **57/102 of 159 = 35.8%** - a banked number re-carried | the register's own grep |
| `grep -c ... \|\| echo 0` counts ARB-FIT | `grep -c` exits 1 on zero, so `\|\| echo 0` printed a SECOND zero | James's paste |
| "the artifact is portable - the summary lines match" | every figure matched and the bytes did not | James's `head -25` |
| the map should be named after the register it read | "highest number = live" is law; one exception is a routing trap | S92's review |
| a first parser bound every CHECKABLE marker | it bound 103 of 159 to ONE rule and said nothing | a duplicate-owner assert |
| expected item count 41 | **36** - I counted LINES where several items share a line | the method's own grep |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- FOURTH AND FINAL CARRY: **`harnesses` is RED on every push and that is CORRECT** - 5.14/5.17.
  Compare the signature against `33572158050`. *Expires at S98 BY MISSION.*
- FOURTH AND FINAL CARRY: **`gni_ci_harness.yml` passes NO secrets**, so a harness importing
  `mad_protocol` resolves `MODEL` to the dead `llama-3.3-70b-versatile` - 9.15. *Expires at S98.*
- SECOND CARRY: **NEVER read `gni_ci_harness.yml` at RUN level.** Run `conclusion` is `failure`
  on every push. Use `gh run view <id> --json jobs`. *Expires when 5.14 ships.*
- THIRD CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  `--ignore-cr-at-eol` did NOT clear S95's `\r\r\n`. Use `git diff -w` and `git show HEAD:<path>`.
  *Expires when 5.21 ships a `.gitattributes`.* **This also blocks trusting any md5 of a
  checked-out file: hash what a tool just wrote, never what git just handed you.**
- NEW: **`docs/GNI_MACRO_MAP_S95.md` is named for the REGISTER it read, not the session**, and it
  is already stale (159 vs 164). Both are known: 5.27 and 5.26. *Expire at S98.*

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `09588b2` + the S96 docs commit (verify by ls-remote) TREE CLEAN -- S97 does not exist as a build session and nothing from it is missing
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = make the detector GREEN -- ship 5.14 + 5.17 + 9.15, then C6 (5.26) and M4 (5.27); done when one no-op push reaches BOTH jobs green job-level AND one deliberate break shows RED
ROADMAP = ROADMAP 1 ACHIEVED 4/4 (`944c4f0` `44a3cba` `b639b54` `09588b2`), archived. ROADMAP 2 = JAMES'S (DECISION S96-1): S98 detector -- S99 §6 -- S100 §5 (AST) -- S101 SLO. Its WRITTEN COMPLETION TEST is in `GNI_ARCHITECTURE_S96.md` and is the only thing that may declare it finished
ORDER = `docs/GNI_TARGET_AND_ORDER_S96.md` (highest number = live) is the queue -- 36 items, the counting COMMAND printed beside the number; CARRY THE GRAVEYARD (7 rows) and verify it with the command printed under it, never with a bare hash
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); an instrument checks its own expectations with a control probe (R-S93-1); a reviewer's CHECKING COMMAND is itself a lead (R-S94-1); verification is computed BEFORE the write (R-S95-1); a constant count is not a constant state (R-S95-4); a checksum without its command verifies nothing (R-S96-2)

## 8. POINTERS (<=5 lines)
`tools/gni_macro_map.py`: exit 0/1/2 - 2 means the INSTRUMENT refused, never a pass; it names its
output after the REGISTER generation, so the name is `_S95` until 5.27 ships. `tools/gni_rule_checks.py`:
five checks; C6 becomes the sixth. `tools/gni_state.py --stdout` needs `PYTHONIOENCODING=utf-8` on
Windows (5.22). `GNI_RULE_CHECKABILITY_S95.tsv` is RETIRED - read the register, not the TSV.
Never put SQL and bash in one message (R-S88-1). Verify by symbol, never by path.

## DIARY S96
The mission was to measure the gap between what this system says and what it can prove, and the
measurement kept landing on the session doing the measuring. The map's first parser swallowed a
hundred and three markers into one rule and told me nothing was wrong. The artifact I certified
byte-identical produced different bytes on James's machine than on mine, and every number in my
own acceptance test agreed across both. The checksum the last close ordered me to verify turned
out to reproduce from nothing at all. And the map itself went stale inside the same session that
shipped it, because five new rules landed in the register two hours after the commit. None of
that was caught by the five checks I wrote or the fixture that watches them. Three of the four
were caught by James pasting terminal output back at me, and the fourth by a duplicate-owner
assertion I nearly did not write. What I would want read from this session is not the map. It is
that the instrument was wrong four times and the operator's paste was right four times, and the
gap the map was supposed to measure was mostly sitting on my side of it.
