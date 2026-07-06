# HANDOFF S56 -> S57
DATE: 2026-07-06 | HEAD: `4d43f10` (verify ls-remote) | MODEL: Fable 5 (full session)
Read ONCE. Standing rules: GNI_RULES.md by ID. Contract: docs/CONTRACT.md.
Do not re-read old audits/handoffs unless a queue item points there.

## 1. STATE (<=10 lines)
L1 Pipeline: healthy; Jul-6 run SUCCESS, 229 collected -> 22, real cost 17312 tokens/6 calls.
L2 MAD: unchanged from S55 (debates complete, Arbitrator 429-starves in storms; quarantine holds).
L3 GPVS: prediction-level verifier ALIVE (`0ae1975`) -- 236 backlog rows judged market_proxy_v1
  (52 materialized / 112 not / 72 inconclusive); ~122 rows pending future verify_by. Report-level unchanged.
L4 Quota: PIPELINE_COSTS truth restored (`4d43f10`): gni_pipeline 17500; honest total 97500/100K TPD.
L5 Public: unchanged. Alert path: HTML-escape fix live (`5f868c1`), live-proof pending next cron.
Sources: Stimson AND Breaking Defense both hard-403 (bot-wall, all UAs fail) -- await reserve picks.
Reserves PROVEN working (Crisis Group->ReliefWeb, AP->RFE, NPR->RFE live in Jul-6 run).
O5 CLOSED: account attribution healthy since Jun 26; no quality skew (arb consist 1.00 both).
Live watch: Iran-US CRITICAL 10/10 ongoing; MAD accounts still tight (evening 96K peak S55).

