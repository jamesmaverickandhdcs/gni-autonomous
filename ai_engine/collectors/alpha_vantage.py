# ============================================================
# GNI Price Collector -- Rewritten
# Primary:  Yahoo Finance (free, no hard limit)
# Fallback: Twelve Data (free, 800 calls/day)
# Removed:  Alpha Vantage (25 calls/day -- too low for volume)
# Architecture decision: March 22, 2026
# ============================================================

import os
import json
import requests
from dotenv import load_dotenv
load_dotenv(override=False)

TWELVE_DATA_API_KEY = os.getenv("TWELVE_DATA_API_KEY", "")
TWELVE_DATA_BASE = "https://api.twelvedata.com"


def _yahoo_primary(ticker: str, days_ago: int):
    """
    Primary price source: Yahoo Finance.
    Free, no hard limit, works most of the time.
    Occasionally blocks Vercel IPs -- Twelve Data fallback handles this.
    """
    try:
        range_map = {3: "5d", 7: "7d", 14: "1mo", 30: "1mo"}
        period = range_map.get(days_ago, "7d")

        # Handle crypto tickers -- Yahoo uses different format
        yahoo_ticker = ticker
        if ticker in ["BTC-USD", "ETH-USD"]:
            yahoo_ticker = ticker  # Yahoo supports BTC-USD directly

        url = (
            "https://query1.finance.yahoo.com/v8/finance/chart/"
            + yahoo_ticker
            + "?interval=1d&range=" + period
        )
        response = requests.get(
            url,
            headers={"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64)"},
            timeout=10,
        )
        if response.status_code != 200:
            return None

        data = response.json()
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
        print("  [Yahoo] Failed for " + ticker + ": " + str(e)[:60])
        return None


def _twelve_data_fallback(ticker: str, days_ago: int):
    """
    Fallback price source: Twelve Data.
    Free tier: 800 calls/day -- covers our volume easily.
    Used when Yahoo Finance blocks Vercel IPs.
    """
    if not TWELVE_DATA_API_KEY:
        print("  [TwelveData] No API key -- skipping fallback")
        return None

    try:
        # Twelve Data uses different crypto format
        td_ticker = ticker
        if ticker == "BTC-USD":
            td_ticker = "BTC/USD"
        elif ticker == "ETH-USD":
            td_ticker = "ETH/USD"

        # Map days_ago to outputsize
        outputsize = max(days_ago + 5, 10)

        url = (
            TWELVE_DATA_BASE + "/time_series"
            + "?symbol=" + td_ticker
            + "&interval=1day"
            + "&outputsize=" + str(outputsize)
            + "&apikey=" + TWELVE_DATA_API_KEY
        )
        response = requests.get(url, timeout=15)
        if response.status_code != 200:
            print("  [TwelveData] HTTP " + str(response.status_code) + " for " + ticker)
            return None

        data = response.json()

        # Check for API errors
        if data.get("status") == "error":
            print("  [TwelveData] Error for " + ticker + ": " + data.get("message", "")[:60])
            return None

        values = data.get("values", [])
        if not values or len(values) < 2:
            return None

        # Values are newest first
        price_latest = float(values[0]["close"])
        needed = min(days_ago, len(values) - 1)
        price_old = float(values[needed]["close"])

        if price_old == 0:
            return None

        change_pct = ((price_latest - price_old) / price_old) * 100
        return round(change_pct, 2)

    except Exception as e:
        print("  [TwelveData] Failed for " + ticker + ": " + str(e)[:60])
        return None


def fetch_price_change_with_fallback(ticker: str, days_ago: int):
    """
    Main entry point -- called by outcome_verifier.py.
    Primary: Yahoo Finance.
    Fallback: Twelve Data.
    Returns float (% change) or None.
    """
    # Primary: Yahoo Finance
    result = _yahoo_primary(ticker, days_ago)
    if result is not None:
        print("  [Yahoo] " + ticker + " " + str(days_ago) + "d: " + str(result) + "%")
        return result

    # Fallback: Twelve Data
    print("  [Yahoo->TwelveData fallback] " + ticker + " " + str(days_ago) + "d")
    result = _twelve_data_fallback(ticker, days_ago)
    if result is not None:
        print("  [TwelveData] " + ticker + " " + str(days_ago) + "d: " + str(result) + "%")
        return result

    print("  [Both failed] " + ticker + " " + str(days_ago) + "d")
    return None


if __name__ == "__main__":
    print("\nGNI Price Collector -- Test Run\n")
    test_tickers = ["SPY", "GLD", "BTC-USD", "SOXX", "VIX"]
    for t in test_tickers:
        result = fetch_price_change_with_fallback(t, 7)
        if result is not None:
            print("  " + t + " 7d: " + str(result) + "%")
        else:
            print("  " + t + ": No data")
