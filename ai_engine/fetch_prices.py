# ============================================================
# GNI fetch_prices.py -- Stock Standby Architecture (P4)
# Fetches Yahoo Finance prices during NYSE hours
# Upserts to stock_prices Supabase table
# Acts as warm cache -- stocks page never shows blank
# Runs via gni_market.yml during NYSE hours (14:30-21:00 UTC)
# GNI-R-237: fetch_prices uses GROQ_MODEL for nothing -- no LLM calls
# ============================================================

import os
import json
import time
import requests
from datetime import datetime, timezone
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv('SUPABASE_URL', '')
SUPABASE_KEY = os.getenv('SUPABASE_SERVICE_KEY', '')

# Key tickers to pre-fetch
TICKERS = ['SPY', 'GLD', 'USO', 'BTC-USD', '^DJI', '^IXIC', 'QQQ', 'TLT']

# Ranges to pre-fetch -- 1y for chart, 3d for live price
RANGES = ['3d', '7d', '1m', '1y']

INTERVAL_MAP = {
    '3d': '5m',  '7d': '1h',
    '1m': '1d',  '1y': '1wk', '10y': '1mo',
}
RANGE_MAP = {
    '3d': '5d',  '7d': '7d',
    '1m': '1mo', '1y': '1y', '10y': '10y',
}

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36',
    'Accept': 'application/json',
}


def fetch_yahoo(ticker: str, period: str, interval: str) -> dict | None:
    """Fetch chart data from Yahoo Finance."""
    url = f'https://query1.finance.yahoo.com/v8/finance/chart/{ticker}?interval={interval}&range={period}'
    try:
        r = requests.get(url, headers=HEADERS, timeout=15)
        if not r.ok:
            print(f'  WARNING: Yahoo {ticker} {period} returned {r.status_code}')
            return None
        data = r.json()
        return data.get('chart', {}).get('result', [None])[0]
    except Exception as e:
        print(f'  WARNING: Yahoo {ticker} {period} error: {str(e)[:60]}')
        return None


def build_record(ticker: str, range_key: str) -> dict | None:
    """Build a stock_prices record for one ticker+range combo."""
    result = fetch_yahoo(ticker, RANGE_MAP[range_key], INTERVAL_MAP[range_key])
    if not result:
        return None

    meta = result.get('meta', {})
    timestamps = result.get('timestamp', [])
    closes = result.get('indicators', {}).get('quote', [{}])[0].get('close', [])

    chart_data = [
        {
            'date': datetime.utcfromtimestamp(ts).strftime('%Y-%m-%d'),
            'close': round(closes[i], 4) if closes[i] else None,
        }
        for i, ts in enumerate(timestamps)
        if i < len(closes) and closes[i] is not None
    ]

    current_price = meta.get('regularMarketPrice', 0)
    prev_close    = meta.get('chartPreviousClose') or meta.get('previousClose', current_price)

    day_change         = round(current_price - prev_close, 4)
    day_change_pct     = round(((current_price - prev_close) / prev_close * 100), 2) if prev_close else 0

    first_close = chart_data[0]['close'] if chart_data else None
    range_change     = round(current_price - first_close, 4) if first_close else 0
    range_change_pct = round(((current_price - first_close) / first_close * 100), 2) if first_close else 0

    return {
        'ticker':               ticker,
        'range':                range_key,
        'current_price':        current_price,
        'day_change':           day_change,
        'day_change_percent':   day_change_pct,
        'range_change':         range_change,
        'range_change_percent': range_change_pct,
        'currency':             meta.get('currency', 'USD'),
        'name':                 meta.get('longName') or meta.get('shortName') or ticker,
        'chart_data':           chart_data,
        'fetched_at':           datetime.now(timezone.utc).isoformat(),
    }


def upsert_record(record: dict) -> bool:
    """Upsert one record to Supabase stock_prices table."""
    if not SUPABASE_URL or not SUPABASE_KEY:
        print('  ERROR: Missing SUPABASE_URL or SUPABASE_SERVICE_KEY')
        return False
    try:
        url = f'{SUPABASE_URL}/rest/v1/stock_prices'
        headers = {
            'apikey':        SUPABASE_KEY,
            'Authorization': f'Bearer {SUPABASE_KEY}',
            'Content-Type':  'application/json',
            'Prefer':        'resolution=merge-duplicates',
        }
        body = dict(record)
        body['chart_data'] = json.dumps(record['chart_data'])
        r = requests.post(url, headers=headers, json=body, timeout=15)
        if r.ok:
            return True
        print(f'  WARNING: Supabase upsert {record["ticker"]} {record["range"]}: {r.status_code} {r.text[:80]}')
        return False
    except Exception as e:
        print(f'  ERROR: Supabase upsert failed: {str(e)[:60]}')
        return False


def main():
    print('=' * 60)
    print(f'GNI fetch_prices.py -- Stock Standby')
    print(f'Start: {datetime.now(timezone.utc).isoformat()}')
    print(f'Tickers: {TICKERS}')
    print(f'Ranges:  {RANGES}')
    print('=' * 60)

    ok = 0
    fail = 0

    for ticker in TICKERS:
        for range_key in RANGES:
            print(f'  Fetching {ticker} {range_key}...')
            record = build_record(ticker, range_key)
            if not record:
                print(f'  SKIP {ticker} {range_key} -- no data')
                fail += 1
                continue
            if upsert_record(record):
                print(f'  OK {ticker} {range_key} -- price={record["current_price"]} chart={len(record["chart_data"])} pts')
                ok += 1
            else:
                fail += 1
            time.sleep(1)  # polite delay between Yahoo requests

    print('=' * 60)
    print(f'Done: {ok} OK, {fail} failed')
    print(f'End: {datetime.now(timezone.utc).isoformat()}')
    print('=' * 60)


if __name__ == '__main__':
    main()
