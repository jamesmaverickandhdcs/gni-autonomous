import urllib.request, json

# Test with valid Key 01 to confirm keys DO work
GNI = "https://gni-autonomous.vercel.app"

print("Test: Valid key -- should be 200")
try:
    # Try with a clearly invalid UUID format key
    req = urllib.request.Request(
        f"{GNI}/api/quota",
        headers={
            "X-GNI-Key": "WRONG_KEY_123",
            "Origin": "https://gni-autonomous.vercel.app"
        }
    )
    with urllib.request.urlopen(req, timeout=10) as r:
        data = json.loads(r.read())
        print(f"Status: {r.status}")
        print(f"Response keys: {list(data.keys())[:5]}")
except urllib.error.HTTPError as e:
    print(f"Status: {e.code}")
except Exception as e:
    print(f"Error: {e}")

print("\nTest: Check if GNI_API_KEYS might be empty")
print("If wrong key returns 200, VALID_KEYS array is likely empty on Vercel")
print("Fix: The condition should be: !VALID_KEYS.includes(key)")  
print("Not: VALID_KEYS.length > 0 && !VALID_KEYS.includes(key)")