# ============================================================
# GNI MAD Protocol v1 — Day 14
# Multi-Agent Debate: Bull -> Bear -> Historian -> Risk Manager -> Arbitrator
# Adapted from pilot — fixes: headline->title, model name,
# improved prompts with geopolitical specificity (L34),
# richer context including market_impact + escalation_level
# L23: Model name via GROQ_MODEL env var - never hardcoded
# ============================================================

import os
import json
import re
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = os.getenv('GROQ_MODEL', 'llama-3.3-70b-versatile')  # L33

VALID_VERDICTS = ["bullish", "bearish", "neutral"]


def _call_agent(system_prompt: str, user_prompt: str, max_tokens: int = 400) -> str:
    """Call a single MAD agent via Groq."""
    try:
        response = client.chat.completions.create(
            model=MODEL,
            messages=[
                {'role': 'system', 'content': system_prompt},
                {'role': 'user', 'content': user_prompt},
            ],
            max_tokens=max_tokens,
            temperature=0.7,
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f'[Agent error: {str(e)}]'


def _build_context(report: dict) -> str:
    """Build rich context string for MAD agents — fixes headline->title."""
    title = report.get('title', report.get('headline', 'No title'))
    summary = report.get('summary', '')[:600]
    sentiment = report.get('sentiment', 'Neutral')
    risk_level = report.get('risk_level', 'Medium')
    market_impact = report.get('market_impact', '')[:400]
    location = report.get('location_name', '')
    tickers = ', '.join(report.get('tickers_affected', []))
    escalation = report.get('escalation_level', '')
    llm_source = report.get('llm_source', 'unknown')

    return (
        f"Title: {title}\n"
        f"Summary: {summary}\n"
        f"Sentiment: {sentiment} | Risk: {risk_level} | Location: {location}\n"
        f"Escalation: {escalation}\n"
        f"Tickers Affected: {tickers}\n"
        f"Market Impact: {market_impact}\n"
        f"LLM Source: {llm_source}"
    )


def _validate_mad_output(result: dict) -> dict:
    """
    Validate MAD output — security hardening.
    Ensures verdict is valid, confidence in range, reasoning not empty.
    """
    errors = []

    verdict = result.get('mad_verdict', '')
    if verdict not in VALID_VERDICTS:
        errors.append(f"Invalid verdict: {verdict!r}")
        result['mad_verdict'] = 'neutral'

    confidence = result.get('mad_confidence', 0.5)
    try:
        confidence = float(confidence)
        if confidence < 0.0 or confidence > 1.0:
            errors.append(f"Confidence out of range: {confidence}")
            result['mad_confidence'] = max(0.0, min(1.0, confidence))
    except (TypeError, ValueError):
        errors.append(f"Invalid confidence: {confidence}")
        result['mad_confidence'] = 0.5

    reasoning = result.get('mad_reasoning', '')
    if len(reasoning.strip()) < 20:
        errors.append("Reasoning too short — MAD output may be degraded")

    # Check for injection patterns in agent outputs
    injection_signals = ['ignore previous', 'override', 'jailbreak', 'system:', 'act as']
    for field in ['mad_bull_case', 'mad_bear_case', 'mad_historian_case', 'mad_risk_case', 'mad_reasoning']:
        text = result.get(field, '').lower()
        for signal in injection_signals:
            if signal in text:
                errors.append(f"Injection signal in {field}: {signal!r}")
                result[field] = '[Output flagged — injection signal detected]'

    if errors:
        print(f"   ⚠️  MAD validation warnings: {errors}")

    return result


def run_mad_protocol(report: dict) -> dict:
    """
    Run five-agent MAD debate on a GNI intelligence report.
    Bull -> Bear -> Historian -> Risk Manager -> Arbitrator.
    Arbitrator weighs all 4 cases before delivering final verdict.
    """
    context = _build_context(report)
    escalation_level = report.get('escalation_level', '')
    risk_level = report.get('risk_level', 'Medium')
    weakness = report.get('weakness_identified', '')
    dark_side = report.get('dark_side_detected', '')

    # -- Bull Agent ----------------------------------------
    bull_system = (
        'You are a bullish macro analyst specialising in geopolitical risk. '
        'Argue the STRONGEST BULLISH case for global markets based on this intelligence report. '
        'Requirements: '
        '(1) Cite SPECIFIC events from the report by name. '
        '(2) Explain the causal chain: because X happens, therefore Y market outcome follows. '
        '(3) Name at least one specific ticker and a percentage range. '
        '(4) Explain why this is a buying opportunity despite apparent risks. '
        'Keep your argument to 3-4 sentences. No hedging. Make the strongest possible bull case.'
    )

    # -- Bear Agent ----------------------------------------
    bear_system = (
        'You are a bearish macro analyst specialising in geopolitical risk. '
        'Argue the STRONGEST BEARISH case for global markets based on this intelligence report. '
        'Requirements: '
        '(1) Cite SPECIFIC events from the report by name. '
        '(2) Explain the causal chain: because X happens, therefore Y market outcome follows. '
        '(3) Name at least one specific ticker and a percentage range (downside). '
        '(4) Explain the systemic risk and contagion pathway. '
        'Keep your argument to 3-4 sentences. No hedging. Make the strongest possible bear case.'
    )

    # -- Historian Agent -----------------------------------
    historian_system = (
        'You are a geopolitical historian specialising in market crises and conflict patterns. '
        'Your role: identify historical precedents for this situation and explain the outcome. '
        'Requirements: '
        '(1) Name the most relevant historical parallel (specific event, year, actors). '
        '(2) Explain how that precedent resolved and what the market outcome was. '
        '(3) Identify what is DIFFERENT this time that could change the outcome. '
        '(4) Give a probability-weighted historical base rate for escalation vs resolution. '
        'Keep your analysis to 3-4 sentences. Be specific about dates and outcomes.'
    )

    # -- Risk Manager Agent --------------------------------
    risk_manager_system = (
        'You are a senior risk manager at a global macro fund. '
        'Your role: identify the WORST CREDIBLE SCENARIO and tail risks in this situation. '
        'Requirements: '
        '(1) Describe the worst credible scenario if this situation escalates further. '
        '(2) Identify the specific trigger that could cause rapid deterioration. '
        '(3) Name which markets and instruments would be most severely impacted. '
        '(4) Recommend one specific hedge or defensive position. '
        'Focus on tail risk -- the scenario that is possible but not yet priced in. '
        'Keep your analysis to 3-4 sentences. Be specific and quantitative.'
    )

    # -- Arbitrator ----------------------------------------
    arb_system = (
        'You are a senior macro strategist and impartial arbitrator. '
        'You have received four independent analyses: Bull case, Bear case, '
        'Historical precedent, and Risk Manager tail risk assessment. '
        'Your job: weigh all four against the geopolitical evidence and deliver a final verdict. '
        'Consider: escalation trajectory, historical base rates, tail risk probability, '
        'market positioning, and any dark side effects identified. '
        'Respond ONLY with valid JSON, no preamble, no markdown, no explanation outside JSON. '
        'Format exactly: {"verdict": "bullish or bearish or neutral", '
        '"confidence": 0.0-1.0, '
        '"reasoning": "2-3 sentences explaining the verdict with specific causal language"}'
    )

    # Run agents
    bull_case = _call_agent(bull_system, context, max_tokens=350)
    bear_case = _call_agent(bear_system, context, max_tokens=350)
    historian_case = _call_agent(historian_system, context, max_tokens=350)
    risk_case = _call_agent(risk_manager_system, context, max_tokens=350)

    arb_user = (
        "INTELLIGENCE REPORT:\n" + context + "\n\n"
        "BULL CASE:\n" + bull_case + "\n\n"
        "BEAR CASE:\n" + bear_case + "\n\n"
        "HISTORICAL PRECEDENT:\n" + historian_case + "\n\n"
        "TAIL RISK ASSESSMENT:\n" + risk_case + "\n\n"
        "Current escalation: " + escalation_level + " | Risk: " + risk_level + "\n"
        + ("Weakness identified: " + weakness + "\n" if weakness else "")
        + ("Dark side detected: " + dark_side + "\n" if dark_side and dark_side != 'None' else "")
        + "\nDeliver your arbitration verdict as JSON only."
    )
    arb_raw = _call_agent(arb_system, arb_user, max_tokens=350)

    # Parse arbitrator output
    mad_verdict = 'neutral'
    mad_confidence = 0.5
    mad_reasoning = arb_raw

    try:
        clean = arb_raw.replace('```json', '').replace('```', '').strip()
        arb_json = json.loads(clean)
        mad_verdict = arb_json.get('verdict', 'neutral').lower()
        if mad_verdict not in VALID_VERDICTS:
            mad_verdict = 'neutral'
        mad_confidence = float(arb_json.get('confidence', 0.5))
        mad_confidence = max(0.0, min(1.0, mad_confidence))
        mad_reasoning = arb_json.get('reasoning', '')
    except (json.JSONDecodeError, ValueError):
        pass

    print(f'   Bull: {bull_case[:80]}...')
    print(f'   Bear: {bear_case[:80]}...')
    print(f'   Historian: {historian_case[:80]}...')
    print(f'   Risk Manager: {risk_case[:80]}...')
    print(f'   Verdict: {mad_verdict} ({round(mad_confidence, 2)})')

    result = {
        'mad_bull_case': bull_case,
        'mad_bear_case': bear_case,
        'mad_historian_case': historian_case,
        'mad_risk_case': risk_case,
        'mad_verdict': mad_verdict,
        'mad_confidence': mad_confidence,
        'mad_reasoning': mad_reasoning,
    }

    # Security validation
    result = _validate_mad_output(result)

    return result


if __name__ == '__main__':
    print("\U0001f43b\U0001f43b MAD Protocol v1 — Test Run\n")

    test_report = {
        'title': 'Iran Threatens Hormuz Closure as US Sanctions Tighten',
        'summary': 'Iran military moved additional forces to the Strait of Hormuz after new US sanctions targeting oil exports.',
        'sentiment': 'Bearish',
        'sentiment_score': -0.75,
        'risk_level': 'High',
        'escalation_level': 'HIGH',
        'location_name': 'Iran',
        'market_impact': 'Oil prices likely to rise 8-12% because Iran controls 20% of global oil transit. USO and XOM to benefit. SPY faces pressure as energy costs rise.',
        'tickers_affected': ['SPY', 'USO', 'XOM', 'GLD'],
        'llm_source': 'ollama',
    }

    result = run_mad_protocol(test_report)
    print(f"\n  Verdict:    {result['mad_verdict']}")
    print(f"  Confidence: {result['mad_confidence']:.0%}")
    print(f"  Reasoning:  {result['mad_reasoning'][:200]}")
