# ============================================================
# GNI Semantic Validator — Day 11
# Validates LLM report output beyond JSON schema
# Catches: sentiment/score mismatch, hallucinated tickers,
# extreme claims, inconsistent risk levels, empty fields
# ============================================================

ALLOWED_TICKERS = {
    'SPY', 'AAPL', 'JPM', 'XOM', 'GLD', 'USO',
    'LMT', 'TLT', 'EWT', 'EWJ', 'FXI', 'DXY',
}

VALID_SENTIMENTS = {'bullish', 'bearish', 'neutral'}
VALID_RISK_LEVELS = {'low', 'medium', 'high', 'critical'}

# Risk levels that are inconsistent with Bullish sentiment
BEARISH_RISK_LEVELS = {'critical'}

# Minimum market_impact length to be meaningful
MIN_MARKET_IMPACT_LENGTH = 50

# Known region names that should not appear as location_name
INVALID_LOCATIONS = {
    'middle east', 'europe', 'asia', 'africa', 'latin america',
    'south america', 'north america', 'southeast asia', 'east asia',
    'central asia', 'global', 'worldwide', 'international',
    'western', 'eastern', 'northern', 'southern',
}


def validate_report(report: dict) -> dict:
    """
    Semantically validate an LLM-generated report.

    Returns:
        dict with keys:
            is_valid: bool
            warnings: list of non-fatal issues
            errors: list of fatal issues
            fixed_report: report with auto-corrections applied
    """
    errors = []
    warnings = []
    fixed = dict(report)

    sentiment = str(report.get('sentiment', '')).lower().strip()
    sentiment_score = report.get('sentiment_score', 0.0)
    risk_level = str(report.get('risk_level', '')).lower().strip()
    tickers = report.get('tickers_affected', [])
    market_impact = str(report.get('market_impact', ''))
    location = str(report.get('location_name', '')).lower().strip()
    source_consensus = report.get('source_consensus_score', 0.0)

    # Check 1: Sentiment field is valid
    if sentiment not in VALID_SENTIMENTS:
        warnings.append(f"Unknown sentiment: {sentiment!r} — defaulting to Neutral")
        fixed['sentiment'] = 'Neutral'
        fixed['sentiment_score'] = 0.0

    # Check 2: Sentiment direction matches sentiment_score
    if sentiment == 'bearish' and sentiment_score > 0.1:
        warnings.append(f"Sentiment mismatch: Bearish but score={sentiment_score:.2f} — correcting score")
        fixed['sentiment_score'] = -abs(sentiment_score)
    elif sentiment == 'bullish' and sentiment_score < -0.1:
        warnings.append(f"Sentiment mismatch: Bullish but score={sentiment_score:.2f} — correcting score")
        fixed['sentiment_score'] = abs(sentiment_score)
    elif sentiment == 'neutral' and abs(sentiment_score) > 0.5:
        warnings.append(f"Sentiment mismatch: Neutral but score={sentiment_score:.2f} — moderating score")
        fixed['sentiment_score'] = sentiment_score * 0.3

    # Check 3: Extreme confidence flag
    if abs(sentiment_score) >= 0.99:
        warnings.append(f"Extreme sentiment score: {sentiment_score:.2f} — LLM overconfidence detected")
        fixed['sentiment_score'] = sentiment_score * 0.85

    # Check 4: Risk level is valid
    if risk_level not in VALID_RISK_LEVELS:
        warnings.append(f"Unknown risk level: {risk_level!r} — defaulting to Medium")
        fixed['risk_level'] = 'Medium'

    # Check 5: Critical risk with Bullish sentiment is suspicious
    if risk_level == 'critical' and sentiment == 'bullish':
        warnings.append("Inconsistency: Critical risk with Bullish sentiment — unusual combination flagged")

    # Check 6: Tickers are from allowed list
    if tickers:
        valid_tickers = [t for t in tickers if t.upper() in ALLOWED_TICKERS]
        invalid_tickers = [t for t in tickers if t.upper() not in ALLOWED_TICKERS]
        if invalid_tickers:
            warnings.append(f"Hallucinated tickers removed: {invalid_tickers} — keeping only allowed list")
            fixed['tickers_affected'] = valid_tickers if valid_tickers else ['SPY']

    # Check 7: Market impact has sufficient content
    if len(market_impact.strip()) < MIN_MARKET_IMPACT_LENGTH:
        warnings.append(f"Market impact too short ({len(market_impact)} chars) — may lack analysis depth")

    # Check 8: Location is not a region
    if location in INVALID_LOCATIONS:
        warnings.append(f"Location is a region not a country: {location!r} — may reduce geocoding accuracy")

    # Check 9: Source consensus score is in valid range
    try:
        scs = float(source_consensus)
        if scs < 0.0 or scs > 1.0:
            warnings.append(f"source_consensus_score out of range: {scs} — clamping to [0,1]")
            fixed['source_consensus_score'] = max(0.0, min(1.0, scs))
    except (TypeError, ValueError):
        warnings.append(f"source_consensus_score invalid: {source_consensus!r} — defaulting to 0.5")
        fixed['source_consensus_score'] = 0.5

    # Check 10: Title and summary not empty
    if not report.get('title', '').strip():
        errors.append("Missing title — report cannot be saved without a title")
    if not report.get('summary', '').strip():
        errors.append("Missing summary — report cannot be saved without a summary")

    is_valid = len(errors) == 0

    return {
        'is_valid': is_valid,
        'warnings': warnings,
        'errors': errors,
        'fixed_report': fixed,
        'checks_passed': 10 - len(warnings) - len(errors),
        'total_checks': 10,
    }


if __name__ == '__main__':
    print("\U0001f9ea GNI Semantic Validator — Test Run\n")

    test_cases = [
        {
            'name': 'Clean report',
            'report': {
                'title': 'Iran threatens Hormuz closure amid sanctions',
                'summary': 'Iran military moves near key chokepoint.',
                'sentiment': 'Bearish',
                'sentiment_score': -0.75,
                'risk_level': 'High',
                'location_name': 'Iran',
                'tickers_affected': ['SPY', 'GLD', 'USO'],
                'market_impact': 'Oil prices will rise because Iran controls access to Hormuz. This leads to energy sector gains therefore USO rises. As a result SPY faces pressure.',
                'source_consensus_score': 0.8,
            }
        },
        {
            'name': 'Sentiment mismatch',
            'report': {
                'title': 'Markets crash on war fears',
                'summary': 'Global markets fell sharply.',
                'sentiment': 'Bearish',
                'sentiment_score': 0.85,
                'risk_level': 'Critical',
                'location_name': 'Middle East',
                'tickers_affected': ['SPY', 'TSLA', 'NVDA', 'FAKE'],
                'market_impact': 'Bad.',
                'source_consensus_score': 1.5,
            }
        },
    ]

    for tc in test_cases:
        print(f"Test: {tc['name']}")
        result = validate_report(tc['report'])
        print(f"  Valid: {result['is_valid']}")
        print(f"  Checks passed: {result['checks_passed']}/{result['total_checks']}")
        if result['warnings']:
            for w in result['warnings']:
                print(f"  \u26a0\ufe0f  {w}")
        if result['errors']:
            for e in result['errors']:
                print(f"  \u274c {e}")
        print()
