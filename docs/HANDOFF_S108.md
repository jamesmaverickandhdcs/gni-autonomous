# HANDOFF S108 -> S109
DATE: 2026-10-03 (UTC) | HEAD: `440b205` + the S108 close commit (verify by ls-remote) | MODEL: Opus 5.5
Read ONCE. Standing rules: docs/GNI_RULES_S108.md by ID (current through R-S108-3).
CONTRACT UNCHANGED at v11, verified by md5 after the copy, not by name. PROTOCOL UNCHANGED at v20.
SIX files ship session-numbered, plus the glossary and the macro map generated LAST.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S108.md` (generation 28). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: not re-read; `pipeline_runs` holds 265 main and 933 adaptive rows (SQL, S108).
L2 MAD: 3 runs since the S107 handoff, split at JOB level - 2 debates + 1 watch. Read by id:
`37131273125` (depth=0, 39/39 arrived, neutral 0.57) and the watch `37132171031` (7 days: 151
consultant / 117 arbitrator hits over 14 runs). The 08:33Z debate `37110117798` was NOT read.
L3 GPVS, L4 Quota: untouched. L5 Public: 7 pages changed (9.24), `/autonomy` + `/health` (9.23).
Two product commits, each CI-green at JOB level and Vercel `success`. One manual adaptive dispatch.
Target: TRUTHFULNESS OF OUTPUT. **Detector: 16 checks. Fixture: 67 families.** Claims 745 at 798
locations; COVERAGE 21/745, **0 DEFEATED**. Order: **68 items** under CAP 70, ORPHAN RATE 49/68.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| 9.24 DONE | 9 claims made true (8 + CLM-498's hidden "70", bound FIRST: 9 DEFEATED, then 0) | `7cfc1d2` |
| live read | 6 pages HTML hits 0->1 after Vercel `success`; home via the deployed chunk, new 1/1, old 0/0 | logs |
| SQL | `pipeline_runs.mode` + `frequency_log.escalation_score_raw`, nullable, added BEFORE the code | info_schema |
| 9.23 part 1 | the adaptive run row records which branch ran | run `37139455249`: 17:09Z `lightweight`, 15:12Z NULL |
| 9.23 part 2 | `frequency_log` carries the uncapped score; `/api/health`, `/autonomy`, `/health` pass it | `440b205`, CERT PENDING |
| close | gen 28: 9.24 closed (mission), 9.18 closed (retire clause), NONE opened | scans 68/68 |
| findings | `mad_preflight` filters a `pipeline_type` no row has (9.20); `/alerts` dead block + false OK line (9.23) | SQL, code |

## 3. ORDER
**MOVED.** `docs/GNI_TARGET_AND_ORDER_S108.md` - generation 28. **68 items, CAP 70** (ROOT 5 at 41).
CLOSED 9.24 and 9.18, OPENED none. GRAVEYARD carried by bytes, md5 `3e8ac222c6ef212261676c02d7d56f6f`,
thirteenth generation. S109's MISSION is at the top of that file: item 9.23 finished.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Does the first main run after 16:51:27Z write a non-NULL raw? | prediction | the SQL in the order's mission |
| Will the count stay below 70 at S109 (DECISION S107-8) | met at S108 | the S109 close |
| Which third layer S69 counted as paper (the replay finds two) | none | the S69 record |
| EU AI Act Art. 50(4) for GNI's audience; ROOT 8's return; 5.25's retire clause | not ruled | James |
| What IS `GROQ_MAD_MODEL`? A run log CANNOT say: GitHub masks the value (`***`) | unknown since July | Groq console usage by model, or the id moved to a repo variable (James) |
| Why the deployed and local chunk hashes differ | hypothesis: build-time env inlining | not needed by any item |

## 5. WRONG THIS SESSION - COUNT: 15 (every one, counted), then the 6 that matter most
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| live read: "bytes must differ" after the deploy | "70"->"81" is same length; hits 0->1 discriminate, bytes do not | the live read |
| P9: home page live hits >= 1 | client component, text in a closed toggle; a fetch reads 0 | live read; chunk read fixed it |
| "the code writes `correlation_patterns`, not `historical_correlations`" | it writes both; my grep was cut by `head -25` | the SQL, then a full grep |
| cert grep trusted `OK Adaptive run logged` | printed whatever the insert did; the row is the proof | reading `save_pipeline_run` |
| S107 record: `GROQ_MAD_MODEL` resolves by a run log's model string | GitHub masks secret values in logs | the log |
| two lettered proposals carried no `LINEAGE:` line | the A-D after "B + C" (option D) and wait-or-close (option A) | this close's audit |
(Also wrong: P2 three unbound count sentences - one, and mis-bound; P4 the 70-list still in the tree - no
such list; P14 half - `historical_correlations` exists; P16 a model string in the log; the chunk hash as
build identity; my census regex missed `methodology:26`; 9.23's `alerts` table - none exists; a
glossary pattern ending in `*`, which the cell reader strips.)

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- CARRIED (fourteenth): **LF/CRLF on a Windows clone.** Never md5 a checked-out file. *Expires with 5.21.*
- CARRIED: **`--stdout` on any `tools/*.py` needs `PYTHONIOENCODING=utf-8` on Windows.** *Expires with 5.22.*
- CARRIED: **the pre-commit guard blocks on UNTRACKED files** - scripts live outside the tree. *Expires
  when the guard scans the index only.* CARRIED: **the order's second scan reads ANY `digits.digits`.** *5.51.*
- CARRIED: **a page edit moves claim lines** - `gni_claims.py --write <N>`. *Expires when CI regenerates it.*
- NEW: **`OK Adaptive run logged` prints whatever the insert did.** Certify by the row. *Expires with 9.23(a).*
- PROMOTED, do not carry: R-S108-1..3; FURTHER INSTANCES of R-S105-2 and R-S105-3.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `440b205` + the S108 close commit (verify by ls-remote) TREE CLEAN -- two product commits (`7cfc1d2` 9.24, `440b205` 9.23), CI green at job level, two nullable columns added by SQL, one manual adaptive dispatch
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = **ITEM 9.23 FINISHED - PART 2 CERTIFIED BY THE SQL IN THE MISSION, THE ADAPTIVE RUN ROW'S SUCCESS LINE MADE TRUE, THE DEAD ESCALATION BLOCK ON `/alerts` RESOLVED, AND THE `historical_correlations` RAW-AVERAGE QUESTION PUT TO JAMES AS A LETTERED RULING**
ROADMAP = **ROADMAP 3, ROWS 1-3 DONE, ROW 4 BOUND** - DECISION S107-8's prediction (item count below 70) MET at its first judging close, 68; judged again at the S109 close with `python tools/gni_lambda.py --window S108:S109` beside it
ORDER = `docs/GNI_TARGET_AND_ORDER_S108.md` (highest number = live) is the queue, **generation 28** -- 68 items, CAP 70, ROOT 5 at most 42, ORPHAN RATE 49/68; CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`). FIRST MOVE: the before/AFTER SQL in the order's mission
GATE = CONTRACT v11 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1) and reads the written row, not the writer's message (R-S108-3); every measurable value in a bound claim has a binding (R-S108-1); fix copy to its referent, never to the instrument's number (R-S108-2); verification AFTER `git add` (R-S100-2); container HEAD equals James's before any generator (R-S107-1); a live read proves the NEW build with content only the new source produces (R-S105-2)

## 8. POINTERS (<=5 lines)
`tools/mk_close_s108.py` is the executable record of this close. The S108 product scripts (outside the
repo) are the pattern: HEAD guard, `SQL_DONE` guard, patch in `rb`/`wb`, fake-client selftest, compile,
per-element greps, regenerate section 5 + macro map after any `.py` edit, verify after `git add`, build.
Claim statuses: `docs/GNI_CLAIMS_S108.md`; verdict and binding rows in the two S108 `.tsv` files.

## DIARY S108
The eight false sentences were nine: one had been bound to its true half and hid its false half
behind a green status. Binding it first turned the check red before it turned it green, and that red
was the session's best moment. The worst kind of easy fix was available twice - copy "9" from the
instrument, trust the writer's "OK" - and each would have shipped a new untruth behind a passing
check. The adaptive run now says which mode it ran, and the first row that said it read `lightweight`.
