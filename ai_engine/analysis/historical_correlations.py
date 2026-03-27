# ============================================================
# GNI Historical Correlation Engine v2
# Escalation patterns + Agent accuracy + Location + Pillar + CI
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


def _score_to_level(score: float) -> str:
    if score >= 9: return "CRITICAL"
    if score >= 7: return "HIGH"
    if score >= 5: return "ELEVATED"
    if score >= 3: return "MODERATE"
    return "LOW"


def build_correlation_table() -> dict:
    """
    Build escalation-level correlation table from prediction_outcomes.
    v2: adds agent accuracy, location, pillar, CI correlation.
    """
    client = _get_client()
    if not client:
        return {}

    try:
        outcomes = client.table("prediction_outcomes") \
            .select("report_id, spy_change_3d, spy_change_7d, direction_correct_3d, direction_correct_7d, accuracy_score") \
            .execute()

        if not outcomes.data:
            print("  Warning: No GPVS outcomes yet -- correlation table empty")
            return {}

        report_ids = [o["report_id"] for o in outcomes.data if o.get("report_id")]
        if not report_ids:
            return {}

        reports = client.table("reports") \
            .select("id, escalation_score, risk_level, mad_verdict, mad_confidence, "
                    "mad_black_swan_case, mad_ostrich_case, mad_bull_case, mad_bear_case, "
                    "location_name, sentiment, confidence_interval_width, "
                    "short_focus_threats, long_shoot_threats") \
            .in_("id", report_ids) \
            .execute()

        report_map = {r["id"]: r for r in (reports.data or [])}

        buckets = {
            "CRITICAL": {"spy_3d": [], "spy_7d": [], "correct_3d": [], "correct_7d": [], "scores": [],
                         "bull_correct": [], "bear_correct": [], "swan_correct": [], "ostrich_correct": [],
                         "narrow_ci": [], "wide_ci": []},
            "HIGH":     {"spy_3d": [], "spy_7d": [], "correct_3d": [], "correct_7d": [], "scores": [],
                         "bull_correct": [], "bear_correct": [], "swan_correct": [], "ostrich_correct": [],
                         "narrow_ci": [], "wide_ci": []},
            "ELEVATED": {"spy_3d": [], "spy_7d": [], "correct_3d": [], "correct_7d": [], "scores": [],
                         "bull_correct": [], "bear_correct": [], "swan_correct": [], "ostrich_correct": [],
                         "narrow_ci": [], "wide_ci": []},
            "MODERATE": {"spy_3d": [], "spy_7d": [], "correct_3d": [], "correct_7d": [], "scores": [],
                         "bull_correct": [], "bear_correct": [], "swan_correct": [], "ostrich_correct": [],
                         "narrow_ci": [], "wide_ci": []},
            "LOW":      {"spy_3d": [], "spy_7d": [], "correct_3d": [], "correct_7d": [], "scores": [],
                         "bull_correct": [], "bear_correct": [], "swan_correct": [], "ostrich_correct": [],
                         "narrow_ci": [], "wide_ci": []},
        }

        # Location and pillar pattern buckets
        location_patterns = {}
        pillar_map = {}

        pillar_buckets = {"geo": {"spy_3d": [], "correct_3d": []},
                          "fin": {"spy_3d": [], "correct_3d": []},
                          "tech": {"spy_3d": [], "correct_3d": []}}

        for outcome in outcomes.data:
            report_id = outcome.get("report_id")
            if not report_id or report_id not in report_map:
                continue

            report = report_map[report_id]
            esc_score = report.get("escalation_score", 0) or 0
            level = _score_to_level(esc_score)
            correct_3d = 1 if outcome.get("direction_correct_3d") else 0
            spy_3d = outcome.get("spy_change_3d")
            spy_7d = outcome.get("spy_change_7d")

            if spy_3d is not None: buckets[level]["spy_3d"].append(spy_3d)
            if spy_7d is not None: buckets[level]["spy_7d"].append(spy_7d)
            if outcome.get("direction_correct_3d") is not None:
                buckets[level]["correct_3d"].append(correct_3d)
            if outcome.get("direction_correct_7d") is not None:
                buckets[level]["correct_7d"].append(1 if outcome["direction_correct_7d"] else 0)
            buckets[level]["scores"].append(esc_score)

            # Agent accuracy -- which verdict was correct?
            verdict = report.get("mad_verdict", "")
            has_swan = bool(report.get("mad_black_swan_case"))
            has_ostrich = bool(report.get("mad_ostrich_case"))

            if verdict == "bearish" and correct_3d:
                buckets[level]["bear_correct"].append(1)
            elif verdict == "bullish" and correct_3d:
                buckets[level]["bull_correct"].append(1)
            elif verdict == "bearish":
                buckets[level]["bear_correct"].append(0)
            elif verdict == "bullish":
                buckets[level]["bull_correct"].append(0)

            if has_swan:
                buckets[level]["swan_correct"].append(correct_3d)
            if has_ostrich:
                buckets[level]["ostrich_correct"].append(correct_3d)

            # CI correlation
            ci_width = report.get("confidence_interval_width") or 0
            if ci_width > 0:
                if ci_width < 0.3:
                    buckets[level]["narrow_ci"].append(correct_3d)
                else:
                    buckets[level]["wide_ci"].append(correct_3d)

            # Location patterns
            location = report.get("location_name", "Global") or "Global"
            if location not in location_patterns:
                location_patterns[location] = {"spy_3d": [], "correct_3d": []}
            if spy_3d is not None:
                location_patterns[location]["spy_3d"].append(spy_3d)
            location_patterns[location]["correct_3d"].append(correct_3d)

            # Pillar patterns
            pillar = pillar_map.get(report_id, "geo").lower()
            if pillar in pillar_buckets:
                if spy_3d is not None:
                    pillar_buckets[pillar]["spy_3d"].append(spy_3d)
                pillar_buckets[pillar]["correct_3d"].append(correct_3d)

        # Build correlation summary
        correlations = {}
        for level, data in buckets.items():
            n = len(data["scores"])
            if n == 0:
                continue

            def avg(lst): return round(sum(lst) / len(lst), 3) if lst else None
            def pct(lst): return round(sum(lst) / len(lst) * 100, 1) if lst else None

            correlations[level] = {
                "avg_escalation_score": round(sum(data["scores"]) / n, 2),
                "avg_spy_3d": avg(data["spy_3d"]),
                "avg_spy_7d": avg(data["spy_7d"]),
                "accuracy_3d": pct(data["correct_3d"]),
                "accuracy_7d": pct(data["correct_7d"]),
                "bull_accuracy": pct(data["bull_correct"]),
                "bear_accuracy": pct(data["bear_correct"]),
                "swan_accuracy": pct(data["swan_correct"]),
                "ostrich_accuracy": pct(data["ostrich_correct"]),
                "narrow_ci_accuracy": pct(data["narrow_ci"]),
                "wide_ci_accuracy": pct(data["wide_ci"]),
                "sample_count": n,
            }

        # Save location and pillar patterns separately
        _save_patterns(client, location_patterns, pillar_buckets)

        return correlations

    except Exception as e:
        print(f"  Warning: Correlation build failed: {e}")
        return {}


