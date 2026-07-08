# HANDOFF S61 -> S62
DATE: 2026-07-08 | HEAD: `6f43aa5` (verify ls-remote) | MODEL: Fable 5 (S61 short session, same-day as S60 close; weekly cap resets Mon 5PM +07)
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S61-1). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
L1 Pipeline: healthy (unchanged from S60 morning: 363/22, quality 8.65).
L2 MAD: G-GATE SHADOW LIVE at `6f43aa5` — 3 seams wired (consultant R1 @~731, R2 @~798,
  arb_final @~886 post-patch), zero tokens, model-independent. ALTER applied (grounding_hits
  jsonb, "Success. No rows returned"). First live shadow data: Jul-9 02:43 UTC MAD.
L3 GPVS: verifier autonomous; FIRST AUTO-RUN Jul-9 10:13 UTC — unverified as of close.
L4 Quota: unchanged watch (evening acct 88386 Jul-7; band 85K).
L5 Public: unchanged. Live: Hormuz/Iran CRITICAL ongoing.
NEW: grounding_watch.py cron 11:13 UTC daily (gni_mad.yml, run-mad guarded off that slot).
LENS: cliff exposure now KNOWN and it is TOTAL (see Delta) — was unknown at S60.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `6f43aa5` | G-GATE CLOSED (shadow): mad_grounding_gate.py (+__main__ specimen tests), 3 seams in mad_protocol.py, grounding_hits in mad_quality.py (+column-absent retry fallback), grounding_watch.py + 11:13 cron, spec in docs/ | push clean; 660 ins, 6 files |
| Specimens | ALL 4 caught by gate against synthetic baskets; zero false-pos on roles/verdict vocab | test output green x2 (pre+post patch) |
| Basket fields | REAL basket = title/summary/entities (jsonb) — NO keywords column (Code corrected spec via GNI-R-076) | Code read of real query |
| Ternary safety | 11:13 slot cannot touch Groq keys — run-mad job-guarded off it; account ternary internal to run-mad | grep :31/:57/:58/:82 |
| Hardening | `or []` on basket build line — redundant (guards exist 616-619) but kept as belt-and-suspenders | sed read + PATCHED |
| ALTER | grounding_hits jsonb added in Supabase | "Success. No rows returned" |
| LENS-GREP | CLOSED: Lens SATURATED with dying strings — ~15 live files (all S2/S3 stages, manager, MA, compendium, entity, rubrics, orchestrator probes x4, fallback map). WORST: lens_quota_guard.py keys TPD tables + role registry (S1-L1, S2-A/D/E/GAP, MA, S3-A) on dying model strings — migration touches ledger keys, not just call strings. NOT-dying: Cerebras/SambaNova entries (different providers). Non-prod: tests/, patch_*.py | grep output banked |
| Behavior note | workflow_dispatch on gni_mad.yml now runs BOTH run-mad AND grounding-watch (Code's guard design) — known, accepted | yml :31/:82 |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| G-VERIFY | TOP TOMORROW: 3-point glance — (1) 02:43 MAD log shows gate ran + grounding_shadow in quality row, (2) 10:13 verify-outcomes both steps green (=V-CRON), (3) 11:13 first grounding_watch digest lands in Telegram | Actions + Telegram, ~5 min total | - | V(shipped) |
| OC-A/B | Mark-validation + miss-regret measurement design. TIME-SENSITIVE (baseline before Aug 16). Fresh session, with first shadow data as reality check | roadmap Part 2 | James | B |
| I-WATCH | Integrity watch Tier A (8 checks) — A1 grounding-rate now HAS data source; extend grounding_watch.py rather than new script (honest lean) | after G-VERIFY | James | B |
| U-AUG9 | Marathon prep unchanged (secrets enum FIRST, funnel:1010, adaptive.yml:48, Tier-3 sweep, governor revalidate) | keyfile | James | V(prep) |
| L-CLIFF | NEW: Lens migration scoping — quota_guard model-keyed redesign question (swap strings in place vs key-agnostic refactor). Own mini-marathon or Aug-9 afternoon. SWOT needed | read lens_quota_guard.py full | James | B |
| SOLV-5 | 5th solver datapoint on next MAD log | next MAD | - | - |
| U-W | Weekly Groq lineup glance | models page | James | - |
| A-VLOG/W9/UNK2/O6/RL-SEED | unchanged from S60 | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Gate behavior on REAL replies (false-pos rate on live consultant text) | untested | G-VERIFY Jul-9 + 7d shadow |
| GROQ secret VALUES (lean: all four dying) | 50% | Aug 9 keyfile FIRST |
| adaptive.yml:48 consumed? | 50% | marathon |
| Lens SECRET values (code strings now known; secrets not) | unknown | L-CLIFF scoping |
| 429-churn <-> solver corr | ~45% | SOLV-5 |

## 5. TRAPS (<=8 lines)
- R-S61-1 (below): never stack a conditional patch behind its own test — operator runs through.
- Gate is SHADOW — resist reading a hit as actionable until false-pos rate known (7d window).
- Whitelist is thin (title/summary/location + 3 Swan headers) — expect legit-entity false
  positives on real text; that is WHY shadow-first. Tune whitelist from data, not intuition.
- LF/CRLF warnings on this repo = autocrlf noise, NOT the PS >> poison class. Ignore.
- workflow_dispatch fires grounding-watch too — a manual MAD test also sends a digest.
- Do NOT reopen: G-GATE build, LENS-GREP, I2-w/V-W13/V-MC/O-SEC (S60 closures stand).
- Standing: R-S60-1 hard-refresh; R-S60-2 quality!=grounding; R-S59-1 census-before-sweep.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `6f43aa5`
TOP3 = G-VERIFY 3-point glance (02:43 gate / 10:13 verifier / 11:13 digest), OC-A/OC-B design, L-CLIFF Lens migration scoping (quota_guard is model-keyed)
DEADLINE = Aug 9 marathon / Groq cliff Aug 16 (GNI full lineup + Lens ~15 files)
TRAP = gate is shadow — no acting on hits until false-pos rate known; whitelist tuning from DATA not intuition
FIRST MOVE = ls-remote verify HEAD; then G-VERIFY results from James (he glances, you interpret)

## 7. POINTERS (<=5 lines)
Gate: ai_engine/analysis/mad_grounding_gate.py (specimen tests in __main__).
Seams live in mad_protocol.py: import @44, setup @~644, seams @~731/~798/~886, result key @~1001.
Watch: ai_engine/analysis/grounding_watch.py | cron: .github/workflows/gni_mad.yml (:13 11 slot, job-guarded).
Quality fallback: mad_quality.py save_mad_quality (column-absent retry).
Lens grep output: banked in S61 chat; quota_guard.py:63-88 is the model-keyed core.

---
RULES APPENDS for GNI_RULES.md:
R-S61-1: Never stack a conditional patch command behind its own diagnostic in one instruction
  block — the operator will run straight through. "If X, then patch" must STOP at the
  diagnostic and wait for output. (S61: an `or []` patch ran against an already-guarded
  file; no-op by luck, not by design.)

DIARY S61 (<=10 lines):
Short session, one mission: the gate the specimens demanded. Opus built it clean in 17
minutes — and made the spec better twice (no keywords column; the ALTER-timing fallback).
The seam pointers survived from S60 within one line. My own miss tonight: I stacked a
conditional patch and James ran through it — R-S61-1 is me writing myself a rule again,
second session running. The rule-writer keeps needing the rules; that's why they're written.
Tomorrow three crons report in and the shadow starts talking. LENS answered too: saturated,
quota_guard model-keyed to dying strings — the cliff is a two-project event now. 👊
