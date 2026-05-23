# ============================================================
# GNI Absence Detector — NN-PHI-5 Implementation
# "Absence is intelligence. What sources do not cover is
#  as important as what they do cover." — PHI-003
# Tracks keyword frequency history and flags coverage gaps.
# ============================================================
import os
from datetime import datetime, timezone, date, timedelta
from dotenv import load_dotenv
load_dotenv()

# Keywords that should never go silent — if they do, that is intelligence
ABSENCE_WATCH_KEYWORDS = [
    # Major geopolitical flashpoints
    "taiwan", "iran", "ukraine", "north korea", "south china sea",
    "hormuz", "strait of hormuz", "nuclear",
    # Critical supply chains
    "semiconductor", "chip", "rare earth", "critical minerals",
    # Security
    "cyberattack", "cyber attack", "critical infrastructure", "ransomware",
    # Economic
    "federal reserve", "oil price", "sanctions", "opec",
    # Humanitarian
    "humanitarian", "human rights", "war crime",
    # Strategic
    "nato", "security council", "united nations",
]

GAP_THRESHOLDS = {
    "CRITICAL": {"min_avg": 3.0, "max_today": 0},
    "HIGH":     {"min_avg": 5.0, "max_today": 1},
    "MODERATE": {"min_avg": 8.0, "max_today": 2},
}


def _get_client():
    try:
        from supabase import create_client
        url = os.getenv("SUPABASE_URL", "")
        key = os.getenv("SUPABASE_SERVICE_KEY", "")
        if not url or not key:
            return None
        return create_client(url, key)
    except Exception:
        return None


def count_keyword_occurrences(articles: list[dict]) -> dict[str, int]:
    """Count how many articles contain each watch keyword."""
    counts = {kw: 0 for kw in ABSENCE_WATCH_KEYWORDS}
    for art in articles:
        text = (art.get("title", "") + " " + art.get("summary", "")).lower()
        for kw in ABSENCE_WATCH_KEYWORDS:
            if kw in text:
                counts[kw] += 1
    return counts


def save_keyword_counts(counts: dict[str, int], run_date: date = None) -> bool:
    """Save today keyword counts to gni_keyword_history."""
    client = _get_client()
    if not client:
        return False
    today = run_date or date.today()
    try:
        records = [
            {"keyword": kw, "run_date": today.isoformat(), "article_count": count}
            for kw, count in counts.items()
        ]
        client.table("gni_keyword_history").upsert(records, on_conflict="keyword,run_date").execute()
        return True
    except Exception as e:
        print(f"  Warning: Could not save keyword history: {str(e)[:60]}")
        return False


def get_7day_averages(run_date: date = None) -> dict[str, float]:
    """Get 7-day rolling average article count per keyword."""
    client = _get_client()
    if not client:
        return {}
    today = run_date or date.today()
    seven_days_ago = (today - timedelta(days=7)).isoformat()
    try:
        result = client.table("gni_keyword_history") \
            .select("keyword,article_count") \
            .gte("run_date", seven_days_ago) \
            .lt("run_date", today.isoformat()) \
            .execute()
        rows = result.data or []
        totals = {}
        day_counts = {}
        for row in rows:
            kw = row["keyword"]
            totals[kw] = totals.get(kw, 0) + row["article_count"]
            day_counts[kw] = day_counts.get(kw, 0) + 1
        averages = {}
        for kw in ABSENCE_WATCH_KEYWORDS:
            days = day_counts.get(kw, 0)
            averages[kw] = round(totals.get(kw, 0) / days, 2) if days > 0 else 0.0
        return averages
    except Exception as e:
        print(f"  Warning: Could not fetch keyword history: {str(e)[:60]}")
        return {}


def detect_gaps(today_counts: dict[str, int], averages: dict[str, float]) -> list[dict]:
    """Compare today counts vs 7-day averages. Return list of coverage gaps."""
    gaps = []
    for kw in ABSENCE_WATCH_KEYWORDS:
        today = today_counts.get(kw, 0)
        avg = averages.get(kw, 0.0)
        if avg < 1.0:
            continue  # Not enough history yet — skip
        for severity, threshold in GAP_THRESHOLDS.items():
            if avg >= threshold["min_avg"] and today <= threshold["max_today"]:
                gaps.append({
                    "keyword": kw,
                    "today_count": today,
                    "avg_7day": avg,
                    "gap_severity": severity,
                    "alert_date": date.today().isoformat(),
                })
                break  # Only report highest severity per keyword
    gaps.sort(key=lambda g: ["CRITICAL","HIGH","MODERATE"].index(g["gap_severity"]))
    return gaps


def save_gaps(gaps: list[dict]) -> bool:
    """Save detected gaps to gni_coverage_alerts."""
    client = _get_client()
    if not client or not gaps:
        return False
    try:
        client.table("gni_coverage_alerts").insert(gaps).execute()
        return True
    except Exception as e:
        print(f"  Warning: Could not save coverage gaps: {str(e)[:60]}")
        return False


def run_absence_detection(articles: list[dict]) -> list[dict]:
    """
    Main entry point. Call after Stage 1 collection.
    Returns list of gap dicts for reporting.
    PHI-003 NN-PHI-5: surfaces what sources are NOT covering.
    """
    print("  NN-PHI-5: Running absence detection...")
    today_counts = count_keyword_occurrences(articles)
    averages = get_7day_averages()
    gaps = detect_gaps(today_counts, averages)
    save_keyword_counts(today_counts)
    if gaps:
        save_gaps(gaps)
        for g in gaps:
            print(f"  COVERAGE GAP [{g['gap_severity']}]: '{g['keyword']}' — "
                  f"today={g['today_count']} vs 7d_avg={g['avg_7day']}")
    else:
        if averages:
            print(f"  No coverage gaps detected ({len(today_counts)} keywords tracked)")
        else:
            print(f"  Building baseline — {len(today_counts)} keywords logged (7 runs needed)")
    return gaps
