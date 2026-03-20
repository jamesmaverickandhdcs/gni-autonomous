# ============================================================
# GNI Weekly Digest Generator — Day 13
# Aggregates 7 days of reports into weekly intelligence summary
# Runs every Sunday or on demand
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
        result = client.table("reports")             .select("id, title, summary, sentiment, risk_level, location_name, tickers_affected, quality_score, escalation_score, created_at, market_impact")             .gte("created_at", week_start)             .lte("created_at", week_end)             .order("created_at", desc=False)             .execute()

        return result.data or []

    except Exception as e:
        print(f"  ⚠️  Failed to fetch week reports: {e}")
        return []


def generate_digest_summary(reports: list[dict]) -> str:
    """Use Groq to generate a weekly digest summary."""
    if not GROQ_API_KEY or not reports:
        return _generate_fallback_summary(reports)

    try:
        import urllib.request
        import json

        report_lines = ""
        for i, r in enumerate(reports[:10], 1):
            report_lines += f"""
Report {i} ({r.get('created_at', '')[:10]}):
- Title: {r.get('title', '')[:80]}
- Sentiment: {r.get('sentiment', '')} | Risk: {r.get('risk_level', '')} | Quality: {r.get('quality_score', 0):.1f}/10
- Summary: {r.get('summary', '')[:200]}
"""

        prompt = f"""You are GNI — Global Nexus Insights. Summarize the following {len(reports)} intelligence reports from the past week into a concise weekly digest.

REPORTS:
{report_lines}

Write a 3-4 sentence weekly intelligence digest that:
1. Identifies the dominant geopolitical theme of the week
2. Explains the cumulative market impact
3. Notes any escalation or de-escalation trend
4. Gives a forward-looking sentence for the coming week

Use professional analytical language. No bullet points. Plain prose only."""

        payload = json.dumps({
            "model": GROQ_MODEL,
            "messages": [{"role": "user", "content": prompt}],
            "max_tokens": 300,
            "temperature": 0.4,
        }).encode("utf-8")

        req = urllib.request.Request(
            "https://api.groq.com/openai/v1/chat/completions",
            data=payload,
            headers={
                "Authorization": f"Bearer {GROQ_API_KEY}",
                "Content-Type": "application/json",
            }
        )

        with urllib.request.urlopen(req, timeout=30) as response:
            data = json.loads(response.read())

        return data["choices"][0]["message"]["content"].strip()

    except Exception as e:
        print(f"  ⚠️  Groq digest failed: {e}")
        return _generate_fallback_summary(reports)


def _generate_fallback_summary(reports: list[dict]) -> str:
    """Generate a rule-based summary without LLM."""
    if not reports:
        return "No reports this week."

    sentiments = [r.get("sentiment", "Neutral") for r in reports]
    sentiment_counts = Counter(sentiments)
    dominant_sentiment = sentiment_counts.most_common(1)[0][0]

    risk_levels = [r.get("risk_level", "Medium") for r in reports]
    risk_counts = Counter(risk_levels)
    dominant_risk = risk_counts.most_common(1)[0][0]

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
    print(f"  📅 Generating weekly digest (weeks_ago={weeks_ago})...")

    reports = fetch_week_reports(weeks_ago)
    if not reports:
        print(f"  ⚠️  No reports found for week {weeks_ago} weeks ago")
        return None

    print(f"  📊 Found {len(reports)} reports for this week")

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

    # Generate summary
    print("  🤖 Generating digest summary...")
    digest_summary = generate_digest_summary(reports)

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
    }

    # Save to Supabase
    client = _get_client()
    if client:
        try:
            client.table("weekly_digests").upsert(digest).execute()
            print(f"  ✅ Weekly digest saved ({week_start[:10]} to {week_end[:10]})")
        except Exception as e:
            print(f"  ⚠️  Failed to save digest: {e}")

    return digest


def should_generate_digest() -> bool:
    """Check if today is Sunday — auto-trigger weekly digest."""
    return datetime.now(timezone.utc).weekday() == 6  # 6 = Sunday


def get_latest_digest() -> dict | None:
    """Get the most recent weekly digest."""
    client = _get_client()
    if not client:
        return None
    try:
        result = client.table("weekly_digests")             .select("*")             .order("week_end", desc=True)             .limit(1)             .execute()
        return result.data[0] if result.data else None
    except Exception:
        return None


if __name__ == "__main__":
    print("\U0001f4c5 GNI Weekly Digest Generator\n")
    digest = generate_weekly_digest(weeks_ago=0)
    if digest:
        print(f"\n  Week: {digest['week_start']} to {digest['week_end']}")
        print(f"  Reports: {digest['report_count']}")
        print(f"  Sentiment: {digest['dominant_sentiment']}")
        print(f"  Risk: {digest['dominant_risk_level']}")
        print(f"  Quality: {digest['avg_quality_score']}/10")
        print(f"  Locations: {digest['top_locations']}")
        print(f"  Tickers: {digest['top_tickers']}")
        print(f"\n  Summary:\n  {digest['digest_summary']}")
