"""
rewrite_price_collector.py
Rewrites ai_engine/collectors/alpha_vantage.py

NEW ARCHITECTURE:
  Primary:  Yahoo Finance (free, no hard limit)
  Fallback: Twelve Data (free, 800 calls/day)
  Removed:  Alpha Vantage (25 calls/day -- too low for our volume)

Public function fetch_price_change_with_fallback() unchanged --
all callers (outcome_verifier.py) work without any changes.

L20: alpha_vantage.py read before this script was written.
L45: py_compile check at end.
"""

import os
import py_compile

OUT_PATH = r"C:\HDCS_Project\03\GNI_Autonomous\ai_engine\collectors\alpha_vantage.py"

content = (
    "# ============================================================\n"
    "# GNI Price Collector -- Rewritten\n"
    "# Primary:  Yahoo Finance (free, no hard limit)\n"
    "# Fallback: Twelve Data (free, 800 calls/day)\n"
    "# Removed:  Alpha Vantage (25 calls/day -- too low for volume)\n"
    "# Architecture decision: March 22, 2026\n"
    "# ============================================================\n"
    "\n"
    "import os\n"
    "import json\n"
    "import requests\n"
    "from dotenv import load_dotenv\n"
    "load_dotenv(override=False)\n"
    "\n"
    "TWELVE_DATA_API_KEY = os.getenv(\"TWELVE_DATA_API_KEY\", \"\")\n"
    "TWELVE_DATA_BASE = \"https://api.twelvedata.com\"\n"
    "\n"
    "\n"
    "def _yahoo_primary(ticker: str, days_ago: int):\n"
    "    \"\"\"\n"
    "    Primary price source: Yahoo Finance.\n"
    "    Free, no hard limit, works most of the time.\n"
    "    Occasionally blocks Vercel IPs -- Twelve Data fallback handles this.\n"
    "    \"\"\"\n"
    "    try:\n"
    "        range_map = {3: \"5d\", 7: \"7d\", 14: \"1mo\", 30: \"1mo\"}\n"
    "        period = range_map.get(days_ago, \"7d\")\n"
    "\n"
    "        # Handle crypto tickers -- Yahoo uses different format\n"
    "        yahoo_ticker = ticker\n"
    "        if ticker in [\"BTC-USD\", \"ETH-USD\"]:\n"
    "            yahoo_ticker = ticker  # Yahoo supports BTC-USD directly\n"
    "\n"
    "        url = (\n"
    "            \"https://query1.finance.yahoo.com/v8/finance/chart/\"\n"
    "            + yahoo_ticker\n"
    "            + \"?interval=1d&range=\" + period\n"
    "        )\n"
    "        response = requests.get(\n"
    "            url,\n"
    "            headers={\"User-Agent\": \"Mozilla/5.0 (Windows NT 10.0; Win64; x64)\"},\n"
    "            timeout=10,\n"
    "        )\n"
    "        if response.status_code != 200:\n"
    "            return None\n"
    "\n"
    "        data = response.json()\n"
    "        result = data.get(\"chart\", {}).get(\"result\", [])\n"
    "        if not result:\n"
    "            return None\n"
    "\n"
    "        closes = result[0].get(\"indicators\", {}).get(\"quote\", [{}])[0].get(\"close\", [])\n"
    "        closes = [c for c in closes if c is not None]\n"
    "\n"
    "        if len(closes) < 2:\n"
    "            return None\n"
    "\n"
    "        if days_ago == 30 and len(closes) >= 20:\n"
    "            closes = closes[-30:] if len(closes) >= 30 else closes\n"
    "\n"
    "        change_pct = ((closes[-1] - closes[0]) / closes[0]) * 100\n"
    "        return round(change_pct, 2)\n"
    "\n"
    "    except Exception as e:\n"
    "        print(\"  [Yahoo] Failed for \" + ticker + \": \" + str(e)[:60])\n"
    "        return None\n"
    "\n"
    "\n"
    "def _twelve_data_fallback(ticker: str, days_ago: int):\n"
    "    \"\"\"\n"
    "    Fallback price source: Twelve Data.\n"
    "    Free tier: 800 calls/day -- covers our volume easily.\n"
    "    Used when Yahoo Finance blocks Vercel IPs.\n"
    "    \"\"\"\n"
    "    if not TWELVE_DATA_API_KEY:\n"
    "        print(\"  [TwelveData] No API key -- skipping fallback\")\n"
    "        return None\n"
    "\n"
    "    try:\n"
    "        # Twelve Data uses different crypto format\n"
    "        td_ticker = ticker\n"
    "        if ticker == \"BTC-USD\":\n"
    "            td_ticker = \"BTC/USD\"\n"
    "        elif ticker == \"ETH-USD\":\n"
    "            td_ticker = \"ETH/USD\"\n"
    "\n"
    "        # Map days_ago to outputsize\n"
    "        outputsize = max(days_ago + 5, 10)\n"
    "\n"
    "        url = (\n"
    "            TWELVE_DATA_BASE + \"/time_series\"\n"
    "            + \"?symbol=\" + td_ticker\n"
    "            + \"&interval=1day\"\n"
    "            + \"&outputsize=\" + str(outputsize)\n"
    "            + \"&apikey=\" + TWELVE_DATA_API_KEY\n"
    "        )\n"
    "        response = requests.get(url, timeout=15)\n"
    "        if response.status_code != 200:\n"
    "            print(\"  [TwelveData] HTTP \" + str(response.status_code) + \" for \" + ticker)\n"
    "            return None\n"
    "\n"
    "        data = response.json()\n"
    "\n"
    "        # Check for API errors\n"
    "        if data.get(\"status\") == \"error\":\n"
    "            print(\"  [TwelveData] Error for \" + ticker + \": \" + data.get(\"message\", \"\")[:60])\n"
    "            return None\n"
    "\n"
    "        values = data.get(\"values\", [])\n"
    "        if not values or len(values) < 2:\n"
    "            return None\n"
    "\n"
    "        # Values are newest first\n"
    "        price_latest = float(values[0][\"close\"])\n"
    "        needed = min(days_ago, len(values) - 1)\n"
    "        price_old = float(values[needed][\"close\"])\n"
    "\n"
    "        if price_old == 0:\n"
    "            return None\n"
    "\n"
    "        change_pct = ((price_latest - price_old) / price_old) * 100\n"
    "        return round(change_pct, 2)\n"
    "\n"
    "    except Exception as e:\n"
    "        print(\"  [TwelveData] Failed for \" + ticker + \": \" + str(e)[:60])\n"
    "        return None\n"
    "\n"
    "\n"
    "def fetch_price_change_with_fallback(ticker: str, days_ago: int):\n"
    "    \"\"\"\n"
    "    Main entry point -- called by outcome_verifier.py.\n"
    "    Primary: Yahoo Finance.\n"
    "    Fallback: Twelve Data.\n"
    "    Returns float (% change) or None.\n"
    "    \"\"\"\n"
    "    # Primary: Yahoo Finance\n"
    "    result = _yahoo_primary(ticker, days_ago)\n"
    "    if result is not None:\n"
    "        print(\"  [Yahoo] \" + ticker + \" \" + str(days_ago) + \"d: \" + str(result) + \"%\")\n"
    "        return result\n"
    "\n"
    "    # Fallback: Twelve Data\n"
    "    print(\"  [Yahoo->TwelveData fallback] \" + ticker + \" \" + str(days_ago) + \"d\")\n"
    "    result = _twelve_data_fallback(ticker, days_ago)\n"
    "    if result is not None:\n"
    "        print(\"  [TwelveData] \" + ticker + \" \" + str(days_ago) + \"d: \" + str(result) + \"%\")\n"
    "        return result\n"
    "\n"
    "    print(\"  [Both failed] \" + ticker + \" \" + str(days_ago) + \"d\")\n"
    "    return None\n"
    "\n"
    "\n"
    "if __name__ == \"__main__\":\n"
    "    print(\"\\nGNI Price Collector -- Test Run\\n\")\n"
    "    test_tickers = [\"SPY\", \"GLD\", \"BTC-USD\", \"SOXX\", \"VIX\"]\n"
    "    for t in test_tickers:\n"
    "        result = fetch_price_change_with_fallback(t, 7)\n"
    "        if result is not None:\n"
    "            print(\"  \" + t + \" 7d: \" + str(result) + \"%\")\n"
    "        else:\n"
    "            print(\"  \" + t + \": No data\")\n"
)

