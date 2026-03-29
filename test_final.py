import urllib.request, json

GNI = "https://gni-autonomous.vercel.app"
MYANMAR = "https://gni-myanmar.vercel.app"

print("=== GNI_Autonomous Tests ===")

print("\nTest 1: No key -- should be 401")
try:
    with urllib.request.urlopen(urllib.request.Request(f"{GNI}/api/reports"), timeout=10) as r:
        print(f"Status: {r.status} -- FAIL")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")

print("\nTest 2: Wrong key -- should be 401")
try:
    req = urllib.request.Request(f"{GNI}/api/reports", headers={"X-GNI-Key": "WRONG"})
    with urllib.request.urlopen(req, timeout=10) as r:
        print(f"Status: {r.status} -- FAIL")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")

print("\nTest 3: Web page (no key) -- should be 200")
try:
    with urllib.request.urlopen(f"{GNI}", timeout=10) as r:
        print(f"Status: {r.status} -- {'PASS' if r.status == 200 else 'FAIL'}")
except Exception as e:
    print(f"FAIL: {e}")

print("\n=== GNI_Myanmar Tests ===")

print("\nTest 4: Myanmar /api/reports -- should be 200 + reports")
try:
    with urllib.request.urlopen(f"{MYANMAR}/api/reports", timeout=15) as r:
        data = json.loads(r.read())
        reports = data.get("reports", [])
        print(f"Status: {r.status} | Reports: {len(reports)} -- {'PASS' if len(reports) > 0 else 'FAIL'}")
except Exception as e:
    print(f"FAIL: {e}")

print("\nTest 5: Myanmar /api/stocks -- should return price")
try:
    with urllib.request.urlopen(f"{MYANMAR}/api/stocks?ticker=SPY&range=7d", timeout=15) as r:
        data = json.loads(r.read())
        print(f"Status: {r.status} | Price: {data.get('price','N/A')} -- {'PASS' if data.get('price') else 'FAIL'}")
except Exception as e:
    print(f"FAIL: {e}")