import feedparser

urls = [
    ("Reuters Top News",      "https://feeds.reuters.com/reuters/topNews"),
    ("Reuters World",         "https://feeds.reuters.com/reuters/worldNews"),
    ("Reuters Business",      "https://feeds.reuters.com/reuters/businessNews"),
    ("Reuters alt 1",         "https://www.reuters.com/rssFeed/worldNews"),
    ("Reuters alt 2",         "https://feeds.reuters.com/news/world"),
    ("Reuters alt 3",         "https://www.reutersagency.com/feed/"),
    ("Reuters via RSSHub",    "https://rsshub.app/reuters/world"),
    ("Reuters via feed43",    "https://feed43.com/reuters.xml"),
    ("Reuters Politics",      "https://feeds.reuters.com/Reuters/PoliticsNews"),
    ("Reuters Markets",       "https://feeds.reuters.com/reuters/USmarketsnews"),
]

print("Testing Reuters RSS feed URLs...\n")
ok = []
for name, url in urls:
    try:
        feed = feedparser.parse(url)
        if feed.entries and not feed.bozo:
            title = feed.entries[0].get("title", "")[:55]
            ok.append((name, len(feed.entries), url))
            print(f"  OK    {name}: {len(feed.entries)} articles")
            print(f"        Sample: {title}")
        else:
            print(f"  EMPTY {name}: bozo={feed.bozo} status={feed.get('status','?')}")
    except Exception as e:
        print(f"  ERR   {name}: {str(e)[:60]}")

print(f"\n{'='*50}")
if ok:
    print(f"WORKING REUTERS FEEDS: {len(ok)}")
    for name, count, url in ok:
        print(f"  {name}: {count} articles")
        print(f"  URL: {url}")
else:
    print("NO WORKING REUTERS RSS FOUND")
    print("\nReuters has been progressively blocking RSS since 2020.")
    print("Suggested alternatives with similar financial news coverage:")
    print("  - Associated Press: https://feeds.apnews.com/rss/apf-business")
    print("  - Bloomberg via Quicktake: check manually")
    print("  - Yahoo Finance RSS: https://finance.yahoo.com/news/rssindex")
