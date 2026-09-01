# HANDOFF S93 -> S94
DATE: 2026-09-01 | HEAD: `944c4f0` + the S93 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S93-1; R-S82-4 and
R-S91-4 each carry a NEW AMENDMENT — R-S91-4's SPECIMEN IS WITHDRAWN, its conclusion stands).
**CONTRACT stays v9 — byte-identical to S92, verified by md5sum.** **Protocol is now v11**
(one template step: the STATE line). SIX files ship session-numbered.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S93.md` (generation 13). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. L2 MAD: **0 unread — 2 debate READ + 1 watch identified.** `33484715285`
  (Sep 1) 200/33/**33** dropped=0 bearish 0.52 · `33420957824` (Aug 31) 213/32/**32**
  dropped=0 bullish 0.67 · `33422581858` is the 11:13 grounding-watch, not a debate.
L3 GPVS: untouched, twelve sessions. L4 Quota: not re-measured.
L5 Public: **1 commit** — `944c4f0` (`gni_ci_harness.yml`). No frontend change.
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE.
SCHEDULE: crons `02:13Z`/`10:13Z` (pipeline), `02:43`/`10:43`/`11:13` (MAD). **Use the
  measured BAND, not the cron time, and RE-MEASURE it — R-S87-6's third amendment says the
  band is wider than recorded and must never be recalled.** S93 re-derived it as a "lead"
  and was wrong: it is already law.
PLATFORM: **9 workflows now.** 8 scheduled + `gni_ci_harness.yml` on push. CI is live.
SECRETS: unchanged. All LIFECYCLE clocks remain PAUSED (DECISION S92-2). Nothing is due.
Target: TRUTHFULNESS OF OUTPUT. ROOT 9 top; 9.13/9.15/9.16 open.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | `gni_ci_harness.yml` — GNI's FIRST push-triggered workflow | `944c4f0` |
| CERT | RED **and discriminating inside one run**: 2 fail / 2 pass | run `33529254247` |
| exit codes | `false_neutral`=1 `mad_redefinition`=1 `nn5_gate`=0 `rate_governor`=0 | CI log |
| no quota cost | `secrets.`=0 in the workflow; `ModuleNotFoundError`=0 | grep + log |
| TRAP RETIRED | 3 "dangling" secrets all traced; **nothing deleted** | `git grep` |
| `GROQ_MODEL_FALLBACK` | read by **6 code files**, 0 workflows — this is **item 1.12** | grep |
| `GROQ_TEST_ONLY` | 4th probe account, deliberately local-only — **S90 already said so** | S90:63 |
| `TELEGRAM_CHAT_ID` | pre-rename remnant; `preflight.sh:75` guards against its return | grep |
| ROOT 1.3 holding | both debates `dropped=0`, no ctx-trim, `ARB-FIT ctx_depth=0` | run logs |
| rho MEASURED | S90 0.75 · S91 1.00 · **S93 9.00** — and it needs a SCOPE | order greps |
| rho scope | it measures QUEUE-WORKING sessions; it cannot measure S92 | ARCH §11 D1 |
| Protocol v11 | STATE line: `L2 MAD: {N debate + M watch, by ARB-FIT}` | template |
| CONTRACT | v9, **byte-identical**, md5 `d7e68e815a17eaffbaedc5d6b4494bde` | md5sum |
| NEW ITEMS | **NINE.** 5.15 5.16 5.17 5.18 5.19 6.9 7.4 9.15 9.16 | order gen 13 |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S93.md` — generation 13, dated, superseding.
S94's MISSION is at the top of that file: **`tools/gni_state.py`, ARCHITECTURE section 7
ONLY** (5 and 6 are deliberately out of scope). There is **NO first move at open**.
**The GRAVEYARD still has SEVEN rows.** The roadmap is JAMES'S (DECISION S93-2) and appears
in three places: this LOAD CHECK, the order's CHANGED section, and the ARCHITECTURE table.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY first |
| Why does `dryrun_two_account_split.py` exit 1? | not ZeroDivisionError; repo ROOT, not `tests/` | unread |
| What does PROBE-DRIFT actually test? | S57-era records only | recover; clock stopped |
| `LR-101` / `GNI-R-122` original text | cited as law, unfound | conversation_search |
| Do `frequency_log` (348) and `reports` (199) still disagree on 2026-06-22? | 6.1 vs 5.0 | ROOT 6 |
| Is the grounding-shadow 9x swing real or an artefact? | n=2 | 7.4, harvest the span |
| What is the CURRENT lateness band? | S92's figure, not re-measured | measure, never recall |
| Does `GROQ_MODEL_FALLBACK`'s VALUE matter now that 6 files read it? | never read | 1.12 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "only 4 of the 10 harnesses exist" | the 10 are RUNNABLE harnesses, not `dryrun_*` | S91 record |
| "the lateness band doesn't match — new lead" | already law, R-S87-6 third amendment | the order |
| "`dryrun_*.py` should appear 3 times" | 2. I counted a loop I had just deleted | the script |
| "`nl= LF`" | `b"\\n"` searched for a backslash — the answer came by DEFAULT | 2nd checker |
| "S92 recorded S91's CLOSED/NEW as its own" | **S92 was a NEW DIRECTION, not S91's sequel** | James |
| (shape) 3 of 5 were INSTRUMENT errors | same shape as S92's five. The system was healthy | — |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- NEW (first carry): **CI is RED on every push and that is CORRECT** — items 5.14 and 5.17.
  A red CI is not news until 5.14 is fixed. **Do not treat the red as a regression signal,
  and do not silence it.** *Expires when 5.14 ships, which also closes 5.17.*
