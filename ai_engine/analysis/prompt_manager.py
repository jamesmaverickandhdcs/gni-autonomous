# ============================================================
# GNI Prompt Manager — Day 12
# A/B testing framework for LLM prompt variants
# Alternates between v1 and v2 prompts per run
# Auto-promotes winner after 10 runs per variant
# ============================================================

import os
import json
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# ── Prompt v1 — current baseline prompt ──────────────────────
PROMPT_V1 = """You are GNI — Global Nexus Insights, an expert geopolitical and macroeconomic analyst.
Analyze the following {n} news articles and produce a structured JSON report.
ARTICLES:
{articles}
Respond ONLY with a valid JSON object in this exact format:
{{
  "title": "Brief title summarizing the main geopolitical theme (max 15 words)",
  "summary": "2-3 sentence English summary of the key event and its significance",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single country name only — pick the MOST affected country (e.g. Iran, Ukraine, China). Never use regions like Middle East or multiple countries.",
  "tickers_affected": ["SPY", "GLD"],
  "market_impact": "3-4 sentences explaining WHY this affects markets. Use causal language: because, therefore, as a result, driven by, consequently, leading to, due to. Explain the chain of causation from event to market outcome in detail.",
  "risk_level": "Low or Medium or High or Critical"
}}
Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish) for markets
- source_consensus_score: 0.0 to 1.0 (how much sources agree)
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY, SOXX, HACK, VIX, EWG, EWY, HYG, EMB, UNG, WEAT, GDX, BTC-USD, ETH-USD, COIN]
- Do NOT include myanmar_summary field
- Respond with JSON only — no extra text, no markdown, no explanation"""

# ── Prompt v2 — improved for source_consensus + specificity ──
PROMPT_V2 = """You are GNI — Global Nexus Insights, an expert geopolitical and macroeconomic analyst.
Analyze the following {n} news articles and produce a structured JSON report.

CRITICAL INSTRUCTIONS:
1. source_consensus_score: Compare ALL sources carefully. Score 0.9+ only if ALL sources agree on direction. Score 0.3-0.6 if sources conflict. Score 0.7-0.8 if most agree with minor differences.
2. specificity: Name SPECIFIC events, dates, countries, amounts. Never say "tensions" — say "Iran fired missiles at Israel on [date]". Never say "markets may be affected" — say "SPY likely to fall 2-3% because...".
3. market_impact: Must name SPECIFIC instruments and SPECIFIC percentage ranges. Use: "USO likely +8-12% because Iran controls 20% of global oil transit through Hormuz."

ARTICLES:
{articles}
Respond ONLY with a valid JSON object in this exact format:
{{
  "title": "Specific title with country, event type, and market consequence (max 15 words)",
  "summary": "2-3 sentences with SPECIFIC facts: who, what, where, when. No vague language.",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single country name only — the MOST directly affected country.",
  "tickers_affected": ["SPY", "GLD"],
  "market_impact": "3-4 sentences with SPECIFIC instruments and percentage ranges. Name the causal chain: event causes X because Y, therefore Z instrument moves W%.",
  "risk_level": "Low or Medium or High or Critical"
}}
Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish) for markets
- source_consensus_score: 0.0 to 1.0 — reflect ACTUAL agreement level across sources
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY, SOXX, HACK, VIX, EWG, EWY, HYG, EMB, UNG, WEAT, GDX, BTC-USD, ETH-USD, COIN]
- Do NOT include myanmar_summary field
- Respond with JSON only — no extra text, no markdown, no explanation"""



