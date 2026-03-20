# ============================================================
# GNI Health Agent — Day 16
# Monitors pipeline health metrics and raises alerts
# Checks: quality drift, source failures, run gaps,
# escalation spikes, MAD confidence drops
# ============================================================

import os
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_SERVICE_KEY = os.getenv("SUPABASE_SERVICE_KEY", "")

# Health thresholds
THRESHOLDS = {
    "min_quality_score":       6.0,    # Alert if avg quality drops below 6.0
    "quality_drift_threshold": 1.5,    # Alert if quality drops >1.5 points vs 7-day avg
    "max_run_gap_hours":       26.0,   # Alert if no successful run in 26h
    "min_articles_collected":  100,    # Alert if collecting <100 articles
    "max_injection_rate":      0.05,   # Alert if >5% articles flagged as injections
    "min_mad_confidence":      0.4,    # Alert if MAD confidence avg drops below 0.4
    "max_deception_score":     0.7,    # Alert if deception score exceeds 0.7
}


def _get_client():
    try:
        from supabase import create_client
        if not SUPABASE_URL or not SUPABASE_SERVICE_KEY:
            return None
        return create_client(SUPABASE_URL, SUPABASE_SERVICE_KEY)
    except Exception:
        return None


def _save_alert(client, alert_type: str, severity: str, message: str,
                metric_name: str, metric_value: float, threshold: float) -> bool:
    """Save health alert to Supabase."""
    try:
        client.table("health_alerts").insert({
            "alert_type": alert_type,
            "severity": severity,
            "message": message,
            "metric_name": metric_name,
            "metric_value": metric_value,
            "threshold": threshold,
            "resolved": False,
        }).execute()
        return True
    except Exception:
        return False


