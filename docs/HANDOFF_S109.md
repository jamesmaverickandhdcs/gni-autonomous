# HANDOFF S109 -> S110
DATE: 2026-10-04 (UTC) | HEAD: `c78c288` + the S109 close commit (verify by ls-remote) | MODEL: Opus 5.5
Read ONCE. Standing rules: docs/GNI_RULES_S109.md by ID (current through R-S109-3).
CONTRACT UNCHANGED at v11, verified by md5 after the copy, not by name. PROTOCOL v21 (Part D step 4 only).
The close ships seven files session-numbered plus the macro map generated LAST; the claims document and
its two S109 `.tsv` files are already in the tree from the product commits.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S109.md` (generation 29). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: two main runs on Oct 4 - 08:26Z (272 articles) and 15:22Z (280); `frequency_log` raw 18.4, 21.5.
L2 MAD: 40 of 40 `run-mad success` runs (Sep 14 - Oct 4) carry `ARB-FIT`, 20 watches beside them. Read by id:
`37190098951` and `37110117798` (`ctx-trim@5121`, `@4930`). The Oct 4 evening debate (verdict bearish) NOT read.
L3 GPVS, L4 Quota: untouched. L5 Public: `/alerts`, `/health`, `/comparison`, `/`, `/history`, `/scenarios`.
Five product commits, each CI-green at job level, Vercel `success`, each live-read against a control.
Target: TRUTHFULNESS OF OUTPUT. **Detector: 16 checks. Fixture: 67 families.** Claims 748 at 801
locations; COVERAGE 21/748, **0 DEFEATED**. Order: **65 items** under CAP 70, ORPHAN RATE 47/65.
Roadmap 3: four rows DONE - R3-4's prediction held at both judging closes; the AGENT TEST has never run.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 9.23 DONE | raw value certified; the logged line reports the row; `/alerts` dead block gone; correlations ruled | `720e374`, run `37201358890` id `0de95f4e` = row |
| 9.20 DONE | preflight filters `main` (was the quota name): "table empty" -> "Gap 251 min"; skip exits 0 of 40 | `ea74cc9` |
| 9.16 CLOSED | both sides measured: 8 of 9 workflows use `setup-python`; `gni_selfcheck.yml` uses runner `python3` | grep |
| 9.5 F12 + class | four `pipeline_runs` readers filter `main`; selftest UNPATCHED -> PATCHED | `d87f57a` |
| live read | `/health` card: "0 articles to 0 via adaptive" -> "272 articles to 22 via groq" | browser |
| 9.5 F13 | `/alerts` tiles that could not count removed; CLM-691 retired, CLM-755/756 minted | `848b256`, chunk |
| 9.5 F14 + 3 pages | `src/lib/verdict.ts`: `pending` no longer DISAGREE, neutral no longer AGREE/DIVERGING | `c78c288`, chunk |
| governor | one active prompt variant (v1); health 6 of 60 under both counts; left dormant | SQL |
| close | gen 29: 9.23, 9.20, 9.16 closed; none opened; 65; protocol v21 | scans |

## 3. ORDER
**MOVED.** `docs/GNI_TARGET_AND_ORDER_S109.md` - generation 29. **65 items, CAP 70** (ROOT 5 at 41).
CLOSED 9.23, 9.20, 9.16; OPENED none. GRAVEYARD carried by bytes, md5 `3e8ac222c6ef212261676c02d7d56f6f`,
fourteenth generation. S110's MISSION is at the top of that file: roadmap 3's agent test, then 9.5.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| P29: `/comparison` shows PENDING on REAL data (not only in the chunk) | chunk-proven | the page in the ~20 min between a main run and its MAD |
| The first health run after `d87f57a` writes no `avg 0` alert | selftest only | `health_alerts` after the next count-multiple-of-ten run |
| v1 `run_count` 383 vs 265 main rows | hypothesis: rows lost in the Supabase-outage shrink | SQL on `pipeline_runs` age vs prompt history |
| Which third layer S69 counted as paper | none | the S69 record |
| EU AI Act Art. 50(4); ROOT 8's return; 5.25's retire clause | not ruled | James |
| What IS `GROQ_MAD_MODEL`? GitHub masks the value | unknown since July | Groq console usage by model (James) |

## 5. WRONG THIS SESSION - COUNT: 16 (every one, counted), then the 6 that matter most
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| F3: "the code is 5-state; 'seven states' is a hidden false half" | a COMMENT said 5-state; the map, the legend and the route hold seven | reading the map (R-S109-1) |
| P13b: the Oct 4 main run writes a LOW_COLLECTION alert | health runs only when the row count is a multiple of ten (`main.py:249`) | the SQL; led to the governor |
| P21: reports with a NULL verdict exist | never: `main.py:284` writes `pending` at insert | the SQL; led to the real F14 |
| P11: a skip-path run hides among `run-mad success` | 0 of 40 - the code has the path, the history never took it | the 60-run census |
| three close-vs-continue lettered proposals carried no `LINEAGE:` line | CONTRACT v11 asks it of every lettered proposal | this close's audit |
| "always type the printf line by hand" | needed once per terminal; the mode stays off until the window closes | the next paste working |
(Also wrong: P1 two AFTER rows - one, the runs drift ~6 h off cron; P3 two debates since close - one; P14
alerts above half the mains - 3 of 60; "mains collect 400+" - 272 and 280; P19 one hit - two, a heading
held the string; P26 three active variants - one; the BEFORE card's row - a newer adaptive run, 12:45Z;
the close's glossary row cited a rule id of the other project - the identity guard blocked the commit.)

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- CARRIED (fifteenth): **LF/CRLF on a Windows clone.** Never md5 a checked-out file. *Expires with 5.21.*
- CARRIED: **`--stdout` on any `tools/*.py` needs `PYTHONIOENCODING=utf-8` on Windows.** *Expires with 5.22.*
- CARRIED: **the pre-commit guard blocks on UNTRACKED files** (*expires when it scans the index only*); **the order's second scan reads ANY `digits.digits`** (*5.51*).
- WIDENED: **a copy change mints claim units** that need a verdict row and a binding row before `gni_claims.py --write` runs. *Expires when CI regenerates it.*
- NEW: **long paste chains are slow** - the commit/push/cert chain rides inside the `.sh` as a `--ship` mode. *Expires when every runner has it.*
- NEW: **the container's GitHub API calls are rate-limited** (shared address); run lists come from James's `gh`. *Expires with authenticated access.*
- EXPIRED: `OK Adaptive run logged` (9.23 shipped). PROMOTED, do not carry: R-S109-1..3; a FURTHER INSTANCE of R-S105-3.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `c78c288` + the S109 close commit (verify by ls-remote) TREE CLEAN -- five product commits (`720e374` 9.23, `ea74cc9` 9.20, `d87f57a` 9.5 class, `848b256` F13, `c78c288` F14), CI green at job level, Vercel success, each live-read against a control
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = **ROADMAP 3's AGENT TEST RUN AND RECORDED - JAMES ASKS "WHY ARE WE DOING SMART OFFICE?", THE SESSION ANSWERS FROM THE REPO ALONE, AND JAMES'S VERDICT IS WRITTEN AS ONE `AGENT-TEST` LINE IN `docs/GNI_ORIGIN.md`; ON PASS ROADMAP 3 IS DECLARED ACHIEVED AND THE PHASE TRANSITION RUNS AT THE S110 CLOSE; THEN ITEM 9.5's F16 TO F19**
ROADMAP = **ROADMAP 3, FOUR ROWS DONE** - DECISION S107-8's prediction HELD at both judging closes (68, then 65); `python tools/gni_lambda.py --window S108:S109` prints 0.00; ACHIEVED waits only on the agent test
ORDER = `docs/GNI_TARGET_AND_ORDER_S109.md` (highest number = live) is the queue, **generation 29** -- 65 items, CAP 70, ROOT 5 at most 42, ORPHAN RATE 47/65; CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`). FIRST MOVE: James asks the agent-test question verbatim
GATE = CONTRACT v11 `LINEAGE:` on every lettered proposal - close-vs-continue included - AND every finding (R-S89-1); a cert DISCRIMINATES (R-S90-1) and reads the written row (R-S108-3); read the map, not the comment (R-S109-1); a table holding two populations names its population in every read (R-S109-2); every reader names a writer's placeholder (R-S109-3); verification AFTER `git add` (R-S100-2); container HEAD equals James's before any generator (R-S107-1); a live read proves the NEW build against a control (R-S105-2)

## 8. POINTERS (<=5 lines)
`tools/mk_close_s109.py` is the executable record of this close. The S109 product scripts (outside the
repo) are the pattern: HEAD guard, a live CONTROL read before the patch, `rb`/`wb` ASCII anchors, a
selftest that reads UNPATCHED before PATCHED, verdict + binding rows for changed copy, regenerate, verify
after `git add`, md5 against the container's dry run, build - and the commit chained behind those md5s.

## DIARY S109
The mission took the morning; the class took the afternoon. One wrong prediction about an alert opened
the table that holds two populations, and every reader that forgot it was telling someone a small lie:
an alert, a card, a gap, a filter. A placeholder did the same on four pages that each had their own
idea of agreement. The worst moment was mine: calling a true sentence false because a comment said so.
