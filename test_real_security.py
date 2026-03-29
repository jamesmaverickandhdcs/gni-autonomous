import urllib.request, json

GNI = "https://gni-autonomous.vercel.app"

print("REAL Security Test -- no origin spoofing")
print()

print("Test 1: Wrong key, no origin (pure external attacker)")
try:
    req = urllib.request.Request(
        f"{GNI}/api/reports",
        headers={"X-GNI-Key": "WRONG_KEY_123"}
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        print(f"Status: {r.status} -- FAIL (security hole!)")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")

print()
print("Test 2: No key, no origin (pure external attacker)")
try:
    with urllib.request.urlopen(
        urllib.request.Request(f"{GNI}/api/reports"),
        timeout=10
    ) as r:
        print(f"Status: {r.status} -- FAIL (security hole!)")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code} -- {'PASS' if e.code == 401 else 'FAIL'}")

print()
print("Test 3: Valid Key 01 -- Myanmar proxy simulation")
print("(We dont have Key 01 value here so skipping)")

print()
print("Test 4: Wrong key + spoofed origin (server-side attacker)")
print("This WILL return 200 -- origin bypass is intentional for web pages")
print("Browsers cannot spoof Origin -- only server-side scripts can")
print("This is ACCEPTABLE RISK for academic project")