- NEW (first carry): **`gni_ci_harness.yml` passes NO secrets**, so any harness importing
  `mad_protocol` resolves `MODEL` to the dead `llama-3.3-70b-versatile` string in CI logs.
  Expected, not a live defect — see 9.15. *Expires when 9.15 ships or the generator (S94)
  publishes the three-layer default chain.*

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S93 docs commit (verify by ls-remote; `944c4f0` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = `tools/gni_state.py` generating ARCHITECTURE section 7 ONLY — workflow, cron, secrets, entrypoint, and `secret -> workflow -> code consumer` as ONE chain
ROADMAP = 4 sessions, JAMES'S (DECISION S93-2): S93 ✅ CI detector (`944c4f0`, run `33529254247`); S94 state generator (§7 only); S95 rule→check; S96 macro map. Source of truth: `GNI_ARCHITECTURE_S93.md` ROADMAP
ORDER = `docs/GNI_TARGET_AND_ORDER_S93.md` (highest number = live) is the queue — CARRY THE GRAVEYARD (7 rows); rho is 9/1 this generation and is not hidden
GATE = CONTRACT v9 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE on the surface the item is about (R-S90-1 + S92 amendment); a deadline must name its evidence (R-S92-1); select on a relation, never a position (R-S92-2); an instrument's expectations are checked BY THE SCRIPT with a control probe (R-S93-1)

## 8. POINTERS (<=5 lines)
Harnesses: `ai_engine/tests/dryrun_*.py` (FOUR). `dryrun_two_account_split.py` is at repo
ROOT and is NOT in the glob. `ai_engine/tests/` has **zero** `__main__` blocks — the four
dryruns execute at top level, the five `test_*.py` do not (item 5.15). `mad_rate_governor.py`
is at `ai_engine/`, `mad_protocol.py` at `ai_engine/analysis/`. Harness `sys.path` is derived
from `HERE`, so CI's working directory does not matter. Never put SQL and bash in one message
(R-S88-1). Verify by symbol, never by path.

## DIARY S93 (<=10 lines)
The mission was forty-four lines of YAML and it worked on the first push — red, for exactly
the two reasons it should have been red, with two green beside them so the red meant
something. What took the session was everything around it. A trap I inherited turned out to
be an eight-generation-old item wearing a new name, and a second one had already been
disproven in a ledger nobody re-reads. A rule I was carefully obeying rested on a specimen
that dissolved the moment I ran it in a room with no network. And five times I said
something confident that the bytes then refused — three of those were my own instruments
again, the same shape S92 wrote about. James stopped the worst of it: I had started
treating the roadmap as a message from a previous session, and he said plainly that it was
his. That is the thing I keep needing told. The documents are ours; the direction is his.
