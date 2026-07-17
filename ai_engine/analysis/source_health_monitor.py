# ============================================================
# GNI Source Health Monitor — S21-5 Reserve Selection
# Tracks per-source article counts and detects RSS failures.
# When source down: sends 5 reserve choices to admin every 3h.
# Admin replies 1-5 via Telegram webhook → reserve activated.
# Before each alert: checks if reserve already activated.
# ============================================================

import os
import html
import requests
from datetime import datetime, timezone, timedelta
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN", "")
TELEGRAM_ADMIN_ID  = os.getenv("TELEGRAM_ADMIN_ID", "") or os.getenv("TELEGRAM_QSChannel_ID", "")

MIN_EXPECTED         = 3
ROLLING_WINDOW       = 7
ALERT_INTERVAL_HOURS = 3

# ── S45 arc A: fetch-health vs yield ─────────────────────────
# A source is DOWN on FETCH health, not post-gate YIELD. The 3-tier freshness
# gate (S44) is a legitimate downstream filter -- a slow opinion source that
# fetches fine but yields 0 survivors is HEALTHY, not down. We measure:
#   fetch_ok -- transport returned a parseable feed (HTTP 200, >=1 entry)
#   raw      -- real candidate entries delivered (post chrome-guard, PRE
#               dedup/freshness). The honest up/down signal.
# DOWN iff: fetch_ok == False (any tier, immediate)
#        OR raw == 0 for a NEWS-tier feed (a fresh wire feed with 0 real
#           entries is genuinely broken)
#        OR raw == 0 sustained >= RAW_ZERO_PATIENCE_HOURS for a slow tier
#           (review/opinion can be legitimately quiet for one run; only a
#           SUSTAINED zero -- time-spanned, not run-counted -- is "down").
# DRY-RUN: detection runs and logs WOULD-alert verdicts but sends nothing and
# writes no reserve/fix rows until proven on live data (LR-105). Flip to False
# only after James sees the dry-run proof.
HEALTH_ALERT_DRY_RUN    = False
RAW_ZERO_PATIENCE_HOURS = 72.0          # slow tiers: zero must persist this long
IMMEDIATE_ZERO_TIERS    = {"news"}      # raw==0 flags on the spot for these

# S63 C3: timed auto-activation. 0 = DISABLED (default). Set the env var to
# e.g. 8 to auto-activate the top reserve after 8h of unanswered DOWN.
# James gates this per-deployment -- autonomy is opt-in, never default.
AUTO_RESERVE_AFTER_HOURS = float(os.getenv("GNI_AUTO_RESERVE_AFTER_HOURS", "0"))
# S63 C4: after a reserve serves cleanly this many days, send a PROPOSAL
# (never an action) to promote it or revive the primary.
PROMOTION_PROPOSAL_DAYS  = 7.0

# ── Reserve Sources Pool ─────────────────────────────────────
GEO_RESERVES = [
    # ORDER IS LOAD-BEARING (R-S63-1): reply-numbers resolve by position.
    # Must match src/app/api/telegram-webhook/route.ts EXACTLY, same order.
    {"name": "The Independent",  "url": "https://www.independent.co.uk/news/world/rss",                    "pillar": "geo", "bias": "Western Liberal",       "democracy_score": 82},
    {"name": "New York Times",   "url": "https://rss.nytimes.com/services/xml/rss/nyt/World.xml",          "pillar": "geo", "bias": "Western Liberal",       "democracy_score": 81},
    {"name": "Washington Post",  "url": "https://feeds.washingtonpost.com/rss/world",                      "pillar": "geo", "bias": "Western Liberal",       "democracy_score": 79},
    {"name": "The Diplomat",     "url": "https://thediplomat.com/feed/",                                   "pillar": "geo", "bias": "Asia-Pacific Analysis", "democracy_score": 84},
    {"name": "Defense News",     "url": "https://www.defensenews.com/arc/outboundfeeds/rss/",              "pillar": "geo", "bias": "US Defense",            "democracy_score": 78},
    # Africa-specific reserves -- for Africa Is A Country (The Africa Report cut S44 PHI-001)
    {"name": "AllAfrica",        "url": "https://allafrica.com/tools/headlines/rdf/latest/headlines.rdf",  "pillar": "geo", "bias": "Pan-African",           "democracy_score": 74},
    {"name": "ReliefWeb",        "url": "https://reliefweb.int/updates/rss.xml",                           "pillar": "geo", "bias": "Humanitarian",          "democracy_score": 90},
]