def _save_patterns(client, location_patterns: dict, pillar_buckets: dict) -> None:
    """Save location and pillar patterns to correlation_patterns table."""
    try:
        now = datetime.now(timezone.utc).isoformat()
        records = []

        # Location patterns (min 3 samples)
        for location, data in location_patterns.items():
            n = len(data["correct_3d"])
            if n < 3:
                continue
            records.append({
                "pattern_type": "location",
                "pattern_key": location,
                "avg_spy_3d": round(sum(data["spy_3d"]) / len(data["spy_3d"]), 2) if data["spy_3d"] else None,
                "accuracy_3d": round(sum(data["correct_3d"]) / n * 100, 1),
                "sample_count": n,
                "last_updated": now,
            })

        # Pillar patterns
        for pillar, data in pillar_buckets.items():
            n = len(data["correct_3d"])
            if n < 3:
                continue
            records.append({
                "pattern_type": "pillar",
                "pattern_key": pillar.upper(),
                "avg_spy_3d": round(sum(data["spy_3d"]) / len(data["spy_3d"]), 2) if data["spy_3d"] else None,
                "accuracy_3d": round(sum(data["correct_3d"]) / n * 100, 1),
                "sample_count": n,
                "last_updated": now,
            })

        for record in records:
            client.table("correlation_patterns").upsert(record,
                on_conflict="pattern_type,pattern_key").execute()

        if records:
            print(f"  OK {len(records)} correlation patterns saved")

    except Exception as e:
        print(f"  Warning: Pattern save failed: {e}")


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
                "accuracy_3d": data.get("accuracy_3d"),
                "accuracy_7d": data.get("accuracy_7d"),
                "bull_accuracy": data.get("bull_accuracy"),
                "bear_accuracy": data.get("bear_accuracy"),
                "swan_accuracy": data.get("swan_accuracy"),
                "ostrich_accuracy": data.get("ostrich_accuracy"),
                "narrow_ci_accuracy": data.get("narrow_ci_accuracy"),
                "wide_ci_accuracy": data.get("wide_ci_accuracy"),
                "sample_count": data["sample_count"],
                "last_updated": now,
            }).execute()

        print(f"  OK Correlation table v2 saved -- {len(correlations)} levels")
        return True

    except Exception as e:
        print(f"  Warning: Correlation save failed: {e}")
        return False


