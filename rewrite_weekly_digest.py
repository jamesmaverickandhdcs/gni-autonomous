"""
GNI Weekly Digest -- Full Clean Rewrite
Replaces mangled weekly_digest.py with correct pillar sections
GNI-R-037: Full file read done -- file was mangled by previous patches
GNI-R-062: py_compile check at end
Run from: C:\HDCS_Project\03\GNI_Autonomous
Usage: python rewrite_weekly_digest.py
"""

import os
import py_compile

file_path = os.path.join("ai_engine", "analysis", "weekly_digest.py")

content = '''\
# ============================================================
# GNI Weekly Digest Generator -- Day 13 (v2 -- Pillar Sections)
# Aggregates 7 days of reports into weekly intelligence summary
# Runs every Sunday or on demand
# GEO / TECH / FIN pillar summaries added March 24, 2026
# ============================================================

import os
from datetime import datetime, timezone, timedelta
from collections import Counter
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")


def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def _get_week_boundaries(weeks_ago: int = 0) -> tuple[str, str]:
    """Get ISO week start (Monday) and end (Sunday) dates."""
    today = datetime.now(timezone.utc)
    days_since_monday = today.weekday()
    monday = today - timedelta(days=days_since_monday + (weeks_ago * 7))
    monday = monday.replace(hour=0, minute=0, second=0, microsecond=0)
    sunday = monday + timedelta(days=6, hours=23, minutes=59, seconds=59)
    return monday.isoformat(), sunday.isoformat()


def fetch_week_reports(weeks_ago: int = 0) -> list[dict]:
    """Fetch all reports from the specified week."""
    client = _get_client()
    if not client:
        return []

    week_start, week_end = _get_week_boundaries(weeks_ago)

    try:
        result = client.table("reports") \\
            .select("id, title, summary, sentiment, risk_level, location_name, tickers_affected, quality_score, escalation_score, created_at, market_impact") \\
            .gte("created_at", week_start) \\
            .lte("created_at", week_end) \\
            .order("created_at", desc=False) \\
            .execute()
        return result.data or []
    except Exception as e:
        print(f"  Warning: Failed to fetch week reports: {e}")
        return []


def fetch_week_pillar_reports(weeks_ago: int = 0) -> list[dict]:
    """Fetch pillar reports from the specified week."""
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
    """Use Groq to generate a pillar-specific weekly summary."""
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


def generate_digest_summary(reports: list[dict]) -> str:
    """Use Groq to generate a weekly digest summary."""
    if not GROQ_API_KEY or not reports:
        return _generate_fallback_summary(reports)

    try:
        import requests as req_lib
        report_lines = ""
        for i, r in enumerate(reports[:10], 1):
            title = r.get("title", "")[:80].encode("ascii", "ignore").decode()
            summary = r.get("summary", "")[:200].encode("ascii", "ignore").decode()
            report_lines += (
                "Report " + str(i) + " (" + r.get("created_at", "")[:10] + "):\\n"
                "- Title: " + title + "\\n"
                "- Sentiment: " + r.get("sentiment", "") +
                " | Risk: " + r.get("risk_level", "") + "\\n"
                "- Summary: " + summary + "\\n"
            )

        prompt = (
            "You are a geopolitical intelligence analyst. "
            "Summarize these " + str(len(reports)) + " intelligence reports "
            "from the past week into a concise weekly digest.\\n\\n"
            "REPORTS:\\n" + report_lines + "\\n"
            "Write 3-4 sentences covering: "
            "(1) dominant geopolitical theme, "
            "(2) cumulative market impact, "
            "(3) escalation or de-escalation trend, "
            "(4) forward outlook for next week. "
            "Professional analytical prose only. No bullet points."
        )

        response = req_lib.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={"Authorization": "Bearer " + GROQ_API_KEY,
                     "Content-Type": "application/json"},
            json={"model": GROQ_MODEL,
                  "messages": [{"role": "user", "content": prompt}],
                  "max_tokens": 300, "temperature": 0.4},
            timeout=30,
        )

        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"].strip()
        else:
            print("  Warning: Groq digest HTTP " + str(response.status_code))
            return _generate_fallback_summary(reports)

    except Exception as e:
        print("  Warning: Groq digest error: " + str(e))
        return _generate_fallback_summary(reports)


def _generate_fallback_summary(reports: list[dict]) -> str:
    """Generate a rule-based summary without LLM."""
    if not reports:
        return "No reports this week."

    sentiments = [r.get("sentiment", "Neutral") for r in reports]
    dominant_sentiment = Counter(sentiments).most_common(1)[0][0]

    risk_levels = [r.get("risk_level", "Medium") for r in reports]
    dominant_risk = Counter(risk_levels).most_common(1)[0][0]

    avg_quality = sum(r.get("quality_score", 0) for r in reports) / len(reports)

    return (
        f"Weekly summary: {len(reports)} intelligence reports generated. "
        f"Dominant sentiment: {dominant_sentiment}. "
        f"Dominant risk level: {dominant_risk}. "
        f"Average quality score: {avg_quality:.1f}/10."
    )


def generate_weekly_digest(weeks_ago: int = 1) -> dict | None:
    """
    Generate and save weekly digest for the specified week.
    weeks_ago=0 = current week, weeks_ago=1 = last week
    """
    print(f"  \U0001f4c5 Generating weekly digest (weeks_ago={weeks_ago})...")

    # Fetch main reports
    reports = fetch_week_reports(weeks_ago)
    if not reports:
        print(f"  Warning: No reports found for week {weeks_ago} weeks ago")
        return None

    print(f"  \U0001f4ca Found {len(reports)} reports for this week")

    # Aggregate stats
    sentiments = [r.get("sentiment", "Neutral") for r in reports]
    dominant_sentiment = Counter(sentiments).most_common(1)[0][0]

    risk_levels = [r.get("risk_level", "Medium") for r in reports]
    dominant_risk = Counter(risk_levels).most_common(1)[0][0]

    locations = [r.get("location_name", "") for r in reports if r.get("location_name")]
    top_locations = [loc for loc, _ in Counter(locations).most_common(3)]

    all_tickers = []
    for r in reports:
        tickers = r.get("tickers_affected", []) or []
        all_tickers.extend(tickers)
    top_tickers = [t for t, _ in Counter(all_tickers).most_common(5)]

    avg_quality = round(sum(r.get("quality_score", 0) for r in reports) / len(reports), 2)

    # Generate main summary
    print("  \U0001f916 Generating digest summary...")
    digest_summary = generate_digest_summary(reports)

    # Fetch pillar reports for the week
    print("  \U0001f30d Fetching pillar reports...")
    pillar_reports_week = fetch_week_pillar_reports(weeks_ago)
    geo_reports  = [r for r in pillar_reports_week if r.get("pillar") == "geo"]
    tech_reports = [r for r in pillar_reports_week if r.get("pillar") == "tech"]
    fin_reports  = [r for r in pillar_reports_week if r.get("pillar") == "fin"]
    print(f"  Pillar reports: GEO={len(geo_reports)} TECH={len(tech_reports)} FIN={len(fin_reports)}")

    # Generate pillar summaries
    print("  \U0001f310 Generating GEO pillar summary...")
    geo_summary  = generate_pillar_summary("geo",  geo_reports)
    print("  \U0001f4bb Generating TECH pillar summary...")
    tech_summary = generate_pillar_summary("tech", tech_reports)
    print("  \U0001f4b0 Generating FIN pillar summary...")
    fin_summary  = generate_pillar_summary("fin",  fin_reports)

    week_start, week_end = _get_week_boundaries(weeks_ago)

    digest = {
        "week_start": week_start[:10],
        "week_end": week_end[:10],
        "report_count": len(reports),
        "avg_quality_score": avg_quality,
        "dominant_sentiment": dominant_sentiment,
        "dominant_risk_level": dominant_risk,
        "top_locations": top_locations,
        "top_tickers": top_tickers,
        "digest_summary": digest_summary,
        "geo_summary": geo_summary,
        "tech_summary": tech_summary,
        "fin_summary": fin_summary,
    }

    # Save to Supabase
    client = _get_client()
    if client:
        try:
            client.table("weekly_digests").upsert(digest).execute()
            print(f"  OK Weekly digest saved ({week_start[:10]} to {week_end[:10]})")
        except Exception as e:
            print(f"  Warning: Failed to save digest: {e}")

    return digest


def should_generate_digest() -> bool:
    """Check if today is Sunday -- auto-trigger weekly digest."""
    return datetime.now(timezone.utc).weekday() == 6  # 6 = Sunday


def get_latest_digest() -> dict | None:
    """Get the most recent weekly digest."""
    client = _get_client()
    if not client:
        return None
    try:
        result = client.table("weekly_digests") \\
            .select("*") \\
            .order("week_end", desc=True) \\
            .limit(1) \\
            .execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


if __name__ == "__main__":
    print("\U0001f4c5 GNI Weekly Digest Generator\\n")
    digest = generate_weekly_digest(weeks_ago=0)
    if digest:
        print(f"\\n  Week: {digest[\'week_start\']} to {digest[\'week_end\']}")
        print(f"  Reports: {digest[\'report_count\']}")
        print(f"  Sentiment: {digest[\'dominant_sentiment\']}")
        print(f"  Risk: {digest[\'dominant_risk_level\']}")
        print(f"  Quality: {digest[\'avg_quality_score\']}/10")
        print(f"  Locations: {digest[\'top_locations\']}")
        print(f"  Tickers: {digest[\'top_tickers\']}")
        print(f"\\n  Summary:\\n  {digest[\'digest_summary\']}")
        print(f"\\n  GEO:\\n  {digest.get(\'geo_summary\', \'N/A\')}")
        print(f"\\n  TECH:\\n  {digest.get(\'tech_summary\', \'N/A\')}")
        print(f"\\n  FIN:\\n  {digest.get(\'fin_summary\', \'N/A\')}")
'''

with open(file_path, "w", encoding="utf-8", newline="\n") as f:
    f.write(content)

print(f"OK Written: {file_path}")

# GNI-R-062: py_compile check
py_compile.compile(file_path, doraise=True)
print("OK py_compile: syntax OK")
print("DONE. Now run: npm run build")