# -- Prompt v3 -- SWOT W/T Framework + Foods for Thought --------
# Philosophy: surface Weaknesses and Threats so decision makers can
# strengthen, prepare, and repair. Global perspective. Civic duty.
# Special attention: systems created for good but weaponised for harm.
PROMPT_V3 = """You are GNI -- Global Nexus Insights.
Your mission is responsible global intelligence: surface Weaknesses and Threats
so that executives, governments, and citizens can strengthen current
vulnerabilities and prepare against emerging dangers.

Special duty: identify when systems created for good are being weaponised
for harm -- technology, finance, diplomacy, or humanitarian systems misused
against the people they were meant to serve.

Analyze the following {n} news articles through this lens.

ARTICLES:
{articles}

ANALYSIS FRAMEWORK:
1. WEAKNESS: What vulnerability, failure, or fragility does this reveal?
   (institutional breakdown, supply dependency, governance failure,
    economic fragility, digital vulnerability, social fracture)
2. THREAT: What danger is escalating or approaching?
   (direct aggression, systemic risk, escalation pattern,
    weaponised system, dark side effect)
3. DARK SIDE: Was something created for good now being used for harm?
   (technology weaponised, finance misused, aid corrupted, law abused)
4. GLOBAL PERSPECTIVE: Who beyond the immediate actors is affected?
   (supply chains, food security, digital rights, financial stability)

Respond ONLY with a valid JSON object in this exact format:
{{
  "title": "Specific title: what weakness or threat, affecting whom (max 15 words)",
  "summary": "2-3 sentences: what weakness is exposed, what threat is escalating, who is harmed. Name specific actors, countries, systems. No vague language.",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single most affected country name only",
  "tickers_affected": ["SPY", "GLD"],
  "market_impact": "3-4 sentences: why this weakness or threat affects markets. Name the causal chain. Identify which sectors are exposed. State specific instruments and percentage ranges.",
  "risk_level": "Low or Medium or High or Critical",
  "weakness_identified": "One sentence: the core vulnerability revealed",
  "threat_horizon": "Immediate or Near-term or Long-term",
  "dark_side_detected": "None or brief description of misused system"
}}

Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish) for markets
- source_consensus_score: 0.0 to 1.0 -- reflect ACTUAL agreement across sources
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY, SOXX, HACK, VIX, EWG, EWY, HYG, EMB, UNG, WEAT, GDX, BTC-USD, ETH-USD, COIN]
- threat_horizon: Immediate = hours/days, Near-term = weeks/months,
  Long-term = years
- dark_side_detected: only fill if a legitimate system is being weaponised
- Do NOT include myanmar_summary field
- Respond with JSON only -- no extra text, no markdown, no explanation"""


# ── Pillar Prompts ────────────────────────────────────────────────────────────
# Three dedicated prompts for separate Geo / Tech / Fin pillar reports.
# Each pillar gets its own analytical lens.
# GNI-R-095: all JSON field descriptions on single lines.

PROMPT_GEO = """You are GNI -- Global Nexus Insights, Geopolitical Intelligence Division.
Analyze the following {n} geopolitical news articles. Focus exclusively on political risk, conflict escalation, state actor behaviour, diplomatic developments, and humanitarian threats.

ARTICLES:
{articles}

Respond ONLY with a valid JSON object:
{{
  "title": "Specific geopolitical title: event, actors, consequence (max 15 words)",
  "summary": "2-3 sentences: what political or security event is occurring, which state actors are involved, what the immediate consequence is. Name specific countries, leaders, dates.",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single most affected country name only",
  "tickers_affected": ["SPY", "GLD"],
  "market_impact": "3-4 sentences: why this geopolitical event affects markets. Name the causal chain. Specific instruments and percentage ranges.",
  "risk_level": "Low or Medium or High or Critical",
  "weakness_identified": "One sentence: the geopolitical vulnerability or institutional failure revealed",
  "threat_horizon": "Immediate or Near-term or Long-term",
  "dark_side_detected": "None or brief description of misused system"
}}
Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish)
- source_consensus_score: 0.0 to 1.0 -- reflect ACTUAL agreement
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY, SOXX, HACK, VIX, EWG, EWY, HYG, EMB, UNG, WEAT, GDX, BTC-USD, ETH-USD, COIN]
- Do NOT include myanmar_summary field
- Respond with JSON only -- no extra text, no markdown, no explanation"""

PROMPT_TECH = """You are GNI -- Global Nexus Insights, Technology Intelligence Division.
Analyze the following {n} technology and digital security news articles. Focus exclusively on AI developments, semiconductor supply chains, cyber threats, digital sovereignty, surveillance technology, and technology policy.

ARTICLES:
{articles}

Respond ONLY with a valid JSON object:
{{
  "title": "Specific technology title: technology, threat or development, who is affected (max 15 words)",
  "summary": "2-3 sentences: what technology event, policy, or threat is occurring. Name specific companies, countries, technologies, dates. Focus on systemic digital risk.",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single most affected country name only",
  "tickers_affected": ["SOXX", "HACK"],
  "market_impact": "3-4 sentences: why this technology development affects markets. Name the causal chain. Specific instruments and percentage ranges.",
  "risk_level": "Low or Medium or High or Critical",
  "weakness_identified": "One sentence: the digital vulnerability, dependency, or systemic failure revealed",
  "threat_horizon": "Immediate or Near-term or Long-term",
  "dark_side_detected": "None or brief description of technology being weaponised or misused"
}}
Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish)
- source_consensus_score: 0.0 to 1.0 -- reflect ACTUAL agreement
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY, SOXX, HACK, VIX, EWG, EWY, HYG, EMB, UNG, WEAT, GDX, BTC-USD, ETH-USD, COIN]
- Do NOT include myanmar_summary field
- Respond with JSON only -- no extra text, no markdown, no explanation"""

