"""
GNI Pillar Keyword Weights
Adds pillar-aware bonus scoring to _score_article() in intelligence_funnel.py
GEO: conflict/diplomacy/military | TECH: AI/cyber/chips | FIN: market/tariff/trade
GNI-R-037: Full file read before edit -- done
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_pillar_weights.py
"""

import os
import py_compile

file_path = os.path.join("ai_engine", "funnel", "intelligence_funnel.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

# Insert pillar bonus block just before the final return in _score_article()
# Target: the last two lines of _score_article()
old = '    reason_str = " | ".join(reasons) if reasons else "Base score only"\n    return round(score, 2), reason_str'

new = '''    # ── PILLAR-SPECIFIC BONUS SCORING (+2 each, max 10) ──────────────
    # Boosts articles that are highly relevant to their assigned pillar
    # so quota selection picks the best-fit article per pillar
    pillar = article.get("pillar", "").lower()

    if pillar == "geo":
        GEO_BONUS = [
            "ceasefire", "peace deal", "peace talks", "diplomatic",
            "ambassador", "state actor", "proxy war", "occupation",
            "territorial", "sovereignty", "humanitarian crisis",
            "civilian", "refugee", "displacement", "airstrike",
            "ground offensive", "siege", "blockade", "military operation",
            "nato", "alliance", "security council", "united nations",
            "coup", "revolution", "protest", "uprising", "civil war",
        ]
        geo_matches = [kw for kw in GEO_BONUS if kw in text]
        geo_score = min(len(geo_matches) * 2, 10)
        score += geo_score
        if geo_matches:
            reasons.append(f"GEO pillar bonus ({geo_score}pts): {', '.join(geo_matches[:3])}")

    elif pillar == "tech":
        TECH_BONUS = [
            "artificial intelligence", "machine learning", "deep learning",
            "large language model", "generative ai", "ai regulation",
            "semiconductor", "chip", "nvidia", "tsmc", "intel",
            "export control", "chip ban", "advanced chips",
            "cyberattack", "ransomware", "zero day", "vulnerability",
            "cyber espionage", "state sponsored hacking", "critical infrastructure",
            "digital sovereignty", "internet shutdown", "surveillance",
            "facial recognition", "quantum computing", "5g", "6g",
            "tech regulation", "data privacy", "platform monopoly",
        ]
        tech_matches = [kw for kw in TECH_BONUS if kw in text]
        tech_score = min(len(tech_matches) * 2, 10)
        score += tech_score
        if tech_matches:
            reasons.append(f"TECH pillar bonus ({tech_score}pts): {', '.join(tech_matches[:3])}")

    elif pillar == "fin":
        FIN_BONUS = [
            "stock market", "equity", "bond", "yield", "interest rate",
            "federal reserve", "central bank", "monetary policy",
            "inflation", "deflation", "recession", "gdp growth",
            "tariff", "trade war", "trade deal", "import duty",
            "sanction", "asset freeze", "swift", "currency",
            "dollar", "yuan", "euro", "exchange rate",
            "oil price", "energy market", "opec", "crude",
            "capital flow", "foreign investment", "fdi",
            "sovereign debt", "bond yield", "credit rating",
            "commodity", "gold", "copper", "lithium price",
        ]
        fin_matches = [kw for kw in FIN_BONUS if kw in text]
        fin_score = min(len(fin_matches) * 2, 10)
        score += fin_score
        if fin_matches:
            reasons.append(f"FIN pillar bonus ({fin_score}pts): {', '.join(fin_matches[:3])}")

    reason_str = " | ".join(reasons) if reasons else "Base score only"
    return round(score, 2), reason_str'''

if old in content:
    content = content.replace(old, new)
    with open(file_path, "w", encoding="utf-8", newline="\n") as f:
        f.write(content)
    print(f"OK Updated: {file_path}")
    print("  + GEO bonus: 29 conflict/diplomacy/military keywords")
    print("  + TECH bonus: 30 AI/cyber/semiconductor keywords")
    print("  + FIN bonus: 35 market/tariff/capital flow keywords")
else:
    print("ERROR: Target block not found -- file may have changed. Do not proceed.")
    exit(1)

# GNI-R-062: py_compile check on modified file
py_compile.compile(file_path, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
