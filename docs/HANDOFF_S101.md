# HANDOFF S101 -> S102
DATE: 2026-09-05 (UTC) | HEAD: `667bd16` + the S101 docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S100-3; four March-2026
`GNI-R-` ids entered PART 0 this close). **CONTRACT stays v10** - byte-identical to S96, verified
by md5 after the copy, not by name. **Protocol is now v16** (PART C step 9a: the fixture gate runs
at the MISSION commit too, and a check ships with its fixture family).
SIX files ship session-numbered, plus the generated map.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S101.md` (generation 20). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green, not re-measured. L2 MAD: **PERISHABLE - do not quote, run it** (R-S98-2);
  the daily unit is 2 debate + 1 watch. Separate them at JOB level, not by log grep:
  `gh run list --workflow=gni_mad.yml --limit 20 --json databaseId,createdAt,conclusion`
  then `gh run view <id> --json jobs` - debate = `run-mad success`, watch = the reverse.
  Read this session, 2026-08-16 to 09-04, all `success`: newest `33886688564`, `33884251974`.
L3 GPVS: untouched, twenty sessions. L4 Quota: not re-measured. Repo is PUBLIC; Actions minutes
  are not metered, so a quota lever does not exist.
L5 Public: **four commits** - `3b3b54a`, `b7eaab4`, `fc40094`, `667bd16` (plus the S101 docs).
STORAGE: 113/500 MB (S90 figure, not re-measured). Backup: NONE - item 6.5, ten generations.
SCHEDULE: **heartbeat check gap p90 is 11.05 h, bound published at 12 h** (window 08-27..09-03).
PLATFORM: 9 workflows. SECRETS: 22. LIFECYCLE clocks PAUSED (DECISION S92-2).
Target: TRUTHFULNESS OF OUTPUT, unchanged. **ROADMAP 2 IS COMPLETE, 4 of 4.**

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| MISSION DONE | ARCHITECTURE section 10 is an SLO + error budget + POLICY | `b7eaab4` |
| new section 4 row | ITIL SLM - external dependencies. First entry: GitHub's scheduler | section 4 |
| **the break has a date** | delivery collapsed 2026-08-26/27, **nothing of ours changed** | `git log` empty |
| **corroborated** | an unrelated public repo reported the identical break on the identical days | web |
| the promise | **GNI promises to tell the truth about its cadence, not to have one** | 10.0 |
| bound = 12 h | DERIVED as the smallest whole hour inside a 0.10 budget, not chosen | 10.3 |
| **SLO-1 VIOLATED** | `monitoring_pipeline.py:317-320` returns before it opens a connection | 10.3 |
| the measured cost | check p90 7.31 -> 11.05 h; worst gap 11.30 -> **30.61 h**; run says `success` | 10.2 |
| `C7` | reads SLO-CFG from the doc, windows by AST, `quantf` from `gni_runtime` | `gni_rule_checks.py` |
| cert, 4 ways | bound 11 FAIL, bound 24 FAIL, window spanning FAIL at 6.47, past-snapshot EXIT 2 | run locally |
| items CLOSED | **5.37**, **6.8** (root cause), **6.11** (answered per regime) | order gen 20 |
| RULES | `GNI-R-114/115/116/122` registered in PART 0 verbatim; manifest 8 rows -> 6 | `3b3b54a` |
| CI | job level at `fc40094` - `harnesses` + `rule_checks` both green | run `33957035842` |
| NEW ITEMS | **EIGHT.** 5.46-5.49, 6.12-6.14, 9.21. rho = **3/8** | order gen 20 |
| the order counts itself | `mk_order_s101.py` runs both published commands BEFORE writing | 64 = 64 |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S101.md` - generation 20, dated, superseding. **64 items**,
with TWO differently-shaped counting commands printed beside the number. **They no longer depend on
a human.** The generator ran both on the ASSEMBLED bytes and refuses to write when they disagree;
it caught carried item **5.18** citing both ids it was retiring, which is the exact failure that
cost generations 18 and 19 a rewrite each. The GRAVEYARD still has SEVEN rows, md5
`3e8ac222c6ef212261676c02d7d56f6f` - a **fifth** generation publishing the same value, carried by
bytes and verified from the assembled file. S102's MISSION is at the top of that file and **was not
declared by James**: the policy in ARCHITECTURE section 10 selected it.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Does removing the standdown actually lower the published bound? | not measured | 6.12 - the mission's own DoD |
| Do any public pages state a monitoring cadence at all? | never read | 9.21 - read them |
| Why is POST suppression 29% when the windows cover 17.7% of the clock? | not separated | 5.49's sibling in 10.7 |
| Are the 22 unreferenced modules reachable from a workflow? | measured one half | join 5.3 against section 7 |
| Do the 36 hidden assertions PASS? | never run | `python -m pytest ai_engine/tests/` LOCALLY |
| What IS the value of `GROQ_MAD_MODEL`? | unknown since July | a run log's model string |
| Would consolidating the `sys.path` roots break imports? | never attempted | 5.38 - wants a ruling |
| Is `GNI-R-115`'s interval table anywhere in the tree? | searched, not found | read `adaptive_pipeline.py` |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| the published bound is 8 h | I counted RUNS; a run inside a protection window checks nothing | recomputing on CHECK gaps |
| five figures in the draft section 10 | I wrote my own quantile; the repo owns `quantf` and they disagree | R-S96-3, forced import |
| POST had 43 runs | I never measured that number, I estimated it | R-S54-2, on re-derivation |
| finding a lost rule id lets you cite it | registration is a separate act | **C1**, on a live document |
| C7 was ready to ship | a check with no fixture family has no control probe | **CI**, at `b7eaab4` |
| the anchor was `compare the two halves'...` | `compare` ends the PREVIOUS line | the patch script refusing |

