# HANDOFF S104 -> S105
DATE: 2026-09-10 (UTC) | HEAD: `bc88bd8` + the S104 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES_S104.md by ID (current through R-S104-4).
**CONTRACT stays v10**, byte-identical to S101, S102 and S103, md5 `9e4b804c4923bcd41b9f62766989a046`
(EOL-normalised) verified after the copy, not by name. **PROTOCOL RISES TO v18** - PART C step 9a's
hard-coded detector count is REMOVED rather than raised, for the reason in its own version log.
PART A, B and D byte-identical to v17. SEVEN files ship session-numbered, plus the generated map.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S104.md` (generation 24). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **not re-measured this session** - the S103 reading
  (`2 debate + 1 watch` on two consecutive days, twelve runs, all success) is the last one; re-run
  it, do not quote it. L3 GPVS: untouched, twenty-three sessions. L4 Quota: not re-measured.
L5 Public: **two commits** - `693ac2b` the check, `bc88bd8` the restamped documents. Repo is PUBLIC.
  CI green at JOB level on the pushed tip: run `34423999423`, `harnesses` and `rule_checks` both
  `success`. That is where a claim about the detector is settled; a local green is not one.
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, thirteen generations.
SCHEDULE: bound published at 8 h, window 08-27 to 09-03, **not re-harvested - item 5.60**, and
  moving that window changes a published SLO, so it needs a ruling and not a close-time side effect.
PLATFORM: 9 workflows. SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2).
Target: TRUTHFULNESS OF OUTPUT. **Detector: 8 checks. Fixture: 25 families. ROADMAP 2: ACHIEVED.**

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | `C8` recomputes every generated section's declared fingerprint from the live tree | `693ac2b` |
| **ROADMAP 2 IS 4 OF 4** | declared, dated, archived - the first arc this project has finished | row four + `34423999423` |
| cert: one stamp, two trees | `8ce57fc` exits 0, `a923ad9` exits 1, on a byte-identical §5 stamp | md5 `e1c9488b...` |
| the verdicts came from trees | the stamp is identical in both, so the document cannot have decided it | `git show` + `md5sum` |
| eleven of twenty-four | §5's declared value disagreed with its own tree at eleven commits | `git ls-tree` sweep |
| the nine that agreed | agreed because no tracked module moved, not because anything checked | same sweep |
| ONE DEFECT, TWO NUMBERS | `5.41` (S100) and `5.54` (S103) are the same defect; both close here | queue read |
| §7 by BYTES, not counts | family `24` edits a workflow without moving a count; `C2` passes, `C8` fails | discriminator |
| `gni_state` refactor | `workflow_manifest` lifted out of `main()`; section renders byte-identically | `cmp` exit 0 |
| **the cert failed twice first** | an empty compare, then a truncated one - both reported IDENTICAL | R-S104-2 |
| a renamed generator lies | `SELF` comes from `__file__`; the copy rendered 23 bytes longer | 9645/9622/9622 |
| the order refused once | a bare `6.14` in the queue made the two scans disagree at 70 and 71 | `mk_order_s104.py` |
| S102's own patch was unsafe | it hard-coded a SUPERSEDED generation; the live file was already correct | `_S103` vs `_S102` |
| the protocol went stale twice | v16 raised the count six to seven; v18 removes it | v16 log, v18 log |
| order generator IN THE TREE | `tools/mk_order_s104.py`, first time in three generations - still a stand-in | item 5.51 |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S104.md` - generation 24, dated, superseding generation
23. **70 items**, with the same TWO differently-shaped counting commands printed beside the number,
both run on the assembled bytes before the write by `tools/mk_order_s104.py` - which is committed
this close, which is new, and which still has no control probe, which is item **5.51** and is not.
It REFUSED once, at 70-against-71, because a bare `6.14` had entered the prose inside the queue
range: the second scan exists for exactly that and had never caught anything before. The count FELL
by two for one mission because two ids named one defect. The GRAVEYARD still has SEVEN rows, md5
`3e8ac222c6ef212261676c02d7d56f6f`, a **ninth** generation publishing the same value, carried by
bytes and hashed with its PUBLISHED command. S105's MISSION is at the top of that file, and it is a
PHASE GATE rather than a queue item.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Does the published bound hold on a MOVED window? | never asked | a deliberate re-harvest, ruled first - 5.60 |
| Do any public pages state a monitoring cadence at all? | never read | 9.21 |
| Which detector branches does the fixture never enter? | two found, rest unasked | 5.53 |
| Does any live document cite an order item that does not exist? | never checked | 5.55 |
| Why does `C1` not see ids cited inside the register itself? | measured, cause unknown | 5.57 |
| What is item **5.12**? | no text found in any generation yet | 5.56 |
| Do the hidden assertions under `ai_engine/tests/` PASS? | never run | `python -m pytest` LOCALLY |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| `cmp` says the refactor changed nothing | both files were EMPTY - the generator had exited 2 on a missing `--session` | my own echoed `lines: 0`, ignored |
| the non-empty guard is enough | both files held 68 bytes of a render that died mid-write on cp1252 | PRE/POST exit=1 |
| the cert probe reads the live document | `sorted()[-1]` is LEXICAL, so it read `_S99` at all three commits - while quoting R-S92-2 | `declared: NONE` three times |
| §6 will fail at `8ce57fc` | it passed: stamp and snapshot were BOTH the older generation there | the detector |
| a renamed copy renders identically | `SELF` is built from `__file__`; the copy counted the original as a consumer | 9645 vs 9622 |
| the workflow is `GNI CI Harness` | `GNI CI -- Harnesses` - completed from a truncated column in a run list | HTTP 404 |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- TENTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  Use `git diff -w`, and **never md5 a checked-out file** - hash what a tool just wrote, or
  normalise first. The register is CRLF; the order, architecture and protocol are LF.
  *Expires with 5.21.*
