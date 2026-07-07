# HANDOFF S58 -> S59
DATE: 2026-07-07 | HEAD: `2890b10` (verify ls-remote; a rules commit `79c8aed` and 2 fix commits precede it) | MODEL: Fable 5 (full session)
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S58-1). Contract: docs/CONTRACT.md (unchanged).
Do not re-read old audits/handoffs unless a queue item points there.

## 1. STATE (<=10 lines)
L1 Pipeline: healthy, Jul-7 morning SUCCESS 13918 tokens; I3-c LIVE-PROVEN (Tech 4/4: Krebs 1, Ars 2, IEEE 1).
L2 MAD: morning clean (93.3% quality, neutral 0.57) despite 5x 429 waits; 87011 real vs solver est 87186
  = 0.2% error THIS run (challenges "overshoot ~10%" claim -- recalib datapoint for I1, do not act early).
L3 GPVS: verifier LIVE-TRUSTED (run 1 of 2 banked: dry-run + --apply + browser all agree; 8 judged
  NOT_MATERIALIZED, SPY +2.41%, fossil=0 correctly). Predictions page: 390/164/226 (52 correct).
L4 Quota: 94% storm burn Jul-6 night (morning 93958, evening 92492) -- consistent with CRITICAL, not a bug.
L5 Public: F1+F3 fossils dead (browser-verified); predictions-list API now filters fossil_error_row
  (null-safe .or), feedback/predictions/reports reconciled to the row; export/predictions RAW by design.
Validation-log page prose honest; its stat cards remain a hardcoded stub (hydrate post-I2-w, see W11).
Live watch: Iran-US CRITICAL 10/10 ongoing. MAD hallucination audit vs forensic trace: 8/8 claims CLEAN.