## 6. TRAPS (<=8 lines) - TEMPORARY ONLY, each with an expiry
- SEVENTH CARRY: **a fresh clone on Windows can present a whole document as changed** - LF/CRLF.
  Use `git diff -w`, and **never md5 a checked-out file** - hash what a tool just wrote, or
  normalise with `.replace(b'\r\n', b'\n')` first. *Expires when 5.21 ships.*
- NEW: **`docs/gni_runtime_snapshot_S99.json` is named S99, stamped with an S98 HEAD, and holds
  data through 2026-09-04.** `C7` and section 6 both read it. Do not trust its name.
  *Expires with 6.14.*
- NEW: **`--limit` truncates from the OLD end.** `gh run list --limit 100` on the heartbeat cut
  the window at 2026-08-24 and reported a day as `6/48` that was `28/48`. Check whether the
  returned count equals the limit before believing the oldest day. *Expires with 5.48.*
- CARRIED: **`gni_runtime.py --stdout` needs `PYTHONIOENCODING=utf-8` on Windows** or it exits on
  a cp1252 encode. The file-writing path is safe. *Expires with 5.22.*
- EXPIRED, do not carry: staging a new tool before regenerating section 5. Now Protocol v16 law.

## 7. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `667bd16` + the S101 docs commit (verify by ls-remote) TREE CLEAN -- four commits, THREE order items closed, eight opened
TARGET = TRUTHFULNESS OF OUTPUT, unchanged; MISSION = item **6.12**, THE WATCHER THAT CHECKS NOTHING: remove the standdown that suppresses a zero-Groq escalation check, certify against a stored case where the old code returned early, and show the published freshness bound FALL -- or say in writing why it did not
ROADMAP = ROADMAP 2 IS COMPLETE, 4 of 4 (S98 detector -- S99 section 6 -- S100 section 5 -- S101 SLO). There is no roadmap row left to rank, and **this mission was selected by the POLICY in `GNI_ARCHITECTURE` section 10, not declared by James**: a cause of lost freshness that IS ours outranks the next mission without a ruling. That is the first mission this repo chose by law
ORDER = `docs/GNI_TARGET_AND_ORDER_S101.md` (highest number = live) is the queue -- 64 items, TWO counting commands printed beside the number and the GENERATOR runs both before it writes; CARRY THE GRAVEYARD (7 rows, `3e8ac222c6ef212261676c02d7d56f6f`, fifth generation). FIRST MOVE: read the mission block, then rule whether `GNI-R-122` is amended, scoped, or left with the heartbeat exempted at the call site
GATE = CONTRACT v10 `LINEAGE:` on every lettered proposal AND every finding (R-S89-1); a cert must DISCRIMINATE (R-S90-1); an instrument checks its own expectations with a control probe (R-S93-1) built from the REAL tree's bytes (R-S100-1); verification is computed BEFORE the write (R-S95-1); a checksum without its command verifies nothing (R-S96-2); a published hash is EOL-normalised or it is platform noise (R-S98-3); a counting command counts what it matches (R-S98-6); an instrument bounded by what it measures reports its smallest answer where the truth is largest (R-S99-1); a fix is not shipped until the recipient has verified the bytes (R-S100-3)

## 8. POINTERS (<=5 lines)
`tools/gni_rule_checks.py` now holds SEVEN checks; `C7` reads `- SLO-CFG KEY: \`value\`` lines out of
the live ARCHITECTURE, `PROTECTION_WINDOWS` out of `monitoring_pipeline.py` by AST, and its quantile
from `gni_runtime.quantf` - it holds no number of its own because `C5` forbids one. Its fixture
families are `15-slo-bound-not-derived` and `16-slo-window-spans-regimes`. Regenerate in this order:
stage -> `gni_blocks.py` -> `gni_state.py` -> `gni_macro_map.py` -> detector -> **fixture** -> commit.

## NOTE ON THIS FILE'S OWN SHAPE
S99 shipped ROADMAP and GATE in place of PART B's TRAP and FIRST MOVE; S100 carried that shape and
said so; this file carries it a third time. FIRST MOVE is folded into the ORDER line, TRAP is
section 6. Three closes is no longer a deviation, it is the practice, and the template still says
otherwise. **This is now item 5.49's sibling and should be ruled or the template changed** - a trap
copied forward unchanged three times has become an unregistered rule. It is not filed as an order
item because it is about this document, not about GNI.

## DIARY S101
Five of my own claims died this session and every one died the same way: I compared what I
remembered against what I had written, instead of against the bytes. The bound was eight hours
because I counted runs and a run inside a protection window checks nothing. Five figures in the
draft were computed with a quantile I wrote from memory while `gni_runtime.quantf` sat two
directories away. One number - forty-three runs - I did not measure at all; I estimated it and
typed it into a table. I read the S99 record that says finding a lost rule id is not permission to
cite it, recovered four ids, and cited one in a live document before registering it. And I added a
seventh check to a detector whose fixture I had never opened.
What is worth writing down is which of those reached James. Two did. The other three were caught
by things this repo built on purpose: C1 refused a citation, CI refused a check with no probe, and
the patch scripts refused their own anchors twice. The machinery is now faster at catching me than
I am at catching myself, and the honest conclusion is that the discipline I actually kept was
running every patch script against real bytes before sending it - and the failures clustered
exactly where I skipped that, in the inline commands I typed straight into the chat.
The best thing here is not the SLO. It is that S102's mission arrived without James declaring it.
