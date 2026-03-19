# ============================================================
# GNI - MAD Protocol (Multi-Agent Debate)
# Day 3 - Three-agent debate: Bull vs Bear -> Arbitrator verdict
# L23: Model name via GROQ_MODEL env var - never hardcoded
# ============================================================

import os
import json
import re
from groq import Groq

client = Groq(api_key=os.getenv('GROQ_API_KEY'))
MODEL = os.getenv('GROQ_MODEL', 'llama3-70b-8192')


def _call_agent(system_prompt, user_prompt, max_tokens=400):
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
        return '[Agent error: ' + str(e) + ']'


def run_mad_protocol(report):
    headline = report.get('headline', 'No headline')
    summary = report.get('summary', '')[:800]
    prediction = report.get('prediction', '')
    sentiment = report.get('sentiment', 'neutral')
    llm_source = report.get('llm_source', 'unknown')
    context = (
        'Headline: ' + headline + chr(10)
        + 'Summary: ' + summary + chr(10)
        + 'Prediction: ' + prediction + chr(10)
        + 'Sentiment: ' + sentiment + chr(10)
        + 'LLM Source: ' + llm_source
    )
    bull_system = (
        'You are a bullish macro analyst. Argue the strongest BULLISH case '
        'for global markets based on the intelligence report. Be specific, '
        'cite the report content, explain why this is a buying opportunity. '
        'Keep your argument to 3-4 sentences.'
    )
    bull_case = _call_agent(bull_system, context, max_tokens=350)
    bear_system = (
        'You are a bearish macro analyst. Argue the strongest BEARISH case '
        'for global markets based on the intelligence report. Be specific, '
        'cite the report content, explain why this is a risk-off signal. '
        'Keep your argument to 3-4 sentences.'
    )
    bear_case = _call_agent(bear_system, context, max_tokens=350)
    verdicts = ["bullish", "bearish", "neutral"]
    verdict_hint = "bullish or bearish or neutral"
    arb_system = (
        'You are a senior macro strategist and impartial arbitrator. '
        'Weigh the bull and bear cases and deliver a final verdict. '
        'Respond ONLY with valid JSON, no preamble, no markdown. '
        'Format: {"verdict": "bullish or bearish or neutral", "confidence": 0.0-1.0, "reasoning": "2-3 sentences"}'
    )
    arb_user = (
        'REPORT CONTEXT:' + chr(10) + context + chr(10) + chr(10)
        + 'BULL CASE:' + chr(10) + bull_case + chr(10) + chr(10)
        + 'BEAR CASE:' + chr(10) + bear_case + chr(10) + chr(10)
        + 'Deliver your arbitration verdict as JSON only.'
    )
    arb_raw = _call_agent(arb_system, arb_user, max_tokens=300)
    mad_verdict = 'neutral'
    mad_confidence = 0.5
    mad_reasoning = arb_raw
    try:
        clean = arb_raw.replace('```json', '').replace('```', '').strip()
        arb_json = json.loads(clean)
        mad_verdict = arb_json.get('verdict', 'neutral').lower()
        if mad_verdict not in verdicts:
            mad_verdict = 'neutral'
        mad_confidence = float(arb_json.get('confidence', 0.5))
        mad_confidence = max(0.0, min(1.0, mad_confidence))
        mad_reasoning = arb_json.get('reasoning', '')
    except (json.JSONDecodeError, ValueError):
        pass
    print('   Bull: ' + bull_case[:80] + '...')
    print('   Bear: ' + bear_case[:80] + '...')
    print('   Verdict: ' + mad_verdict + ' (' + str(round(mad_confidence, 2)) + ')')
    return {
        'mad_bull_case': bull_case,
        'mad_bear_case': bear_case,
        'mad_verdict': mad_verdict,
        'mad_confidence': mad_confidence,
        'mad_reasoning': mad_reasoning,
    }
