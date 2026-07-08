# HANDOFF S60 -> S61
DATE: 2026-07-08 | HEAD: `2c4be45` (verify ls-remote) | MODEL: Fable 5 (full session; 80% weekly cap at close, resets Mon 5PM +07)
Read ONCE. Standing rules: GNI_RULES.md by ID (current through R-S60-3). Contract: docs/CONTRACT.md (unchanged).

## 1. STATE (<=10 lines)
L1 Pipeline: healthy (Jul-8 morning: 363 collected, 22 selected, 16248 tok, staging 9/9, quality 8.65).
L2 MAD: Jul-8 morning SUCCESS 0.58 BUT laundering specimens #3 (cryptocurrency) + #4 (dollar-depegging,
  published as 180d Long Shoot prediction) — consultant->R3->Arbitrator channel firing ~DAILY under
  CRITICAL storms. Quality scorer gave that run 100% — structure != grounding.
L3 GPVS: verifier FULLY AUTONOMOUS — trusted-run #2 triple-agreed (8 rows), cron wired `2c4be45`,
  first auto-run Jul-9 10:13 UTC. Solver datapoints #3 (+4.0%) #4 (-4.5%) banked; sign flipped.
L4 Quota: evening acct hit 88386 (>85K band) Jul-7; morning 82497 Jul-8. Watch band.
L5 Public: V-W13 verified (arb-failure line live). O-SEC CLEAN: webhook fail-closed 403; RLS 37/37 true, SELECT-only.
Live watch: Hormuz/Iran CRITICAL 10/10 ongoing (US strikes after 3 ships hit).

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| `2c4be45` | I2-w CLOSED: verifier wired into verify-outcomes job (6 lines) | diff 6 green; YAML OK; push clean |
| I2-w runs | dry-run = apply = DB (8 preds, market_proxy_v1, Jun-24 batch) | SQL 8 rows 00:30:41Z |
| V-W13 | CLOSED: fossil was STALE CLIENT BUNDLE; code/API/DB all clean | hard-refresh -> honest line renders |
| V-MC | CLOSED: W12-b live green incl. finding-runs; 2 reds predate fix | Actions #1248+ green |
| O-SEC | CLOSED both halves (webhook secret-token first+fail-closed; RLS full) | route.ts:67-72; pg query |
| U-W | Groq wave WIDER: 8b-instant, qwen3-32b, llama-4-scout also die Aug 16; heir gpt-oss-120b; qwen3.6-27b = PREVIEW TRAP | web-verified |
| Cliff grep | Tier1: funnel:1010 hardcode 8b; adaptive.yml:48 hardcode 70b. Tier2: secrets lean = ALL FOUR strings dying | docs/MODEL_CLIFF_AUDIT_S60.md |
| Specimens | #2 Caucasus (Jul-7 eve, arb action), #3 crypto (Jul-8, blind spot+action), #4 dollar-depeg (Jul-8, LONG SHOOT). Vector = consultants, 4/4. Root: consultants receive NO basket (S28 lean-ctx side-effect); S46 GROUNDING_RULE prompt guard leaks | debate pages + basket cross-check |
| Design | Layer-1 gate settled: shadow-first, 3 seams, noun-phrase (not just proper-noun, per #4) + grounding_watch 7d cron on not_mad. James extended -> full rolling watch | ROLLING_WATCH_RL_ROADMAP_S60.md |
| Roadmap | 13 integrity checks (8 Tier-A now), OC-A mark-validation + OC-B miss/regret, 8 learning systems ($0) | same doc |
| A-VLOG BEV | validation-log page has ZERO fetch — fully static; bigger build than queued | grep 1 hit (prose only) |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| G-GATE | TOP: mad_grounding_gate.py SHADOW build (Claude Code; ~150-200 ln + mad_quality_log col + 3 wires) + grounding_watch.py 7d cron. Spec: both S60 docs. Noun-phrase extraction; whitelist report title/summary/location + Swan FALLOUT headers | read both docs -> Claude Code | James | V(design) |
| I-WATCH | Integrity watch Tier A (8 checks, one daily script, Telegram digest; red only A1-arb/A8/2-sigma) — merges I4 | after G-GATE (shares cron) | James | B |
| OC-A/B | Mark-validation + miss-regret measurement. TIME-SENSITIVE: collect BEFORE Aug 16 for before/after baseline | design from roadmap Part 2 | James | B |
| U-AUG9 | MARATHON + cliff-audit additions (funnel:1010, adaptive.yml:48 verify, secrets enum FIRST, Tier-3 sweep, governor revalidate) | keyfile | James | V(prep) |
| LENS-GREP | Deprecation grep in LENS working copy (never ran — Jul-8 grep hit GNI by accident) | cmd in cliff doc | - | - |
| V-CRON | Glance Jul-9 10:13 UTC verify-outcomes: both GPVS steps green (expect Due:0) | Actions 1 click | - | 90% |
| U-W | Weekly Groq lineup glance | models page | James | - |
| SOLV-5 | 5th solver datapoint then recal decision (series: +0.2/+8.8/+4.0/-4.5; churn corr ~45%) | next MAD log | - | - |
| A-VLOG | Full build: page static, needs fetch layer + W11 status col + pattern-count SSOT | design | James | V(BEV'd) |
| W9/UNK2/O6 | unchanged from S59 | - | - | - |
| RL-SEED | James's conclusion-article corpus = L5 seed schema {fact_check[], invisible_links[], cw_read}, hypothesis-tier labels | bank w/ L5 | - | - |
| BUDGET | Fable 80% at S60 close; S61 on fresh week (Mon 5PM) or Sonnet-executes-docs for mechanical work | James | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| GROQ_MODEL/MAD/FALLBACK secret VALUES (lean: all four = dying models) | 50% | Aug 9 keyfile FIRST |
| adaptive.yml:48 actually consumed? (S46 banked Cerebras-only) | 50% | marathon verify |
| Endpoint sends rich CRITICAL Telegram detail | 85% | next natural CRITICAL |
| 429-churn <-> solver error correlation | ~45% (sign flip #4) | SOLV-5 |
| Telegram verdict 57% vs site 58% (rounding?) | micro | 1-line check someday |
| Lens Groq model strings | unknown | LENS-GREP |

## 5. TRAPS (<=8 lines)
- R-S60-1: browser-verify = HARD-REFRESH FIRST. V-W13 burned an hour on a cached bundle.
- R-S60-2: quality 100% != grounded. Scorer measures structure; specimens #3/#4 scored perfect.
- Do NOT reopen: I2-w, V-W13, V-MC, O-SEC, W12/W13 family (all closed with proof).
- qwen3.6-27b: recommended in Groq migration notes but PREVIEW — never production.
- Specimen fix is G-GATE, NOT another prompt patch — S46 GROUNDING_RULE already proven leaky.
- S60 docs live in chat outputs — COPY INTO docs/ + commit at S61 open before anything else.
- Standing: R-S59-1 census-before-sweep; verified_at stays; except-branch exit(1) sacred; PS >> poison.

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `2c4be45`
TOP3 = G-GATE shadow build (specimens firing daily), OC-A/OC-B before Aug 16, Aug-9 marathon prep (secrets enum first)
DEADLINE = Aug 9 marathon / Groq cliff Aug 16 (FULL lineup, not just MAD)
TRAP = hard-refresh before browser-verify (R-S60-1); quality-100% != grounded (R-S60-2); commit S60 docs into repo first
FIRST MOVE = ls-remote verify HEAD; copy MODEL_CLIFF_AUDIT_S60.md + ROLLING_WATCH_RL_ROADMAP_S60.md into docs/ + commit; V-CRON glance; then G-GATE

## 7. POINTERS (<=5 lines)
Gate seams: mad_protocol.py ~690/746 (consultant ctx build), 850 (arb final), _validate_mad_output:385.
Consultant blindness: r1_cons_ctx/r2_cons_ctx = title+escalation+compressed positions ONLY (no articles).
Cliff detail: docs/MODEL_CLIFF_AUDIT_S60.md | Watch+RL: docs/ROLLING_WATCH_RL_ROADMAP_S60.md.
Webhook auth: src/app/api/telegram-webhook/route.ts:67-72 (fail-closed).
Verifier cron: .github/workflows/gni_pipeline.yml:88 (verify-outcomes job, daily 10:13 UTC).

---
RULES APPENDS for GNI_RULES.md:
R-S60-1: Browser verification requires a hard-refresh (Ctrl+Shift+R) first — a stale client
  bundle perfectly mimics a code bug (V-W13: code, API, and DB were all clean; cache was the bug).
R-S60-2: Structural quality scores do not measure grounding. A MAD run scoring 100% published
  two fabricated entities. Grounding requires its own deterministic gate against the article basket.
R-S60-3: Never pipe an ungrounded layer's output into grounded layers unchecked. Consultants
  receive no article basket; labeling their text "PERSONAL CONSULTANT TO YOU" launders invention
  into evidence. 4/4 confirmed specimens entered through this channel.

DIARY S60 (<=10 lines):
The verifier went autonomous today — S56 built it, S58 restored it, S60 wired it. GNI now
labels its own predictions daily with no human touch; the roadmap doc explains why that
quietly changes everything. We caught the laundering channel firing two days running and
finally understood WHY: the consultants coach blind. And one for the record — I hallucinated
a typo in James's YAML, argued with myself in public, and had to invoke GNI-R-233 on myself
mid-sentence. The rule works on the rule-writer. Good session. Fist-bump earned. 👊
