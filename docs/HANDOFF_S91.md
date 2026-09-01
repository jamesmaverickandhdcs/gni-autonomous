# HANDOFF S91 -> S92
DATE: 2026-09-01 | HEAD: `33578de` + the S91 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S91-5; R-S55-1, R-S87-6
and R-S81-5 each carry a NEW AMENDMENT/INSTANCE). **CONTRACT stays v8 and Protocol stays v10 —
no rule of engagement changed.** All five files ship SESSION-NUMBERED.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S91.md` (generation 11). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. Last scheduled run `33420536876` (17:37Z) success.
L2 MAD: green. `33420957824` + `33422581858` both scheduled, both success, evidence UNREAD.
L3 GPVS: untouched, ten sessions. L4 Quota: not re-measured this session.
L5 Public: **no commits this session** — the one commit was a test file.
STORAGE: 113/500 MB meter (S90 figure, not re-measured). Backup: NONE.
SCHEDULE: crons `02:13Z`/`10:13Z` (pipeline), `02:43`/`10:43`/`11:13` (MAD). **Lateness band
  re-measured 2026-08-31 over 8 slots: 6h03-7h24, ABOVE the recorded 4h39-6h05. Zero missed.**
PLATFORM: all 8 workflows on `checkout@v7` + `setup-python@v7` — **CERT COMPLETE (6.7 closed)**.
SECRETS: `GROQ_GNI_NOT_MAD` rotated, certified on dispatch AND on schedule. `GROQ_API_KEY`
  (THREE workflows) and `GROQ_MAD_EVENING` NOT — **first move at open, DECISION S91-3**.
Target: TRUTHFULNESS OF OUTPUT. ROOT 9 top; ROOT 8 has 8.5 closed, 8.10 still open.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 8.5 DISCHARGED | `33578de` — `dryrun_nn5_gate.py`, two arms, 6/6, EXIT=0 | harness output |
| 8.5 evidence | CONTROL prints `NN-5: 2 hard constraint(s)`; TREATMENT prints none | A1-A4 |
| 8.5 key result | TREATMENT still returns `bearish`, `arb_failed=False` | A5 |
| 8.1c MEASURED | branch costs **555 chars** of arb prompt on a stubbed 8-article run | A6 |
| 8.1b re-measured | `reports` 199 rows: 198 CRITICAL at **exactly 10.0**, 1 ELEVATED@5.0 | SQL |
| Protocol 8h | 2 of the gate's 3 OR clauses have NEVER decided a run | same SQL |
| 6.7 CLOSED | post-fix runs node20=**0**/**0**; controls **8**/**4** (order said 2) | log grep |
| Rotation cert 2 | `not_mad` key green on a SCHEDULED run `33420536876` | env dump `***` |
| **5.14 NEW** | **3 of 10 harnesses DEAD, one cause** — `all_articles=[]` + `c3ce662` | 10 runs |
| 5.14 lineage | harnesses last touched `460ce84` (Jun 21); wiring `c3ce662` (Jun 27) | git log |
| 9.13 NEW | published band table wrong in 2 of 5 rows (CRITICAL, upper HIGH) | code read |
| 9.14 NEW | `route.ts:39` `.limit(5)` hides the 2 rows that would cert 9.9 + 9.10 | SQL + read |
| 5.13 CLOSED | its premise is false — S90 fixed that header in the same close | grep = 0 |
| COMMIT 2 | S51's deferred commit DID land (`mad_depth_est` at `:1288`, used at `:638`) | grep |
| Order | generation 11; GRAVEYARD 7 rows copied forward BY BYTES, not retyped | assert |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S91.md` — generation 11, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file. **The GRAVEYARD still has SEVEN
rows: read it before proposing anything in ROOT 8, ROOT 1, retention, or a published figure.**

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do 9.9/9.10 render right? | shipped, build green, outputs coincide on live data | 9.14 |
| Can `all_articles` be EMPTY in production? | 3 code paths return `[], []`; 0 of 30 MAD runs | 5.14's SWOT |
| Why does `dryrun_two_account_split.py` exit 1? | different cause, NOT ZeroDivisionError | unread |
| Do the 42 `__main__` selftests outside `tests/` work? | never run — running them runs the pipeline | needs a method |
| Why do `frequency_log` and `reports` disagree on 2026-06-22? | 6.1 vs 5.0, same second | unread |
| Why does `reports` start 2026-05-24 but `frequency_log` 2026-03-20? | 199 vs 338 rows | retention, ROOT 6 |
| What does PROBE-DRIFT actually test? | S57-era records only | recover, don't infer |
| `LR-101` / `GNI-R-122` original text | cited as law, unfound | conversation_search |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "the slot-vs-actual mismatch is a NEW lead" | R-S81-7 + R-S87-6 already law; band already in S89's order | James: "read the S90 record" |
| "6.7 does not certify / its criterion is obsolete" | node20 = 0 both arms; my grep ORed 3 unrelated patterns (R-S91-3) | splitting the grep |
| "`'HIGH' in escalation` is a substring hazard" | `escalation` is a level string, not prose — retracted same turn | reading `:214-215` |
| "COMMIT 2 (S51) probably never shipped" | it did — `mad_depth_est` at `:1288`, consumed at `mad_runner:638` | the grep I proposed |
| "`net=0` means safe to run" | `dryrun_rate_governor` scored 0 and hit the network anyway (R-S91-4) | its own output |
| **"expected 62 unique item ids"** | **47.** S90 made the SAME error with the SAME number; R-S81-5's own instance note says so, and I had just read it | the advance count, working |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- (PROMOTED at this close: S90's `GROQ_API_KEY`-feeds-three-workflows trap became **R-S91-5**.
  It had ridden forward once; CONTRACT bans a second unchanged carry. The operational half now
  lives in the order's LIFECYCLE section and in S92's first-move block.)
