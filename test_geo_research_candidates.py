import feedparser

sources = [
    ("Global Voices",        "https://globalvoices.org/feed/"),
    ("Crisis Group",         "https://www.crisisgroup.org/rss.xml"),
    ("Crisis Group alt",     "https://www.crisisgroup.org/feed"),
    ("Bellingcat",           "https://www.bellingcat.com/feed/"),
    ("Bellingcat alt",       "https://feeds.feedburner.com/bellingcat"),
    ("openDemocracy",        "https://www.opendemocracy.net/en/rss.xml"),
    ("Just Security",        "https://www.justsecurity.org/feed/"),
    ("The New Humanitarian", "https://www.thenewhumanitarian.org/rss.xml"),
]

print("Testing Geo research candidates...\n")
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
            print(f"  EMPTY {name}: 0 articles (bozo={feed.bozo})")
    except Exception as e:
        print(f"  ERR   {name}: {str(e)[:60]}")

print(f"\nWORKING: {len(ok)}")
for name, count, url in ok:
    print(f"  {name}: {count} articles -- {url}")
