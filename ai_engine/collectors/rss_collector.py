import feedparser
import hashlib
from datetime import datetime, timezone
from typing import Optional

# ============================================================
# GNI RSS Collector -- Updated
# 25 sources: 12 Geo + 8 Tech + 5 Fin
# Democracy framework applied -- minimum 50% threshold
# Each source has pillar field for 60/20/20 funnel quota
# ============================================================

SOURCES = [

    # ── GEOPOLITICAL PILLAR (12 sources) ─────────────────────
    {"name": "BBC",
     "url": "https://feeds.bbci.co.uk/news/world/rss.xml",
     "pillar": "geo", "bias": "Western Liberal", "democracy_score": 88},

    {"name": "DW News",
     "url": "https://rss.dw.com/xml/rss-en-world",
     "pillar": "geo", "bias": "Western Liberal", "democracy_score": 84},

    {"name": "France 24",
     "url": "https://www.france24.com/en/rss",
     "pillar": "geo", "bias": "Western Liberal", "democracy_score": 81},

    {"name": "Al Jazeera",
     "url": "https://www.aljazeera.com/xml/rss/all.xml",
     "pillar": "geo", "bias": "Non-Western", "democracy_score": 70},

    {"name": "CNN",
     "url": "http://rss.cnn.com/rss/edition.rss",
     "pillar": "geo", "bias": "Western Liberal", "democracy_score": 69},

    {"name": "Eye on the Arctic",
     "url": "https://www.rcinet.ca/eye-on-the-arctic/feed/",
     "pillar": "geo", "bias": "Specialist", "democracy_score": 55},

    {"name": "USNI News",
     "url": "https://news.usni.org/feed",
     "pillar": "geo", "bias": "Specialist", "democracy_score": 55},

    {"name": "The Diplomat",
     "url": "https://thediplomat.com/feed/",
     "pillar": "geo", "bias": "Academic", "democracy_score": 85},

    {"name": "The Conversation",
     "url": "https://theconversation.com/global/articles.atom",
     "pillar": "geo", "bias": "Academic", "democracy_score": 83},

    {"name": "Human Rights Watch",
     "url": "https://www.hrw.org/rss.xml",
     "pillar": "geo", "bias": "Human Rights", "democracy_score": 93},

    {"name": "Foreign Policy",
     "url": "https://foreignpolicy.com/feed/",
     "pillar": "geo", "bias": "Research", "democracy_score": 84},

    {"name": "Crisis Group",
     "url": "https://www.crisisgroup.org/rss.xml",
     "pillar": "geo", "bias": "Research", "democracy_score": 92},

    # ── FINANCIAL PILLAR (5 sources) ──────────────────────────
    {"name": "Financial Times",
     "url": "https://www.ft.com/?format=rss",
     "pillar": "fin", "bias": "Financial", "democracy_score": 79},

    {"name": "The Economist",
     "url": "https://www.economist.com/finance-and-economics/rss.xml",
     "pillar": "fin", "bias": "Financial", "democracy_score": 88},

    {"name": "Project Syndicate",
     "url": "https://www.project-syndicate.org/rss",
     "pillar": "fin", "bias": "Research", "democracy_score": 79},

    {"name": "Nikkei Asia",
     "url": "https://asia.nikkei.com/rss/feed/nar",
     "pillar": "fin", "bias": "Financial", "democracy_score": 62},

    {"name": "CNBC World",
     "url": "https://www.cnbc.com/id/100727362/device/rss/rss.html",
     "pillar": "fin", "bias": "Financial", "democracy_score": 65},

    # ── TECHNOLOGY PILLAR (8 sources) ─────────────────────────
    {"name": "Wired",
     "url": "https://www.wired.com/feed/rss",
     "pillar": "tech", "bias": "Technology", "democracy_score": 68},

    {"name": "MIT Technology Review",
     "url": "https://www.technologyreview.com/feed/",
     "pillar": "tech", "bias": "Technology", "democracy_score": 71},

    {"name": "EFF Deeplinks",
     "url": "https://www.eff.org/rss/updates.xml",
     "pillar": "tech", "bias": "Digital Rights", "democracy_score": 91},

    {"name": "Rest of World",
     "url": "https://restofworld.org/feed/",
     "pillar": "tech", "bias": "Global Tech", "democracy_score": 87},

    {"name": "Krebs on Security",
     "url": "https://krebsonsecurity.com/feed/",
     "pillar": "tech", "bias": "Cybersecurity", "democracy_score": 81},

    {"name": "Bellingcat",
     "url": "https://www.bellingcat.com/feed/",
     "pillar": "tech", "bias": "OSINT", "democracy_score": 90},

    {"name": "Ars Technica",
     "url": "https://feeds.arstechnica.com/arstechnica/index",
     "pillar": "tech", "bias": "Technology", "democracy_score": 68},

    {"name": "IEEE Spectrum",
     "url": "https://spectrum.ieee.org/feeds/feed.rss",
     "pillar": "tech", "bias": "Technology", "democracy_score": 74},

]


def make_id(title: str, source: str) -> str:
    """Generate unique article ID from title + source."""
    raw = f"{source}:{title}".encode("utf-8")
    return hashlib.md5(raw).hexdigest()


def parse_date(entry) -> str:
    """Extract published date from RSS entry."""
    if hasattr(entry, "published_parsed") and entry.published_parsed:
        dt = datetime(*entry.published_parsed[:6], tzinfo=timezone.utc)
        return dt.isoformat()
    return datetime.now(timezone.utc).isoformat()


def collect_articles(max_per_source: int = 20) -> list[dict]:
    """
    Collect articles from all RSS sources.
    Returns list of article dicts with pillar field.
    """
    articles = []
    seen_ids = set()

    for source in SOURCES:
        try:
            print(f"  Fetching: {source['name']}...")
            feed = feedparser.parse(source["url"])

            if feed.bozo and not feed.entries:
                print(f"  Warning: {source['name']}: Feed error -- skipping")
                continue

            count = 0
            for entry in feed.entries[:max_per_source]:
                title = entry.get("title", "").strip()
                summary = entry.get("summary", "").strip()
                link = entry.get("link", "").strip()

                if not title:
                    continue

                article_id = make_id(title, source["name"])
                if article_id in seen_ids:
                    continue
                seen_ids.add(article_id)

                articles.append({
                    "id": article_id,
                    "title": title,
                    "summary": summary,
                    "link": link,
                    "source": source["name"],
                    "bias": source["bias"],
                    "pillar": source["pillar"],
                    "democracy_score": source.get("democracy_score", 50),
                    "published_at": parse_date(entry),
                    "collected_at": datetime.now(timezone.utc).isoformat(),
                })
                count += 1

            print(f"  OK {source['name']}: {count} articles")

        except Exception as e:
            print(f"  Error {source['name']}: {e}")
            continue

    print(f"\n  Total collected: {len(articles)} articles")
    return articles


if __name__ == "__main__":
    print("GNI RSS Collector -- Test Run\n")
    articles = collect_articles(max_per_source=5)
    if articles:
        print(f"\nSample article:")
        a = articles[0]
        print(f"  Source:  {a['source']} ({a['bias']}) [{a['pillar'].upper()}]")
        print(f"  Title:   {a['title'][:80]}")
        print(f"  Democracy score: {a['democracy_score']}%")
    geo = len([s for s in SOURCES if s['pillar']=='geo'])
    fin = len([s for s in SOURCES if s['pillar']=='fin'])
    tech = len([s for s in SOURCES if s['pillar']=='tech'])
    print(f"\nSource pool: {geo} Geo + {fin} Fin + {tech} Tech = {len(SOURCES)} total")
