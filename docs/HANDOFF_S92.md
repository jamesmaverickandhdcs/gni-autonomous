# HANDOFF S92 -> S93
DATE: 2026-09-01 | HEAD: `467dba0` + the S92 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S92-2; R-S90-1 and
R-S91-4 each carry a NEW AMENDMENT). **CONTRACT is now v9** (fifth ROUTING home + close
method). **Protocol stays v10 — byte-identical to S91, deliberately.** SIX files ship
session-numbered — a new one, `GNI_ARCHITECTURE_S92.md`.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S92.md` (generation 12). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. L2 MAD: `33420957824` + `33422581858` (Aug 31) still UNREAD; today's
  morning MAD not checked — count it at open by RUN ID, never by time.
L3 GPVS: untouched, eleven sessions. L4 Quota: not re-measured.
L5 Public: **3 commits** — `416a2fb`, `9d2dba8` (9.14 + certs), `467dba0` (ARCHITECTURE).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE.
SCHEDULE: crons `02:13Z`/`10:13Z` (pipeline), `02:43`/`10:43`/`11:13` (MAD). Lateness band
  6h03-7h24 (measured 8 slots, 2026-08-31). **Use the BAND, not the cron time** — S92 opened
  by predicting a run 16 minutes out that was in fact ~6 hours out.
PLATFORM: all 8 workflows on `checkout@v7` + `setup-python@v7`. CERT COMPLETE.
SECRETS: `GROQ_API_KEY` + `GROQ_MAD_EVENING` unrotated and **NO LONGER DUE** — DECISION
  S92-1 struck the deadline. Do not re-raise without exposure evidence.
Target: TRUTHFULNESS OF OUTPUT. ROOT 9 top; 9.9/9.10/9.14 closed, 9.13 open.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 9.14 CLOSED | `limit(5)` -> `limit(1000)`, 5 columns, divergence block | `416a2fb`+`9d2dba8` |
| 9.9 CERTIFIED | page renders `1.5h` / `1h`; old ladder would say `2h` / `30 min` | browser |
| 9.10 CERTIFIED | `HIGH`/`CRITICAL` come from the `escalation_level` column | browser |
| 9.13 PUBLISHED | band table and the two contradicting runs on the SAME page | browser |
| `frequency_log` | **348 rows**; exactly TWO diverge from the published band | SQL |
| **ARCHITECTURE** | `docs/GNI_ARCHITECTURE_S92.md`, arc42, 11880 B, byte-verified | `467dba0` |
| DECISION S92-1 | KEYFILE deadline STRUCK — origin unrecoverable, policies disagree | search |
| DECISION S92-2 | all LIFECYCLE clocks PAUSED until work in progress completes | James |
| DECISION S92-3 | one discipline per concern (ARCHITECTURE section 4) | James |
| DECISION S92-5 | close artifacts by BYTE COPY + anchored patch, never retyped | CONTRACT v9 |
| Secrets audited | 3 stored secrets read by NO workflow: `GROQ_MODEL_FALLBACK`, | two-list |
| | `GROQ_TEST_ONLY`, `TELEGRAM_CHAT_ID`. **Nothing deleted.** | diff |
| `MYANMAR_DISPATCH_PAT` | **LIVE** — `gni_mad.yml:66` -> `mad_runner.py:604`. Do not touch | grep |
| `TELEGRAM_WEBHOOK_SECRET` | read by VERCEL (`telegram-webhook/route.ts:12`), not Actions | grep |
| Order | generation 12; GRAVEYARD 7 rows carried BY BYTES, never re-read | `cp` |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S92.md` — generation 12, dated, superseding.
S93's MISSION is at the top of that file: **run the harnesses in CI**. There is **NO first
move at open** this time; the credential block that headed S91 and S92 has been struck.
**The GRAVEYARD still has SEVEN rows.** The S92 diagnosis (D1-D7) is NOT in the order and
NOT here — it is `GNI_ARCHITECTURE_S92.md` section 11. One finding, one home.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| What is in the two unread MAD runs? | scheduled, success | read at open, by RUN ID |
| Do the 42 `__main__` selftests work? | never run | S93's mission |
| Why does `dryrun_two_account_split.py` exit 1? | not ZeroDivisionError | unread |
| What does PROBE-DRIFT actually test? | S57-era records only | recover; clock stopped |
| `LR-101` / `GNI-R-122` original text | cited as law, unfound | conversation_search |
| Why do `frequency_log` (348) and `reports` (199) disagree on 2026-06-22? | 6.1 vs 5.0 | ROOT 6 |
| Is `limit(1000)` enough as the table grows? | 348 now; no guard | R-S92-2 says relation, not count |
| rho (findings in / items closed) across generations | never measured | S93, one grep |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "`TELEGRAM_QSC` secret is missing" | `TELEGRAM_QSChannel_ID`, healthy; my `[A-Z0-9_]` cut at `h` | byte grep |
| "`!= CRITICAL` finds every discriminating row" | it EXCLUDED the 9.3 CRITICAL row I needed | pos 332 |
| "fix 9.13 and the cert follows" | `intervalMap` is dead code — `stored` is never null | reading the file |
| "arc42 sections 10 and 12 are..." (from memory) | correct — **by luck, not method** | fetching the source |
| "`limit(332)` catches both rows" | one. The offset had already decayed by one run | the JSON |
| "the 02:43Z cron is 16 minutes away" | ~6 hours away; I ignored the band I had just read | the run log |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- **RETIRED, not carried:** S91's dead-harness trap (`dryrun_false_neutral.py`,
  `dryrun_mad_redefinition.py`, `mad_protocol.py`'s `__main__`) has been PROMOTED into
  S93's mission. It rode once; CONTRACT bans a second unchanged carry, so it is now work,
  not a warning. Those three still cannot run — cite them as evidence and you cite nothing.