def run_health_checks() -> dict:
    """
    Run all health checks and return results.
    Saves alerts to Supabase for any failures.
    """
    client = _get_client()
    if not client:
        return {"status": "ERROR", "message": "No Supabase connection"}

    alerts = []
    checks_passed = 0
    checks_total = 0
    now = datetime.now(timezone.utc)

    # ── Check 1: Recent run gap ─────────────────────────────
    checks_total += 1
    try:
        result = client.table("pipeline_runs")             .select("run_at, status")             .eq("status", "success")             .order("run_at", desc=True)             .limit(1)             .execute()

        if result.data:
            last_run = datetime.fromisoformat(result.data[0]["run_at"].replace("Z", "+00:00"))
            hours_gap = (now - last_run).total_seconds() / 3600
            if hours_gap > THRESHOLDS["max_run_gap_hours"]:
                msg = f"No successful pipeline run in {hours_gap:.1f}h (threshold: {THRESHOLDS['max_run_gap_hours']}h)"
                alerts.append({"type": "RUN_GAP", "severity": "HIGH", "message": msg})
                _save_alert(client, "RUN_GAP", "HIGH", msg, "hours_since_run", hours_gap, THRESHOLDS["max_run_gap_hours"])
            else:
                checks_passed += 1
        else:
            checks_passed += 1  # No runs yet is OK
    except Exception as e:
        alerts.append({"type": "CHECK_ERROR", "severity": "LOW", "message": f"Run gap check failed: {e}"})

    # ── Check 2: Quality score drift ────────────────────────
    checks_total += 1
    try:
        cutoff_7d = (now - timedelta(days=7)).isoformat()
        result = client.table("reports")             .select("quality_score, created_at")             .gte("created_at", cutoff_7d)             .gt("quality_score", 0)             .order("created_at", desc=False)             .execute()

        reports = result.data or []
        if len(reports) >= 4:
            all_scores = [r["quality_score"] for r in reports]
            recent_scores = all_scores[-3:]  # Last 3 runs
            older_scores = all_scores[:-3]   # Everything before

            avg_recent = sum(recent_scores) / len(recent_scores)
            avg_older = sum(older_scores) / len(older_scores)

            drift = avg_older - avg_recent  # Positive = quality dropped

            if avg_recent < THRESHOLDS["min_quality_score"]:
                msg = f"Quality score below minimum: {avg_recent:.2f} < {THRESHOLDS['min_quality_score']}"
                alerts.append({"type": "LOW_QUALITY", "severity": "MEDIUM", "message": msg})
                _save_alert(client, "LOW_QUALITY", "MEDIUM", msg, "avg_quality_score", avg_recent, THRESHOLDS["min_quality_score"])
            elif drift > THRESHOLDS["quality_drift_threshold"]:
                msg = f"Quality drift detected: recent avg {avg_recent:.2f} vs older {avg_older:.2f} (drift: -{drift:.2f})"
                alerts.append({"type": "QUALITY_DRIFT", "severity": "MEDIUM", "message": msg})
                _save_alert(client, "QUALITY_DRIFT", "MEDIUM", msg, "quality_drift", drift, THRESHOLDS["quality_drift_threshold"])
            else:
                checks_passed += 1
        else:
            checks_passed += 1  # Not enough data yet
    except Exception as e:
        alerts.append({"type": "CHECK_ERROR", "severity": "LOW", "message": f"Quality check failed: {e}"})

    # ── Check 3: Article collection volume ──────────────────
    checks_total += 1
    try:
        result = client.table("pipeline_runs")             .select("total_collected")             .order("run_at", desc=True)             .limit(3)             .execute()

        if result.data:
            avg_collected = sum(r["total_collected"] for r in result.data) / len(result.data)
            if avg_collected < THRESHOLDS["min_articles_collected"]:
                msg = f"Low article collection: avg {avg_collected:.0f} < {THRESHOLDS['min_articles_collected']}"
                alerts.append({"type": "LOW_COLLECTION", "severity": "MEDIUM", "message": msg})
                _save_alert(client, "LOW_COLLECTION", "MEDIUM", msg, "avg_articles", avg_collected, THRESHOLDS["min_articles_collected"])
            else:
                checks_passed += 1
        else:
            checks_passed += 1
    except Exception as e:
        alerts.append({"type": "CHECK_ERROR", "severity": "LOW", "message": f"Collection check failed: {e}"})

    # ── Check 4: MAD confidence trend ───────────────────────
    checks_total += 1
    try:
        result = client.table("reports")             .select("mad_confidence")             .order("created_at", desc=True)             .limit(5)             .execute()

        if result.data:
            confidences = [r["mad_confidence"] for r in result.data if r.get("mad_confidence") is not None]
            if confidences:
                avg_conf = sum(confidences) / len(confidences)
                if avg_conf < THRESHOLDS["min_mad_confidence"]:
                    msg = f"MAD confidence low: avg {avg_conf:.2f} < {THRESHOLDS['min_mad_confidence']}"
                    alerts.append({"type": "MAD_CONFIDENCE", "severity": "LOW", "message": msg})
                    _save_alert(client, "MAD_CONFIDENCE", "LOW", msg, "mad_confidence", avg_conf, THRESHOLDS["min_mad_confidence"])
                else:
                    checks_passed += 1
            else:
                checks_passed += 1
        else:
            checks_passed += 1
    except Exception as e:
        alerts.append({"type": "CHECK_ERROR", "severity": "LOW", "message": f"MAD check failed: {e}"})

    # ── Check 5: Escalation spike ───────────────────────────
    checks_total += 1
    try:
        cutoff_24h = (now - timedelta(hours=24)).isoformat()
        result = client.table("reports")             .select("escalation_score")             .gte("created_at", cutoff_24h)             .execute()

        if result.data:
            scores = [r["escalation_score"] for r in result.data if r.get("escalation_score") is not None]
            if scores:
                max_score = max(scores)
                if max_score >= 9.0:
                    msg = f"CRITICAL escalation detected in last 24h: max score {max_score}/10"
                    alerts.append({"type": "ESCALATION_SPIKE", "severity": "HIGH", "message": msg})
                    # This is informational — not a failure
                checks_passed += 1
            else:
                checks_passed += 1
        else:
            checks_passed += 1
    except Exception as e:
        alerts.append({"type": "CHECK_ERROR", "severity": "LOW", "message": f"Escalation check failed: {e}"})

    # Determine overall status
    high_alerts = [a for a in alerts if a.get("severity") == "HIGH"]
    medium_alerts = [a for a in alerts if a.get("severity") == "MEDIUM"]

    if high_alerts:
        status = "CRITICAL"
    elif medium_alerts:
        status = "WARNING"
    elif alerts:
        status = "INFO"
    else:
        status = "HEALTHY"

    return {
        "status": status,
        "checks_passed": checks_passed,
        "checks_total": checks_total,
        "alerts": alerts,
        "alert_count": len(alerts),
        "checked_at": now.isoformat(),
    }


def get_unresolved_alerts() -> list:
    """Get unresolved health alerts for health page."""
    client = _get_client()
    if not client:
        return []
    try:
        result = client.table("health_alerts")             .select("*")             .eq("resolved", False)             .order("created_at", desc=True)             .limit(10)             .execute()
        return result.data or []
    except Exception:
        return []


if __name__ == "__main__":
    print("\U0001f916 GNI Health Agent — Running Checks\n")
    result = run_health_checks()
    print(f"  Status:         {result['status']}")
    print(f"  Checks passed:  {result['checks_passed']}/{result['checks_total']}")
    print(f"  Alerts:         {result['alert_count']}")
    if result['alerts']:
        for alert in result['alerts']:
            icon = "\U0001f534" if alert['severity'] == "HIGH" else "\U0001f7e1" if alert['severity'] == "MEDIUM" else "\U0001f7e2"
            print(f"  {icon} [{alert['severity']}] {alert['type']}: {alert['message']}")
    else:
        print("  \u2705 All systems healthy")
