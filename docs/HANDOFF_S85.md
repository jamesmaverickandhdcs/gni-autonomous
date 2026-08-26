# HANDOFF S85 -> S86
DATE: 2026-08-26 | HEAD: `228634c` + THIS docs commit (verify by ls-remote) | MODEL: Opus 5
Read ONCE. Standing rules: docs/GNI_RULES.md by ID (current through R-S85-6). CONTRACT v7.
**The QUEUE lives in `docs/GNI_TARGET_AND_ORDER_S85.md` (generation 5). This file is STATE ONLY.**

## 1. STATE (<=10 lines)
L1 Pipeline: green. ~14 runs/day. `available` ran 193-234 across the four harvested debates.
L2 MAD: ARB-DRYRUN live since `5a20277`. **`228634c` changed the arbitrator's intake — UNCERTIFIED.**
L3 GPVS: untouched, four sessions running. L4 Quota: C1's real bill STILL unread since Jul 27.
L5 Public: `/methodology` + `/about` fixed this session; `/debate` still publishes R1; `/comparison`
  may still render "Both signals point BEARISH" over a NEUTRAL verdict (S69 flag F14, unresolved).
STORAGE: 113/500 MB, runway 520-660 days. Backup: NONE — `LAST BACKUP: No backups`.
Live watch: **the first debate after `228634c`.** Debates land ~03:3x-03:5xZ and ~11:0x-11:2xZ;
  the 11:4xZ run is the grounding-watch (no ARB-FIT).
Target: TRUTHFULNESS OF OUTPUT — definition of done now has FIVE items, not four.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `228634c` | 1.3 SHIPPED: arb ctx built at `depth=0`; `ARB-FIT ctx_depth` echo unhardcoded | 2+/2-, anchors 1/1, COMPILE OK |
| n=4 | `arrived=20`, `GEO=15/15 FIN=6/15 TECH=0/N` on ALL FOUR runs, `available` 193-234 | 4 run logs, two instruments |
| TECH | Pillar zeroed EVERY run — S84's "maybe a GEO-dominant artifact" is ANSWERED: no | dryrun `pillars` lines |
| Margin | depth=0 spare chars 420 -> 367 -> 190 -> **177** as assembled 36->38; ~124 chars/article | greedy sweep, 4 runs |
| Ship gate | `_grounding_basket = all + weak` = FULL basket, so arb depth cannot weaken the gate | `mad_protocol.py:738` bytes |
| Cross-check | Browser log zips matched `gh run view --log` to the digit on all shared fields | two independent paths |
| `2afec7b` | `/methodology` stops naming a decommissioned model | 2+/2-, live fetch confirmed pre-fix |
| `bb9e299` | `/about` drops `(Llama 3)` — closes S69 flag F5's UNPAID half | 1+/1- |
| F5 | Named TWO sites, folded into CLIFF scope, CLIFF DECLARED ACHIEVED at S81 with one live | census + certification files |
| 1.10 | ANSWERED: five call sites DO read a declared fallback | `grep -rni fallback` on ai_engine |
| 1.12 | But `grep -rni 'fallback' .github/` = **0**: the secret never reaches CI | count-first grep |
| D-11 | 109/110 scored reports = escalation **10.0** — promoted to ROOT 8 | DEBT_REGISTER_S69, S74 append |
| Register | `docs/DEBT_REGISTER_S69.md` unread since Jul 17; found by accident | no doc cites it |
| Workflows | `gh workflow list --all` = **8, all active**; six pages say "4" | CLI + 6 grep hits |
| v7 | LINEAGE-BEV enters the GATE SEQUENCE, before PROPOSE | ruled by James |

## 3. ORDER
**MOVED.** See `docs/GNI_TARGET_AND_ORDER_S85.md` — generation 5, dated, superseding.
Do not re-derive a queue from this file. Do not fold items forward without re-ranking.
NEXT SESSION'S MISSION is declared at the top of that file.

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Did `228634c` do what its commit body predicted? | 0 runs | S86 mission — five predictions + 1 failure test |
| Does `GROUNDING SHADOW` arb_hits rise after the change? | unmeasured | same cert; a rise REFUTES the ruling |
| Is `bool(mad_bull_case)` still leaking success past the veto? | docstring says closed, chain says no | 1.8 — read L275-295 |
| What is the VALUE of the `GROQ_MODEL_FALLBACK` secret? | never read | do not wire it before reading it |
| Are `gni_graph`/`market`/`selfbias`/`selfcheck` "pipelines"? | vocabulary, not fact | 9.3 — James rules |
| C1's real token bill (predicted 60-75K vs July's 91-93%) | unmeasured since Jul 27 | the `groq_quota` TELEGRAM line |
| Why does MSYS `grep` drop `--include` beside a variable of excludes? | reproduced, uncaused | trap, expires on diagnosis |
| Do S69 flags F2/F3/F8/F9/F12-F15 still fire on the live site? | unaudited since Jul | 9.5 |