## 2. DELTA (<=15 lines)
| Commit | What | Proof |
|--------|------|-------|
| `5f868c1` | I3: HTML-escape failure reason in reserve alert + confess non-200 Telegram sends | PATCHED->COMPILE->hostile-reason proof->selftest 5/8 |
| `0ae1975` | I2: debate_prediction_verifier.py NEW -- market_proxy_v1, dry-run default, schema-adaptive | judge bands 6/6; dry-run eyeballed; apply wrote 236 |
| `4d43f10` | O2: PIPELINE_COSTS gni_pipeline 6175->17500 + reserved-total comment 97500 truth | verify-grep 2 hits, 0 stale 6175 |
Root causes: (1) alert-send died because the 403 failure reason contained literal `<unknown>` which
Telegram's HTML parser rejected 400 -- the failure reason poisoned its own alert; status!=200 returned
False with NO print (requests doesn't raise on 400). Reserves "not activating" was purely this shadow.
(2) debate_predictions was a WRITE-ONLY table -- MAD wrote, nothing ever read; verifier never existed.
(3) Tech pillar 2/4 is NOT a fetch bug: all 6 tech sources fetch fine; slow-cadence publishers
(Ars/Krebs/RoW/Bellingcat raw 10-20 -> 0 pass) die at the 18h news-tier capture gate. Policy, not code.
Built, uncommitted: mad_model_probe.py (U3 harness, py_compile OK, imports byte-exact ARB_FINAL,
captures finish_reason/reasoning tokens; NOT yet run -- llama baseline unrepeatable after Aug 16).
Discoveries: ARB schema is 12 keys not 10; ARB runs max_tokens=600 plain-JSON no response_format
(reasoning-model truncation = sharpest migration risk); RC comment fossils (6 vs 8 tech; actual 6).

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| U1 | Model decision by ~Aug 2 (weekly Groq lineup watch) | check Groq models page | James | L |
| U2 | Migration build before Aug 9 (cliff Aug 16); ~13 sites; consolidate to one GROQ_MODEL | re-BEV site list | James | L60 |
| U3 | RUN the probe (script BUILT, unfired): llama baseline x3 first, then candidates + max_tokens sweep | pick key/account, fire baseline | James | V(built) B(run) |
| I1 | Integrated MAD session AFTER U1: migrate + solver recal + Arbitrator reserve + <95K + C scorer fix + grounding gate | after U1 | James | B |
| I3-r | Reserve picks for Stimson + Breaking Defense (menu should arrive via fixed alert next cron; else check confess line in log) | read Telegram / run log | James | V |
| I3-b | HTML-escape siblings: code_fix_suggester.py:126, telegram_notifier.py:26/55 (same unescaped-input class) | BEV both call sites | James | L |
| I3-c | Tech-tier policy: 4/6 tech sources slow-cadence stuck in 18h news tier -> chronic Tech starvation | James steers tier map | James | V |
| I2-b | 429-fossil prediction rows judged as real (prediction text = '[Agent error: 429...]') | SQL sweep OR verifier skip-guard | James | V |
| I2-w | Wire verifier into pipeline once trusted (2-line patch near gni_pipeline.yml:81 step) + browser-check predictions page | after a few manual runs | James | B |
| I4 | Rolling 7-day integrity check on not_mad | design | James | B |
| O1 | docs/ + exports/ version-control call (S55_appends.md, dryrun_two_account_split.py, exports/ still untracked) | decide | James | - |
| O3 | homepage:1008 "81 patterns" hardcode; blocked by BOM U+FEFF in intelligence_funnel.py | kill BOM then count | - | L |
| O4 | Optional SQL: clean historical raw-429 mad_reasoning rows | James in Supabase | James | B |
| O6 | Arc C temporal pattern discovery (LAST, by design) | - | - | B |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| Alert fix live behavior (menu arrives vs confess-line shows new cause) | 70% menu | next pipeline cron log / Telegram |
| GROQ_MODEL secret value (whole-pipeline vs MAD-only exposure) | 50% | one run log's model string |
| gpt-oss-120b JSON + reasoning-token behavior on real ARB structure | unknown | U3 run |
| Arbitrator terminal-fail = TPD vs TPM | 80% TPD | x-ratelimit headers on one failed run |
| Whether debate_predictions long-horizon rows (~122) verify sanely at 180d SPY proxy | 60% | first long rows due; eyeball before trusting |

## 5. TRAPS (<=8 lines)
- Do NOT reopen: L4 quota consumers, L5 sweep, Mission Control, O5 attribution (CLOSED, healthy), O2.
- market_proxy_v1 verdicts are COARSE directional proxies; `accurate=True` on a Bull row is NOT a
  verified bullish call -- ALL agents' rows are threat-framed and judged on one risk-off SPY axis.
- `not_mad` account RESERVED (pipeline + I4 + Arc C). Never route MAD/Arbitrator to it.
- Do NOT run U3 probe on morning/evening near red line, and never on not_mad.
- Do NOT recalibrate solver against llama before migration -- one calibration, inside I1 (R-S55-4).
- Verify the PATCHED/DONE tail print before trusting paste bodies (R-S55-3 -- saved us once this session).
- .env exists at repo root (git-ignored, verified S56); verifier + probe load it via dotenv. Key never in shell.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `4d43f10`
TOP3 = U3 probe RUN (llama dies Aug 16), U1 model decision (~Aug 2), I1 integrated MAD session
DEADLINE = decide ~Aug 2 / migrate by Aug 9 / Groq cliff Aug 16
TRAP = not_mad reserved; market_proxy_v1 = coarse proxy, not semantic truth
FIRST MOVE = verify HEAD via ls-remote; check Telegram/log for reserve-alert live-proof; then James picks: U3 fire, I3-r/b, or I2-b

## 7. POINTERS (<=5 lines)
Alert root cause + fix: source_health_monitor.py lines 85-125; commit `5f868c1`.
Verifier design + schema: ai_engine/analysis/debate_prediction_verifier.py header; debate_predictions cols in S56 chat.
Probe harness: mad_model_probe.py at repo root (save from S56 outputs if missing); run flags in its header.
Tech-tier evidence: Jul-6 run log (Ars 20->0, Krebs 10->0, RoW 12->0, Bellingcat 10->0 at 18h gate).
Rule candidate R-S56-1: a failure reason is hostile input to any formatting channel -- escape at the boundary.
