import os

hubMap = {
    "brief": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "debate": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "comparison": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "scenarios": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "stocks": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "map": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "pillars": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "alerts": ("QS", "/", "← Quantum Strategist", "bg-blue-900 hover:bg-blue-700 border border-blue-700 text-blue-200"),
    "history": ("PI", "/researcher", "← Pattern Intelligence", "bg-green-900 hover:bg-green-700 border border-green-700 text-green-200"),
    "research": ("PI", "/researcher", "← Pattern Intelligence", "bg-green-900 hover:bg-green-700 border border-green-700 text-green-200"),
    "correlations": ("PI", "/researcher", "← Pattern Intelligence", "bg-green-900 hover:bg-green-700 border border-green-700 text-green-200"),
    "weekly-digest": ("PI", "/researcher", "← Pattern Intelligence", "bg-green-900 hover:bg-green-700 border border-green-700 text-green-200"),
    "methodology": ("PI", "/researcher", "← Pattern Intelligence", "bg-green-900 hover:bg-green-700 border border-green-700 text-green-200"),
    "developer": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "transparency": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "autonomy": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "health": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "security": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "source-health": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "adaptive-log": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "quota": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "mission-control": ("DC", "/developer-hub", "← Dev Console", "bg-purple-900 hover:bg-purple-700 border border-purple-700 text-purple-200"),
    "predictions": ("FL", "/reports", "← Feedback Loop", "bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200"),
    "validation-log": ("FL", "/reports", "← Feedback Loop", "bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200"),
    "model-learning": ("FL", "/reports", "← Feedback Loop", "bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200"),
    "pattern-library": ("FL", "/reports", "← Feedback Loop", "bg-amber-900 hover:bg-amber-700 border border-amber-700 text-amber-200"),
}

print(f"{'Page':<20} {'Hub':<4} {'HasCorrectBack':<16} {'HasCrossNav':<12} {'HasDashboard'}")
print("-" * 75)

for page, (hub, url, label, colors) in hubMap.items():
    path = f"src/app/{page}/page.tsx"
    if not os.path.exists(path):
        continue
    with open(path, "r", encoding="utf-8") as f:
        content = f.read()
    
    has_correct_back = label in content
    has_crossnav = "Cross-nav" in content or "Cross-Navigation" in content or "GNI-R-140" in content
    has_dashboard = "Dashboard" in content and ("larr" in content or "\u2190" in content)
    
    back_status = "YES" if has_correct_back else "NO -- MISSING/WRONG"
    print(f"{page:<20} {hub:<4} {back_status:<16} {str(has_crossnav):<12} {str(has_dashboard)}")