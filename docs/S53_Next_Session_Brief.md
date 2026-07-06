# GNI S53 -- Next Session Brief
**Closed:** 2026-06-30 - Chiang Mai UTC+7 - Team Geeks / Bro Alpha - Claude Opus 4.8
**Repo HEAD:** 8c08530

## COMMIT LEDGER (S53 -- 10 commits, all BEV-gated, James ran every commit)
- 41239e5  dedup fix (URL-novelty gate, injectable, current-run-excluded)
- 3fff939  dedup-fix test landed
- 6a82e4a  stats Half A (live injection_patterns -> about tile)
- 02eb854  L6 guardian on nexus response path
- f770b81  7-layer UI-sync (honest 7, dropped NER overclaim)
- 82d5eaa  homepage triple-fossil fix (69->81, 29->42, 4-stage->multi-stage)
- 0b03a70  remove about/.bak (James-authored)
- 58bff85  remove autonomy/.bak
- eeb8237  stats Half B (real per-run Groq token meter)
- 8c08530  perf: disable pillar-CI (~6 Groq calls/run saved)   [HEAD]

## CLOSED ARCS (from S52 bank)
- Dedup false-skip: FIXED (URL-novelty replaces asymmetric keyword-Jaccard)
- 7-layer security hardening: COMPLETE (L1 NFKC S52 + L6 guardian + L7 UI-sync)
- Stats (pipeline emits real numbers): COMPLETE (Half A injection tile + Half B token meter)
- Leak hunt: CLEAN (dedup bug was one-off; deception_detector:87 structurally immune)

## *** TOP PRIORITY NEXT SESSION -- HARD DEADLINE ***
### GROQ MODEL DEPRECATION -- internal deadline AUG 9 2026 (cliff Aug 16, +1wk buffer)
**BOTH models GNI uses die Aug 16** (confirmed Groq deprecation docs, announced June 17):
- llama-3.3-70b-versatile (PRIMARY default -- 8 sites)
- llama-3.1-8b-instant (FALLBACK -- nexus_analyzer:29, llm_health_probe:17, intelligence_funnel:1010)
- Retry chain [primary, fallback] = [DEAD, DEAD] after Aug 16 -- failover net fully rotted.
**Groq-named replacements:** gpt-oss-120b or qwen3.6-27b (for 70b); gpt-oss-20b (for 8b-instant).
**Exposed sites (8 primary + 3 fallback + 1 workflow + 2 secrets):**
  nexus_analyzer.py:28, mad_protocol.py:51, keyword_sensor.py, llm_health_probe.py,
  code_fix_suggester.py, weekly_digest.py, src/app/api/stock-context/route.ts,
  .github/workflows/gni_adaptive.yml:48 (HARDCODED, ignores secret).
**OPEN UNKNOWN (James must resolve FIRST):** actual value of GROQ_MAD_MODEL secret.
  - fix_mad_model.py (repo root) already STAGES gpt-oss-120b for MAD.
  - IF secret = gpt-oss-120b -> MAD SAFE, migration = non-MAD default cleanup.
  - IF secret = dead model/unset -> MAD EXPOSED, needs model-change re-audit (sacred path).
  - Check: GitHub Settings > Secrets > GROQ_MAD_MODEL, OR a recent MAD run's actual model in logs.
**Migration shape (future gated arc):** consolidate to ONE shared GROQ_MODEL default const =
  gpt-oss-120b; patch 8+3 sites + adaptive workflow hardcode; verify both secrets; if MAD was
  exposed, model-change re-audit + test debates (gpt-oss may differ from llama -- not drop-in,
  per Cerebras migration lesson). SMALL-but-multi-file. ~6 weeks runway to Aug 9 deadline.

## BANKED FINDINGS (decision-ready, fresh-session)
### 1. MISSION CONTROL red cluster -- needs ONE runtime data point
S52 "benign-warning-reddens" hypothesis REFUTED (selfcheck provably passes on WARNING).
Real cause is (b) real CRITICAL [likely groq_quota >=90%] OR (c) Vercel timeout [route has
no maxDuration, ~5 sequential awaits -> 504 -> json.load throws -> exit 1]. Undeterminable
from code. ACTION: open any red Mission Control run -> "Run GNI Mission Control" step ->
read last line. "Status: CRITICAL" = (b), names check. "JSONDecodeError"/"check failed" = (c).
NOTE: tonight's pillar-CI savings may reduce reds if quota was the cause.