- CARRIED, NARROWED: **the generators count the INDEX but stamp HEAD.** Commit first, then
  regenerate, then commit again. What changed at S104: the CONSEQUENCE is now caught - a stale
  stamp reddens `C8` on the CI run of the push that carries it. The generators still skew.
  *Expires with 5.52, which now carries its closure test in writing.*
- CARRIED, WIDENED TO ITS FAMILY (R-S104-4): **`--stdout` on ANY `tools/*.py` needs
  `PYTHONIOENCODING=utf-8` on Windows.** The S103 trap named `gni_runtime.py`; `gni_state.py` has
  it too, cost a false certification this session, and was already item **5.22**. *Expires with 5.22.*
- CARRIED: **`gni_runtime.py --stdout` still WRITES the snapshot.** Not a dry run. *Expires when
  the flag is fixed or documented.*
- CARRIED: **`--limit` truncates from the OLD end.** Check the returned count against the limit
  before believing the oldest entry. *Expires with 5.48.*
- CARRIED: **MINGW64 gives bash a `/tmp` that Windows Python reads as `C:\tmp\`.** Write scratch
  files into the working directory. *Expires when a `tools/` helper owns temp files.*
- NEW: **`docs/` holds TWO runtime snapshots and `C8` resolves the newest by RELATION.** A harvest
  that lands a newer snapshot without regenerating section six turns the detector RED immediately.
  That is correct behaviour and it will look like a break. *Expires with 5.60.*
- PROMOTED, do not carry: "a program that identifies itself from `__file__` cannot be certified
  against a renamed copy." It is R-S104-3. Cite the rule.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `bc88bd8` + the S104 docs commit (verify by ls-remote) TREE CLEAN -- two mission commits, TWO order items closed on one defect, three opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = **JAMES DECLARES ROADMAP 3, OR DECLINES IT, WITH ITS WRITTEN COMPLETION TEST.** That is a PHASE GATE, not a queue item: Protocol PART C step 4a assigns it to him and DECISION S103-2 fixed the date. If he declines, the mission falls to item **9.21** - no public page has ever been read against the published freshness bound, four generations at the top of ROOT 9 and never once the mission
ROADMAP = **ROADMAP 2 IS 4 OF 4 - DECLARED ACHIEVED AT THE S104 CLOSE, AND ARCHIVED.** All four rows of the completion test in `GNI_ARCHITECTURE` hold, each answerable from bytes by the command printed beside it; row four was the last and closed at `693ac2b` + `bc88bd8` with CI green at JOB level (`34423999423`). This is the first arc this project has run to completion rather than renamed near its end. There is NO declared roadmap 3 until James declares one, and a roadmap without a written completion test is SUBPAGE-IC with a new name
ORDER = `docs/GNI_TARGET_AND_ORDER_S104.md` (highest number = live) is the queue, **generation 24** -- 70 items, TWO counting commands printed beside the number, both run on the assembled bytes BEFORE the write by `tools/mk_order_s104.py`, which is IN THE TREE this close and still has no control probe (5.51); CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`, ninth generation, hashed with its PUBLISHED command). FIRST MOVE: read the mission block, then put the roadmap 3 question to James before touching the queue
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1) -- S104 shipped nine lettered proposals and all nine carried one; a cert must DISCRIMINATE (R-S90-1) and its guards must test the failure mode they guard against, exit code included (R-S104-2); an instrument checks its own expectations with a control probe (R-S93-1) built from the REAL tree's bytes (R-S100-1); verification is computed BEFORE the write (R-S95-1); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches (R-S98-6); a check must not derive its target from what the target names (R-S103-1); a generated section's fingerprint is recomputed by the generator's own code and the number of sections is never written down (R-S104-1); a program that names itself from `__file__` cannot be certified against a renamed copy (R-S104-3); read a trap's FAMILY, not its example (R-S104-4)

