# HANDOFF S98 -> S99
DATE: 2026-09-04 | HEAD: `1d5bcab` + the S98 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S98-6; every rule carries
a **CHECKABLE** marker). **CONTRACT stays v10** - byte-identical to S96, nothing changed.
**Protocol is now v13** (PART C step 9a, REGENERATE GENERATED ARTIFACTS). SIX files ship
session-numbered, plus the generated map.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S98.md` (generation 17). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **PERISHABLE - do not quote this field, run it**
  (R-S98-2). At 2026-09-03 21:10Z it was six unread; the daily unit is 2 debate + 1 watch:
  `gh run list --workflow=gni_mad.yml --limit 20 --json databaseId,createdAt,conclusion`
  then split by `ARB-FIT` presence, never by time. Ids already read: `33768475533`.
L3 GPVS: untouched, seventeen sessions. L4 Quota: not re-measured.
L5 Public: **six commits** - `98a9bc3` `447ce55` `328be08` `173bce9` `a5f2813` `1d5bcab`.
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, seven generations.
SCHEDULE: unchanged. PLATFORM: 9 workflows = 7 scheduled + 1 push + 1 dispatch-only. SECRETS: 22.
LIFECYCLE clocks PAUSED (DECISION S92-2). Target: TRUTHFULNESS OF OUTPUT, unchanged.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | detector GREEN and DISCRIMINATING - all five items shipped | 6 commits |
| 5.14 + 5.17 | article pool restored to two June harnesses; NO allowlist built | `98a9bc3` |
| the cert pair | deliberate break RED, revert GREEN, `git diff HEAD~2` empty | `447ce55`/`328be08` |
| 9.15 | decommissioned model string removed from its two live homes | `173bce9` |
| 5.27 (M4) | `--session` required; artifact named for the SESSION; md5 EOL-normalised | `a5f2813` |
| 5.26 (C6) | map staleness now RED, on marker count AND normalised md5 | `1d5bcab` |
| fixture | 11 families -> 14; `12-map-stale-count`, `13-map-stale-md5`, `14-map-missing` | 0 mismatches |
| the ruling that mattered | generation 16 had INVERTED DECISION S93-1 into "build the allowlist" | R-S98-1 |
| Groq, dated | `llama-3.3-70b-versatile` deprecated 2026-06-17, decommissioned 2026-08-16 | Groq docs |
| production is fine | MAD run `33768475533`: zero agent errors, three distinct verdicts | log read |
| 9.19 first bytes | `ARB-FIT: ctx_depth=0 est=4997/5000 steps=drop-R1,R3@110w`, run reports success | same log |
| the count was wrong | generation 16 said 36 beside a command returning 36; the file held 47 | R-S98-6 |
| NEW ITEMS | **FOUR.** 5.30 - 5.31 - 5.32 - 9.20. rho = **4/5**, closing more than opening | order gen 17 |
| RULES | `R-S98-1` .. `R-S98-6` + an AMENDMENT to R-S90-1 (where a negative arm may live) | rules appendix |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S98.md` - generation 17, dated, superseding. **46 items**,
and TWO differently-shaped counting commands are printed beside the number, because generation 16
published one command that returned 36 for a file holding 47. Every id is bolded so the published
command is true of the file it sits in. **The GRAVEYARD still has SEVEN rows**, copied by bytes and
verified against generation 16's published md5 BEFORE this file was written. S99's MISSION is at
the top of that file, together with the one item I would rank above it for James to rule on.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Does a `ctx-trim@0` run really report SUCCESS? | still unmeasured | 9.19 - find the run, read it |
| How often does "MAD skipped cleanly" fire? | never counted | 9.20 |
| Why does `dryrun_two_account_split.py` exit 1? | still unread; it is at the REPO ROOT | 5.32 |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July; CI masks it | a run log's model string |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| Which 3 markers belong to which NN-PHI rule? | unbindable by any parser | 5.29 |
| What did the unread MAD debates decide? | one of six opened | read before ranking ROOT 9 |
| How many of the 61 CHECKABLE survive a build? | 1 of 5 died at S95 | roadmap 2 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| `grep -c $'\r$'` says the file has 0 CR bytes | it had **1488** - the pattern never matched | a control probe |
| 14 MAD runs are NEW | they were already-read runs; my baseline held UNREAD ids, not READ ids | the output's own dates |
| `<newest_id>` / `<id_of_the_new_run>` | a placeholder in a fenced bash block is a shell redirect - **twice**, the second after logging the first | bash |
| the module is at `analysis/mad_protocol.py` | `ai_engine/analysis/` - I transcribed a traceback frame with an unresolved `..` | the symbol grep |
| production MAD may be calling a decommissioned model | zero agent errors, three distinct verdicts | ONE log read |
| the order holds 36 items | **47** - the published command counts bolded heads only | a second-shaped scan |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- FOURTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  `git ls-files --eol` now shows the REGISTER alone at `i/lf w/crlf`. Use `git diff -w`, and
  **never md5 a checked-out file** - hash what a tool just wrote. *Expires when 5.21 ships.*