## 2. DELTA (<=15 lines)
| Commit | What | Proof |
|--------|------|-------|
| `abaed45` | F1: validation-log "verifier is offline" -> S57 truth (restored/manual/backfilling) | browser-verified |
| `a956094` | F3: Q3/Q4 badges (migrated to about/feedback L51-52) -> "(planned)" | browser-verified |
| `79c8aed` | R-S58-1 appended to GNI_RULES.md (binary-mode-only patching) | tail shows rule |
| `2890b10` | W10: predictions-list excludes verified_by='fossil_error_row' via null-safe .or filter | live 390/172/218 then 390/164/226 post-verifier |
Root causes: (1) W10 leak = verified_at written on quarantined rows (verifier uses it as processed-flag);
feedback counted !!verified_at as "verified" -> 18 fossils inflated 236. Fixed at API choke point, 3 pages
inherit. (2) F3 quarter badges had MIGRATED from reports (already FUTURE) to feedback SWOT strings.
(3) My F1 patch text-mode-normalized whole-file endings -- caught same turn, gave R-S58-1; F3 onward rb/wb.
No-commit: verifier --apply run (8 verdicts persisted, DB not repo); mid-session MAD added 5 rows
(SQL-confirmed, explains 403->390 arithmetic); export sibling audited SAFE (ships verified_by column).

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| U-AUG9 | MARATHON unchanged (see S57 handoff row verbatim): keyfile -> U3 baseline x3 -> U1 -> probes -> U2 migrate -> I1 -> copy sweep. Cliff Aug 16. ADD to I1: solver 0.2%-error datapoint (S58) vs banked ~10% overshoot -- measure before recal. | notepad ../groq_probe_key.txt | James | V(prep) |
| U-W | Weekly July Groq lineup glance (2 min) | Groq models page | James | - |
| I2-w | Verifier cron wiring (2-line patch near gni_pipeline.yml:81) after trusted-run #2 (any later day: dry-run -> --apply -> browser triple-agree) | run verifier dry-run | James | B->V |
| W12 | NEW: "GNI selfcheck run FAILED" crash-looping in Telegram (12:19/2:14x2/4:09/5:45 AM Jul-7). Monitoring that lies about itself. | open one failed Actions run log | - | 50% |
| W11 | NEW: verified_at overloaded (verifier processed-flag AND consumers' "verified"). API shields it now; fix = dedicated status column WHEN validation-log hydrates | design with hydration | James | V(diagnosed) |
| A-VLOG | Hydrate validation-log stat cards (0/Backlogged is hardcoded stub) from CLEAN filtered API; bundle with W11 | after I2-w | James | B |
| O3 | BOM kill intelligence_funnel.py + live pattern count + "81" sweep now FOUR mentions: homepage:1008, developer-hub~82, feedback x2 (Strengths+Threats) | kill BOM | James | L |
| UNK-5 | mad_reasoning honest-text render: today's debate clean; ONE click on a Jul-6 evening debate closes it | sidebar click | - | 90% |
| W9 | Double-down alert path tripwire (unchanged) | next multi-fail day | - | 50% |
| UNK | Arb terminal 429 TPD-vs-TPM: read x-ratelimit on one failed EVENING run (morning Jul-7 429s all recovered -- not evidence) | one log read | - | 80% TPD |
| UNK2 | 180d long-horizon rows eyeball when first mature | when due | - | 60% |
| I4 | Rolling 7-day integrity check (not_mad) | design | James | B |
| O6 | Arc C temporal discovery (LAST, by design) | - | - | B |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| GROQ_MODEL/GROQ_MAD_MODEL/GROQ_MODEL_FALLBACK secret VALUES | 50% | run-log model string or Aug 9 |
| Selfcheck crash-loop cause (W12) -- workflow bug vs env vs quota-check throw | 50% | one Actions log |
| Solver error profile: 0.2% (S58, N=37 D=300) vs ~10% banked -- which is typical? | 40% | next 3 MAD runs' est-vs-real |
| Arb terminal 429 TPD vs TPM | 80% TPD | evening-fail x-ratelimit headers |
| Jul-6 evening debate honest-text render (UNK-5) | 90% | one sidebar click |

## 5. TRAPS (<=8 lines)
- Do NOT reopen: F1/F2/F3/W10/I3-c/I3-b/I2-b/O1/O4/I3-r (closed), L4 consumers, L5 sweep, O5, O2.
- export/predictions stays RAW deliberately (self-describing verified_by) -- filtering it = editing history.
- Verifier's verified_at-on-fossils is its rescan-guard: do NOT "fix" it in the verifier (reopens I2-b);
  the API filter is the shield; real fix is W11's status column, bundled with A-VLOG.
- R-S58-1: patch scripts rb/wb + byte anchors ONLY. Text-mode open() normalizes endings (bit us Jul-7).
- Probe waits for Aug 9; NEVER on morning/evening; FIXTURE_USER frozen; PowerShell >> = UTF-16 poison.
- No solver recalibration before migration (R-S55-4) -- S58's 0.2% datapoint is EVIDENCE, not a trigger.
- Verifier is $0-token (stdlib+Yahoo, grep-proven) -- safe any quota day; needs no venv.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `2890b10`
TOP3 = Aug 9 marathon prep (keyfile!), I2-w trusted-run #2 then cron wire, W12 selfcheck crash-loop read
DEADLINE = Aug 9 marathon / Groq cliff Aug 16
TRAP = don't "fix" verified_at in verifier (it's the rescan-guard; W11 owns the real fix); rb/wb patches only (R-S58-1)
FIRST MOVE = verify HEAD via ls-remote; one click Jul-6 evening debate (UNK-5); then verifier dry-run for trusted-run #2

## 7. POINTERS (<=5 lines)
W10 filter: src/app/api/predictions-list/route.ts (.or between select and order, commented).
W11/A-VLOG anatomy + consumer census: this session's chat "S58" -- feedback filters at page.tsx:27-30.
Verifier fossil/quarantine mechanics: debate_prediction_verifier.py header + line ~173 update dict.
Forensic-trace audit method (hallucination check vs XLSX basket): S58 chat, reusable pattern.
F1/F3 final copy: validation-log/page.tsx:49; about/feedback/page.tsx:51-52.
