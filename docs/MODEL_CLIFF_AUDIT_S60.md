# MODEL CLIFF AUDIT — S60 (2026-07-08)
Transferable finding. Feeds U-AUG9 marathon. Cliff: Groq deprecations effective Aug 16 2026.
Source: Groq deprecations page (Jun 17 2026 announcement) + repo grep (GNI working copy, HEAD 2c4be45).

## DEPRECATION WAVE (verified via web, Jul 8)
Dying Aug 16 (free/developer tier): llama-3.3-70b-versatile, llama-3.1-8b-instant,
qwen/qwen3-32b, meta-llama/llama-4-scout-17b-16e-instruct.
Groq-recommended heirs: openai/gpt-oss-120b (70B-class), openai/gpt-oss-20b (8B-class).
TRAP: qwen/qwen3.6-27b is recommended in migration notes but served as PREVIEW —
evaluation only, NOT production. Strike from production candidates; probe-only.

## TIER 1 — LIVE HARDCODED STRINGS (die Aug 16 regardless of secrets)
1. ai_engine/funnel/intelligence_funnel.py:1010 — hardcoded "llama-3.1-8b-instant"
   in L4 call. Runs EVERY pipeline run. Confirmed casualty-in-waiting. MUST FIX.
2. .github/workflows/gni_adaptive.yml:48 — hardcoded GROQ_MODEL: llama-3.3-70b-versatile.
   S46 banked adaptive as Cerebras-only / zero real Groq → possibly vestigial, but that is
   a ~50% claim. VERIFY at marathon: does anything in adaptive's path consume GROQ_MODEL?

## TIER 2 — SECRETS PICTURE (values still 50% unknown, leaning grim)
fix_mad_model.py (lines 14-15, 89-90) records intent:
  GROQ_MODEL          = meta-llama/llama-4-scout-17b-16e-instruct  ← ALSO deprecated
  GROQ_MODEL_FALLBACK = llama-3.3-70b-versatile                    ← deprecated
GNI-R-237: GROQ_MAD_MODEL confirmed secret = llama-3.3-70b-versatile ← deprecated
IF secrets still hold these values: EVERY Groq model string GNI uses (primary, MAD,
both fallbacks) dies the same day. Plan marathon as FULL-LINEUP replacement, not MAD swap.
Resolve actual secret values via run-log or keyfile step on Aug 9 (first marathon move).

## TIER 3 — DEFAULTS & DOCS (fire only if secrets absent; sweep anyway)
os.getenv defaults pointing at dying models (stale defaults = fossil fuel):
  code_fix_suggester.py:16, keyword_sensor.py:22, llm_health_probe.py:16-17,
  mad_protocol.py:51, nexus_analyzer.py:28-29, weekly_digest.py:17
Docs/comments to sync after migration: llm_health_probe.py:6, mad_protocol.py:9,
mad_preflight.py:155, mad_rate_governor.py:8 (429 probe grounded on old model —
governor timings need RE-VALIDATION on new model), mad_model_probe.py:3,227 (probe
harness default), fix_mad_model.py (historical, consider archiving).

## MARATHON SCOPE ADDITIONS (append to U-AUG9 row)
- [ ] Fix funnel:1010 hardcode (Tier 1.1)
- [ ] Verify adaptive.yml:48 consumption (Tier 1.2)
- [ ] Enumerate ACTUAL secret values first (Tier 2) — keyfile step
- [ ] Sweep all Tier 3 defaults to new model
- [ ] Re-validate mad_rate_governor timings on new model (429 profile will differ)
- [ ] Model-Change Re-Audit Ritual applies: ALL prior prompt/behavior verifications
      partially reset on swap (Four Treasures)
- [ ] PENDING: same grep in PROJECT LENS working copy (never run — the Jul-8 grep
      ran in GNI by accident). Lens Groq roles' model strings unknown.
      grep -rn "llama-3.3-70b\|llama-3.1-8b\|qwen3-32b\|llama-4-scout" --include="*.py" --include="*.yml" . | grep -v venv

## HALLUCINATION SPECIMEN LOG (separate track, feeds Layer-1 grounding gate build)
Specimen 1 (S55): consultant fabricated "Iranian rare earths / invisible broker" in R1,
agent laundered into R3 final position.
Specimen 2 (S60, Jul-7 evening debate): consultant introduced "Caucasus region" in R2
(zero article anchor), Bull R3 absorbed as fact, ARBITRATOR published it in the final
action recommendation (site + Telegram). Same channel, same layer, milder payload.
Benign tier same run: unsourced quantifications ("10% of EU GDP", "trillions of dollars").
Conclusion: personal-consultant layer is the confirmed infection vector (2/2 specimens).
Fix in flight S60: Layer 1 deterministic grounding gate (model-independent, survives
cliff). Layer 2 (consultant prompt reframe) deferred to marathon — re-tuned for new
model anyway. Citations in both specimens were REAL (scores matched funnel exactly);
the fabrications are entity/geography/quantity insertions, exactly what a span-check catches.