def get_historical_context(escalation_score: float) -> str:
    """Get historical context string for a given escalation score."""
    client = _get_client()
    if not client:
        return ""

    try:
        level = _score_to_level(escalation_score)
        result = client.table("historical_correlations") \
            .select("*") \
            .eq("escalation_level", level) \
            .execute()

        if not result.data:
            return ""

        row = result.data[0]
        n = row.get("sample_count", 0)
        spy_3d = row.get("spy_change_3d")
        spy_7d = row.get("spy_change_7d")
        acc_3d = row.get("accuracy_3d")
        bear_acc = row.get("bear_accuracy")
        swan_acc = row.get("swan_accuracy")

        if not n or n < 3:
            return ""

        parts = [f"Historical pattern ({n} similar events):"]
        if spy_3d is not None:
            direction = "up" if spy_3d > 0 else "down"
            parts.append(f"SPY averaged {direction} {abs(spy_3d):.1f}% in 3 days")
        if spy_7d is not None:
            direction = "up" if spy_7d > 0 else "down"
            parts.append(f"and {direction} {abs(spy_7d):.1f}% in 7 days")
        if acc_3d is not None:
            parts.append(f"({acc_3d:.0f}% directional accuracy)")
        if swan_acc is not None and swan_acc > 0:
            parts.append(f"Black Swan agent accuracy: {swan_acc:.0f}%")

        return " ".join(parts)

    except Exception:
        return ""


def update_correlations() -> bool:
    """Full correlation update -- build and save."""
    print("  Building historical correlations v2...")
    correlations = build_correlation_table()
    if not correlations:
        print("  Warning: No correlation data available yet")
        return False
    return save_correlation_table(correlations)


def get_correlation_status() -> list:
    """Return correlation table for /health page."""
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("historical_correlations") \
            .select("*") \
            .order("avg_escalation_score", desc=True) \
            .execute()
        return result.data or []
    except Exception:
        return []


def get_pattern_status() -> list:
    """Return location and pillar patterns for /correlations page."""
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("correlation_patterns") \
            .select("*") \
            .order("sample_count", desc=True) \
            .execute()
        return result.data or []
    except Exception:
        return []


if __name__ == "__main__":
    print("GNI Historical Correlation Engine v2\n")
    update_correlations()
    status = get_correlation_status()
    if status:
        print(f"\n  {'Level':<12} {'N':>4} {'SPY3d':>7} {'Acc3d':>7} {'Bear%':>7} {'Swan%':>7}")
        print("  " + "-" * 55)
        for row in status:
            spy3 = f"{row['spy_change_3d']:+.1f}%" if row.get("spy_change_3d") is not None else "N/A"
            acc = f"{row['accuracy_3d']:.0f}%" if row.get("accuracy_3d") is not None else "N/A"
            bear = f"{row['bear_accuracy']:.0f}%" if row.get("bear_accuracy") is not None else "N/A"
            swan = f"{row['swan_accuracy']:.0f}%" if row.get("swan_accuracy") is not None else "N/A"
            print(f"  {row['escalation_level']:<12} {row['sample_count']:>4} {spy3:>7} {acc:>7} {bear:>7} {swan:>7}")
    patterns = get_pattern_status()
    if patterns:
        print(f"\n  Location/Pillar patterns: {len(patterns)}")
