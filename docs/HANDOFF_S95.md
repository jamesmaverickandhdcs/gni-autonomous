# HANDOFF S95 -> S96
DATE: 2026-09-03 | HEAD: `b70fc08` + the S95 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S95-5; every rule in
the register now carries a **CHECKABLE** marker).
**CONTRACT stays v9 — byte-identical to S93, md5 `d7e68e815a17eaffbaedc5d6b4494bde`.**
**Protocol stays v11 — byte-identical.** SIX files ship session-numbered.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S95.md` (generation 15). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **0 unread.** No new debate arrived during S95 —
  latest is `33525874914` (Sep 1, 15:27Z), already identified as a grounding-watch. The gap
  was not a gift this session. ROOT 1.3 still holds across FIVE debates, unchanged.
L3 GPVS: untouched, fourteen sessions. L4 Quota: not re-measured.
L5 Public: **6 commits** — `b639b54` (detector + manifest) · `66c105e` (cert break) ·
  `a5e9c1e` (cert revert) · `a7f6378` (fixture selftest) · `280243f` (control probe step) ·
  `6989fad` (154 markers + TSV) · `b70fc08` (CRLF repair).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE.
SCHEDULE: unchanged. **Lateness band +4h07m to +6h58m over n=9 — item 6.10. Never quote a
  cron as a start time.** PLATFORM: **9 workflows = 7 scheduled + 1 push + 1 dispatch-only**,
  re-derived from YAML by C2 this session. `gni_ci_harness.yml` now has **TWO jobs**.
SECRETS: 22 stored. LIFECYCLE clocks remain PAUSED (DECISION S92-2). Nothing is due.
Target: TRUTHFULNESS OF OUTPUT. ROOT 9 top; 9.13/9.15/9.16/9.17/9.18 open.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | 159 rules classified; 53 CHECKABLE, 106 not, one reason each | `6989fad` |
| five executable | C1 `R-S90-2` · C2 `R-S91-5` · C3 `R-S74-1` · C4 `R-S62-3` · C5 `R-S81-5` | `b639b54` |
| CERT | green -> break one manifest row -> RED (ONE check) -> revert -> green | 3 runs |
| the control | `harnesses` RED in all three runs and never moved | job-level |
| first green square | `rule_checks success` — GNI's first CI job meant to pass | `33680416374` |
| escape design | backticks DISPROVEN: `GNI-R-114` is backticked AND load-bearing | order:316 |
| manifest | PART 0 gains 8 rows, statuses closed; C1's only escape source | rules PART 0 |
| `R-S92-2` | DEMOTED to NOT CHECKABLE — three designs died against measurement | `route.ts:39` |
| banked WRONG | "134 rules" was banked with no method; measured **154**, now 159 | census |
| the eight | S90's 8 unregistered = S95's 8, **but 4 rotated out and 4 in** | R-S95-4 |
| UNKNOWN closed | CI exit integers still read **1/1/0/0**, two `ZeroDivisionError` | run log |
| 5.20 half | fixture is a self-asserting selftest, runs in CI before the checks | `280243f` |
| NEW ITEMS | **SIX.** 5.22 · 5.23 · 5.24 · 5.25 · 6.11 · 9.18 | order gen 15 |
| rho | **6/1 = 6.00** this generation | order greps |
| RULES | `R-S95-1` .. `R-S95-5`, each with a CHECKABLE marker | rules appendix |
| RULINGS | **NONE this session** — S95 executed DECISION S93-2's assignment | — |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S95.md` — generation 15, dated, superseding.
S96's MISSION is at the top of that file: **the time-series macro map**. There is **NO first
move at open**. **The GRAVEYARD still has SEVEN rows**, verified md5-identical to generation 14.
The roadmap is JAMES'S (DECISION S93-2) and S96 is its LAST row.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| Why does `dryrun_two_account_split.py` exit 1? | not ZeroDivisionError | unread |
| What does PROBE-DRIFT actually test? | S57-era records only | recover; clock stopped |
| `LR-101` / `GNI-R-122` original text | manifested as DANGLING-LAW | conversation_search |
| Do `frequency_log` (348) and `reports` (199) still disagree on 2026-06-22? | 6.1 vs 5.0 | ROOT 6 |
| Which 50 rows does `mad_runner.py:104` get? | unordered `limit(50)` | 6.11 |
| Is the lateness band stable, or drifting? | n=9, one 4-day window | 6.10, widen it |
| How many of the 53 CHECKABLE survive an actual build? | 1 of 5 died at S95 (20%) | S96 axis |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "`docs/` holds 126 md files" | **117** — hand-counted from an `ls` I already had | deriving it |
| `R-S81-1` applied to the FINDING, not the INPUT | a doc citing zero rules is legitimate | fixture |
| `body.split("\n" + "on:")` finds the trigger block | a workflow may START with `on:` | fixture |
| `out.count(b"| \`")` counts what I inserted | it counted the whole file; 12 vs 8, then 9 vs 7 | detector |
| `print(...) % a - b` in a patch script | `%` binds tighter than `-`; crashed AFTER the write | traceback |
| `split("\n")` on a CRLF file, rejoined with CRLF | wrote `\r\r\n` on 1235 lines; killed `gni_state.py` | diff stat |
| (shape) SEVEN instrument errors; five inside `/tmp` scripts C5 cannot see | — | 5.23 |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- THIRD CARRY: **`harnesses` is RED on every push and that is CORRECT** — items 5.14 and 5.17.
  Exit integers are `1/1/0/0`; compare the signature against `33572158050`.
  *Expires when 5.14 ships.*
