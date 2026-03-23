import feedparser

sources = [
    ("AP Business",          "https://feeds.apnews.com/rss/apf-business"),
    ("AP Top News",          "https://feeds.apnews.com/rss/apf-topnews"),
    ("AP Finance",           "https://feeds.apnews.com/rss/apf-economy"),
    ("Yahoo Finance",        "https://finance.yahoo.com/news/rssindex"),
    ("The Economist",        "https://www.economist.com/finance-and-economics/rss.xml"),
    ("Economist World",      "https://www.economist.com/the-world-this-week/rss.xml"),
    ("Project Syndicate",    "https://www.project-syndicate.org/rss"),
    ("IMF Blog",             "https://www.imf.org/en/Blogs/rss"),
    ("World Bank Blog",      "https://blogs.worldbank.org/rss"),
    ("Seeking Alpha",        "https://seekingalpha.com/feed.xml"),
    ("Quartz",               "https://qz.com/feed"),
    ("The Balance",          "https://www.thebalancemoney.com/rss-news-4487456"),
]

print("Testing Financial pillar Reuters replacement candidates...\n")
ok = []
for name, url in sources:
    try:
        feed = feedparser.parse(url)
        if feed.entries and not feed.bozo:
            title = feed.entries[0].get("title", "")[:55]
            count = len(feed.entries)
            ok.append((name, count, url))
            print(f"  OK    {name}: {count} articles")
            print(f"        Sample: {title}")
        else:
            print(f"  EMPTY {name}: bozo={feed.bozo} status={feed.get('status','?')}")
    except Exception as e:
        print(f"  ERR   {name}: {str(e)[:60]}")

print(f"\n{'='*50}")
print(f"WORKING: {len(ok)}")
for name, count, url in ok:
    print(f"  {name}: {count} articles")
