# ============================================================
# GNI - Alpha Vantage Price Collector
# Day 3 - Primary price source, Yahoo Finance as fallback
# ============================================================

import os
import json
import urllib.request
from dotenv import load_dotenv

load_dotenv(override=False)

AV_API_KEY = os.getenv("ALPHA_VANTAGE_API_KEY", "")
AV_BASE = "https://www.alphavantage.co/query"


def fetch_price_change_av(ticker: str, days_ago: int):
    """
    Fetch price change % for ticker over days_ago using Alpha Vantage.
    Returns float or None on failure.
    """
    if not AV_API_KEY:
        print("  WARNING: ALPHA_VANTAGE_API_KEY not set")
        return None
    try:
        url = (
            AV_BASE
            + "?function=TIME_SERIES_DAILY"
            + "&symbol=" + ticker
            + "&outputsize=compact"
            + "&apikey=" + AV_API_KEY
        )
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0"
        })
        with urllib.request.urlopen(req, timeout=15) as response:
            data = json.loads(response.read())

        if "Note" in data:
            print("  WARNING: Alpha Vantage rate limit hit")
            return None

        if "Error Message" in data:
            print("  WARNING: Alpha Vantage error for " + ticker)
            return None

        ts = data.get("Time Series (Daily)", {})
        if not ts:
            return None

        dates = sorted(ts.keys(), reverse=True)
        if len(dates) < 2:
            return None

        needed = min(days_ago, len(dates) - 1)
        price_latest = float(ts[dates[0]]["4. close"])
        price_old = float(ts[dates[needed]]["4. close"])

        if price_old == 0:
            return None

        change_pct = ((price_latest - price_old) / price_old) * 100
        return round(change_pct, 2)

    except Exception as e:
        print("  WARNING: Alpha Vantage fetch failed for " + ticker + ": " + str(e))
        return None


def fetch_price_change_with_fallback(ticker: str, days_ago: int):
    """
    Primary: Alpha Vantage. Fallback: Yahoo Finance.
    Returns float or None.
    """
    result = fetch_price_change_av(ticker, days_ago)
    if result is not None:
        print("  [AV] " + ticker + " " + str(days_ago) + "d: " + str(result) + "%")
        return result

    print("  [AV->Yahoo fallback] " + ticker + " " + str(days_ago) + "d")
    return _yahoo_fallback(ticker, days_ago)


def _yahoo_fallback(ticker: str, days_ago: int):
    """Yahoo Finance fallback — original outcome_verifier logic."""
    try:
        range_map = {3: "5d", 7: "7d", 14: "1mo", 30: "1mo"}
        period = range_map.get(days_ago, "7d")
        url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            + ticker
            + "?interval=1d&range=" + period
        )
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"
        })
        with urllib.request.urlopen(req, timeout=10) as response:
            data = json.loads(response.read())
        result = data.get("chart", {}).get("result", [])
        if not result:
            return None
        closes = result[0].get("indicators", {}).get("quote", [{}])[0].get("close", [])
        closes = [c for c in closes if c is not None]
        if len(closes) < 2:
            return None
        if days_ago == 30 and len(closes) >= 20:
            closes = closes[-30:] if len(closes) >= 30 else closes
        change_pct = ((closes[-1] - closes[0]) / closes[0]) * 100
        return round(change_pct, 2)
    except Exception as e:
        print("  WARNING: Yahoo fallback failed for " + ticker + ": " + str(e))
        return None
