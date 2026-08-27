# HANDOFF S86 -> S87
DATE: 2026-08-28 | HEAD: `a4514ee` + THIS docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S86-6). CONTRACT v7
(UNCHANGED this close — carry `CONTRACT_S85.md` forward). Protocol v6.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S86.md` (generation 6). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. `available` ran 209-233 on the two post-change runs.
L2 MAD: **`228634c` CERTIFIED — ROOT 1.3 CLOSED.** arrived 20 -> 39/41, TECH 0 -> 9/12.
L3 GPVS: untouched, five sessions running. L4 Quota: C1's real bill STILL unread since Jul 27.
L5 Public: `/debate` still publishes R1; `/comparison` may still render "Both signals point
  BEARISH" over a NEUTRAL verdict (S69 flag F14, unresolved); "4 pipelines" wrong in 6 places.
STORAGE: 113/500 MB, runway 520-660 days. Backup: NONE — `LAST BACKUP: No backups`.
**SCHEDULE MOVED ~9.5h on Aug 27** (03:3x/11:0x/11:4xZ -> 13:0x/20:4x/21:0xZ), cause unknown.
  Never infer debate-vs-watch from the clock — use `ARB-FIT`.
Target: TRUTHFULNESS OF OUTPUT. Item 1 is CERTIFIED but conditional; item 5 (ROOT 8) is now top.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| CERT | `33114821663` meets ALL FIVE predictions exactly; `33075059391` meets 2 | two run logs |
| Boundary | The difference is ONE variable: `assembled` 39 vs 43. At/below ~40 the ladder never cuts | both runs |
| Failure test | arb hits 10 and 10 vs baseline **n=20 mean 8.3 max 13 SD 2.6** — did NOT fire | banked pre-read |
| Baseline | n=20 debates Aug 17-26, all pre-`228634c`, harvested by RUN ID not clock | `gh run view --log` |
| 2.1 | Clause 1 RULED: 8.3 < `~12` trigger, scale error runs SAFE ⇒ **B does not fire** | n=20 + bytes |
| 8.1 | Saturation 3 layers confirmed by bytes; PHI-003 gate muted by its own `combo_bonus < 3` | scorer L60-130 |
| 8.1a | D-11's feeds list MISSES 3 consumers: arb prompt L989, `nexus_analyzer:567`, `self_bias_gate:46` | grep |
| 8.1b | `_high_escalation` True **6/6**; `1da3dfe` shows NN-5 is deliberate design, not a bias bug | 6 logs + subject |
| 8.1c | `constraint=987` of `ctx_room=5091` = ~6-7 articles/run spent by an always-on branch | DRYRUN tiers |
| 7.4 | Per-run shadow line = `len(hits)` (dialect IN); digest and `hit_count` exclude it | L753/L299 |
| 7.1 | `checked_spans` is computed and thrown away at the print — the RATE denominator exists | gate L213/286 |
| 2.3 | bearish 94%->17%, conf 0.794->0.549 over 4 months: a SLIDE, no step at any commit | monthly SQL |
| 3.1 | `conf = 0.5` exactly: Jun **11**, Jul **7** ⇒ contamination wider than the Jul 19-22 window | same SQL |
| F-86-6 | "June Option B" is not in `docs/`; the design is the 2026-03-24 record, called "Fix 2" | grep + record |
| 1.11 | TRIGGER FIRED — `assembled=43 >= 39` AND `ctx-trim@5091` returned | `33075059391` |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S86.md` — generation 6, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Why did the MAD schedule move ~9.5h on Aug 27? | reproduced, uncaused | trap; expires on cause or 7 stable days |
| What causes the 4-month verdict slide? | measured, uncaused | 2.3 — no control exists yet |
| Does `_high_escalation` EVER go False in production? | 0/6 observed | 8.5 — exercise the branch |
| Is `bool(mad_bull_case)` still leaking success past the veto? | docstring says closed, chain says no | 1.8 — read L275-295 |
| What is the VALUE of the `GROQ_MODEL_FALLBACK` secret? | never read | do not wire it before reading it |
| Does 2.1's clause 2 (LABELED coverage) trigger B? | unmeasured | the only thing keeping 2.1 open |
| C1's real token bill (predicted 60-75K vs July's 91-93%) | unmeasured since Jul 27 | the `groq_quota` TELEGRAM line |
| Do S69 flags F2/F3/F8/F9/F12-F15 still fire on the live site? | unaudited since Jul | 9.5 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| Watch runs emit no shadow line, so "the run's name doesn't match what it does" | They emit `Consultant-level hits: N \| Arbitrator-level hits: M` — a digest my pattern could not match. The watch IS the grounding instrument | the digest line, one block later |
| "Two instruments agree to the digit" (per-run 8.3 vs digest ~8.1) | Different counters — dialect IN vs OUT. Near-equality is a finding about dialect, not corroboration | `mad_protocol.py:753` bytes |
| NN-5's Swan+Ostrich-only constraints are "a bias defect" | `1da3dfe` subject: a deliberate hard correction channel for HIGH/CRITICAL. The defect is the stuck switch, not the content | `git log -S` |
| Predicted bullish verdicts existed BEFORE NN-5 and vanished after | Exactly reversed: bull = 0 in May and June, 1 in July, **4 in August** | the monthly cut |
| Built a trend from July's n=2 (S70/S71 shadow lines) | n=2 across an unread code change is not a trend; the order named the right evidence (S83 harvest + S85 runs) and I went elsewhere | re-reading the order |
| Added a schedule note into PART D, and gave a lettered proposal with no `LINEAGE:` line | State in a template is the law-vs-state leak (R-S82-5); a proposal without lineage has not been made (CONTRACT v7) | James asking me to re-read |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- `_arb_asm` counts lines in the FULL built context, so `fits=N/assembled` is never against
  `available` — expires when 1.7 lands. **SECOND CARRY: promote or expire at the S87 close.**
