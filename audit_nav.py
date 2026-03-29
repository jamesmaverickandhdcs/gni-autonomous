import os
import glob

pages = [
    "brief","debate","comparison","scenarios","stocks","map","pillars","alerts",
    "history","research","correlations","weekly-digest","methodology",
    "developer","transparency","autonomy","health","security","source-health",
    "adaptive-log","quota","mission-control",
    "predictions","validation-log","model-learning","pattern-library"
]

for page in pages:
    path = f"src/app/{page}/page.tsx"
    if os.path.exists(path):
        with open(path, 'r', encoding='utf-8') as f:
            content = f.read()
        has_crossnav = 'Cross-nav' in content or 'Cross-Navigation' in content or 'GNI-R-140' in content
        has_dashboard = 'Dashboard' in content and ('larr' in content or '\u2190' in content)
        has_back_qs = '\u2190 Quantum Strategist' in content or '&larr; Quantum' in content
        has_back_pi = '\u2190 Pattern Intelligence' in content
        has_back_dc = '\u2190 Dev Console' in content
        has_back_fl = '\u2190 Feedback Loop' in content
        has_any_back = has_back_qs or has_back_pi or has_back_dc or has_back_fl
        print(f"{page:20} CrossNav:{str(has_crossnav):5} Dashboard:{str(has_dashboard):5} BackBtn:{str(has_any_back):5}")