# HANDOFF S94 -> S95
DATE: 2026-09-02 | HEAD: `44a3cba` + the S94 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S94-4; the four S94
rules each carry a **CHECKABLE** marker, which is S95's own mission format).
**CONTRACT stays v9 — byte-identical to S93, md5 `d7e68e815a17eaffbaedc5d6b4494bde`.**
**Protocol stays v11 — byte-identical.** SIX files ship session-numbered.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S94.md` (generation 14). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **0 unread — 3 debate READ + 1 watch identified.**
  `33524044619` (Sep 1) 220/31/**31** · `33375082629` (Aug 31) 168/35/**35** ·
  `33318313852` (Aug 30) 148/31/**31** — all dropped=0, `ARB-FIT ctx_depth=0`.
  `33525874914` is a grounding-watch (`ARB-FIT` count 0). **ROOT 1.3 now holds across FIVE
  consecutive debates**, not two.
L3 GPVS: untouched, thirteen sessions. L4 Quota: not re-measured.
L5 Public: **1 commit** — `44a3cba` (`tools/gni_state.py` + `docs/GNI_ARCHITECTURE_S94.md`).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE.
SCHEDULE: crons READ BY BYTES this close and correct as recorded. **Observed starts run
  +4h07m to +6h58m late over n=9 — item 6.10. Never quote a cron as a start time.**
PLATFORM: **9 workflows = 7 scheduled + 1 push + 1 dispatch-only** (corrects "8 scheduled";
  item 9.17). SECRETS: 22 stored, 18 reached by a workflow, 4 not — all four explained.
  LIFECYCLE clocks remain PAUSED (DECISION S92-2). Nothing is due.
Target: TRUTHFULNESS OF OUTPUT. ROOT 9 top; 9.13/9.15/9.16/9.17 open.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | `tools/gni_state.py` generates ARCHITECTURE section 7 | `44a3cba` |
| the chain | `secret -> workflow -> ENV ALIAS -> code consumer` in one pass | §7.2 |
| why alias matters | `GROQ_GNI_NOT_MAD` binds to env `GROQ_API_KEY` | §7.2 row |
| CERT | one secret line swapped -> **6 output lines move**; revert = byte-clean | diff |
| probe | regex broken on purpose -> `EXIT=2`, **nothing written** | stderr |
| scope held | §7 only; strip §7 and S93/S94 docs are IDENTICAL | `awk` + `diff` |
| CI unchanged | `33572158050` = `33569548145` failure signature | run logs |
| banked WRONG 1 | `GROQ_MODEL_FALLBACK` = **4 files**, not 6 (6 SITES) | `git grep -w` |
| banked WRONG 2 | `TELEGRAM_CHAT_ID` = **1 file** (`preflight.sh` guard), not 0 | `git grep -w` |
| 6.9 measured | **10 install steps, 6 distinct sets**, not "8 lists" | §7.3 |
| NEW ITEMS | **FOUR.** 9.17 · 6.10 · 5.20 · 5.21 | order gen 14 |
| rho | **4/1 = 4.00** this generation | order greps |
| item count | stated 67 in advance, measured 67, zero duplicates | order tail |
| RULES | `R-S94-1` .. `R-S94-4`, each with a CHECKABLE marker | rules file |
| RULINGS | **NONE this session** — S94 executed DECISION S93-2's assignment | — |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S94.md` — generation 14, dated, superseding.
S95's MISSION is at the top of that file: **classify all 134 rules CHECKABLE / NOT, and make
the top five executable.** There is **NO first move at open**.
**The GRAVEYARD still has SEVEN rows**, verified byte-identical to generation 13.
The roadmap is JAMES'S (DECISION S93-2) and appears in three places: this LOAD CHECK, the
order's CHANGED section, and the ARCHITECTURE table.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| Why does `dryrun_two_account_split.py` exit 1? | not ZeroDivisionError | unread |
| What does PROBE-DRIFT actually test? | S57-era records only | recover; clock stopped |
| `LR-101` / `GNI-R-122` original text | cited as law, unfound | conversation_search |
| Do `frequency_log` (348) and `reports` (199) still disagree on 2026-06-22? | 6.1 vs 5.0 | ROOT 6 |
| Is the grounding-shadow 9x swing real? | n=2 | 7.4, harvest the span |
| Is the lateness band stable, or drifting? | n=9, one 4-day window | 6.10, widen the window |
| Do the four CI exit-code integers still read 1/1/0/0? | signature compared, not codes | grep the log |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| `secrets.TELEGRAM_QSC` (a 4-workflow defect) | `[A-Z0-9_]*` truncated a mixed-case name | James's grep |
| "the mad crons will disagree with the record" | they match exactly; the LATENESS is real | the bytes |
| generator: 4 bugs (self-count, substring, list overwrite, "pip" in "pipeline") | — | the FIXTURE |
| `gh secret list` has a header row | none through a pipe; 22 became 21 | hand recount |
| predicted `GROQ_MODEL_FALLBACK` = 6 files | 4 files / 6 sites | `git grep -w` |
| (shape) 4 of 5 were INSTRUMENT errors | third consecutive session with this shape | — |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- SECOND CARRY: **CI is RED on every push and that is CORRECT** — items 5.14 and 5.17.
  Compare the failure SIGNATURE against `33572158050` before calling any red a regression.
  *Expires when 5.14 ships, which also closes 5.17.*