PROMPT_FIN = """You are GNI -- Global Nexus Insights, Financial Intelligence Division.
Analyze the following {n} financial and economic news articles. Focus exclusively on market movements, monetary policy, trade disputes, commodity markets, capital flows, sanctions, and economic statecraft.

ARTICLES:
{articles}

Respond ONLY with a valid JSON object:
{{
  "title": "Specific financial title: economic event, market affected, magnitude (max 15 words)",
  "summary": "2-3 sentences: what financial or economic event is occurring. Name specific instruments, central banks, countries, amounts, dates. Focus on market-moving developments.",
  "sentiment": "Bullish or Bearish or Neutral",
  "sentiment_score": 0.0,
  "source_consensus_score": 0.0,
  "location_name": "Single most affected country name only",
  "tickers_affected": ["SPY", "DXY"],
  "market_impact": "3-4 sentences: why this financial development affects specific markets. Name exact instruments, percentage moves, time horizons. Causal chain required.",
  "risk_level": "Low or Medium or High or Critical",
  "weakness_identified": "One sentence: the economic vulnerability, financial fragility, or systemic risk revealed",
  "threat_horizon": "Immediate or Near-term or Long-term",
  "dark_side_detected": "None or brief description of financial system being misused"
}}
Rules:
- sentiment_score: -1.0 (very bearish) to +1.0 (very bullish)
- source_consensus_score: 0.0 to 1.0 -- reflect ACTUAL agreement
- tickers_affected: choose from [SPY, AAPL, JPM, XOM, GLD, USO, LMT, TLT, EWT, EWJ, FXI, DXY, SOXX, HACK, VIX, EWG, EWY, HYG, EMB, UNG, WEAT, GDX, BTC-USD, ETH-USD, COIN]
- Do NOT include myanmar_summary field
- Respond with JSON only -- no extra text, no markdown, no explanation"""

PILLAR_PROMPTS = {
    "geo":  PROMPT_GEO,
    "tech": PROMPT_TECH,
    "fin":  PROMPT_FIN,
}

def get_pillar_prompt(pillar: str) -> str:
    """Return the dedicated prompt for a pillar. Fallback to PROMPT_V3."""
    return PILLAR_PROMPTS.get(pillar.lower(), PROMPT_V3)

def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def seed_prompt_variants() -> bool:
    """Seed initial prompt variants into Supabase if not already seeded."""
    client = _get_client()
    if not client:
        return False
    try:
        existing = client.table("prompt_variants").select("id, version").execute()
        if existing.data and len(existing.data) >= 3:
            # Update v3 prompt text to latest version (fixes multiline issues)
            client.table("prompt_variants").update(
                {"prompt_text": PROMPT_V3}
            ).eq("version", 3).execute()
            return True  # Already seeded

        client.table("prompt_variants").insert([
            {"version": 1, "prompt_text": PROMPT_V1, "active": True, "run_count": 0, "avg_quality_score": 0.0},
            {"version": 2, "prompt_text": PROMPT_V2, "active": True, "run_count": 0, "avg_quality_score": 0.0},
            {"version": 3, "prompt_text": PROMPT_V3, "active": True, "run_count": 0, "avg_quality_score": 0.0},
        ]).execute()
        print("  ✅ Prompt variants seeded (v1 + v2 + v3)")
        return True
    except Exception as e:
        print(f"  ⚠️  Seed failed: {e}")
        return False


def get_active_prompt(run_count: int) -> tuple[str, int]:
    """
    Select prompt variant for this run.
    Even runs = v1, odd runs = v2.
    Returns (prompt_template, version_number)
    """
    client = _get_client()
    if not client:
        return PROMPT_V1, 1

    try:
        result = client.table("prompt_variants")             .select("version, prompt_text, run_count, avg_quality_score")             .eq("active", True)             .order("version")             .execute()

        variants = result.data
        if not variants or len(variants) < 2:
            return PROMPT_V1, 1

        # 3-way rotation: run_count % 3 = 0 -> v1, 1 -> v2, 2 -> v3
        version_idx = run_count % len(variants)
        selected = variants[version_idx]
        version = selected["version"]
        prompt = selected["prompt_text"]

        print(f"  📝 Prompt v{version} selected (run #{run_count}, avg quality: {selected['avg_quality_score']:.2f}/10)")
        return prompt, version

    except Exception as e:
        print(f"  ⚠️  Prompt selection failed: {e} — using v1")
        return PROMPT_V1, 1