## 8. POINTERS (<=5 lines)
`tools/gni_rule_checks.py` holds EIGHT checks; `C8` is `check_c8_generated_sections_fresh` and uses
`arch_stamps`, `live_snapshot_path` and the `ARCH_GENERATORS` registry, which dispatches on the
GENERATOR NAME and raises `InstrumentError` on one it does not know. `control_probe` runs three
probes now. The seven `tools/patch_s104_*.py` and `tools/mk_*_s104.py` scripts are the executable
record of how every byte moved this close; read them before re-deriving any of it.

## DIARY S104
The mission was one loop over three stamps, and it was never in doubt. What the day was actually
about was instruments, and the ratio is the thing to keep: on the mission I read bytes before every
move and every prediction held - the fixture's blind spot, the git-index dependency, the anchor that
would have matched the scoreboard grading the check. Off the mission I was wrong eight times, and
four of the eight share one shape: a guard that tested something ADJACENT to what it was guarding.
A cert asked "is this file non-empty" when the claim was "these bytes are identical", and passed on
two empty files, then on two truncated ones. A probe picked the live document by lexical sort in the
same paragraph where I quoted the rule forbidding it. I completed a workflow name from a truncated
column. I used a line number my own edit had already moved. R-S104-2 is what the first became.
Three things this close were caught by machines rather than by me, and that is the report. The order
generator refused to write on a bare decimal the second scan found. The detector went red on the
close's own documents. And the previous session's proposed patch, written by the session that
documented this exact disease, would have edited a superseded generation - caught because the live
file is resolved by RELATION now and not by name.
Roadmap 2 is finished. Not renamed, not quietly dropped, not declared and left unmeasured -
finished, with a command beside every row that anyone can run. This project has never done that
before, and the reason it could is that S103 refused to read row four narrowly when reading it
narrowly would have ended the arc a week earlier and one row short.
