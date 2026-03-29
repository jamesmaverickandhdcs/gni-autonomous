import urllib.request, json

# Test directly with the key value from gni-myanmar env
# Read from .env.local
key = ""
try:
    with open(r"C:\HDCS_Project\03\gni-myanmar\.env.local", "r") as f:
        for line in f:
            line = line.strip()
            if line.startswith("NEXT_PUBLIC_GNI_API_KEY="):
                key = line.split("=", 1)[1].strip()
            if line.startswith("GNI_API_KEY="):
                key = line.split("=", 1)[1].strip()
                print(f"Found GNI_API_KEY in .env.local")
                break
except Exception as e:
    print(f"Read error: {e}")

print(f"Key found: '{key}'")
print(f"Key length: {len(key)}")

if key:
    # Test directly against GNI_Autonomous with this key
    GNI = "https://gni-autonomous.vercel.app"
    print(f"\n=== Direct test with this key ===")
    try:
        req = urllib.request.Request(f"{GNI}/api/reports",
            headers={"X-GNI-Key": key})
        with urllib.request.urlopen(req, timeout=10) as r:
            data = json.loads(r.read())
            print(f"Status: {r.status} | Reports: {len(data.get('reports',[]))} -- PASS")
    except urllib.error.HTTPError as e:
        body = e.read().decode()
        print(f"Status: {e.code} | Response: {body} -- FAIL")