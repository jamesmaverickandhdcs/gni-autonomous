# HANDOFF S103 -> S104
DATE: 2026-09-09 (UTC) | HEAD: `60af1a5` + the S103 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES_S103.md by ID (current through R-S103-4).
**CONTRACT stays v10**, byte-identical to S101 and S102, md5 `9e4b804c4923bcd41b9f62766989a046`
(EOL-normalised) verified after the copy, not by name. **PROTOCOL RISES TO v17** - PART B's LOAD
CHECK template is corrected to the shape S99 through S103 all actually shipped, and its
session-numbered paths are swept in the same block. PART A, C and D byte-identical to v16.
SIX files ship session-numbered, plus the generated map already committed at `60af1a5`.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S103.md` (generation 23). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **MEASURED at JOB level** - 09-07 and 09-08 both
  `2 debate + 1 watch`, twelve runs read, all `success`, `run-mad` and `grounding-watch`
  alternating exactly. Re-run it; do not quote it.
L3 GPVS: untouched, twenty-two sessions. L4 Quota: not re-measured. Repo is PUBLIC.
L5 Public: **two commits** - `6c05076` the check, `60af1a5` the regenerated sections and map -
  plus the S103 docs commit. CI green at JOB level on both (`rule_checks` + `harnesses`).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, twelve generations.
SCHEDULE: **bound published at 8 h, window 08-27..09-03, NOT re-harvested this close** - the
  window is frozen history and a re-harvest cannot move it. Heartbeat delivery measured separately
  over 08-31..09-09: 60 runs, 6.70/day, p90 5.30 h. That is a DIFFERENT window; do not compare it
  to the published 4-of-40 without re-deriving.
PLATFORM: 9 workflows. SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2).
Target: TRUTHFULNESS OF OUTPUT, unchanged. Detector: **7 checks green**. Fixture: **21 families**.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | `C6` reads EVERY `INPUT ... md5` line the map declares | `6c05076` |
| the defect was DIRECTION | the INPUT pattern was interpolated from the stamp that names the register | `re.escape(stamp...)` |
| live, not named | each input resolves to the LIVE file of its family; a rename is caught with no md5 involved | `20-map-arch-renamed` |
| cert on REAL commits | `b7eaab4`: old detector PASS 7/0, new detector FAIL naming `a4fb9fce` vs `0d944f64` | one tree, two instruments |
| the S102 md5 pair | recovered from `git show`, not from prose - the exact numbers the S102 record captured | `git show 3268c14:...` |
| second cert shape | `3268c14`: `map read _S99.md; the live is _S100.md` - liveness, no md5 in the message | rename |
| it fired UNPLANNED | on the LIVE tree between the generators and the map run, exactly as S102 described | `60af1a5` message |
| **§5 was already stale** | S102 stamped `86 tracked *.py`; that close's tree held **89**. Nothing saw it | `git ls-tree` 86/89/90 |
| fixture could not fail | `_map_text` emitted ONE input line, so no family could cover a stale architecture | 5.53's kin |
| order matters in `base()` | the SLO block APPENDS to the architecture after the map was stamped | map now written LAST |
| row four from bytes | half closed, half not, and DECISION S103-1 written into the document | `60af1a5` |
| **SLO-1 CLOSED** | post-fix run in a protection window logs all three checks executing | `34335454766` |
| `GNI-R-118` acquitted | it suspends the ADAPTIVE pipeline AFTER the checks - `GNI-R-114`'s own subject | same log |
| **C1 caught the close** | `GNI-R-118` is registered nowhere, and the register has cited it since S102 | item 5.57 |
| the order counted itself | 69 = 69, after REFUSING once at 69-when-68-was-declared | a closed id cited inside THE ORDER |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S103.md` - generation 23, dated, superseding generation
22. **69 items**, with the same TWO differently-shaped counting commands printed beside the number,
both run on the assembled bytes before the write. They refused to write once, at 69: item 5.54's
draft cited **5.50** by number inside `## THE ORDER`, and a closed id cited in the queue counts as
a queue item. That is the failure generations 18, 19 and 20 each shipped and rewrote afterwards;
this is the first close where it never reached the file. The generator is STILL a stand-in written
for the occasion, for the second generation running, because `tools/mk_order_s101.py` is not in the
tree - item 5.51. The GRAVEYARD still has SEVEN rows, md5 `3e8ac222c6ef212261676c02d7d56f6f`, an
**eighth** generation publishing the same value, carried by bytes and hashed with its PUBLISHED
command. S104's MISSION is at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Does the published bound hold on a MOVED window? | never asked | a deliberate re-harvest, ruled first |
| Where is item **5.12**'s text? | absent from `_S95.md` | 5.56 - search generations before S95 |
| Do any public pages state a monitoring cadence at all? | never read | 9.21 |
| Does section seven go stale when a SECRET changes? | reasoned, unmeasured | the ruling at S104's open |
| Which other detector branches does the fixture never enter? | two found, rest unasked | 5.53 |
| Why is POST suppression 29% when windows cover 17.7% of the clock? | not separated | 5.49's sibling |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| the S102 silence exists at no commit boundary | it exists at four, one carrying the S102 md5 pair exactly | `git show` - I had read four commit messages instead of measuring four trees |
| a re-harvest could exhaust the error budget | the published window is frozen history; two harvests three days apart agree digit for digit | the handoff line I echoed myself at the open |
| tracked `.py` will be 87 | **90** - and the gap exposed that §5 had shipped stale at S102 | the generator's own output |
| the S102 CANDIDATE commits are S102's | all four are S99-S101; the number matched and the reason was wrong | reading the scan instead of the count |
| log fetch failed / step names differ / the `sed` range is wrong | all three wrong; `gh` labels the steps `UNKNOWN STEP` | writing the log to a file and counting |
| three shell instruments built from structure assumptions | `awk` dynamic regex ate `**`, `grep` read `-` as a flag, a `grep -E` cert hid the exit code | running them |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- NINTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  Use `git diff -w`, and **never md5 a checked-out file** - hash what a tool just wrote, or
  normalise first. The register is CRLF; the order and architecture are LF. *Expires with 5.21.*
