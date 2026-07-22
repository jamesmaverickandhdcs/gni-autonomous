# HANDOFF S79 -> S80
DATE: 2026-07-22 | HEAD: `5e6e1fb` (verify ls-remote) | MODEL: Fable 5 (next: Opus 4.8 OR Fable 5 on promo)
Read ONCE. NEW: docs/MODEL_TRANSITION_BRIEF.md — new-model sessions read it AFTER CONTRACT, before this.
Standing rules: GNI_RULES.md by ID (current through R-S78-2 IN BOOK; R-S79-1/2 pending below). CONTRACT v2.

## 1. STATE (<=10 lines)
MODEL-404 ROOT-CAUSED 3 LAYERS DEEP + FIXED, CERT PENDING: (1) old primary dead in Groq's Jul 17
  shutdown (secret was ~3 months stale, hadn't been touched since April — S78's "failed Jul 18
  update" prediction confirmed and exceeded); (2) secret now openai/gpt-oss-120b via gh CLI with
  byte receipt; (3) probe was starving the reasoning model (max_tokens 50 -> empty content ->
  parse fail char 0) — patched to 1024, LOCAL CERT PASSED (primary ready print seen).
CI CERT = S80 FIRST MOVE: next Intelligence cron ~05:29 UTC. Runs #303/#304 predate the probe fix.
Sweeps landed: model-name defaults+adaptive.yml+.env (e526ff0), small max_tokens 120-300 -> 1024
  starvation pre-empt (5e6e1fb). Quota fitness PROVEN: gpt-oss-120b = 200K TPD (2x old 100K),
  caution TPM 12K->8K (existing sleeps should hold; watch 429s).
Fable5->Opus4.8 transition prepared: MODEL_TRANSITION_BRIEF.md committed (10f42aa), CONTRACT v2.

## 2. DELTA (<=15 lines)
| Item | What | Proof |
|------|------|-------|
| e7a2e2d | R-S78-1/2 appended (landing gate done) | grep 2 |
| 10f42aa | MODEL_TRANSITION_BRIEF.md + CONTRACT v2 log | 121 lines, tail sig |
| 613aabb | probe max_tokens 50->1024 (repro->patch->proof locally) | primary-ready print |
| e526ff0 | GROQ_MODEL defaults sweep 6 files -> gpt-oss-120b (MAD scope excluded) | 6 PATCHED + residual grep |
| 5e6e1fb | max_tokens 120/150/200/300 -> 1024 (keyword_sensor/code_fix/weekly_digest) | 5 PATCHED |
| Secret fixed | gh secret set GROQ_MODEL -> gpt-oss-120b; was "3 months ago" stale | gh secret list before/after |
| Mystery run closed | "manual" #301 = S78's own gh dispatch, not intruder | databaseId match 29855563370 |
| Phishing handled | fake repo-scanner email (trypatchhog.com) via Vercel-URL recon; repo access clean | collaborators=1, keys=0 |
| GT5 digest READ | arb-level fabrication real: 118 consultant / 27 arb hits, 7d 10/10 runs | grounding log 81049186383 |
| MAD corrected | MAD = GROQ_MAD_MODEL 3.3-70b (mad_protocol.py:9), dies Aug 16; mad_model_probe.py exists | bytes beat search memory |
| Lens cleared | Lens-1 HTTP 200 + quality 6.7-7.8 all 8 logs Jul 19-22 — NOT bleeding | lens manage-analyze logs |
| Corpse ID revised | old GNI primary likely llama-4-scout (qwen3-32b still 200s for Lens) | lens logs vs deprecation list |

## 3. QUEUE (<=25 lines)
| ID | Task | First move | Gate | Trust |
|----|------|-----------|------|-------|
| RULES-APPEND | R-S79-1/2 below (landing gate) | tail docs/GNI_RULES.md | James | - |
| MODEL-FIX-CERT | read first post-05:29UTC cron: PASS = "primary model ready (openai/gpt-oss-120b)", no 404, no parse-fail; then watch analysis calls for gpt-oss quirks (JSON shape, report quality) | ID=$(gh run list -w "GNI Intelligence Pipeline" -L1 --json databaseId -q '.[0].databaseId'); gh run view $ID --log \| grep -E "Probe\|ready\|fallback\|attempt" | - | V(local) |
| FALLBACK-SWAP (U3) | after ONE clean cert: GROQ_MODEL_FALLBACK -> openai/gpt-oss-20b (secret via gh + probe default line 17 + funnel:1070 hardcode REDESIGN: max_tokens 5 can never serve a reasoning model) | design first (funnel L4 call) | James | - |
| MAD-MIGRATE | MAD on 3.3-70b, dies Aug 16; instrument exists (mad_model_probe.py) — baseline then switch GROQ_MAD_MODEL; own arc, NOT a sweep | python mad_model_probe.py --model openai/gpt-oss-120b --trials 3 | James | V(bytes) |
| TRANS-COUNT-CERT | certifiable from any green log Deduplication line vs pipeline_runs.total_after_dedup | grep + SQL | - | B |
| GT5-T2-DECISION | DEFERRED by design: re-read grounding digest 1wk AFTER primary certs clean (fallback-era contamination) | digest read ~Jul 30+ | James | - |
| LENS-SESSION | opener: which model actually serves Lens-1 (workflow fires lens_s1_report.py — unread); then migrate 3.3-70b hardcodes (compendium/entity_extract/framing_rubrics + "AI 5 verdict" judge) before Aug 16; Cerebras paths unaffected; gh secret list 403 = token lacks fintelplan scope, use web | read code/lens_s1_report.py | James | V(logs) |
| PHISH-HOMEWORK | OAuth apps review + security log + report email in Gmail | browser (James solo) | James | - |
| ADAPTIVE-DRIFT | CLOSED by e526ff0 (adaptive.yml now on new model; still hardcoded not secret-fed — optional tidy) | - | - | V |
| CI-DEGRADE | "2 additional runs" -> runs=1 width=0.00 on fallback-era; recheck on certified primary | read CI code | - | I |
| Fallback-era quarantine | Jul 19-22 DB rows are 8b-written; exclude from quality baselines | SQL tag | James | - |
| RE-CERT / F3 / WORD-CONV / PHASE-NARR / WEIGHT-PRIOR / GATE-DESIGN / F20-CERT / FED-DOE-WATCH / FT-GAP-B-CERT / F22 / D-11 / DEAD-COLS / J-RULINGS / CRED-TOTAL-WATCH | unchanged from S78 handoff | - | see S78 | - |
| Reserve choices | France 24 / Crisis Group / Myanmar Now menus pending in Telegram (reply 1-7) | telegram | James | - |
| OC-A ~Jul 24 / GT5 re-read ~Jul 30 / CERT ~Aug 2 / keyfile Aug 9 / TRIPLE CLIFF Aug 16 (accounts + 3.3-70b + 8b fallback all die) | - | - | James | - |
| Parked 16 | unchanged | - | - | - |

## 4. UNKNOWNS (<=8 lines)
| Fact | Trust | Resolve by |
|------|-------|-----------|
| CI cert outcome (probe fix in CI) | local-proven only | MODEL-FIX-CERT |
| gpt-oss analysis-call behavior (JSON shape, quality, reasoning field) | untested in pipeline | first certified run review |
| Which model serves Lens-1 at runtime | config says qwen3-32b, logs say alive | LENS-SESSION read |
| Exact identity of old dead GNI primary | masked; scout likely | optional (not needed) |
| TPM 8K adequacy under 10/10 heat | inferred OK (sleeps) | watch 429s post-cert |
| GROQ_MAD_MODEL actual secret value | comment says 3.3-70b | MAD-MIGRATE step 1 |

## 5. TRAPS (<=8 lines)
- Cron schedule: Intelligence runs ~05:29 + ~12:02 UTC ONLY (sacred 2/day; 10/10 adds none).
  Don't wait for an 18:0x run that never comes; don't burn a dispatch to "check".
- gh run list -L1 returns the LAST run — check its timestamp before treating it as new.
- Browser-UI steps are NOT executable in this partnership (R-S79-1). gh CLI + byte receipts only.
- Deprecation-list match is a LEAD not a diagnosis — Lens-1 200'd with a "dead" model configured.
- Reasoning models: any small max_tokens is a starvation bomb; funnel:1070 (max_tokens 5) must be
  REDESIGNED not renamed when fallback swaps.
- Quota: 85% standing; ONE manual dispatch per diagnosis cycle, prefer free cron reads.
- MAD scope excluded from sweeps DELIBERATELY (own arc, own instrument, 90+ sessions of tuning).

## 6. LOAD CHECK - next AI echoes EXACTLY these 5 lines, nothing more
HEAD = `5e6e1fb` TREE CLEAN (.env local-modified, unstaged, correct) -- MODEL-404 fixed 3 layers deep, LOCAL cert passed, CI cert pending ~05:29 UTC cron
TOP3 = RULES-APPEND (R-S79-1/2), MODEL-FIX-CERT (grep probe: "primary model ready (openai/gpt-oss-120b)"), then FALLBACK-SWAP design (funnel:1070 redesign, not rename)
DEADLINE = OC-A ~Jul 24 / GT5 re-read ~Jul 30 / CERT ~Aug 2 / keyfile Aug 9 / TRIPLE CLIFF Aug 16 (accounts + 3.3-70b + 8b all die)
TRAP = crons 05:29+12:02 UTC only; -L1 needs timestamp check; deprecation-list = lead not diagnosis; small max_tokens = starvation bomb; browser steps not executable
FIRST MOVE = ls-remote + git status; if new-model session: read MODEL_TRANSITION_BRIEF.md after CONTRACT; then cert read
