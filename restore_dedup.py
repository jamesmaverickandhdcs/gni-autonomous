"""
restore_dedup.py
Restores dedup window to 6 hours after test run confirmed.
"""
import py_compile

MAIN_PATH = r"C:\HDCS_Project\03\GNI_Autonomous\ai_engine\main.py"

with open(MAIN_PATH, "r", encoding="utf-8") as f:
    content = f.read()

OLD = "duplicate = check_recent_duplicate(top_articles, hours=0, overlap_threshold=0.7)  # TEMP: restored after test run"
NEW = "duplicate = check_recent_duplicate(top_articles, hours=6, overlap_threshold=0.7)"

if OLD in content:
    content = content.replace(OLD, NEW, 1)
    print("OK dedup window restored to 6 hours")
else:
    print("WARN temp line not found -- may already be restored")

with open(MAIN_PATH, "w", encoding="utf-8") as f:
    f.write(content)

try:
    py_compile.compile(MAIN_PATH, doraise=True)
    print("OK main.py syntax check passed")
except py_compile.PyCompileError as e:
    print(f"FAIL {e}")
    exit(1)

print("OK Done. Now: npm run build && git push")
