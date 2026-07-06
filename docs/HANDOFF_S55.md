# HANDOFF S55 -> S56
DATE: 2026-07-06 | HEAD: `ee93fc5` (verify ls-remote) | MODEL: Fable 5 (took over from Opus 4.8 mid-S55)
Read ONCE. Standing rules: GNI_RULES.md by ID. Contract: docs/CONTRACT.md.
Do not re-read old audits/handoffs unless a queue item points there.

## 1. STATE (<=10 lines)
L1 Pipeline: healthy; SUCCESS both Jul-5 runs; measured ~16.9K Groq tokens/run.
L2 MAD: debates complete + basket-grounded (fact-checked clean), BUT Arbitrator starves on 429 during storm; evening hit 96,216/100K (past 95K red line); `mad_arb_failed` quarantine holding, no data pollution.
L3 GPVS: prediction-level verifier DEAD (358 pending / 0 verified) - BACKFILLABLE (historical SPY data, nothing lost). Report-level works.
L4 Quota: CLOSED - all 3 consumers of /api/quota account-aware (third fixed this session).
L5 Public: fossil sweep COMPLETE - schedules true, roadmap date-free, raw-429 leak dead, honest GPVS status live.
Live watch: Iran-US storm CRITICAL 10/10 ongoing (real event: Khamenei killed Feb 28); MAD accounts 93-96% daily; Stimson 403 dead + its alert-send failing; tech pillar starved 2/4.

## 2. DELTA (<=15 lines)
| Commit | What | Proof |
|--------|------|-------|
| `463d782` | F2: dev-hub endpoint count 27->21 | grep + 40/40 + push |
| `a502487` | F1: validation-log honest backlog + backfill truth | greps 0/0 + 40/40 |
| `dabbc46` | F3: date-free roadmap badges (reports/model-learning/pattern-library) | grep silent + 40/40 |
| `2f64bb0` | U1: honest Arbitrator-failure message; raw-429 leak dead (mad_protocol 877+914) | greps 0 + 2 hits + py_compile |
| `1819a36` | G1: /about/devops account-aware quota tile (4th false-185% sibling killed) | greps 2/1/0 + 40/40 |
| `579de19` | G2: true cron times, 10 sites, 6 files (02:13/10:13, 02:43/10:43; casual = "twice daily") | remote fossil-grep silent |
| `ee93fc5` | G3: patterns-page honest GPVS + date-free prose | remote greps 1/0 |
Rules appended: R-S55-1..5. Key discoveries: MAD runs the DEAD llama (live 429 string = proof); `fix_mad_model.py` does NOT exist (S54-brief fossil); Groq Aug-16 deprecation confirmed real (targets gpt-oss-120b/qwen3.6-27b/gpt-oss-20b); gpt-oss reasoning tokens threaten P5 quota math; PIPELINE_COSTS gni_pipeline=6175 vs ~16.9K measured; Mission Control reds = real CRITICAL (quota 96%) - question CLOSED.

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| U1 | Model decision by ~Aug 2 (James watching Groq lineup weekly for new options) | check Groq models page | James | L |
| U2 | Migration build before Aug 9 (cliff Aug 16): ~13 sites incl no-env hardcodes `intelligence_funnel.py:1010` + `gni_adaptive.yml:48` + methodology copy x2 + 2 secrets; consolidate to one GROQ_MODEL | re-BEV site list | James | L60 |
| U3 | Probe harness (10-field Arbitrator JSON + token profile; model-agnostic; buildable NOW, baseline on llama) | draft script | James | B |
| I1 | Integrated MAD session AFTER model decision: migrate + solver recal WITH Arbitrator reserve + hold <95K + C scorer fix (bear_used_numbers + consultant boilerplate, mad_quality.py) + deterministic grounding gate | after U1 | James | B |
| I2 | ARC B: revive GPVS prediction verifier; backfills once running | BEV outcome_verifier.py + its cron + predictions-list route | James | L |
| I3 | Source health: Stimson 403 + failing alert-send + tech pillar 2/4 + reserves not activating | BEV rss_collector reserve logic | James | V(symptoms) |
| I4 | Rolling 7-day integrity check on not_mad (prereqs done, window filled ~Jul 1) | design | James | B |
| O1 | docs/ + exports/ version-control call (lean: track docs/ - handoffs are small now) | decide | James | - |
| O2 | G4: PIPELINE_COSTS['gni_pipeline'] 6175 vs ~16.9K measured; (a) bump 17000 (S48 precedent) or (b) leave (sacred bypasses gate) | James picks a/b | James | V |
| O3 | G5: homepage:1008 hardcodes "81 patterns"; live count blocked by BOM (U+FEFF) in intelligence_funnel.py | count then align | - | L |
| O4 | Optional SQL: clean historical raw-429 mad_reasoning rows (UPDATE ... WHERE mad_reasoning LIKE '[Agent error%') | James in Supabase | James | B |
| O5 | Account-attribution re-check (read-only; tagged rows accumulated since S50) | run V2-flags query | - | B |
| O6 | Arc C temporal pattern discovery (LAST, by design) | - | - | B |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| GROQ_MODEL secret value (whole-pipeline vs MAD-only exposure) | 50% | James reads one pipeline run log's model string |
| gpt-oss-120b JSON + token behavior on real MAD structure | unknown | U3 probe |
| "gpt-oss ran on MAD at S32, 100+ runs" (contradicts live code) | 40% | git history if ever needed; treat as false |
| Arbitrator terminal-fail = TPD exhaustion (vs TPM) | 80% | read x-ratelimit headers on one failed run |
| Solver overshoot cause (storm context size vs curve drift) | 60% | measure inside I1 |

## 5. TRAPS (<=8 lines)
- Do NOT reopen: L4 quota (3 consumers), L5 sweep (F1-F3, G1-G3, U1), Mission Control cause (real CRITICAL, closed).
- `not_mad` account is RESERVED (pipeline + I4 + Arc C). NEVER route MAD/Arbitrator to it - James's explicit ruling.
- methodology's llama copy x2 is DELIBERATE - accurate today; sweeps at migration only (part of U2).
- curl/web-fetch is a dead-end live-verify; browser only (R-S54-4). Key is never in shell.
- Do NOT recalibrate solver against llama before migration - one calibration, inside I1 (R-S55-4).
- Verify the PATCHED print before trusting verify-greps - James's pastes can split blocks (R-S55-3).

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `ee93fc5`
TOP3 = U1 model decision (~Aug 2), I1 integrated MAD session, I2 GPVS revive
DEADLINE = decide ~Aug 2 / migrate by Aug 9 / Groq cliff Aug 16
TRAP = not_mad is reserved - never route MAD to it
FIRST MOVE = verify HEAD via ls-remote, then James picks: U3 probe build, I2, or I3

## 7. POINTERS (<=5 lines)
Migration footprint + Arbitrator diagnosis: S55 chat; `mad_protocol.py:49-51`, `intelligence_funnel.py:1010`, `gni_adaptive.yml:48`.
Model criteria + revision scaffold: GNI_Model_Selection_Note.md (save to docs/).
Transfer protocol spec: docs/GNI_Session_Transfer_Protocol.md. Old-format archive: S54 audit/brief set.
