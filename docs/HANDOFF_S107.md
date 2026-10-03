# HANDOFF S107 -> S108
DATE: 2026-10-03 (UTC) | HEAD: `fbf9c06` + the S107 close commit (verify by ls-remote) | MODEL: Opus 5.5
Read ONCE. Standing rules: docs/GNI_RULES_S107.md by ID (current through R-S107-3).
CONTRACT UNCHANGED at v11. PROTOCOL v20 (Part C step 9a: the claims document and the HEAD rule).
SIX files ship session-numbered, plus the glossary and the macro map generated LAST.
`docs/GNI_ORIGIN.md` is append-only and is not re-shipped.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S107.md` (generation 27). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: not re-read. L2 MAD: no run between the S106 close and the S107 open (5 runs listed, all
before it, all `success`). L3 GPVS, L4 Quota: untouched. L5 Public: NO page changed this session.
Seven commits, each CI-green at JOB level (`3e09ec3` was red, fixed by `5235776`).
Target: TRUTHFULNESS OF OUTPUT. **Detector: 16 checks. Fixture: 67 families.**
**ROADMAP 3: ROWS 1-3 DONE, ROW 4 BOUND** - its outcome is judged at the S108 and S109 closes.
Claims: 745 at 798 locations; COVERAGE 25/745, **8 DEFEATED**. ORPHAN RATE 50/70.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| White Paper | located, frozen verbatim from the .docx as `docs/GNI_WHITE_PAPER_S107.md` | `3e09ec3` |
| R3-2 DONE | `gni_claims.py`, 1389 verdicts, `GNI_CLAIMS_S107.md`; check `claims resolve` | `cf1742c` |
| R3-3 (1/3) | `gni_fitness.py`, 7 fitness functions, bindings; check `claim status derived` | `d0612e0` |
| R3-3 (2/3) | module buckets; check `dead symbols`; `--only` replay mode | `203e048` |
| R3-3 (3/3) | layer map; check `declared layers wired`; DONE command prints 3 | `4b2b391` |
| OWED paid | `tools/gni_lambda.py`: baseline 1.50/close (S105:S106) | `fbf9c06` |
| R3-4 BOUND | gen 27 items carry claim tags; check `order bound to claims` | close commit |
| Test 1 | S68 FAILs `dead symbols` + `declared layers wired`; S91 FAILs `order bound to claims` | local replay |
| 9.24 OPENED | the 8 DEFEATED claims; 5.24 closed by the retire clause | order |

## 3. ORDER
**MOVED.** `docs/GNI_TARGET_AND_ORDER_S107.md` - generation 27. **70 items, CAP 70** (ROOT 5 at 41).
CLOSED 5.24, OPENED 9.24. GRAVEYARD carried by bytes, md5 `3e8ac222c6ef212261676c02d7d56f6f`,
twelfth generation. S108's MISSION is at the top of that file: item 9.24, done at 0 DEFEATED.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Which third layer S69 counted as paper (the replay finds two) | none | the S69 record |
| Will the item count fall below 70 by S109 (DECISION S107-8) | prediction | the S108, S109 closes |
| Does EU AI Act Art. 50(4) apply to GNI's audience? | not ruled | James |
| Does ROOT 8 return from the archive on item 9.23's measurement? | not ruled | James |
| 5.25's retire clause (secret wiring; clocks paused by S92-2) | not ruled | James |
| What IS `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |
| The 419 UNREVIEWED claims: how many have a repository measurement? | none | binding work |

