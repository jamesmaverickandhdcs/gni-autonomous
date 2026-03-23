import feedparser
import urllib.request

urls = [
    ("Economist Finance",       "https://www.economist.com/finance-and-economics/rss.xml"),
    ("Economist World",         "https://www.economist.com/the-world-this-week/rss.xml"),
    ("Economist Leaders",       "https://www.economist.com/leaders/rss.xml"),
    ("Economist Business",      "https://www.economist.com/business/rss.xml"),
    ("Economist Asia",          "https://www.economist.com/asia/rss.xml"),
    ("Economist all sections",  "https://www.economist.com/sections/rss.xml"),
    ("Economist print edition", "https://www.economist.com/printedition/rss.xml"),
    ("Economist via feedburner","https://feeds.feedburner.com/economist/full_rss"),
    ("Economist via feed.rss",  "https://www.economist.com/rss"),
    ("Economist via atom",      "https://www.economist.com/atom.xml"),
]

print("Testing The Economist RSS patterns...\n")
ok = []

for name, url in urls:
    try:
        # Try with custom headers to mimic browser
        req = urllib.request.Request(url, headers={
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept": "application/rss+xml, application/xml, text/xml, */*",
        })
        with urllib.request.urlopen(req, timeout=10) as resp:
            content = resp.read()
            status = resp.status

        feed = feedparser.parse(content)
        if feed.entries:
            title = feed.entries[0].get("title", "")[:55]
            count = len(feed.entries)
            ok.append((name, count, url))
            print(f"  OK    {name}: {count} articles")
            print(f"        Sample: {title}")
        else:
            print(f"  EMPTY {name}: 0 entries (bozo={feed.bozo}, status={status})")

    except Exception as e:
        # Also try feedparser directly
        feed = feedparser.parse(url)
        if feed.entries:
            ok.append((name, len(feed.entries), url))
            print(f"  OK*   {name}: {len(feed.entries)} articles (via feedparser)")
        else:
            print(f"  ERR   {name}: {str(e)[:55]} (bozo={feed.bozo})")

print(f"\n{'='*50}")
if ok:
    print(f"WORKING: {len(ok)}")
    for name, count, url in ok:
        print(f"  {name}: {count} articles")
        print(f"  URL: {url}")
else:
    print("NO WORKING ECONOMIST RSS FOUND")
    print("\nThe Economist likely requires JavaScript rendering or login.")
    print("Cannot be added to feedparser-based pipeline.")