- MSYS/MINGW `grep` silently IGNORES `--include` when the command also expands an unquoted
  variable of `--exclude-dir` flags. Pass explicit PATHS on any census that matters — expires
  when the cause is identified. **SECOND CARRY: promote or expire at the S87 close.**
- NEW: the MAD schedule moved ~9.5h on Aug 27 with no change of ours. Any clock-based reasoning
  about run identity is unsound — expires on cause, or after 7 days of a stable pattern.
(PROMOTED at this close: R-S86-1..6. RETIRED: the ARB-DRYRUN partial-line trap — its stated
 expiry `truncated=0` arrived, and pillar sum 39 == `arrived` 39 exactly on that run.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S86 docs commit (verify by ls-remote; `a4514ee` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = ship 8.2 (`score_breakdown` persistence), then SWOT 8.3 having READ the March-24 design first
ORDER = `docs/GNI_TARGET_AND_ORDER_S86.md` (highest number = live) is the queue — regenerate, never fold forward
GATE = CONTRACT v7: every lettered proposal carries a `LINEAGE:` line, or it has not been made
FIRST MOVE = `date -u` + git status + ls-remote; then count unread MAD debates by RUN ID, and never by the clock — the schedule moved

## 8. POINTERS (<=5 lines)
Instruments: `ai_engine/analysis/mad_protocol.py` — arb ctx build L984, ARB-FIT L1046, ARB-ARRIVAL
L1051-1082, ARB-DRYRUN L1084-1149, NN-5 L986-1004, shadow print L1164-1168, grounding basket L738.
`mad_grounding_gate.py` (429) — `check_grounding` L202, `checked_spans` L286, `hit_count` L299.
`escalation_scorer.py` (191) — signal lists L8-40, `CRITICAL_COMBOS` L42, PHI-003 gate L110-125.
Registers nothing reads: `DEBT_REGISTER_S69.md` (read at S86), `SUBPAGE_IC_CENSUS.md`,
`SUBPAGE_CERTIFICATION.md`. Prompts: `docs/GNI_Session_Transfer_Protocol_S86.md` PART C / PART D.

## DIARY S86 (<=10 lines)
Five times today I said something the bytes then corrected, and four of those were about my own
instruments rather than the system's. The pattern is the same every time: I compared two numbers
without checking they were made the same way. The scorer taught the harder lesson. I read the
saturation, saw the always-on constraint block, saw Black Swan and Ostrich enforced with no
counterweight, and called it a bias defect -- and one commit subject line from May said, plainly,
that a human had designed exactly that, on purpose, for a reason. Then the data said the verdicts
had moved the opposite way from my story. Two corrections in ten minutes, both from records that
had been sitting there the whole time. James asked three times today whether I had read the past
before answering, and three times the answer improved when I did. The gate we wrote at S85 is the
right gate. I am still learning to reach for it before I have an opinion, not after.