## 5. WRONG THIS SESSION (<=6 lines)
| Claim | What was true instead | Caught by |
|-------|----------------------|-----------|
| **Proposed A/B/C on the arb budget and leaned round-robin** | DECISION S83-1 had ALREADY ruled the direction (per-article cost) and reasoned that ordering fixes cannot raise a stable share. James chose C **because I urged it** and said so | James telling me twice to read past records; then reading [[gni-s83]] |
| "`gni_mad.yml` never passes `GROQ_MAD_MODEL`" + a whole FMEA story on it | It is there at L60. My grep pattern `'GROQ_MODEL'` cannot match `GROQ_MAD_MODEL` | the bytes, one block later |
| "S80 shipped 2 of the 6 planned default sites" / "only one corpse default remains" | Four of six were paid; TWO corpse defaults remain, and I had one of them on screen | `MODEL_CLIFF_AUDIT_S60` + the M grep |
| "B1==B2 byte-identical ⇒ zero `fallback` in json/yml/yaml"; also `2>/dev/null` on a presence check | `--include` was silently dropped, so identical bytes proved the FILTER never ran; and a redirected error is not silence | `.md`/`.ts` paths inside a supposedly `.py`-only file |
| The model census was complete; "35 pages" contradicts build's 40 | Case-sensitive `-e 'llama'` missed `'Groq API (Llama 3)'` — F5's second site. 35 pages and 40 build routes have different denominators | `-i` re-run; S69 census; James's own route list |
| Two smaller ones: an idempotency guard that ABORTed on pre-existing text; `cd ~/path/to/...` invented at the first block | Guard must test the ANCHOR's absence, not the sentinel's presence; never invent a path | the shell, immediately |

## 6. TRAPS (<=8 lines) — TEMPORARY ONLY, each with an expiry
- ARB-DRYRUN's per-pillar counts can include a truncated partial line, so the pillar sum can
  exceed `arrived` by one — expires when the cert shows `truncated=0` (which `228634c` should).
- `_arb_asm` counts lines in the FULL built context, so `fits=N/assembled` is never against
  `available` — expires when 1.7 lands.
- MSYS/MINGW `grep` silently IGNORES `--include` when the command also expands an unquoted
  variable of `--exclude-dir` flags; a standalone `--include` works. Pass explicit PATHS on any
  census that matters — expires when the cause is identified.
(PROMOTED at this close: R-S85-1..6. RETIRED: the `gh run view --log` TLS trap — 5/5 exit 0 this
 session, and the browser zips matched the CLI to the digit.)

## 7. LOAD CHECK — next AI echoes EXACTLY these 5 lines, nothing more
HEAD = the S85 docs commit (verify by ls-remote; `228634c` was HEAD before it) TREE CLEAN
TARGET = TRUTHFULNESS OF OUTPUT; MISSION = certify `228634c` vs its 5 pre-registered predictions + the arb_hits failure test, then open ROOT 8
ORDER = `docs/GNI_TARGET_AND_ORDER_S85.md` (highest number = live) is the queue — regenerate, never fold forward
GATE = CONTRACT v7: every lettered proposal carries a `LINEAGE:` line, or it has not been made
FIRST MOVE = `date -u` + git status + ls-remote; then count unread MAD debates by RUN ID, not by content

## 8. POINTERS (<=5 lines)
Instruments: `ai_engine/analysis/mad_protocol.py` (1311 lines) — arb ctx build L984, fit ladder
L1032-1045, ARB-FIT L1046, ARB-ARRIVAL L1051-1082, ARB-DRYRUN L1084-1149, `_assemble_arb` L1013.
Grounding basket L738. Success chain: `mad_runner.py` L275 `_compute_mad_succeeded`, L582, L651.
Unread registers: `docs/DEBT_REGISTER_S69.md`, `docs/SUBPAGE_IC_CENSUS.md`, `SUBPAGE_CERTIFICATION.md`.
Close/open prompts: `docs/GNI_Session_Transfer_Protocol_S85.md` PART C / PART D (v5).

## DIARY S85 (<=10 lines)
Twice today James had to tell me to read the past. The second time cost more: I put three
options in front of him, leaned on one, he picked it -- and then told me plainly that he picked
it because I urged it. When I finally read the record, the direction I had urged was the one he
himself had ruled against two sessions earlier, for a reason the day's own numbers confirmed.
Nothing was lost but a decision, and a decision is not nothing. The gate we wrote out of it is
deliberately not about my memory; it makes the absence of a read something HE can see, because a
gate firing only inside my head has now failed him twice. The other thing I keep turning over is
the debt register: 131 lines of careful archaeology, appended twice, then read by nobody for ten
sessions, sitting three feet from every question we asked today. We are good at building
instruments and bad at building the thing that reads them. That one is still unfixed.