- NEW (first carry): **`dryrun_false_neutral.py`, `dryrun_mad_redefinition.py` and
  `mad_protocol.py`'s `__main__` are DEAD.** Any session citing them as evidence is citing a
  test that cannot run. **Expires when 5.14 ships and all three exit 0.**

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S91 docs commit (verify by ls-remote; `33578de` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = item 9.14 — raise `route.ts:39`'s `.limit(5)` so the two stored discriminating rows reach the page; it certifies 9.9 AND 9.10 with no live non-CRITICAL run
ORDER = `docs/GNI_TARGET_AND_ORDER_S91.md` (highest number = live) is the queue — regenerate, never fold forward, but CARRY THE GRAVEYARD (7 rows)
GATE = CONTRACT v8 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); a bundle claim is a claim, verify each item's condition (R-S91-2); one pattern per number (R-S91-3)
FIRST MOVE = `date -u` + git status + ls-remote; then ROTATE `GROQ_API_KEY` (THREE workflows — enumerate with `git grep -n 'GROQ_API_KEY' -- .github/` first, R-S91-5) and `GROQ_MAD_EVENING`, deferred twice already

## 8. POINTERS (<=5 lines)
**THREE STORED POINTERS WERE WRONG THIS SESSION — verify by symbol, never by path.**
`frequency_controller.py` is at `ai_engine/analysis/`, NOT `ai_engine/`. `mad_runner.py` is at
`ai_engine/`, NOT repo root. **`tools/replay_scorer.py` is NOT 8.5's simulator** — it imports
`escalation_scorer`, never `mad_protocol`; the working pattern is `ai_engine/tests/dryrun_*.py`.
`_high_escalation` = `mad_protocol.py:989` (arbitrator) and has NOTHING to do with
`frequency_log` (scheduler). `FREQUENCY_MAP` + `get_recommended_interval` are the interval
truth. Empty `all_articles` raises before the protocol runs. Never put SQL and bash in one
message (R-S88-1). Run `python tools/design_bench.py` BEFORE any scorer OPINION.

## DIARY S91 (<=10 lines)
The mission was to prove a branch could run, and it ran — but the thing I will carry is that
the harness crashed first, and the crash was not mine. Three regression tests and a module's
own selftest have been dead since June, killed by a wiring commit that swept the callers inside
the function and never the callers outside it. They fail loudly. Nobody looked. That is the
same shape as `GNI-R-076` last session and the empty secret that printed a tick: the signal was
available and unread. Then, at this very close, I stated "expected 62 unique item ids" — the
identical wrong number S90 stated, recorded three paragraphs from the end of a file I had read
today. The advance count caught it, as designed. I did not catch it. What the guard is for is
exactly the moment the person holding it is confident, and I keep being that person.
