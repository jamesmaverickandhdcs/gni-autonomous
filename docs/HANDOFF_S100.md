# HANDOFF S100 -> S101
DATE: 2026-09-04 (UTC) | HEAD: `3268c14` + the S100 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S100-3; every rule carries
a **CHECKABLE** marker). **CONTRACT stays v10** - byte-identical to S96, nothing changed.
**Protocol is now v15** (PART C step 9a: STAGE a new tool before regenerating any section).
SIX files ship session-numbered, plus the generated map.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S100.md` (generation 19). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **PERISHABLE - do not quote, run it** (R-S98-2);
  the daily unit is 2 debate + 1 watch. Separate them at JOB level, not by log grep:
  `gh run list --workflow=gni_mad.yml --limit 20 --json databaseId,createdAt,conclusion`
  then `gh run view <id> --json jobs` - debate = `run-mad success`, watch = the reverse.
  Ids already read: `33886688564`, `33884251974`, `33848611889`, `33770071442`, `33768475533`.
L3 GPVS: untouched, nineteen sessions. L4 Quota: not re-measured.
L5 Public: **two commits** - `cbd34a7`, `3268c14` (plus the S100 docs commit).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, nine generations.
SCHEDULE: declared unchanged; DELIVERY measured at S99, not re-measured. PLATFORM: 9 workflows.
SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2). Target: TRUTHFULNESS OF OUTPUT, unchanged.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | ARCHITECTURE section 5 BUILDING BLOCK VIEW, generated from the AST | `cbd34a7` |
| the tool | `tools/gni_blocks.py`, 875 lines, single-phase, no snapshot | 29 self-counted probes |
| **ROADMAP 2 ROW 2 PASSES** | sections 5, 6 AND 7 all byte-identical, first time | `5ed36f4c...` twice |
| items CLOSED | **5.33** (section 7's clock) + **5.34** (`--session` default=94) | `3268c14` |
| 5.33 discriminates | the stamp's manifest md5 MOVES when a workflow changes | probed both ways |
| CI | job level, this exact SHA - `harnesses` + `rule_checks` both green | run `33904077322` |
| detector | six checks, exit 0, on the finished tree | `gni_rule_checks.py .` |
| **the finding** | **29 of 80 modules call `sys.path`**, 35 calls - one file, several names | section 5.0 |
| the consequence | a package-relative resolver matched almost nothing: **3 edges, not 84** | my own v1 |
| test coverage | **61 of 68 non-test modules imported by NO test**; 5 of 11 tests import one module | section 5.5 |
| dead surface | **35 of 965** module-level symbols read nowhere; 23 modules imported by nothing | 5.3, 5.4 |
| the gap row 4 keeps | sections 5 and 6 are generated and **nothing goes RED when they go stale** | item 5.41 |
| NEW ITEMS | **EIGHT.** 5.38-5.45. rho = **2/8** - two closed, two opened per closed | order gen 19 |
| RULES | `R-S100-1..3` + an INSTANCE recorded against R-S99-1 | rules appendix |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S100.md` - generation 19, dated, superseding. **59 items**,
with TWO differently-shaped counting commands printed beside the number. They DISAGREED at 61/64
on the first assembly and again at 59/60 on the second - three bare decimals had entered my new
prose, and the sentence announcing the two closures cited the very ids it was retiring, which
kept them in the queue. **The prose was rewritten each time; the commands were never weakened.**
The file is produced by `tools/mk_order_s100.py` as a TRANSFORM of generation 18's bytes, so the
51 carried items and the GRAVEYARD are never retyped. **The GRAVEYARD still has SEVEN rows**, md5
`3e8ac222c6ef212261676c02d7d56f6f` - a fourth generation publishing the same value, verified from
generation 18's bytes BEFORE the write and from generation 19's own bytes after. S101's MISSION is
at the top of that file, with the one item ranked above it for James to rule.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Are the 23 unreferenced modules reachable from a workflow? | measured one half only | join 5.3 against section 7's entrypoint column |
| How many of the 35 lonely symbols are pytest discovery? | not separated | 5.40 - subtract `test_*` and `Test*` |
| WHY the 30-minute crons lost ~86% of slots | measured S99, uncaused | 6.11 - and there may be no lever |
| Does a `ctx-trim@0` run really report SUCCESS? | still unmeasured | 9.19 |
| What do 5.5, 5.6, 5.7, 5.8, 5.11, 5.12 actually SAY? | text lost before gen 16 | read `..._S95.md` or earlier |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| Would consolidating the `sys.path` roots break imports? | never attempted | 5.38 - wants a ruling before a line moves |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| `grep 'ast\.\|AST'` finds prior AST work | it matched `last.`, `broadcast.`, `FORECAST` - nearly every doc | a 4-line probe |
| the generator passed 22/22, so it works | the fixture was one I INVENTED; it reported 3 edges across 79 modules | 5.1 summing to 3 |
| the probe line was missing, so nothing ran | it prints to **stdout**; my command read `.err` | reading the tool |
| the flip test failed - grep found 0 | my pattern assumed two table cells were ADJACENT | reading the row |
| the fixed tool was delivered | I copied it to the output dir and issued NO new download | his md5, unchanged |
| every `render()` parameter is unused | I compared `ast.arg` OBJECTS against a set of STRINGS | `wfs` in the output |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- SIXTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  Use `git diff -w`, and **never md5 a checked-out file** - hash what a tool just wrote, or
  normalise with `.replace(b'\r\n', b'\n')` first. *Expires when 5.21 ships.*
