# ============================================================
# GNI Historical Correlation Engine — Day 13
# Finds patterns between escalation levels and market outcomes
# Builds correlation table from historical GPVS data
# ============================================================

import os
from datetime import datetime, timezone
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")


def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def build_correlation_table() -> dict:
    """
    Build historical correlation table from prediction_outcomes.
    Groups by escalation_level and computes avg market movements.
    Returns dict of {level: {avg_spy_3d, avg_spy_7d, sample_count, accuracy}}
    """
    client = _get_client()
    if not client:
        return {}

    try:
        # Get outcomes joined with reports for escalation scores
        outcomes = client.table("prediction_outcomes")             .select("report_id, spy_change_3d, spy_change_7d, direction_correct_3d, direction_correct_7d, accuracy_score")             .execute()

        if not outcomes.data:
            print("  ⚠️  No GPVS outcomes yet — correlation table empty")
            return {}

        # Get escalation scores from reports
        report_ids = [o["report_id"] for o in outcomes.data if o.get("report_id")]
        if not report_ids:
            return {}

        reports = client.table("reports")             .select("id, escalation_score, risk_level")             .in_("id", report_ids)             .execute()

        report_map = {r["id"]: r for r in (reports.data or [])}

        # Group by escalation level
        buckets = {
            "CRITICAL": {"spy_3d": [], "spy_7d": [], "correct_3d": [], "scores": []},
            "HIGH":     {"spy_3d": [], "spy_7d": [], "correct_3d": [], "scores": []},
            "ELEVATED": {"spy_3d": [], "spy_7d": [], "correct_3d": [], "scores": []},
            "MODERATE": {"spy_3d": [], "spy_7d": [], "correct_3d": [], "scores": []},
            "LOW":      {"spy_3d": [], "spy_7d": [], "correct_3d": [], "scores": []},
        }

        for outcome in outcomes.data:
            report_id = outcome.get("report_id")
            if not report_id or report_id not in report_map:
                continue

            report = report_map[report_id]
            escalation_score = report.get("escalation_score", 0) or 0

            # Map score to level
            if escalation_score >= 9:
                level = "CRITICAL"
            elif escalation_score >= 7:
                level = "HIGH"
            elif escalation_score >= 5:
                level = "ELEVATED"
            elif escalation_score >= 3:
                level = "MODERATE"
            else:
                level = "LOW"

            if outcome.get("spy_change_3d") is not None:
                buckets[level]["spy_3d"].append(outcome["spy_change_3d"])
            if outcome.get("spy_change_7d") is not None:
                buckets[level]["spy_7d"].append(outcome["spy_change_7d"])
            if outcome.get("direction_correct_3d") is not None:
                buckets[level]["correct_3d"].append(1 if outcome["direction_correct_3d"] else 0)
            buckets[level]["scores"].append(escalation_score)

        # Build correlation summary
        correlations = {}
        for level, data in buckets.items():
            n = len(data["scores"])
            if n == 0:
                continue
            correlations[level] = {
                "avg_escalation_score": round(sum(data["scores"]) / n, 2),
                "avg_spy_3d": round(sum(data["spy_3d"]) / len(data["spy_3d"]), 2) if data["spy_3d"] else None,
                "avg_spy_7d": round(sum(data["spy_7d"]) / len(data["spy_7d"]), 2) if data["spy_7d"] else None,
                "accuracy_3d": round(sum(data["correct_3d"]) / len(data["correct_3d"]) * 100, 1) if data["correct_3d"] else None,
                "sample_count": n,
            }

        return correlations

    except Exception as e:
        print(f"  ⚠️  Correlation build failed: {e}")
        return {}


def save_correlation_table(correlations: dict) -> bool:
    """Save correlation table to Supabase historical_correlations."""
    client = _get_client()
    if not client:
        return False

    try:
        now = datetime.now(timezone.utc).isoformat()
        for level, data in correlations.items():
            client.table("historical_correlations").upsert({
                "escalation_level": level,
                "avg_escalation_score": data["avg_escalation_score"],
                "spy_change_3d": data.get("avg_spy_3d"),
                "spy_change_7d": data.get("avg_spy_7d"),
                "sample_count": data["sample_count"],
                "last_updated": now,
            }).execute()

        print(f"  ✅ Correlation table saved — {len(correlations)} levels")
        return True

    except Exception as e:
        print(f"  ⚠️  Correlation save failed: {e}")
        return False


def get_historical_context(escalation_score: float) -> str:
    """
    Get historical context string for a given escalation score.
    Used to enrich reports with pattern-based predictions.
    """
    client = _get_client()
    if not client:
        return ""

    try:
        # Map score to level
        if escalation_score >= 9:
            level = "CRITICAL"
        elif escalation_score >= 7:
            level = "HIGH"
        elif escalation_score >= 5:
            level = "ELEVATED"
        elif escalation_score >= 3:
            level = "MODERATE"
        else:
            level = "LOW"

        result = client.table("historical_correlations")             .select("*")             .eq("escalation_level", level)             .execute()

        if not result.data:
            return ""

        row = result.data[0]
        n = row.get("sample_count", 0)
        spy_3d = row.get("spy_change_3d")
        spy_7d = row.get("spy_change_7d")

        if not n or n < 3:
            return ""

        parts = [f"Historical pattern ({n} similar events):"]
        if spy_3d is not None:
            direction = "up" if spy_3d > 0 else "down"
            parts.append(f"SPY averaged {direction} {abs(spy_3d):.1f}% in 3 days")
        if spy_7d is not None:
            direction = "up" if spy_7d > 0 else "down"
            parts.append(f"and {direction} {abs(spy_7d):.1f}% in 7 days")

        return " ".join(parts)

    except Exception:
        return ""


def update_correlations() -> bool:
    """Full correlation update — build and save."""
    print("  📊 Building historical correlations...")
    correlations = build_correlation_table()
    if not correlations:
        print("  ⚠️  No correlation data available yet")
        return False
    return save_correlation_table(correlations)


def get_correlation_status() -> list:
    """Return correlation table for /health page."""
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("historical_correlations")             .select("*")             .order("avg_escalation_score", desc=True)             .execute()
        return result.data or []
    except Exception:
        return []


if __name__ == "__main__":
    print("\U0001f4ca GNI Historical Correlation Engine\n")
    update_correlations()
    status = get_correlation_status()
    if status:
        print(f"\n  {'Level':<12} {'Avg Score':>10} {'SPY 3d':>8} {'SPY 7d':>8} {'N':>5}")
        print("  " + "-" * 50)
        for row in status:
            spy3 = f"{row['spy_change_3d']:+.1f}%" if row.get("spy_change_3d") is not None else "N/A"
            spy7 = f"{row['spy_change_7d']:+.1f}%" if row.get("spy_change_7d") is not None else "N/A"
            print(f"  {row['escalation_level']:<12} {row['avg_escalation_score']:>10.2f} {spy3:>8} {spy7:>8} {row['sample_count']:>5}")
    else:
        print("  No correlation data yet — needs GPVS outcomes to accumulate")
