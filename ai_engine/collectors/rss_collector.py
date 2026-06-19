import feedparser
import hashlib
from datetime import datetime, timezone
from typing import Optional

# ============================================================
# GNI RSS Collector — Updated with Reserve Source Support
# Primary sources: 31 Geo + 5 Fin + 6 Tech = 42 (S44: PHI-001 cut + O1 swap + §4 ports)
# Democracy framework applied -- minimum 50% threshold
# Reserve sources activated by admin via Telegram reply (1-5)
# Active reserves fetched from Supabase source_reserves table
# ============================================================

SOURCES = [

    # ── GEOPOLITICAL PILLAR (12 sources) ─────────────────────
    {"name": "BBC",
     "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
     "content_type": "news", "pillar": "geo", "bias": "Western Liberal", "democracy_score": 88},

    {"name": "DW News",
     "url": "https://rss.dw.com/xml/rss-en-world",
     "content_type": "news", "pillar": "geo", "bias": "Western Liberal", "democracy_score": 84},

    {"name": "France 24",
     "url": "https://www.france24.com/en/rss",
     "content_type": "news", "pillar": "geo", "bias": "Western Liberal", "democracy_score": 81},

    {"name": "Al Jazeera",
     "url": "https://www.aljazeera.com/xml/rss/all.xml",
     "content_type": "news", "pillar": "geo", "bias": "Non-Western", "democracy_score": 70},

    # O1 swap (S44): CNN removed — rss.cnn.com host frozen Aug 2024 (serves
    #   archive entries with NO machine-readable date; strict gate drops all).
    #   Replaced with NDTV World (live-verified fresh 8.3h).
    {"name": "NDTV World",
     "url": "https://feeds.feedburner.com/ndtvnews-world-news",
     "content_type": "news", "pillar": "geo", "bias": "Non-Western", "democracy_score": 68},

    {"name": "Eye on the Arctic",
     "url": "https://www.rcinet.ca/eye-on-the-arctic/feed/",
     "content_type": "news", "pillar": "geo", "bias": "Specialist", "democracy_score": 55},

    {"name": "USNI News",
     "url": "https://news.usni.org/feed",
     "content_type": "news", "pillar": "geo", "bias": "Specialist", "democracy_score": 55},

    {"name": "The Conversation",
     "url": "https://theconversation.com/global/articles.atom",
     "content_type": "news", "pillar": "geo", "bias": "Academic", "democracy_score": 83},

    {"name": "Human Rights Watch",
     "url": "https://www.hrw.org/rss.xml",
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "Human Rights", "democracy_score": 93},

    {"name": "Crisis Group",
     "url": "https://www.crisisgroup.org/rss.xml",
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "Research", "democracy_score": 92},


    {"name": "NPR World News",
     "url": "https://feeds.npr.org/1004/rss.xml",
     "content_type": "news", "pillar": "geo", "bias": "Wire Service", "democracy_score": 82},

    {"name": "AP News via Google News",
     "url": "https://apnews.com/rss/apf-topnews",
     "content_type": "news", "pillar": "geo", "bias": "Wire Service", "democracy_score": 88},

    {"name": "Africa Is A Country",
     "url": "https://africasacountry.com/feed",
     "content_type": "news", "pillar": "geo", "bias": "Post-Colonial Analysis", "democracy_score": 75},

    # PHI-001 cut (S44): The Africa Report removed — teaser-only feed on a metered site
    #   (dead-on-arrival link for free Telegram readers). Africa Is A Country retained for coverage.
    # ── S38 NEW GEO SOURCES ───────────────────────────────────

    {"name": "War on the Rocks",
     "url": "https://warontherocks.com/feed/",
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "Security Research",
     "democracy_score": 82},

    {"name": "DFRLab",
     "url": "https://dfrlab.org/feed/",  # O1 swap (S44): moved off Medium Feb 2025; ~150h cadence
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "OSINT/Disinformation",
     "democracy_score": 88},

    {"name": "ICIJ",
     "url": "https://icij.org/feed/",
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "Investigative",
     "democracy_score": 92},

    {"name": "Stimson Center",
     "url": "https://www.stimson.org/feed/",
     "content_type": "news", "pillar": "geo", "bias": "Peace Research",
     "democracy_score": 88},

    {"name": "Amnesty International",
     "url": "https://www.amnesty.org/en/feed/",
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "Human Rights",
     "democracy_score": 91},
    {"name": "Breaking Defense",
     "url": "https://breakingdefense.com/full-rss-feed/",
     "content_type": "news", "pillar": "geo", "bias": "Specialist",
     "democracy_score": 78},
    {"name": "Dawn",
     "url": "https://www.dawn.com/feeds/world",
     "content_type": "news", "pillar": "geo", "bias": "Non-Western",
     "democracy_score": 68},

    # ── S44 NEW GEO SOURCES (§4 ports — all live-verified fresh this session) ──
    # news tier (18h default gate):
    {"name": "Fox News World",
     "url": "https://moxie.foxnews.com/google-publisher/world.xml",
     "content_type": "news", "pillar": "geo", "bias": "Western Conservative", "democracy_score": 60},

    {"name": "Myanmar Now",
     "url": "https://myanmar-now.org/en/feed/",
     "content_type": "news", "pillar": "geo", "bias": "Myanmar Independent", "democracy_score": 80},

    {"name": "Meduza EN",
     "url": "https://meduza.io/rss/en/all",
     "content_type": "news", "pillar": "geo", "bias": "Russian Independent (exile)", "democracy_score": 85},

    {"name": "The Moscow Times",
     "url": "https://www.themoscowtimes.com/rss/news",
     "content_type": "news", "pillar": "geo", "bias": "Russian Independent (exile)", "democracy_score": 82},

    {"name": "Daily NK",
     "url": "https://www.dailynk.com/english/feed/",
     "content_type": "news", "pillar": "geo", "bias": "North Korea Focus", "democracy_score": 75},

    {"name": "Hong Kong Free Press",
     "url": "https://hongkongfp.com/feed/",
     "content_type": "news", "pillar": "geo", "bias": "HK Independent", "democracy_score": 85},

    # review tier (48h) + opinion (RFA, 120h) via inline "tier" fields (S44 arc 4).
    #   gov-funded (RFE/RL, RFA): §5 bias-guard + OP-005, democracy_score set
    #   BELOW reader/NGO outlets so no state narrative is laundered.
    {"name": "RFE/RL",
     "url": "https://news.google.com/rss/search?q=when:48h+site:rferl.org&hl=en-US&gl=US&ceid=US:en",
     "content_type": "news", "pillar": "geo", "tier": "review", "bias": "US-Gov Funded", "democracy_score": 72},

    {"name": "Global Voices",
     "url": "https://globalvoices.org/feed/",
     "content_type": "news", "pillar": "geo", "tier": "review", "bias": "Citizen Media/Global South", "democracy_score": 87},

    {"name": "Radio Free Asia",
     "url": "https://www.rfa.org/english/rss2.xml",
     "content_type": "news", "pillar": "geo", "tier": "opinion", "bias": "US-Gov Funded", "democracy_score": 70},

    {"name": "The Irrawaddy",
     "url": "https://news.google.com/rss/search?q=when:48h+site:irrawaddy.com&hl=en-US&gl=US&ceid=US:en",
     "content_type": "news", "pillar": "geo", "tier": "review", "bias": "Myanmar Independent", "democracy_score": 80},

    {"name": "IranWire",
     "url": "https://news.google.com/rss/search?q=when:48h+site:iranwire.com&hl=en-US&gl=US&ceid=US:en",
     "content_type": "news", "pillar": "geo", "tier": "review", "bias": "Iranian Independent", "democracy_score": 82},

    # ── FINANCIAL PILLAR (5 sources) ──────────────────────────
    # PHI-001 cut (S44): Project Syndicate (register-gate) + Bloomberg Economics
    #   (the entry formerly mislabeled "ING Think" carried feeds.bloomberg.com,
    #   hard-metered) removed. Backfilled with free Google-News FIN feeds below.
    {"name": "Yahoo Finance",
     "url": "https://finance.yahoo.com/news/rssindex",
     "content_type": "news", "pillar": "fin", "bias": "Financial Aggregator", "democracy_score": 70},

    {"name": "CNBC World",
     "url": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
     "content_type": "news", "pillar": "fin", "bias": "Financial", "democracy_score": 65},

    # S44 FIN backfill — free Google-News search feeds (when:24h keeps them fresh)
    {"name": "FIN Financial Stability (Google News)",
     "url": "https://news.google.com/rss/search?q=when:24h+%22sanctions%22+OR+%22financial+stability%22+OR+%22debt+crisis%22&hl=en-US&gl=US&ceid=US:en",
     "content_type": "news", "pillar": "fin", "bias": "Financial Aggregator", "democracy_score": 70},

    {"name": "FIN Central Banks (Google News)",
     "url": "https://news.google.com/rss/search?q=when:24h+%22central+bank%22+OR+%22Federal+Reserve%22+OR+%22interest+rates%22+OR+%22inflation%22&hl=en-US&gl=US&ceid=US:en",
     "content_type": "news", "pillar": "fin", "bias": "Financial Aggregator", "democracy_score": 70},

    {"name": "FIN IMF/World Bank (Google News)",
     "url": "https://news.google.com/rss/search?q=when:24h+%22IMF%22+OR+%22World+Bank%22+OR+%22sovereign+debt%22&hl=en-US&gl=US&ceid=US:en",
     "content_type": "news", "pillar": "fin", "bias": "Financial Aggregator", "democracy_score": 70},

    # ── TECHNOLOGY PILLAR (8 sources) ─────────────────────────
    # PHI-001 cut (S44): Wired removed — metered paywall (dead link for free readers).
    {"name": "EFF Deeplinks",
     "url": "https://www.eff.org/rss/updates.xml",
     "content_type": "news", "pillar": "tech", "tier": "opinion", "bias": "Digital Rights", "democracy_score": 91},

    {"name": "Rest of World",
     "url": "https://restofworld.org/feed/",
     "content_type": "news", "pillar": "tech", "bias": "Global Tech", "democracy_score": 87},

    {"name": "Krebs on Security",
     "url": "https://krebsonsecurity.com/feed/",
     "content_type": "news", "pillar": "tech", "bias": "Cybersecurity", "democracy_score": 81},

    {"name": "Bellingcat",
     "url": "https://www.bellingcat.com/feed/",
     "content_type": "news", "pillar": "tech", "tier": "opinion", "bias": "OSINT", "democracy_score": 90},

    {"name": "Ars Technica",
     "url": "https://feeds.arstechnica.com/arstechnica/index",
     "content_type": "news", "pillar": "tech", "bias": "Technology", "democracy_score": 68},

    {"name": "IEEE Spectrum",
     "url": "https://spectrum.ieee.org/feeds/feed.rss",
     "content_type": "news", "pillar": "tech", "tier": "opinion", "bias": "Technology", "democracy_score": 74},

]


