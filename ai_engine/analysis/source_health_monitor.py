# ============================================================
# GNI Source Health Monitor — S21-5 Reserve Selection
# Tracks per-source article counts and detects RSS failures.
# When source down: sends 5 reserve choices to admin every 3h.
# Admin replies 1-5 via Telegram webhook → reserve activated.
# Before each alert: checks if reserve already activated.
# ============================================================

import os
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_ID  = os.getenv("TELEGRAM_ADMIN_ID", "") or os.getenv("TELEGRAM_CHAT_ID", "")

MIN_EXPECTED         = 3
ROLLING_WINDOW       = 7
ALERT_INTERVAL_HOURS = 3

# ── Reserve Sources Pool ─────────────────────────────────────
GEO_RESERVES = [
    {"name": "Global Voices",     "url": "https://globalvoices.org/feed/",                          "pillar": "geo", "bias": "Global South",   "democracy_score": 88},
    {"name": "The Independent",   "url": "https://www.independent.co.uk/news/world/rss",            "pillar": "geo", "bias": "Western Liberal", "democracy_score": 82},
    {"name": "Radio Free Europe", "url": "https://www.rferl.org/api/epiqq",                         "pillar": "geo", "bias": "Pro-Democracy",   "democracy_score": 85},
    {"name": "New York Times",    "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",  "pillar": "geo", "bias": "Western Liberal", "democracy_score": 81},
    {"name": "Washington Post",   "url": "https://feeds.washingtonpost.com/rss/world",              "pillar": "geo", "bias": "Western Liberal", "democracy_score": 79},
]

FIN_RESERVES = [
    {"name": "Wall Street Journal", "url": "https://feeds.a.dj.com/rss/RSSWorldNews.xml", "pillar": "fin", "bias": "Financial", "democracy_score": 76},
    {"name": "Newsweek",            "url": "https://www.newsweek.com/rss",                "pillar": "fin", "bias": "News",      "democracy_score": 68},
]

TECH_RESERVES = [
    {"name": "The Verge",    "url": "https://www.theverge.com/rss/index.xml", "pillar": "tech", "bias": "Technology",    "democracy_score": 63},
    {"name": "Dark Reading", "url": "https://www.darkreading.com/rss.xml",    "pillar": "tech", "bias": "Cybersecurity", "democracy_score": 75},
]

ALL_RESERVES = GEO_RESERVES + FIN_RESERVES + TECH_RESERVES


def _get_reserves_for_pillar(pillar: str) -> list:
    if pillar == "geo":  return GEO_RESERVES
    if pillar == "fin":  return FIN_RESERVES
    if pillar == "tech": return TECH_RESERVES
    return GEO_RESERVES


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


def _send_admin_message(message: str) -> bool:
    if not TELEGRAM_BOT_TOKEN or not TELEGRAM_ADMIN_ID:
        return False
    try:
        resp = requests.post(
            "https://api.telegram.org/bot" + TELEGRAM_BOT_TOKEN + "/sendMessage",
            json={"chat_id": TELEGRAM_ADMIN_ID, "text": message, "parse_mode": "HTML"},
            timeout=10,
        )
        return resp.status_code == 200
    except Exception as e:
        print("  Warning: Telegram send failed: " + str(e)[:60])
        return False


def _build_reserve_alert(source_name: str, pillar: str, avg: float, hours_down: float) -> str:
    reserves = _get_reserves_for_pillar(pillar)
    lines = [
        "\U0001f534 <b>[GNI RSS Alert] Source DOWN: " + source_name + "</b>",
        "Pillar: " + pillar.upper() + " | Was averaging: " + str(avg) + " articles",
    ]
    if hours_down > 3:
        lines.append("\u23f0 Down for: " + str(round(hours_down, 1)) + " hours")
    lines.append("")
    lines.append("Please choose a reserve source:")
    for i, r in enumerate(reserves, 1):
        lines.append(str(i) + "\ufe0f\u20e3 " + r["name"] + " (" + str(r["democracy_score"]) + "% democracy score)")
    lines.append("")
    lines.append("Reply with number <b>1-" + str(len(reserves)) + "</b> to activate.")
    lines.append("\u23f3 Next reminder in " + str(ALERT_INTERVAL_HOURS) + " hours if no reply.")
    return "\n".join(lines)


def _is_reserve_already_active(client, source_name: str) -> bool:
    """Check if webhook already activated a reserve — if yes skip alert."""
    try:
        result = client.table("source_reserves") \
            .select("status") \
            .eq("primary_source", source_name) \
            .eq("status", "active") \
            .limit(1) \
            .execute()
        return bool(result.data)
    except Exception:
        return False


def _should_send_alert(client, source_name: str) -> tuple:
    """
    Returns (should_alert: bool, hours_down: float)
    Order of checks:
    1. Reserve already active via webhook? → skip
    2. First detection? → alert immediately
    3. ALERT_INTERVAL_HOURS passed? → alert again
    """
    if _is_reserve_already_active(client, source_name):
        print("  Reserve already active for " + source_name + " — skipping alert")
        return False, 0.0

    try:
        result = client.table("source_reserves") \
            .select("id, status, last_alerted_at, created_at") \
            .eq("primary_source", source_name) \
            .in_("status", ["pending", "alerted"]) \
            .order("created_at", desc=True) \
            .limit(1) \
            .execute()

        now = datetime.now(timezone.utc)

        if not result.data:
            return True, 0.0

        record       = result.data[0]
        last_alerted = record.get("last_alerted_at")
        created_at   = record.get("created_at")

        try:
            created_dt = datetime.fromisoformat(created_at.replace("Z", "+00:00"))
            hours_down = (now - created_dt).total_seconds() / 3600
        except Exception:
            hours_down = 0.0

        if not last_alerted:
            return True, hours_down

        try:
            last_dt     = datetime.fromisoformat(last_alerted.replace("Z", "+00:00"))
            hours_since = (now - last_dt).total_seconds() / 3600
            if hours_since >= ALERT_INTERVAL_HOURS:
                return True, hours_down
        except Exception:
            return True, hours_down

        return False, hours_down

    except Exception as e:
        print("  Warning: Could not check alert status: " + str(e)[:60])
        return True, 0.0


