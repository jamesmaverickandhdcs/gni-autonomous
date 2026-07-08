# G-GATE BUILD SPEC — for Claude Code (S61)
Repo: C:/HDCS_Project/03/GNI_Autonomous | HEAD at spec time: ca33985
Design settled S60 (see docs/ROLLING_WATCH_RL_ROADMAP_S60.md + docs/MODEL_CLIFF_AUDIT_S60.md,
specimen log). Rules in force: R-S60-2 (structure != grounding), R-S60-3 (never pipe
ungrounded layer into grounded layers unchecked), GNI-R-076 (read full files before patching).

## MISSION
Deterministic Layer-1 grounding gate catching entity/geography/quantity fabrications
(the consultant->agent->arbitrator laundering channel, 4/4 confirmed specimens).
SHADOW MODE ONLY this build: detect + log + flag. NO blocking, NO text modification,
NO verdict changes. Zero Groq tokens. Model-independent (must survive Aug-16 cliff).

## DELIVERABLE 1 — ai_engine/analysis/mad_grounding_gate.py (~150-200 lines)
Pure stdlib (re, collections; no LLM calls, no new deps).

### Core function
    check_grounding(text: str, basket: list[dict], whitelist_extra: list[str]) -> dict
Returns: {
  "hits": [ {"span": str, "kind": "entity|quantity", "location": str} ],
  "hit_count": int,
  "checked_spans": int,
  "grounded": bool   # hit_count == 0
}

### Extraction — NOUN-PHRASE level, not just proper nouns
Specimen #4 ("dollar-depegging") proves lowercase compound concepts fabricate too.
Extract from the checked text:
  1. Capitalized multi-word spans (proper-noun sequences, e.g. "Caucasus region")
  2. Hyphenated/compound noun phrases (e.g. "dollar-depegging", "rare-earth broker")
  3. Quantity claims: number + unit/scale patterns ("10% of EU GDP", "trillions of dollars",
     "$4.2 billion") — flag kind="quantity"
Skip: single common capitalized words at sentence start, agent role names
(Bull/Bear/Swan/Ostrich/Arbitrator), verdict vocabulary (bullish/bearish/neutral,
confidence, escalation), standard finance tickers already in basket scope (SPY/GLD/USO).

### Grounding test
A span is GROUNDED if it (case-insensitive, after basic normalization:
lowercase, collapse whitespace, strip punctuation/hyphens for comparison) appears in:
  - any basket article's title, summary, or keywords fields
  - the report title / summary / location (whitelist_extra)
  - Swan FALLOUT headers (whitelist_extra — caller supplies)
Substring match is acceptable for v1 (e.g. "Caucasus" grounded if any basket text
contains "caucasus"). Quantities: match the NUMBER portion — if "10%" appears nowhere
in the basket, "10% of EU GDP" is a hit even if "EU GDP" appears.

### CRITICAL: read mad_protocol.py IN FULL first (GNI-R-076)
Verify the exact structure of the article basket dict fields before writing the
matcher (title/summary/keywords key names must come from the real code, not this spec).

## DELIVERABLE 2 — wire 3 seams in ai_engine/analysis/mad_protocol.py
Confirmed line anchors at HEAD ca33985 (re-verify with grep -n before patching):
  SEAM 1 — line ~691: r1_cons_ctx build. After each c1_* consultant reply returns
           (lines ~700-703), run check_grounding(reply, basket, whitelist) on each.
  SEAM 2 — line ~747: r2_cons_ctx, same treatment on c2_* replies (~761-764).
  SEAM 3 — line ~850: arb_final_raw = _call_arbitrator(...). Gate AFTER the call
           returns (the W-02 retry machinery lives inside _call_arbitrator at 138 —
           do NOT wire inside the wrapper). Arbitrator-level hits are the alarm class.
Shadow behavior at every seam: collect results into a run-level dict
  grounding_shadow = {"consultant_hits": [...], "arb_hits": [...], "total": int}
and pass through to logging. DO NOT alter any text, prompt, or control flow.

## DELIVERABLE 3 — mad_quality_log column
New column: grounding_hits (jsonb or text; match table's existing style — read the
existing ALTER/insert code first). Store the grounding_shadow dict per run.
Provide the ALTER TABLE statement for James to run in Supabase SQL editor
(same pattern as S46 mad_arb_failed backfill — but NO backfill needed here).
Insert path: wherever mad_quality_log rows are written (grep for the insert; likely
mad_quality.py) — add the new field.

## DELIVERABLE 4 — ai_engine/analysis/grounding_watch.py + cron
Daily digest script (7d window) reading mad_quality_log.grounding_hits:
  - counts: runs checked, consultant hits, arb hits, top fabricated spans
  - Telegram digest: INFO level normally; RED only if arb-level hit in window
    (alarm philosophy from W12-b — copy its Telegram send pattern, fail-closed)
  - Account: not_mad Groq account is NOT used (zero LLM calls) — "not_mad cron slot"
    means schedule placement only, no token spend anywhere.
Cron: new job or step in existing workflow, daily, offset from existing crons
(pipeline 02:13/10:13, MAD 02:43/10:43, graph 02:58/10:58 UTC — pick a clear slot,
e.g. 11:13 UTC). Read the existing workflow YAML in full before editing (census the
env/secrets blocks it needs — Supabase URL/key + Telegram token only).

## CONSTRAINTS (hard)
- $0: stdlib only in the gate; no new pip deps.
- Shadow only: zero behavior change to MAD output this build.
- Windows Git Bash environment; James commits/pushes himself — produce files +
  the ALTER statement + a verification checklist, do NOT run git commands.
- Pure-ASCII anchors in any str-replace patching (LR-101).
- Census-before-sweep (R-S59-1): grep every mad_quality_log insert site before
  assuming there is only one.
- npm build untouched (Python-only change) — but note if any dashboard surface
  reads mad_quality_log with SELECT * that could choke on a new column.

## ACCEPTANCE CHECKLIST (Claude Code self-verify before handing back)
[ ] check_grounding catches all 4 known specimens when fed synthetic reproductions:
    "Iranian rare earths", "Caucasus region", the crypto specimen span, "dollar-depegging"
    against a basket that lacks them — write these as inline test cases in a
    if __name__ == "__main__" block, runnable via: python mad_grounding_gate.py
[ ] Zero false-positive on verdict vocabulary and agent names (test case included)
[ ] mad_protocol.py diff touches ONLY the 3 seams + one import + logging pass-through
[ ] grounding_watch.py dry-runs against empty data without crashing
[ ] No new dependencies introduced (pip freeze diff empty)