### 2. HALLUCINATION grounding gate (research-grounded) -- MAD-path arc
06-28 debate: Ostrich asserted false "Iranian-sourced rare earths" (fact: China ~90%, Iran ~0).
ORIGIN: the personal CONSULTANT layer fabricated it in R1 ("invisible broker could be...Iranian
rare earths"); agent laundered it into R3 as fact. ROOT CAUSE: MAD has NO grounding gate anywhere
-- closed LLM loop, consultant prompt rewards confident specificity with no truth requirement.
Research (NIST AI RMF GenAI Profile names "fabrication" a top risk; EU AI Act high-risk accuracy
+ human-oversight, full application Aug 2 2026) confirms PROMPT-ONLY FIXES INSUFFICIENT -- field
mandates LAYERED architectural mitigation. FIX DIRECTION: Layer 1 = deterministic basket-grounding
span-check (named entity must appear in a source article, else flag hypothetical -- "Iranian rare
earths" fails); Layer 2 = consultant prompt reframed for calibrated-uncertainty (hypothesis-flag
not fact-assert); Layer 3 = formalize human-oversight (validates James's catch). REJECT fact-check
LLM (quota cost + also hallucinates). North star: agents may HYPOTHESIZE connections but must NOT
ASSERT invented entities as established fact. Pre-work: read current consultant prompts + check
2-3 more debates for systemic-vs-one-off. CANDIDATE TOOL: Firecrawl Search (see #3).

### 3. FIRECRAWL -- tested, capability confirmed, use = grounding gate NOT AP/CNN ingestion
TEST RESULT (with free API key; keyless failed IP-gated): scrapes BOTH AP + CNN successfully --
clean FRESH markdown (AP June-29 headlines; CNN "a min ago", NOT the 2023 archive-ghosts that
removed it S43). Capability CONFIRMED. BUT: (a) result is front-page index not article bodies --
real ingestion = 1 credit/article, ~1200/mo at production scale -> BREAKS $0 principle; (b) access-
permitted != republish-permitted (AP is a licensing business); (c) GNI's own LENS project already
solved AP/CNN via Google News RSS ($0, ToS-clean, public-index). VERDICT: for AP/CNN ingestion,
Google News RSS is the better tool. Firecrawl's high-value GNI use = hallucination grounding gate
(Search = verify-a-claim, low-call, ToS-clean). Free tier: 1000 credits/mo. [KEY ROTATED after
accidental exposure -- new key in James's terminal only, never in repo.]

### 4. CONFIRMED-HEALTHY (verified live this session, no action)
- Account split (morning/evening): working across a real day, each pool starts at 0/85000.
- MAD production-healthy: 3 scheduled runs SUCCESS, 100% quality, neutral 0.57/0.58/0.57.
- S51 depth solver ACCURATE: est 87,186 vs billed 86,331/86,452 (~1%).
- MAD token cost stable ~86-95K (under 100K cap; DRIFT flag = above 85K band, not breaching).

## WATCH-ITEMS (next scheduled cron / next debate)
- Pillar-CI savings: next INTELLIGENCE PIPELINE cron "Real Groq usage this run:" should drop
  ~6 calls + a few thousand tokens vs prior CI-on runs (GHA only, not local).
- Token meter (eeb8237): same line confirms real per-run cost replacing the dead 6175/6 literal.
- L6 guardian: next debate should match clean baseline (acts only on bad responses).
- Stats Half A tile: flips to live-sourced after next pipeline writes injection_patterns column.

## NEW RULES/LESSONS EARNED S53
- Believe-bytes-over-banked-note: S52's Mission Control hypothesis was WRONG; the code refuted it.
  A banked finding is a hypothesis, not a fact -- re-verify before fixing.
- When an audit reports a file-class to delete, sweep ALL siblings before the first delete.
- Recount catches its own slip (test-dropped-from-commit, .bak wrong path, 4th analyze() caller,
  2nd legit "69", 4th analyze __main__ caller).
- Cross-lab-evidence (LR-085): "check real-world apps + legal research first" turned a weak
  prompt-hunch hallucination fix into a NIST-framed layered design. Check the world before designing.
- Deadline discipline: set internal deadline ONE WEEK ahead of a hard cliff (Aug 9 not Aug 16) --
  buffer = runway to fix a bad migration while the old model is still alive.
- Metric integrity: a measurement tool that's subtly wrong is worse than none (cerebras-exclusion
  guard on the token meter).

## SESSION STATUS
10 commits shipped clean. 4 S52-arcs closed. Public site honest top-to-bottom. Pipeline meters
real cost. Pillar quota waste eliminated. Major Aug-9 Groq deadline SCOPED (one secret-value
unknown remains). Firecrawl tested + correctly-placed. Mission Control re-diagnosed (needs 1 log
line). Hallucination fix research-grounded + decision-ready. NEXT SESSION OPENS WITH: (1) check
GROQ_MAD_MODEL secret, (2) Groq migration arc [TOP, Aug-9], (3) Mission Control log-line, (4)
hallucination grounding arc.

--- end of brief ---