- NEW: **`tools/gni_macro_map.py` now REQUIRES `--session N`.** A bare invocation exits 2, the
  INSTRUMENT REFUSING and never a pass. *Expires once one session has run it.*
- EXPIRED THIS CLOSE, do not carry: `harnesses` red on every push · never read the harness
  workflow at run level · the map named for its register · MODEL resolving to a dead string.
  All four were trap-shaped only because their items were open; the items shipped.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `1d5bcab` + the S98 docs commit (verify by ls-remote) TREE CLEAN -- six commits, five order items closed, four opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = ARCHITECTURE section 6 RUNTIME VIEW, GENERATED by a named tool in `tools/`, byte-identical on a second run; FIRST MOVE is to decide IN WRITING where section 6 ends and section 5 (AST, S100) begins
ROADMAP = ROADMAP 2 is JAMES'S (DECISION S96-1) and is **1 of 4**: S98 detector ACHIEVED (`98a9bc3` `173bce9` `a5f2813` `1d5bcab`) -- S99 section 6 -- S100 section 5 -- S101 SLO. Its WRITTEN COMPLETION TEST is in `GNI_ARCHITECTURE_S98.md` with a per-row status table and is the only thing that may declare it finished
ORDER = `docs/GNI_TARGET_AND_ORDER_S98.md` (highest number = live) is the queue -- 46 items, TWO counting commands printed beside the number and both must agree; CARRY THE GRAVEYARD (7 rows) and verify it with the command printed under it, which now strips `\r` first
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1, amended S98 - a CI fixture family may be the negative arm); an instrument checks its own expectations with a control probe (R-S93-1); verification is computed BEFORE the write (R-S95-1); a constant count is not a constant state (R-S95-4); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches, not what you meant (R-S98-6)

## 8. POINTERS (<=5 lines)
`tools/gni_macro_map.py --session N`: exit 2 = the INSTRUMENT refused, never a pass; `norm_md5`
strips BOM and CRLF before hashing. `tools/gni_rule_checks.py .` = six checks; the fixture runs
FIRST in CI and is C6's negative arm. **Protocol PART C step 9a is new: regenerate the map AFTER
appending rules, or the close's own docs commit reddens the detector.** Verify by symbol, never by
path - a traceback frame is not a path (R-S98-4). Never put SQL and bash in one message (R-S88-1).

## DIARY S98
The mission was to make a detector that had been red on every push for three sessions go green,
and what nearly went wrong was not the code. Generation 16 had compressed a ruling into four words
- "Allowlist, paired with 5.14" - that said the opposite of what James ruled at S93, and I opened
the session ready to build it. What stopped me was searching the session record before designing,
a habit written down as a preference and not as a rule. The rest followed one pattern: every claim
I made about my own instruments was wrong, and every one was caught by measuring the same object a
second way. A grep reporting zero CR bytes in a file holding 1488. A baseline calling fourteen
already-read runs new. A published command returning 36 for a file holding 47. The system's own
cross-root diagnosis says to ask who guaranteed a constant before tuning it. This session the
constant was my own confidence, and the guarantor was me.
