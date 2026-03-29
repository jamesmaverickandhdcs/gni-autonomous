import urllib.request, json

GNI = "https://gni-autonomous.vercel.app"

print("Test A: Wrong key + Origin header (simulates browser) -- should be 401")
try:
    req = urllib.request.Request(
        f"{GNI}/api/reports",
        headers={
            "X-GNI-Key": "WRONG_KEY",
            "Origin": "https://evil.com"
        }
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        print(f"Status: {r.status} -- FAIL")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")

print("\nTest B: Wrong key + no Origin (server-side) -- should be 401 after deploy")
try:
    req = urllib.request.Request(
        f"{GNI}/api/reports",
        headers={"X-GNI-Key": "WRONG_KEY"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        print(f"Status: {r.status} -- FAIL (old cache still active)")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")

print("\nTest C: No key + no Origin (server-side) -- should be 401")
try:
    with urllib.request.urlopen(
        urllib.request.Request(f"{GNI}/api/reports"),
        timeout=10
    ) as r:
        print(f"Status: {r.status} -- FAIL")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")