- THIRD CARRY: **`gni_ci_harness.yml` passes NO secrets**, so a harness importing
  `mad_protocol` resolves `MODEL` to the dead `llama-3.3-70b-versatile` string — 9.15.
  *Expires when 9.15 ships.*
- NEW (first carry): **NEVER read `gni_ci_harness.yml` at RUN level.** Run `conclusion` is
  `failure` on every push because `harnesses` is correctly red, so a run-level read cannot
  see `rule_checks` change. Use `gh run view <id> --json jobs`. *Expires when 5.14 ships.*
- SECOND CARRY: **a fresh clone on Windows can present the WHOLE architecture document as
  changed** — LF/CRLF, not content. This bit S95 for real: `git diff --stat` reported
  1385/1235 for 150 inserted lines and `--ignore-cr-at-eol` did NOT clear it, because the
  damage was `\r\r\n` (two CRs), not one. Use `git diff -w` and `git show HEAD:<path>`.
  *Expires when 5.21 ships a `.gitattributes`.*

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S95 docs commit (verify by ls-remote; `b70fc08` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = build the time-series macro map — X session, Y White Paper layer, Z vision-to-executable — as ONE generated artifact that names its source for every point and shows absent points as absent
ROADMAP = 4 sessions, JAMES'S (DECISION S93-2): S93 ✅ CI detector (`944c4f0`); S94 ✅ state generator §7 (`44a3cba`); S95 ✅ rule→check (`b639b54`, 53/159 CHECKABLE, five shipped); S96 macro map — the LAST row. Source of truth: `GNI_ARCHITECTURE_S95.md` ROADMAP
ORDER = `docs/GNI_TARGET_AND_ORDER_S95.md` (highest number = live) is the queue — CARRY THE GRAVEYARD (7 rows, md5 `203d371bc1d5522cd259ed1daf4bb0ab`); rho is 6/1 this generation and is not hidden; the item-count METHOD is written beside the number, so re-grep, never recall
GATE = CONTRACT v9 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); select on a relation, never a position (R-S92-2); an instrument checks its own expectations with a control probe (R-S93-1); a reviewer's CHECKING COMMAND is itself a lead (R-S94-1); verification is computed BEFORE the write (R-S95-1); a constant count is not a constant state (R-S95-4)

## 8. POINTERS (<=5 lines)
`tools/gni_rule_checks.py`: five checks, exit 0/1/2 — 2 means the INSTRUMENT refused, never a
pass. `tools/gni_rule_checks_fixture.py`: 11 families, self-asserting, runs first in CI.
`tools/gni_state.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows (5.22); the
file-writing path is fine. `docs/GNI_RULE_CHECKABILITY_S95.tsv` is the machine-readable
classification — S96 should read it, not re-derive it. Never put SQL and bash in one message
(R-S88-1). Verify by symbol, never by path.

## DIARY S95
The mission was to turn judgement into code, and what the code turned out to be for was
finding out how badly the judgement had been written down. Three rules I had marked
CHECKABLE could not be built; R-S92-2 took four designs and killed all of them, and the last
one died on a byte James pasted — `.order('run_at')` sitting right there in front of
`limit(1000)`, the direct descendant of the constant the rule was minted for. The rule was
never wrong. It was never finished. An LLM reading it supplies the missing boundary from
context and never notices the gap; a script cannot, so the script demands the boundary and
the demand is the whole value. I made seven instrument errors. The fixture caught three
before the repo saw them, the detector caught one of my own counters, and two reached James's
terminal — including one where I wrote a rule about verifying before mutating and then broke
it seven minutes later in the next script. The one I would most want read is the corruption:
I wrote `\r\r\n` across twelve hundred lines, all five of my new checks stayed green, git
said nothing, and the only witness was a diff stat I had asked for out of habit.
