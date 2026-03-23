import os
import sys
import json
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv

# Load env
dotenv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))), '.env')
load_dotenv(dotenv_path)

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from analysis.supabase_saver import get_client
from collectors.alpha_vantage import fetch_price_change_with_fallback

# ============================================================
# GNI Outcome Verifier
# Compares GNI predictions against actual market movements
# Implements GPVS — GNI Prediction Validation Standard v1.1
# Day 1: Added 30-day window + black swan auto-detection
# ============================================================

TICKERS_TO_CHECK = ['SPY', 'GLD', 'USO', 'DXY', 'XOM', 'TLT']
BLACK_SWAN_THRESHOLD = 5.0   # SPY move % in 48h that triggers black swan
BLACK_SWAN_HOURS = 48


def fetch_price_change(ticker: str, days_ago: int) -> float | None:
    """Fetch actual price change % for a ticker over N days."""
    try:
        import urllib.request
        range_map = {3: '5d', 7: '7d', 14: '1mo', 30: '1mo', 90: '3mo', 180: '6mo'}
        period = range_map.get(days_ago, '7d')
        url = f"https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval=1d&range={period}"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())

        result = data.get('chart', {}).get('result', [])
        if not result:
            return None

        closes = result[0].get('indicators', {}).get('quote', [{}])[0].get('close', [])
        closes = [c for c in closes if c is not None]

        if len(closes) < 2:
            return None

        # For 30-day: use last 30 closes if available
        if days_ago == 30 and len(closes) >= 20:
            closes = closes[-30:] if len(closes) >= 30 else closes

        change_pct = ((closes[-1] - closes[0]) / closes[0]) * 100
        return round(change_pct, 2)

    except Exception as e:
        print(f"  ⚠️  Price fetch failed for {ticker}: {e}")
        return None