def _get_active_reserves() -> dict:
    """
    Fetch active reserve sources from Supabase.
    Returns dict: {primary_source_name: reserve_source_dict}
    Only called once per pipeline run for efficiency.
    """
    try:
        from analysis.source_health_monitor import get_active_reserves
        return get_active_reserves()
    except Exception as e:
        print("  Warning: Could not fetch active reserves: " + str(e)[:60])
        return {}


def make_id(title: str, source: str) -> str:
    """Generate unique article ID from title + source."""
    raw = f"{source}:{title}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()


def parse_date(entry) -> tuple:
    """Extract published date from RSS entry.
    Returns (iso_string, date_is_real). date_is_real is False when the feed
    gave no machine-readable date and we fell back to now() -- the U2 capture-lag
    gate must know the difference so a faked 'now' cannot silently pass."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt.isoformat(), True
    return datetime.now(timezone.utc).isoformat(), False


# ============================================================
# U2 -- Capture-Lag Freshness Gate (3-tier model, S44 arc 4)
# lag = collected_at - published_at; drop if lag > TIER_WINDOW_HOURS[tier].
# Each source declares "tier" ("news"|"review"|"opinion"); absent => "news".
# Missing/unparseable publish date = STRICT DROP (date_is_real from parse_date).
# DRY-RUN: logs what it WOULD drop, drops nothing, until verified live.
# ============================================================
TIER_WINDOW_HOURS = {"news": 18.0, "review": 48.0, "opinion": 120.0}
DEFAULT_TIER = "news"
CAPTURE_GATE_DRY_RUN = False          # arc-4 FLIP: gate now enforcing (drops in production)

# §1 tier mapping (inline "tier" field on each source dict; search '"tier":'):
#   opinion (120h) = the old 168h "analysis" set, tightened: Crisis Group, HRW,
#     Amnesty, ICIJ, Bellingcat, War on the Rocks, DFRLab, Radio Free Asia.
#   review (48h): RFE/RL, Global Voices, The Irrawaddy, IranWire.
#   news (18h): all others (default).
# NOTE (S44, user-accepted): opinion@120h drops Crisis Group (~250h) and DFRLab
#   (~150h) while they are stale -- their slow cadence exceeds the strict ceiling.


def _window_for(source: dict) -> float:
    """Return the freshness window (hours) for a source by its declared tier.
    Absent tier defaults to 'news' (18h, the strict fresh standard)."""
    tier = source.get("tier", DEFAULT_TIER)
    return TIER_WINDOW_HOURS.get(tier, TIER_WINDOW_HOURS[DEFAULT_TIER])


def _within_capture_window(published_iso: str, collected_iso: str,
                           date_is_real: bool, max_hours: float = TIER_WINDOW_HOURS["news"]) -> tuple:
    """Return (keep, reason). lag = collected - published.
    Strict: a missing real publish date fails the gate.
    max_hours is the per-source freshness window (tiered)."""
    if not date_is_real:
        return False, "no-real-date"
    try:
        p = datetime.fromisoformat(published_iso)
        c = datetime.fromisoformat(collected_iso)
    except Exception:
        return False, "unparseable-date"
    lag_h = (c - p).total_seconds() / 3600.0
    if lag_h > max_hours:
        return False, "stale " + format(lag_h, ".1f") + "h"
    return True, "ok " + format(lag_h, ".1f") + "h"


# ============================================================
# Feed-chrome guard (S45 arc B)
# Some site:/archive feeds emit nav/breadcrumb rows AS entries (epoch-zero
# dates, feed-title echoes). They are not articles. Skip them BEFORE the
# pipeline AND before they count toward a source's raw-entry total -- so the
# (Arc A) health monitor never sees feed chrome as real fetched content.
# Two independent signals (OR):
#   1. implausibly old publish date  (lag > CHROME_MAX_LAG_HOURS ~ 5 years)
#   2. title is nav/breadcrumb chrome (feed-title echo or denylist label)
# Pure-ASCII anchors (LR-101). Short labels match EXACT title only -- a
# substring "home" would wrongly drop "Homes destroyed in ...".
# ============================================================
CHROME_MAX_LAG_HOURS = 43800.0          # ~5 years: older => feed-chrome, not an article
CHROME_TITLE_EXACT = ("home", "majlis", "archives")        # whole-title nav labels
CHROME_TITLE_CONTAINS = ("video archive", "donate to")     # distinctive chrome phrases


def _is_feed_chrome(title: str, feed_title: str, pub_iso: str,
                    date_is_real: bool, collected_iso: str) -> tuple:
    """Return (is_chrome, reason). True => skip this entry as feed chrome."""
    tl = title.strip().lower()

    # signal 1: implausibly old publish date (epoch-ish chrome marker)
    if date_is_real:
        try:
            p = datetime.fromisoformat(pub_iso)
            c = datetime.fromisoformat(collected_iso)
            lag_h = (c - p).total_seconds() / 3600.0
            if lag_h > CHROME_MAX_LAG_HOURS:
                return True, "chrome-stale " + format(lag_h, ".0f") + "h"
        except Exception:
            pass

    # signal 2: title is the feed's own name / a breadcrumb / a nav label
    ftl = (feed_title or "").strip().lower()
    if ftl:
        if tl == ftl:
            return True, "title==feed-title"
        if tl.endswith(" - " + ftl) or tl.endswith(" | " + ftl):
            return True, "feed-title breadcrumb"
    for bad in CHROME_TITLE_EXACT:
        if tl == bad:
            return True, "chrome-title '" + bad + "'"
    for bad in CHROME_TITLE_CONTAINS:
        if bad in tl:
            return True, "chrome-phrase '" + bad + "'"

    return False, ""


def collect_articles(max_per_source: int = 20) -> tuple[list[dict], dict]:
    """
    Collect articles from all RSS sources.
    If a primary source is down and admin has activated a reserve,
    the reserve source is used automatically.
    Returns (articles, source_stats).
      articles     -- list of article dicts (post chrome/dedup/freshness gate).
      source_stats -- {primary_name: {"fetch_ok": bool, "raw": int, "yield": int,
                       "reason": str}} for the source actually served (primary or
                       reserve). raw = real candidate entries the feed delivered
                       (post chrome-guard, PRE dedup/freshness) -- the honest
                       up/down signal the S45 arc-A health monitor measures on.
                       yield = survivors after the gate (expected LOW for opinion
                       tier; NOT a health signal).
    """
    articles = []
    seen_ids = set()
    capture_dropped = 0
    chrome_skipped = 0
    source_stats = {}

    # Fetch active reserves once at start of collection
    active_reserves = _get_active_reserves()
    if active_reserves:
        print("  Active reserves: " + ", ".join(
            f"{k} → {v['name']}" for k, v in active_reserves.items()
        ))

    for source in SOURCES:
        name = source["name"]

        # Check if this source has an active reserve
        # Try primary first — if it fails and reserve exists, use reserve
        sources_to_try = [source]
        if name in active_reserves:
            sources_to_try.append(active_reserves[name])

        collected = 0
        for src in sources_to_try:
            src_name = src["name"]
            is_reserve = src_name != name

            # Per-attempt fetch-health (S45 arc A). Reset each attempt so the
            # recorded stat reflects the source that actually served the slot.
            fetch_ok = False
            raw_count = 0
            fetch_reason = "not-fetched"

            try:
                label = f"{src_name} [RESERVE for {name}]" if is_reserve else src_name
                print(f"  Fetching: {label}...")
                feed = feedparser.parse(src["url"])

                if feed.bozo and not feed.entries:
                    bozo_exc = getattr(feed, "bozo_exception", "")
                    fetch_reason = ("fetch-fail status=" + str(getattr(feed, "status", "?"))
                                    + (" " + str(bozo_exc)[:80] if bozo_exc else ""))
                    if is_reserve:
                        print(f"  Warning: Reserve {src_name} also failed — no articles for {name}")
                    else:
                        print(f"  Warning: {src_name}: Feed error -- trying reserve if available")
                    continue

                # Transport succeeded: HTTP-level fetch is healthy regardless of
                # how many entries survive the downstream gate.
                fetch_ok = True
                fetch_reason = "ok status=" + str(getattr(feed, "status", "?"))

                feed_title = ""
                try:
                    feed_title = feed.feed.get("title", "")
                except Exception:
                    feed_title = ""

                count = 0
                for entry in feed.entries[:max_per_source]:
                    title   = entry.get("title", "").strip()
                    summary = entry.get("summary", "").strip()
                    link    = entry.get("link", "").strip()

                    if not title:
                        continue

                    pub_iso, date_is_real = parse_date(entry)
                    col_iso = datetime.now(timezone.utc).isoformat()

                    # Feed-chrome guard (S45 arc B): drop nav/archive rows BEFORE
                    # the pipeline and before they count as raw fetched content.
                    is_chrome, chrome_reason = _is_feed_chrome(
                        title, feed_title, pub_iso, date_is_real, col_iso)
                    if is_chrome:
                        chrome_skipped += 1
                        print("  [CHROME-SKIP] (" + chrome_reason + "): " + src_name + " | " + title[:60])
                        continue

                    # Real candidate entry the feed delivered. Count it as RAW
                    # fetch health BEFORE dedup/freshness -- those are legitimate
                    # downstream filters, not feed-down signals (S45 arc A).
                    raw_count += 1

                    article_id = make_id(title, src_name)
                    if article_id in seen_ids:
                        continue

                    keep, reason = _within_capture_window(pub_iso, col_iso, date_is_real, _window_for(source))
                    if not keep:
                        capture_dropped += 1
                        if CAPTURE_GATE_DRY_RUN:
                            print("  [CAPTURE-LAG dry-run] would drop (" + reason + "): " + src_name + " | " + title[:60])
                        else:
                            print("  [CAPTURE-LAG] dropped (" + reason + "): " + src_name + " | " + title[:60])
                            continue

                    seen_ids.add(article_id)

                    articles.append({
                        "id":               article_id,
                        "title":            title,
                        "summary":          summary,
                        "link":             link,
                        "source":           name,           # Always log as primary source name
                        "source_actual":    src_name,       # Track actual source used
                        "is_reserve":       is_reserve,
                        "bias":             src.get("bias", source.get("bias", "")),
                        "pillar":           src.get("pillar", source.get("pillar", "geo")),
                        "democracy_score":  src.get("democracy_score", source.get("democracy_score", 50)),
                        "content_type":     src.get("content_type", source.get("content_type", "news")),
                        "published_at":     pub_iso,
                        "collected_at":     col_iso,
                    })
                    count += 1

                if is_reserve:
                    print(f"  OK {src_name} [RESERVE]: {count} articles (replacing {name})")
                else:
                    print(f"  OK {src_name}: {count} articles")

                collected = count
                break  # Success — no need to try reserve

            except Exception as e:
                fetch_ok = False
                fetch_reason = "exception: " + str(e)[:80]
                print(f"  Error {src_name}: {e}")
                continue

        # Record fetch health for the slot (values reflect the last attempt =
        # the source that served, or the final failed attempt). Keyed by the
        # PRIMARY name -- the health monitor tracks slots, not reserve URLs.
        source_stats[name] = {
            "fetch_ok": fetch_ok,
            "raw":      raw_count,
            "yield":    collected,
            "reason":   fetch_reason,
        }

        if collected == 0 and name not in active_reserves:
            print(f"  Warning: {name}: 0 articles collected — reserve not yet activated")

    print(f"\n  Total collected: {len(articles)} articles")

    if chrome_skipped:
        print("  Feed-chrome guard: skipped " + str(chrome_skipped) + " nav/archive row(s) (not articles)")

    if capture_dropped:
        mode = "would drop (dry-run)" if CAPTURE_GATE_DRY_RUN else "dropped"
        print("  Capture-lag gate (3-tier 18/48/120h): " + mode + " " + str(capture_dropped) + " stale article(s)")

    # Show reserve usage summary
    reserve_used = [a for a in articles if a.get("is_reserve")]
    if reserve_used:
        print(f"  Reserve articles included: {len(reserve_used)}")

    return articles, source_stats


def _selftest_chrome() -> None:
    """S45 arc B self-test (no network): the live junk rows flag, real
    headlines do not. W2 -- assert exact counts."""
    now = datetime.now(timezone.utc)
    n = now.isoformat()
    old = now.replace(year=now.year - 8).isoformat()   # ~70,000h old

    # (title, feed_title, pub_iso, date_is_real)
    junk = [
        ("Video Archive - Radio Free Europe/Radio Liberty", "Radio Free Europe/Radio Liberty", old, True),
        ("Rohingya Archives - The Irrawaddy", "The Irrawaddy", old, True),
        ("Majlis", "Radio Free Europe/Radio Liberty", n, True),
        ("Home", "Radio Free Europe/Radio Liberty", n, True),
        ("Donate to ICIJ", "ICIJ", n, False),
    ]
    real = [
        ("Myanmar junta launches new offensive in Rakhine", "Myanmar Now", n, True),
        ("Meduza editor detained at the border", "Meduza", n, True),
        ("Homes destroyed as floods hit Pakistan", "Dawn", n, True),
        ("Pentagon archives declassified after 50 years", "USNI News", n, True),
    ]

    flagged = [t for (t, ft, p, r) in junk if _is_feed_chrome(t, ft, p, r, n)[0]]
    assert len(flagged) == len(junk), \
        "chrome guard MISSED junk: " + repr([t for (t, *_ ) in junk if t not in flagged])

    passed = [t for (t, ft, p, r) in real if not _is_feed_chrome(t, ft, p, r, n)[0]]
    assert len(passed) == len(real), \
        "chrome guard FALSE-POSITIVED a real headline: " + repr([t for (t, *_ ) in real if t not in passed])

    print("  [selftest] chrome guard OK: " + str(len(junk)) + " junk flagged, "
          + str(len(real)) + " real passed")


if __name__ == "__main__":
    print("GNI RSS Collector -- Test Run\n")
    _selftest_chrome()
    articles, _stats = collect_articles(max_per_source=5)
    if articles:
        print(f"\nSample article:")
        a = articles[0]
        print(f"  Source:  {a['source']} ({a['bias']}) [{a['pillar'].upper()}]")
        print(f"  Title:   {a['title'][:80]}")
        print(f"  Democracy score: {a['democracy_score']}%")
    geo  = len([s for s in SOURCES if s['pillar']=='geo'])
    fin  = len([s for s in SOURCES if s['pillar']=='fin'])
    tech = len([s for s in SOURCES if s['pillar']=='tech'])
    print(f"\nSource pool: {geo} Geo + {fin} Fin + {tech} Tech = {len(SOURCES)} total")