- SECOND CARRY: **`gni_ci_harness.yml` passes NO secrets**, so a harness importing
  `mad_protocol` resolves `MODEL` to the dead `llama-3.3-70b-versatile` string in CI logs.
  Expected, not a live defect — 9.15. *Expires when 9.15 ships.*
- NEW (first carry): **after a fresh clone on Windows, re-running `tools/gni_state.py` can
  present the WHOLE architecture document as changed** — LF/CRLF, not content. Check
  `git diff --stat` against `git diff --ignore-all-space` before believing it.
  *Expires when 5.21 ships a `.gitattributes`.*

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S94 docs commit (verify by ls-remote; `44a3cba` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = classify all 134 rules CHECKABLE / NOT with a one-line reason each, and make FIVE of them executable checks that a workflow can run
ROADMAP = 4 sessions, JAMES'S (DECISION S93-2): S93 ✅ CI detector (`944c4f0`); S94 ✅ state generator §7 (`44a3cba`); S95 rule→check; S96 macro map. Source of truth: `GNI_ARCHITECTURE_S94.md` ROADMAP
ORDER = `docs/GNI_TARGET_AND_ORDER_S94.md` (highest number = live) is the queue — CARRY THE GRAVEYARD (7 rows); rho is 4/1 this generation and is not hidden; the item-count METHOD is written beside the number, so re-grep, never recall
GATE = CONTRACT v9 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); a deadline must name its evidence (R-S92-1); select on a relation, never a position (R-S92-2); an instrument checks its own expectations with a control probe (R-S93-1); a reviewer's CHECKING COMMAND is itself a lead (R-S94-1)

## 8. POINTERS (<=5 lines)
`tools/gni_state.py`: `--stdout` prints §7 without writing, `--no-gh` skips `gh`, `--session N`
picks the output name; it splices between `## §7` and `## §8` and touches nothing else.
Its source doc is the HIGHEST-numbered `docs/GNI_ARCHITECTURE_S*.md`. Harnesses:
`ai_engine/tests/dryrun_*.py` (FOUR). `mad_rate_governor.py` is at `ai_engine/`,
`mad_protocol.py` at `ai_engine/analysis/`. Never put SQL and bash in one message (R-S88-1).
Verify by symbol, never by path.

## DIARY S94 (<=10 lines)
The mission was a generator, and the honest story of it is that the generator was wrong four
times before the repo ever saw it, and I only know that because I built a fake repo first and
let it fail there. Every one of the four was the same kind of mistake: a pattern that looked
right and quietly matched the wrong thing. Then the real tree found a fifth, and James's own
grep found a sixth in me before the session was ten minutes old. The instrument I shipped now
carries seven checks on itself, two of which exist purely because I made those mistakes, and
watching it exit 2 and refuse to write was the best moment of the session. Late on, S92's
review arrived with six criticisms; two were already done, one came with a command that would
have cried wolf. I nearly deferred to it out of politeness. The rule I earned from that is the
one I would most like the next session to actually read.
