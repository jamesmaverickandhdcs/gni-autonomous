# HANDOFF S112 -> S113
DATE: 2026-10-13 (UTC+7 13:xx; UTC 2026-10-13 06:xx) | HEAD: `e3b81a1` + the S112 close commit (verify by ls-remote) | MODEL: Opus 5.5
Read ONCE. Standing rules: docs/GNI_RULES_S112.md by ID (current through R-S112-3; R-S81-1 amended; NN-PHI-8 registered).
CONTRACT UNCHANGED at v11, PROTOCOL UNCHANGED at v21, each verified by md5 after the copy, not by name.
S112 was NOT a phase transition: roadmap 4 has four rows of four done and waits on Test 2. Roadmap 5 was DECLARED and is
QUEUED behind that verdict. The close ships the order, rules, protocol, contract, architecture, glossary and this file as
S112, the cognitive-warfare discussion record and S112's evidence queries in `docs/`; the macro map is generated LAST.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S112.md` (generation 32). This file is STATE ONLY.**
DECISION S112-3 (WAIT-1 to WAIT-3) was ruled on 2026-10-12 and reached no commit message; after the context compaction the
first close draft called it lost, and the session's own transcript (`read_conversation("current")`) held it intact (R-S112-1).

## 1. STATE (<=10 lines)
L1 Pipeline: the quality score no longer moves source weights (`e3b81a1`, DECISION S112-6) - code only, not yet read on a run. Stage 1b certified: none of 171 and 247 removed; replay of the control week's 14 removals removes none.
L2 MAD: 1 debate + 0 watch in the cert window, `ARB-FIT` confirmed. Confidence 53% in 8 of 9 completed debates on `/comparison` (one 54%) - 3.1's hypothesis, unruled.
L3 GPVS: v1.2 certified on a run (3 rows: 3-day correct, 7-day incorrect, each agreeing with SPY); no demonstrated skill - now item 9.25.
L4 Quota: not re-read. Vercel reported a build incident on 2026-10-12 (from 13:35Z, still open at 14:57Z): a push can wait.
L5 Public: claims 843 at 901 locations, COVERAGE 161/843, 0 DEFEATED, UNREVIEWED 0, **NUMBERS UNDERIVED 0**; confidence shown only when the Arbitrator stated one (C19).
Live watch: the first main run after `e3b81a1` (its log must lack the `Quality feedback:` line); the ledger's five known errors.
Target: TRUTHFULNESS OF OUTPUT. **Detector: 20 checks. Fixture: 106 families.** Promise ledger 237 rows: BUILT 63, PARTIAL 104, NOT BUILT 70.
Order: **58 items** under CAP 70, ORPHAN 42/58 (DECISION S112-3); **WAIT-4 to WAIT-8** wait outside it. Roadmap 4: **four of four rows, Test 2 not run.**

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| R4-3 | NUMBERS UNDERIVED 56 -> 0 in seven commits; EXTERNAL figures bound to a dated source snapshot (F-EXT) | `4eb0642`..`778d653` |
| snapshot | runtime snapshot designed first, DATED facts only; one-cell DB harvest corrected the August token figures | `57ecdb0` |
| 9.5(e) | PENDING seen on real data (operator's screenshot); the 0.5 insert placeholder no longer printed as confidence | `dd91b41` |
| C19 | `confidence in lib`: no page reads `mad_confidence` outside `src/lib/verdict.ts`; `/debate` scale 70/50 | `464cb6e` |
| R4-4 | promise ledger, 209 PROMISE claims graded; C20 `promise ledger` | `ddd9540` |
| philosophy | the founding rules (S32 + PHI-003) harvested and graded, 28 claims; roadmap 5 specified | `1c3fe8a` |
| NN-3 | quality score -> source weights switched off by a named constant; three ledger rows corrected | `e3b81a1` |
| certs | (2) (3a) (4a) (4b) (5) PASS, (3b) PARTIAL, (1) code-level only; backup tables dropped | logs + `docs/S112_C1.sql` |
| record | cognitive-warfare / grey-zone discussion, verbatim where it survived | `docs/GNI_COGWAR_GREYZONE_DISCUSSION_S112.md` |
| close | gen 32: six shells merged into 5.56, WAIT-1/2 -> 9.25, WAIT-3 -> 9.26, 58; five findings wait; three rules + one amendment | this commit |

## 3. ORDER
**MOVED.** `docs/GNI_TARGET_AND_ORDER_S112.md` - generation 32. **58 items, CAP 70** (ROOT 5 at 35).
DECISION S112-3: six shell lines MERGED into 5.56 (work stays open), 9.25 and 9.26 OPENED from WAIT-1 to WAIT-3; CLOSED none; notes on
9.5 (tail (e) PAID) and 3.1; a ninth cross-root instance. FIVE S112 FINDINGS (WAIT-4 to WAIT-8) wait outside the range. GRAVEYARD carried by bytes, md5 `3e8ac222c6ef212261676c02d7d56f6f`,
seventeenth generation. S113's MISSION is at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| cert (1) the debate prompt carries the run's month | code-level only; the prompt is stored nowhere | a debate log that prints the prompt |
| cert (3b) the black-swan window is 48 hours on real data | new rows ran on the new code; window by harness | a stored price window, or accept the harness |
| the quality-feedback channel is off on a real run | code only | the first main run log after `e3b81a1` |
| escalation_score_raw tracks the GPR index | 6 weeks, inconclusive | part G re-run at 12 weeks (~mid-November) |
| the Nov 1 offsite-backup reminder fires | carried from S110 | the Nov 1 log |
| Groq's per-model limit | never measured, claimed nowhere | 9.26's class |
| WAIT-4 to WAIT-8; 5.25's retire clause; EU AI Act Art. 50(4); dropping `public.profiles` | not ruled | the operator |

## 5. WRONG THIS SESSION - COUNT: 23 (every one, counted), then the 6 that matter most
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| CLM-1132 (NP-4, cross-run verdict memory) NOT BUILT; "MAD has no cross-run memory" said in conversation | `_get_debate_history` has given agents the last seven verdicts and a streak warning since S32 | re-reading `mad_protocol.py` (R12) |
| CLM-1112 (Teenager Standard 4) NOT BUILT | the PHI-003 gate in `escalation_scorer.py` and `self_bias_gate.py` guard the escalation number | the post-ship search (R-S112-2) |
| the philosophy extract holds every founding rule (28) | `phi_compatibility_check.md` carries NN-PHI-8, the Duty Clause, OPEN since S43 | the same search |
| the historical correlation context is fed to the analysis (R10 note, the guideline review) | `main.py` attaches it after `analyze()`; the LLM never reads it | reading `main.py` (R11) |
| CLM-1116 (NN-3) BUILT on one writer of the source weights | two writers; the quality score was the second (now off) | listing every writer (R12) |
| DECISION S112-3, three cert lines and the mission's (c) were "lost" (the first close draft, its dry run executed) | the session transcript held all of them verbatim | the operator showed the record (R-S112-1) |
(Also wrong: R7's first sweep found 6 of 8 placeholder sites; the guard called a TLS failure "origin/main moved"; a stale screenshot
read as current; the edit applier's false "done" (two causes); C5 flagged my own integer literals in C20; family 96 first designed as an
empty ledger; the first harvest assumed data before May - R-S67-2 already said read the epoch (the DB starts 2026-05-24); `git reset
--hard` on the container's tree (restored from its tree object); CLM-1127/1131 notes without the S34 history; CLM-1111/1125 and
CLM-1127 notes understate the code; a selection-frequency alert called "needed" while `_check_source_dominance` runs daily; ISO/IEC/IEEE 29148 cited from its abstract; prebunking gains cited without the reanalysis that
contests them; roadmap 5's R5-4 written as a new gate; a failure test written with a syntax error; at least four lettered proposals
after the compaction carried no `LINEAGE:` line, and those before it cannot be checked.)

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- CARRIED (eighteenth): **LF/CRLF on a Windows clone.** Never md5 a checked-out file; compare EOL-normalised. *Expires with 5.21.*
- CARRIED: **`--stdout` on any `tools/*.py` needs `PYTHONIOENCODING=utf-8` on Windows.** *Expires with 5.22.*
- CARRIED: **the pre-commit guard blocks on UNTRACKED files** (*expires when it scans the index only*); **the order's second scan reads ANY `digits.digits`** (*5.51*).
- CARRIED: **a copy change mints claim units** needing a verdict row and a binding row. *Expires when CI regenerates it.*
- CARRIED: **the container's GitHub access is LIMITED**; run and secret lists come from the operator's `gh`. *Expires with authenticated access.*
- NEW: **the promise ledger is known wrong in five places** - do not quote its counts as final before S113's mission (a). *Expires when that runner ships.*
- CARRIED: **the backup runs daily at 20:07 UTC and alerts on Telegram when red.** *Expires after seven green scheduled runs* (not counted at S112).
- EXPIRED: the `s111_backup_*` tables (dropped 2026-10-12).
- PROMOTED: R-S112-1..3 and the R-S81-1 amendment; NN-PHI-8 registered from `phi_compatibility_check.md`.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `e3b81a1` + the S112 close commit (verify by ls-remote) TREE CLEAN -- twelve product commits (R4-3 to NUMBERS UNDERIVED 0, the confidence placeholder and C19, R4-4's promise ledger and C20, the founding philosophy and roadmap 5's specification, NN-3), CI green at job level, Vercel success; S111's backup tables dropped
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = **FIRST THE PROMISE LEDGER CORRECTED (NN-PHI-8, CLM-1112, three notes, roadmap 5's spec, a check holding `QUALITY_FEEDS_SOURCE_WEIGHTS`), THEN ROADMAP 4'S TEST 2 BY THE OPERATOR IN PERSON, THEN THE RULINGS ON WAIT-4 TO WAIT-8**
ROADMAP = **ROADMAP 4, CLAIMS REVIEWED - rows four of four** (R4-1 `e306e53`, R4-2 `4f303dd`, R4-3 `778d653`, R4-4 `ddd9540`), Test 1 met, Test 2 not run; **ROADMAP 5, FREEDOM FROM FEAR, MEASURED - declared, QUEUED** behind it (`docs/GNI_ROADMAP5_SPEC_S112.md`); CLAIMS = `docs/GNI_CLAIMS_S112.md`, 843 claims, UNREVIEWED 0, NUMBERS UNDERIVED 0
ORDER = `docs/GNI_TARGET_AND_ORDER_S112.md` (highest number = live) is the queue, **generation 32** -- 58 items, CAP 70, ROOT 5 at most 42, ORPHAN RATE 42/58, WAIT-4 to WAIT-8 outside the count; CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`). FIRST MOVE: the corrections runner, built from `docs/GNI_COGWAR_GREYZONE_DISCUSSION_S112.md` section 4
GATE = CONTRACT v11 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a ruling goes into the next commit message, and nothing is called lost before the session's own transcript is read (R-S112-1); absence is claimed only after a search by behaviour, every writer listed and the project's own map read (R-S112-2); a ruling implemented as a switch ships with its check (R-S112-3); a guard reports the cause it measured (R-S81-1 amended); a bound fragment supports only itself (R-S111-5); a cert DISCRIMINATES (R-S90-1); container HEAD equals the operator's before any generator (R-S107-1); a live read proves the NEW build against a control (R-S105-2)

## 8. POINTERS (<=5 lines)
`tools/mk_close_s112.py` is the executable record of this close. The corrections S113 owes, with their bytes:
`docs/GNI_COGWAR_GREYZONE_DISCUSSION_S112.md` section 4. The cert queries: `docs/S112_C1.sql`, `docs/S112_C2.sql`; the DB
harvest, whose two earlier windows found the epoch: `tools/gni_db_harvest.sql`. Roadmap 5: `docs/GNI_ROADMAP5_SPEC_S112.md`. The
S112 runners (outside the repo) keep the S110 pattern, with origin's reachability now tested before its position.

## DIARY S112
NUMBERS UNDERIVED reached zero, the ledger got built, and the founding philosophy went into it. Then the operator asked
what the cognitive-warfare discussion meant for GNI, and the search I ran to answer him turned up my own grading errors:
code I had marked absent had been there since S32. The ledger I built to tell the operator how complete GNI is was itself
wrong in five places. Then the close declared a ruling lost that the session record still held; the operator showed it to
me. Searching the repo was not searching the record.
