"""
GNI Weekly Digest Pillar Sections
Adds geo_summary, tech_summary, fin_summary to weekly_digest.py
GNI-R-037: Full file read done
GNI-R-008: ALTER TABLE ran first -- confirmed
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python add_digest_pillars.py
"""

import os
import py_compile

file_path = os.path.join("ai_engine", "analysis", "weekly_digest.py")

with open(file_path, "r", encoding="utf-8") as f:
    content = f.read()

fixes = 0

# Fix 1: Add fetch_week_pillar_reports function after fetch_week_reports()
old1 = "def generate_digest_summary(reports: list[dict]) -> str:"
new1 = """def fetch_week_pillar_reports(weeks_ago: int = 0) -> list[dict]:
    \"\"\"Fetch pillar reports from the specified week, grouped by pillar.\"\"\"
    client = _get_client()
    if not client:
        return []

    week_start, week_end = _get_week_boundaries(weeks_ago)

    try:
        result = client.table("pillar_reports") \\
            .select("id, pillar, title, summary, sentiment, risk_level, tickers_affected, quality_score, created_at") \\
            .gte("created_at", week_start) \\
            .lte("created_at", week_end) \\
            .order("created_at", desc=False) \\
            .execute()
        return result.data or []
    except Exception as e:
        print(f"  Warning: Failed to fetch pillar reports: {e}")
        return []


def generate_pillar_summary(pillar: str, reports: list[dict]) -> str:
    \"\"\"Use Groq to generate a pillar-specific weekly summary.\"\"\"
    if not reports:
        return f"No {pillar.upper()} pillar reports this week."

    if not GROQ_API_KEY:
        sentiments = [r.get("sentiment", "Neutral") for r in reports]
        dominant = Counter(sentiments).most_common(1)[0][0]
        return f"{pillar.upper()} pillar: {len(reports)} reports. Dominant sentiment: {dominant}."

    pillar_focus = {
        "geo": "conflict, diplomacy, military operations, state actors, humanitarian",
        "tech": "AI, cybersecurity, semiconductors, digital sovereignty, surveillance",
        "fin": "markets, capital flows, sanctions, tariffs, energy economics",
    }.get(pillar, "geopolitical intelligence")

    try:
        import requests as req_lib
        report_lines = ""
        for i, r in enumerate(reports[:5], 1):
            title = r.get("title", "")[:80].encode("ascii", "ignore").decode()
            summary = r.get("summary", "")[:150].encode("ascii", "ignore").decode()
            report_lines += (
                "Report " + str(i) + " (" + r.get("created_at", "")[:10] + "):\\n"
                "- Title: " + title + "\\n"
                "- Sentiment: " + r.get("sentiment", "") +
                " | Risk: " + r.get("risk_level", "") + "\\n"
                "- Summary: " + summary + "\\n"
            )

        prompt = (
            "You are a geopolitical intelligence analyst specialising in " + pillar_focus + ". "
            "Summarize these " + str(len(reports)) + " " + pillar.upper() + " pillar reports "
            "from the past week into 2-3 sentences covering: "
            "(1) dominant theme, (2) key risk or opportunity, (3) outlook. "
            "Professional analytical prose only. No bullet points.\\n\\n"
            "REPORTS:\\n" + report_lines
        )

        response = req_lib.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + GROQ_API_KEY,
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 200, "temperature": 0.4},
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print("  Warning: Groq pillar digest HTTP " + str(response.status_code))
            return f"{pillar.upper()} pillar: {len(reports)} reports this week."

    except Exception as e:
        print("  Warning: Groq pillar digest error: " + str(e))
        return f"{pillar.upper()} pillar: {len(reports)} reports this week."


def generate_digest_summary(reports: list[dict]) -> str:"""

if old1 in content:
    content = content.replace(old1, new1)
    fixes += 1
    print("OK Fix 1: Added fetch_week_pillar_reports() and generate_pillar_summary()")

# Fix 2: Add pillar fetching and summaries inside generate_weekly_digest()
old2 = '    # Generate summary\n    print("  \\U0001f916 Generating digest summary...")\n    digest_summary = generate_digest_summary(reports)'
new2 = '    # Fetch pillar reports for the week\n    print("  \\U0001f30d Fetching pillar reports...")\n    pillar_reports = fetch_week_pillar_reports(weeks_ago)\n    geo_reports  = [r for r in pillar_reports if r.get("pillar") == "geo"]\n    tech_reports = [r for r in pillar_reports if r.get("pillar") == "tech"]\n    fin_reports  = [r for r in pillar_reports if r.get("pillar") == "fin"]\n    print(f"  Pillar reports: GEO={len(geo_reports)} TECH={len(tech_reports)} FIN={len(fin_reports)}")\n\n    # Generate summary\n    print("  \\U0001f916 Generating digest summary...")\n    digest_summary = generate_digest_summary(reports)'

if old2 in content:
    content = content.replace(old2, new2)
    fixes += 1
    print("OK Fix 2: Added pillar report fetching inside generate_weekly_digest()")

# Fix 3: Add pillar summaries generation after digest_summary
old3 = '    week_start, week_end = _get_week_boundaries(weeks_ago)'
new3 = '    # Generate pillar summaries\n    print("  \\U0001f1ec\\U0001f1ea Generating GEO pillar summary...")\n    geo_summary  = generate_pillar_summary("geo",  geo_reports)\n    print("  \\U0001f4bb Generating TECH pillar summary...")\n    tech_summary = generate_pillar_summary("tech", tech_reports)\n    print("  \\U0001f4b0 Generating FIN pillar summary...")\n    fin_summary  = generate_pillar_summary("fin",  fin_reports)\n\n    week_start, week_end = _get_week_boundaries(weeks_ago)'

if old3 in content:
    content = content.replace(old3, new3)
    fixes += 1
    print("OK Fix 3: Added pillar summary generation calls")

# Fix 4: Add pillar fields to digest dict
old4 = '        "digest_summary": digest_summary,\n    }'
new4 = '        "digest_summary": digest_summary,\n        "geo_summary": geo_summary,\n        "tech_summary": tech_summary,\n        "fin_summary": fin_summary,\n    }'

if old4 in content:
    content = content.replace(old4, new4)
    fixes += 1
    print("OK Fix 4: Added geo/tech/fin_summary to digest dict")

# Fix 5: Print pillar summaries in __main__ block
old5 = '        print(f"\\n  Summary:\\n  {digest[\'digest_summary\']}")'
new5 = '        print(f"\\n  Summary:\\n  {digest[\'digest_summary\']}")\n        print(f"\\n  GEO:\\n  {digest.get(\'geo_summary\', \'N/A\')}")\n        print(f"\\n  TECH:\\n  {digest.get(\'tech_summary\', \'N/A\')}")\n        print(f"\\n  FIN:\\n  {digest.get(\'fin_summary\', \'N/A\')}")'

if old5 in content:
    content = content.replace(old5, new5)
    fixes += 1
    print("OK Fix 5: Added pillar summary output in __main__ block")

if fixes == 0:
    print("ERROR: No target blocks found -- file may have changed.")
    exit(1)

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"OK Updated: {file_path} ({fixes} fixes applied)")

# GNI-R-062: py_compile check on modified file
py_compile.compile(file_path, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
