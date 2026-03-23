import feedparser

sources = [
    ("Foreign Policy",  "https://foreignpolicy.com/feed/"),
    ("IISS",            "https://www.iiss.org/rss/online-analysis"),
    ("IISS alt 1",      "https://www.iiss.org/feeds/"),
    ("IISS alt 2",      "https://www.iiss.org/rss"),
]

for name, url in sources:
    try:
        feed = feedparser.parse(url)
        if feed.entries:
            title = feed.entries[0].get("title", "(no title)")[:60]
            print(f"  OK    {name}: {len(feed.entries)} articles")
            print(f"        Sample: {title}")
        else:
            print(f"  EMPTY {name}: 0 articles (bozo={feed.bozo})")
            print(f"        URL: {url}")
    except Exception as e:
        print(f"  ERR   {name}: {e}")