- NEW (first carry): **`GROQ_MODEL_FALLBACK`, `GROQ_TEST_ONLY` and `TELEGRAM_CHAT_ID` are
  stored but read by no workflow.** Do NOT delete on that basis alone — `TELEGRAM_WEBHOOK_SECRET`
  looked identical and is read by Vercel. **Expires when each is traced to a consumer or none.**

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S92 docs commit (verify by ls-remote; `467dba0` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = run `ai_engine/tests/dryrun_*.py` in CI on every push, failing the run on non-zero exit — the harnesses are offline by design, so it costs no quota
ORDER = `docs/GNI_TARGET_AND_ORDER_S92.md` (highest number = live) is the queue — CARRY THE GRAVEYARD (7 rows); the diagnosis lives in `GNI_ARCHITECTURE_S92.md` section 11, not in the order
GATE = CONTRACT v9 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE and be visible on the surface the item is about (R-S90-1 + S92 amendment); a deadline must name its evidence (R-S92-1); select on a relation, never a position (R-S92-2)
FIRST MOVE = `date -u` + git status + ls-remote, then count MAD runs BY RUN ID. **No credential block. No LIFECYCLE item may claim the opening (DECISION S92-2).** Open with the mission.

## 8. POINTERS (<=5 lines)
`frequency_controller.py` is at `ai_engine/analysis/`; `mad_runner.py` at `ai_engine/`.
`FREQUENCY_MAP` + `get_recommended_interval` (`:39-55`) are the interval truth: CRITICAL
base 1.0, 0.5 only at score >= 9.5; HIGH base 2.0, 1.5 only at >= 8.5. `intervalMap` in
`autonomy/page.tsx` and `health/page.tsx` is DEAD CODE — `recommended_interval_hours` is
never null. Harnesses live at `ai_engine/tests/dryrun_*.py`; `tools/replay_scorer.py` is not
one. Never put SQL and bash in one message (R-S88-1). Verify by symbol, never by path.

## DIARY S92 (<=10 lines)
The mission was one line of TypeScript and it was not the day's work. James asked why we
were touching a secret key at all, and the honest answer turned out to be that nobody knew
— a date with no origin had been riding the order for eleven generations, steering the
opening of session after session. Pulling that thread took us to the thing underneath: GNI
has four documents and all four record change, so every session re-derives the system by
grepping and calls that work. We wrote item 5.3 fifteen months of sessions ago, named the
disease exactly, and closed it without building the cure. Today it exists. What I will
carry is smaller and worse: five wrong claims this session, all five mine, and not one of
them a fault in GNI — every single one was my own instrument. The system was healthy each
time I said it was broken. I keep being the thing I am checking for.
