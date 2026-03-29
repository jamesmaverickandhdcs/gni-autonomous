import urllib.request, json

MYANMAR = "https://gni-myanmar.vercel.app"

print("=== Raw response from Myanmar /api/reports ===")
try:
    with urllib.request.urlopen(f"{MYANMAR}/api/reports", timeout=15) as r:
        raw = r.read().decode("utf-8")
        print(f"Status: {r.status}")
        print(f"Raw response: {raw[:500]}")
except Exception as e:
    print(f"FAIL: {e}")

print("\n=== Raw response from Myanmar /api/stocks ===")
try:
    with urllib.request.urlopen(f"{MYANMAR}/api/stocks?ticker=SPY&range=7d", timeout=15) as r:
        raw = r.read().decode("utf-8")
        print(f"Status: {r.status}")
        print(f"Raw response: {raw[:500]}")
except Exception as e:
    print(f"FAIL: {e}")