with open(OUT_PATH, "w", encoding="utf-8") as f:
    f.write(content)

try:
    py_compile.compile(OUT_PATH, doraise=True)
    print("✅ alpha_vantage.py rewritten -- Yahoo primary, Twelve Data fallback")
    print("✅ Syntax check passed")
except py_compile.PyCompileError as e:
    print(f"❌ Syntax error: {e}")
    exit(1)

# Add TWELVE_DATA_API_KEY to workflow
WORKFLOW_DIR = r"C:\HDCS_Project\03\GNI_Autonomous\.github\workflows"
for yml_file in os.listdir(WORKFLOW_DIR):
    if not yml_file.endswith(".yml"):
        continue
    yml_path = os.path.join(WORKFLOW_DIR, yml_file)
    with open(yml_path, "r", encoding="utf-8") as f:
        yml_content = f.read()

    if "TWELVE_DATA_API_KEY" in yml_content:
        print("✅ TWELVE_DATA_API_KEY already in " + yml_file)
        continue

    OLD = "          ALPHA_VANTAGE_API_KEY: ${{ secrets.ALPHA_VANTAGE_API_KEY }}"
    NEW = (
        "          ALPHA_VANTAGE_API_KEY: ${{ secrets.ALPHA_VANTAGE_API_KEY }}\n"
        "          TWELVE_DATA_API_KEY: ${{ secrets.TWELVE_DATA_API_KEY }}"
    )
    if OLD in yml_content:
        yml_content = yml_content.replace(OLD, NEW)
        with open(yml_path, "w", encoding="utf-8") as f:
            f.write(yml_content)
        print("✅ TWELVE_DATA_API_KEY added to " + yml_file)
    else:
        print("⚠️  Could not find ALPHA_VANTAGE_API_KEY in " + yml_file)

print("\n✅ Script complete")
print("   Yahoo Finance: primary (free, no limit)")
print("   Twelve Data:   fallback (free, 800 calls/day)")
print("   Alpha Vantage: removed (25 calls/day too low)")
print("   BTC-USD and ETH-USD supported by both sources")