FIN_RESERVES = [
    # ORDER IS LOAD-BEARING (R-S63-1): must match route.ts exactly.
    {"name": "Newsweek",         "url": "https://www.newsweek.com/rss",                                    "pillar": "fin", "bias": "News",              "democracy_score": 68},
    {"name": "MarketWatch",      "url": "https://feeds.content.dowjones.io/public/rss/mw_topstories",      "pillar": "fin", "bias": "Financial",         "democracy_score": 74},
    {"name": "Investing.com News","url": "https://www.investing.com/rss/news.rss",                         "pillar": "fin", "bias": "Financial Markets", "democracy_score": 70},
]

TECH_RESERVES = [
    # ORDER IS LOAD-BEARING (R-S63-1): must match route.ts exactly.
    {"name": "The Verge",              "url": "https://www.theverge.com/rss/index.xml",       "pillar": "tech", "bias": "Technology",          "democracy_score": 63},
    {"name": "Dark Reading",           "url": "https://www.darkreading.com/rss.xml",          "pillar": "tech", "bias": "Cybersecurity",       "democracy_score": 75},
    {"name": "MIT Technology Review",  "url": "https://www.technologyreview.com/feed/",       "pillar": "tech", "bias": "Technology Research", "democracy_score": 80},
    {"name": "TechCrunch",             "url": "https://techcrunch.com/feed/",                 "pillar": "tech", "bias": "Tech Industry",       "democracy_score": 65},
    # The Register requires Commit 1 (RESERVE_FETCH_HEADERS) -- WAF-blocked on bare parse.
    {"name": "The Register",           "url": "https://www.theregister.com/headlines.atom",   "pillar": "tech", "bias": "Tech Independent",    "democracy_score": 72},
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
        if resp.status_code != 200:
            print("  Warning: Telegram send HTTP " + str(resp.status_code)
                  + ": " + resp.text[:100])
            return False
        return True
    except Exception as e:
        print("  Warning: Telegram send failed: " + str(e)[:60])
        return False


def _build_reserve_alert(source_name: str, pillar: str, avg: float,
                         hours_down: float, reason: str = "",
                         failing_reserve: str = "", escalation: bool = False) -> str:
    reserves = _get_reserves_for_pillar(pillar)
    header = ("\U0001f6a8 <b>[GNI RSS Alert] RESERVE ALSO DOWN: " + source_name
              + " (reserve: " + failing_reserve + ")</b>") if escalation else \
             ("\U0001f534 <b>[GNI RSS Alert] Source DOWN: " + source_name + "</b>")
    lines = [
        header,
        "Pillar: " + pillar.upper() + " | Avg raw entries: " + str(avg),
    ]
    if reason:
        lines.append("Why: " + html.escape(reason))
    if hours_down > 3:
        lines.append("\u23f0 Down for: " + str(round(hours_down, 1)) + " hours")
    lines.append("")
    lines.append("Please choose a reserve source:")
    for i, r in enumerate(reserves, 1):
        # S63 C5 guard: annotate, NEVER remove -- webhook maps reply-number to
        # list POSITION, so filtering would silently activate the wrong source.
        note = ""
        if r["name"] == source_name:
            note = " \u26a0\ufe0f (self -- do not pick)"
        elif failing_reserve and r["name"] == failing_reserve:
            note = " \u26a0\ufe0f (currently failing)"
        lines.append(str(i) + "\ufe0f\u20e3 " + r["name"] + " ("
                     + str(r["democracy_score"]) + "% democracy score)" + note)
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


def raw_val_guard(stat: dict, count: int) -> bool:
    """FT-GAP write-time warn condition: transport+entries OK, gate ate all."""
    return (stat.get("raw") or 0) > 0 and count == 0

def save_source_counts(articles: list, sources: list, source_stats: dict = None) -> bool:
    client = _get_client()
    if not client:
        return False

    source_stats = source_stats or {}

    counts = {}       # total articles per source (post-gate YIELD)
    geo_counts = {}   # geopolitically relevant articles per source (stage1_passed)
    for art in articles:
        src = art.get("source", "")
        counts[src] = counts.get(src, 0) + 1
        if art.get("stage1_passed", False):
            geo_counts[src] = geo_counts.get(src, 0) + 1

    run_at  = datetime.now(timezone.utc).isoformat()
    records = []

    for source in sources:
        name  = source["name"]
        count = counts.get(name, 0)            # YIELD (survivors) -- dashboard field
        stat  = source_stats.get(name, {})
        fetch_ok  = stat.get("fetch_ok")
        served_by = None
        if stat.get("is_reserve"):
            try:
                served_by = _get_active_reserve_name(client, name) or None
            except Exception:
                served_by = None
        if fetch_ok and raw_val_guard(stat, count):
            print("  WARNING [STALE-GATED] " + name + ": raw="
                  + str(stat.get("raw")) + " yield=0 -- gate ate all entries (FT-GAP)")
        raw   = stat.get("raw", count)         # RAW fetch health (pre-gate); fall
                                               # back to yield if stats absent
        records.append({
            "run_at":        run_at,
            "source_name":   name,
            "pillar":        source.get("pillar", ""),
            "article_count": count,
            "raw_count":     raw,
            "geo_count": geo_counts.get(name, 0),
            "geo_ratio": round(geo_counts.get(name, 0) / count, 2) if count > 0 else 0.0,
            "low_quality_flag": (count > 5 and (geo_counts.get(name, 0) / count) < 0.25),
            "fetch_ok":      fetch_ok,
            "served_by":     served_by,
            "status":        "ok" if count > 0 else "empty",
        })

    try:
        client.table("source_health").insert(records).execute()
        return True
    except Exception as e:
        # Migration-safe: raw_count column may not exist yet. Retry without it
        # so health history keeps saving until the ALTER TABLE lands.
        if "raw_count" in str(e):
            for r in records:
                r.pop("raw_count", None)
            try:
                client.table("source_health").insert(records).execute()
                print("  Note: source_health.raw_count column missing -- saved "
                      "without it. Run: ALTER TABLE source_health ADD COLUMN raw_count int;")
                return True
            except Exception as e2:
                print("  Warning: Could not save source health: " + str(e2))
                return False
        print("  Warning: Could not save source health: " + str(e))
        return False


def _health_verdict(tier: str, fetch_ok: bool, raw: int,
                    zero_streak_hours: float,
                    patience_hours: float = RAW_ZERO_PATIENCE_HOURS) -> tuple:
    """Pure DOWN/UP decision for one source. Returns (is_down, reason).
    No I/O -- deterministically testable (W2). Yield is intentionally NOT an
    input: a slow source that fetches fine but yields 0 is HEALTHY (S45 arc A)."""
    if not fetch_ok:
        return True, "fetch-down"
    if raw > 0:
        return False, "healthy (raw=" + str(raw) + ")"
    # raw == 0 and transport OK below:
    if tier in IMMEDIATE_ZERO_TIERS:
        return True, "raw==0 (news tier, immediate)"
    if zero_streak_hours >= patience_hours:
        return True, ("raw==0 sustained " + format(zero_streak_hours, ".0f")
                      + "h (>= " + format(patience_hours, ".0f") + "h, slow tier)")
    return False, ("raw==0 quiet " + format(zero_streak_hours, ".0f")
                   + "h (< " + format(patience_hours, ".0f") + "h patience, slow tier)")


def _raw_zero_streak_hours(client, source_name: str) -> float:
    """How long (hours) raw_count has been CONTINUOUSLY 0 across saved
    source_health rows -- time-spanned, not run-counted (S45 arc A, James).
    Returns 0.0 if the most recent run delivered raw>0, or if raw_count history
    is unavailable (column missing / pre-migration) -- both => 'do not flag'."""
    if client is None:
        return 0.0
    try:
        cutoff = (datetime.now(timezone.utc)
                  - timedelta(hours=RAW_ZERO_PATIENCE_HOURS * 2)).isoformat()
        result = client.table("source_health") \
            .select("raw_count, run_at") \
            .eq("source_name", source_name) \
            .gte("run_at", cutoff) \
            .order("run_at", desc=True) \
            .limit(ROLLING_WINDOW * 4) \
            .execute()
        rows = result.data or []
        newest_zero_dt = None
        oldest_zero_dt = None
        for r in rows:
            rc = r.get("raw_count")
            if rc is None or rc > 0:       # unknown or delivered -> streak ends
                break
            try:
                dt = datetime.fromisoformat(str(r["run_at"]).replace("Z", "+00:00"))
            except Exception:
                break
            if newest_zero_dt is None:
                newest_zero_dt = dt
            oldest_zero_dt = dt
        if newest_zero_dt is None or oldest_zero_dt is None:
            return 0.0
        return (newest_zero_dt - oldest_zero_dt).total_seconds() / 3600.0
    except Exception:
        return 0.0


def _avg_raw(client, source_name: str) -> float:
    """Rolling avg of raw_count (informational, for the alert text). The old
    article_count (yield) average is obsolete under the enforcing gate."""
    if client is None:
        return 0.0
    try:
        cutoff = (datetime.now(timezone.utc) - timedelta(days=7)).isoformat()
        result = client.table("source_health") \
            .select("raw_count, run_at") \
            .eq("source_name", source_name) \
            .gte("run_at", cutoff) \
            .order("run_at", desc=True) \
            .limit(ROLLING_WINDOW) \
            .execute()
        vals = [r["raw_count"] for r in (result.data or []) if r.get("raw_count") is not None]
        return round(sum(vals) / len(vals), 1) if vals else 0.0
    except Exception:
        return 0.0


def detect_rss_failures(sources: list, source_stats: dict = None) -> list:
    """Detect DOWN sources on FETCH health (not post-gate yield). Requires the
    per-source fetch stats emitted by collect_articles (S45 arc A)."""
    client = _get_client()
    source_stats = source_stats or {}

    failed = []
    healthy_quiet = []   # fetched fine, low/zero yield or under-patience -> NOT down

    for source in sources:
        name = source["name"]
        tier = source.get("tier", "news")
        stat = source_stats.get(name)

        if stat is None:
            # No fetch stat for this slot (e.g. called without arc-A stats).
            # Be conservative: cannot judge fetch health -> do not flag.
            continue

        fetch_ok = bool(stat.get("fetch_ok", False))
        raw      = int(stat.get("raw", 0))

        zero_streak = 0.0
        if fetch_ok and raw == 0 and tier not in IMMEDIATE_ZERO_TIERS:
            zero_streak = _raw_zero_streak_hours(client, name)

        is_down, reason = _health_verdict(tier, fetch_ok, raw, zero_streak)

        if not is_down:
            if stat.get("yield", 0) == 0:
                healthy_quiet.append(name + "[" + tier + ",raw=" + str(raw) + "]")
            continue

        # alert-facing reason -- include HTTP/parse detail for a fetch-down
        full_reason = reason
        if not fetch_ok:
            full_reason = reason + ": " + str(stat.get("reason", ""))[:90]

        failed.append({
            "name":    name,
            "pillar":  source.get("pillar", "geo"),
            "tier":    tier,
            "current": stat.get("yield", 0),
            "raw":     raw,
            "avg":     _avg_raw(client, name),
            "reason":  full_reason,
            "url":     source.get("url", ""),
            "run_at":  datetime.now(timezone.utc).isoformat(),
        })

    # Surface slow-but-healthy sources so the dry-run proves they do NOT flag
    # (PHI-002: never auto-drop slow deep sources just for publishing slowly).
    if healthy_quiet:
        print("  Healthy (fetched, low/zero yield -- NOT down): " + ", ".join(healthy_quiet))

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
        reason = src.get("reason", "")

        print("  RSS FAILURE: " + name + " (" + pillar.upper() + ") -- " + reason
              + " | avg raw " + str(avg))

        if HEALTH_ALERT_DRY_RUN:
            print("  [HEALTH dry-run] WOULD alert DOWN: " + name + " (" + reason
                  + ") -- no Telegram / no reserve / no fix-row written")
            continue

        # S63 C1: a DOWN verdict while a reserve is ACTIVE means the reserve
        # itself is failing. The old flow skipped alerting entirely here --
        # a slot could die silently forever. Escalate instead.
        active_res = _get_active_reserve_name(client, name)
        if active_res:
            _escalate_reserve_down(client, src, active_res)
            continue

        should_alert, hours_down = _should_send_alert(client, name)

        # S63 C3 (flag-gated, default OFF): unanswered DOWN past the window
        # -> auto-activate the top non-self reserve, announce loudly.
        if (AUTO_RESERVE_AFTER_HOURS > 0
                and hours_down >= AUTO_RESERVE_AFTER_HOURS
                and _auto_activate_reserve(client, src, hours_down)):
            continue

        if should_alert:
            msg  = _build_reserve_alert(name, pillar, avg, hours_down, reason)
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
                        "error_message":  name + " fetch-health DOWN: " + reason + ". Avg raw " + str(avg) + ". URL: " + url,
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


def run_source_health_check(articles: list, sources: list, source_stats: dict = None) -> None:
    """Main entry point -- called from main.py after collection.
    source_stats (S45 arc A) carries per-source fetch health from the collector;
    health is judged on fetch success, not post-gate yield."""
    save_source_counts(articles, sources, source_stats)
    reserve_lifecycle(sources, source_stats)   # S63 C2 recovery + C4 proposals
    failed = detect_rss_failures(sources, source_stats)
    if failed:
        mode = " [DRY-RUN]" if HEALTH_ALERT_DRY_RUN else ""
        print("  " + str(len(failed)) + " RSS source(s) DOWN (fetch-based)" + mode
              + " -- checking reserve alerts")
        alert_and_log_failures(failed)
    else:
        print("  All " + str(len(sources)) + " sources healthy (fetch-based)")


# ============================================================
# S63 C1-C4 -- reserve lifecycle helpers
# ============================================================

def _get_active_reserve_name(client, primary: str) -> str:
    """Name of the ACTIVE reserve for this primary slot, or '' if none."""
    if client is None:
        return ""
    try:
        r = client.table("source_reserves") \
            .select("reserve_source") \
            .eq("primary_source", primary) \
            .eq("status", "active") \
            .limit(1).execute()
        if r.data:
            return r.data[0].get("reserve_source") or ""
        return ""
    except Exception:
        return ""


def _escalate_reserve_down(client, src: dict, failing_reserve: str) -> None:
    """C1: slot DOWN while its reserve is active -> the reserve is failing.
    Throttled by last_alerted_at on the ACTIVE record (ALERT_INTERVAL_HOURS)."""
    name = src["name"]
    try:
        r = client.table("source_reserves") \
            .select("id, last_alerted_at") \
            .eq("primary_source", name) \
            .eq("status", "active") \
            .limit(1).execute()
        if not r.data:
            return
        rec = r.data[0]
        now = datetime.now(timezone.utc)
        last = rec.get("last_alerted_at")
        if last:
            try:
                last_dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
                if (now - last_dt).total_seconds() / 3600 < ALERT_INTERVAL_HOURS:
                    print("  Reserve-down escalation throttled for " + name)
                    return
            except Exception:
                pass
        msg = _build_reserve_alert(name, src.get("pillar", "geo"), src.get("avg", 0.0),
                                   0.0, src.get("reason", ""),
                                   failing_reserve=failing_reserve, escalation=True)
        if _send_admin_message(msg):
            print("  ESCALATION sent: reserve " + failing_reserve
                  + " also down for slot " + name)
            client.table("source_reserves").update(
                {"last_alerted_at": now.isoformat()}).eq("id", rec["id"]).execute()
    except Exception as e:
        print("  Warning: escalation failed for " + name + ": " + str(e)[:60])


def _auto_activate_reserve(client, src: dict, hours_down: float) -> bool:
    """C3 (flag-gated): pick the highest-priority pillar reserve (roster
    order = priority, R-S63-1 load-bearing) that is not the primary and is
    not already actively serving another slot; mark active, announce.
    All-busy falls back to full pool with a loud DOUBLE-VOICE confession.
    Returns True if activated. (FT-GAP-B, S74)"""
    if client is None:
        return False
    name = src["name"]
    pool = [r for r in _get_reserves_for_pillar(src.get("pillar", "geo"))
            if r["name"] != name]
    if not pool:
        return False
    # FT-GAP-B (S74): exclude reserves already serving ANOTHER slot --
    # two dead primaries must not double one reserve's voice (R-S64-3 kin).
    # Roster order = deliberate priority; NEVER reorder (R-S63-1 webhook).
    busy = set()
    try:
        act = client.table("source_reserves") \
            .select("reserve_source") \
            .eq("status", "active") \
            .neq("primary_source", name) \
            .execute()
        busy = {r["reserve_source"] for r in (act.data or [])}
    except Exception as e:
        print("  Warning: busy-reserve check failed, using full pool: " + str(e)[:60])
    avail = [r for r in pool if r["name"] not in busy]
    if not avail:
        print("  DOUBLE-VOICE: all " + src.get("pillar", "geo")
              + " reserves busy -- falling back to full pool (declared, not silent)")
        avail = pool
    choice = avail[0]
    try:
        rec = client.table("source_reserves") \
            .select("id") \
            .eq("primary_source", name) \
            .in_("status", ["pending", "alerted"]) \
            .order("created_at", desc=True) \
            .limit(1).execute()
        now = datetime.now(timezone.utc).isoformat()
        if rec.data:
            client.table("source_reserves").update({
                "status": "active", "reserve_source": choice["name"],
                "last_alerted_at": now,
            }).eq("id", rec.data[0]["id"]).execute()
        else:
            client.table("source_reserves").insert({
                "primary_source": name, "reserve_source": choice["name"],
                "status": "active", "last_alerted_at": now, "days_down": 0,
                "pillar": src.get("pillar", "geo"),
            }).execute()
        _send_admin_message(
            "\u26a1 <b>AUTO-ACTIVATED reserve</b> (unanswered "
            + format(hours_down, ".1f") + "h >= "
            + format(AUTO_RESERVE_AFTER_HOURS, ".1f") + "h)\n"
            + "Slot: " + name + "\nReserve: " + choice["name"]
            + "\nReply a number from the last alert anytime to override.")
        print("  AUTO-ACTIVATED " + choice["name"] + " for " + name)
        return True
    except Exception as e:
        print("  Warning: auto-activate failed for " + name + ": " + str(e)[:60])
        return False


def reserve_lifecycle(sources: list, source_stats: dict = None) -> None:
    """C2: retire the reserve record when the PRIMARY serves again (collector
    tries primary first every run -- recovery is organic; this keeps the DB
    truthful and tells James). C4: after a reserve serves cleanly >=
    PROMOTION_PROPOSAL_DAYS, send a throttled PROPOSAL -- never an action."""
    client = _get_client()
    if client is None or not source_stats:
        return
    try:
        rows = client.table("source_reserves") \
            .select("id, primary_source, reserve_source, created_at, last_alerted_at") \
            .eq("status", "active").execute().data or []
    except Exception:
        return
    now = datetime.now(timezone.utc)
    for row in rows:
        primary = row.get("primary_source", "")
        stat = source_stats.get(primary)
        if not stat:
            continue
        ok  = bool(stat.get("fetch_ok", False))
        raw = int(stat.get("raw", 0))
        served_by_reserve = bool(stat.get("is_reserve", False))

        # C2 -- primary recovered (it served this run with real entries)
        if ok and int(stat.get("yield", 0)) > 0 and not served_by_reserve:
            try:
                client.table("source_reserves").update(
                    {"status": "recovered"}).eq("id", row["id"]).execute()
                _send_admin_message(
                    "\u2705 <b>Primary recovered:</b> " + primary
                    + "\nReserve " + str(row.get("reserve_source"))
                    + " deactivated -- primary serving again.")
                print("  Reserve retired (primary recovered): " + primary)
            except Exception as e:
                print("  Warning: reserve retire failed: " + str(e)[:60])
            continue

        # C4 -- reserve serving cleanly long enough: proposal, 24h-throttled
        if ok and raw > 0 and served_by_reserve:
            try:
                created = datetime.fromisoformat(
                    str(row.get("created_at")).replace("Z", "+00:00"))
                days = (now - created).total_seconds() / 86400.0
            except Exception:
                continue
            if days < PROMOTION_PROPOSAL_DAYS:
                continue
            last = row.get("last_alerted_at")
            if last:
                try:
                    last_dt = datetime.fromisoformat(str(last).replace("Z", "+00:00"))
                    if (now - last_dt).total_seconds() / 3600 < 24.0:
                        continue
                except Exception:
                    pass
            _send_admin_message(
                "\U0001f4cb <b>PROMOTION PROPOSAL</b> (no action taken)\n"
                + "Reserve <b>" + str(row.get("reserve_source")) + "</b> has served slot <b>"
                + primary + "</b> cleanly for ~" + format(days, ".0f") + " days.\n"
                + "Options: promote it to primary (edit rss_collector.py), keep as-is, "
                + "or investigate reviving the primary. Your call.")
            try:
                client.table("source_reserves").update(
                    {"last_alerted_at": now.isoformat()}).eq("id", row["id"]).execute()
            except Exception:
                pass
            print("  Promotion proposal sent for " + primary)


def _selftest_health_verdict() -> None:
    """S45 arc A offline proof (no network/DB): replays the 2026-06-18 0643/1244
    enforcing scenario through the PURE verdict fn. The genuinely fetch-broken
    feeds flag DOWN; the slow-but-fetched opinion feeds (DFRLab/ICIJ/Bellingcat/
    HRW/WoR) do NOT -- even at yield 0. W2: assert exact membership."""
    P = RAW_ZERO_PATIENCE_HOURS

    # (label, tier, fetch_ok, raw, zero_streak_hours, EXPECT_DOWN)
    cases = [
        # genuinely fetch-broken -> DOWN (any tier, immediate)
        ("Stimson Center",          "news",    False, 0,  0.0,   True),
        ("AP News via Google News", "news",    False, 0,  0.0,   True),
        ("Crisis Group",            "opinion", False, 0,  0.0,   True),
        # news tier delivering 0 real entries -> DOWN immediately
        ("BBC (broken feed)",       "news",    True,  0,  0.0,   True),
        # slow tier, raw==0 SUSTAINED past patience -> DOWN (truly dead slow feed)
        ("Dead slow feed",          "opinion", True,  0,  P + 1, True),
        # slow-but-fetched opinion feeds, yield 0 but raw>0 -> HEALTHY (PHI-002)
        ("DFRLab",                  "opinion", True,  6,  0.0,   False),
        ("ICIJ",                    "opinion", True,  4,  0.0,   False),
        ("Bellingcat",              "opinion", True,  3,  0.0,   False),
        ("Human Rights Watch",      "opinion", True,  9,  0.0,   False),
        ("War on the Rocks",        "opinion", True,  2,  0.0,   False),
        # slow tier quiet for ONE run (raw==0, streak < patience) -> NOT down yet
        ("DFRLab (quiet day)",      "opinion", True,  0,  24.0,  False),
        ("RFE/RL (quiet review)",   "review",  True,  0,  12.0,  False),
        # healthy news feed -> NOT down
        ("BBC",                     "news",    True,  18, 0.0,   False),
    ]

    down    = [c[0] for c in cases if _health_verdict(c[1], c[2], c[3], c[4])[0]]
    exp_dn  = [c[0] for c in cases if c[5]]
    assert down == exp_dn, ("verdict mismatch\n  got DOWN:      " + repr(down)
                            + "\n  expected DOWN: " + repr(exp_dn))

    # W2: exactly the 5 broken feeds flag, exactly the 8 healthy/quiet do not
    assert len(exp_dn) == 5,  "expected 5 DOWN, scenario drifted: " + str(len(exp_dn))
    assert len(down)   == 5,  "verdict flagged != 5: " + repr(down)

    print("  [selftest] health verdict OK: " + str(len(down))
          + " fetch-broken flagged, " + str(len(cases) - len(down))
          + " slow-but-fetched / quiet held (NOT flagged)")


if __name__ == "__main__":
    print("GNI Source Health Monitor -- Test Run (offline)\n")
    _selftest_health_verdict()