def detect_black_swan() -> dict:
    """
    Auto-detect black swan event: SPY moves >5% within 48 hours.
    Returns dict with flag and details.
    """
    try:
        import urllib.request
        url = "https://query1.finance.yahoo.com/v8/finance/chart/SPY?interval=1h&range=5d"
        req = urllib.request.Request(url, headers={
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())

        result = data.get('chart', {}).get('result', [])
        if not result:
            return {'detected': False, 'spy_48h_change': None}

        closes = result[0].get('indicators', {}).get('quote', [{}])[0].get('close', [])
        closes = [c for c in closes if c is not None]

        # Take last 48 hourly candles
        last_48 = closes[-BLACK_SWAN_HOURS:] if len(closes) >= BLACK_SWAN_HOURS else closes

        if len(last_48) < 2:
            return {'detected': False, 'spy_48h_change': None}

        change_48h = ((last_48[-1] - last_48[0]) / last_48[0]) * 100
        change_48h = round(change_48h, 2)
        detected = abs(change_48h) >= BLACK_SWAN_THRESHOLD

        if detected:
            direction = "DOWN" if change_48h < 0 else "UP"
            print(f"  🚨 BLACK SWAN DETECTED: SPY {direction} {abs(change_48h):.1f}% in 48h")

        return {
            'detected': detected,
            'spy_48h_change': change_48h,
            'threshold_used': BLACK_SWAN_THRESHOLD,
        }

    except Exception as e:
        print(f"  ⚠️  Black swan check failed: {e}")
        return {'detected': False, 'spy_48h_change': None}


def calculate_accuracy_score(
    predicted_sentiment: str,
    spy_change_3d: float | None,
    spy_change_7d: float | None,
    spy_change_30d: float | None = None,
    black_swan: bool = False,
    context_credit: bool = False
) -> float:
    """
    Calculate GPVS accuracy score — v1.1 with 30-day window.
    - Full credit (1.0): direction correct in 2+ timeframes
    - Partial credit (0.5): direction correct in 1 timeframe
    - Context credit (0.25): black swan overrode prediction
    - No credit (0.0): direction wrong, no mitigating factors
    """
    if black_swan or context_credit:
        return 0.25

    if predicted_sentiment is None:
        return 0.0

    is_bearish = predicted_sentiment.lower() == 'bearish'
    is_bullish = predicted_sentiment.lower() == 'bullish'

    results = []

    for change in [spy_change_3d, spy_change_7d, spy_change_30d]:
        if change is None:
            continue
        if is_bearish and change < 0:
            results.append(True)
        elif is_bullish and change > 0:
            results.append(True)
        else:
            results.append(False)

    if not results:
        return 0.0

    correct = sum(results)
    total = len(results)

    if correct >= 2:
        return 1.0
    elif correct == 1:
        return 0.5
    else:
        return 0.0


def check_human_review_needed(
    predicted_sentiment: str,
    spy_change_3d: float | None,
    accuracy_score: float
) -> bool:
    """Check if human review is needed per GPVS rules."""
    if spy_change_3d is not None and abs(spy_change_3d) > 3.0:
        return True
    if accuracy_score == 0.0:
        return True
    return False




# Financial event categories for expanded GPVS
FINANCIAL_EVENT_KEYWORDS = {
    'currency_shock':   ['currency collapse', 'devaluation', 'capital flight', 'hyperinflation'],
    'commodity_shock':  ['oil price spike', 'commodity shock', 'food crisis', 'energy crisis'],
    'banking_crisis':   ['bank run', 'banking crisis', 'credit crunch', 'liquidity crisis'],
    'market_crash':     ['market crash', 'stock market crash', 'circuit breaker', 'sell-off'],
    'debt_crisis':      ['debt default', 'debt ceiling', 'sovereign debt', 'bond yield spike'],
    'trade_shock':      ['trade war', 'tariff', 'sanctions', 'export control', 'trade embargo'],
}


def detect_financial_event_category(title: str, summary: str) -> str | None:
    """
    Detect the primary financial event category from report text.
    Used to enrich GPVS records with event type for pattern analysis.
    """
    text = f'{title} {summary}'.lower()
    for category, keywords in FINANCIAL_EVENT_KEYWORDS.items():
        if any(kw in text for kw in keywords):
            return category
    return None


def check_escalation_accuracy(predicted_level: str, actual_spy_change: float | None) -> bool | None:
    """
    Check if escalation level prediction was accurate.
    CRITICAL/HIGH prediction is correct if SPY moved >2% in either direction.
    MODERATE/LOW prediction is correct if SPY stayed within +-1%.
    """
    if actual_spy_change is None:
        return None
    abs_move = abs(actual_spy_change)
    if predicted_level in ['CRITICAL', 'HIGH']:
        return abs_move >= 2.0
    elif predicted_level in ['MODERATE', 'ELEVATED']:
        return 0.5 <= abs_move < 3.0
    elif predicted_level == 'LOW':
        return abs_move < 1.0
    return None
def verify_pending_outcomes():
    """
    Fetch reports that need outcome verification and measure them.
    Runs reports that are 3+ days old and haven't been verified yet.
    Now includes 30-day window and black swan auto-detection.
    """
    client = get_client()
    if not client:
        print("❌ Cannot connect to Supabase")
        return

    print("\n📊 GNI Outcome Verifier — GPVS v1.1")
    print("=" * 50)

    # Auto-detect black swan before processing reports
    print("  Checking for black swan events...")
    black_swan_result = detect_black_swan()
    black_swan_active = black_swan_result['detected']

    cutoff = (datetime.now(timezone.utc) - timedelta(days=3)).isoformat()
    already_verified = client.table('prediction_outcomes').select('report_id').execute()
    verified_ids = {r['report_id'] for r in (already_verified.data or [])}

    reports_result = client.table('reports') \
        .select('id, title, sentiment, risk_level, tickers_affected, created_at') \
        .lte('created_at', cutoff) \
        .order('created_at', desc=True) \
        .limit(20) \
        .execute()

    reports = [r for r in (reports_result.data or []) if r['id'] not in verified_ids]

    if not reports:
        print("  ✅ No pending outcomes to verify")
        return

    print(f"  Found {len(reports)} reports to verify")
    verified_count = 0

    for report in reports:
        print(f"\n  Verifying: {report['title'][:60]}...")
        print(f"  Prediction: {report['sentiment']} | Risk: {report['risk_level']}")

        # Fetch price changes across all timeframes
        spy_180d = None  # initialized before fetch
        gld_180d = None
        direction_180d = None
        spy_3d  = fetch_price_change_with_fallback('SPY', 3)
        gld_3d  = fetch_price_change_with_fallback('GLD', 3)
        uso_3d  = fetch_price_change_with_fallback('USO', 3)

        spy_7d  = fetch_price_change_with_fallback('SPY', 7)
        gld_7d  = fetch_price_change_with_fallback('GLD', 7)
        uso_7d  = fetch_price_change_with_fallback('USO', 7)

        spy_30d  = fetch_price_change_with_fallback('SPY', 30)
        gld_30d  = fetch_price_change_with_fallback('GLD', 30)
        uso_30d  = fetch_price_change_with_fallback('USO', 30)
        spy_180d = fetch_price_change_with_fallback('SPY', 180)
        gld_180d = fetch_price_change_with_fallback('GLD', 180)

        # Expanded tickers: dollar, oil stock, bonds
        dxy_7d  = fetch_price_change_with_fallback('DXY', 7)
        xom_7d  = fetch_price_change_with_fallback('XOM', 7)
        tlt_7d  = fetch_price_change_with_fallback('TLT', 7)

        # Financial event category detection
        fin_category = detect_financial_event_category(
            report.get('title', ''), report.get('summary', '')
        )

        # Escalation level accuracy
        escalation_accurate = check_escalation_accuracy(
            report.get('risk_level', ''), spy_3d
        )

        print(f"  SPY: 3d={spy_3d}% / 7d={spy_7d}% / 30d={spy_30d}% / 180d={spy_180d}%")
        print(f"  GLD: 3d={gld_3d}% / 7d={gld_7d}% / 30d={gld_30d}%")
        print(f"  USO: 3d={uso_3d}% / 7d={uso_7d}% / 30d={uso_30d}%")

        sentiment = report.get('sentiment', 'Neutral')

        def direction(change, sent):
            if change is None:
                return None
            if sent.lower() == 'bearish':
                return change < 0
            elif sent.lower() == 'bullish':
                return change > 0
            return None

        direction_3d   = direction(spy_3d, sentiment)
        direction_7d   = direction(spy_7d, sentiment)
        direction_30d  = direction(spy_30d, sentiment)
        direction_180d = direction(spy_180d, sentiment)

        accuracy = calculate_accuracy_score(
            sentiment, spy_3d, spy_7d, spy_30d,
            black_swan=black_swan_active
        )
        review_needed = check_human_review_needed(sentiment, spy_3d, accuracy)

        print(f"  Accuracy Score: {accuracy} | Black Swan: {black_swan_active} | Review: {review_needed}")

        record = {
            'report_id': report['id'],
            'run_at': report['created_at'],
            'predicted_sentiment': sentiment,
            'predicted_risk': report.get('risk_level', ''),
            'tickers_checked': TICKERS_TO_CHECK,
            'spy_change_3d': spy_3d,
            'gld_change_3d': gld_3d,
            'uso_change_3d': uso_3d,
            'direction_correct_3d': direction_3d,
            'spy_change_7d': spy_7d,
            'gld_change_7d': gld_7d,
            'uso_change_7d': uso_7d,
            'direction_correct_7d': direction_7d,
            'spy_change_30d': spy_30d,
            'gld_change_30d': gld_30d,
            'uso_change_30d': uso_30d,
            'direction_correct_30d': direction_30d,
            'spy_change_180d': spy_180d,
            'gld_change_180d': gld_180d,
            'direction_correct_180d': direction_180d,
            'accuracy_score': accuracy,
            'human_review_needed': review_needed,
            'black_swan_flag': black_swan_active,
            'black_swan_48h_change': black_swan_result.get('spy_48h_change'),
            'context_credit': False,
            'status': 'measured',
            'measured_at': datetime.now(timezone.utc).isoformat(),
            'dxy_change_7d': dxy_7d,
            'xom_change_7d': xom_7d,
            'tlt_change_7d': tlt_7d,
            'financial_event_category': fin_category,
            'escalation_accurate': escalation_accurate,
        }

        client.table('prediction_outcomes').insert(record).execute()
        verified_count += 1
        print(f"  ✅ Saved outcome record")

    print(f"\n{'=' * 50}")
    print(f"  Verified: {verified_count} reports")
    print(f"  Done.")


def get_accuracy_summary() -> dict:
    """Get overall GNI prediction accuracy summary."""
    client = get_client()
    if not client:
        return {}

    result = client.table('prediction_outcomes') \
        .select('accuracy_score, direction_correct_3d, direction_correct_7d, direction_correct_30d, predicted_sentiment, measured_at') \
        .eq('status', 'measured') \
        .execute()

    outcomes = result.data or []
    if not outcomes:
        return {'total': 0, 'avg_score': 0, 'directional_3d': 0, 'directional_7d': 0, 'directional_30d': 0}

    total = len(outcomes)
    avg_score = sum(o['accuracy_score'] or 0 for o in outcomes) / total

    def pct(key):
        valid = [o for o in outcomes if o.get(key) is not None]
        if not valid:
            return 0.0
        return round(sum(1 for o in valid if o[key] is True) / len(valid) * 100, 1)

    return {
        'total': total,
        'avg_score': round(avg_score * 100, 1),
        'directional_3d': pct('direction_correct_3d'),
        'directional_7d': pct('direction_correct_7d'),
        'directional_30d': pct('direction_correct_30d'),
        'pending_review': sum(1 for o in outcomes if o.get('human_review_needed')),
    }


def get_gpvs_timeline() -> list:
    """
    Return GPVS accuracy scores over time for the /history chart.
    Returns list of {date, accuracy_score, sentiment, black_swan_flag}
    sorted oldest to newest.
    """
    client = get_client()
    if not client:
        return []

    result = client.table('prediction_outcomes') \
        .select('measured_at, accuracy_score, predicted_sentiment, black_swan_flag, spy_change_3d, spy_change_7d, spy_change_30d') \
        .eq('status', 'measured') \
        .order('measured_at', desc=False) \
        .execute()

    timeline = []
    for o in (result.data or []):
        timeline.append({
            'date': o['measured_at'][:10],
            'accuracy_score': round((o['accuracy_score'] or 0) * 100, 0),
            'sentiment': o.get('predicted_sentiment', 'Neutral'),
            'black_swan': o.get('black_swan_flag', False),
            'spy_3d': o.get('spy_change_3d'),
            'spy_7d': o.get('spy_change_7d'),
            'spy_30d': o.get('spy_change_30d'),
        })

    return timeline


if __name__ == "__main__":
    verify_pending_outcomes()

    print("\n📈 Accuracy Summary:")
    summary = get_accuracy_summary()
    print(f"  Total verified:          {summary.get('total', 0)}")
    print(f"  Average GPVS score:      {summary.get('avg_score', 0)}%")
    print(f"  3-day directional:       {summary.get('directional_3d', 0)}%")
    print(f"  7-day directional:       {summary.get('directional_7d', 0)}%")
    print(f"  30-day directional:      {summary.get('directional_30d', 0)}%")
    print(f"  Pending human review:    {summary.get('pending_review', 0)}")

    print("\n📅 GPVS Timeline (last 5):")
    timeline = get_gpvs_timeline()
    for entry in timeline[-5:]:
        swan = " 🚨 BLACK SWAN" if entry['black_swan'] else ""
        print(f"  {entry['date']} | {entry['sentiment']:8} | Score: {entry['accuracy_score']}%{swan}")
