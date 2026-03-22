# ============================================================
# GNI Source Health Monitor
# Tracks per-source article counts and detects RSS failures.
# Alerts admin via Telegram when a source goes down.
# ============================================================

import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_CHAT_ID = os.getenv("TELEGRAM_ADMIN_CHAT_ID", "") or os.getenv("TELEGRAM_CHAT_ID", "")

# Minimum expected articles -- sources below this after being healthy are flagged
MIN_EXPECTED = 3
# Number of recent runs to calculate rolling average
ROLLING_WINDOW = 7


def _get_client():
    from supabase import create_client
    url = os.getenv("SUPABASE_URL", "")
    key = os.getenv("SUPABASE_SERVICE_KEY", "")
    if not url or not key:
        return None
    try:
        return create_client(url, key)
    except Exception:
        return None


def _send_admin_alert(message: str):
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_ADMIN_CHAT_ID:
        return
    try:
        requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_ADMIN_CHAT_ID, "text": message},
            timeout=10,
        )
    except Exception:
        pass


def save_source_counts(articles: list, sources: list) -> bool:
    """
    Save per-source article counts to source_health table.
    Called after every collection run.
    articles: list of collected article dicts
    sources: list of source dicts from rss_collector.SOURCES
    """
    client = _get_client()
    if not client:
        return False

    # Count articles per source
    counts = {}
    for art in articles:
        src = art.get("source", "")
        counts[src] = counts.get(src, 0) + 1

    run_at = datetime.now(timezone.utc).isoformat()
    records = []

    for source in sources:
        name = source["name"]
        count = counts.get(name, 0)
        records.append({
            "run_at": run_at,
            "source_name": name,
            "pillar": source.get("pillar", ""),
            "article_count": count,
            "status": "ok" if count > 0 else "empty",
        })

    try:
        client.table("source_health").insert(records).execute()
        return True
    except Exception as e:
        print("  Warning: Could not save source health: " + str(e))
        return False


def detect_rss_failures(sources: list) -> list:
    """
    Compare current source counts vs rolling average.
    Returns list of failed sources that need alerting.
    """
    client = _get_client()
    if not client:
        return []

    failed = []
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    for source in sources:
        name = source["name"]
        try:
            # Get last ROLLING_WINDOW records for this source
            result = client.table("source_health") \
                .select("article_count, run_at, alert_sent") \
                .eq("source_name", name) \
                .gte("run_at", cutoff) \
                .order("run_at", desc=True) \
                .limit(ROLLING_WINDOW) \
                .execute()

            rows = result.data or []
            if len(rows) < 2:
                continue  # Not enough history

            # Current count is the most recent row
            current = rows[0]["article_count"]
            # Rolling average excludes the current row
            historical = [r["article_count"] for r in rows[1:]]
            avg = sum(historical) / len(historical) if historical else 0

            # Check if alert already sent today
            already_alerted = rows[0].get("alert_sent", False)

            # Flag if: currently 0, was healthy (avg > MIN_EXPECTED), not alerted today
            if current == 0 and avg >= MIN_EXPECTED and not already_alerted:
                failed.append({
                    "name": name,
                    "pillar": source.get("pillar", ""),
                    "current": current,
                    "avg": round(avg, 1),
                    "url": source.get("url", ""),
                    "run_at": rows[0]["run_at"],
                })

        except Exception as e:
            print("  Warning: Health check failed for " + name + ": " + str(e))

    return failed


def alert_and_log_failures(failed_sources: list) -> None:
    """
    Send Telegram alerts and log fix suggestions for failed sources.
    """
    if not failed_sources:
        return

    client = _get_client()

    for src in failed_sources:
        name = src["name"]
        pillar = src["pillar"].upper()
        avg = src["avg"]
        url = src["url"]

        print("  RSS FAILURE detected: " + name + " (" + pillar + ") -- was averaging " + str(avg) + " articles")

        # Send Telegram alert to admin
        msg = (
            "[GNI RSS Alert] Source down: " + name + "\n"
            "Pillar: " + pillar + "\n"
            "Articles this run: 0 (was averaging " + str(avg) + ")\n"
            "URL: " + url + "\n"
            "Action: test RSS feed manually and update URL if changed."
        )
        _send_admin_alert(msg)

        # Log fix suggestion
        if client:
            try:
                existing = client.table("code_fix_suggestions") \
                    .select("id") \
                    .eq("bug_class", "rss_feed_down") \
                    .eq("affected_file", name) \
                    .eq("status", "pending") \
                    .execute()
                if not existing.data:
                    client.table("code_fix_suggestions").insert({
                        "bug_class": "rss_feed_down",
                        "error_message": name + " returned 0 articles. Was averaging " + str(avg) + ". URL: " + url,
                        "suggested_fix": "Test " + url + " manually. Check if RSS URL has changed. Run test_rss_sources.py to verify.",
                        "affected_file": name,
                        "status": "pending",
                        "admin_required": False,
                        "strike_count": 0,
                    }).execute()
            except Exception as e:
                print("  Warning: Could not log RSS fix suggestion: " + str(e))

        # Mark alert as sent
        if client:
            try:
                client.table("source_health") \
                    .update({"alert_sent": True}) \
                    .eq("source_name", name) \
                    .eq("run_at", src["run_at"]) \
                    .execute()
            except Exception:
                pass


def run_source_health_check(articles: list, sources: list) -> None:
    """
    Main entry point -- called from main.py after collection.
    Saves counts then checks for failures.
    """
    save_source_counts(articles, sources)
    failed = detect_rss_failures(sources)
    if failed:
        print("  " + str(len(failed)) + " RSS source(s) down -- alerting admin")
        alert_and_log_failures(failed)
    else:
        print("  All " + str(len(sources)) + " sources healthy")
