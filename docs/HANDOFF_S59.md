# HANDOFF S59 -> S60
DATE: 2026-07-07 | HEAD: `a17724e` (verify ls-remote) | MODEL: Fable 5 (full session)
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S59-1). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
L1 Pipeline: healthy (Jul-6 evening 16950 tok, 311 collected, 22 selected; staging 9/9).
L2 MAD: Jul-6 EVENING arb TERMINAL-FAILED (TPD exhaustion, 92492 tok burned) -- honest-rendered on site,
  flagged mad_arb_failed, correctly excluded. Jul-7 morning clean. Solver error datapoints: 0.2% AND +8.8%.
L3 GPVS: verifier trusted-run #1 banked (Jul-7); run #2 gated to ANY LATER DAY (dry-run -> --apply -> browser).
L4 Quota: storm burn normal; date rollover healed.
L5 Public: 81->70 pattern-count sweep COMPLETE (11 mentions, 7 files -- handoff's "4 mentions" was 2.75x under);
  BOM stripped from funnel/intelligence_funnel.py; predictions empty-state now names arb-failure cause.
Ops: Mission Control CRITICAL findings now exit 0 (green); red reserved for real crashes. Live from tonight.
Live watch: Iran-US + Ukraine CRITICAL 10/10 ongoing.

## 2. DELTA (<=15 lines)
| Commit | What | Proof |
|--------|------|-------|
| `3b538f9` | W12-b: mission_control_check.py CRITICAL findings exit 0 | cat + VERIFY OK; live-verify tonight |
| `b78d947` | O7: ARB RAW slice 200->400 BOTH sites (mad_protocol.py:876,913 -- NOT mad_runner) | grep count 2 |
| `f0f0540` | W13: predictions empty-state honest (mad_arb_failed ternary, both cards) | build 40/40; browser-verify PENDING |
| `c8b946c` | O3-a: BOM stripped funnel/intelligence_funnel.py (real path: ai_engine/funnel/) | xxd clean + PARSE OK |
| `28b1ee1`+`a17724e` | O3-b/c: 81->70 across 11 mentions/7 files (live count: 70 patterns; 42 sources TRUE, kept) | SWEEP CLEAN grep |
Closed no-commit: UNK-5 (Jul-6 evening debate honest text browser-confirmed); UNK (arb 429 = TPD,
behavioral 95%: five 60s+ waits failed, morning TPM 429s recovered); W12 (NOT crash-loop -- selfcheck
worked, exit-1-on-findings design flaw; ~40% red history Jul 5-7 all storm-tracking).
W12-b patch note: first (buggy) script applied the exit fix; guard-abort on second was correct behavior.

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| U-AUG9 | MARATHON unchanged (S57 row verbatim): keyfile -> U3 x3 -> U1 -> probes -> U2 -> I1 -> copy sweep. I1 now holds TWO solver datapoints (0.2% N=37 D=300; +8.8% N=32 D=342 w/ heavy 429 churn) -- measure 3 more before recal. Cliff Aug 16. | notepad ../groq_probe_key.txt | James | V(prep) |
| U-W | Weekly July Groq lineup glance | Groq models page | James | - |
| I2-w | Verifier trusted-run #2 (dry-run -> --apply -> browser triple-agree) then cron wire (gni_pipeline.yml:81 area, 2-line) | run dry-run | James | B->V |
| V-W13 | Browser-verify W13: Jul-6 evening debate Predictions tab shows rate-limit line | one click post-deploy | - | 90% |
| V-MC | Confirm tonight+ Mission Control runs green during CRITICAL; glance whether ENDPOINT sends rich CRITICAL detail msg (never confirmed -- failed runs 12:19-5:44 AM predate screenshot window). If absent: 1-line endpoint add. | Telegram + Actions glance | - | 70% detail exists |
| W11 | verified_at overload -- status column WHEN validation-log hydrates | design with A-VLOG | James | V(diagnosed) |
| A-VLOG | Hydrate validation-log stat cards from filtered API; bundle W11 + pattern-count single-source-of-truth (expose 70 via /api/status or build const -- it forked once, it will fork again) | after I2-w | James | B |
| W9 | Double-down alert tripwire (unchanged) | next multi-fail day | - | 50% |
| UNK2 | 180d long-horizon rows eyeball when first mature | when due | - | 60% |
| I4 | Rolling 7-day integrity check (not_mad) | design | James | B |
| O6 | Arc C temporal discovery (LAST) | - | - | B |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| GROQ_MODEL/GROQ_MAD_MODEL/FALLBACK secret VALUES | 50% | run-log or Aug 9 |
| Endpoint sends CRITICAL detail Telegram (vs WARNING-only) | 70% yes | next natural CRITICAL (V-MC) |
| Solver error profile: 0.2% vs +8.8% -- 429-churn correlation? | 40% | next 3 MAD est-vs-real |
| Next terminal 429 limit-type string | - | self-documents via O7's 400-char slice |

## 5. TRAPS (<=8 lines)
- Do NOT reopen: everything in S58 traps PLUS W12/W13/O3/O7/UNK/UNK-5 (closed/shipped this session).
- verified_at-in-verifier stays (rescan-guard); API filter is the shield; W11 owns real fix.
- R-S58-1 rb/wb only; R-S59-1 census-before-sweep, no commit chained after a sweep-grep.
- Handoff numeric claims are LEADS: "4 mentions" was really 11; funnel path was stale (ai_engine/funnel/).
- exit(1) in mission_control_check.py except-branch is the REAL-CRASH alarm -- never remove it.
- 42-source claims are TRUE (live-counted) -- do not "fix" them.
- Probe waits for Aug 9; NEVER morning/evening; PowerShell >> = UTF-16 poison.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `a17724e`
TOP3 = Aug 9 marathon prep (keyfile!), I2-w trusted-run #2 then cron wire, V-W13+V-MC cheap browser/Telegram verifies
DEADLINE = Aug 9 marathon / Groq cliff Aug 16
TRAP = census-before-sweep (R-S59-1); don't touch verified_at in verifier; except-branch exit(1) is the real alarm
FIRST MOVE = ls-remote verify HEAD; V-W13 one click; V-MC Telegram glance; then verifier dry-run for run #2

## 7. POINTERS (<=5 lines)
Mission Control exit logic: scripts/mission_control_check.py (CRITICAL=0, except=1); yml is thin curl wrapper.
ARB RAW: ai_engine/analysis/mad_protocol.py:876,913 (now [:400]); GH masking shrinks display, not slice.
Pattern count truth: len(INJECTION_PATTERNS) in ai_engine/funnel/prompt_injection_detector.py:28 (=70).
W13 ternary: src/app/debate/page.tsx ~460/468. Source count truth: collectors/rss_collector.py:14 (=42).
S59 chat: TPD behavioral proof, W12 mechanism, sweep census method.