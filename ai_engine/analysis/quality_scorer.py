import os
import re
from datetime import datetime, timezone

# ============================================================
# GNI Report Quality Scorer — Day 1
# 10-point rubric scoring LLM-generated reports
# Dimensions: specificity, market linkage, source consensus,
#             analytical novelty, prediction specificity
# ============================================================

KNOWN_TICKERS = ['SPY', 'AAPL', 'JPM', 'XOM', 'GLD', 'USO', 'LMT', 'TLT', 'EWT', 'EWJ', 'FXI', 'DXY']
KNOWN_SENTIMENTS = ['bullish', 'bearish', 'neutral']
VAGUE_PHRASES = [
    'could', 'might', 'may', 'possibly', 'perhaps', 'unclear',
    'uncertain', 'unknown', 'remains to be seen', 'it depends',
    'various', 'several factors', 'complex situation'
]
MARKET_LINKAGE_WORDS = [
    'rate', 'yield', 'inflation', 'gdp', 'fed', 'central bank',
    'supply chain', 'sanctions', 'tariff', 'trade', 'oil', 'energy',
    'equity', 'bond', 'currency', 'dollar', 'export', 'import',
    'market', 'investor', 'risk', 'volatility', 'recession'
]


def score_specificity(report: dict) -> float:
    """
    Dimension 1 — Specificity (0-2 points)
    Does the report name specific countries, people, events?
    Penalises vague language.
    """
    score = 2.0
    text = f"{report.get('title','')} {report.get('summary','')} {report.get('market_impact','')}".lower()

    # Penalise vague phrases
    vague_hits = sum(1 for phrase in VAGUE_PHRASES if phrase in text)
    score -= min(vague_hits * 0.3, 1.0)

    # Reward named location
    location = report.get('location_name', '')
    if not location or location.lower() in ['global', 'unknown', '']:
        score -= 0.5

    # Reward specific title (more than 5 words)
    title_words = len(report.get('title', '').split())
    if title_words < 5:
        score -= 0.5

    return round(max(score, 0.0), 2)


def score_market_linkage(report: dict) -> float:
    """
    Dimension 2 — Market Linkage (0-2 points)
    Does the report connect geopolitical events to markets?
    """
    score = 0.0
    text = f"{report.get('market_impact','')} {report.get('summary','')}".lower()

    # Count market linkage keywords
    hits = sum(1 for word in MARKET_LINKAGE_WORDS if word in text)
    score = min(hits * 0.25, 1.5)

    # Reward having specific tickers
    tickers = report.get('tickers_affected', [])
    if len(tickers) >= 2:
        score += 0.5
    elif len(tickers) == 1:
        score += 0.25

    return round(min(score, 2.0), 2)


def score_source_consensus(report: dict) -> float:
    """
    Dimension 3 — Source Consensus (0-2 points)
    Based on source_consensus_score from LLM + number of sources used.
    """
    consensus = report.get('source_consensus_score', 0.5)
    sources = report.get('sources_used', [])
    articles_count = report.get('articles_analyzed', 1)

    # Base: LLM-reported consensus (0-1) scaled to 0-1.5
    score = consensus * 1.5

    # Reward diversity of sources
    if len(sources) >= 4:
        score += 0.5
    elif len(sources) >= 2:
        score += 0.25

    return round(min(score, 2.0), 2)


def score_analytical_novelty(report: dict) -> float:
    """
    Dimension 4 — Analytical Novelty (0-2 points)
    Does the report go beyond restating headlines?
    Rewards causal reasoning and multi-step analysis.
    """
    score = 0.0
    market_impact = report.get('market_impact', '').lower()
    summary = report.get('summary', '').lower()

    # Reward causal language
    causal_words = ['because', 'therefore', 'as a result', 'leading to',
                    'this means', 'consequently', 'driven by', 'due to',
                    'in response to', 'which could', 'likely to']
    causal_hits = sum(1 for w in causal_words if w in market_impact + summary)
    score += min(causal_hits * 0.4, 1.2)

    # Reward length of market_impact (more analysis = longer)
    impact_words = len(market_impact.split())
    if impact_words >= 40:
        score += 0.8
    elif impact_words >= 20:
        score += 0.4

    return round(min(score, 2.0), 2)


def score_prediction_specificity(report: dict) -> float:
    """
    Dimension 5 — Prediction Specificity (0-2 points)
    Is the sentiment/risk clear and directional?
    """
    score = 0.0

    # Reward clear sentiment
    sentiment = report.get('sentiment', '').lower()
    if sentiment in ['bullish', 'bearish']:
        score += 1.0
    elif sentiment == 'neutral':
        score += 0.5

    # Reward non-zero sentiment score
    sentiment_score = abs(report.get('sentiment_score', 0.0))
    if sentiment_score >= 0.6:
        score += 0.7
    elif sentiment_score >= 0.3:
        score += 0.4
    elif sentiment_score > 0:
        score += 0.2

    # Reward specific risk level
    risk = report.get('risk_level', '').lower()
    if risk in ['high', 'critical']:
        score += 0.3
    elif risk == 'medium':
        score += 0.2
    elif risk == 'low':
        score += 0.1

    return round(min(score, 2.0), 2)


def score_report(report: dict) -> dict:
    """
    Run all 5 dimensions and return quality score + breakdown.
    Total: 10 points max.
    Badge: Excellent (8+), Good (6-7.9), Fair (4-5.9), Poor (<4)
    """
    if not report:
        return {'quality_score': 0.0, 'quality_breakdown': {}, 'quality_badge': 'Poor'}

    breakdown = {
        'specificity':            score_specificity(report),
        'market_linkage':         score_market_linkage(report),
        'source_consensus':       score_source_consensus(report),
        'analytical_novelty':     score_analytical_novelty(report),
        'prediction_specificity': score_prediction_specificity(report),
    }

    total = round(sum(breakdown.values()), 2)

    if total >= 8.0:
        badge = 'Excellent'
    elif total >= 6.0:
        badge = 'Good'
    elif total >= 4.0:
        badge = 'Fair'
    else:
        badge = 'Poor'

    print(f"  📊 Quality Score: {total}/10 [{badge}]")
    for dim, val in breakdown.items():
        print(f"     {dim:28s}: {val}/2")

    return {
        'quality_score':     total,
        'quality_breakdown': breakdown,
        'quality_badge':     badge,
        'scored_at':         datetime.now(timezone.utc).isoformat(),
    }


if __name__ == "__main__":
    # Test with a sample report
    sample = {
        'title': 'US Sanctions on Iran Trigger Oil Price Surge and Market Volatility',
        'summary': 'The United States imposed new sanctions on Iran because of nuclear violations, leading to a sharp rise in crude oil prices and increased volatility in equity markets.',
        'sentiment': 'Bearish',
        'sentiment_score': -0.7,
        'source_consensus_score': 0.8,
        'location_name': 'Iran',
        'tickers_affected': ['SPY', 'USO', 'XOM'],
        'market_impact': 'Oil prices rose sharply due to supply concerns, therefore energy stocks like XOM may benefit while broader equities face headwinds. As a result of sanctions, dollar strength could increase driving TLT lower.',
        'risk_level': 'High',
        'sources_used': ['Reuters', 'BBC', 'Al Jazeera', 'Bloomberg'],
        'articles_analyzed': 8,
    }

    result = score_report(sample)
    print(f"\n  Total: {result['quality_score']}/10 — {result['quality_badge']}")