- CARRIED: **the generators count the INDEX but stamp HEAD.** Commit first, then regenerate, then
  commit again. This is what made §5 wrong by three at S102. *Expires with 5.52.*
- CARRIED: **`gni_runtime.py --stdout` still WRITES the snapshot.** Not a dry run. *Expires when
  the flag is fixed or documented.*
- CARRIED: **`--limit` truncates from the OLD end.** Check the returned count against the limit
  before believing the oldest entry - it decided a real reading this close. *Expires with 5.48.*
- CARRIED: **`gni_runtime.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows.** *Expires with 5.22.*
- NEW: **MINGW64 gives bash a `/tmp` that Windows Python reads as `C:\tmp\`.** Write scratch files
  into the working directory. Same family as `python -m pip`. *Expires when a `tools/` helper owns
  temp files.*
- EXPIRED, do not carry: "the map must run after the section generators **and `C6` will not say
  so**." The ordering still holds; the SILENCE does not. `C6` now says so, and said so on the live
  tree this session.
- PROMOTED, do not carry: "a published checksum is its command." It was already R-S96-2; carrying
  it as a trap was a duplicate home. Cite the rule.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `60af1a5` + the S103 docs commit (verify by ls-remote) TREE CLEAN -- two mission commits, ONE order item closed, three opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = item **5.54**, GIVE SECTIONS FIVE AND SIX A STALENESS CHECK: derive each generated section's DECLARED fingerprint from the live tree and go RED when they disagree, with no count of sections written anywhere; one fixture family per failure shape; replay §5's S102 staleness as the cert against the real commit that carried it; update row four from bytes; then declare roadmap 2 four of four WITH evidence, or NOT ACHIEVED with the reason. **This is the LAST unmet half of roadmap 2's row four**
ROADMAP = **ROADMAP 2 IS 3 OF 4.** Row four is HALF closed: the macro-map half shipped at S103 as item 5.50, the sections five and six half has never had a check and is item 5.54. DECISION S103-1 read the row as written - it names four surfaces, the S98 table recorded §5 and §6 as ABSENT rather than excluded, and the row's own published command settles it, since flipping a §5 figure today still exits 0. DECISION S103-2 binds the other side: **roadmap 3 begins at S105 whatever happens**, and if 5.54 has not closed by then roadmap 2 is DECLARED NOT ACHIEVED with the reason written down. A plan needs a completion test, including ours
ORDER = `docs/GNI_TARGET_AND_ORDER_S103.md` (highest number = live) is the queue, **generation 23** -- 69 items, TWO counting commands printed beside the number, both run on the assembled bytes BEFORE the write by a stand-in script for the second generation running because the real generator is not in the tree (5.51); CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`, eighth generation, hashed with its PUBLISHED command). FIRST MOVE: read the mission block, then rule whether 5.54 must also cover section seven's SECRETS, which its workflow manifest does not hash
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1) -- S103 shipped three of four proposals without one, so check yourself; a cert must DISCRIMINATE (R-S90-1); an instrument checks its own expectations with a control probe (R-S93-1) built from the REAL tree's bytes (R-S100-1); verification is computed BEFORE the write (R-S95-1); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches (R-S98-6); a check must not derive its target from what the target names (R-S103-1); a filtered cert prints its exit code (R-S103-2)

## 8. POINTERS (<=5 lines)
`tools/gni_rule_checks.py` holds SEVEN checks and now three module helpers - `live_map_path`,
`map_inputs`, `stem_of` - plus `_probe_halts`, which `control_probe` calls TWICE. `C6` loops over
`INPUT_RE` matches and compares each against `ctx["docs"][stem]`. `tools/patch_s103_c6.py` and
`tools/patch_s103_row4.py` are the executable record of how those bytes changed. Order that worked:
`git add` the tool -> commit -> `gni_blocks` -> `gni_state` -> `gni_runtime` -> row-four patch ->
`gni_macro_map` LAST -> detector -> fixture -> commit.

## DIARY S103
The mission was one line of regex. `C6` was believed to read one of two inputs because it
hard-coded a count; it did not, and no count was ever involved. It built its search pattern by
interpolating the name of the file it was about to search for, so the second input could not have
matched however many there were. Fixing a count would have fixed nothing. That distinction cost
two hours of reading and it is the only reason the fix works.
The rest of the day divided cleanly in two, and the division is the thing worth keeping. On the
mission I read bytes before every move, and every prediction held: the fixture's blind spot, the
ordering hazard in `base()`, the two cert shapes, the counting refusal at 69. On the diagnostics I
guessed explanations first, and I was wrong ten times - three of them consecutive shell predictions
inside five minutes, each one an instrument built from an assumption about structure rather than
from a look at the bytes. Same session, same person, opposite results, and the only variable was
whether I measured before I spoke.
Two things were carried here for four closes and stopped today. A paragraph recording a debt, which
four closes read and deferred because prose has no rank; it is now an item with a number. And a
template that had described a shape nobody shipped since S99, which two closes named and neither
ruled. The instruments this repo builds catch the things it points them at. What it has never had
is anything that notices when an obligation stops being pointed at, and both of today's carries
ended the same way - not because a check fired, but because someone finally asked the file a
question it had been quietly failing to answer.