def _upsert_reserve_record(client, source_name: str, pillar: str) -> None:
    try:
        existing = client.table("source_reserves") \
            .select("id, days_down") \
            .eq("primary_source", source_name) \
            .in_("status", ["pending", "alerted"]) \
            .limit(1) \
            .execute()

        now = datetime.now(timezone.utc).isoformat()

        if not existing.data:
            client.table("source_reserves").insert({
                "primary_source":  source_name,
                "reserve_source":  "pending_selection",
                "status":          "alerted",
                "last_alerted_at": now,
                "days_down":       0,
                "pillar":          pillar,
            }).execute()
        else:
            record_id = existing.data[0]["id"]
            days_down = existing.data[0].get("days_down", 0) or 0
            client.table("source_reserves").update({
                "status":          "alerted",
                "last_alerted_at": now,
                "days_down":       days_down,
            }).eq("id", record_id).execute()

    except Exception as e:
        print("  Warning: Could not upsert reserve record: " + str(e)[:60])


def save_source_counts(articles: list, sources: list) -> bool:
    client = _get_client()
    if not client:
        return False

    counts = {}
    for art in articles:
        src = art.get("source", "")
        counts[src] = counts.get(src, 0) + 1

    run_at  = datetime.now(timezone.utc).isoformat()
    records = []

    for source in sources:
        name  = source["name"]
        count = counts.get(name, 0)
        records.append({
            "run_at":        run_at,
            "source_name":   name,
            "pillar":        source.get("pillar", ""),
            "article_count": count,
            "status":        "ok" if count > 0 else "empty",
        })

    try:
        client.table("source_health").insert(records).execute()
        return True
    except Exception as e:
        print("  Warning: Could not save source health: " + str(e))
        return False


def detect_rss_failures(sources: list) -> list:
    client = _get_client()
    if not client:
        return []

    failed = []
    cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()

    for source in sources:
        name = source["name"]
        try:
            result = client.table("source_health") \
                .select("article_count, run_at") \
                .eq("source_name", name) \
                .gte("run_at", cutoff) \
                .order("run_at", desc=True) \
                .limit(ROLLING_WINDOW) \
                .execute()

            rows = result.data or []
            if len(rows) < 2:
                continue

            current    = rows[0]["article_count"]
            historical = [r["article_count"] for r in rows[1:]]
            avg        = sum(historical) / len(historical) if historical else 0

            if current == 0 and avg >= MIN_EXPECTED:
                failed.append({
                    "name":   name,
                    "pillar": source.get("pillar", "geo"),
                    "current": current,
                    "avg":    round(avg, 1),
                    "url":    source.get("url", ""),
                    "run_at": rows[0]["run_at"],
                })

        except Exception as e:
            print("  Warning: Health check failed for " + name + ": " + str(e))

    return failed


def alert_and_log_failures(failed_sources: list) -> None:
    if not failed_sources:
        return

    client = _get_client()

    for src in failed_sources:
        name   = src["name"]
        pillar = src["pillar"]
        avg    = src["avg"]
        url    = src["url"]

        print("  RSS FAILURE: " + name + " (" + pillar.upper() + ") -- was averaging " + str(avg))

        should_alert, hours_down = _should_send_alert(client, name)

        if should_alert:
            msg  = _build_reserve_alert(name, pillar, avg, hours_down)
            sent = _send_admin_message(msg)
            if sent:
                print("  Reserve choice alert sent to admin for: " + name)
                if client:
                    _upsert_reserve_record(client, name, pillar)
            else:
                print("  Warning: Could not send alert for: " + name)
        else:
            print("  Skipping alert for " + name + " (active or recently alerted)")

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
                        "bug_class":      "rss_feed_down",
                        "error_message":  name + " returned 0 articles. Was averaging " + str(avg) + ". URL: " + url,
                        "suggested_fix":  "Admin selecting reserve via Telegram webhook. Test " + url + " manually.",
                        "affected_file":  name,
                        "status":         "pending",
                        "admin_required": True,
                        "strike_count":   0,
                    }).execute()
            except Exception as e:
                print("  Warning: Could not log fix suggestion: " + str(e)[:60])


def get_active_reserves(client=None) -> dict:
    """Called from rss_collector to get active reserve sources."""
    if client is None:
        client = _get_client()
    if not client:
        return {}

    try:
        result = client.table("source_reserves") \
            .select("primary_source, reserve_source") \
            .eq("status", "active") \
            .execute()

        active = {}
        if result.data:
            for row in result.data:
                primary      = row["primary_source"]
                reserve_name = row["reserve_source"]
                for r in ALL_RESERVES:
                    if r["name"] == reserve_name:
                        active[primary] = r
                        break
        return active

    except Exception as e:
        print("  Warning: Could not fetch active reserves: " + str(e)[:60])
        return {}


def run_source_health_check(articles: list, sources: list) -> None:
    """Main entry point -- called from main.py after collection."""
    save_source_counts(articles, sources)
    failed = detect_rss_failures(sources)
    if failed:
        print("  " + str(len(failed)) + " RSS source(s) down -- checking reserve alerts")
        alert_and_log_failures(failed)
    else:
        print("  All " + str(len(sources)) + " sources healthy")
