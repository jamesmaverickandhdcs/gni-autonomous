# ============================================================
# GNI Autonomous Frequency Controller — Day 15
# Adjusts pipeline run frequency based on escalation level
# CRITICAL: run every 1h | HIGH: every 2h | ELEVATED: every 4h
# MODERATE: every 6h | LOW: every 12h
# ============================================================

import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# Escalation level -> recommended interval in hours
FREQUENCY_MAP = {
    'CRITICAL':  1.0,   # Run every 1 hour — maximum urgency
    'HIGH':      2.0,   # Run every 2 hours
    'ELEVATED':  4.0,   # Run every 4 hours
    'MODERATE':  6.0,   # Run every 6 hours
    'LOW':      12.0,   # Run every 12 hours — default
    'NONE':     12.0,   # Same as LOW
}

DEFAULT_INTERVAL_HOURS = 12.0


def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def get_recommended_interval(escalation_level: str, escalation_score: float = 0.0) -> float:
    """
    Get recommended pipeline run interval in hours based on escalation.
    Higher escalation = more frequent runs.
    """
    level = escalation_level.upper() if escalation_level else 'NONE'
    interval = FREQUENCY_MAP.get(level, DEFAULT_INTERVAL_HOURS)

    # Fine-tune within level based on score
    # e.g. escalation_score=9.8 within CRITICAL gets slightly more urgent than 9.0
    if level == 'CRITICAL' and escalation_score >= 9.5:
        interval = 0.5  # Every 30 minutes for extreme events
    elif level == 'HIGH' and escalation_score >= 8.5:
        interval = 1.5  # Every 90 minutes for upper-HIGH

    return interval


def should_run_now(escalation_level: str = 'LOW', escalation_score: float = 0.0) -> tuple[bool, str]:
    """
    Check if pipeline should run now based on last run time and escalation.
    Returns (should_run, reason).
    """
    client = _get_client()
    if not client:
        return True, "No Supabase connection — defaulting to run"

    try:
        # Get most recent successful pipeline run
        result = client.table("pipeline_runs")             .select("run_at, status")             .eq("status", "success")             .order("run_at", desc=True)             .limit(1)             .execute()

        if not result.data:
            return True, "No previous runs found — first run"

        last_run_at = result.data[0]["run_at"]
        last_run_dt = datetime.fromisoformat(last_run_at.replace('Z', '+00:00'))
        now = datetime.now(timezone.utc)
        hours_since_last = (now - last_run_dt).total_seconds() / 3600

        recommended = get_recommended_interval(escalation_level, escalation_score)

        if hours_since_last >= recommended:
            return True, f"Interval elapsed: {hours_since_last:.1f}h >= {recommended:.1f}h ({escalation_level})"
        else:
            remaining = recommended - hours_since_last
            return False, f"Too soon: {hours_since_last:.1f}h since last run, need {recommended:.1f}h ({escalation_level}), wait {remaining:.1f}h more"

    except Exception as e:
        return True, f"Check failed: {e} — defaulting to run"


def log_frequency_decision(
    escalation_score: float,
    escalation_level: str,
    recommended_interval: float,
    reason: str,
) -> bool:
    """Log frequency decision to Supabase."""
    client = _get_client()
    if not client:
        return False

    try:
        client.table("frequency_log").insert({
            "escalation_score": escalation_score,
            "escalation_level": escalation_level,
            "recommended_interval_hours": recommended_interval,
            "reason": reason,
        }).execute()
        return True
    except Exception as e:
        print(f"  ⚠️  Frequency log failed: {e}")
        return False


def get_current_frequency_status() -> dict:
    """Get current recommended frequency for health page."""
    client = _get_client()
    if not client:
        return {}

    try:
        # Get latest escalation from reports
        result = client.table("reports")             .select("escalation_score, escalation_level, created_at")             .order("created_at", desc=True)             .limit(1)             .execute()

        if not result.data:
            return {"level": "LOW", "interval_hours": 12.0, "status": "No data"}

        report = result.data[0]
        level = report.get("escalation_level", "LOW") or "LOW"
        score = report.get("escalation_score", 0.0) or 0.0
        interval = get_recommended_interval(level, score)

        should_run, reason = should_run_now(level, score)

        return {
            "level": level,
            "score": score,
            "interval_hours": interval,
            "should_run_now": should_run,
            "reason": reason,
            "last_report_at": report.get("created_at", ""),
        }

    except Exception as e:
        return {"error": str(e)}


if __name__ == "__main__":
    print("\u23f1  GNI Autonomous Frequency Controller — Status\n")

    # Show frequency map
    print("  Frequency Schedule:")
    for level, hours in FREQUENCY_MAP.items():
        mins = int(hours * 60)
        print(f"    {level:<12} every {hours:.0f}h ({mins} min)")

    print()
    status = get_current_frequency_status()
    if status:
        print(f"  Current Level:    {status.get('level', 'N/A')}")
        print(f"  Escalation Score: {status.get('score', 0):.1f}/10")
        print(f"  Recommended:      every {status.get('interval_hours', 12):.1f}h")
        print(f"  Should Run Now:   {status.get('should_run_now', True)}")
        print(f"  Reason:           {status.get('reason', '')}")
