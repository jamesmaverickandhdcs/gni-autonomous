import os
import shutil
import py_compile

# ── Files and folders to remove ─────────────────────────────
# 1. The keywords page folder
KEYWORDS_PAGE = os.path.join("src", "app", "keywords")

# 2. Any keywords API route (if exists)
KEYWORDS_API  = os.path.join("src", "app", "api", "emerging-keywords")

removed = []
not_found = []

# ── Remove keywords page ─────────────────────────────────────
if os.path.exists(KEYWORDS_PAGE):
    shutil.rmtree(KEYWORDS_PAGE)
    removed.append(KEYWORDS_PAGE)
    print(f"OK  Removed: {KEYWORDS_PAGE}")
else:
    not_found.append(KEYWORDS_PAGE)
    print(f"NOT FOUND (already removed?): {KEYWORDS_PAGE}")

# ── Remove keywords API route ────────────────────────────────
if os.path.exists(KEYWORDS_API):
    shutil.rmtree(KEYWORDS_API)
    removed.append(KEYWORDS_API)
    print(f"OK  Removed: {KEYWORDS_API}")
else:
    not_found.append(KEYWORDS_API)
    print(f"NOT FOUND (already removed?): {KEYWORDS_API}")

# ── Summary ──────────────────────────────────────────────────
print("")
print("=" * 50)
if removed:
    print(f"REMOVED {len(removed)} item(s):")
    for r in removed:
        print(f"  - {r}")
if not_found:
    print(f"NOT FOUND (skip): {len(not_found)} item(s)")
    for n in not_found:
        print(f"  - {n}")
print("")
print("Next steps:")
print("  1. npm run build")
print("  2. Check build passes")
print("  3. git add -A")
print('  4. git commit -m "remove keywords page -- keyword sensor disabled GNI-R-108"')
print("  5. git push")
print("=" * 50)