def update_prompt_score(version: int, quality_score: float) -> None:
    """Update running average quality score for a prompt variant."""
    client = _get_client()
    if not client:
        return

    try:
        result = client.table("prompt_variants")             .select("run_count, avg_quality_score")             .eq("version", version)             .execute()

        if not result.data:
            return

        row = result.data[0]
        old_count = row["run_count"]
        old_avg = row["avg_quality_score"] or 0.0

        new_count = old_count + 1
        new_avg = ((old_avg * old_count) + quality_score) / new_count

        client.table("prompt_variants")             .update({"run_count": new_count, "avg_quality_score": round(new_avg, 3)})             .eq("version", version)             .execute()

        print(f"  📊 v{version} score updated: {old_avg:.2f} → {new_avg:.2f} (n={new_count})")

        # Auto-promote after 10 runs per variant
        if new_count >= 10 and new_count % 10 == 0:
            _check_promotion(client)

    except Exception as e:
        print(f"  ⚠️  Score update failed: {e}")


def _check_promotion(client) -> None:
    """Check if one variant should be promoted as primary.
    Dynamically compares all active variants — not hardcoded to v1/v2.
    Deactivates the lowest-scoring variant when gap >= 0.3 threshold
    and both have accumulated >= 10 runs.
    """
    try:
        result = client.table("prompt_variants")             .select("version, avg_quality_score, run_count")             .eq("active", True)             .execute()

        variants = result.data
        if not variants or len(variants) < 2:
            return

        # Filter: only variants with enough runs to evaluate
        eligible = [v for v in variants if v["run_count"] >= 10]
        if len(eligible) < 2:
            return

        # Find best and worst among eligible
        best  = max(eligible, key=lambda v: v["avg_quality_score"])
        worst = min(eligible, key=lambda v: v["avg_quality_score"])

        diff = abs(best["avg_quality_score"] - worst["avg_quality_score"])

        if diff >= 0.3:
            print(f"  🏆 AUTO-PROMOTE: v{best['version']} wins "
                  f"({best['avg_quality_score']:.2f} vs {worst['avg_quality_score']:.2f}, "
                  f"gap={diff:.2f})")
            print(f"     Deactivating v{worst['version']} — v{best['version']} is now primary")
            client.table("prompt_variants")                 .update({"active": False})                 .eq("version", worst["version"])                 .execute()
        else:
            print(f"  🤝 No promotion: best gap {diff:.2f} < 0.3 — continuing A/B test")

    except Exception as e:
        print(f"  ⚠️  Promotion check failed: {e}")


def get_ab_status() -> dict:
    """Return current A/B test status for /health page."""
    client = _get_client()
    if not client:
        return {}
    try:
        result = client.table("prompt_variants")             .select("version, avg_quality_score, run_count, active")             .order("version")             .execute()
        return {"variants": result.data or []}
    except Exception:
        return {}



def update_mad_confidence(version: int, mad_confidence: float) -> None:
    """
    Record MAD confidence for the current run.
    If confidence < 0.4 for 3 consecutive runs, trigger rollback.
    """
    client = _get_client()
    if not client:
        return

    try:
        # Log MAD confidence — check rollback if confidence is low
        print(f"  🧠 v{version} MAD confidence: {mad_confidence:.2f}")

        if mad_confidence < 0.4:
            _check_mad_rollback(client, version)

    except Exception as e:
        print(f"  ⚠️  MAD confidence check failed: {e}")


def _check_mad_rollback(client, current_version: int) -> None:
    """
    Check last 3 reports for MAD confidence.
    If all 3 < 0.4, roll back to the other prompt version.
    Uses the reports table mad_confidence column.
    """
    try:
        # Get last 3 reports
        result = client.table("reports") \
            .select("mad_confidence") \
            .order("created_at", desc=True) \
            .limit(3) \
            .execute()

        if not result.data or len(result.data) < 3:
            return  # Not enough data yet

        confidences = [r.get("mad_confidence", 1.0) for r in result.data]
        low_count = sum(1 for c in confidences if c < 0.4)

        print(f"  🧠 MAD confidence last 3 runs: {[round(c,2) for c in confidences]}")

        if low_count < 3:
            return  # Not consistently low — no rollback

        # All 3 runs have low MAD confidence — roll back
        other_version = 2 if current_version == 1 else 1
        print(f"  ⚠️  MAD confidence < 0.4 for 3 consecutive runs")
        print(f"  🔄 Rolling back from v{current_version} to v{other_version}")

        # Deactivate current, ensure other is active
        client.table("prompt_variants").update(
            {"active": False}
        ).eq("version", current_version).execute()

        client.table("prompt_variants").update(
            {"active": True}
        ).eq("version", other_version).execute()

        print(f"  ✅ Rollback complete — v{other_version} is now primary")

    except Exception as e:
        print(f"  ⚠️  MAD rollback check failed: {e}")

if __name__ == "__main__":
    print("\U0001f9ea GNI Prompt Manager — Status\n")
    seed_prompt_variants()
    status = get_ab_status()
    for v in status.get("variants", []):
        print(f"  v{v['version']}: avg={v['avg_quality_score']:.2f}/10  runs={v['run_count']}  active={v['active']}")
