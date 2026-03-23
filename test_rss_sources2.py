import feedparser

sources = [
    ("The Verge",       "https://www.theverge.com/rss/index.xml"),
    ("Digital Trends",  "https://www.digitaltrends.com/feed/"),
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