## 5. WRONG THIS SESSION - COUNT: 25 (every one, counted), then the 6 that matter most
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| "green" before the first commit | the run preceded `git add`; section 5 counts the index | CI red, `3e09ec3` |
| Test 1's replay command (the spec) | a full run halts on an old tree before any check | running it |
| the container's regenerated architecture | stamped HEAD `d0612e0`; James was at `203e048` | md5 mismatch, pre-ship |
| "~6.5 per session" (the record) | S100's NEW line was a copy of S99's; bytes say 7.60 | `gni_lambda.py` |
| "60 pages" (the spec) | 30 files counted twice without globstar; 35 pages | re-running it |
| P3: 80-200 claims | 745; the White Paper alone holds 219 | the verdict tally |
(Also wrong: P2 350-600 candidates, 2073; P4 the two paper files differ, they do not; the ~600 manual
verdicts, 1061; P6 ORPHAN 40-65%, 71%; a commit block without `cd` into the repo; "the context is
long" offered as a reason to close at an hour James called the start; the first fixture claim bound to
page count, three older families red; family 43's instrument error; C5 self-lint, four times; the
extractor read a CRLF paper's marker as absent; `$'..'` quoting in dash; a patch anchor with a stray
quote; the reason `UNREVIEWED` used before it was registered; and FOUR lettered proposals made
without a `LINEAGE:` line - continue-or-close after R3-2, verdicts-now-or-S108, C15's three shapes,
and binding-at-close - wrong-ledger entries under CONTRACT v7 whatever was chosen.)

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- CARRIED (thirteenth): **LF/CRLF on a Windows clone.** Never md5 a checked-out file. *Expires with 5.21.*
- CARRIED: **`--stdout` on any `tools/*.py` needs `PYTHONIOENCODING=utf-8` on Windows.** *Expires with 5.22.*
- CARRIED: **the pre-commit guard blocks on UNTRACKED files too** - commit scripts live outside the tree.
  *Expires when the guard scans the index only.*
- CARRIED: **the order's second count scan reads ANY `digits.digits`** in the queue. *Expires with 5.51.*
- NEW: **a page edit moves claim lines** - `claims resolve` and `claim status derived` go red until
  `python tools/gni_claims.py --write <N>` runs. *Expires when the document regenerates in CI.*
- PROMOTED, do not carry: generators count the index (R-S100-2, further instance); HEAD (R-S107-1).

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `fbf9c06` + the S107 close commit (verify by ls-remote) TREE CLEAN -- seven pushes before the close, CI green at job level on each, no public page changed
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = **ITEM 9.24 - THE EIGHT DEFEATED CLAIMS MADE TRUE, DONE WHEN `claim status derived` PRINTS 0 DEFEATED AND EACH PAGE IS READ LIVE**; after any page edit `python tools/gni_claims.py --write 108` runs before the commit
ROADMAP = **ROADMAP 3, ROWS 1-3 DONE, ROW 4 BOUND AT S107** - its outcome (DECISION S107-8: the item count below 70) is judged at the S108 and S109 closes, with `tools/gni_lambda.py` printed beside it
ORDER = `docs/GNI_TARGET_AND_ORDER_S107.md` (highest number = live) is the queue, **generation 27** -- 70 items, **CAP 70, ROOT 5 at most 42**, ORPHAN RATE 50/70 printed and derived by `order bound to claims`; CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`, twelfth generation)
GATE = CONTRACT v11 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); verification BEFORE the write and AFTER `git add` (R-S95-1, R-S100-2); the container's HEAD equals James's before any generator (R-S107-1); a replay runs only the checks it names (R-S107-2); a live read proves the NEW build with a rendered literal (R-S105-2); the order may not grow past its cap (R-S105-7)

## 8. POINTERS (<=5 lines)
`tools/mk_close_s107.py` is the executable record of this close and of every binding. A claim's id,
status and evidence are in `docs/GNI_CLAIMS_S107.md` (generated); its verdict and binding rows in the
two `.tsv` files beside it. `--only '<label regex>' <tree>` replays checks on an old tree. The S107
commit scripts (outside the repo) are the pattern: HEAD guard, bytes, stage, regenerate, verify, commit.

## DIARY S107
The paper was in James's Downloads folder all along, a .docx and its PDF twenty seconds apart. From it
and thirty-five pages came seven hundred and forty-five sentences that promise something, and the
tree could already judge twenty-five of them; eight were false. The best moment was the replay: the
S68 tree, read by today's checks, failed for exactly the reasons S69 found by hand - the detector
nobody imported, and a layer no code ever implemented. The worst was the first commit, red because I
read the trap and did not apply it. The order did not grow, and every item in it now says whom it serves.