- NEW: **stage a new tool with `git add` BEFORE regenerating section 5.** `gni_blocks.py` reads
  `git ls-files`, so an untracked generator is invisible to its own output and the section is
  stale at the commit that introduces it. This bit twice in one session. *Expires with 5.41.*
- CARRIED: **`gni_runtime.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows** or it exits on
  a cp1252 encode. The file-writing path is safe. *Expires with 5.22.*
- EXPIRED, do not carry: `gni_state.py`'s `--session` default of 94. Closed at `3268c14`.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `3268c14` + the S100 docs commit (verify by ls-remote) TREE CLEAN -- two mission commits, TWO order items closed, eight opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = ROADMAP 2 ROW 4, THE SLO: a committed statement of what GNI promises on cadence and freshness, plus a check that FAILS when the promise is not met, wired into `gni_ci_harness.yml` and demonstrated against a case it must CATCH and one it must MISS
ROADMAP = ROADMAP 2 is JAMES'S (DECISION S96-1) and is **3 of 4**: S98 detector ACHIEVED -- S99 section 6 ACHIEVED -- S100 section 5 ACHIEVED (`cbd34a7`, CI run `33904077322` green at JOB level) -- S101 SLO. Its WRITTEN COMPLETION TEST is in `GNI_ARCHITECTURE_S100.md`; **row 2 now PASSES for the first time**, row 4 still fails and item 5.41 says why
ORDER = `docs/GNI_TARGET_AND_ORDER_S100.md` (highest number = live) is the queue -- 59 items, TWO counting commands printed beside the number and both must agree; CARRY THE GRAVEYARD (7 rows) and verify it with the command printed under it. FIRST MOVE: read the mission block, then rule item **6.11**, carried unresolved from two closes
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); an instrument checks its own expectations with a control probe (R-S93-1) built from the REAL tree's bytes, never from sources you invented (R-S100-1); verification is computed BEFORE the write (R-S95-1); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches (R-S98-6); an instrument bounded by what it measures reports its smallest answer where the truth is largest (R-S99-1); a fix is not shipped until the recipient has verified the bytes (R-S100-3)

## 8. POINTERS (<=5 lines)
`tools/gni_blocks.py --session N [--src DOC]`: exit 2 = the INSTRUMENT refused, 3 = input missing.
Single-phase, no snapshot - the tree IS the evidence. `collect`, `analyse`, `render`, `norm_md5`
are importable ON PURPOSE so a staleness check can call this parser instead of writing a second
one (R-S96-3, the precedent C6 set). `tools/gni_state.py` now REQUIRES `--session`. Regenerate in
this order: stage -> `gni_blocks.py` -> `gni_state.py` -> detector -> commit. SQL and bash never
share a message (R-S88-1).

## NOTE ON THIS FILE'S OWN SHAPE
PART B's LOAD CHECK template names five fields: HEAD, TARGET+MISSION, ORDER, TRAP, FIRST MOVE.
S99 shipped ROADMAP and GATE in place of TRAP and FIRST MOVE, and I carried that shape rather
than silently restoring the template - a trap copied forward unchanged twice becomes an
unregistered rule. FIRST MOVE is folded into the ORDER line above; TRAP is section 6, which the
open reads anyway. Whether the template or the practice is canonical is a ruling nobody has made.
It is not filed as an order item because it is about this document, not about GNI.

## DIARY S100
The mission took two hours and my own instruments took the rest, again - six times, one more
than S99. The pattern underneath every one of them is the same and I want to name it plainly,
because naming it is the only thing that has ever helped: I checked my work against something I
had made myself. The control probe passed 22 of 22 because I wrote the fixture AND the resolver,
so of course they agreed; the fixture used `from ai_engine.analysis.mad_protocol import ...` and
the actual repo has never once written that line. Twenty-nine modules push their own directory
onto `sys.path`, so a file answers to `analysis.mad_protocol` and to `mad_protocol` and to
neither of the names I had assumed. The tool reported three internal edges across seventy-nine
modules and zero test coverage, and both numbers were impossible, and it took reading the output
rather than the test results to see it. James caught nothing wrong; he ran what I gave him and
the numbers spoke. The fix was not a better resolver, it was rebuilding the probe out of import
lines he had grepped out of the real tree - which is now R-S100-1, and which is the only reason
the second version found eighty-four edges and reproduced a five-edge module exactly.
The close earned one more. The sentence I wrote to announce that two items were closed cited
their ids, which put them back in the queue, and the two counting commands disagreed at 61 and
64 because of it. S99 hit the same wall and wrote that it rewrote the prose rather than weaken
the command. I read that sentence at the open, and did the same thing anyway, and then did what
it said.
